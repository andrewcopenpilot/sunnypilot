import unittest
from dataclasses import replace

from openpilot.tools.longitudinal_maneuvers.maneuversd import (
  BrakeCharacterizationManeuver, MANEUVERS, BRAKE_CHARACTERIZATION_MANEUVERS, RECOVERY_SPEED, DT_MDL, brake_hold_maneuvers,
)


class TestBrakeProfiles(unittest.TestCase):
  def start(self, m):
    for _ in range(round(2. / DT_MDL)):
      m.get_accel(m.initial_speed, True, False, False)
    self.assertTrue(m.brake_test_active)
    self.assertEqual(m.brake_counts, 0.)

  def test_default_sweep_rate_bounds_and_repeat_acknowledgement(self):
    self.assertIs(MANEUVERS, BRAKE_CHARACTERIZATION_MANEUVERS)
    m = replace(MANEUVERS[0])
    for repeat in range(3):
      self.start(m)
      commands = []
      for i in range(round(m.duration / DT_MDL)):
        self.assertEqual(m.get_accel(1., True, False, False), 0.)
        commands.append(m.brake_counts)
        self.assertAlmostEqual(m.brake_counts, min(12., max(0., (i * DT_MDL - 2.) * 0.5)))
      self.assertEqual(max(commands), 12.)
      self.assertLess(m.get_accel(1., True, False, False), 0.)
      self.assertFalse(m.brake_test_active)
      self.assertEqual(m._end_reason, 'profile complete')
      for _ in range(100):
        self.assertLess(m.get_accel(0., True, True, True), 0.)
        self.assertTrue(m.stopping_intent)
      m.get_accel(0., False, True, True, True)
      self.assertTrue(m._recovering)
      self.assertFalse(m.brake_test_active)
      for _ in range(round(3. / DT_MDL)):
        m.get_accel(RECOVERY_SPEED, True, False, False)
      self.assertTrue(m._run_completed)
      self.assertEqual(m.finished, repeat == 2)

  def test_hold_levels_are_constant_for_five_seconds(self):
    for m in brake_hold_maneuvers([1., 3., 5.]):
      self.start(m)
      hold_frames = 0
      while m.active:
        m.get_accel(1., True, False, False)
        if m.brake_test_active and m.brake_counts == m.max_counts:
          hold_frames += 1
      self.assertEqual(hold_frames, round(5. / DT_MDL))
      self.assertTrue(m.stopping_intent)

  def test_bounds_terminate_with_reason_without_advancing_before_ack(self):
    for speed, standstill, css, reason in ((0.4, False, False, 'lower speed bound'),
                                         (2., False, False, 'upper speed bound'),
                                         (1., True, False, 'lower speed bound'),
                                         (1., False, True, 'lower speed bound')):
      m = replace(MANEUVERS[0])
      self.start(m)
      self.assertLess(m.get_accel(speed, True, standstill, css), 0.)
      self.assertFalse(m.brake_test_active)
      self.assertEqual(m._end_reason, reason)
      self.assertEqual(m._repeated, 0)
      self.assertTrue(m.stopping_intent)

  def test_interruption_resets_entire_sweep(self):
    m = replace(MANEUVERS[0])
    self.start(m)
    for _ in range(120):
      m.get_accel(1., True, False, False)
    self.assertGreater(m.brake_counts, 0.)
    self.assertEqual(m.get_accel(1., False, False, False), 0.)
    self.assertFalse(m.brake_test_active)
    self.assertEqual(m.brake_counts, 0.)
    self.start(m)
    self.assertEqual(m._test_frames, 0)

  def test_invalid_profile_is_rejected(self):
    for kwargs in ({'max_counts': 13.}, {'max_counts': -1.}, {'counts_per_second': 1.}, {'hold_seconds': 100.}):
      with self.assertRaises(AssertionError):
        BrakeCharacterizationManeuver('invalid', [], **kwargs)
