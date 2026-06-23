# NVM3 Kernel FreeRTOS

Demonstrates the NVM3 non-volatile storage API with FreeRTOS. Use the serial CLI to write, read, delete, and repack objects; counts are tracked.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example demonstrates the NVM3 interface in a FreeRTOS application. You use a CLI over the serial connection to write, read, delete, and repack NVM3 data objects. Write and delete counts are tracked. The repack operation allows you to reclaim space and optimize NVM3 storage.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with NVM3/Flash support.
- USB cable for serial/VCOM.

**Software**
- Simplicity Studio 5 (or later).
- A terminal application to connect to the kit's VCOM/serial port.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB and flash the application.
3. Open the Studio Console or a serial terminal and connect to the kit's VCOM port.
4. Use the CLI commands (write, read, delete, repack) to interact with NVM3.
5. Observe the counter values and try repack to see how it affects storage.

## Troubleshooting

- **No serial output:** Ensure the kit is connected and VCOM is selected.
- **NVM3/repack errors:** Ensure the project is built for a part that supports NVM3 and that you have followed the CLI usage documented in the app.

## Resources

- [AN1135: Using Third Generation Non-Volatile Memory (NVM3) Data Storage](https://www.silabs.com/documents/public/application-notes/an1135-using-third-generation-nonvolatile-memory.pdf)
- [NVM3 Documentation](https://docs.silabs.com/gecko-platform/latest/service-api/group-nvm3)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
