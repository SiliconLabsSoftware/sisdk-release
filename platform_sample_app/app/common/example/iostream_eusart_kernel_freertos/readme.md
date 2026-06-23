# I/O Stream EUSART FreeRTOS

Uses the I/O Stream service with FreeRTOS to demonstrate EUSART over VCOM. Characters you send are echoed back; connect via USB or Ethernet port 4902.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example shows how to use the I/O Stream service with a FreeRTOS task to send and receive data over EUSART. The kit appears as a virtual COM port (VCOM). Characters you type in a terminal are echoed back. The demo works over USB or over TCP port 4902 when the kit is connected by Ethernet.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with EUSART support.
- USB cable or Ethernet connection.

**Software**
- Simplicity Studio 5 (or later).
- A terminal application to connect to VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB or Ethernet.
3. Flash and run the application on the board.
4. Open the Studio Console or a serial terminal and select the kit's VCOM port (or connect to the kit's IP on port 4902 if using Ethernet).
5. Type characters; they should be echoed back.

## Troubleshooting

- **No VCOM port:** Ensure the kit is connected and the VCOM driver is installed.
- **No echo:** Confirm the terminal is on the correct port and baud rate.
- **Port 4902:** If using Ethernet, ensure the kit and host are on the same network and port 4902 is not blocked.

## Resources

- [I/O Stream Documentation](https://docs.silabs.com/gecko-platform/latest/service-api/group-iostream)
- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
