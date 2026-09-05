# Longitudinal Maneuvers Testing Tool

Test your vehicle's longitudinal control tuning with this tool. The tool will test the vehicle's ability to follow a few longitudinal maneuvers and includes a tool to generate a report from the route.

<details><summary>Sample snapshot of a report.</summary><img width="600px" src="https://github.com/user-attachments/assets/d18d0c7d-2bde-44c1-8e86-1741ed442ad8"></details>

## Volt braking comparison sequence

This branch runs five braking targets from 20 mph (8.94 m/s), in order:
**-0.5, -0.75, -1.0, -1.25 and -1.5 m/s²**. Each target is repeated three times.
Each run holds the braking target for three seconds, then requests zero acceleration
for two seconds to capture brake release. Zero target acceleration is speed holding,
not a guarantee of zero gas or brake actuation. Between runs, the tool returns to
20 mph and waits for its existing three-second ready condition.

The same 15 runs (approximately 75 seconds of active commands, plus setup) are
followed by **six full stops from 10 mph**: **-0.5, -0.75 and -1.0 m/s²**, twice each.
Each stop continues until both standstill is reported and speed is below 0.1 m/s,
then maintains stopping intent for **three continuous seconds** at standstill.
If the car moves during the hold, the hold timer restarts. These tests exercise
low-speed PID braking, the transition into stopping control, and brake hold.
The longitudinal gains, actuator mapping and production stopping logic are unchanged.

Before the first stop test, disengage and take control. When ready on a clear,
straight section, manually move above the car's minimum engagement speed (3 mph
on this branch) and engage; the tool sets up at 10 mph and waits three seconds.
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
also written to the log. Keep full rlogs to distinguish completed trials from
interrupted attempts; the generic HTML report can include interrupted intervals.

Record these added stops with the current gains before changing them, then repeat
the same sequence and road
direction for the candidate tune. Note the software commit and approximate charge
for each route. Keep the full rlogs, including CAN, for torque/pressure and controller
analysis; the generated report alone does not include all of that feedback.

## Instructions

1. Check out this branch on your comma device so the targeted sequence is used.
2. Locate either a large empty parking lot or road devoid of any car or foot traffic. Flat, straight road is preferred. The full maneuver suite can take 1 mile or more if left running, however it is recommended to disengage openpilot between maneuvers and turn around if there is not enough space.
3. Turn off the vehicle and set this parameter which will signal to openpilot to start the longitudinal maneuver daemon:

   ```sh
   echo -n 1 > /data/params/d/LongitudinalManeuverMode
   ```

4. Turn your vehicle back on. You will see the "Longitudinal Maneuver Mode" alert:

   ![videoframe_6652](https://github.com/user-attachments/assets/e9d4c95a-cd76-4ab7-933e-19937792fa0f)

5. Ensure the road ahead is clear, as openpilot will not brake for any obstructions in this mode. Once you are ready, press "Set" on your steering wheel to start the tests. Allow time for 21 successful runs. The first 15 automatically recover to 20 mph between runs; the six stops require driver takeover between runs as described above. Press "Cancel" to disengage before turning around. Re-engage only when ready on the next clear, straight section; an interrupted trial starts over.

   **Note:** The first 15 runs start at 20 mph; the final six start at 10 mph and stop completely. Review the setup, takeover and timeout behavior above before enabling maneuver mode.

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
