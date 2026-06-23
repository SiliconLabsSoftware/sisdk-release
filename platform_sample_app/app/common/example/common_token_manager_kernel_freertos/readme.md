# Common Token Manager Kernel FreeRTOS

This example demonstrates use of the CTM (Common Token Manager) interface with FreeRTOS. Use the CLI to write, read, and delete tokens.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example shows the Common Token Manager (CTM) for series 3 devices running with FreeRTOS. The CLI is used to execute token operations. Commands include write_static_token, read_static_token, write_dynamic_token, read_dynamic_token, delete_dynamic_token, write_counter_token, read_counter_token, increment_counter_token. CAUTION: Static device token writes are limited; they are disabled by default (define SAMPLE_APP_ENABLE_STATIC_DEVICE_TOKENS in ctm_app.c to enable). See application source for arguments.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board (series 3) with CTM and serial (VCOM).

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB, flash and run.
3. Open a serial terminal on the kit's VCOM port.
4. Use the CLI commands to write, read, and delete tokens as needed.

## Troubleshooting

- **No VCOM or no CLI response:** Ensure the kit is connected and VCOM drivers are installed; confirm correct port and baud rate.
- **Token errors:** Check token key/size; note static device token write limits.
- **Build errors:** Verify target part and that CTM/CLI/FreeRTOS are correctly configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
