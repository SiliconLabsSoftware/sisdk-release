# Blink PWM FreeRTOS

This example uses the PWM driver with a TIMER to gradually adjust LED intensity up and down in a FreeRTOS task.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example drives an LED with PWM in a FreeRTOS task to create a breathing or fade effect. PWM inputs and the PWM LED instance can be configured in the application source (e.g. `blink_pwm_app.c`). Use it to learn PWM with FreeRTOS.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with an on-board PWM LED.

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and flash the application.
3. Run the application. The LED should fade up and down in a repeating pattern.
4. Optionally adjust PWM settings in the source, then rebuild and flash.

## Troubleshooting

- **LED does not change intensity:** Confirm the LED is on a PWM-capable pin and the project pin/route matches your board.
- **No PWM output:** Check TIMER and PWM driver configuration and FreeRTOS task scheduling.
- **Build or flash errors:** Verify target part and board; ensure the kit is connected and recognized.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
