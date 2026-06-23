# DMADRV Kernel FreeRTOS

This example shows how to use the DMADRV driver to transfer data between memory and an EUSART peripheral in a FreeRTOS configuration.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This FreeRTOS example demonstrates DMA-based data transfer using DMADRV with EUSART. It uses FreeRTOS tasks and semaphores for synchronization and provides echo functionality: data you send over VCOM is transferred via DMA and echoed back. Use it to integrate DMADRV with a multitasking application.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with EUSART and DMA support.

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB, flash and run.
3. Open a serial terminal on the kit's VCOM port.
4. Send data; the application echoes it back after the DMA transfer completes.

## Troubleshooting

- **No echo or wrong data:** Confirm the terminal is on the correct VCOM port and baud rate; check DMA and EUSART configuration and FreeRTOS task scheduling.
- **Transfer never completes:** Verify DMA channel, EUSART, and semaphore usage in the application.
- **Build errors:** Ensure the target part has DMA and that DMADRV, EUSART, and FreeRTOS are configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
