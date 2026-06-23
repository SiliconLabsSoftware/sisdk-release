# TEMPDRV FreeRTOS

This example demonstrates the internal temperature sensor driver in a FreeRTOS kernel task. Temperature limits and LED feedback are shown; status is printed on VCOM.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This FreeRTOS example uses the temperature sensor (TEMPDRV) driver. The initial temperature is read; upper and lower limits are calculated from TEMPERATURE_BAND_C. If temperature goes outside the range, LED0 (low) or LED1 (high) turns on and stays on until temperature returns within the acceptable range (± HYSTERESIS_C). Status is also printed on the VCOM serial port. Use it to learn on-chip temperature sensing with FreeRTOS.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with an internal temperature sensor and (optionally) two LEDs.

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM output.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and flash the application.
3. Run the application. Observe LED behavior and/or VCOM output as temperature changes (e.g. touch the part or change ambient temperature).
4. Optionally adjust TEMPERATURE_BAND_C and HYSTERESIS_C and rebuild.

## Troubleshooting

- **No temperature or wrong readings:** Verify TEMPDRV is configured for your part; ensure the ADC/input is correct for the internal sensor.
- **No VCOM output:** Ensure correct VCOM port and baud rate; check FreeRTOS task and USART.
- **Build errors:** Verify target part has an internal temperature sensor and that TEMPDRV and FreeRTOS are configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
