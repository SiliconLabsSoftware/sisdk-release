# Sleeptimer Wallclock FreeRTOS

This example demonstrates the sleeptimer wall clock interface in a FreeRTOS environment. Set and get date/time via RTC over VCOM.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This FreeRTOS example uses the sleeptimer wall clock with the low-frequency RTC. All wall clock logic runs in a FreeRTOS task. You can get/set Unix time, NTP time, and date/time (YYYY-MM-DD HH:MM:SS) over VCOM. CLI commands: Help, get_unix_time, set_unix_time, get_ntp_time, set_ntp_time, get_datetime, set_datetime. Use it to learn RTC and wall clock with FreeRTOS.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with RTC (low-frequency) peripheral.

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM. FreeRTOS kernel enabled.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB, flash and run.
3. Open a serial terminal on the kit's VCOM port. Use the CLI commands to get and set time.

## Troubleshooting

- **No VCOM or no response:** Ensure the kit is connected and VCOM drivers are installed; check FreeRTOS task and CLI initialization.
- **Time not persisting:** RTC may need battery backup or correct clock source configuration.
- **Build errors:** Verify target part has RTC and that sleeptimer wall clock and FreeRTOS are configured.

## Resources

- [AN0014: EFM32 Timers](https://www.silabs.com/documents/public/application-notes/AN0014.pdf)
- [FreeRTOS Kernel Documentation](https://www.freertos.org/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
