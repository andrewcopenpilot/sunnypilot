# ASCM longitudinal control inputs — 2026-09-18

Scope: the acceleration-feedback, actuator-allocation and torque-output path
rooted at `FUN_00139d80`, plus the preparation of its inputs in `FUN_00131440`
and `FUN_001344b0`. This is an evidence inventory, not a claim that every status
bit or upstream estimator has been fully decoded. Function addresses refer to
ASCM MPU1 OS `84876565.bin`.

Design constraint: use feedback signals traced into the ASCM longitudinal loop.
Do not add hydraulic pressure as a production feedback or handoff input on the
current evidence. It remains useful for analyzing test logs.

## Confirmed numeric inputs

| Input | Source / entry | Use in the traced controller |
|---|---|---|
| Vehicle speed | `c0de0` → `4001d998`; published by vehicle-state routine `dce50` | Speed scheduling, torque-to-acceleration conversion and low-speed behavior |
| Vehicle longitudinal acceleration | `c0d50` → `4001d99a` (also copied into `4001d99c`); publisher `dce50` | Acceleration error in `13a5d0`, response history, speed prediction |
| Actual axle torque | `c5430` → `4001dc96/98`; CAN `0x1C5` | Capability preparation: `139ce0` compares actual with minimum; `139b50` converts the adjusted actual-torque value into acceleration |
| Minimum available axle torque | `c5480` → `4001dc92`; CAN `0x1C5` | Minimum-powertrain capability, allocation boundary, torque initialization at handoff |
| Maximum available axle torque | `c5c10` → `4001dc94`; CAN `0x1C5` | Maximum-powertrain capability (`139950`) and feedback limiting |
| Engine rotational speed | `c5b90` → `4001dc9a`; `4a320`/`798b0`, CAN `0x0C9` | Engine/wheel ratio calculation in `139c10`; state-dependent, with fallback behavior |
| Two rear wheel speeds, each with validity | `c5de0/c5d90`, validity `c5e10/c5dc0`; CAN `0x34A` | `134390` averages valid wheels (or uses the one valid wheel), converts to rotation using tire circumference, stores `4001dc9c` for `139c10` |

The vehicle speed and acceleration getters read ASCM vehicle-state outputs.
Their underlying estimation/filtering is not fully traced here. Do not assume
that raw CAN acceleration, differentiated wheel speed, and openpilot `aEgo`
are interchangeable just because they describe the same physical quantity.

The engine-speed input is present in this firmware's general controller path;
that does not establish that its ratio branch matters in every Volt EV state.
Likewise, inclusion here is permission to investigate an input, not a reason to
make every one mandatory for our first creep change.

## Requests and discrete inputs

| Input group | Evidence | Qualification |
|---|---|---|
| Candidate acceleration requests and request state | `131440` → `1397c0` → request block `4001dc80`; selection in `13ade0` | Upstream ACC intent, not a measured actuator signal; multiple states/requests, not just the sign of acceleration |
| Gear / transmission state | `c5bc0` from `4a560`, CAN `0x1F5`; state bytes at `4001dc9e/9f` | Conditions model/transition processing; some branches depend on calibration |
| EBCM one-bit status | `483b0` → `c34d0` → vehicle-state flags in `131440` | CAN `0x170`, byte 1 bit 1; physical meaning not fully recovered |
| EBCM two-bit status | `48440` → `c2f20` → vehicle-state flags in `131440` | CAN `0x170`, byte 0 bits 0–1; compared with state 3; physical meaning not fully recovered |
| Other upstream enable/transition/validity flags | `c0c10`, `c0ff0`, `c1050`, `bfc80/bfca0/bfcc0/bfce0` and precomputed `4001d9xx` flags | Consumption is established; exact naming and mapping are incomplete. Do not assign pedal/ABS/hold meanings without tracing each bit |

Previous actuator mode, previous gear state, and stop/hold-related request state
also influence the loop. They are not hydraulic pressure feedback. Existing
openpilot engagement and driver-override handling still applies; this inventory
addresses the inputs to the proposed control strategy.

## Derived state and unresolved inputs

| State/input | What is established | What remains unresolved |
|---|---|---|
| Filtered acceleration-difference correction `4001d8f4` | `1344b0` filters `1000*c32d0() - 4001d938`; `132a60` supplies the latter from `c0d50`. Used in gain scheduling and actuator selection/output processing | CAN source now traced to the eight-byte `0x140` message (see update below); transmitting ECU and physical definition remain unresolved |
| Additional dynamics input `c1250` | Scaled by 1000 and compared with thresholds alongside `4001d8f4` to build state `4001d8f2` | Physical definition; publisher `e31f0` reads `40011004`. Do not call it pitch or grade yet |
| Expected/minimum/maximum acceleration | Torque conversion using vehicle parameters and speed (`139b50/139950/1399a0`) | Exact suitability of stock calibration at our very low creep speeds |
| Filtered request, PI state, response history, mode timers | `13a5d0`, `13afc0`, `13b6c0`, `13b910` | Some state meanings and conditions remain undecoded |
| Vehicle model/calibration | Model block `4001e148`, tire circumference, conversion factors and calibrated tables | Parameters and internal learned state are not additional sensor requirements |

Stock clamps the minimum-torque intermediate to −5000…0 in this calibration
(offsets `0x68e/0x690`). Using positive AxleTorqueMin to model creep is therefore
an extension using an OEM input, not a recovered stock rule.

## Hydraulic pressure: specific trace

The local chassis DBC identifies CAN `0x170` bytes 2–3 as
`FrictionBrakePressure` (`23|16@0+`). The ASCM receive map places this message at
`40004fc0`, making those bytes `40004fc2/3`.

- The direct references found to those bytes are bulk copies `81310` and `81350`.
- Their callers `48310` and `48270` decode signed 12-bit values via `79a40`
  (bytes 4–5) and `79a70` (bytes 6–7), scaled by 0.01. These are different fields
  from the DBC pressure value; their physical meanings are not assumed here.
- Their validity accessors `77210/77240` read bits in bytes 0–1.
- The additional staged-buffer consumer `8cf60` also uses `79a70`, not pressure.
- Direct references to the copied pressure-byte addresses were absent in this
  check. The EBCM statuses traced into `131440` are the separate bit fields
  listed above.

Conclusion: no numeric hydraulic-pressure feedback path into the traced ASCM
longitudinal loop was established. Receiving/copying the message is not evidence
of using pressure in that loop. Static references do not prove the absence of
every possible indirect access, so this is deliberately narrower than claiming
that pressure is unused everywhere in the firmware.

## Source record and next design step

Existing decompilations:
`/home/acremins/volt_reverse_engineering/ASCM/decoded/ghidra_longitudinal/mpu1/`.
New read-only Ghidra exports and getter maps:
`/home/acremins/volt_reverse_engineering/ASCM/decoded/control_inputs_20260918/`.
The receive mapping is `ASCM/decoded/ascm_rx_list.txt`; the older `rxmap.txt`
uses a different indexing assumption and must not be used for these CAN IDs.

Use speed, acceleration, axle-torque capability, request state, mode history and
hysteresis as the starting architecture. Trace `c32d0` and `c1250` before choosing
an OEM-equivalent slope/disturbance input. Feedback/state coordination can be
improved without adding pressure. This inventory supersedes the earlier
pressure-supervised handoff recommendation in `SIGNED_BRAKE_CONTROL_OPTIONS.md`.

## Follow-up: origins of the two dynamics inputs

`c32d0` has a concrete CAN input path:

```
8-byte CAN 0x140, buffer 40004fb8
  -> 81410 copies bytes 2–5 into 400048a4
  -> 79b00 extracts the low 12 bits of original bytes 4–5
  -> 484c0 sign-extends and scales by 1/64 into 40008b28
  -> 9d0f0(2) / c32c0 publish it for c32d0
  -> 1344b0 uses it in the filtered acceleration difference
```

The decoded validity bit is original byte 2 bit 5. The transmitting ECU is not
identified by this receive-side trace. The receive list's `BCMTurnSignals` label
must not be trusted for this eight-byte entry: there is a separate three-byte
`0x140` entry at `400050e0`. Matching an ID across buses is not sender evidence.
The older notes' attribution of `40008b28` to MPU2 IPC is not supported by this
newly traced CAN path and should not be used as the source conclusion.

`c1250` is published from `40011004` by `e31f0`. Its callers (`e3260`, `e32e0`,
`e2f90`) execute local ASCM processing before publication. The regular path is
`e3050` (gather inputs) -> `dfe90` (calculation) -> `e31f0` (publish). This points
to an ASCM-computed quantity, rather than a single directly decoded CAN field;
its exact output-pointer mapping, physical meaning, and contributing sensor
sources still need tracing. No external sending ECU has been established for
that derived quantity.

Evidence is preserved in the `ascm_dynamics_*_20260918` subdirectories of the
source record above. No controller or parser behavior was changed.

Turn-signal cross-check: `49d90` extracts a two-bit state from `400050e2`
(original byte 2 bits 3–2) and publishes it through `c58c0`. This matches the
three-byte powertrain DBC `BCMTurnSignals.TurnSignals` field (`19|2@0+`).
It is a separate decoder/buffer from the signed 12-bit dynamics field in the
eight-byte receive entry. Turn-signal-based overtaking behavior remains plausible
upstream ACC behavior, but its downstream use was not traced in this check and
does not identify the signed dynamics field. The firmware exports are preserved
in `ascm_turn_signal_check_20260918` alongside the other evidence.

## Firmware audit follow-up

[ASCM_FIRMWARE_AUDIT.md](ASCM_FIRMWARE_AUDIT.md) resolves `c1250` to the filtered
residual output of `dfad0`, including its output-pointer mapping, wheel-processing
comparison inputs and 10 ms schedule. Physical grade/slope units remain unproven.
The −1 dynamics class is prohibited below **40 km/h**, so its special gain/slew
branches cannot activate at creep speeds in this calibration.

The formerly unresolved `4001dcc0` stop flags are **first-object record flags**
written through pointer `4001d7e0 -> 4001dcb0`. They derive from the first incoming
object's state byte +0x3c, with a sticky 2→1 transition. The audit includes the
producer chain and corrects the earlier direct-reference scan's incomplete result.

The same audit establishes the per-cycle model reload, inactive auxiliary/rate
feedback terms, complete request/allocation/hold predicates, and final brake
publication shaping. These findings supersede the corresponding open questions
in this earlier input inventory.

## Dynamics/source and hold-label follow-up

[The follow-up](ASCM_DYNAMICS_AND_OUTPUTS.md) corrects the earlier bf9b0 path:
it uses `cbc10 -> cbdb0 -> cc070/cbf30 -> cc8e0`, not neighboring `cb120`. Both
classifier inputs share c32d0 as a sensor source. The residual compares its
conditioned, initialized-bias-subtracted output with wheel acceleration. The
initialized bias has a stored-record read/write path.

The extended receive table also resolves c61d0 to the driver-door-open signal
(filter key 0x00630000, corroborated DBC ID 0x10630000, byte0 bit0). The other
two hold fields now have precise masked receive keys and payload bits, while
their physical labels remain open. See the linked follow-up for mappings and
validity qualifications.
