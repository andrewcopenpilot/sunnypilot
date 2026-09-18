import unittest
from dataclasses import replace

from openpilot.tools.longitudinal_maneuvers.maneuversd import (
  BrakeCharacterizationManeuver, BRAKE_CHARACTERIZATION_MANEUVERS, BRAKE_SWEEP_MANEUVERS,
  BRAKE_HOLD_MANEUVERS, BRAKE_RELEASE_MANEUVERS, RECOVERY_SPEED, DT_MDL,
)


class TestBrakeProfiles(unittest.TestCase):
  def start(self, m):
    for _ in range(round(2. / DT_MDL)):
      m.get_accel(m.initial_speed, True, False, False)
    self.assertTrue(m.brake_test_active)
    self.assertEqual(m.brake_counts, m.start_counts)

  def test_preserved_sweep_rate_bounds_and_repeat_acknowledgement(self):
    m = replace(BRAKE_SWEEP_MANEUVERS[0])
    self.assertEqual(m.duration, 64.)
    for repeat in range(3):
      self.start(m)
      commands = []
      for i in range(round(m.duration / DT_MDL)):
        self.assertEqual(m.get_accel(1., True, False, False), 0.)
        commands.append(m.brake_counts)
        self.assertAlmostEqual(m.brake_counts, min(20., max(5., 5. + (i * DT_MDL - 2.) * 0.25)))
      self.assertEqual(min(commands), 5.)
      self.assertEqual(max(commands), 20.)
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

  def test_preserved_holds_and_descending_release_repeat_from_fresh_start(self):
    self.assertEqual([m.max_counts for m in BRAKE_HOLD_MANEUVERS], [11., 12., 13.])
    self.assertEqual(sum(m.repeat + 1 for m in BRAKE_HOLD_MANEUVERS), 9)
    for profile, duration in zip(BRAKE_HOLD_MANEUVERS, (24., 31., 38.), strict=True):
      m = replace(profile)
      self.assertEqual(m.duration, duration)
      for repeat in range(3):
        self.start(m)
        commands = []
        for _ in range(round(m.duration / DT_MDL)):
          self.assertEqual(m.get_accel(1., True, False, False), 0.)
          self.assertTrue(m.brake_test_active)
          commands.append(m.brake_counts)
        peak_start = round((2. + (m.max_counts - 5.) / 0.5) / DT_MDL)
        hold_frames = round(5. / DT_MDL)
        expected_levels = list(range(int(m.max_counts), 9, -1))
        self.assertEqual(commands[peak_start:], [float(level) for level in expected_levels for _ in range(hold_frames)])
        self.assertEqual(commands[:round(2. / DT_MDL)], [5.] * round(2. / DT_MDL))
        self.assertLess(m.get_accel(1., True, False, False), 0.)
        self.assertFalse(m.brake_test_active)
        self.assertTrue(m.stopping_intent)
        self.assertFalse(m.finished)
        m.get_accel(0., False, True, True, True)
        for _ in range(round(3. / DT_MDL)):
          m.get_accel(RECOVERY_SPEED, True, False, False)
        self.assertTrue(m._run_completed)
        self.assertEqual(m.finished, repeat == 2)

  def test_preserved_release_suite_timing_zero_output_and_two_repeats(self):
    self.assertEqual(len(BRAKE_RELEASE_MANEUVERS), 12)
    self.assertEqual(sum(m.repeat + 1 for m in BRAKE_RELEASE_MANEUVERS), 24)
    expected = [
      (12., 4., (0.,)), (12., 4., (5.,)), (12., 4., (8.,)),
      (13., 3., (0.,)), (13., 3., (5.,)), (13., 3., (8.,)),
      (12., 4., (2.,)), (12., 4., (10.,)), (12., 2., (0.,)), (12., 2., (5.,)),
      (12., 4., (10., 8., 6., 4., 2., 0.)),
      (12., 4., (11., 10., 9., 8., 7., 6., 5., 4., 3., 2., 1., 0.)),
    ]
    for profile, (peak, hold, releases) in zip(BRAKE_RELEASE_MANEUVERS, expected, strict=True):
      m = replace(profile)
      self.assertEqual((m.max_counts, m.hold_seconds, m.release_counts), (peak, hold, releases))
      peak_start = round((2. + (peak - 5.) / 0.5) / DT_MDL)
      expected_holds = [peak] * round(hold / DT_MDL)
      for count in releases[:-1]:
        expected_holds += [count] * round(1.5 / DT_MDL)
      expected_holds += [releases[-1]] * round(8. / DT_MDL)
      self.assertEqual(round(m.duration / DT_MDL), peak_start + len(expected_holds))
      for repeat in range(2):
        self.start(m)
        commands = []
        for _ in range(round(m.duration / DT_MDL)):
          self.assertEqual(m.get_accel(1., True, False, False), 0.)
          self.assertTrue(m.brake_test_active)  # Includes the entire zero-count hold.
          self.assertFalse(m.stopping_intent)
          commands.append(m.brake_counts)
        self.assertEqual(commands[peak_start:], expected_holds)
        self.assertLess(m.get_accel(1., True, False, False), 0.)
        self.assertFalse(m.brake_test_active)
        self.assertTrue(m.stopping_intent)
        self.assertFalse(m.finished)
        m.get_accel(0., False, True, True, True)
        for _ in range(round(3. / DT_MDL)):
          m.get_accel(RECOVERY_SPEED, True, False, False)
        self.assertTrue(m._run_completed)
        self.assertEqual(m.finished, repeat == 1)

  def test_preserved_exit_suite_phase_timing_and_repeats(self):
    self.assertEqual(len(BRAKE_CHARACTERIZATION_MANEUVERS), 6)
    self.assertEqual(sum(m.repeat + 1 for m in BRAKE_CHARACTERIZATION_MANEUVERS), 12)
    expected = [(12., 4., None), (12., 4., 0.), (12., 4., 2.),
                (13., 3., None), (13., 3., 0.), (13., 3., 2.)]
    for profile, (peak, hold, inactive_after) in zip(BRAKE_CHARACTERIZATION_MANEUVERS, expected, strict=True):
      m = replace(profile)
      self.assertEqual((m.max_counts, m.hold_seconds, m.inactive_brake_after), (peak, hold, inactive_after))
      release_start = 2. + (peak - 5.) / 0.5 + hold
      inactive_start = release_start + inactive_after if inactive_after is not None else float('inf')
      for repeat in range(2):
        self.start(m)
        inactive_frames = 0
        for frame in range(round(m.duration / DT_MDL)):
          self.assertEqual(m.get_accel(1., True, False, False), 0.)
          elapsed = frame * DT_MDL
          self.assertTrue(m.brake_test_active)
          self.assertFalse(m.stopping_intent)
          self.assertEqual(m.brake_release, elapsed >= inactive_start)
          if elapsed >= release_start:
            self.assertEqual(m.brake_counts, 0.)
          inactive_frames += m.brake_release
        self.assertEqual(inactive_frames, 0 if inactive_after is None else round(8. / DT_MDL))
        self.assertLess(m.get_accel(1., True, False, False), 0.)
        self.assertFalse(m.brake_release)
        self.assertTrue(m.stopping_intent)
        m.get_accel(0., False, True, True, True)
        for _ in range(round(3. / DT_MDL)):
          m.get_accel(RECOVERY_SPEED, True, False, False)
        self.assertTrue(m._run_completed)
        self.assertEqual(m.finished, repeat == 1)

  def test_final_zero_hold_keeps_guard_and_resets_on_interruption(self):
    for profile in BRAKE_CHARACTERIZATION_MANEUVERS:
      for interrupted in (False, True):
        m = replace(profile)
        self.start(m)
        for _ in range(round((m.duration - 4.) / DT_MDL)):
          m.get_accel(1., True, False, False)
        self.assertTrue(m.brake_test_active)
        self.assertEqual(m.brake_counts, 0.)
        m.get_accel(1. if interrupted else 0.4, not interrupted, False, False)
        self.assertFalse(m.brake_test_active)
        self.assertFalse(m.brake_release)
        if interrupted:
          self.start(m)
          self.assertEqual(m.brake_counts, 5.)
          self.assertEqual(m._test_frames, 0)
        else:
          self.assertEqual(m._end_reason, 'lower speed bound')
          self.assertTrue(m.stopping_intent)

  def test_release_phase_keeps_speed_guard_and_interruption_reset(self):
    for interrupted in (False, True):
      m = replace(BRAKE_HOLD_MANEUVERS[-1])
      self.start(m)
      for _ in range(round(24. / DT_MDL)):
        m.get_accel(1., True, False, False)
      self.assertEqual(m.brake_counts, 12.)
      m.get_accel(0.4 if not interrupted else 1., not interrupted, False, False)
      self.assertFalse(m.brake_test_active)
      self.assertEqual(m.brake_counts, 0.)
      if interrupted:
        self.start(m)
        self.assertEqual(m.brake_counts, 5.)
        self.assertEqual(m._test_frames, 0)
      else:
        self.assertEqual(m._end_reason, 'lower speed bound')
        self.assertTrue(m.stopping_intent)

  def test_bounds_terminate_with_reason_without_advancing_before_ack(self):
    for speed, standstill, css, reason in ((0.4, False, False, 'lower speed bound'),
                                         (2., False, False, 'upper speed bound'),
                                         (1., True, False, 'lower speed bound'),
                                         (1., False, True, 'lower speed bound')):
      m = replace(BRAKE_CHARACTERIZATION_MANEUVERS[0])
      self.start(m)
      self.assertLess(m.get_accel(speed, True, standstill, css), 0.)
      self.assertFalse(m.brake_test_active)
      self.assertEqual(m._end_reason, reason)
      self.assertEqual(m._repeated, 0)
      self.assertTrue(m.stopping_intent)

  def test_interruption_resets_entire_sweep(self):
    m = replace(BRAKE_CHARACTERIZATION_MANEUVERS[0])
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
    for kwargs in ({'max_counts': 21.}, {'max_counts': -1.}, {'start_counts': -1.}, {'start_counts': 5.5},
                   {'start_counts': 6., 'max_counts': 5.}, {'counts_per_second': 1.}, {'hold_seconds': 100.},
                   {'release_counts': (21.,)}, {'release_counts': (12., 13.)}, {'release_counts': (-1.,)},
                   {'release_counts': (10.5,)}, {'release_hold_seconds': 0.},
                   {'release_final_hold_seconds': 8.}, {'release_counts': (0.,), 'release_final_hold_seconds': 0.},
                   {'release_counts': (0.,), 'release_final_hold_seconds': float('nan')},
                   {'inactive_brake_after': 0.}, {'release_counts': (5.,), 'inactive_brake_after': 0.},
                   {'release_counts': (0.,), 'inactive_brake_after': -1.},
                   {'release_counts': (0.,), 'inactive_brake_after': 5.}):
      with self.assertRaises(AssertionError):
        BrakeCharacterizationManeuver('invalid', [], **kwargs)
