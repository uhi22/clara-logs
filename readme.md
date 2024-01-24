# Log files of ccs32clara

References:
- https://github.com/uhi22/ccs32clara

How the logs are created? The foccci/clara provides a debug log on the serial line with 921600 baud. Using a 3.3V-serial-to-USB converter and Putty on the notebook.
Putty is configured to write a log file.

## 2024-01-19_clara_alpitronic_HYC300_7minutes_lightbulb_ok

- Charger: Alpitronic hypercharger HYC300
- Test setup: Foccci/Clara with Lightbulb (230V, 60V)
- Recorded by: uhi
- Result: 7 minutes "charging" worked fine. Stopped on charger.
- Later found: Clara requests EVTargetCurrent=0A during the charging loop. The alpitronic seems not to care too much and provides the requested voltage nevertheless :-)

## 2024-01-19_clara_numbat_lightbulb_verydark

- Charger: Numbat
- Test setup: Foccci/Clara with Lightbulb (230V, 60V)
- Recorded by: uhi
- Results:
    - Reaching the charging loop, but the bulb is very weak. Found later: Clara requests EVTargetCurrent=0A during the charging loop. This most likely drove the charger into current-limiting mode.
    - Even after terminating on the chargers screen, and PowerDeliveryStop, the charger did not stop to provide voltage. This leads to endless welding detection loop.
    - Wrong EVSEPresentVoltage in the trace due to data type mix in Clara.

## 2024-01-24_clara_ABBHPC_no_load_voltage_ramps_down

- Charger: ABB HPC
- Test setup: Foccci/Clara with Lightbulb (230V, 60V). Bulb not connected in the beginning.
- Recorded by: uhi
- Results:
    - Reaching the charging loop, but after good voltage during preCharge, the voltage ramps down at the beginning of the charging loop. Found later: Clara requests EVTargetCurrent=0A during the charging loop. This most likely drove the charger into current-limiting mode.
