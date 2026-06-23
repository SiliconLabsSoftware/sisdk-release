# MEMLCD Kernel Micrium OS

This example demonstrates the Memory LCD (MEMLCD) module in a Micrium OS kernel task using the Silicon Labs Graphics Library (glib).

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the Memory LCD module and glib in a Micrium OS kernel task. Button 0 clears the LCD; Button 1 prints "Hello World!" on the LCD. Use it to learn MEMLCD and glib in a multitasking application.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with a Memory LCD (e.g. Sharp memory LCD) and two buttons.

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and flash the application.
3. Run the application. Use Button 0 to clear the display and Button 1 to show "Hello World!".

## Troubleshooting

- **No display output:** Verify MEMLCD connections and LCD type; check SPI/pin configuration and Micrium OS task scheduling.
- **Buttons not responding:** Ensure button GPIOs match the board and are configured in the project.
- **Build errors:** Verify target part and MEMLCD, glib, and Micrium OS components.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
