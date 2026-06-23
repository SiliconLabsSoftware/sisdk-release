# Sleeptimer Kernel FreeRTOS

Demonstrates periodic and one-shot RTC timers in a FreeRTOS task. Use buttons to stop or restart timers; status is reported over VCOM.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example demonstrates the Sleeptimer service in a FreeRTOS application. It uses the low-frequency RTC to create periodic and one-shot timers running in a FreeRTOS task. A periodic timer toggles LED0; a one-shot timer toggles LED1 once; a status timer prints the remaining time of the other two over VCOM. Button0 controls the periodic timer start/stop; Button1 controls the one-shot timer. This shows how to combine Sleeptimer with FreeRTOS for timed behavior and button-driven control.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with low-frequency RTC, at least 2 buttons and 2 LEDs.
- USB cable for VCOM.

**Software**
- Simplicity Studio 5 (or later).
- A terminal application to connect to VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB and flash the application.
3. Open the Studio Console or a serial terminal and select the kit's VCOM port.
4. After reset, both timers start. Observe LED0 (periodic) and LED1 (one-shot).
5. Use Button0 to stop/start the periodic timer; use Button1 to stop/start the one-shot timer.
6. Watch the terminal for status messages.

## Troubleshooting

- **No LED or button response:** Ensure the board has 2 buttons and 2 LEDs and pin configuration matches your board.
- **No VCOM output:** Check kit connection and VCOM port; verify baud rate.
- **Timers not firing:** Ensure the low-frequency oscillator and RTC are configured for the part.

## Resources

- [AN0014: EFM32 Timers](https://www.silabs.com/documents/public/application-notes/an0014-efm32-timers.pdf)
- [Sleeptimer Service](https://docs.silabs.com/gecko-platform/latest/service-api/group-sleeptimer)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
