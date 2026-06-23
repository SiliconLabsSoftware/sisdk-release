# Segment LCD LDMA

This project shows how to use the LCD segment peripheral with the LDMA to update the segment LCD in EM2.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the segment LCD driver with the LDMA so the display updates in EM2 without CPU intervention. The LCD frame counter triggers a DMA request every second; the LDMA uses linked descriptors to copy a display buffer to the LCD segment registers. The display cycles 00000 → 11111 → … → 99999. Use it to learn low-power segment LCD updates with LDMA.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with segment LCD (see project or board documentation for supported boards).

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the board via USB, flash the application, and reset the board.
3. Observe the segment LCD displaying 00000 → 11111 → … → 99999, updating every second. The device can remain in EM2 while the LDMA updates the display.

## Troubleshooting

- **LCD not updating:** Verify segment LCD and LDMA configuration; ensure the correct board/part is selected and LCD pins match the board.
- **Wrong digits or no display:** Check display buffer content and LCD segment register mapping for your board.
- **Build errors:** Ensure the target part has segment LCD and LDMA; verify board support.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
