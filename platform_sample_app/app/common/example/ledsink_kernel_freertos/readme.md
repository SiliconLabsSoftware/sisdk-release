# LEDSINK FreeRTOS

This example demonstrates the LEDSINK peripheral with hardware pattern generation with no PWM, PWM brightness, software direct drive, and a button-triggered EM2 deep-sleep test in a FreeRTOS kernel task.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example exercises the LEDSINK peripheral from a FreeRTOS task. A demo task cycles every 5 seconds through three modes: hardware pattern generator (NON-PWM), hardware pattern generator with PWM brightness, and software direct drive of a 4-bit binary counter. A second, higher-priority task is dedicated to the BTN0-triggered EM2 deep-sleep test: it configures an LEDSINK pattern, drops the demo's EM1 power-manager floor, and `vTaskDelay`s for a few seconds so tickless idle takes the chip into EM2 while the LEDs pause, then re-triggers the pattern on wake. Status is conveyed by the LEDs and the `em2_entry_count` variable can be inspected in the debugger to confirm EM2 transitions. Use it to learn the LEDSINK HAL API with FreeRTOS.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs board with the LEDSINK0 peripheral, four LED channels, and BTN0.

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
- **Build errors:** Verify target part and that the `hal_ledsink`, `power_manager`, `simple_button`, and FreeRTOS components are present.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
