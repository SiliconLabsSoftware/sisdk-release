# CLI Bare-metal

This example demonstrates how to use the CLI driver in a bare-metal configuration over the VCOM serial port.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example shows how to use the command line interface (CLI) component over the kit's virtual COM port (VCOM). It provides sample commands such as echo_str (echo arguments as strings), echo_int (parse and echo integers), and LED (turn on, off, or toggle board LEDs). Use it to add CLI to your own bare-metal application.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with USART and on-board LED.

**Software**
- Simplicity Studio 5 (or later). A serial terminal to connect to VCOM (e.g. Studio Console, PuTTY).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB (or Ethernet for network VCOM), flash and run.
3. Open the Console or serial terminal and select the kit's VCOM port.
4. Type commands (e.g. `echo_str hello`, `LED toggle`) and press Enter to see responses.

## Troubleshooting

- **No VCOM port:** Ensure the kit is connected and VCOM drivers are installed. Check Device Manager (Windows) or `ls /dev/tty*` (Linux/macOS).
- **No response to commands:** Confirm the terminal is attached to the correct port and baud rate; check that CLI is initialized and linked to the correct stream.
- **LED command does nothing:** Verify the board has an on-board LED and the LED instance in the project matches your board.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
