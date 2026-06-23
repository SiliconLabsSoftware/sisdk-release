# USB Device HID FreeRTOS

This example demonstrates the USB stack HID class with FreeRTOS. When connected to a PC, the device acts as a mouse and triggers continuous mouse movements.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This FreeRTOS example uses the USB stack HID class to implement a USB mouse. Once the device is connected to a computer, it enumerates as an HID mouse and drives continuous mouse movements so you can see the cursor move. Use it to learn USB HID device implementation with FreeRTOS.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with USB device support.

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB to the PC. Flash and run the application.
3. The PC should recognize the device as a mouse; the cursor will move continuously to demonstrate HID reporting.

## Troubleshooting

- **Device not recognized:** Ensure USB cable supports data; check device manager for HID device; install any required drivers.
- **No mouse movement:** Verify USB enumeration and that the HID report descriptor and report data are correct for a mouse.
- **Build errors:** Verify target part has USB device support and that the USB stack (HID) and FreeRTOS are configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
