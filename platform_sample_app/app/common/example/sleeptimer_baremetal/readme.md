# Sleeptimer Bare-metal

Demonstrates periodic and one-shot timers using the low-frequency RTC. Use buttons to stop or restart timers; status is reported over VCOM.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example demonstrates the Sleeptimer service in a bare-metal application using the low-frequency RTC (real-time clock). It creates periodic and one-shot timers: one periodic timer toggles LED0 on timeout, one one-shot timer toggles LED1 on timeout, and a status timer prints the remaining time of the other two timers over the virtual COM port. Button0 starts/stops the periodic timer; Button1 starts/stops the one-shot timer. This shows how to use the Sleeptimer API for timing and how to control timers from button input.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with low-frequency RTC, at least 2 buttons and 2 LEDs.
- USB cable for VCOM (to view status output).

**Software**
- Simplicity Studio 5 (or later).
- A terminal application to connect to VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB and flash the application.
3. Open the Studio Console or a serial terminal and select the kit's VCOM port.
4. After reset, both the periodic and one-shot timers start. Observe LED0 toggling (periodic) and LED1 toggling once (one-shot).
5. Use Button0 to stop/start the periodic timer; use Button1 to stop/start the one-shot timer.
6. Watch the terminal for status messages showing remaining time of the timers.

## Troubleshooting

- **No LED or button response:** Ensure the board has 2 buttons and 2 LEDs and that the pin configuration in the project matches your board.
- **No VCOM output:** Check that the kit is connected and the correct VCOM port is selected. Verify baud rate.
- **Timers not firing:** Ensure the low-frequency oscillator (LFRCO or LFXO) is enabled and the RTC is configured correctly for the part.

## Resources

- [AN0014: EFM32 Timers](https://www.silabs.com/documents/public/application-notes/AN0014.pdf)
- [Sleeptimer Service](https://docs.silabs.com/gecko-platform/latest/service-api/group-sleeptimer)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
