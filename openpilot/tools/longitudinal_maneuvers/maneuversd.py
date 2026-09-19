#!/usr/bin/env python3
import numpy as np
from dataclasses import dataclass

from opendbc.car.gm.brake_characterization import (
  BRAKE_TEST_MIN, BRAKE_TEST_MAX, BRAKE_TEST_MIN_SPEED, BRAKE_TEST_MAX_SPEED, brake_test_enabled,
)
from openpilot.common.constants import CV
from openpilot.common.realtime import DT_MDL
from openpilot.selfdrive.controls.lib.drive_helpers import should_stop

RECOVERY_SPEED = 3. * CV.MPH_TO_MS


@dataclass
class Action:
  accel_bp: list[float]  # m/s^2
  time_bp: list[float]   # seconds

  def __post_init__(self):
    assert len(self.accel_bp) == len(self.time_bp)


@dataclass
class Maneuver:
  description: str
  actions: list[Action]
  repeat: int = 0
  initial_speed: float = 0.  # m/s

  _interrupted: bool = False
  _active: bool = False
  _finished: bool = False
  _run_completed: bool = False
  _action_index: int = 0
  _action_frames: int = 0
  _ready_cnt: int = 0
  _repeated: int = 0
  _setup_started: bool = False
  _recovering: bool = False

  @property
  def setup_speed(self):
    return self.initial_speed

  def _speed_control(self, v_ego, target, cruise_standstill, duration):
    ready = abs(v_ego - target) < 0.1 and not cruise_standstill
    self._ready_cnt = self._ready_cnt + 1 if ready else 0
    return float(np.clip(target - v_ego, -0.5, 0.75)), self._ready_cnt * DT_MDL >= duration

  def _setup(self, v_ego, cruise_standstill):
    self._setup_started = True
    accel, ready = self._speed_control(v_ego, self.setup_speed, cruise_standstill, 2.)
    if ready:
      self._active = True
      self._interrupted = False
      self._ready_cnt = 0
    return accel

  def _recover(self, v_ego, cruise_standstill):
    accel, ready = self._speed_control(v_ego, RECOVERY_SPEED, cruise_standstill, 3.)
    if ready:
      self._run_completed = True
      if self._repeated < self.repeat:
        self._repeated += 1
        self.reset()
      else:
        self._recovering = False
        self._finished = True
    return accel

  def _step(self) -> float:
    self._run_completed = False
    action = self.actions[self._action_index]
    action_accel = np.interp(self._action_frames * DT_MDL, action.time_bp, action.accel_bp)

    self._action_frames += 1

    # reached duration of action
    if self._action_frames > (action.time_bp[-1] / DT_MDL):
      # next action
      if self._action_index < len(self.actions) - 1:
        self._action_index += 1
        self._action_frames = 0
      else:
        self._active = False
        self._recovering = True
        self._ready_cnt = 0

    return float(action_accel)

  def get_accel(self, v_ego: float, long_active: bool, standstill: bool, cruise_standstill: bool, gas_pressed: bool = False, /) -> float:
    self._run_completed = False
    if self.finished:
      return 0.
    if not long_active:
      if not self._recovering and (self._active or self._setup_started or self._ready_cnt):
        self.reset()
        self._interrupted = True
      self._ready_cnt = 0
      return 0.

    if self._recovering:
      return self._recover(v_ego, cruise_standstill)
    if not self._active:
      return self._setup(v_ego, cruise_standstill)
    return self._step()

  def reset(self):
    self._active = False
    self._action_frames = 0
    self._action_index = 0
    self._ready_cnt = 0
    self._setup_started = False
    self._recovering = False

  @property
  def finished(self):
    return self._finished

  @property
  def active(self):
    return self._active


@dataclass
class StopManeuver(Maneuver):
  stop_accel: float = -0.5
  timeout: float = 20.
  hold_time: float = 3.
  # Creep pulses: once standstill is reached, drop stopping intent for pulse_off_time with a small positive
  # target and the stop flag off, the way the e2e model flaps at a no-lead stop (2026-09-12 route 40:
  # 0.05-0.4 s pulses, desiredAccel -0.08..+0.08, speeds[0] 0.2). The hold timer only runs after the last pulse.
  creep_pulses: int = 0
  pulse_off_time: float = 0.3   # s
  pulse_period: float = 1.5     # s between pulse starts
  pulse_accel: float = 0.05     # m/s^2 target during a pulse
  pulse_start: float = 1.0      # s of standstill before the first pulse
  _elapsed_frames: int = 0
  _hold_frames: int = 0
  _holding_frames: int = 0
  _holding: bool = False
  _pulse_active: bool = False
  _failed: bool = False
  _complete: bool = False

  @property
  def stopping_intent(self):
    return (self._holding and not self._pulse_active) or self._failed or self._complete

  @property
  def pulse_active(self):
    return self._pulse_active

  def _pulse_state(self, t):
    """(in a pulse now, all pulses finished) for t seconds since standstill was first reached."""
    if self.creep_pulses <= 0:
      return False, True
    in_pulse = any(s <= t < s + self.pulse_off_time
                   for s in (self.pulse_start + k * self.pulse_period for k in range(self.creep_pulses)))
    done = t >= self.pulse_start + (self.creep_pulses - 1) * self.pulse_period + self.pulse_off_time
    return in_pulse, done

  def reset(self):
    super().reset()
    self._elapsed_frames = 0
    self._hold_frames = 0
    self._holding_frames = 0
    self._holding = False
    self._pulse_active = False
    self._failed = False
    self._complete = False

  def get_accel(self, v_ego: float, long_active: bool, standstill: bool, cruise_standstill: bool, gas_pressed: bool = False, /) -> float:
    self._run_completed = False
    # A completed hold waits for driver acknowledgement before returning to 3 mph.
    # Gas can override longActive, so latch acknowledgement before checking it.
    if self._complete and (gas_pressed or not long_active):
      self.reset()
      self._recovering = True
    if self._recovering or self.finished:
      return super().get_accel(v_ego, long_active, standstill, cruise_standstill, gas_pressed)
    if not long_active:
      if self._active or self._failed or self._setup_started or self._ready_cnt:
        self._interrupted = True
      self.reset()
      return 0.

    if self._holding or self._failed or self._complete:
      if self._holding and not self._complete and not self._failed:
        self._elapsed_frames += 1
        self._holding_frames += 1
        self._pulse_active, pulses_done = self._pulse_state(self._holding_frames * DT_MDL)
        if self._pulse_active:
          self._hold_frames = 0
          return self.pulse_accel
        self._hold_frames = self._hold_frames + 1 if pulses_done and standstill and abs(v_ego) < 0.1 else 0
        if self._hold_frames * DT_MDL >= self.hold_time:
          self._complete = True
        elif self._elapsed_frames * DT_MDL >= self.timeout:
          self._failed = True
      return self.stop_accel

    if not self._active:
      return self._setup(v_ego, cruise_standstill)

    self._elapsed_frames += 1
    if standstill and abs(v_ego) < 0.1:
      self._holding = True
      self._hold_frames = 0
    elif self._elapsed_frames * DT_MDL >= self.timeout:
      self._failed = True
    return self.stop_accel


@dataclass
class MovingCreepManeuver(Maneuver):
  """Start timed commands on a speed crossing, without requiring stable creep."""
  creep_speed: float = 1.0  # m/s, start on the downward crossing with room before standstill
  acquisition_timeout: float = 20.
  min_speed: float = 0.4
  max_speed: float = 1.5
  _creep_setup: bool = False
  _acquisition_frames: int = 0
  _failure: str = ''
  _run_failed: bool = False

  @property
  def setup_speed(self):
    return self.creep_speed if self._creep_setup else super().setup_speed

  @property
  def stopping_intent(self):
    return bool(self._failure) and not self._recovering and not self.finished

  def _setup(self, v_ego, cruise_standstill):
    if self._creep_setup:
      # A fixed gentle approach exposes poor creep tracking instead of gating on it.
      if v_ego <= self.creep_speed:
        self._active = True
        self._interrupted = False
      return -0.15
    accel = super()._setup(v_ego, cruise_standstill)
    if self._active and not self._creep_setup:
      # Settle at 3 mph, then brake toward the entry speed.
      self._active = False
      self._creep_setup = True
    return accel

  def get_accel(self, v_ego, long_active, standstill, cruise_standstill, gas_pressed=False, /):
    self._run_completed = False
    self._run_failed = False
    if self.stopping_intent and (gas_pressed or not long_active):
      self._recovering = True
      self._ready_cnt = 0
    if long_active and self._creep_setup and not self._recovering and not self.finished:
      if not self._failure:
        if standstill or cruise_standstill or v_ego < self.min_speed:
          self._failure = 'lost moving crawl'
        elif v_ego > self.max_speed:
          self._failure = 'above creep speed range'
        elif not self._active:
          self._acquisition_frames += 1
          if self._acquisition_frames * DT_MDL >= self.acquisition_timeout:
            self._failure = 'crawl setup timed out'
      if self._failure:
        # Do not let an unintended stop turn into a successful timed crawl trial.
        # Wait for acknowledgement before recovering and advancing this failed attempt.
        self._active = False
        return -0.3
    return super().get_accel(v_ego, long_active, standstill, cruise_standstill, gas_pressed)

  def _recover(self, v_ego, cruise_standstill):
    failure = self._failure
    accel = super()._recover(v_ego, cruise_standstill)
    # Repetition reset clears _failure; preserve the outcome for this frame's log.
    self._run_failed = self._run_completed and bool(failure)
    return accel

  def reset(self):
    super().reset()
    self._creep_setup = False
    self._acquisition_frames = 0
    self._failure = ''
    self._run_failed = False


@dataclass
class CreepSpeedManeuver(MovingCreepManeuver):
  """Timed speed ramps through normal longitudinal control; no creep settling gate."""
  speed_points: tuple[float, ...] = ()  # m/s
  time_points: tuple[float, ...] = ()   # seconds from measurement start
  min_speed: float = 0.1               # guard below the lowest 0.5 mph target
  max_speed: float = 1.8
  _measured_speed: float = 0.
  _target_speed: float = RECOVERY_SPEED

  def __post_init__(self):
    assert len(self.speed_points) == len(self.time_points) >= 2
    assert self.time_points[0] == 0.
    assert all(np.isfinite(t) for t in self.time_points)
    assert all(b > a for a, b in zip(self.time_points[:-1], self.time_points[1:], strict=True))
    assert all(self.min_speed < v < self.max_speed for v in self.speed_points)
    assert self.speed_points[0] == self.initial_speed and self.speed_points[-1] == RECOVERY_SPEED

  @property
  def target_speed(self):
    return self._target_speed if self.active else RECOVERY_SPEED

  def reference(self, elapsed):
    i = int(np.clip(np.searchsorted(self.time_points, elapsed, side='right') - 1, 0, len(self.time_points) - 2))
    speed = float(np.interp(elapsed, self.time_points, self.speed_points))
    accel = ((self.speed_points[i + 1] - self.speed_points[i]) / (self.time_points[i + 1] - self.time_points[i])
             if elapsed < self.time_points[-1] else 0.)
    return speed, accel

  def _setup(self, v_ego, cruise_standstill):
    # Begin the timed descent immediately after the standard 3 mph setup.
    accel = Maneuver._setup(self, v_ego, cruise_standstill)
    if self.active:
      self._creep_setup = True
    return accel

  def _step(self):
    elapsed = self._action_frames * DT_MDL
    self._target_speed, feedforward = self.reference(elapsed)
    # Test trajectory tracking only: leave the production acceleration PI unchanged.
    accel = float(np.clip(feedforward + 0.5 * (self._target_speed - self._measured_speed), -0.3, 0.3))
    self._action_frames += 1
    if elapsed >= self.time_points[-1]:
      self._active = False
      self._recovering = True
      self._ready_cnt = 0
    return accel

  def get_accel(self, v_ego, long_active, standstill, cruise_standstill, gas_pressed=False, /):
    self._measured_speed = v_ego
    # Some gas overrides leave longActive asserted; interrupt instead of advancing the profile.
    return super().get_accel(v_ego, long_active and not gas_pressed, standstill, cruise_standstill, gas_pressed)

  def reset(self):
    super().reset()
    self._measured_speed = 0.
    self._target_speed = self.initial_speed


def creep_speed_maneuvers():
  maneuvers = []
  for cycling in (False, True):
    for low in (1.5, 1., 0.5):
      legs = [(low, 6.), (3., 3.)] if not cycling else [(low, 5.), (2., 4.), (low, 5.), (2., 4.), (low, 5.), (3., 3.)]
      speeds, times = [RECOVERY_SPEED], [0.]
      for mph, hold in legs:
        speed = mph * CV.MPH_TO_MS
        # Constant 0.10 m/s² reference ramps; tracking correction is separately bounded.
        arrival = times[-1] + abs(speed - speeds[-1]) / 0.1
        times.extend((arrival, arrival + hold))
        speeds.extend((speed, speed))
      sequence = ' → '.join(['3', *(f'{mph:g}' for mph, _ in legs)])
      description = f"creep speed: C{len(maneuvers) + 1:02d}, {sequence} mph"
      maneuvers.append(CreepSpeedManeuver(description, [], repeat=1, initial_speed=RECOVERY_SPEED,
                                         speed_points=tuple(speeds), time_points=tuple(times)))
  return maneuvers


def maneuver_should_stop(maneuver, v_ego, accel):
  explicit_stop = isinstance(maneuver, (StopManeuver, MovingCreepManeuver, BrakeCharacterizationManeuver)) and maneuver.stopping_intent
  pulse = isinstance(maneuver, StopManeuver) and maneuver.pulse_active
  moving_test = (isinstance(maneuver, MovingCreepManeuver) and maneuver._creep_setup and
                 not maneuver._recovering and not maneuver.finished)
  # Bypass the speed/acceleration heuristic only while a moving test owns stop intent.
  # Its speed and standstill guards can still request a stop at any target acceleration.
  return explicit_stop or (should_stop(v_ego, accel) and not pulse and not moving_test)


@dataclass
class BrakeCharacterizationManeuver(Maneuver):
  """EBCM demand ramp, target hold, and optional descending release holds."""
  start_counts: float = 0.
  max_counts: float = BRAKE_TEST_MAX
  counts_per_second: float = 0.25
  baseline_seconds: float = 2.
  hold_seconds: float = 2.
  release_counts: tuple[float, ...] = ()
  release_hold_seconds: float = 5.
  release_final_hold_seconds: float | None = None
  inactive_brake_after: float | None = None  # seconds after the start of the zero-demand hold
  _test_frames: int = 0
  _brake_counts: float = 0.
  _brake_release: bool = False
  _end_reason: str = ''
  _awaiting_ack: bool = False

  def __post_init__(self):
    assert 0. <= self.max_counts <= BRAKE_TEST_MAX and self.max_counts == int(self.max_counts)
    assert 0. <= self.start_counts <= self.max_counts and self.start_counts == int(self.start_counts)
    assert 0. < self.counts_per_second <= 0.5
    assert self.baseline_seconds >= 0. and self.hold_seconds >= 0.
    assert self.release_hold_seconds > 0.
    assert self.release_final_hold_seconds is None or (self.release_counts and self.release_final_hold_seconds > 0.)
    assert all(0. <= level < previous and level == int(level)
               for previous, level in zip((self.max_counts, *self.release_counts[:-1]), self.release_counts, strict=False))
    if self.inactive_brake_after is not None:
      assert self.release_counts == (0.,)
      zero_hold = self.release_final_hold_seconds if self.release_final_hold_seconds is not None else self.release_hold_seconds
      assert 0. <= self.inactive_brake_after < zero_hold
    assert self.duration <= 90.
    self._brake_counts = self.start_counts

  @property
  def duration(self):
    release_duration = len(self.release_counts) * self.release_hold_seconds
    if self.release_counts and self.release_final_hold_seconds is not None:
      release_duration += self.release_final_hold_seconds - self.release_hold_seconds
    return self.baseline_seconds + (self.max_counts - self.start_counts) / self.counts_per_second + self.hold_seconds + release_duration

  @property
  def stopping_intent(self):
    return self._awaiting_ack

  @property
  def brake_test_active(self):
    return self.active and not self._awaiting_ack and not self._recovering

  @property
  def brake_counts(self):
    return self._brake_counts if self.brake_test_active else 0.

  @property
  def brake_release(self):
    return self.brake_test_active and self._brake_release

  def _end(self, reason):
    self._active = False
    self._awaiting_ack = True
    self._end_reason = reason
    self._brake_counts = 0.
    return -0.3

  def _step(self):
    elapsed = self._test_frames * DT_MDL
    self._test_frames += 1
    if elapsed >= self.duration:
      return self._end('profile complete')
    release_start = self.baseline_seconds + (self.max_counts - self.start_counts) / self.counts_per_second + self.hold_seconds
    if self.release_counts and elapsed >= release_start:
      index = min(int((elapsed - release_start) / self.release_hold_seconds), len(self.release_counts) - 1)
      self._brake_counts = float(self.release_counts[index])
    else:
      self._brake_counts = float(np.clip(self.start_counts + (elapsed - self.baseline_seconds) * self.counts_per_second,
                                        self.start_counts, self.max_counts))
    self._brake_release = (self.inactive_brake_after is not None and
                           elapsed >= release_start + self.inactive_brake_after)
    return 0.  # No acceleration target during direct actuator characterization.

  def get_accel(self, v_ego, long_active, standstill, cruise_standstill, gas_pressed=False, /):
    self._run_completed = False
    if self._awaiting_ack:
      if gas_pressed or not long_active:
        self._awaiting_ack = False
        self._recovering = True
        self._ready_cnt = 0
      else:
        return -0.3
    long_active = long_active and not gas_pressed
    if long_active and self.active:
      if standstill or cruise_standstill or v_ego <= BRAKE_TEST_MIN_SPEED:
        return self._end('lower speed bound')
      if v_ego >= BRAKE_TEST_MAX_SPEED:
        return self._end('upper speed bound')
    return super().get_accel(v_ego, long_active, standstill, cruise_standstill, gas_pressed)

  def reset(self):
    super().reset()
    self._test_frames = 0
    self._brake_counts = self.start_counts
    self._brake_release = False
    self._end_reason = ''
    self._awaiting_ack = False


@dataclass
class SignedBrakeManeuver(BrakeCharacterizationManeuver):
  """Timed signed EBCM acceleration requests, staying in ordinary mode 0xA."""
  request_steps: tuple[tuple[float, float], ...] = ((-15., 4.), (0., 3.), (15., 4.), (0., 4.))

  def __post_init__(self):
    assert self.request_steps
    assert all(np.isfinite(request) and -BRAKE_TEST_MAX <= request <= -BRAKE_TEST_MIN and request == int(request)
               and np.isfinite(seconds) and seconds >= DT_MDL for request, seconds in self.request_steps)
    assert self.duration <= 90.
    self.start_counts = -self.request_steps[0][0]
    self._brake_counts = self.start_counts

  @property
  def duration(self):
    return sum(seconds for _, seconds in self.request_steps)

  def _step(self):
    elapsed = self._test_frames * DT_MDL
    self._test_frames += 1
    end = 0.
    for request, seconds in self.request_steps:
      end += seconds
      if elapsed < end:
        # Existing brakeTestCommand uses positive-for-braking counts. Preserve
        # that schema convention for old suites/logs; CAN uses the opposite sign.
        self._brake_counts = -request
        self._brake_release = False
        return 0.
    return self._end('profile complete')



@dataclass
class CreepSignedBrakeManeuver(SignedBrakeManeuver):
  """Ramp braking to a speed crossing, then run timed signed requests."""
  creep_speed: float = 1.5 * CV.MPH_TO_MS
  start_counts: float = 5.
  counts_per_second: float = 1.
  acquisition_timeout: float = 20.
  _acquisition_frames: int = 0
  _target_reached: bool = False
  _measured_speed: float = RECOVERY_SPEED

  def __post_init__(self):
    start_counts = self.start_counts
    super().__post_init__()
    assert BRAKE_TEST_MIN_SPEED < self.creep_speed < self.initial_speed < BRAKE_TEST_MAX_SPEED
    assert 0. <= start_counts <= self.max_counts <= BRAKE_TEST_MAX
    assert 0. < self.counts_per_second <= 1.
    assert 0. < self.acquisition_timeout <= 30.
    self.start_counts = start_counts
    self._brake_counts = start_counts

  @property
  def duration(self):
    return self.acquisition_timeout + super().duration

  def _step(self):
    if not self._target_reached:
      if self._measured_speed <= self.creep_speed:
        self._target_reached = True
      else:
        elapsed = self._acquisition_frames * DT_MDL
        if elapsed >= self.acquisition_timeout:
          return self._end('creep speed not reached')
        self._acquisition_frames += 1
        self._brake_counts = min(self.start_counts + elapsed * self.counts_per_second, self.max_counts)
        return 0.
    return super()._step()

  def get_accel(self, v_ego, long_active, standstill, cruise_standstill, gas_pressed=False, /):
    self._measured_speed = v_ego
    return super().get_accel(v_ego, long_active, standstill, cruise_standstill, gas_pressed)

  def reset(self):
    super().reset()
    self._acquisition_frames = 0
    self._target_reached = False
    self._measured_speed = self.initial_speed


def signed_brake_maneuvers():
  maneuvers = []
  for index, level in enumerate((3., 6., 10., 15., 20., 200.), 1):
    requests = ((0., 1.), (level, 4.), (0., 4.))
    description = f'brake characterization: C{index:02d}, signed 0xA: ramp -5 to -20 at 1 count/s until 1.5 mph; '
    description += f'0 (1s) -> +{level:g} (4s) -> 0 (4s)'
    maneuvers.append(CreepSignedBrakeManeuver(description, [], repeat=1, initial_speed=RECOVERY_SPEED,
                                              request_steps=requests))
  return maneuvers


def fixed_signed_brake_maneuvers():
  # Short application holds leave speed available for the positive-request phase.
  levels = (15., 18., 20.)
  maneuvers = []
  for index, level in enumerate(levels, 1):
    requests = ((-5., 2.), (-level, 4.), (0., 3.), (level, 4.), (0., 4.))
    label = ' -> '.join(f'{request:+g} ({seconds:g}s)' for request, seconds in requests)
    maneuvers.append(SignedBrakeManeuver(f'brake characterization: S{index:02d}, signed 0xA: {label}', [],
                                         repeat=1, initial_speed=RECOVERY_SPEED, request_steps=requests))
  return maneuvers


def brake_hold_maneuvers(levels):
  # Each peak gets a fresh 3 mph start, then descending holds to measure release.
  maneuvers = []
  for level in levels:
    assert 0. <= level <= BRAKE_TEST_MAX and level == int(level)
    release_counts = tuple(float(count) for count in range(int(level) - 1, 9, -1))
    release_description = " -> ".join(f"{count:g}" for count in release_counts)
    description = f"brake characterization: mode 0xA hold {level:g} counts for 5s"
    if release_counts:
      description += f"; release {release_description} (5s each)"
    maneuvers.append(BrakeCharacterizationManeuver(description, [], repeat=2, initial_speed=3. * CV.MPH_TO_MS,
                                                 start_counts=min(5., level), max_counts=level, counts_per_second=0.5,
                                                 hold_seconds=5., release_counts=release_counts))
  return maneuvers


def brake_release_maneuvers():
  # Direct releases first: they are most likely to finish before the low-speed guard.
  # Entries are (peak count, exact-peak hold seconds, descending levels, seconds per step).
  profiles = [
    (12., 4., (0.,), 8.),
    (12., 4., (5.,), 8.),
    (12., 4., (8.,), 8.),
    (13., 3., (0.,), 8.),
    (13., 3., (5.,), 8.),
    (13., 3., (8.,), 8.),
    (12., 4., (2.,), 8.),
    (12., 4., (10.,), 8.),
    (12., 2., (0.,), 8.),
    (12., 2., (5.,), 8.),
    (12., 4., (10., 8., 6., 4., 2., 0.), 1.5),
    (12., 4., tuple(float(count) for count in range(11, -1, -1)), 1.5),
  ]
  maneuvers = []
  for index, (peak, hold, releases, step_seconds) in enumerate(profiles, 1):
    release_label = f"drop to {releases[0]:g} for 8s" if len(releases) == 1 else (
      f"step -{peak - releases[0]:g} every {step_seconds:g}s to 0; hold 8s")
    description = f"brake characterization: R{index:02d} mode 0xA, {peak:g} counts {hold:g}s; {release_label}"
    maneuvers.append(BrakeCharacterizationManeuver(description, [], repeat=1, initial_speed=3. * CV.MPH_TO_MS,
                                                 start_counts=5., max_counts=peak, counts_per_second=0.5,
                                                 hold_seconds=hold, release_counts=releases, release_hold_seconds=step_seconds,
                                                 release_final_hold_seconds=8.))
  return maneuvers


def brake_exit_maneuvers():
  # Mode is selected by the existing CAN helper; inactive release is legal only at zero demand.
  maneuvers = []
  for peak, hold in ((12., 4.), (13., 3.)):
    for inactive_after, release_label in (
      (None, "0 in 0xA for 8s"),
      (0., "0 in 0x1 for 8s"),
      (2., "0 in 0xA 2s, then 0x1 8s"),
    ):
      description = f"brake characterization: E{len(maneuvers) + 1:02d}, {peak:g} counts {hold:g}s; {release_label}"
      maneuvers.append(BrakeCharacterizationManeuver(description, [], repeat=1, initial_speed=3. * CV.MPH_TO_MS,
                                                   start_counts=5., max_counts=peak, counts_per_second=0.5, hold_seconds=hold,
                                                   release_counts=(0.,), release_hold_seconds=8. + (inactive_after or 0.),
                                                   inactive_brake_after=inactive_after))
  return maneuvers


# Original creep suite: 8 scenarios, each run twice. Settle at 3 mph for two
# seconds before each test, then recover to 3 mph after the test.
LOW_SPEED_MANEUVERS = [
  StopManeuver(
    f"creep stop and hold: {accel:g}m/s^2 from 3mph",
    [], repeat=1, initial_speed=3. * CV.MPH_TO_MS, stop_accel=accel,
  )
  for accel in (-0.15, -0.3, -0.5)
] + [
  StopManeuver(
    f"creep pulses: 3 x {duration:g}s at +{accel:g}m/s^2",
    [], repeat=1, initial_speed=3. * CV.MPH_TO_MS, stop_accel=-0.3,
    timeout=30., creep_pulses=3, pulse_off_time=duration, pulse_accel=accel,
  )
  for duration, accel in ((0.1, 0.05), (0.3, 0.05), (0.4, 0.08))
] + [
  Maneuver(
    "creep crawl: coast, gentle stop, release",
    [Action([-0.4], [2.]), Action([0.], [4.]), Action([-0.15], [4.]), Action([0.], [2.])],
    repeat=1, initial_speed=3. * CV.MPH_TO_MS,
  ),
  Maneuver(
    "creep feather: brake, coast, accelerate",
    [Action([-0.3], [2.]), Action([-0.15], [2.]), Action([0.], [3.]), Action([0.15], [2.]), Action([0.], [3.])],
    repeat=1, initial_speed=3. * CV.MPH_TO_MS,
  ),
]
# Append transition trials; keep the original 16 runs unchanged for route comparisons.
MOVING_CREEP_MANEUVERS = [
  MovingCreepManeuver("moving creep: brake then zero accel for 6s", [
    Action([-0.15], [0.5]), Action([0.], [6.]),
  ], repeat=1, initial_speed=3. * CV.MPH_TO_MS),
  MovingCreepManeuver("moving creep: small steps then torque handoff", [
    Action([-0.15], [0.5]), Action([0.], [1.]),
    Action([0.05], [1.]), Action([-0.05], [1.]),
    Action([0.15], [1.]), Action([-0.05], [1.]),
    Action([0.3], [0.75]), Action([-0.15], [0.75]), Action([0.], [1.]),
  ], repeat=1, initial_speed=3. * CV.MPH_TO_MS),
  MovingCreepManeuver("moving creep: brake to torque ramp and back", [
    Action([-0.15], [0.5]), Action([-0.15, 0.3, -0.15], [0., 2., 4.]), Action([0.], [2.]),
  ], repeat=1, initial_speed=3. * CV.MPH_TO_MS),
]
STANDARD_MANEUVERS = LOW_SPEED_MANEUVERS + MOVING_CREEP_MANEUVERS
BRAKE_SWEEP_MANEUVERS = [
  BrakeCharacterizationManeuver("brake characterization: mode 0xA, 5 to 20 counts at 0.25 count/s", [],
                               repeat=2, initial_speed=3. * CV.MPH_TO_MS, start_counts=5.),
]
BRAKE_HOLD_MANEUVERS = brake_hold_maneuvers([11., 12., 13.])
BRAKE_RELEASE_MANEUVERS = brake_release_maneuvers()
# Active zero retained pressure. Compare releasing the brake-active request at zero.
BRAKE_CHARACTERIZATION_MANEUVERS = brake_exit_maneuvers()
CREEP_SPEED_MANEUVERS = creep_speed_maneuvers()
FIXED_SIGNED_BRAKE_MANEUVERS = fixed_signed_brake_maneuvers()
SIGNED_BRAKE_MANEUVERS = signed_brake_maneuvers()
MANEUVERS = SIGNED_BRAKE_MANEUVERS


def main():
  from openpilot.cereal import messaging, custom
  from opendbc.car import structs
  from openpilot.common.params import Params
  from openpilot.common.swaglog import cloudlog

  params = Params()
  cloudlog.info("maneuversd is waiting for CarParams")
  CP = messaging.log_from_bytes(params.get("CarParams", block=True), structs.CarParams)
  CP_SP = messaging.log_from_bytes(params.get("CarParamsSP", block=True), custom.CarParamsSP)

  sm = messaging.SubMaster(['carState', 'carControl', 'carOutput', 'controlsState', 'selfdriveState', 'modelV2'], poll='modelV2')
  pm = messaging.PubMaster(['longitudinalPlan', 'longitudinalPlanSP', 'driverAssistance', 'alertDebug'])

  maneuvers = iter(MANEUVERS if brake_test_enabled(CP, CP_SP) else STANDARD_MANEUVERS)
  maneuver = None
  previous_status = None

  while True:
    sm.update()

    if maneuver is None:
      maneuver = next(maneuvers, None)

    alert_msg = messaging.new_message('alertDebug')
    alert_msg.valid = True

    plan_send = messaging.new_message('longitudinalPlan')
    plan_send.valid = sm.all_checks()

    longitudinalPlan = plan_send.longitudinalPlan
    accel = 0
    v_ego = max(sm['carState'].vEgo, 0)

    if maneuver is not None:
      run_number = maneuver._repeated + 1
      if (isinstance(maneuver, BrakeCharacterizationManeuver) and maneuver.active and
          sm['carControl'].longActive and sm['carControl'].brakeTestActive and
          sm['carOutput'].actuatorsOutput.longControlState == structs.CarControl.Actuators.LongControlState.stopping):
        maneuver._end('controller stopped test')
      accel = maneuver.get_accel(v_ego, sm['carControl'].longActive, sm['carState'].standstill,
                                 sm['carState'].cruiseState.standstill, sm['carState'].gasPressed)

      if isinstance(maneuver, BrakeCharacterizationManeuver) and maneuver.stopping_intent:
        alert_msg.alertDebug.alertText1 = f'Brake test ended: {maneuver._end_reason}; tap throttle or disengage'
      elif isinstance(maneuver, BrakeCharacterizationManeuver) and maneuver.brake_test_active:
        mode = '0x1' if maneuver.brake_release else '0xA'
        alert_msg.alertDebug.alertText1 = f'Maneuver Active: EBCM {-maneuver.brake_counts:+.1f} counts, mode {mode}'
      elif isinstance(maneuver, MovingCreepManeuver) and maneuver.stopping_intent:
        alert_msg.alertDebug.alertText1 = f'Creep test invalid: tap throttle or disengage ({maneuver._failure})'
      elif isinstance(maneuver, StopManeuver) and maneuver._failed:
        alert_msg.alertDebug.alertText1 = 'Stop timed out: take control'
      elif isinstance(maneuver, StopManeuver) and maneuver._complete:
        alert_msg.alertDebug.alertText1 = 'Stop complete: tap throttle'
      elif maneuver._recovering:
        alert_msg.alertDebug.alertText1 = ('Test complete: tap throttle' if sm['carState'].standstill
                                         else f'Recovering to {RECOVERY_SPEED * CV.MS_TO_MPH:.0f} mph')
      elif isinstance(maneuver, StopManeuver) and maneuver.pulse_active:
        alert_msg.alertDebug.alertText1 = f'Maneuver Active: pulse {maneuver.pulse_off_time:0.1f}s'
      elif isinstance(maneuver, StopManeuver) and maneuver._holding:
        alert_msg.alertDebug.alertText1 = 'Maneuver Active: holding stop'
      elif maneuver._interrupted:
        alert_msg.alertDebug.alertText1 = f'Restarting: setup at {maneuver.setup_speed * CV.MS_TO_MPH:.0f} mph'
      elif isinstance(maneuver, MovingCreepManeuver) and maneuver._creep_setup and not maneuver.active:
        alert_msg.alertDebug.alertText1 = f'Setting up: slowing through {maneuver.creep_speed * CV.MS_TO_MPH:.1f} mph'
      elif isinstance(maneuver, CreepSpeedManeuver) and maneuver.active:
        alert_msg.alertDebug.alertText1 = f'Maneuver Active: target {maneuver.target_speed * CV.MS_TO_MPH:.2f} mph; actual {v_ego * CV.MS_TO_MPH:.2f} mph'
      elif maneuver.active:
        alert_msg.alertDebug.alertText1 = f'Maneuver Active: {accel:0.2f} m/s^2'
      else:
        alert_msg.alertDebug.alertText1 = f'Setting up: settle at {maneuver.setup_speed * CV.MS_TO_MPH:.0f} mph'
      alert_msg.alertDebug.alertText1 += f' (run {run_number}/{maneuver.repeat + 1})'
      alert_msg.alertDebug.alertText2 = maneuver.description
      if maneuver._run_completed:
        outcome = 'failed' if isinstance(maneuver, MovingCreepManeuver) and maneuver._run_failed else 'completed'
        cloudlog.info("longitudinal maneuver %s: %s | run %d/%d", outcome, maneuver.description, run_number, maneuver.repeat + 1)
    else:
      alert_msg.alertDebug.alertText1 = 'Maneuvers Finished'

    status = None if maneuver is None else (
      id(maneuver), maneuver._repeated, maneuver.active, maneuver._action_index,
      maneuver._interrupted, maneuver._run_completed, maneuver.finished, maneuver._setup_started, maneuver._recovering,
      isinstance(maneuver, StopManeuver) and (maneuver._holding, maneuver.pulse_active, maneuver._failed, maneuver._complete),
      isinstance(maneuver, MovingCreepManeuver) and (maneuver._creep_setup, maneuver._failure),
      isinstance(maneuver, BrakeCharacterizationManeuver) and (maneuver._awaiting_ack, maneuver._end_reason),
    )
    if status != previous_status:
      cloudlog.info("longitudinal maneuver: %s | %s", alert_msg.alertDebug.alertText1, alert_msg.alertDebug.alertText2)
      previous_status = status
    pm.send('alertDebug', alert_msg)

    longitudinalPlan.aTarget = accel
    if isinstance(maneuver, BrakeCharacterizationManeuver):
      longitudinalPlan.brakeTestActive = maneuver.brake_test_active
      longitudinalPlan.brakeTestCommand = maneuver.brake_counts
      longitudinalPlan.brakeTestRelease = maneuver.brake_release
    stopping_intent = isinstance(maneuver, (StopManeuver, MovingCreepManeuver, BrakeCharacterizationManeuver)) and maneuver.stopping_intent
    longitudinalPlan.shouldStop = maneuver_should_stop(maneuver, v_ego, accel)

    longitudinalPlan.allowBrake = True
    longitudinalPlan.allowThrottle = not stopping_intent
    longitudinalPlan.hasLead = True

    # Suppress automatic resume throughout stop hold, timeout and takeover wait.
    longitudinalPlan.speeds = [0.] if stopping_intent else [0.2]
    if isinstance(maneuver, CreepSpeedManeuver) and not stopping_intent:
      longitudinalPlan.speeds = [maneuver.target_speed]

    pm.send('longitudinalPlan', plan_send)

    plan_sp_send = messaging.new_message('longitudinalPlanSP')
    plan_sp_send.valid = True
    pm.send('longitudinalPlanSP', plan_sp_send)

    assistance_send = messaging.new_message('driverAssistance')
    assistance_send.valid = True
    pm.send('driverAssistance', assistance_send)

    if maneuver is not None and maneuver.finished:
      maneuver = None
