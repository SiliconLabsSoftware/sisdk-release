# USB Device CDC ACM FreeRTOS

This example uses the USB stack CDC ACM class with FreeRTOS. The device creates a COM port on your PC; connect with a terminal to use the echo menu.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This FreeRTOS example demonstrates the USB stack with the CDC ACM class. When the USB device is connected to a PC, it enumerates as a virtual COM port. Open a terminal on that COM port to see a menu (e.g. Echo 1, Echo N, Echo N asynchronously). Choose an option to echo characters you type. **Note:** For options 2 and 3 you can send up to 512 bytes at once. If the payload is an exact multiple of the Bulk OUT max packet size (64 bytes at full speed), the demo can block because some terminals do not send a zero-length packet (ZLP); this is a known demo limitation.

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

- **COM port not found:** Ensure USB cable supports data (not charge-only); check device manager for the CDC ACM port; install any required USB drivers.
- **Demo blocks on large transfer:** Avoid sending a payload that is an exact multiple of 64 bytes when using Echo N or Echo N asynchronously; or send additional data so a ZLP is sent.
- **Build errors:** Verify target part has USB device support and that the USB stack and FreeRTOS are configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
