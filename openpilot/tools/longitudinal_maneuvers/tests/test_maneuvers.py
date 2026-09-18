import unittest
from types import SimpleNamespace
from dataclasses import replace

from openpilot.common.constants import CV
from openpilot.tools.longitudinal_maneuvers.maneuversd import (
  Action, Maneuver, StopManeuver, MovingCreepManeuver, LOW_SPEED_MANEUVERS, STANDARD_MANEUVERS, RECOVERY_SPEED, DT_MDL,
)
from openpilot.tools.longitudinal_maneuvers.maneuver_helpers import collect_maneuvers


class TestManeuvers(unittest.TestCase):
  def stop(self):
    return StopManeuver('test', [], repeat=1, initial_speed=3. * CV.MPH_TO_MS, stop_accel=-0.5)

  def start(self, m):
    for _ in range(round(2. / DT_MDL)):
      m.get_accel(m.initial_speed, True, False, False)
    self.assertTrue(m.active)

  def hold(self, m):
    for _ in range(62):
      self.assertLess(m.get_accel(0., True, True, False), 0.)
    self.assertTrue(m._complete)

  def recover(self, m):
    for _ in range(round(3. / DT_MDL)):
      m.get_accel(RECOVERY_SPEED, True, False, False)
    self.assertTrue(m._run_completed)

  def test_creep_suite(self):
    self.assertEqual(len(STANDARD_MANEUVERS), 11)
    self.assertEqual(sum(m.repeat + 1 for m in STANDARD_MANEUVERS), 22)
    self.assertEqual(sum(m.repeat + 1 for m in LOW_SPEED_MANEUVERS), 16)
    self.assertEqual(STANDARD_MANEUVERS[:8], LOW_SPEED_MANEUVERS)
    self.assertTrue(all(m.initial_speed == 3. * CV.MPH_TO_MS for m in STANDARD_MANEUVERS))
    self.assertTrue(all(m.repeat == 1 for m in STANDARD_MANEUVERS))
    self.assertEqual(RECOVERY_SPEED, 3. * CV.MPH_TO_MS)

  def test_suite_with_simulated_vehicle(self):
    completed = 0
    for template in STANDARD_MANEUVERS:
      with self.subTest(maneuver=template.description):
        m = replace(template)
        v = 0.
        pulses = runs = 0
        was_pulse = False
        active_speeds = []
        for _ in range(12000):
          if isinstance(m, StopManeuver) and m._complete:
            # The driver taps the throttle; longitudinal control is overridden during the tap.
            self.assertEqual(m.get_accel(v, False, True, True, True), 0.)
            self.assertTrue(m._recovering)
          was_active = m.active
          accel = m.get_accel(v, True, v == 0., v == 0.)
          if m.active and not was_active:
            active_speeds.append(v)
          if isinstance(m, StopManeuver):
            pulses += m.pulse_active and not was_pulse
            was_pulse = m.pulse_active
            if m.pulse_active:
              self.assertEqual(accel, m.pulse_accel)
              self.assertFalse(m.stopping_intent)
            self.assertFalse(m._failed)
          if isinstance(m, MovingCreepManeuver):
            self.assertFalse(m._failure)
          v = max(0., v + accel * DT_MDL)
          self.assertLessEqual(v, RECOVERY_SPEED + 0.1)
          if m._run_completed:
            self.assertAlmostEqual(v, RECOVERY_SPEED, delta=0.1)
            runs += 1
          if m.finished:
            break
        self.assertTrue(m.finished)
        self.assertEqual(runs, template.repeat + 1)
        self.assertEqual(len(active_speeds), runs)
        test_speed = m.creep_speed if isinstance(m, MovingCreepManeuver) else m.initial_speed
        self.assertTrue(all(abs(v - test_speed) < 0.1 for v in active_speeds))
        if isinstance(m, StopManeuver):
          self.assertEqual(pulses, template.creep_pulses * runs)
        completed += runs
    self.assertEqual(completed, 22)

  def test_setup_requires_only_continuous_2s_at_3mph(self):
    m = self.stop()
    self.assertEqual(m.setup_speed, 3. * CV.MPH_TO_MS)
    self.assertGreater(m.get_accel(0., True, True, False), 0.)
    self.assertFalse(m.active)
    for _ in range(39):
      m.get_accel(m.initial_speed, True, False, False)
    self.assertFalse(m.active)
    m.get_accel(m.initial_speed + 0.2, True, False, False)
    self.assertEqual(m._ready_cnt, 0)
    for _ in range(39):
      m.get_accel(m.initial_speed, True, False, False)
    self.assertFalse(m.active)
    m.get_accel(m.initial_speed, True, False, False)
    self.assertTrue(m.active)
    self.assertEqual(m._elapsed_frames, 0)

  def test_setup_interruption_restarts_at_3mph(self):
    for frames in (1, 30):
      m = self.stop()
      for _ in range(frames):
        m.get_accel(m.initial_speed, True, False, False)
      self.assertEqual(m.get_accel(m.initial_speed, False, False, False), 0.)
      self.assertEqual(m.setup_speed, 3. * CV.MPH_TO_MS)
      self.assertEqual(m._ready_cnt, 0)
      self.start(m)

  def test_interrupted_step_restarts_whole_run(self):
    m = Maneuver('step', [Action([-0.15], [3]), Action([0.], [2])], repeat=1, initial_speed=3. * CV.MPH_TO_MS)
    self.start(m)
    for _ in range(70):
      m.get_accel(1., True, False, False)
    self.assertEqual(m._action_index, 1)
    for _ in range(200):
      self.assertEqual(m.get_accel(1., False, False, False), 0.)
    self.assertFalse(m.finished)
    self.assertEqual(m._repeated, 0)
    self.assertEqual(m._action_index, 0)
    self.assertEqual(m._ready_cnt, 0)
    self.start(m)
    self.assertEqual(m.get_accel(1., True, False, False), -0.15)

  def test_completed_stop_waits_for_acknowledgement_then_recovers(self):
    for gas_pressed, long_active in ((True, True), (True, False), (False, False)):
      with self.subTest(gas_pressed=gas_pressed, long_active=long_active):
        m = self.stop()
        for run in range(2):
          self.start(m)
          self.hold(m)
          for _ in range(100):
            self.assertEqual(m.get_accel(0., True, True, True), -0.5)
            self.assertTrue(m.stopping_intent)
            self.assertFalse(m.finished)
          m.get_accel(0., long_active, True, True, gas_pressed)
          self.assertTrue(m._recovering)
          self.assertFalse(m.stopping_intent)
          self.assertFalse(m._run_completed)
          # Keep recovery pending through the throttle override or disengagement.
          for _ in range(20):
            self.assertEqual(m.get_accel(0., False, True, True), 0.)
          self.assertTrue(m._recovering)
          self.assertGreater(m.get_accel(0., True, True, False), 0.)
          self.recover(m)
          self.assertEqual(m.finished, run == 1)

  def test_recovery_waits_for_3mph_before_counting_run(self):
    m = Maneuver('crawl', [Action([0.], [0.1])], initial_speed=3. * CV.MPH_TO_MS)
    self.start(m)
    for _ in range(3):
      m.get_accel(m.initial_speed, True, False, False)
    self.assertTrue(m._recovering)
    for _ in range(100):
      self.assertGreater(m.get_accel(2. * CV.MPH_TO_MS, True, False, False), 0.)
      self.assertFalse(m._run_completed)
    m.get_accel(RECOVERY_SPEED, False, False, False)
    self.assertTrue(m._recovering)
    self.recover(m)
    self.assertTrue(m.finished)
    self.assertEqual(m.get_accel(RECOVERY_SPEED, True, False, False), 0.)
    self.assertFalse(m._run_completed)

  def test_interrupt_stop_or_hold_does_not_count(self):
    for during_hold in (False, True):
      m = self.stop()
      self.start(m)
      if during_hold:
        for _ in range(20):
          m.get_accel(0., True, True, False)
      m.get_accel(1., False, False, False, True)
      self.assertFalse(m.finished)
      self.assertFalse(m._run_completed)
      self.assertFalse(m._recovering)
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

  def test_creep_pulses_timing_and_hold_after_last_pulse(self):
    m = StopManeuver('pulse', [], initial_speed=3. * CV.MPH_TO_MS, stop_accel=-0.3, timeout=30., creep_pulses=2,
                     pulse_off_time=0.3, pulse_period=1.5, pulse_start=1.0)
    self.start(m)
    m.get_accel(0., True, True, False)
    trace = []
    for _ in range(int(6. / DT_MDL)):
      a = m.get_accel(0., True, True, False)
      trace.append((round(m._holding_frames * DT_MDL, 3), m.pulse_active, m.stopping_intent, a))
    pulse_times = [t for t, p, _, _ in trace if p]
    self.assertAlmostEqual(min(pulse_times), 1.0, places=3)
    self.assertTrue(all(0.999 <= t < 1.3 + 1e-6 or 2.499 <= t < 2.8 + 1e-6 for t in pulse_times))
    self.assertEqual(len(pulse_times), 2 * round(0.3 / DT_MDL))
    self.assertTrue(all((not s) and a == 0.05 for _, p, s, a in trace if p))
    self.assertTrue(all(s and a == -0.3 for _, p, s, a in trace if not p))
    self.assertTrue(m._complete)
    self.assertGreaterEqual(m._holding_frames * DT_MDL, 2.5 + 0.3 + m.hold_time - 0.1)

  def test_timeout_keeps_stopping_intent_and_retries_same_run(self):
    for moving in (True, False):
      m = self.stop()
      self.start(m)
      for i in range(int(m.timeout / DT_MDL) + 10):
        v = 2. if moving else (0.2 if i % 20 == 0 else 0.)
        m.get_accel(v, True, v == 0., False)
      self.assertTrue(m._failed)
      self.assertTrue(m.stopping_intent)
      self.assertFalse(m._complete)
      self.assertEqual(m.get_accel(2., True, False, False), -0.5)
      m.get_accel(2., False, False, False)
      self.assertFalse(m._failed)
      self.assertFalse(m._recovering)
      self.assertEqual(m._repeated, 0)
      self.start(m)


class TestMovingCreepManeuvers(unittest.TestCase):
  def acquire(self):
    m = MovingCreepManeuver('moving', [Action([0.], [6.])], repeat=1, initial_speed=3. * CV.MPH_TO_MS)
    for _ in range(round(2. / DT_MDL)):
      m.get_accel(m.initial_speed, True, False, False)
    self.assertFalse(m.active)
    self.assertTrue(m._creep_setup)
    self.assertEqual(m.setup_speed, m.creep_speed)
    return m

  def start(self, m):
    m.get_accel(m.creep_speed, True, False, False)
    self.assertTrue(m.active)
    self.assertEqual(m._action_frames, 0)

  def test_acquisition_starts_on_first_crossing_without_settling(self):
    m = self.acquire()
    for speed in (1.3, 1.2, 1.25, 1.1, 1.01):
      self.assertEqual(m.get_accel(speed, True, False, False), -0.15)
      self.assertFalse(m.active)
    self.start(m)
    # It continues even if speed immediately leaves the old settling band.
    self.assertEqual(m.get_accel(0.65, True, False, False), 0.)
    self.assertEqual(m._action_frames, 1)

  def test_invalid_crawl_latches_stop_until_acknowledgement(self):
    for during_acquisition in (False, True):
      for speed, standstill, cruise_standstill in ((0.39, False, False), (0.8, True, False),
                                                  (0.8, False, True), (1.51, False, False)):
        with self.subTest(acquiring=during_acquisition, speed=speed, standstill=standstill, cruise=cruise_standstill):
          m = self.acquire()
          if not during_acquisition:
            self.start(m)
          self.assertEqual(m.get_accel(speed, True, standstill, cruise_standstill), -0.3)
          self.assertTrue(m.stopping_intent)
          self.assertFalse(m.active)
          for _ in range(200):
            self.assertEqual(m.get_accel(0.8, True, False, False), -0.3)
            self.assertFalse(m._run_completed)
            self.assertFalse(m._recovering)
          self.assertFalse(m.finished)

  def test_failed_attempt_recovers_and_advances_only_after_acknowledgement(self):
    for gas_pressed, long_active in ((True, True), (True, False), (False, False)):
      for final_run in (False, True):
        m = self.acquire()
        m._repeated = int(final_run)
        self.start(m)
        m.get_accel(0.2, True, False, False)
        self.assertTrue(m.stopping_intent)
        m.get_accel(0., long_active, True, True, gas_pressed)
        self.assertTrue(m._recovering)
        self.assertFalse(m.stopping_intent)
        for _ in range(20):
          self.assertEqual(m.get_accel(0., False, True, True), 0.)
          self.assertFalse(m._run_completed)
        for _ in range(round(3. / DT_MDL)):
          m.get_accel(RECOVERY_SPEED, True, False, False)
        self.assertTrue(m._run_completed)
        self.assertTrue(m._run_failed)
        self.assertEqual(m._repeated, 1)
        self.assertEqual(m.finished, final_run)
        self.assertFalse(m.stopping_intent)
        m.get_accel(RECOVERY_SPEED, True, False, False)
        self.assertFalse(m._run_completed)
        self.assertFalse(m._run_failed)

  def test_acquisition_timeout(self):
    m = self.acquire()
    for _ in range(round(m.acquisition_timeout / DT_MDL)):
      m.get_accel(1.1, True, False, False)
    self.assertEqual(m._failure, 'crawl setup timed out')
    self.assertTrue(m.stopping_intent)
    self.assertEqual(m._action_frames, 0)

  def test_interrupt_acquisition_or_active_trial_restarts_setup(self):
    for active in (False, True):
      m = self.acquire()
      if active:
        self.start(m)
        m.get_accel(0.8, True, False, False)
      m.get_accel(0.8, False, False, False)
      self.assertEqual(m.setup_speed, RECOVERY_SPEED)
      self.assertEqual(m._action_frames, 0)
      self.assertEqual(m._acquisition_frames, 0)
      self.assertFalse(m._creep_setup)
      self.assertTrue(m._interrupted)

  def test_report_preserves_failure_at_end_of_active_trial(self):
    def alert(text):
      return SimpleNamespace(which=lambda: 'alertDebug', alertDebug=SimpleNamespace(alertText1=text, alertText2='moving'))
    messages = [alert('Setting up'), alert('Maneuver Active'), alert('Creep test invalid: take control'),
                alert('Setting up'), alert('Maneuver Active'), alert('Recovering to 3 mph')]
    maneuvers = collect_maneuvers(messages)
    self.assertEqual(len(maneuvers), 1)
    description, runs = maneuvers[0]
    self.assertEqual(description, 'moving')
    self.assertEqual(len(runs), 2)
    self.assertIn(messages[2], runs[0])
    self.assertNotIn(messages[2], runs[1])


if __name__ == '__main__':
  unittest.main()
