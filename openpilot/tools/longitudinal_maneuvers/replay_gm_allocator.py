#!/usr/bin/env python3
"""Replay logged inputs through the GM longitudinal allocator (opendbc gm/carcontroller.py).

Every input of CarController.update() is already logged: carControl (corrected acceleration, stop
state, direct brake-test commands), carState and the HPCM torque limits on CAN. Replaying them
  1. checks that the checked-out allocator reproduces the commands the car actually sent, and
  2. recovers the torque/brake ownership at every 25 Hz update without a log schema change.

Recorded-input replay checks interfaces and arithmetic. It does not predict how the vehicle
would have responded to different commands: after the first changed command the recorded
feedback no longer belongs to the replayed controller. A log recorded with a different
allocator is therefore expected to mismatch; use --transitions to see where.
"""
import argparse
import ast
import csv
import sys
from dataclasses import dataclass, field
from types import SimpleNamespace

from opendbc.car import structs
from opendbc.car.gm.carcontroller import CarController
from opendbc.car.gm.values import DBC, CanBus, LongOwner
from openpilot.tools.lib.logreader import LogReader

AXLE_TORQUE_LIMITS = 0x1C5
BRAKE_COMMAND = 0x315
COLUMNS = ("t", "v_ego", "a_ego", "long_active", "stopping", "brake_test", "axle_torque_min", "accel", "brake_mode",
           "gas", "brake", "mode", "logged_gas", "logged_brake", "logged_mode")


def brake_command(messages, bus):
  """(mode, signed request counts) of the last EBCMFrictionBrakeCmd among CAN tuples/readers."""
  result = None
  for address, dat, src in messages:
    if address == BRAKE_COMMAND and src == bus and len(dat) >= 2:
      raw = ((dat[0] & 0xf) << 8) | dat[1]
      result = (dat[0] >> 4, raw - 0x1000 if raw & 0x800 else raw)
  return result


@dataclass
class Replay:
  """One controller at one of the four possible 25 Hz phases, which the log does not record."""
  controller: CarController
  rows: list = field(default_factory=list)
  pending: dict | None = None
  compared: int = 0
  mismatched: int = 0

  def step(self, t, CC, CS, now_nanos):
    actuators, can_sends = self.controller.update(CC, None, CS, now_nanos)
    if (self.controller.frame - 1) % 4 != 0:
      return
    command = brake_command(can_sends, CanBus.OBSTACLE)
    self.pending = {
      "t": t, "v_ego": CS.out.vEgo, "a_ego": CS.out.aEgo, "long_active": CC.longActive,
      "stopping": CC.actuators.longControlState == "stopping", "brake_test": CC.brakeTestActive,
      "axle_torque_min": CS.axle_torque_min, "accel": CC.actuators.accel,
      "brake_mode": self.controller.owner == LongOwner.BRAKE, "gas": actuators.gas, "brake": actuators.brake,
      "mode": command[0] if command else "",
    }

  def compare(self, logged_gas, logged_brake, logged_mode):
    # card publishes each update's actuatorsOutput at the start of its next iteration.
    if self.pending is None:
      return
    row, self.pending = self.pending, None
    row.update(logged_gas=logged_gas, logged_brake=logged_brake, logged_mode="" if logged_mode is None else logged_mode)
    self.compared += 1
    self.mismatched += (abs(row["gas"] - logged_gas) > 0.5 or abs(row["brake"] - logged_brake) > 0.5 or
                        (logged_mode is not None and row["mode"] != logged_mode))
    self.rows.append(row)


def make_replays(CP, overrides=None):
  if CP.brand != "gm" or not CP.openpilotLongitudinalControl:
    raise SystemExit(f"Not a GM openpilot-longitudinal log: {CP.carFingerprint}")
  # Maneuver mode is not logged; carControl.brakeTestActive was already gated by it upstream.
  CP_SP = structs.CarParamsSP(longitudinalManeuverMode=True)
  replays = []
  for phase in range(4):
    controller = CarController(DBC[CP.carFingerprint], CP, CP_SP)
    controller.frame = phase
    for name, value in (overrides or {}).items():
      if not hasattr(controller.params, name):
        raise SystemExit(f"Unknown CarControllerParams field: {name}")
      setattr(controller.params, name, value)
    replays.append(Replay(controller))
  return replays


def replay(events, overrides=None):
  """events must be re-iterable: carParams is logged rarely, so it is located before replaying."""
  CP = next((event.carParams for event in events if event.which() == "carParams"), None)
  if CP is None:
    raise SystemExit("No carParams in log")
  replays = make_replays(CP, overrides)
  CC, axle_torque_min, logged_mode, t0 = None, float("nan"), None, None
  for event in events:
    kind = event.which()
    if kind == "carControl":
      CC = event.carControl
    elif kind == "can":
      for message in event.can:
        if message.address == AXLE_TORQUE_LIMITS and message.src == CanBus.POWERTRAIN and len(message.dat) >= 4:
          axle_torque_min = int.from_bytes(message.dat[2:4], "big") * 2 - 22534
    elif kind == "sendcan":
      command = brake_command(((m.address, m.dat, m.src) for m in event.sendcan), CanBus.OBSTACLE)
      if command is not None:
        logged_mode = command[0]
    elif kind == "carOutput":
      output = event.carOutput.actuatorsOutput
      for r in replays:
        r.compare(output.gas, output.brake, logged_mode)
    elif kind == "carState" and CC is not None:
      t0 = event.logMonoTime if t0 is None else t0
      CS = SimpleNamespace(out=event.carState, axle_torque_min=axle_torque_min, axle_torque_min_valid=axle_torque_min < 30000,
                           lka_steering_cmd_counter=0, pt_lka_steering_cmd_counter=0,
                           loopback_lka_steering_cmd_updated=False, loopback_lka_steering_cmd_ts_nanos=0)
      for r in replays:
        r.step((event.logMonoTime - t0) * 1e-9, CC, CS, event.logMonoTime)
  return min(replays, key=lambda r: r.mismatched / max(r.compared, 1))


def transitions(rows):
  previous = None
  for row in rows:
    if previous is not None and (row["brake_mode"], row["mode"]) != (previous["brake_mode"], previous["mode"]):
      yield row
    previous = row


def main():
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("log", nargs="+", help="rlog path(s) or route identifier, in order")
  parser.add_argument("--csv", help="write every 25 Hz replay row")
  parser.add_argument("--transitions", action="store_true", help="print ownership and CAN mode changes")
  parser.add_argument("--set", action="append", default=[], metavar="NAME=VALUE",
                      help="override a CarControllerParams field, e.g. --set BRAKE_RELEASE_MARGIN=0.1")
  args = parser.parse_args()

  overrides = {name: ast.literal_eval(value) for name, value in (item.split("=", 1) for item in args.set)}
  best = replay(LogReader(args.log if len(args.log) > 1 else args.log[0], sort_by_time=True), overrides)
  active = [r for r in best.rows if r["long_active"]]
  bad_command = [r for r in active if abs(r["gas"] - r["logged_gas"]) > 0.5 or abs(r["brake"] - r["logged_brake"]) > 0.5]
  bad_mode = [r for r in active if r["logged_mode"] != "" and r["mode"] != r["logged_mode"]]
  bad = sorted(bad_command + [r for r in bad_mode if r not in bad_command], key=lambda r: r["t"])
  print(f"25 Hz updates: {best.compared}, longitudinally active: {len(active)}, "
        f"gas/brake mismatches: {len(bad_command)}, CAN mode mismatches: {len(bad_mode)}")
  if bad:
    print(f"first mismatch at t={bad[0]['t']:.2f}s: replay gas/brake/mode {bad[0]['gas']:.0f}/{bad[0]['brake']:.0f}/{bad[0]['mode']}"
          f" vs logged {bad[0]['logged_gas']:.0f}/{bad[0]['logged_brake']:.0f}/{bad[0]['logged_mode']}")
  positive = [r for r in active if r["brake"] < 0 and not r["brake_test"]]
  print(f"closed-loop positive requests: {len(positive)} updates"
        + (f", largest +{-min(r['brake'] for r in positive):.0f} counts, all in 0xA: {all(r['mode'] == 0xa for r in positive)}" if positive else ""))

  changes = list(transitions(active))
  print(f"ownership/mode changes while active: {len(changes)}")
  if args.transitions:
    for row in changes:
      print(f"t={row['t']:8.2f}s v={row['v_ego']:5.2f} {'brake ' if row['brake_mode'] else 'torque'} accel={row['accel']:+.3f} "
            f"aEgo={row['a_ego']:+.3f} gas={row['gas']:+7.1f} brake={row['brake']:+5.0f} mode=0x{row['mode']:x}")
  if args.csv:
    with open(args.csv, "w", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=COLUMNS)
      writer.writeheader()
      writer.writerows(best.rows)
  return 1 if bad else 0


if __name__ == "__main__":
  sys.exit(main())
