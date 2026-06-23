# USB Device Composite FreeRTOS

This example demonstrates a composite USB device (CDC ACM + HID mouse) with FreeRTOS. Use the serial interface to send commands that move the mouse.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This FreeRTOS example creates a composite USB device with a CDC ACM interface and an HID mouse interface. Connect to the CDC ACM COM port with a serial client and send text commands to change the mouse position. **Note:** Commands are parsed only when an End of Line is received. For correct behavior, set your terminal EOL to CR or LF only, not CRLF.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with USB device support.

**Software**
- Simplicity Studio 5 (or later). A serial terminal to connect to the CDC ACM COM port.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB to the PC. Flash and run the application.
3. On the PC, open the CDC ACM COM port with a serial terminal. Send commands (per the application menu or documentation) to move the mouse. Ensure EOL is set to CR or LF only.

## Troubleshooting

- **COM port not found:** Ensure USB cable supports data; check that the composite device enumerates and the CDC ACM interface is available.
- **Commands not working:** Set terminal EOL to CR or LF (not CRLF); verify command format.
- **Build errors:** Verify target part has USB device support and that the USB stack (CDC ACM + HID) and FreeRTOS are configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
