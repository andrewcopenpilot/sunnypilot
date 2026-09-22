#!/usr/bin/env python3
"""Plot recovered ASCM ramp limits and illustrative scalar responses, not a drive.

Requires matplotlib. Calibration identity and table bytes are checked against
ascm_reference_evidence/evidence.json. Uses the reference's integer arithmetic.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import struct

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from ascm_loop_reference import stock_integer_slew, stock_lookup

ROOT = Path(__file__).resolve().parent


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  fw_root = Path(os.environ.get('ASCM_FIRMWARE_ROOT', str(Path.home() / 'volt_reverse_engineering/ASCM')))
  parser.add_argument('--calibration', type=Path, default=fw_root / 'decoded/23366550.bin')
  parser.add_argument('--output', type=Path, default=ROOT / 'ascm_ramp_reference')
  args = parser.parse_args()
  manifest = json.loads((ROOT / 'ascm_reference_evidence/evidence.json').read_text())
  blob = args.calibration.read_bytes()
  digest = hashlib.sha256(blob).hexdigest()
  if digest != manifest['firmware']['23366550.bin']:
    raise ValueError('Expected the audited ACC calibration 23366550')
  cal = blob[0xa0:]
  tables = {}
  for key, expected in manifest['tables_raw'].items():
    offset = int(key, 16)
    actual = [list(struct.unpack_from('>hh', cal, offset + 4 * i)) for i in range(len(expected))]
    if actual != expected:
      raise ValueError(f'Table bytes differ from evidence at {key}')
    tables[offset] = tuple(tuple(pair) for pair in actual)

  def scalar(offset, fmt='h'):
    return struct.unpack_from('>' + fmt, cal, offset)[0]

  def lookup(offset, argument):
    return stock_lookup(tables[offset], argument)

  output = args.output
  output.mkdir(parents=True, exist_ok=True)
  plt.rcParams.update({'font.size': 10, 'axes.titlesize': 12, 'axes.titleweight': 'bold',
                       'axes.spines.top': False, 'axes.spines.right': False, 'figure.facecolor': 'white',
                       'axes.grid': True, 'grid.alpha': 0.18, 'lines.linewidth': 2})
  blue, orange, green = '#1764a0', '#c05a15', '#227b51'
  dt_ms = 40
  speeds_raw = list(range(0, 3001, 5))
  speed_kph = [v * 0.036 for v in speeds_raw]

  def table_curve(ax, offset, scale, label, color):
    ax.plot(speed_kph, [lookup(offset, v) / scale for v in speeds_raw], color=color, label=label)
    ax.scatter([x * 0.036 for x, _ in tables[offset]], [y / scale for _, y in tables[offset]], color=color, s=22, zorder=3)
    ax.set_xlabel('Vehicle speed (km/h)')
    ax.set_xlim(0, 108)

  def save(fig, name, footer):
    fig.text(0.5, 0.012, footer, ha='center', va='bottom', fontsize=9, color='#444444')
    fig.tight_layout(rect=(0, 0.055, 1, 0.94), h_pad=2.5, w_pad=2.5)
    for suffix in ('png', 'svg'):
      fig.savefig(output / f'{name}.{suffix}', dpi=160)
    plt.close(fig)

  fig, axes = plt.subplots(2, 2, figsize=(12, 8))
  fig.suptitle('ASCM friction-brake request shaping — ACC calibration 23366550', fontsize=16, y=0.985)
  ax = axes[0, 0]
  table_curve(ax, 0x810, 1000, 'Increasing acceleration / releasing braking', blue)
  ax.plot(speed_kph, [-lookup(0x810, v) / 1000 for v in speeds_raw], color=orange, label='Decreasing acceleration / adding braking')
  ax.set(title='1. Ordinary brake ramp: table 0x810', ylabel='Acceleration change rate (m/s³)', ylim=(-6.5, 6.5))
  ax.text(54, 0, '±5 m/s³ = ±0.20 m/s² per 40 ms\nAlready-braking branch only', ha='center', va='center')
  ax.legend(loc='center', bbox_to_anchor=(0.5, 0.75), fontsize=8)
  ax = axes[0, 1]
  table_curve(ax, 0x5F6, 1000, 'Lower envelope (0x5f6)', blue)
  ax.axhline(2, color=orange, label='Upper envelope (+2.0 m/s²)')
  ax.set(title='2. Final envelope target', ylabel='Acceleration (m/s²)', ylim=(-5.8, 2.8))
  ax.legend(loc='lower right', fontsize=8)
  ax.text(52, 0, 'Used to form a target; publication\napproaches it by at most 0.40 m/s² per call.', ha='center')

  ax = axes[1, 0]
  times, targets, commands = [0.0], [-0.5], [-0.5]
  previous = -500
  for tick in range(1, 66):
    target = -500 if tick < 10 else -3000 if tick < 35 else -1000
    previous = stock_integer_slew(target, previous, -lookup(0x810, 500), lookup(0x810, 500), dt_ms)
    times.append(tick * dt_ms / 1000)
    targets.append(target / 1000)
    commands.append(previous / 1000)
  ax.step(times, targets, where='post', color=orange, linestyle='--', label='Brake target after feedback/correction')
  ax.step(times, commands, where='post', color=blue, label='Ordinary ramp output')
  ax.set(title='3. Example at 18 km/h, already braking', xlabel='Time (s)', ylabel='Acceleration (m/s²)')
  ax.legend(loc='upper right', fontsize=8)

  ax = axes[1, 1]
  inputs = list(range(-6000, 3001, 10))
  envelope_rate = scalar(0x620)
  def publish(value, speed):
    target = min(max(value, lookup(0x5F6, speed)), 2000)
    return stock_integer_slew(target, value, -envelope_rate, envelope_rate, dt_ms)
  ax.plot([a / 1000 for a in inputs], [a / 1000 for a in inputs], color='#999999', linestyle=':', label='Unchanged')
  ax.plot([a / 1000 for a in inputs], [publish(a, 0) / 1000 for a in inputs], color=blue, label='Published value at 0 km/h')
  ax.scatter([-3], [-2.6], color=orange, zorder=4)
  ax.annotate('−3.0 → −2.6\n(lower envelope is −1.5)', (-3, -2.6), xytext=(-1.8, -4.5),
              arrowprops={'arrowstyle': '->', 'color': orange}, fontsize=9)
  ax.set(title='4. Final envelope: one-call input/output', xlabel='THIS cycle’s allocation result (m/s²)', ylabel='Published brake acceleration (m/s²)')
  ax.legend(loc='upper left', fontsize=8)
  save(fig, 'friction_brake_ramps', 'Panel 3 isolates the ramp with supplied targets; no vehicle/PI simulation. Mode 0xB has no separate ramp table.')

  fig, axes = plt.subplots(1, 2, figsize=(12, 5.4))
  fig.suptitle('ASCM additional rate limits', fontsize=16, y=0.985)
  ax = axes[0]
  table_curve(ax, 0x6E4, 1, 'Normal upward limit (0x6e4)', blue)
  table_curve(ax, 0x6F0, 1, 'Conditional class −1 upward limit (0x6f0)', orange)
  ax.set(title='Primary torque: upward ramp tables', ylabel='Torque increase limit (Nm/s)', ylim=(0, 1200))
  ax.text(54, 300, f'Downward limit: {scalar(0x6DC, "i")} Nm/s\nContinuing torque: filter first, then slew.\nTorque entry uses a separate seed.',
          ha='center', fontsize=9)
  ax.legend(loc='upper right', fontsize=8)
  ax = axes[1]
  labels = ['Ordinary brake\n(table 0x810)', 'Envelope approach\n(cal 0x620)', 'Capability override\ntoward minimum', 'Second override step\ntoward maximum']
  lower = [-lookup(0x810, 0), -envelope_rate, scalar(0x6D8, 'i'), -scalar(0x6D0, 'i')]
  upper = [lookup(0x810, 0), envelope_rate, scalar(0x6D4, 'i'), scalar(0x6D0, 'i')]
  for i, (lo, hi) in enumerate(zip(lower, upper, strict=True)):
    ax.barh(i, lo / 1000, color=orange, height=0.5)
    ax.barh(i, hi / 1000, color=blue, height=0.5)
    ax.text(lo / 1000 - 0.25, i, f'{lo / 1000:g}', ha='right', va='center')
    ax.text(hi / 1000 + 0.25, i, f'+{hi / 1000:g}', ha='left', va='center')
  ax.set_yticks(range(4), labels)
  ax.invert_yaxis()
  ax.set(title='Acceleration rate limits by branch', xlabel='Acceleration change rate (m/s³)', xlim=(-12, 12))
  ax.axvline(0, color='#444444', linewidth=0.8)
  save(fig, 'other_ramps', 'The envelope starts from the current allocation value; the other acceleration ramps use the states described in ASCM_RAMPS.md.')

  fig, axes = plt.subplots(1, 2, figsize=(12, 5.4))
  fig.suptitle('ASCM related tables — request scaling and allocation margins', fontsize=16, y=0.985)
  ax = axes[0]
  low_speeds = list(range(401))
  ax.step([v / 100 for v in low_speeds], [lookup(0x7DE, v) / 1000 for v in low_speeds], where='post',
          color=orange, label='Request bit28: 0x7de (predicted speed)')
  ax.plot([v / 100 for v in low_speeds], [lookup(0x7EA, v) / 1000 for v in low_speeds],
          color=blue, label='Else bit27 + prior request >0: 0x7ea')
  ax.set(title='Request multipliers, not time ramps', xlabel='Lookup speed (m/s)', ylabel='Selected request multiplier', ylim=(0, 4.5))
  ax.text(2.55, 2.4, '0x7de preserves stored order:\n1.0 at speed ≤2 m/s;\n0.1 above 2 m/s.', fontsize=9, ha='center')
  ax.legend(loc='upper right', fontsize=8)
  ax = axes[1]
  margin_curves = [(0x708, 'Previous owner = brake', blue), (0x714, 'Other owner: normal', orange),
                   (0x720, 'Other owner: conditional class −1', green)]
  for offset, label, color in margin_curves:
    table_curve(ax, offset, 1000, f'{label} (0x{offset:x})', color)
  ax.axhline(0, color='#888888', linewidth=0.8)
  ax.set(title='Brake/torque boundary margins', ylabel='Acceleration margin (m/s²)', ylim=(-0.25, 0.32))
  ax.legend(loc='upper right', fontsize=8)
  save(fig, 'request_and_allocation_tables',
       'Boundary also includes minimum powertrain acceleration, weighted dynamics correction and a request-state margin. No inferred physical class names.')

  with (output / 'table_points.csv').open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['offset', 'speed_m_s', 'value', 'value_unit'])
    for offset, scale, unit in [(0x810, 1000, 'm/s^3'), (0x5F6, 1000, 'm/s^2'), (0x6E4, 1, 'Nm/s'),
                               (0x6F0, 1, 'Nm/s'), (0x7DE, 1000, 'multiplier'), (0x7EA, 1000, 'multiplier'),
                               (0x708, 1000, 'm/s^2'), (0x714, 1000, 'm/s^2'), (0x720, 1000, 'm/s^2')]:
      for x, y in tables[offset]:
        writer.writerow([f'0x{offset:x}', x / 100, y / scale, unit])
  with (output / 'brake_step_example.csv').open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time_s', 'target_m_s2', 'ordinary_ramp_output_m_s2'])
    writer.writerows(zip(times, targets, commands, strict=True))
  (output / 'provenance.json').write_text(json.dumps({
    'calibration': '23366550.bin', 'sha256': digest, 'dt_ms': dt_ms,
    'scalar_raw': {f'0x{off:x}': scalar(off, fmt) for off, fmt in [(0x620, 'h'), (0x6DC, 'i'), (0x6D0, 'i'), (0x6D4, 'i'), (0x6D8, 'i')]},
    'example_scope': 'Scalar ramp only; supplied target, fixed speed, continuing brake branch, no feedback or vehicle dynamics.',
  }, indent=2) + '\n')
  # Sanity checks for the plotted examples and the exceptional descending table.
  assert lookup(0x7DE, 200) == 1000 and lookup(0x7DE, 201) == 100
  assert publish(-3000, 0) == -2600
  assert max(abs(b - a) for a, b in zip(commands[:-1], commands[1:], strict=True)) <= 0.200000001
  print(f'Wrote three PNG/SVG figures, two CSV files and provenance to {output}')


if __name__ == '__main__':
  main()
