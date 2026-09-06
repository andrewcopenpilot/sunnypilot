#!/usr/bin/env python3
import numpy as np
from dataclasses import dataclass

from openpilot.common.constants import CV
from openpilot.common.realtime import DT_MDL


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
      # repeat maneuver
      elif self._repeated < self.repeat:
        self._repeated += 1
        self._run_completed = True
        self.reset()
      # finish maneuver
      else:
        self._run_completed = True
        self._finished = True

    return float(action_accel)

  def get_accel(self, v_ego: float, long_active: bool, standstill: bool, cruise_standstill: bool, /) -> float:
    self._run_completed = False
    if not long_active:
      if self._active:
        self.reset()
        self._interrupted = True
      self._ready_cnt = 0
      return 0.

    ready = abs(v_ego - self.initial_speed) < 0.3 and long_active and not cruise_standstill
    if self.initial_speed < 0.01:
      ready = ready and standstill
    self._ready_cnt = (self._ready_cnt + 1) if ready else 0

    if self._ready_cnt > (3. / DT_MDL):
      self._active = True
      self._interrupted = False

    if not self._active:
      return min(max(self.initial_speed - v_ego, -2.), 2.)

    return self._step()

  def reset(self):
    self._active = False
    self._action_frames = 0
    self._action_index = 0
    self._ready_cnt = 0

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
  _elapsed_frames: int = 0
  _hold_frames: int = 0
  _holding: bool = False
  _failed: bool = False
  _complete: bool = False
  _armed: bool = False

  @property
  def stopping_intent(self):
    return self._holding or self._failed or self._complete

  def reset(self):
    super().reset()
    self._elapsed_frames = 0
    self._hold_frames = 0
    self._holding = False
    self._failed = False
    self._complete = False

  def get_accel(self, v_ego: float, long_active: bool, standstill: bool, cruise_standstill: bool, /) -> float:
    self._run_completed = False
    # Every stop requires driver disengagement before setup; after the hold we
    # keep stopping intent until takeover, never automatically launch again.
    if not long_active:
      if self._complete:
        self._run_completed = True
        if self._repeated < self.repeat:
          self._repeated += 1
        else:
          self._finished = True
      elif self._active or self._failed:
        self._interrupted = True
      self.reset()
      self._armed = True
      return 0.

    if not self._armed:
      return 0.
    if self.stopping_intent:
      if self._holding and not self._complete and not self._failed:
        self._elapsed_frames += 1
        self._hold_frames = self._hold_frames + 1 if standstill and abs(v_ego) < 0.1 else 0
        if self._hold_frames * DT_MDL >= self.hold_time:
          self._complete = True
        elif self._elapsed_frames * DT_MDL >= self.timeout:
          self._failed = True
      return self.stop_accel

    if not self._active:
      ready = abs(v_ego - self.initial_speed) < 0.3 and not cruise_standstill
      self._ready_cnt = self._ready_cnt + 1 if ready else 0
      if self._ready_cnt * DT_MDL <= 3.:
        return min(max(self.initial_speed - v_ego, -2.), 2.)
      self._active = True
      self._interrupted = False

    self._elapsed_frames += 1
    if standstill and abs(v_ego) < 0.1:
      self._holding = True
      self._hold_frames = 0
    elif self._elapsed_frames * DT_MDL >= self.timeout:
      self._failed = True
    return self.stop_accel


# Volt tuning suite (16 runs). Each step holds long enough to measure steady state,
# the sweep maps the actuator path continuously, the 40 mph runs sit above the
# regen power cap at high charge, the ramp is a planner-shaped request, and one
# stop level exercises the stopping transition.
STEP_HOLD = 5.  # seconds; steady-state metrics are taken after the transient
MANEUVERS = [
  Maneuver(
    f"brake step and release: {accel:g}m/s^2 from 20mph",
    [Action([accel], [STEP_HOLD]), Action([0.], [2])],
    repeat=1,
    initial_speed=20. * CV.MPH_TO_MS,
  )
  for accel in (-0.75, -1.25, -2.)
] + [
  Maneuver(
    "brake ramp and release: 0.5m/s^3 to -1.5m/s^2 from 20mph",
    [Action([0., -1.5], [0., 3.]), Action([-1.5], [2]), Action([0.], [2])],
    repeat=1,
    initial_speed=20. * CV.MPH_TO_MS,
  ),
  Maneuver(
    "brake sweep and release: 0 to -2.5m/s^2 over 10s from 40mph",
    [Action([0., -2.5], [0., 10.]), Action([0.], [2])],
    repeat=1,
    initial_speed=40. * CV.MPH_TO_MS,
  ),
  Maneuver(
    "brake step and release: -1m/s^2 from 40mph",
    [Action([-1.], [4]), Action([0.], [2])],
    repeat=1,
    initial_speed=40. * CV.MPH_TO_MS,
  ),
  Maneuver(
    "brake step and partial release: -1.5 then -0.5m/s^2 from 40mph",
    [Action([-1.5], [3]), Action([-0.5], [3]), Action([0.], [2])],
    repeat=1,
    initial_speed=40. * CV.MPH_TO_MS,
  ),
  StopManeuver(
    "stop and hold: -0.75m/s^2 from 10mph",
    [],
    repeat=1,
    initial_speed=10. * CV.MPH_TO_MS,
    stop_accel=-0.75,
  ),
]

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
      accel = maneuver.get_accel(v_ego, sm['carControl'].longActive, sm['carState'].standstill, sm['carState'].cruiseState.standstill)

      if isinstance(maneuver, StopManeuver) and maneuver._failed:
        alert_msg.alertDebug.alertText1 = 'Stop timed out: take control; retry required'
      elif isinstance(maneuver, StopManeuver) and maneuver._complete:
        alert_msg.alertDebug.alertText1 = 'Stop complete: take control before next run'
      elif isinstance(maneuver, StopManeuver) and not maneuver._armed:
        alert_msg.alertDebug.alertText1 = 'Stop tests: disengage, then engage when ready'
      elif isinstance(maneuver, StopManeuver) and maneuver._holding:
        alert_msg.alertDebug.alertText1 = 'Maneuver Active: holding standstill for 3 seconds'
      elif maneuver._interrupted:
        alert_msg.alertDebug.alertText1 = 'Run interrupted: restarting from setup'
      elif maneuver.active:
        alert_msg.alertDebug.alertText1 = f'Maneuver Active: {accel:0.2f} m/s^2'
      else:
        alert_msg.alertDebug.alertText1 = f'Setting up to {maneuver.initial_speed * CV.MS_TO_MPH:0.2f} mph'
      alert_msg.alertDebug.alertText1 += f' (run {run_number}/{maneuver.repeat + 1})'
      alert_msg.alertDebug.alertText2 = maneuver.description
      if maneuver._run_completed:
        cloudlog.info("longitudinal maneuver completed: %s | run %d/%d", maneuver.description, run_number, maneuver.repeat + 1)
    else:
      alert_msg.alertDebug.alertText1 = 'Maneuvers Finished'

    status = None if maneuver is None else (
      id(maneuver), maneuver._repeated, maneuver.active, maneuver._action_index,
      maneuver._interrupted, maneuver._run_completed, maneuver.finished,
      isinstance(maneuver, StopManeuver) and (maneuver._armed, maneuver._holding, maneuver._failed, maneuver._complete),
    )
    if status != previous_status:
      cloudlog.info("longitudinal maneuver: %s | %s", alert_msg.alertDebug.alertText1, alert_msg.alertDebug.alertText2)
      previous_status = status
    pm.send('alertDebug', alert_msg)

    longitudinalPlan.aTarget = accel
    stopping_intent = isinstance(maneuver, StopManeuver) and maneuver.stopping_intent
    longitudinalPlan.shouldStop = stopping_intent or should_stop(v_ego, accel)

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
