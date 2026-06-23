# Common Token Manager Bare-metal

This example demonstrates use of the CTM (Common Token Manager) interface. Use the CLI to write, read, and delete tokens.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example shows how to use the Common Token Manager (CTM) for series 2 devices. The application uses the command line interface so you can write, read, and delete tokens. Commands include: write_custom_static_token, read_custom_static_token, write_dynamic_token, read_dynamic_token, delete_dynamic_token, write_counter_token, read_counter_token, increment_counter_token. See the application source and CLI help for arguments. Use this to integrate token management into your application.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board (series 2) with support for CTM and serial (VCOM).

**Software**
- Simplicity Studio 5 (or later). A serial terminal to connect to VCOM.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB, flash and run.
3. Open a serial terminal on the kit's VCOM port.
4. Use the CLI commands to write, read, and delete tokens as needed.

## Troubleshooting

- **No VCOM or no CLI response:** Ensure the kit is connected and VCOM drivers are installed; confirm correct port and baud rate.
- **Token errors:** Check token key/size and that the device supports the token types you use.
- **Build errors:** Verify target part and that CTM/CLI components are correctly configured.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
