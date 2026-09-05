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

There are 15 runs and approximately 75 seconds of active maneuver commands, plus
setup and speed recovery. The sequence replaces the starting, creep and strong
braking/acceleration tests with measurements around the Volt's braking transition.
It does not change the longitudinal gains, actuator mapping or stopping logic.

Record a baseline before changing gains, then repeat the same sequence and road
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

5. Ensure the road ahead is clear, as openpilot will not brake for any obstructions in this mode. Once you are ready, press "Set" on your steering wheel to start the tests. Allow time for 15 runs, including automatic speed recovery to 20 mph between runs. If you need to pause the tests, press "Cancel" on your steering wheel. You can resume the tests by pressing "Resume" on your steering wheel.

   **Note:** This sequence starts each run at 20 mph. Review the targets above before enabling maneuver mode; it will automatically accelerate back to that speed between runs.

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
