# ASCM remaining questions after the source/consumer follow-up

The arithmetic and ownership decisions are substantially recovered. The study
is still not a complete ASCM simulation. This review separates questions that
can change a faithful implementation from physical labels that cannot be proved
by plausible naming. See [the audit](ASCM_FIRMWARE_AUDIT.md) and
[the follow-up](ASCM_DYNAMICS_AND_OUTPUTS.md) for positive evidence.

## Reassessment and best next approach

| Question | Current evidence | Best way to close it |
|---|---|---|
| Are the dynamics classifier inputs independent sensors? | No. Both trace to c32d0; the second uses conditioned, initialized-bias-subtracted sensor data and wheel acceleration. | Resolved source mapping; preserve both separate filters when replaying. |
| Is the second input an angle/grade percentage? | It is an acceleration-domain discrepancy, with ±2.3793 bounds. | Sensor definition or synchronized wheel speed, sensor and attitude data to distinguish grade, pitch and bias. No amount of renaming the residual establishes that distinction. |
| Can initialized sensor bias be assumed zero? | Only as an explicit default assumption. Stored record 100 supplies the initial bias; adaptation has a save path. | Read an existing saved record/state trace, or sweep plausible initial biases in replay and label the assumption. |
| Does an invalid sensor force the dynamics class to zero? | Not inside 1344b0. Separate processing retains values and 1333f0/132c70 aggregate sensor faults upstream. | Reconstruct the upstream supervisor and its scheduling for exact disengagement timing. Keep the classifier's local rule distinct. |
| Do auxiliary/ratio numbers command a second actuator? | No such publication found in the traced MPU1 path. A conditional raw block transfer includes both. | For control modeling, preserve their local state/side effects. Trace the transfer hardware endpoint only if observability or an external consumer matters. |
| What enables that transfer? | Stored byte 8 must successfully read as 0x5a; firmware default is zero. | Actual module storage establishes whether it is active on that module. |
| What do hold input enums mean? | Driver-door source corroborated; two other fields mapped to extended filters 0x00608000 and 0x00336000, byte0 bits0/1. | Match a trustworthy CAN definition or correlate already recorded payloads with the corresponding physical controls. |
| What are object states 1/2? | Exact object producer, pass-through enum and sticky 2→1 behavior recovered. | Trace the internal perception enum's producer, including MPU2 if necessary; corroborate stationary/moving labels with object traces. |
| What do brake modes physically do? | ASCM selects the active bit/submode and acceleration request. | EBCM implementation or synchronized command/response measurements. ASCM code cannot establish hydraulic pressure behavior by itself. |
| Does the reference reproduce a whole drive? | No; 70,000 snapshots and 6,000 successive request/feedback/allocation cycles pass against recovered C; other stages are not joined into that replay. | A sequential harness preserving actual state, startup storage, task ordering and 10/40 ms schedules, then comparison with binary execution or an OEM state trace. |

## Sanity-check scope

The consequential ordering to preserve is:

1. Sensor processing reads previously published wheel/residual data; wheel
   processing then runs, followed by the residual estimator in the 10 ms task.
2. The 40 ms ACC path prepares dynamics and upstream flags before the inner loop.
3. Vehicle-model calibration reload precedes capability conversion. The later
   class +1 model adjustment affects output conversions, not the already computed
   capability. The attempted mass update is overwritten at the next reload.
4. Request selection sees the previous I contribution. Feedback sees the old
   owner/hold and its separate owner history; it can reset the allocation latch.
5. Allocation chooses the new owner and submode using the old hold. The hold
   update occurs afterward, affecting the next allocation.
6. Primary torque gets its transition seed and filter/slew treatment. The ratio
   value is calculated separately, before that treatment, and is not published
   in place of the primary torque.
7. The caller approaches the brake envelope from the current allocation result,
   writes it back, and publishes commands with separate enable/submode logic.

The branch comparison harness covers request selection, feedback, allocation,
submode/hold predicates and vehicle-model conversions. All **70,000** snapshot
comparisons pass. The added **6,000-cycle** check carries request, PI/history,
owner/latch and submode state between calls and covers all five request states,
all three owners and all five submodes. Its external hold, capability, torque
and sensor inputs are synthetic; the final caller envelope and full supervisor
are outside this three-stage replay. These cycles also pass. Its checks do not prove
upstream state reachability, a particular saved bias, sensor orientation,
machine overflow equivalence, or receiving-ECU behavior. Those are explicit
boundaries for the next validation work, not reasons to invent defaults.

The highest-value next implementation step is a sequential harness for the
recovered ACC stages and supervisor boundary, followed by a trace comparison.
For the two unnamed hold inputs and physical slope interpretation, targeted
signal evidence is more decisive than further inspection of already understood
arithmetic. No vehicle traffic or configuration writes are required to continue
static work or analyze existing traces.
