#!/usr/bin/env python3
import numpy as np
from dataclasses import dataclass

from openpilot.common.constants import CV
from openpilot.common.realtime import DT_MDL

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
        if standstill or cruise_standstill or v_ego < 0.4:
          self._failure = 'lost moving crawl'
        elif v_ego > 1.5:
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
MANEUVERS = STANDARD_MANEUVERS


def main():
  from openpilot.cereal import messaging
  from openpilot.common.params import Params
  from openpilot.common.swaglog import cloudlog
  from openpilot.selfdrive.controls.lib.drive_helpers import should_stop

  params = Params()
  cloudlog.info("maneuversd is waiting for CarParams")
  params.get("CarParams", block=True)

  sm = messaging.SubMaster(['carState', 'carControl', 'controlsState', 'selfdriveState', 'modelV2'], poll='modelV2')
  pm = messaging.PubMaster(['longitudinalPlan', 'longitudinalPlanSP', 'driverAssistance', 'alertDebug'])

  maneuvers = iter(MANEUVERS)
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
      accel = maneuver.get_accel(v_ego, sm['carControl'].longActive, sm['carState'].standstill,
                                 sm['carState'].cruiseState.standstill, sm['carState'].gasPressed)

      if isinstance(maneuver, MovingCreepManeuver) and maneuver.stopping_intent:
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
    )
    if status != previous_status:
      cloudlog.info("longitudinal maneuver: %s | %s", alert_msg.alertDebug.alertText1, alert_msg.alertDebug.alertText2)
      previous_status = status
    pm.send('alertDebug', alert_msg)

    longitudinalPlan.aTarget = accel
    stopping_intent = isinstance(maneuver, (StopManeuver, MovingCreepManeuver)) and maneuver.stopping_intent
    pulse_active = isinstance(maneuver, StopManeuver) and maneuver.pulse_active
    # a creep pulse mimics the model: stop flag off at standstill with a slightly positive target
    longitudinalPlan.shouldStop = stopping_intent or (should_stop(v_ego, accel) and not pulse_active)

    longitudinalPlan.allowBrake = True
    longitudinalPlan.allowThrottle = not stopping_intent
    longitudinalPlan.hasLead = True

    # Suppress automatic resume throughout stop hold, timeout and takeover wait.
    longitudinalPlan.speeds = [0.] if stopping_intent else [0.2]

    pm.send('longitudinalPlan', plan_send)

    plan_sp_send = messaging.new_message('longitudinalPlanSP')
    plan_sp_send.valid = True
    pm.send('longitudinalPlanSP', plan_sp_send)

    assistance_send = messaging.new_message('driverAssistance')
    assistance_send.valid = True
    pm.send('driverAssistance', assistance_send)

    if maneuver is not None and maneuver.finished:
      maneuver = None
