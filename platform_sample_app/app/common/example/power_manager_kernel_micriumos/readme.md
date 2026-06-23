# Power Manager Kernel Micrium OS

This example demonstrates use of the Power Manager module in a Micrium OS kernel task. Cycle through energy modes with buttons.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example shows the Power Manager in a Micrium OS task. Click Button 1 to cycle energy modes (1 click → EM1, 2 clicks → EM2, etc.); Button 0 confirms. The device stays in the selected mode until: EM1/EM2 — sleep timer expires; EM3 — button push; EM4 — reset. **Note:** DCDC Boost devices do not enter EM4. Enabling SL_POWER_MANAGER_INIT_EMU_EM2_DEBUG_ENABLE keeps PD0B/PD0D active in EM2 for debugger connectivity but increases EM2/EM3 power.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with buttons (and optional LCD if used by the demo).

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and flash the application.
3. Run the application. Use Button 1 to cycle modes, Button 0 to confirm.
4. Use Energy Profiler to measure current in each mode if desired.

## Troubleshooting

- **Cannot enter EM4:** On DCDC Boost devices, EM4 is not supported.
- **Debugger loses connection in EM2/EM3:** Consider EM2 debug option; note it increases power.
- **Build errors:** Verify target part and Power Manager and Micrium OS components.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
