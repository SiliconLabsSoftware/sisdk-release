# Emode Bare-metal

Demo for energy mode current consumption testing using Energy Profiler. Select configuration via LCD; run tests with different emodes, clocks, and DCDC.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal demo illustrates power consumption for different combinations of energy modes (EM1–EM4), clocks, and DCDC using the Energy Profiler. Configuration (emode, oscillator, etc.) is selected via the LCD. Press Button 1 to cycle options; press Button 0 to select and start the test. After the test, reset the board to try another configuration. **Note:** This is a demo only to understand power consumption; do not use as a starting point for product implementation. DCDC Boost devices do not enter EM4. The EMU power configuration register may only be written once after power-on reset; a full power-on reset may be needed for DCDC configuration.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with two buttons and an LCD screen.

**Software**
- Simplicity Studio 5 (or later). Energy Profiler for current measurement.

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and set up Energy Profiler for current measurement.
3. Flash and run. Use Button 1 to cycle options on the LCD, Button 0 to select and start the test.
4. Observe current in Energy Profiler. Reset the board to select and run another configuration.

## Troubleshooting

- **Cannot enter EM4:** On DCDC Boost devices, EM4 is not supported.
- **DCDC not as expected:** Perform a full power-on reset; the EMU power register may be locked after first write.
- **LCD or buttons not responding:** Verify pin and driver configuration for your board.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
