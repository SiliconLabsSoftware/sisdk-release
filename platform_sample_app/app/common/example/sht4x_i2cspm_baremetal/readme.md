# SHT4x I2C SPM Bare-metal

This example demonstrates the I2C Simple Polled Master driver with the SHT4x humidity and temperature sensor in a bare-metal configuration.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example uses the I2C Simple Polled Master (SPM) driver to read the SHT4x relative humidity and temperature sensor. Upper and lower limits are set from TEMPERATURE_BAND_C. When temperature exceeds the upper limit, LED0 turns on and "Temperature is high" is printed on VCOM; when it falls below the lower limit, LED1 turns on and "Temperature is low" is printed. If only the console is available, the messages still appear on VCOM. Use it to learn I2C SPM with the SHT4x sensor.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with I2C support and an SHT4x sensor (on-board or expansion). On-board LEDs if using LED feedback.

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM output.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and SHT4x sensor (if on expansion board) with correct I2C wiring.
3. Flash and run. Observe temperature-based LED behavior and/or "Temperature is high/low" on VCOM.
4. Optionally adjust TEMPERATURE_BAND_C and rebuild.

## Troubleshooting

- **No sensor readings:** Check I2C wiring, pull-ups, and SHT4x address; verify SCL/SDA pins in the project.
- **No VCOM output:** Ensure correct VCOM port and baud rate; confirm USART is configured for the console.
- **Build errors:** Verify target part and that I2C SPM and SHT4x components are present.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)

## Note

This project talks to the **SHT4x** using explicit I2C writes and reads in `i2cspm.c`, so the I2CSPM usage stays easy to step through. It does **not** add the SHT4x driver component or the **RHT UniDriver**—those wrap the same sensor protocol for normal application code.

The **SHT4x** RHT is on **Wireless Pro Kit BRD4002B**; **BRD4002A** uses Si70xx instead. To build **one** firmware that discovers and works with either mainboard, use an **RHT UniDriver** example such as **`rht_unidriver_baremetal`** or **`segment_lcd_tempsensor`**.

