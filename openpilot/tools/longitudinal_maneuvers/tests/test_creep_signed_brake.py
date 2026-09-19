import unittest
from dataclasses import replace

from openpilot.tools.longitudinal_maneuvers.maneuversd import (
  DT_MDL, MANEUVERS, SIGNED_BRAKE_MANEUVERS, RECOVERY_SPEED, maneuver_should_stop,
)


class TestCreepSignedBrake(unittest.TestCase):
  def start(self, m):
    for _ in range(round(2. / DT_MDL)):
      m.get_accel(RECOVERY_SPEED, True, False, False)
    self.assertTrue(m.brake_test_active)

  def test_speed_crossing_then_timed_steps_and_repeats(self):
    self.assertIs(MANEUVERS, SIGNED_BRAKE_MANEUVERS)
    self.assertEqual(len(MANEUVERS), 6)
    self.assertEqual(sum(m.repeat + 1 for m in MANEUVERS), 12)
    for template, level in zip(MANEUVERS, (3., 6., 10., 15., 20., 200.), strict=True):
      m = replace(template)
      self.assertEqual(m.request_steps, ((0., 1.), (level, 4.), (0., 4.)))
      self.assertEqual(m.duration, 29.)
      for repeat in range(2):
        self.start(m)
        # Different acquisition times must not consume any positive hold time.
        for frame in range(40 + repeat * 60):
          m.get_accel(m.creep_speed + 0.1, True, False, False)
          self.assertAlmostEqual(m.brake_counts, 5. + frame * DT_MDL)
          self.assertFalse(m._target_reached)
        # Hold speed fixed: even a positive request with no response must finish on time.
        for signed, seconds in m.request_steps:
          for _ in range(round(seconds / DT_MDL)):
            self.assertEqual(m.get_accel(m.creep_speed, True, False, False), 0.)
            self.assertEqual(-m.brake_counts, signed)
            self.assertFalse(m.brake_release)
            self.assertFalse(maneuver_should_stop(m, m.creep_speed, 0.))
        m.get_accel(m.creep_speed, True, False, False)
        self.assertEqual(m._end_reason, 'profile complete')
        self.assertTrue(m.stopping_intent)
        m.get_accel(0., False, True, True, True)
        for _ in range(round(3. / DT_MDL)):
          m.get_accel(RECOVERY_SPEED, True, False, False)
        self.assertEqual(m.finished, repeat == 1)

  def test_ramp_is_capped_and_times_out_without_positive_request(self):
    m = replace(MANEUVERS[-1])
    self.start(m)
    for frame in range(round(m.acquisition_timeout / DT_MDL)):
      m.get_accel(RECOVERY_SPEED, True, False, False)
      self.assertAlmostEqual(m.brake_counts, min(5. + frame * DT_MDL, 20.))
      self.assertFalse(m._target_reached)
    m.get_accel(RECOVERY_SPEED, True, False, False)
    self.assertEqual(m._end_reason, 'creep speed not reached')
    self.assertFalse(m.brake_test_active)
    self.assertTrue(m.stopping_intent)

  def test_speed_crossing_immediately_ends_ramp(self):
    m = replace(MANEUVERS[0])
    self.start(m)
    m.get_accel(m.creep_speed + 0.01, True, False, False)
    self.assertEqual(m.brake_counts, 5.)
    m.get_accel(m.creep_speed - 0.01, True, False, False)
    self.assertEqual(m.brake_counts, 0.)
    # No stable-speed gate and no return to the ramp if speed rebounds.
    for _ in range(round(1. / DT_MDL)):
      m.get_accel(m.creep_speed + 0.05, True, False, False)
    self.assertEqual(-m.brake_counts, 3.)

  def test_guards_abort_ramp_and_positive_phase(self):
    for positive in (False, True):
      for speed, stopped, cruise_stopped in ((0.4, False, False), (2., False, False),
                                            (0.7, True, False), (0.7, False, True)):
        m = replace(MANEUVERS[-1])
        self.start(m)
        if positive:
          for _ in range(round(1. / DT_MDL) + 1):
            m.get_accel(m.creep_speed, True, False, False)
          self.assertEqual(-m.brake_counts, 200.)
        m.get_accel(speed, True, stopped, cruise_stopped)
        self.assertFalse(m.brake_test_active)
        self.assertTrue(maneuver_should_stop(m, speed, 0.))

  def test_interruptions_restart_acquisition(self):
    for positive in (False, True):
      for gas, engaged in ((True, True), (False, False)):
        m = replace(MANEUVERS[-1])
        self.start(m)
        for _ in range(25):
          m.get_accel(m.creep_speed if positive else RECOVERY_SPEED, True, False, False)
        m.get_accel(0.7, engaged, False, False, gas)
        self.assertFalse(m.brake_test_active)
        self.assertFalse(m._target_reached)
        self.assertEqual(m._acquisition_frames, 0)
        self.start(m)
        m.get_accel(RECOVERY_SPEED, True, False, False)
        self.assertEqual(m.brake_counts, 5.)
