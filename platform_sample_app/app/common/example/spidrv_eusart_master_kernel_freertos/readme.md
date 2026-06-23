# SPIDRV Master FreeRTOS (EUSART)

This example demonstrates the SPI driver in master mode using EUSART in a FreeRTOS task. Connect two kits to exchange data; log output over VCOM.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This FreeRTOS example uses the SPI driver in master mode (EUSART). Install this app on one kit and the SPI slave example on a second kit; connect them via the expansion header (CS–CS, SCLK–SCLK, MOSI–MOSI, MISO–MISO). The two devices periodically exchange data; exchanges are logged over VCOM. Use it to learn SPIDRV master operation with FreeRTOS.

## Prerequisites / Setup Requirements

**Hardware**
- Two Silicon Labs kits with EUSART/SPI support. Connect CS–CS, SCLK–SCLK, MOSI–MOSI, MISO–MISO.

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it. Build and flash the slave example on the second kit.
2. Connect the two kits via SPI lines.
3. Flash and run both boards. Connect a serial terminal to either kit's VCOM to see exchange logs.

## Troubleshooting

- **No data exchange:** Verify wiring; ensure one board is master and one is slave; check clock and baud rate.
- **No VCOM output:** Ensure correct VCOM port and baud rate; check FreeRTOS task and USART.
- **Build errors:** Verify target part has EUSART and that SPIDRV and FreeRTOS are configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
