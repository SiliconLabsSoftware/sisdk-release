# NVM3 Bare-metal

Demonstrates the NVM3 non-volatile storage API. Use the serial CLI to write, read, and delete data objects; write and delete counts are tracked.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example demonstrates the NVM3 (Third Generation Non-Volatile Memory) interface in a bare-metal application. You use a command-line interface over the serial connection to write, read, and delete NVM3 data objects. The application can store multiple objects (e.g. up to 10 files); write and delete operations are tracked in counter objects so you can see how many times each operation has been performed.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with NVM3/Flash support (e.g. EFM32, EFR32, PG28).
- USB cable for serial/VCOM.

**Software**
- Simplicity Studio 5 (or later).
- A terminal application to connect to the kit's VCOM/serial port.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB and flash the application.
3. Open the Studio Console or a serial terminal and connect to the kit's VCOM port.
4. Use the CLI commands (e.g. write, read, delete) to interact with NVM3. Refer to the application output or source for the exact command syntax.
5. Observe the counter values for writes and deletes.

## Troubleshooting

- **No serial output:** Ensure the kit is connected and VCOM is selected. Check baud rate matches the project configuration.
- **NVM3 errors:** Some parts require the MPU module for NVM3. Ensure your board is supported and the project is built for the correct part.
- **Commands not recognized:** Verify you are sending the correct CLI commands; see the application source (e.g. `nvm3_app.c`) for the command set.

## Resources

- [AN1135: Using Third Generation Non-Volatile Memory (NVM3) Data Storage](https://www.silabs.com/documents/public/application-notes/an1135-using-third-generation-nonvolatile-memory.pdf)
- [NVM3 Documentation](https://docs.silabs.com/gecko-platform/latest/service-api/group-nvm3)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
