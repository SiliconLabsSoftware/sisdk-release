# Coulomb Counter Bare-metal

This example shows how to use the coulomb counter in a bare-metal configuration. Read total charge and store it in NVM3 via polling or CLI.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example demonstrates the coulomb counter: read total charge consumed and store it in NVM3. You can poll periodically (e.g. every second) or use CLI commands: coulomb_get (coulombs since last boot), coulomb_calibrate, coulomb_get_total (lifetime), coulomb_update_total, coulomb_reset_total. See [AN1188: EFP01 Coulomb Counting](https://www.silabs.com/documents/public/application-notes/an1188-efp01-coulomb-counting.pdf) for details.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with analog pins and UART (for CLI/VCOM).

**Software**
- Simplicity Studio 5 (or later). A serial terminal for VCOM if using CLI.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB, flash and run.
3. Either observe periodic NVM3 updates or open a serial terminal and use coulomb_* CLI commands.

## Troubleshooting

- **No coulomb readings:** Verify analog and coulomb counter configuration for your part; check calibration.
- **No CLI response:** Ensure VCOM port and baud rate are correct; confirm CLI is linked to the right stream.
- **Build errors:** Verify target part and that coulomb counter and NVM3 components are configured.

## Resources

- [AN1188: EFP01 Coulomb Counting](https://www.silabs.com/documents/public/application-notes/an1188-efp01-coulomb-counting.pdf)
- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
