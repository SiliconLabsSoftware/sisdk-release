# Blink PWM Bare-metal

This example uses the PWM driver with a TIMER to gradually adjust LED intensity up and down.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example drives an LED with PWM to create a breathing or fade effect: intensity ramps up and down using a TIMER. Use it to learn the PWM driver and timer-based dimming without an RTOS.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with an on-board LED connected to a PWM-capable pin.

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and flash the application.
3. Run the application. The LED should fade up and down in a repeating pattern.
4. Optionally adjust PWM period or duty in the project configuration and source, then rebuild and flash.

## Troubleshooting

- **LED does not change intensity:** Confirm the LED is on a PWM-capable pin and the pin/route in the project matches your board.
- **No PWM output:** Check TIMER and PWM driver configuration; ensure the correct pin and timer instance are used.
- **Build or flash errors:** Verify target part and board; ensure the kit is connected and recognized.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
