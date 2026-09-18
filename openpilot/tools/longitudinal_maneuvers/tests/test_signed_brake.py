import unittest
from dataclasses import replace

from openpilot.tools.longitudinal_maneuvers.maneuversd import (
  DT_MDL, MANEUVERS, SIGNED_BRAKE_MANEUVERS, RECOVERY_SPEED, SignedBrakeManeuver, maneuver_should_stop,
)


class TestSignedBrakeProfiles(unittest.TestCase):
  def start(self, maneuver):
    for _ in range(round(2. / DT_MDL)):
      maneuver.get_accel(RECOVERY_SPEED, True, False, False)
    self.assertTrue(maneuver.brake_test_active)

  def test_exact_sequences_repeats_and_acknowledgement(self):
    self.assertIs(MANEUVERS, SIGNED_BRAKE_MANEUVERS)
    expected = (
      ((-5., 2.), (-14., 4.), (0., 3.), (14., 4.), (0., 4.)),
      ((-5., 2.), (-14., 4.), (0., 3.), (7., 4.), (0., 4.)),
      ((-5., 2.), (-14., 4.), (0., 3.), (4., 2.), (8., 2.), (14., 2.), (0., 4.)),
    )
    self.assertEqual(sum(m.repeat + 1 for m in MANEUVERS), 6)
    for template, steps in zip(MANEUVERS, expected, strict=True):
      m = replace(template)
      self.assertEqual(m.request_steps, steps)
      for repeat in range(2):
        self.start(m)
        for signed, seconds in steps:
          for _ in range(round(seconds / DT_MDL)):
            self.assertEqual(m.get_accel(1., True, False, False), 0.)
            self.assertEqual(-m.brake_counts, signed)
            self.assertFalse(m.brake_release)
            self.assertFalse(maneuver_should_stop(m, 1., 0.))
        m.get_accel(1., True, False, False)
        self.assertEqual(m._end_reason, 'profile complete')
        self.assertTrue(m.stopping_intent)
        self.assertFalse(m.brake_test_active)
        m.get_accel(0., False, True, True, True)
        for _ in range(round(3. / DT_MDL)):
          m.get_accel(RECOVERY_SPEED, True, False, False)
        self.assertEqual(m.finished, repeat == 1)

  def test_positive_phase_still_honors_guards(self):
    for speed, standstill, cruise_stop in ((0.4, False, False), (2., False, False), (1., True, False), (1., False, True)):
      m = replace(MANEUVERS[0])
      self.start(m)
      m._test_frames = round(9. / DT_MDL)
      m.get_accel(1., True, False, False)
      self.assertEqual(-m.brake_counts, 14.)
      m.get_accel(speed, True, standstill, cruise_stop)
      self.assertFalse(m.brake_test_active)
      self.assertTrue(maneuver_should_stop(m, speed, 0.))

  def test_gas_override_restarts_instead_of_resuming_positive_phase(self):
    m = replace(MANEUVERS[0])
    self.start(m)
    m._test_frames = round(9. / DT_MDL)
    m.get_accel(1., True, False, False)
    m.get_accel(1., True, False, False, True)
    self.assertFalse(m.brake_test_active)
    self.assertEqual(m._test_frames, 0)
    self.start(m)
    self.assertEqual(-m.brake_counts, -5.)

  def test_invalid_profiles(self):
    for steps in ((), ((15., 1.),), ((-21., 1.),), ((float('nan'), 1.),), ((1., 0.),), ((1., 91.),)):
      with self.assertRaises(AssertionError):
        SignedBrakeManeuver('invalid', [], request_steps=steps)
