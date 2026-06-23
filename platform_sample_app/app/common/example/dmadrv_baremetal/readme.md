# DMADRV Bare-metal

This example shows how to use the DMADRV driver to transfer data between memory and a USART peripheral in a bare-metal configuration.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example demonstrates the direct memory access (DMA) driver: data is transferred between memory and a USART. You are prompted to enter data over the VCOM serial port; once the configured amount of data has been transferred, it is echoed back. Use it to learn DMA-based UART transfers without an RTOS.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with USART and DMA support.

**Software**
- Simplicity Studio 5 (or later). A serial terminal to connect to VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB, flash and run.
3. Open a serial terminal on the kit's VCOM port.
4. Enter the expected amount of data; the application echoes it back after the DMA transfer completes.

## Troubleshooting

- **No echo or wrong data:** Confirm the terminal is on the correct VCOM port and baud rate; check DMA channel and USART configuration.
- **Transfer never completes:** Verify the configured transfer size and that DMA and USART are correctly linked.
- **Build errors:** Ensure the target part has DMA and that DMADRV and USART components are configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
