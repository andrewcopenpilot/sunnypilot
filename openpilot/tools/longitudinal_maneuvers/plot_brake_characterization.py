#!/usr/bin/env python3
"""Plot direct brake-characterization trials from local full rlogs (no steady-state fit)."""
import argparse
import csv
import glob
import json
from pathlib import Path

import numpy as np


def extract(events):
  rows = {name: [] for name in ('state', 'control', 'brake', 'pressure', 'output')}
  trials = []
  active = False
  last_time = 0.
  for m in events:
    t = m.logMonoTime * 1e-9
    last_time = max(last_time, t)
    kind = m.which()
    if kind == 'alertDebug':
      a = m.alertDebug
      current = a.alertText2.startswith('brake characterization:') and a.alertText1.startswith('Maneuver Active:')
      if current and not active:
        trials.append({'description': a.alertText2, 'start': t, 'end': None, 'outcome': 'unfinished'})
      elif active and not current:
        trials[-1].update(end=t, outcome=a.alertText1)
      active = current
    elif kind == 'carState':
      c = m.carState
      rows['state'].append((t, c.vEgo, c.aEgo, c.vEgoRaw, c.gasPressed, c.brakePressed))
    elif kind == 'carControl':
      c = m.carControl
      rows['control'].append((t, c.brakeTestCommand, c.brakeTestActive, c.longActive))
    elif kind == 'carOutput':
      rows['output'].append((t, m.carOutput.actuatorsOutput.gas))
    elif kind in ('can', 'sendcan'):
      for c in getattr(m, kind):
        data = bytes(c.dat)
        if kind == 'sendcan' and c.src == 1 and c.address == 0x315 and len(data) >= 5:
          encoded = ((data[0] & 15) << 8) | data[1]
          demand = -(encoded - 4096 if encoded >= 2048 else encoded)
          rows['brake'].append((t, demand, data[0] >> 4))
        elif kind == 'can' and c.src == 2 and c.address == 0x170 and len(data) >= 4:
          rows['pressure'].append((t, int.from_bytes(data[2:4], 'big')))
  if active:
    trials[-1]['end'] = last_time
  arrays = {}
  for key, values in rows.items():
    a = np.asarray(values, dtype=float)
    arrays[key] = a[np.argsort(a[:, 0], kind='stable')] if len(a) else a
  return arrays, trials


def sample(array, times, columns):
  if not len(array):
    return np.full((len(times), columns), np.nan)
  indices = np.searchsorted(array[:, 0], times, side='right') - 1
  result = array[np.maximum(indices, 0), 1:].copy()
  result[indices < 0] = np.nan
  return result


def trial_samples(arrays, trial):
  brake = arrays['brake']
  if not len(brake):
    return np.empty((0, len(COLUMNS)))
  brake = brake[(brake[:, 0] >= trial['start']) & (brake[:, 0] < trial['end'])]
  t = brake[:, 0]
  return np.column_stack((t - trial['start'], sample(arrays['control'], t, 3), brake[:, 1:],
                          sample(arrays['state'], t, 5), sample(arrays['pressure'], t, 1), sample(arrays['output'], t, 1)))


COLUMNS = ['seconds', 'requested_counts', 'test_requested', 'long_active', 'sent_counts', 'brake_mode',
           'speed_m_s', 'accel_m_s2', 'raw_speed_m_s', 'gas_pressed', 'brake_pressed', 'pressure_raw', 'gas_regen_nm']


def write_report(arrays, trials, output):
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt

  if not trials:
    raise ValueError('No brake-characterization trials found; this report needs the direct-command sweep logs.')
  output.mkdir(parents=True, exist_ok=True)
  (output / 'trials.json').write_text(json.dumps(trials, indent=2))
  plt.rcParams.update({'font.size': 10, 'axes.grid': True, 'grid.alpha': 0.25})
  response, response_axes = plt.subplots(3, 1, figsize=(11, 11), sharex=True)
  for i, trial in enumerate(trials, 1):
    values = trial_samples(arrays, trial)
    if not len(values):
      continue
    with (output / f'trial_{i}.csv').open('w') as f:
      writer = csv.writer(f)
      writer.writerow(COLUMNS)
      writer.writerows(values)
    # Plot all samples inside the measured interval, including any terminal stop command.
    t, requested, _, _, sent, mode, speed, accel, raw, _, _, pressure, gas = values.T
    fig, axes = plt.subplots(4, 1, figsize=(11, 11), sharex=True)
    axes[0].plot(t, requested, label='Requested count ramp')
    axes[0].step(t, sent, where='post', label='Actual CAN counts')
    axes[0].step(t, mode, where='post', label='CAN brake mode', alpha=0.5, ls=':')
    axes[0].set_ylabel('Counts / mode')
    axes[1].plot(t, speed, label='Filtered speed')
    axes[1].plot(t, raw, label='Raw speed', alpha=0.6)
    axes[1].set_ylabel('m/s')
    axes[2].plot(t, accel, label='Measured acceleration')
    axes[2].axhline(0., color='black', ls=':')
    axes[2].set_ylabel('m/s²')
    axes[3].plot(t, pressure, label='Brake pressure signal (raw)')
    axes[3].set_ylabel('Raw units')
    axes[3].set_xlabel('Seconds from trial entry')
    for ax in axes:
      ax.legend()
    fig.suptitle(f"Trial {i}: {trial['description']}\n{trial['outcome']}", fontsize=11)
    fig.tight_layout()
    fig.savefig(output / f'trial_{i}.png', dpi=140)
    fig.savefig(output / f'trial_{i}.pdf')
    plt.close(fig)
    # Only valid direct-command samples belong on the command-response plot.
    measured = ((values[:, 2] == 1) & (values[:, 3] == 1) & np.isin(mode, (10, 11)) &
                (sent >= 0) & (sent <= 12) & (values[:, 9] == 0) & (values[:, 10] == 0))
    for ax, column in zip(response_axes, (6, 7, 11), strict=True):
      ax.plot(sent[measured], values[measured, column], '.-', ms=2, lw=0.7, label=f'Trial {i}')
    print(f"Trial {i}: {t[-1]:.2f}s, max sent {sent.max():g} counts, gas/regen {np.nanmin(gas):g}..{np.nanmax(gas):g} Nm | {trial['outcome']}")
  for ax, label in zip(response_axes, ('Speed (m/s)', 'Acceleration (m/s²)', 'Pressure signal (raw)'), strict=True):
    ax.set_ylabel(label)
    ax.legend()
  response_axes[-1].set_xlabel('Actual EBCM brake command (counts)')
  response.suptitle('Brake response by command — transient sweeps, not a steady-state calibration')
  response.tight_layout()
  response.savefig(output / 'command_response.png', dpi=140)
  response.savefig(output / 'command_response.pdf')
  plt.close(response)


def main():
  import zstandard as zstd
  from openpilot.cereal import log

  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('rlogs', help='Quoted glob for local rlog.zst files from one route')
  parser.add_argument('--output', type=Path, default=Path('brake_characterization_report'))
  args = parser.parse_args()
  paths = sorted(glob.glob(args.rlogs), key=lambda p: int(Path(p).parent.name.rsplit('--', 1)[-1]))
  if not paths:
    parser.error('No rlogs matched')

  def events():
    for path in paths:
      with zstd.ZstdDecompressor().stream_reader(Path(path).read_bytes()) as reader:
        data = reader.read()
      yield from log.Event.read_multiple_bytes(data)

  arrays, trials = extract(events())
  write_report(arrays, trials, args.output)
  print(f'Report: {args.output.resolve()}')


if __name__ == '__main__':
  main()
