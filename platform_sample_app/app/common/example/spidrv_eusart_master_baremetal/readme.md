# SPIDRV Master Bare-metal (EUSART)

This example demonstrates the SPI driver in master mode using EUSART in a bare-metal configuration. Connect two kits to exchange data; log output over VCOM.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example uses the Serial Peripheral Interface in master mode (EUSART). Install this app on one kit and the SPI slave example on a second kit; connect them via the expansion header (CS–CS, SCLK–SCLK, MOSI–MOSI, MISO–MISO). The two devices periodically exchange data; exchanges are logged over VCOM. Use it to learn SPIDRV master operation without an RTOS.

## Prerequisites / Setup Requirements

**Hardware**
- Two Silicon Labs kits with EUSART/SPI support. Connect primary CS to secondary CS, SCLK to SCLK, MOSI to MOSI, MISO to MISO (e.g. via 20-pin expansion header).

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it. Build and flash the slave example on the second kit.
2. Connect the two kits via SPI lines (CS, SCLK, MOSI, MISO).
3. Flash and run both boards. Connect a serial terminal to either kit's VCOM to see exchange logs.

## Troubleshooting

- **No data exchange:** Verify wiring (CS, SCLK, MOSI, MISO); ensure one board is master and one is slave; check clock polarity/phase and baud rate.
- **No VCOM output:** Ensure correct VCOM port and baud rate; confirm USART is used for console.
- **Build errors:** Verify target part has EUSART and that SPIDRV is configured for master mode.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
