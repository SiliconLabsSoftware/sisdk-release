# Simple Button Kernel Micrium OS

This example demonstrates button use in a Micrium OS kernel task. The LED toggles on each button press.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the Simple Button driver in a Micrium OS kernel task: each button press toggles an LED. You can change task priority, task stack size, LED and button instance in the application source. Use it to learn button handling and LED control with Micrium OS.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with at least one button and one LED.

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and flash the application.
3. Run the application. Press the button to toggle the LED.

## Troubleshooting

- **LED does not toggle:** Verify button and LED instances and GPIO pins match your board; check Micrium OS task and button driver configuration.
- **Multiple toggles per press:** Consider debouncing; ensure task and button handling are correct.
- **Build errors:** Verify target part and Simple Button, LED driver, and Micrium OS components.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
