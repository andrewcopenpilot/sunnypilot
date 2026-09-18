# ASCM transitions into and out of brake mode 0xB

Firmware review, 2026-09-17. This review changes no controller, calibration, or
maneuver behavior. It extends [the control-loop review](ASCM_CONTROL_REVIEW.md).
The mode-0xA characterization override was already present before this review.

## Main finding

Stock separates ordinary brake control from the submode encoded as **0xB**.
Low speed alone does not select 0xB. Separate state conditions select it, and the
ordinary brake-to-torque release path explicitly checks the **previous submode**.
A positive acceleration request alone therefore does not necessarily release 0xB.

This supports treating moving creep and intentional stopping separately. It is
consistent with the hypothesis that 0xB invokes EBCM stop behavior, but ASCM code
cannot establish the EBCM's internal control law.

## Encoding and timing

`0013afc0` selects an outer actuator mode and a brake submode independently:

- Outer mode: 0 = off, 1 = torque, 2 = brake.
- Submode: 1, 2, 3, 4, or 5.
- CAN mode nibble = `(brake_active << 3) | submode`.

Consequently, active submodes 2/3/4/5 encode as **0xA/0xB/0xC/0xD**. Submode 1
can encode as **0x9**, not just 0x1; it depends on the independently generated
active bit. Do not assume every submode-1 transition means brake deactivation.

The ACC arithmetic runs with a **40 ms** step: `0012dce0` invokes `00130cc0(40)`
and `00131440(40)`. The output state is rooted at `4001dae4`; outer mode is byte
`+0xA`, submode byte `+0xE`. `00131440` exports submode through `000c2810` and active
through `000c26b0`; MPU1 `000b2390` carries these through IPC, and MPU2 `00048420`
packs the brake message using getters `00047c30` and `00047c70`.

## Entry conditions, in priority order

The following table describes the final submode selection in `0013afc0`, after
that function has selected or retained the outer actuator mode. Names such as
“hold” and “stop qualifier” describe inferred roles, not recovered OEM symbols.

| Priority | Condition | Selected submode / active encoding |
|---|---|---|
| 1 | Outer mode is not brake | 1; active encoding depends on the output-active timer |
| 2 | Cruise main is off, or a separate internal suppression condition is true | 1; normally 0x9 while outer mode remains brake |
| 3 | Internal hold flag is set and speed is below 1.5 m/s | 4 or 5: 0xC or 0xD |
| 4 | Stop qualifier is true, previous outer mode was brake, and the history gate permits it | 3: 0xB |
| 5 | Otherwise | 2: 0xA |

With the dumped calibration, the stop qualifier is:

```text
(speed < 1.5 m/s AND internal_flag_27)
OR (speed < 1.5 m/s AND internal_flag_28)
OR (speed < 1.5 m/s AND OEM_CruiseState == 4 [Standstill])
OR (special_speed_timer == 0)
```

The speed comparisons are strict `<`; 1.5 m/s is approximately **3.36 mph**.
The special timer is an exception to the speed-qualified branches, but does not
normally expire during forward creep with this calibration (details below).

The history gate is `4001e170 == 0 OR calibration[0x824] == 0`. Here `0x824` is
zero, so it does not block entry. The previous-outer-mode requirement remains:
a transition from torque into brake with a qualifying stop condition ordinarily
first selects 0xA, then can select 0xB on the next cycle. Higher-priority hold or
suppression conditions can supersede that sequence.

## Leaving 0xB

Two decisions must be distinguished: leaving submode 3, and leaving outer brake
control. The latter happens earlier in the function and reads the old submode.

In the ordinary request-state-1 and request-state-2 release branches, after the
corrected acceleration reaches the applicable release threshold:

```text
if OEM_CruiseState != Standstill AND special_speed_timer != 0:
    if NOT hold_flag AND previous_submode != 3:
        outer_mode = torque
        brake_request = 0
    # Otherwise this branch retains the previous outer mode and brake request.
```

The threshold itself includes mode history, calibration, capability and
correction terms; it is not simply zero acceleration.

| Change while in 0xB | Result in the relevant normal path |
|---|---|
| Small positive request, with stop qualifier still true | Does not by itself unlock the ordinary torque-release branch |
| Stop qualifier clears; outer brake mode is retained | Submode changes to 2 / 0xA |
| Following cycle, release threshold is met, hold is clear, and no other blocking condition applies | Torque release is now permitted because previous submode is no longer 3 |
| Speed reaches/exceeds 1.5 m/s, with the special timer nonzero | Speed-qualified stop branches clear; typically returns to 0xA if outer brake remains selected |
| Hold flag becomes set below 1.5 m/s | Higher-priority submode 4 or 5 / 0xC or 0xD |
| Suppression condition or cruise-main-off condition applies | Submode 1, with active bit evaluated separately |

Thus **0xB → 0xA → torque** is a code-supported ordinary release sequence, with
one additional 40 ms control step between clearing the submode and being eligible
for torque release. It is not a universal mandatory sequence: request state 4 and
some upstream override branches force torque without this particular interlock.
The hold flag is updated by `0013a180` after `0013afc0`, so the selector uses the
hold state from the previous update.

No measured brake-pressure threshold appears in this submode selection or this
release interlock. They are state/request conditions; that does not rule out
pressure-dependent behavior elsewhere, particularly inside the EBCM.

## Two timers with different purposes

**Special speed timer (`4001d91c`):** `001344b0` calls `0012df00` using speed from
`00132a60`, scaled as 100 counts per km/h. Calibration `0x680` is 5000 ms, but the
signed threshold at `0x682` is **-50 = -0.5 km/h**. The recovered bit arithmetic
implements `signed_speed < -50` for its countdown/reset-to-zero condition. At
normal forward or stationary speeds it instead reloads to `5000 / 40 = 125`
cycles. This is **not a five-second timer that automatically selects 0xB while
creeping forward**. The zero-timer branch is retained in the entry logic above
for completeness.

**Brake-active retention timer (`4001dc30`):** selecting submode 5 reloads it from
`calibration[0x832] / 40 = 2500 / 40 = 62` integer cycles. The output stage decrements
it, then asserts brake-active whenever outer mode is brake or the remaining timer
is nonzero. This provides roughly 2.5 seconds of active-bit retention after the
last reload; exact duration depends on cycle ordering. It does not keep submode 3
selected, and must not be interpreted as a fixed 0xB dwell time.

## Verified inputs and remaining unknowns

- `4001d928`: cruise-main permission. `001327a0` reads getter `000c5cb0`; setter
  `000c5ca0` is fed by `0004a2e0`. Assembly reads bytes 2–3 of CAN 0x0C9 and extracts
  byte 3 bit 5, matching `CruiseMainOn` in the local GM DBC.
- `4001d9a0` bit 25: comparison `4001d949 == 4` in `00131440`. `00133320` obtains
  this state through getter `000c5be0`; setter `000c5bd0` is called by `00049780`.
  `00049570` copies CAN 0x1C4 byte 1 through `00081040` into buffer `400048f0`;
  `00076e20` extracts its top three bits. This matches DBC `CruiseState : 15|3@0`,
  where value 4 is Standstill. Assembly checked because the decompiler's inferred
  RAM types obscure the byte copy.
- `4001dcc0` bits 27/28: actual selector reads verified in assembly, but their
  producers and physical meanings remain unresolved. A scan of 160 recovered
  ACC-region functions and direct references did not identify writes. This is
  not evidence that those conditions are unreachable.
- The separate suppression condition is `4001da04.bit26 AND 4001d93f == 1`.
  `4001d93f` traces through `000c5e50`/`000c5e40` and `0009ce80` to an IPC-derived
  status. Its physical meaning is unresolved.
- The hold flag is `4001df9c` (controller-state offset `0xE8`), updated in
  `0013a180`. `4001d8e2` selects hold variant 4 versus 5; their complete physical
  distinction has not been established.

## Implications for the current test and control design

The active test's 0xA override is appropriate for determining the relationship
between numeric brake request and moving creep. Earlier zero-demand measurements
in 0xB cannot be assumed to describe that relationship in 0xA.

If 0xA removes the zero-request stop behavior, that would strengthen the case for
reserving 0xB for deliberate stopping while retaining 0xA for moving creep. It
would still not prove the EBCM's internal algorithm. If pressure rises similarly
in 0xA, investigate the active-bit/zero-request semantics and preceding actuator
state before attributing the behavior solely to 0xB.

The useful OEM strategy is explicit state coordination: brake allocation,
stopping/holding, and permission to return to torque are separate decisions.
Preserving an integral bias for grade is compatible with that strategy. Copying
every stock entry predicate is premature while two flags and hold variants remain
unmapped. No change to the running test is required by this review.

## Sources and reproducibility

Local source: `/home/acremins/volt_reverse_engineering/ASCM/`.
MPU1 OS `decoded/84876565.bin` and ACC calibration `decoded/23366550.bin` match the
SHA-256 identifiers in the linked control review. Calibration values are
big-endian integers at file offset `0xA0 + offset`, not an array of floats.

| Calibration offset | Decoded value | Use |
|---|---|---|
| 0x626 | byte 0 | Brake-output suppression calibration is inactive |
| 0x680 | unsigned 5000 | Special speed timer duration, ms |
| 0x682 | signed -50 | Special timer speed threshold, 0.01 km/h |
| 0x820 | signed 150 | Stop/hold speed threshold, 0.01 m/s |
| 0x822 | signed 150 | Alternate stop speed threshold, 0.01 m/s |
| 0x824 | signed 0 | Disables the history exclusion for submode-3 entry |
| 0x832 | unsigned 2500 | Active retention after submode 5, ms |

Ghidra was run with `-readOnly -noanalysis`. Decompilations are in
`/tmp/ascm_mode_b/`, input mapping and assembly in `/tmp/ascm_mode_b_inputs/`, and
reference scans in `/tmp/ascm_mode_b_refs/`. Regenerate targeted exports with
`ghidra_scripts/DecompileLong.java` and the addresses cited above. Original output
packing exports are under `decoded/ghidra_longitudinal/mpu1/` and `mpu2/`.
These are static firmware findings, not an observed OEM drive trace.
