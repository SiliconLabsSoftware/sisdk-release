# LEDSINK Bare-metal

This example demonstrates the LEDSINK peripheral with hardware pattern generation with no PWM, PWM brightness, software direct drive, and a button-triggered EM2 deep-sleep test in a bare-metal configuration.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This bare-metal example exercises the LEDSINK peripheral on four channels. A periodic 5 s sleeptimer cycles the demo through three modes: hardware pattern generator (NON-PWM), hardware pattern generator with PWM brightness, and software direct drive of a 4-bit binary counter. Pressing BTN0 runs a one-shot EM2 deep-sleep test: the device blinks an LEDSINK pattern, sleeps in EM2 for a few seconds with the LEDs paused, then wakes and re-triggers the pattern. Status is conveyed by the LEDs and the `em2_entry_count` variable can be inspected in the debugger to confirm EM2 transitions. Use it to learn the LEDSINK HAL API and basic low-power integration.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with the LEDSINK0 peripheral, four LEDs to connect to four LED channels, and BTN0.

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB and flash the application.
3. Observe the LEDs cycling through the three modes every 5 seconds.
4. Press BTN0 to run the EM2 test: the LEDs blink, pause for a few seconds while the device is in EM2, then resume.
5. Can observe the led data either by hw leds or connect analyzer at pins on WPK Board LED(0 to 3) at P30,P31,P32,P33 pins.
6. Use "COMMANDER AEM MEASURE" or Energy Profiler to measure current in each mode if desired.

## Troubleshooting

- **LEDs not lighting:** Verify the board has LEDSINK0 and that the LED channels are correctly mapped.
- **`em2_entry_count` not incrementing after BTN0:** A stray EM1 requirement is keeping the device out of deepsleep. With a debugger attached, confirm `SL_DEVICE_INIT_EMU_EM2_DEBUG_ENABLE` is `1` in `sl_device_init_emu_config.h`.
- **Build errors:** Verify target part and that the `hal_ledsink`, `sleeptimer`, `power_manager`, and `simple_button` components are present.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
