import unittest
from dataclasses import replace
from types import SimpleNamespace

from opendbc.car import structs

from openpilot.common.constants import CV
from openpilot.selfdrive.controls.lib.drive_helpers import should_stop
from openpilot.selfdrive.controls.lib.longcontrol import long_control_state_trans
from openpilot.tools.longitudinal_maneuvers.maneuversd import (
  CREEP_SPEED_MANEUVERS, MANEUVERS, BRAKE_CHARACTERIZATION_MANEUVERS, CreepSpeedManeuver,
  Maneuver, StopManeuver, RECOVERY_SPEED, DT_MDL, maneuver_should_stop,
)


class TestCreepSpeed(unittest.TestCase):
  def start(self, m):
    for _ in range(round(2. / DT_MDL)):
      m.get_accel(RECOVERY_SPEED, True, False, False)
    self.assertTrue(m.active)
    self.assertEqual(m._action_frames, 0)

  def test_default_profiles_and_all_repeats(self):
    self.assertIs(MANEUVERS, CREEP_SPEED_MANEUVERS)
    self.assertEqual(len(MANEUVERS), 6)
    self.assertEqual(sum(m.repeat + 1 for m in MANEUVERS), 12)
    for i, template in enumerate(MANEUVERS):
      self.assertAlmostEqual(min(template.speed_points) * CV.MS_TO_MPH, (1.5, 1., .5)[i % 3])
      m = replace(template)
      # Ideal acceleration-following fixture exercises scheduling, not real vehicle stability.
      v = RECOVERY_SPEED
      completed = 0
      for _ in range(6000):
        accel = m.get_accel(v, True, False, False)
        self.assertFalse(m._failure)
        self.assertFalse(maneuver_should_stop(m, v, accel))
        if m.active:
          self.assertLessEqual(abs(accel), .3)
          self.assertLess(abs(m.target_speed - v), .02)
        v += accel * DT_MDL
        completed += m._run_completed
        if m.finished:
          break
      self.assertTrue(m.finished)
      self.assertEqual(completed, 2)
      self.assertAlmostEqual(v, RECOVERY_SPEED, delta=.02)

  def test_speed_and_feedforward_are_continuous_and_bounded(self):
    for m in MANEUVERS:
      for i, t in enumerate(m.time_points):
        speed, _ = m.reference(t)
        self.assertAlmostEqual(speed, m.speed_points[i])
        before, _ = m.reference(max(0., t - 1e-6))
        after, _ = m.reference(t + 1e-6)
        self.assertAlmostEqual(before, after, places=5)
      for frame in range(int(m.time_points[-1] / DT_MDL) + 2):
        _, accel = m.reference(frame * DT_MDL)
        self.assertLessEqual(abs(accel), .1 + 1e-9)

  def test_profile_keeps_advancing_when_speed_never_reaches_target(self):
    m = replace(MANEUVERS[2])
    self.start(m)
    for _ in range(int(m.time_points[-1] / DT_MDL) + 2):
      m.get_accel(RECOVERY_SPEED, True, False, False)
    self.assertTrue(m._recovering)
    self.assertFalse(m._failure)

  def test_stop_heuristic_bypass_is_limited_to_moving_test(self):
    m = replace(MANEUVERS[2])
    self.assertTrue(should_stop(.2, 0.))
    self.assertTrue(maneuver_should_stop(m, .2, 0.))  # Setup retains normal behavior.
    self.start(m)
    for accel in (-.2, 0., .05):
      m.get_accel(.2, True, False, False)
      self.assertFalse(maneuver_should_stop(m, .2, accel))
    for other in (None, Maneuver('normal', []), StopManeuver('stop', []), replace(BRAKE_CHARACTERIZATION_MANEUVERS[0])):
      self.assertTrue(maneuver_should_stop(other, .2, 0.))
    m._recovering = True
    self.assertTrue(maneuver_should_stop(m, .2, 0.))

  def test_controller_stays_in_pid_until_explicit_test_abort(self):
    m = replace(MANEUVERS[2])
    self.start(m)
    state = structs.CarControl.Actuators.LongControlState.pid
    cp_sp = SimpleNamespace(enableGasInterceptor=False)
    for _ in range(20):
      accel = m.get_accel(.2, True, False, False)
      stop = maneuver_should_stop(m, .2, accel)
      state = long_control_state_trans(cp_sp, True, state, stop, False, False)
      self.assertEqual(state, structs.CarControl.Actuators.LongControlState.pid)
    accel = m.get_accel(.09, True, False, False)
    stop = maneuver_should_stop(m, .09, accel)
    state = long_control_state_trans(cp_sp, True, state, stop, False, False)
    self.assertEqual(state, structs.CarControl.Actuators.LongControlState.stopping)

  def test_guards_override_bypass_and_failure_requires_acknowledgement(self):
    for speed, standstill, cruise in ((.09, False, False), (.2, True, False), (.2, False, True), (1.81, False, False)):
      m = replace(MANEUVERS[2])
      self.start(m)
      self.assertEqual(m.get_accel(speed, True, standstill, cruise), -.3)
      self.assertTrue(m.stopping_intent)
      self.assertTrue(maneuver_should_stop(m, speed, .3))  # Explicit abort wins even over positive accel.
      self.assertFalse(m.active)
      for _ in range(20):
        m.get_accel(1., True, False, False)
        self.assertFalse(m._recovering)
      m.get_accel(0., True, True, True, True)
      self.assertTrue(m._recovering)
      for _ in range(round(3. / DT_MDL)):
        m.get_accel(RECOVERY_SPEED, True, False, False)
      self.assertTrue(m._run_failed)
      self.assertEqual(m._repeated, 1)

  def test_pedal_override_or_disengagement_restarts_profile(self):
    for gas, active in ((True, True), (False, False)):
      m = replace(MANEUVERS[2])
      self.start(m)
      for _ in range(20):
        m.get_accel(1., True, False, False)
      m.get_accel(1., active, False, False, gas)
      self.assertFalse(m.active)
      self.assertTrue(m._interrupted)
      self.assertEqual(m._action_frames, 0)
      self.start(m)
      self.assertEqual(m.target_speed, RECOVERY_SPEED)

  def test_invalid_trajectory_is_rejected(self):
    for speeds, times in (((RECOVERY_SPEED, .2), (0., 1.)),
                          ((RECOVERY_SPEED, RECOVERY_SPEED), (0., 0.)),
                          ((RECOVERY_SPEED, .05, RECOVERY_SPEED), (0., 1., 2.))):
      with self.assertRaises(AssertionError):
        CreepSpeedManeuver('invalid', [], initial_speed=RECOVERY_SPEED, speed_points=speeds, time_points=times)


if __name__ == '__main__':
  unittest.main()
