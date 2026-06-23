# Segment LCD Tempsensor

This project demonstrates using the Si70xx temperature sensor to measure temperature and display values on the segment LCD.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the Si70xx (or Si7021) relative humidity and temperature sensor to read temperature and display it on the segment LCD. A periodic sleeptimer callback (e.g. every 5 seconds) reads the sensor and updates the LCD. Use it to learn I2C sensor integration and segment LCD display. **Note:** Board self-heating can affect readings; for better accuracy use battery or Mini Simplicity connector so the on-board debugger is in a low-power state.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with segment LCD and Si70xx/Si7021 sensor (on-board or expansion).

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the board via USB, flash the application, and reset the board.
3. Observe the LCD showing initial value (e.g. 00000 or 25.000); after about 5 seconds it updates with the current temperature. The display updates every 5 seconds.

## Troubleshooting

- **No temperature reading:** Check I2C wiring and sensor address; verify Si70xx driver and segment LCD are configured for your board.
- **Stale or wrong values:** Ensure the sensor is connected and powered; consider thermal isolation from the board for more accurate readings.
- **Build errors:** Verify target part and that Si70xx and segment LCD components are included.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)