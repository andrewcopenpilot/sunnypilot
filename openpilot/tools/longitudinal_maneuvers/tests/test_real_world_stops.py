import unittest
from dataclasses import replace

from openpilot.tools.longitudinal_maneuvers.maneuversd import (
  DT_MDL, MANEUVERS, CREEP_SPEED_MANEUVERS, REAL_WORLD_STOP_MANEUVERS, RECOVERY_SPEED, LOW_SPEED_MANEUVERS,
  QueueCreepManeuver, StopManeuver, maneuver_should_stop,
)


def simulate(template, steps=12000):
  """Ideal vehicle: tracks the request exactly. Returns one record per model frame until finished."""
  m, v, records = replace(template), 0., []
  for _ in range(steps):
    if m._complete and not (isinstance(m, QueueCreepManeuver) and m._creeps_done < m.creeps):
      m.get_accel(v, False, True, True, True)  # driver acknowledges the completed stop
    was_active = m.active  # the frame that activates a test still returns the setup request
    accel = m.get_accel(v, True, v == 0., v == 0.)
    records.append(dict(v=v, accel=accel, active=was_active and m.active, holding=m._holding, pulse=m.pulse_active,
                        creeping=getattr(m, "_creeping", False), stop=maneuver_should_stop(m, v, accel),
                        completed=m._run_completed, failed=m._failed))
    v = max(0., v + accel * DT_MDL)
    if m.finished:
      break
  return m, records


class TestRealWorldStops(unittest.TestCase):
  def test_active_suite(self):
    self.assertEqual(MANEUVERS, CREEP_SPEED_MANEUVERS[3:5] + REAL_WORLD_STOP_MANEUVERS)
    self.assertEqual([m.description.split(",")[0] for m in MANEUVERS],
                     ["creep speed: C04", "creep speed: C05", "real stop: S01", "real stop: S02", "real stop: S03", "real stop: S04"])
    self.assertEqual(sum(m.repeat + 1 for m in MANEUVERS), 12)

  def test_every_scenario_completes_twice(self):
    for template in REAL_WORLD_STOP_MANEUVERS:
      with self.subTest(maneuver=template.description):
        m, records = simulate(template)
        self.assertTrue(m.finished)
        self.assertEqual(sum(r["completed"] for r in records), 2)
        self.assertFalse(any(r["failed"] for r in records))

  def test_fading_target_follows_speed_and_uses_planner_stop_rule(self):
    _, records = simulate(replace(REAL_WORLD_STOP_MANEUVERS[0], repeat=0))
    approach = [r for r in records if r["active"] and not r["holding"]]
    self.assertAlmostEqual(approach[0]["accel"], -0.45, delta=0.01)
    self.assertTrue(all(b["accel"] >= a["accel"] for a, b in zip(approach[:-1], approach[1:], strict=True) if b["v"] > 0.))
    moving = [r for r in approach if r["v"] > 0.]
    self.assertAlmostEqual(moving[-1]["accel"], -0.2, delta=0.01)
    # No early stop intent: only the planner's v < 0.3 m/s rule, as in the logged traffic stops.
    self.assertTrue(all(r["stop"] == (r["v"] < 0.3) for r in moving))

  def test_constant_stops_are_unchanged(self):
    _, records = simulate(LOW_SPEED_MANEUVERS[1])
    self.assertEqual({r["accel"] for r in records if r["active"]}, {-0.3})

  def test_flaps_start_early_and_release_stop_intent(self):
    template = REAL_WORLD_STOP_MANEUVERS[2]
    m = replace(template)
    for _ in range(round(2. / DT_MDL)):
      m.get_accel(RECOVERY_SPEED, True, False, False)
    m.get_accel(0., True, True, False)  # first standstill
    self.assertTrue(m._holding)
    pulses = []
    for frame in range(1, round(4. / DT_MDL)):
      accel = m.get_accel(0., True, True, False)
      stop = maneuver_should_stop(m, 0., accel)
      self.assertEqual((accel, stop), (0.05, False) if m.pulse_active else (-0.3, True))
      if m.pulse_active and (not pulses or pulses[-1][-1] != frame - 1):
        pulses.append([frame])
      elif m.pulse_active:
        pulses[-1].append(frame)
    self.assertEqual([(round(p[0] * DT_MDL, 2), round(len(p) * DT_MDL, 2)) for p in pulses], [(0.3, 0.4), (1.1, 1.0), (2.5, 0.3)])
    self.assertFalse(m._complete)  # the hold timer starts only after the last flap

  def test_uniform_pulse_train_is_unchanged(self):
    m = StopManeuver("test", [], creep_pulses=3, pulse_off_time=0.3)
    for t, expected in ((0.9, (False, False)), (1.0, (True, False)), (1.3, (False, False)), (2.5, (True, False)),
                        (4.0, (True, False)), (4.3, (False, True))):
      self.assertEqual(m._pulse_state(t), expected, t)
    self.assertEqual(StopManeuver("test", [])._pulse_state(0.), (False, True))

  def test_queue_creeps_forward_between_stops_without_acknowledgement(self):
    m, records = simulate(replace(REAL_WORLD_STOP_MANEUVERS[3], repeat=0))
    creeps = [i for i, r in enumerate(records) if r["creeping"] and not records[i - 1]["creeping"]]
    self.assertEqual(len(creeps), 2)
    for start in creeps:
      # The frame that ends the creep still returns a creep request, with the flag already cleared.
      creep = records[start:start + round(5. / DT_MDL) - 1]
      self.assertEqual(records[start - 1]["v"], 0.)
      self.assertTrue(all(r["creeping"] and not r["stop"] and not r["holding"] for r in creep))
      self.assertEqual(creep[0]["accel"], 0.3)
      # 0.5 1/s speed tracking: about 92% of the 1.5 mph target after 5 s, without overshoot.
      self.assertAlmostEqual(creep[-1]["v"], m.creep_speed, delta=0.1)
      self.assertLessEqual(max(r["v"] for r in creep), m.creep_speed)
      self.assertFalse(records[start + len(creep)]["creeping"])
      self.assertLess(records[start + len(creep) + 1]["accel"], -0.2)  # fading approach to the next stop
    # Three stops in one run; only the last waits for the driver.
    self.assertEqual(sum(r["holding"] and not records[i - 1]["holding"] for i, r in enumerate(records)), 3)
    self.assertEqual(sum(r["completed"] for r in records), 1)

  def test_queue_interruption_restarts_the_whole_run(self):
    m = replace(REAL_WORLD_STOP_MANEUVERS[3])
    m._active = m._complete = True
    self.assertEqual(m.get_accel(0., True, True, True), 0.3)
    self.assertTrue(m._creeping)
    self.assertEqual(m.get_accel(0.2, False, False, False), 0.)
    self.assertTrue(m._interrupted)
    self.assertEqual((m._creeping, m._creeps_done, m.active), (False, 0, False))


if __name__ == "__main__":
  unittest.main()
