# Log files of ccs32clara

![image](clara_logs.jpg)

References:
- https://github.com/uhi22/ccs32clara

How the logs are created? The foccci/clara provides a debug log on the serial line with 921600 baud. Using a 3.3V-serial-to-USB converter and Putty on the notebook.
Putty is configured to write a log file.

How the "decoded" and "values" files are created? By running claralogConverter.py from https://github.com/uhi22/pyPLC. This reads the log file, decodes the EXI data and writes the two new files.


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

## 2024-01-27_clara_SuCV3_preCharge_uMin229V

- Charger: Tesla Supercharger V3
- Test setup: Foccci/Clara with Lightbulb demo configuration. No bulb connected.
- Recorded by: uhi
- Results:
    - PreCharge loop is reached
    - Foccci does not end the precharge, because the Supercharger announced minimum voltage 229.99V, and we wanted 210V.
    - Found afterwards: TCP connect needs multiple tries. Issue https://github.com/uhi22/ccs32clara/issues/10

## 2024-01-30_clara_pyPLC_withEthLogBeforeChargeLoop

- Testsetup: Foccci/Clara with pyPLC on the bench
- Goal: verify that the logging of ethernet traffic before the charge loop works.
- Recorded by: uhi
- Result: works. Ethernet traffic is logged before the charging loop, and not logged during the charging loop.

## 2024-02-09_clara_tesla_timeout_in_cablecheck_due_to_wrong_PP

- Testsetup: Foccci/Clara in johus Touran on Tesla Supercharger. PP pull-up to 12V with 3k3. Discussed here: https://openinverter.org/forum/viewtopic.php?p=67036#p67036
- Recorded by: johu
- Result: During cable check, the Supercharger permanently reports "EVSEProcessing": "Ongoing". After 55s in CableCheck, clara gives up and enters the safeshutdownsequence.
- Likely root cause: The supercharger seems to check the PP circuit and does not finish the chablecheck if the PP circuit does not match the expectations.