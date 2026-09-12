# Longitudinal Maneuvers Testing Tool

Test your vehicle's longitudinal control tuning with this tool. The tool will test the vehicle's ability to follow a few longitudinal maneuvers and includes a tool to generate a report from the route.

<details><summary>Sample snapshot of a report.</summary><img width="600px" src="https://github.com/user-attachments/assets/d18d0c7d-2bde-44c1-8e86-1741ed442ad8"></details>

## Volt tuning suite

This branch runs a 19-run suite, low speed first. The stop and creep block is where the comma 4 /
end-to-end model problems live (stopping ramp from zero, torque mode unable to hold creep, model
stop-flag pulses), so it runs first and every trial repeats. The higher-speed block sits at the end,
at 35 mph as single runs, with one 40 mph run last; disengage to skip it if there is no room.

| Runs | Setup speed | Command | What it measures |
|---|---|---|---|
| 2 | 10 mph | stop at -0.75 to standstill, hold 3 s | baseline stopping transition and brake hold (stop-test procedure below) |
| 2 | 5 mph | stop at -0.5 to standstill, hold 3 s | gentle approach with a long creep-speed tail: does the tune crawl or surge below 1 m/s |
| 2 | 15 mph | stop at -1.5 to standstill, hold 3 s | model-like harder approach; friction bite and integrator state at the hand-over to standstill |
| 2 | 10 mph | stop at -0.75, then at standstill three 0.3 s creep pulses (stop flag off, +0.05 m/s² target) 1.5 s apart, then hold 3 s | reproduces the model's stop-flag flap: the hold must survive a pulse without releasing the brake or rolling |
| 2 | 5 mph | -0.5 for 3.5 s (to ~0.5 m/s), 0 for 4 s, -0.3 for 4 s, 0 for 2 s | creep crawl: holding a crawl at zero target, then a slightly negative target at crawl speed (the route-41 case) |
| 2 | 10 mph | -0.5 held 3 s, then 0 for 3 s | low-speed brake step and the brake-to-torque re-entry near 3 m/s |
| 1 each | 35 mph | -0.75, -1.25, -2.0 m/s² held 5 s, then 0 for 2 s | regen-only tracking, the regen-to-friction hand-off, friction delivery; steady state after the transient; brake release |
| 1 | 35 mph | ramp 0.5 m/s³ down to -1.5, hold 2 s, then 0 | a planner-shaped request; separates actuator delay from gain |
| 1 | 35 mph | sweep 0 to -2.5 m/s² over 10 s, then 0 | one continuous map of command vs delivered torque: dead band, friction gain, regen saturation (ends near 7 mph) |
| 1 | 35 mph | -1.5 held 3 s, then -0.5 held 3 s, then 0 | the same plus a partial release (integrator unwind) |
| 1 | 40 mph | -1.0 held 4 s, then 0 | regen at the breakpoint where the pack power cap binds at high charge; the only 40 mph run, last |

The creep crawl ends below the 0.3 m/s stop rule, so the car stops at the end of its -0.3 phase; if the
ECM is then in cruise standstill, tap the accelerator to resume so the tool can set up the repeat.

Zero target acceleration is speed holding, not a guarantee of zero gas or brake actuation.
Between runs the tool returns to the setup speed and waits for its three-second ready
condition. The 40 mph runs need more road; the sweep covers roughly 180 m of braking and ends
near 12 mph so the tool can recover to the next setup speed on its own.

Each stop continues until standstill is reported and speed is below 0.1 m/s, then maintains
stopping intent for three continuous seconds. If the car moves during the hold, the hold timer
restarts. In the creep-pulse trial the hold timer only runs after the last pulse, and the timeout
for that trial is 30 s instead of 20 s.

Before the first stop test, disengage and take control. When ready on a clear,
straight section, manually move above the car's minimum engagement speed (3 mph
on this branch) and engage; the tool sets up at the trial's speed and waits three seconds.
After each stop, wait for **"Stop complete: take control before next run"**, then
take control and disengage. The tool keeps stopping intent until disengagement;
it does **not** automatically accelerate out of a completed stop. Manually set up
and re-engage for the next trial. Disengage after the final hold too, to acknowledge
completion and reach "Maneuvers Finished."

A stop/hold that has not completed within **20 seconds of braking onset** shows
**"Stop timed out: take control; retry required"**. It keeps stopping intent and
suppresses automatic resume until you take control; the failed trial must be retried.
During any active trial, disengagement discards that attempt and restarts the same
trial from speed setup on re-engagement. It does not count as a completed run.
Disengagement during a completed stop hold acknowledges success instead.

Alerts identify the run number and phase. Phase changes and completed trials are
also written to the log. Keep full rlogs, including CAN, for torque and controller
analysis; the generated report alone does not include all of that feedback.

Record the software commit and the pack voltage at rest (or state of charge) for
each route, and keep the same road direction when comparing tunes.

## Regen-only characterisation (historical)

`REGEN_ONLY_MANEUVERS` in maneuversd.py is a two-run test (a -2 m/s² request from 40 mph held 25 s)
that is only meaningful with friction brakes disabled in the GM car controller. It was run once on
2026-09-06 (commit e8d3546715) to measure what openpilot's regen request alone delivers; the result is
the `MAX_REGEN_TORQUE` curve in opendbc/car/gm/values.py. It is not part of the standard suite.

## Instructions

1. Check out this branch on your comma device so the targeted sequence is used.
2. Locate either a large empty parking lot or road devoid of any car or foot traffic. Flat, straight road is preferred. The full maneuver suite can take 1 mile or more if left running, however it is recommended to disengage openpilot between maneuvers and turn around if there is not enough space.
3. Turn off the vehicle and set this parameter which will signal to openpilot to start the longitudinal maneuver daemon:

   ```sh
   echo -n 1 > /data/params/d/LongitudinalManeuverMode
   ```

4. Turn your vehicle back on. You will see the "Longitudinal Maneuver Mode" alert:

   ![videoframe_6652](https://github.com/user-attachments/assets/e9d4c95a-cd76-4ab7-933e-19937792fa0f)

5. Ensure the road ahead is clear, as openpilot will not brake for any obstructions in this mode. Once you are ready, press "Set" on your steering wheel to start the tests. Allow time for 16 successful runs. The first 14 automatically recover to their setup speed between runs; the two stops require driver takeover between runs as described above. Press "Cancel" to disengage before turning around. Re-engage only when ready on the next clear, straight section; an interrupted trial starts over.

   **Note:** The step, ramp and sweep runs start at 20 or 40 mph; the final two start at 10 mph and stop completely. Review the setup, takeover and timeout behavior above before enabling maneuver mode.

   ![cog-clip-00 01 11 250-00 01 22 250](https://github.com/user-attachments/assets/c312c1cc-76e8-46e1-a05e-bb9dfb58994f)

6. When the testing is complete, you'll see an alert that says "Maneuvers Finished." Complete the route by pulling over and turning off the vehicle.

   ![fin2](https://github.com/user-attachments/assets/c06960ae-7cfb-44af-beaa-4dc28848e49d)

7. Visit https://connect.comma.ai and locate the route(s). They will stand out with lots of orange intervals in their timeline. Ensure "All logs" show as "uploaded."

   ![image](https://github.com/user-attachments/assets/cfe4c6d9-752f-4b24-b421-4b90a01933dc)

8. Gather the route ID and then run the report generator. The file will be exported to the same directory:

    ```sh
    $ python openpilot/tools/longitudinal_maneuvers/generate_report.py 57048cfce01d9625/0000010e--5b26bc3be7 'Volt braking baseline'

    processing report for CHEVROLET_VOLT
    plotting maneuver: brake step and release: -0.5m/s^2 from 20mph, runs: 3
    plotting maneuver: brake step and release: -0.75m/s^2 from 20mph, runs: 3
    ...

    Report written to /home/batman/openpilot/tools/longitudinal_maneuvers/longitudinal_reports/CHEVROLET_VOLT_57048cfce01d9625_0000010e--5b26bc3be7.html
    ```

You can reach out on [Discord](https://discord.comma.ai) if you have any questions about these instructions or the tool itself.
