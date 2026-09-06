import unittest

from openpilot.tools.longitudinal_maneuvers.maneuversd import Action, Maneuver, StopManeuver, MANEUVERS, REGEN_ONLY_MANEUVERS, DT_MDL


class TestManeuvers(unittest.TestCase):
  def stop(self):
    return StopManeuver('test', [], repeat=1, initial_speed=4.47, stop_accel=-0.5)

  def start(self, m):
    m.get_accel(m.initial_speed, False, False, False)
    for _ in range(62):
      m.get_accel(m.initial_speed, True, False, False)
    self.assertTrue(m.active)

  def hold(self, m):
    for _ in range(62):
      self.assertLess(m.get_accel(0., True, True, False), 0.)
    self.assertTrue(m._complete)

  def test_tuning_suite_sequence(self):
    steps = [m for m in MANEUVERS if not isinstance(m, StopManeuver)]
    stops = [m for m in MANEUVERS if isinstance(m, StopManeuver)]
    self.assertEqual(sum(m.repeat + 1 for m in MANEUVERS), 16)
    self.assertEqual([m.actions[0].accel_bp for m in steps[:3]], [[-0.75], [-1.25], [-2.]])
    self.assertEqual([round(m.initial_speed / 0.44704) for m in steps], [20, 20, 20, 20, 40, 40, 40])
    self.assertEqual([m.stop_accel for m in stops], [-0.75])
    for template in steps:
      m = Maneuver(template.description, template.actions, repeat=template.repeat, initial_speed=template.initial_speed)
      completed = 0
      for _ in range(3000):
        m.get_accel(m.initial_speed, True, False, False)
        completed += m._run_completed
        if m.finished:
          break
      self.assertTrue(m.finished)
      self.assertEqual(completed, template.repeat + 1)

  def test_regen_only_list(self):
    self.assertEqual(sum(m.repeat + 1 for m in REGEN_ONLY_MANEUVERS), 2)
    m = REGEN_ONLY_MANEUVERS[0]
    self.assertEqual(m.actions[0].accel_bp, [-2.])
    self.assertEqual(round(m.initial_speed / 0.44704), 40)
    self.assertFalse(isinstance(m, StopManeuver))

  def test_ramp_and_sweep_shapes(self):
    def copy(template):
      return Maneuver(template.description, template.actions, repeat=template.repeat, initial_speed=template.initial_speed)
    ramp = copy([m for m in MANEUVERS if 'ramp' in m.description][0])
    self.start(ramp)  # the activating call already consumed frame 0
    accels = [ramp.get_accel(ramp.initial_speed, True, False, False) for _ in range(int(3. / DT_MDL) - 1)]
    self.assertLess(abs(accels[0]), 0.1)
    self.assertAlmostEqual(accels[-1], -1.5, places=1)
    self.assertTrue(all(b <= a + 1e-9 for a, b in zip(accels, accels[1:])))
    sweep = copy([m for m in MANEUVERS if 'sweep' in m.description][0])
    self.start(sweep)
    accels = [sweep.get_accel(sweep.initial_speed, True, False, False) for _ in range(int(10. / DT_MDL) - 1)]
    self.assertAlmostEqual(accels[-1], -2.5, places=1)
    self.assertTrue(all(b <= a + 1e-9 for a, b in zip(accels, accels[1:])))

  def test_stops_with_simulated_vehicle(self):
    completed = 0
    for template in [m for m in MANEUVERS if isinstance(m, StopManeuver)]:
      m = StopManeuver(template.description, [], repeat=template.repeat,
                       initial_speed=template.initial_speed, stop_accel=template.stop_accel)
      for _ in range(m.repeat + 1):
        self.start(m)
        v = m.initial_speed
        for _ in range(400):
          accel = m.get_accel(v, True, v == 0., v == 0.)
          self.assertLess(accel, 0.)
          v = max(0., v + accel * DT_MDL)
          if m._complete:
            break
        self.assertTrue(m._complete)
        self.assertFalse(m._failed)
        self.assertEqual(v, 0.)
        self.assertTrue(m.stopping_intent)
        m.get_accel(0., False, True, True)
        completed += m._run_completed
      self.assertTrue(m.finished)
    self.assertEqual(completed, 2)

  def test_interrupted_step_restarts_whole_run(self):
    m = Maneuver('step', [Action([-1.], [3]), Action([0.], [2])], repeat=2, initial_speed=8.94)
    self.start(m)
    for _ in range(70):
      m.get_accel(8., True, False, False)
    self.assertEqual(m._action_index, 1)
    for _ in range(200):
      self.assertEqual(m.get_accel(5., False, False, False), 0.)
    self.assertFalse(m.finished)
    self.assertEqual(m._repeated, 0)
    self.assertEqual(m._action_index, 0)
    self.assertEqual(m._ready_cnt, 0)
    self.start(m)
    self.assertEqual(m.get_accel(8., True, False, False), -1.)

  def test_stop_requires_takeover_before_setup(self):
    m = self.stop()
    for _ in range(100):
      self.assertEqual(m.get_accel(4.47, True, False, False), 0.)
    self.assertFalse(m.active)
    self.start(m)

  def test_completed_stop_waits_for_takeover_then_repeats(self):
    m = self.stop()
    self.start(m)
    self.hold(m)
    for _ in range(100):
      self.assertEqual(m.get_accel(0., True, True, False), -0.5)
      self.assertTrue(m.stopping_intent)
      self.assertFalse(m.finished)
    m.get_accel(0., False, True, False)
    self.assertEqual(m._repeated, 1)
    self.assertTrue(m._run_completed)
    self.start(m)
    self.hold(m)
    m.get_accel(0., False, True, False)
    self.assertTrue(m.finished)

  def test_interrupt_stop_or_hold_does_not_count(self):
    for during_hold in (False, True):
      m = self.stop()
      self.start(m)
      if during_hold:
        for _ in range(20):
          m.get_accel(0., True, True, False)
      m.get_accel(1., False, False, False)
      self.assertFalse(m.finished)
      self.assertFalse(m._run_completed)
      self.assertEqual(m._repeated, 0)
      self.assertEqual(m._hold_frames, 0)
      self.start(m)
      self.assertFalse(m.stopping_intent)

  def test_hold_requires_continuous_confirmed_standstill(self):
    m = self.stop()
    self.start(m)
    for _ in range(40):
      m.get_accel(0., True, True, False)
    m.get_accel(0.2, True, False, False)
    self.assertEqual(m._hold_frames, 0)
    for _ in range(40):
      m.get_accel(0., True, True, False)
    self.assertFalse(m._complete)
    for _ in range(21):
      m.get_accel(0., True, True, False)
    self.assertTrue(m._complete)

  def test_timeout_keeps_stopping_intent_and_retries_same_run(self):
    for moving in (True, False):
      m = self.stop()
      self.start(m)
      for i in range(int(m.timeout / DT_MDL) + 10):
        # Also test an unstable hold that never gets three continuous seconds.
        v = 2. if moving else (0.2 if i % 20 == 0 else 0.)
        m.get_accel(v, True, v == 0., False)
      self.assertTrue(m._failed)
      self.assertTrue(m.stopping_intent)
      self.assertFalse(m._complete)
      self.assertEqual(m.get_accel(2., True, False, False), -0.5)
      m.get_accel(2., False, False, False)
      self.assertFalse(m._failed)
      self.assertEqual(m._repeated, 0)
      self.start(m)


if __name__ == '__main__':
  unittest.main()
