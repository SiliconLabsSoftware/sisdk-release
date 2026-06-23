# Joystick Bare-metal

Prints joystick position at intervals over VCOM so you can view it in a terminal. Requires Wireless Pro Kit (BRD4002A) as the mainboard.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example demonstrates the Joystick driver in a bare-metal application. It reads the joystick position at regular intervals and prints the values over the virtual COM port (VCOM). You can view the output in a terminal to see how position changes as you move the joystick. This example requires the Wireless Pro Kit (BRD4002A) as the mainboard to mount a compatible radio board with a joystick.

## Prerequisites / Setup Requirements

**Hardware**
- Wireless Pro Kit (BRD4002A) as mainboard.
- Compatible radio board with joystick (e.g. BRD4184A, BRD4185A).
- USB cable for VCOM.

**Software**
- Simplicity Studio 5 (or later).
- A terminal application to connect to VCOM.

## Steps to Run Demo

1. Mount the compatible radio board on the Wireless Pro Kit (BRD4002A).
2. Open the project in Simplicity Studio and build it.
3. Connect the kit via USB and flash the application.
4. Open the Studio Console or a serial terminal and select the kit's VCOM port.
5. Move the joystick; position values should be printed at intervals.

## Troubleshooting

- **No output:** Ensure you are using BRD4002A as the mainboard and a radio board with a joystick.
- **Wrong or no VCOM:** Check that the kit is connected and the VCOM driver is installed.
- **Incorrect readings:** Verify the radio board is firmly seated and the joystick hardware is working.

## Resources

- [Joystick Driver Documentation](https://docs.silabs.com/gecko-platform/latest/driver-api/group-joystick)
- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
