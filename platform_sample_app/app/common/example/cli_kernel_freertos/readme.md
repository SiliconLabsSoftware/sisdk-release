# CLI Kernel FreeRTOS

This example demonstrates how to use the CLI driver with a FreeRTOS kernel task over the VCOM serial port.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example shows the command line interface (CLI) component running in a FreeRTOS task. Use the CLI over the kit's VCOM serial port. Sample commands: echo_str (echo arguments as strings), echo_int (parse and echo integers), LED (turn on, off, or toggle board LEDs). Use it to add CLI to a FreeRTOS-based application.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with USART and on-board LED.

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM (e.g. Studio Console, PuTTY).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB (or Ethernet for network VCOM), flash and run.
3. Open the Console or serial terminal and select the kit's VCOM port.
4. Type commands (e.g. `echo_str hello`, `LED toggle`) and press Enter to see responses.

## Troubleshooting

- **No VCOM port:** Ensure the kit is connected and VCOM drivers are installed.
- **No response to commands:** Confirm the terminal is on the correct port and baud rate; check FreeRTOS task and CLI initialization.
- **LED command does nothing:** Verify the board has an on-board LED and the LED instance in the project matches your board.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
