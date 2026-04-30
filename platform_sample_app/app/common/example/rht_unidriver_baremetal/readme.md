# RHT UniDriver Bare-metal Example

## Summary

This project exercises **RHT UniDriver** (`sl_rht_unidriver_*`) on the on-board humidity and temperature sensor. The same firmware discovers **Si70xx** (e.g. **Wireless Pro Kit BRD4002A**) or **SHT4x** on **Wireless Pro Kit BRD4002B** and prints results on the **VCOM** serial console.

On startup the application:

- Calls `sl_rht_unidriver_init(sl_i2cspm_sensor)`; discovery probes Si70xx then SHT4x at fixed on-board addresses.
- Prints `sl_rht_unidriver_get_device_id`.
- Runs optional API checks: `get_firmware_revision`, `enable_low_power_mode`, `measure_analog_voltage`, and on Si70xx `start_no_hold_measure_rh_and_temp` + `read_rh_and_temp`.
- Starts a periodic timer that prints `sl_rht_unidriver_measure_rh_and_temp` (RH in percent×1000, temperature in milli-degrees C).

## Setup

1. Import the `.slcp` from this repository in Simplicity Studio (or use the example from the SDK package list).
2. Select a board that exposes the RHT sensor on the default I2C sensor instance (Si7021 on many kits; SHT4x on **BRD4002B**).
3. Build, flash, and open the VCOM serial port (115200 8N1 typical for SDK retarget).

## Hardware

- **Si70xx RHT:** common on **BRD4002A** and many Pro Kits with Si7021.
- **SHT4x:** **BRD4002B** (Wireless Pro Kit mainboard).

Enable **VCOM** and **sensor RHT** in board configuration if your kit uses `SL_BOARD_ENABLE_VCOM` / `SL_BOARD_ENABLE_SENSOR_RHT`.
