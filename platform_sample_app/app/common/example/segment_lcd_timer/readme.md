# Segment LCD Timer

This project shows how to use the segment LCD peripheral to display timer functions (start/stop, reset, compare mode).

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the segment LCD to show a timer. LETIMER runs at 1 Hz and updates the display. **Regular mode:** Button 0 — start/stop timer; Button 1 single click — reset timer. **Compare mode:** Button 1 hold 2+ seconds to enter compare mode; Button 0 sets compare value; Button 1 exits setup; Button 0 starts timer; on compare match the LCD blinks with the value; Button 0 or 1 exits compare mode. Use it to learn segment LCD and LETIMER for a simple timer UI.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with segment LCD and two push buttons.

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the board via USB, flash the application, and reset the board.
3. Observe the segment LCD showing 00000. Press Button 0 to start/stop the timer; Button 1 to reset. Use Button 1 hold to enter compare mode and follow the button sequence above.

## Troubleshooting

- **LCD not updating:** Verify segment LCD and LETIMER configuration; check GPIO for buttons.
- **Buttons not responding:** Ensure button pins match the board and are configured as inputs with interrupts.
- **Build errors:** Verify target part and segment LCD and LETIMER components; check board support.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
