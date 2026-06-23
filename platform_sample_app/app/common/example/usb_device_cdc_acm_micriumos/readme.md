# USB Device CDC ACM Micrium OS

This example uses the USB stack CDC ACM class with the Micrium OS kernel. The device creates a COM port on your PC; connect with a terminal to use the echo menu.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This Micrium OS example demonstrates the USB stack with the CDC ACM class. When the USB device is connected to a PC, it enumerates as a virtual COM port. Open a terminal on that COM port to see a menu (e.g. Echo 1, Echo N, Echo N asynchronously). Choose an option to echo characters you type. **Note:** For options that accept multiple bytes, if the payload is an exact multiple of the Bulk OUT max packet size (64 bytes at full speed), the demo can block if the terminal does not send a zero-length packet (ZLP).

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with USB device support.

**Software**
- Simplicity Studio 5 (or later). A serial/terminal application to open the CDC ACM COM port.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB to the PC. Flash and run the application.
3. On the PC, open the new COM port with a terminal. Use the menu to choose an echo option and type characters to see them echoed.

## Troubleshooting

- **COM port not found:** Ensure USB cable supports data; check device manager for the CDC ACM port; install any required USB drivers.
- **Demo blocks on large transfer:** Avoid sending an exact multiple of 64 bytes when using multi-byte echo options, or ensure the terminal sends a ZLP.
- **Build errors:** Verify target part has USB device support and that the USB stack and Micrium OS are configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
