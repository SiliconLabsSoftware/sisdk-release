# I2C Simple Polled Master Bare-metal

This example demonstrates the I2C Simple Polled Master driver with the Si7021 humidity and temperature sensor in a bare-metal configuration.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example uses the I2C Simple Polled Master (SPM) driver to read the Si7021 relative humidity and temperature sensor. The initial temperature is read and upper/lower limits are calculated from TEMPERATURE_BAND_C. When temperature reaches the upper limit, LED0 turns on (LED1 off); when it reaches the lower limit, LED1 turns on (LED0 off). Status is also printed on the VCOM serial port. Use it to learn I2C SPM and sensor integration.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with I2C support and an Si7021 sensor (or compatible). On-board LEDs if using LED feedback.

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM output.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit (and Si7021 if on an expansion board) via the required connections.
3. Flash and run. Observe temperature-based LED behavior and/or VCOM output.
4. Optionally adjust TEMPERATURE_BAND_C and rebuild.

## Troubleshooting

- **No sensor readings:** Check I2C wiring, pull-ups, and Si7021 address; verify SCL/SDA pins in the project.
- **No VCOM output:** Ensure the correct VCOM port and baud rate; confirm USART is configured for the console.
- **Build errors:** Verify target part and that I2C SPM and Si7021 (or equivalent) components are present.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)

## Note

This project talks to the **Si7021** using explicit I2C writes and reads in `i2cspm.c`, so the I2CSPM usage stays easy to step through. It does **not** add the Si70xx driver component or the **RHT UniDriver**—those wrap the same sensor protocol for normal application code.

Silicon Labs **Wireless Pro Kit** mainboards differ: **BRD4002A** includes Si70xx RHT; **BRD4002B** includes SHT4x. To build **one** firmware that discovers and works with either part, use an **RHT UniDriver** example such as **`rht_unidriver_baremetal`** or **`segment_lcd_tempsensor`**.

