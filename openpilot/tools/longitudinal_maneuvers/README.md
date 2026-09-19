# Longitudinal Maneuvers Testing Tool

Test your vehicle's longitudinal control tuning with this tool. The tool will test the vehicle's ability to follow a few longitudinal maneuvers and includes a tool to generate a report from the route.

<details><summary>Sample snapshot of a report.</summary><img width="600px" src="https://github.com/user-attachments/assets/d18d0c7d-2bde-44c1-8e86-1741ed442ad8"></details>

## Current Volt default: signed EBCM acceleration requests

`SIGNED_BRAKE_MANEUVERS` runs three profiles twice each (six attempts), all in
**0xA**. The sign below is the actual CAN sign: negative requests deceleration,
positive requests acceleration. These are protocol counts, not measured pressure
or a demonstrated physical acceleration increment. The experiment measures the
EBCM's response; it does not assume positive demand must release all pressure.

Each attempt settles at 3 mph for two seconds, sends -5 counts for two seconds,
then follows one row. Intermediate phases are timed, with no stability gate.
Gas/regen stays at -650 Nm throughout measurement. Production acceleration PI,
brake scaling and brake/torque selection are bypassed during direct commands.

| ID | Signed request sequence | Measurement duration, including -5 baseline |
|---|---|---:|
| S01 | -15 (4 s) → 0 (3 s) → +15 (4 s) → 0 (4 s) | 17 s |
| S02 | -18 (4 s) → 0 (3 s) → +18 (4 s) → 0 (4 s) | 17 s |
| S03 | -20 (4 s) → 0 (3 s) → +20 (4 s) → 0 (4 s) | 17 s |

Total measured time is 102 seconds, plus setup, stopping, acknowledgement and
recovery. Existing direct-test guards remain: 0.4–2.0 m/s, no standstill, valid
CAN and commands no older than 250 ms. Endpoint stopping and the throttle-tap
acknowledgement are unchanged. Accelerator interruption restarts the unfinished
attempt. Only the selected suite runs; previous suites are preserved below.

Enable `LongitudinalManeuverMode` as before and start a new drive. The signed
experiment additionally needs the matching rebuilt Panda firmware. This prebuilt
branch includes it in `panda/board/obj/panda_h7.bin.signed`; pulling source alone
does not compile firmware. After deploying the binary and restarting, pandad
automatically flashes it when the firmware signature differs. The DBC and CAN
checksum already support signed values. Panda accepts positive signed demand in
**0xA**, with longitudinal actuation allowed, and at most **+200 counts (+2.0 m/s²)**, through
the common GM brake-command check. There is no test-specific, EV, or ASCM gate.
The existing **−400-count** negative-demand brake limit and transmit allowlists are unchanged:
configurations without brake-message transmit permission still cannot send it.
Panda independently checks message/bus permission, mode, sign, bounds and
actuation permission.
Direct-command generation still requires Volt maneuver mode in the host; its
speed/freshness guards remain active. The characterization range is **−20 to +20 signed counts**. Normal driving
control is unchanged and does not yet generate positive EBCM requests.

The separate chassis interceptor must also have the signed-request update
(−400 to +200 counts). Its old unsigned check latches a fault on positive
requests and replaces subsequent brake commands with mode 0x0, zero demand.
Confirm the request reaches the chassis bus and interceptor status stays healthy
before interpreting pressure release as a response to positive demand.

Look for pressure before the positive step, partial versus complete pressure
reduction, resulting acceleration, and whether the final zero request arrests
acceleration while retaining 0xA. Compare actual axle torque and AxleTorqueMin;
fixed commanded torque does not ensure fixed delivered torque. A run with no
initial pressure or a speed-bound endpoint does not establish successful tracking.

Use `plot_brake_characterization.py` below. Plots and UI show the signed CAN
convention. For compatibility, `brakeTestCommand`, `actuatorsOutput.brake`, and
CSV `requested_counts`/`sent_counts` retain the legacy positive-for-braking
convention: **negate those fields to obtain signed acceleration counts**.

## Preserved moving-creep speed tracking

The preserved `CREEP_SPEED_MANEUVERS` suite is **six speed profiles, two runs each: 12 attempts**.
These exercise normal longitudinal control, including its acceleration PI and
brake/torque transitions. They use no direct brake-count or mode override.

For the Volt gateway with `STOCK_CREEP_TRANSITIONS` enabled, moving braking now
uses **0xA**. **0xB** requires the controller's explicit stopping state as well as
low speed. Brake exit uses **zero demand in 0x1**, the existing separate entry
and release thresholds, and the existing AxleTorqueMin torque initialization.
The transition thresholds, production PI gains and brake-demand scaling are
unchanged. Other platforms and the disabled-feature baseline retain their mode
selection.

Every attempt first settles at **3 mph for two seconds**, then follows a timed
speed reference. Ramps use **0.10 m/s²** in either direction. The test's acceleration
request is ramp feedforward plus **0.5 × speed error**, limited to **±0.30 m/s²**.
This outer speed correction defines the test trajectory; it does not change
production acceleration PI gains. Intermediate targets have fixed holds, with
**no stability requirement** to advance to the next phase.

| ID | Speed sequence (mph) | Holds |
|---|---|---|
| C01 | 3 → 1.5 → 3 | 6 s at creep, 3 s at final 3 mph |
| C02 | 3 → 1 → 3 | 6 s at creep, 3 s at final 3 mph |
| C03 | 3 → 0.5 → 3 | 6 s at creep, 3 s at final 3 mph |
| C04 | 3 → 1.5 → 2 → 1.5 → 2 → 1.5 → 3 | 5 s at each creep hold, 4 s at each 2 mph hold, 3 s at final 3 mph |
| C05 | 3 → 1 → 2 → 1 → 2 → 1 → 3 | Same cycle holds |
| C06 | 3 → 0.5 → 2 → 0.5 → 2 → 0.5 → 3 | Same cycle holds |

Each profile runs twice consecutively. The complete suite has about **8.9 minutes
of measured profiles**, plus setup and recovery. Completion means the timed
profile finished, not that speed tracking passed a tolerance. Compare repeats
using speed error during holds, overshoot, acceleration, pressure, mode switch
count and axle torque. Keep full CAN rlogs.

The automatic low-speed `should_stop(v_ego, accel)` heuristic is bypassed only
during a moving-creep test. Explicit failure stops still take priority. Normal
planning, stop maneuvers, setup and recovery retain the helper. A measured speed
below **0.1 m/s (0.22 mph)**, above **1.8 m/s (4.03 mph)**, or either vehicle or
cruise standstill indication aborts the new speed profile. This first suite tests
down to **0.5 mph**, not 0.2 mph or launch from rest. The preserved older moving
trials keep their original 0.4–1.5 m/s guards.

The active alert shows **target and actual mph**. Requested speed is logged in
`longitudinalPlan.speeds[0]`; the normal maneuver report overlays it on measured
speed. Completed profiles recover automatically to 3 mph and advance after
three seconds settled there. A failed profile shows **"Creep test invalid"** and
requests stopping until a throttle tap or disengagement acknowledges it, then
recovers and advances. Accelerator override or disengagement during an unfinished
profile restarts that attempt from setup. Disengage before turning around.

Use the existing `LongitudinalManeuverMode` parameter and instructions below.
To select these speed profiles, set `MANEUVERS = CREEP_SPEED_MANEUVERS`.
To repeat the previous brake-exit experiment, set
`MANEUVERS = BRAKE_CHARACTERIZATION_MANEUVERS` in `maneuversd.py`.

## Preserved brake characterization suite

The preserved `BRAKE_CHARACTERIZATION_MANEUVERS` suite contains **six brake-exit
profiles, two runs each: 12 attempts total**. They compare zero demand in active
mode **0xA** with zero demand in inactive mode **0x1**, including a delayed
transition. The earlier release, hold and sweep suites are preserved separately.

Each attempt:

1. Settle at **3 mph for two seconds** using normal control.
2. Enter ordinary active brake mode **0xA** with **5 counts for two seconds**.
3. Ramp from 5 to the profile's peak at **0.5 count/second**, then hold the exact
   peak for the time listed below. Counts are rounded onto CAN, so the transmitted
   peak begins approximately one second before the exact requested peak.
4. Drop to **zero counts** and follow the mode sequence below.
5. End at profile completion or if speed leaves **0.4–2.0 m/s (0.9–4.5 mph)**,
   including a standstill indication. All guards remain active during release
   and zero-count holds. A guarded endpoint is useful data, not a completed hold.
6. The screen says **"Brake test ended"** with the endpoint reason. Stopping
   intent remains asserted until a throttle tap or disengagement. Recover to
   **3 mph** after acknowledgement, then advance to the next repeat or profile.

Every row below runs **twice consecutively**. Durations are per run and exclude
setup, stopping, acknowledgement and recovery.

| ID | Peak and exact-peak hold | Zero-demand sequence | Full duration |
|---|---|---|---:|
| E01 | 12 for 4 s | 0xA for 8 s | 28 s |
| E02 | 12 for 4 s | 0x1 for 8 s | 28 s |
| E03 | 12 for 4 s | 0xA for 2 s, then 0x1 for 8 s | 30 s |
| E04 | 13 for 3 s | 0xA for 8 s | 29 s |
| E05 | 13 for 3 s | 0x1 for 8 s | 29 s |
| E06 | 13 for 3 s | 0xA for 2 s, then 0x1 for 8 s | 31 s |

The suite has **5 minutes 50 seconds of measured profiles** if every attempt
completes, plus setup, acknowledgement and recovery. E01 and E04 repeat the
previous suite's active-zero commands for comparison. E02 and E05 test immediate
brake deactivation; E03 and E06 separate the numeric-demand drop from deactivation
within the same run.

During measurement, longitudinal control remains active and gas/regen stays at
**−650 Nm**, including the inactive-brake hold. A test-only release flag ends the
brake-active request through the existing CAN helper. It is valid **only at zero
demand**; it cannot force an arbitrary mode or request 0x1 with nonzero counts.
The experiment stays active throughout this hold. Setup, recovery, and endpoint
or invalid-command stopping retain their existing behavior. PI and the
experimental brake-demand scaling do not alter these direct commands.

Application is timed, not triggered by a pressure threshold. Check the logs to
verify that each run actually developed pressure before release. A run with no
pressure to begin with is not evidence of successful release. The 13-count
profiles provide additional application cases; they do not isolate peak magnitude
from hold duration because their exact-peak hold is shorter to preserve speed.

For each release, compare pressure before the drop, delay and extent of pressure
reduction after the mode transition, speed, acceleration, delivered axle torque
and AxleTorqueMin. Pressure is in raw units, and changing speed/torque can affect
it. The question is whether ending the active request clears pressure more
reliably than active zero, and whether two seconds of active zero changes that
response. This informs the brake-exit transition before changing normal control.

This is **EBCM demand characterization, not direct hydraulic-pressure control**:
the EBCM still blends braking internally, and constant commanded gas/regen does
not guarantee constant delivered axle torque. Keep full CAN rlogs. One command
count is a protocol unit, not a measured pressure or demonstrated physical
acceleration increment.

Direct commands require per-drive `LongitudinalManeuverMode`, Volt gateway
hardware, engaged longitudinal control, valid CAN, and a fresh plan no older than
250 ms. Stale/invalid commands latch stopping until the test request ends; the
screen reports **"controller stopped test"** and waits for acknowledgement. Pedal overrides or inactive
longitudinal control cancel the direct output. Normal driving defaults this path
off. The old acceleration suite is used on unsupported configurations.

### Plot the release response

After fetching the route's full rlogs, run:

```sh
python openpilot/tools/longitudinal_maneuvers/plot_brake_characterization.py \
  '/path/to/drive_NAME--*/rlog.zst' --output /path/to/brake_report
```

The report writes PNG/PDF time traces for requested/sent brake counts, filtered
and raw speed, acceleration, and raw pressure. `command_response.png` compares
speed, acceleration, and pressure against **actual CAN brake counts** across
repeats. Per-trial CSVs also include brake mode, gas/regen request, engagement,
pedal state, and the zero-demand release flag. Endpoint reasons are preserved in `trials.json`.

Use the traces to locate where pressure and deceleration begin changing, then
check whether that location repeats. Speed integrates acceleration, so a bend
in speed alone is not a steady-state brake calibration. No automatic inflection
finder or fitted pressure model is used.

The brake-exit profiles are built by `brake_exit_maneuvers()` in `maneuversd.py`.
Their descriptions include E01–E06, the mode, peak hold, and release sequence.
The active alert shows the current requested count and mode. Compare each repeat
separately and exclude fallback stopping commands after a guard triggers.

To select a suite, set `MANEUVERS` to:

- `SIGNED_BRAKE_MANEUVERS`: the current signed-request experiment, three profiles, two runs each.
- `CREEP_SPEED_MANEUVERS`: the preserved six speed-tracking profiles, two runs each.
- `BRAKE_CHARACTERIZATION_MANEUVERS`: the six zero-demand brake-exit profiles, two runs each.

- `BRAKE_RELEASE_MANEUVERS`: the previous 12 active-mode release profiles, two runs each.
- `BRAKE_HOLD_MANEUVERS`: nine earlier 11/12/13-count hold-and-release attempts.
- `BRAKE_SWEEP_MANEUVERS`: three earlier 5–20-count sweeps at 0.25 count/second.
- `STANDARD_MANEUVERS`: the preserved acceleration suite described below.

Only the selected suite runs.

## Preserved acceleration comparison suite

The following section describes `STANDARD_MANEUVERS`, not the current Volt
signed-request default. Set `MANEUVERS = STANDARD_MANEUVERS` to run it again.

The suite contains **22 runs: eleven creep scenarios, each repeated twice**. The
original eight scenarios remain first, with identical active commands, durations,
and order for comparison with the previous 16-run drive. Setup and recovery now
use 3 mph instead of the earlier 8 mph excursions; compare the measured entry
speed and acceleration when evaluating results across that change. Three moving transition
scenarios follow. The test portion starts at 3 mph or below. The old higher-speed braking and regen trials have
been removed.

Every run follows the same sequence:

1. Reach **3 mph** and settle there for **two continuous seconds** while showing
   the upcoming test.
2. Perform the creep test below. The three added moving tests first request
   **-0.15 m/s²** and start their timed commands on the first downward crossing of
   **1.0 m/s (2.2 mph)**; they do not require stable creep.
3. Return to **3 mph** and stay near that speed for three seconds before advancing.
   Stop-and-hold tests wait for driver acknowledgement first, as described below.

Setup and recovery target 3 mph, with a 0.1 m/s settling tolerance. They use up to
+0.75 m/s² acceleration and -0.5 m/s² deceleration. The stop timeout starts when the
actual test begins, excluding setup and recovery.

| Runs | Command after settling at 3 mph | What it measures |
|---|---|---|
| 2 | -0.15 m/s² to standstill, hold 3 s | very gentle approach and extended creep-speed tail |
| 2 | -0.3 m/s² to standstill, hold 3 s | normal creep stop and brake hold |
| 2 | -0.5 m/s² to standstill, hold 3 s | firmer low-speed stopping transition |
| 2 | stop at -0.3, then three 0.1 s pulses at +0.05 m/s², hold 3 s | brief stop-flag interruptions |
| 2 | stop at -0.3, then three 0.3 s pulses at +0.05 m/s², hold 3 s | repeated stop-flag flapping |
| 2 | stop at -0.3, then three 0.4 s pulses at +0.08 m/s², hold 3 s | longer, stronger creep requests during a hold |
| 2 | -0.4 for 2 s, 0 for 4 s, -0.15 for 4 s, 0 for 2 s | crawl near 0.5 m/s, gentle braking to a stop, and release |
| 2 | -0.3 for 2 s, -0.15 for 2 s, 0 for 3 s, +0.15 for 2 s, 0 for 3 s | feathering the brake and re-entering positive torque at creep speed |

All accelerations are in m/s². Pulse tests drop stopping intent during each pulse;
pulses start one second after first reaching standstill and are spaced 1.5 s apart.
The final three-second hold only counts after the last pulse. Zero target acceleration
is speed holding, not a guarantee of zero gas or brake actuation.

### Added moving transition trials (runs 17–22)

The earlier timed crawl could overshoot into the stopping controller before its
zero-acceleration interval. After the 3 mph setup, these additions
request a fixed -0.15 m/s² until measured speed first reaches 1.0 m/s or below.
The timed profile starts immediately after that crossing, without a speed-hold
or acceleration-settling requirement. The former two-second hold near 1.8 mph
blocked every added trial in route 68, so it is no longer a prerequisite.

Both approach and active commands are acceleration requests without added speed
correction. The initial speed and acceleration remain visible in the rlogs;
compare those initial conditions when evaluating different drives. Starting at
1.0 m/s leaves more room for braking overshoot before the low-speed guard.

| Runs | Commands after crossing 1.0 m/s | What it measures |
|---|---|---|
| 17–18 | -0.15 for 0.5 s, then 0 for 6 s | speed drift, residual braking, and brake-mode chatter near zero requested acceleration |
| 19–20 | -0.15 for 0.5 s; 0, +0.05, -0.05, +0.15, -0.05 for 1 s each; +0.3 and -0.15 for 0.75 s each; 0 for 1 s | small positive requests while braking, followed by torque handoff and brake re-entry |
| 21–22 | -0.15 for 0.5 s; linear ramp -0.15 → +0.3 → -0.15 over 4 s; 0 for 2 s | transition hysteresis and acceleration discontinuities under a gradual request |

All accelerations are in m/s². A small initial braking request exercises the
brake path; confirm actual mode from CAN, since PI-corrected actuator acceleration
can differ from the planner request. A zero-acceleration request tests whether
speed stays steady; it does not impose a target speed during the active trial.

During acquisition or the active trial, standstill, speed below **0.4 m/s**, or
speed above **1.5 m/s** invalidates the run. Acquisition also times out after
**20 seconds**. The screen shows **"Creep test invalid: tap throttle or disengage"** with the
reason. Until acknowledgement,
stopping intent stays asserted. Then recover to 3 mph with longitudinal control
active; that failed attempt advances to the next repetition or scenario so one
poorly tracked trial cannot block the rest. Its outcome is logged as **failed**,
not completed. Interruptions before any failure still retry the same attempt.
The report marks an aborted active trial invalid; acquisition failures are
logged but have no active interval to plot. Normal stop/resume logic is retained.

These trials exercise moving control above the GM standstill threshold, not
0.2 mph crawling or launch from rest. Existing stop and feather trials remain
regression checks for those transitions. For analysis, compare acceleration
error, speed drift, brake-mode switch count, pressure release, and torque jump
at handoff alongside `AxleTorqueMin`. The added trials need their own baseline
run with the old controller and the same revised entry procedure for an exact
before/after comparison; the first 16 runs can be compared directly with the previous drive.

### Stops, recovery, and status

A stop must report standstill with speed below 0.1 m/s and then hold for three
continuous seconds. Movement resets the hold timer. Until the hold is complete,
the screen says **"Maneuver Active: holding stop"**.

After **"Stop complete: tap throttle"** appears, tap the throttle
to acknowledge the completed hold. The tool releases stopping intent and recovers to
3 mph once longitudinal control is active again. Alternatively, disengage, manually
move above the minimum engagement speed (3 mph on this branch), and re-engage to
recover. Completed stop holds do not automatically launch without acknowledgement.

The two original timed crawl tests and successful added moving trials enter recovery
automatically after their timed commands. Failed moving trials wait for acknowledgement first.
If stock cruise holds the car stopped, tap the throttle when **"Test complete: tap throttle"** appears.
While moving, the screen says **"Recovering to 3 mph"**. A run is only counted after
the 3 mph recovery has settled. This includes the final run; then the screen shows
**"Maneuvers Finished"**. Take control to end the drive.

During longitudinal maneuver testing, the low-speed steering warning is suppressed
so test progress and completion remain visible. Normal driving retains the warning.
Other alerts and the actual steering-assist speed limit are unchanged.

A stop/hold that has not completed within **20 seconds of braking onset** shows
**"Stop timed out: take control"**. Pulse trials allow 30 seconds.
A timed-out stop maintains stopping intent until takeover; disengage and re-engage
to retry the same run. Interrupting setup or an unfinished test also restarts that
run from the 3 mph setup. Interrupting recovery pauses it; re-engagement resumes
recovery without repeating the completed test.

Alerts identify the run number and phase. Phase changes, failed attempts, and completed trials are
also written to the log. Keep full rlogs, including CAN, for torque and controller
analysis; the generated report alone does not include all of that feedback.

Record the software commit and the pack voltage at rest (or state of charge) for
each route, and keep the same road direction when comparing tunes.

## Instructions

1. Check out this branch on your comma device so the targeted sequence is used.
2. Locate either a large empty parking lot or road devoid of any car or foot traffic. Flat, straight road is preferred. Leave enough room for the 3 mph setup and recovery on every run. Disengage and take control before turning around.
3. Turn off the vehicle and set this parameter which will signal to openpilot to start the longitudinal maneuver daemon:

   ```sh
   echo -n 1 > /data/params/d/LongitudinalManeuverMode
   ```

4. Turn your vehicle back on. You will see the "Longitudinal Maneuver Mode" alert:

   ![videoframe_6652](https://github.com/user-attachments/assets/e9d4c95a-cd76-4ab7-933e-19937792fa0f)

5. Ensure the road ahead is clear, as openpilot will not brake for any obstructions in this mode. Once you are ready, press "Set" on your steering wheel to start the tests. For the default Volt speed-tracking suite, allow 12 attempts (six profiles, two runs each); completed profiles advance automatically after recovery, while failed profiles require acknowledgement. For the preserved brake-exit suite, acknowledge each endpoint. For the preserved acceleration suite, allow 16 original runs and six added moving attempts (22 total). The first 12 are stop-and-hold trials requiring acknowledgement before recovery; the next four are the original timed crawl trials, followed by six moving transition attempts. A failed moving attempt requires acknowledgement and recovery before advancing. Press "Cancel" to disengage before turning around. Re-engage only when ready on the next clear, straight section; an interrupted trial starts over unless it has already failed and is awaiting acknowledgement.

   **Note:** Every run settles at 3 mph before the test and recovers to 3 mph afterward. Review the stop acknowledgement and timeout behavior above before enabling maneuver mode.

   ![cog-clip-00 01 11 250-00 01 22 250](https://github.com/user-attachments/assets/c312c1cc-76e8-46e1-a05e-bb9dfb58994f)

6. When the testing is complete, you'll see an alert that says "Maneuvers Finished." Complete the route by pulling over and turning off the vehicle.

   ![fin2](https://github.com/user-attachments/assets/c06960ae-7cfb-44af-beaa-4dc28848e49d)

7. Visit https://connect.comma.ai and locate the route(s). They will stand out with lots of orange intervals in their timeline. Ensure "All logs" show as "uploaded."

   ![image](https://github.com/user-attachments/assets/cfe4c6d9-752f-4b24-b421-4b90a01933dc)

8. For the preserved brake-characterization suites, use `plot_brake_characterization.py` above. For the current speed-tracking suite or preserved acceleration suite, gather the route ID and run the maneuver report generator. The file will be exported to the same directory:

    ```sh
    $ python openpilot/tools/longitudinal_maneuvers/generate_report.py 57048cfce01d9625/0000010e--5b26bc3be7 'Volt creep baseline'

    processing report for CHEVROLET_VOLT
    plotting maneuver: creep stop and hold: -0.15m/s^2 from 3mph, runs: 2
    plotting maneuver: creep stop and hold: -0.3m/s^2 from 3mph, runs: 2
    ...

    Report written to /home/batman/openpilot/tools/longitudinal_maneuvers/longitudinal_reports/CHEVROLET_VOLT_57048cfce01d9625_0000010e--5b26bc3be7.html
    ```

You can reach out on [Discord](https://discord.comma.ai) if you have any questions about these instructions or the tool itself.
