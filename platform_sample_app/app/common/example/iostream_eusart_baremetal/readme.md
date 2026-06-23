# I/O Stream EUSART Bare-metal

Uses the I/O Stream service to demonstrate EUSART over the kit's virtual COM port (VCOM). Characters you send are echoed back; connect via USB or Ethernet port 4902.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example shows how to use the I/O Stream service in a bare-metal application to send and receive data over EUSART. The kit appears as a virtual COM port (VCOM) on the host. Any characters you type in a terminal are sent to the device and echoed back, so you can verify the serial link and the I/O Stream EUSART component. The demo works over USB (when the kit is connected by USB) or over TCP port 4902 when the kit is connected by Ethernet.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with EUSART support (e.g. xG24 Explorer Kit, xG28 Dev Kit).
- USB cable or Ethernet connection, depending on how you want to use VCOM.

**Software**
- Simplicity Studio 5 (or later).
- A terminal application (e.g. the Studio Console, PuTTY, or a serial terminal) to connect to VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB (or Ethernet, if using network VCOM).
3. Flash and run the application on the board.
4. In Studio, open the **Console** or use your serial terminal and select the kit's VCOM port (or connect to the kit's IP on port 4902 if using Ethernet).
5. Type characters in the terminal; they should be echoed back by the device.

## Troubleshooting

- **No VCOM port:** Ensure the kit is connected and the correct VCOM driver is installed. Check Device Manager (Windows) or `ls /dev/tty*` (Linux/macOS).
- **No echo:** Confirm the terminal is attached to the correct port and baud rate. The example uses the default VCOM configuration from the project.
- **Port 4902 (Ethernet):** If using Ethernet, ensure the kit and host are on the same network and that port 4902 is not blocked by a firewall.

## Resources

- [I/O Stream Documentation](https://docs.silabs.com/gecko-platform/latest/service-api/group-iostream)
- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
