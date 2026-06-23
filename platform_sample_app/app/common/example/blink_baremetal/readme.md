# Blink Bare-metal

This example project shows how to blink an LED in a bare-metal configuration.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example demonstrates the simplest bare-metal application: it blinks an on-board LED at a fixed period (e.g. 500 ms) without an RTOS. It uses the Sleeptimer service for delay and the Simple LED driver. You can change the LED instance and toggle period in `blink.c`. This is a good starting point to verify toolchain, board support, and basic drivers.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with at least one on-board LED.

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and flash the application.
3. Run the application. The LED should blink at the configured period (e.g. 500 ms).
4. Optionally edit `blink.c` to change the period or LED instance, then rebuild and flash.

## Troubleshooting

- **LED does not blink:** Ensure the board has an on-board LED and that the LED instance (e.g. led0) in the project matches your board.
- **Wrong blink rate:** Check the period defined in `blink.c` and that the clock/sleeptimer configuration is correct for your part.
- **Build or flash errors:** Verify the correct target part and board are selected; check that the kit is connected and recognized by Studio.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
