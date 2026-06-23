# Sleeptimer Wallclock Bare-metal

This example demonstrates the sleeptimer wall clock interface in a bare-metal application. Set and get date/time via RTC over VCOM.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example uses the sleeptimer wall clock with the low-frequency RTC to set and get date and time. Operations are controlled over the virtual COM serial port. You can get/set: Unix time (integer), Network Protocol (NTP) time (integer), and date/time (YYYY-MM-DD HH:MM:SS). CLI commands: Help, get_unix_time, set_unix_time, get_ntp_time, set_ntp_time, get_datetime, set_datetime. Use it to learn RTC and wall clock integration.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with RTC (low-frequency) peripheral.

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB, flash and run.
3. Open a serial terminal on the kit's VCOM port. Use the CLI commands to get and set time (e.g. set_unix_time 17, set_datetime YYYY-MM-DD HH:MM:SS).

## Troubleshooting

- **No VCOM or no response:** Ensure the kit is connected and VCOM drivers are installed; confirm correct port and baud rate.
- **Time not persisting:** RTC may need battery backup or correct clock source configuration for your part.
- **Build errors:** Verify target part has RTC and that the sleeptimer wall clock component is configured.

## Resources

- [AN0014: EFM32 Timers](https://www.silabs.com/documents/public/application-notes/AN0014.pdf)
- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
