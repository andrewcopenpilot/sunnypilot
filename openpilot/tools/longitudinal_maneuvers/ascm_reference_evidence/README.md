# Reproducible ASCM reference evidence

See [the audit](../ASCM_FIRMWARE_AUDIT.md) for conclusions and limits.

- `evidence.json`: SHA-256 identities, typed calibration values and startup-copy mapping.
- `exports/`: selected unmodified Ghidra exports; recovered upstream switch is
  explicitly named `FUN_00138c90_recovered.c`.
- `assembly.txt`: assembly checks for argument registers, signed loads, cycle
  ordering, the model reload, object-record writes and recovered state machine.
- `RecoverASCMState.java`: restores initialized data from the flash descriptor
  **in the analysis session**, exposes the RAM jump table and expands function
  `138c90` to its actual body. Always invoke with `-readOnly -noanalysis`.
- `verify_reference.py`: 80,000 seeded comparisons of translated Python against
  native compilation of recovered C routines and integer helpers, plus 6,000
  successive request/feedback/allocation cycles with carried state.

Run checks from the repository:

```sh
python3 openpilot/tools/longitudinal_maneuvers/ascm_reference_evidence/verify_reference.py
```

Requirements: Linux, Python 3, gcc, and ACC calibration
`~/volt_reverse_engineering/ASCM/decoded/23366550.bin`.
Set `ASCM_FIRMWARE_ROOT` to the ASCM directory if located elsewhere. The harness
maps private emulated RAM at 0x40000000 in its own process and writes temporary
compiler artifacts into a fresh temporary directory. It does not execute the
PowerPC firmware or communicate with a vehicle.

Checks: 20,000 allocation/submode snapshots, 10,000 request selections,
10,000 hold-latch snapshots, 20,000 model conversions and 10,000 feedback
snapshots, plus 10,000 auxiliary numeric-output comparisons against 13a180. Cases include boundary equalities, negative/positive requests,
owner changes, submode interlocks, raw flag combinations and retained state.
They are deterministic (seed 84876565), not an observed stock-drive trace.

The native harness supplies ordinary C types and memory access for Ghidra's
synthetic types. Helpers compare **signed 32-bit** values as the firmware does.
Two request-selector decompiler defects are repaired from assembly: missing
arguments to max at `13aec6`, and signed predicted-speed load at `13aefc`.
The omitted auxiliary-integral table argument is supplied as speed; that path
is bounded to zero by `0x762`, so its table argument cannot affect the compared
output. No claim is made about that supplied argument in other calibrations.
The harness does not validate unknown physical names, all overflow cases,
request-planner reachability, scheduling, or an end-to-end firmware simulation.

Recover the upstream switch in the existing project (adjust tool/project paths):

```sh
JAVA_HOME=/home/acremins/tools/jdk-21.0.12.1+1 \
/home/acremins/tools/ghidra_12.1.2_PUBLIC/support/analyzeHeadless \
  /home/acremins/ghidra_projects gm_ascm -process 84876565.bin \
  -readOnly -noanalysis \
  -scriptPath openpilot/tools/longitudinal_maneuvers/ascm_reference_evidence \
  -postScript RecoverASCMState.java /tmp/ascm_loop_state_recovered.c
```

The table's flash bytes and address translation are supported by the actual
startup descriptor, not inferred solely by finding plausible code addresses.
The existing Ghidra project and firmware files were left unchanged.

## Dynamics/output follow-up

[The follow-up](../ASCM_DYNAMICS_AND_OUTPUTS.md) corrects the bf9b0 source branch,
resolves the uncompensated/compensated output distinction, and identifies a raw
block-transfer consumer for the auxiliary and ratio values. `evidence.json`
includes the added calibration identity/values and transfer-table record.
`dynamics_output_assembly.txt` preserves stack-argument checks and scheduling;
`output_references.txt` and `output_table_references.txt` record reference-scan
coverage. Added exports are unmodified Ghidra output, including its incomplete
SPE call signatures; consult the assembly before treating them as compilable C.

The reference scans used `FindRefsInRange.java` from the local ASCM
`ghidra_scripts` directory with a 15-second per-function decompile timeout.
Ranges were `4001d7d0-4001db00` (with initialized RAM restored) and
`14d400-14d700`, respectively, in read-only/no-analysis sessions. No selected
function failed to export. The scan is evidence about recognized references,
not an exhaustive proof about arbitrary computed pointers.

The added sequential check preserves request/PI/history, owner/latch and
submode state across 6,000 calls. It covers every request state, owner and
submode. Its external hold, capabilities, torque and sensor values are
synthetic; it does not execute the supervisor, sensor estimator, torque output
stage or final caller envelope. It therefore checks composition of these
three stages rather than claiming a whole-vehicle drive simulation.

`extended_receive_map.json` decodes the 39 previously unlisted extended CAN
filters and records the software ID mask. `hold_receive_assembly.txt` includes
that mask and the hold-gate argument checks. The manifest records the local
DBC identity used to corroborate the door-open signal, and the storage
descriptors/defaults for sensor bias record 100 and transfer-enable record 8.

## Readable-code additions

The new sensor conditioning, bias split and residual recurrence have illustrative
regressions for retention/reacceptance, product-before-sum clamping, branch
separation, initialization and unclamped versus final filter state. These do
**not** add recovered-C or float32-equivalence coverage for sensor processing.
Hold-input enums and the ratio output have illustrative boundary examples.

The additional 10,000 auxiliary checks compare `auxiliary_torque_number` with
full recovered `13a180`, exercising both ordinary/hold branches, all previous
and current owners, and both slew settings. They compare the numeric field;
they do not claim the excerpt implements that routine's flag23/timer effects.

`auxiliary_signed_assembly.txt` records the signed argument extensions omitted
by Ghidra's `undefined2` types: model result at 13a25e/13a2e4/13a30c, brake
acceleration/speed at 13a2d4/13a2da, and -40 ceiling at 13a2f0. The harness
restores signed short types at these calls; the saved C export is unchanged.
Without those ABI repairs, native C treats negative torque as a large positive
value and the new numeric comparison fails.
