# LED Boost DCDC Bare-metal

This example demonstrates the DCDC boost LEDVDD output running in a bare-metal (no RTOS) build. The application runs a self-driven loop that continuously alternates between an LEDVDD ramp in EM0 and a low-power EM2 dwell, so the behavior on the LEDVDD pin and on the AEM can be observed without any user input.

- **Boot**            -> Leaves the DCDC untouched (LEDVDD = input-rail passthrough, ~3.2 V on a typical board), subscribes to EM-transition events, and enters the main loop.
- **Odd iteration**   -> Brings DCDC boost up, ramps LEDVDD 1.8 V -> 3.8 V using the `LEDVDDRAMPDONE` interrupt flag, then powers the DCDC off and gates its bus clock.
- **Even iteration**  -> Brings DCDC boost up, parks LEDVDD at 1.8 V, and drops the device into EM2 for a fixed dwell. EM2 exit is driven by the sleeptimer.

A short delay (`LEDBOOST_DEBOUNCE_MS`) separates each iteration so the transitions are clearly visible  on a scope.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example brings up the DCDC boost regulator on a bare-metal application and runs a two-action sequence in an infinite loop:

| Iteration   | Action                                                                                     | Power state           |
|-------------|--------------------------------------------------------------------------------------------|-----------------------|
| Odd         | Init DCDC boost, ramp LEDVDD 1.8 V -> 3.8 V, power DCDC off, gate DCDC bus clock           | EM0                   |
| Even        | Init DCDC boost, park LEDVDD at 1.8 V, dwell in EM2 for `LEDBOOST_EM2_MS`                  | EM2 (LEDVDD = 1.8 V)  |

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with DCDC LEDVDD support.
- USB cable for flashing and powering the board.
- An external current meter to observe the EM0/EM2 current.
- Multimeter or oscilloscope on the LEDVDD pin to observe the voltage transitions.

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit via USB and flash the application with Simplicity Commander.
3. Reset the board. The application begins running the alternating sequence automatically:
   - Odd iteration: LEDVDD ramps 1.8 V -> 3.8 V, then drops to the passthrough level (~3.2 V) after the DCDC is powered off.
   - Even iteration: LEDVDD is regulated at 1.8 V and the current drops to the EM2 plateau (typically a few microamps with DCDC in boost mode).
4. Observe the LEDVDD pin on a scope to see the ramp edges, and to confirm the EM0 / EM2 transitions.

> Note: `SL_DEVICE_INIT_DCDC_ENABLE` is set to `0` in `config/sl_device_init_dcdc_config.h` so the DCDC stays off at boot and LEDVDD starts in input-rail passthrough (~3.2 V).

## Troubleshooting

- **Ramp interrupt never fires:** Confirm the part has DCDC LEDVDD support.
- **LEDVDD stays at 1.8 V:** Verify `sl_hal_emu_dcdc_get_ledvddon()` returns true after init; if it never does, the DCDC bus clock or DCDC enable may not have been applied.
- **Build error on `DCDC_IF_LEDVDDRAMPDONE`:** The selected part does not expose the LEDVDD ramp-done flag; this example targets boost parts that do.

## Resources

- [EMU HAL Documentation](https://docs.silabs.com/gecko-platform/latest/platform-peripheral/emu)
- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)

> Note: Before running the example, make sure the DCDC feature macro in the device header is set to BOOST. Set `_SILICON_LABS_DCDC_FEATURE` to `_SILICON_LABS_DCDC_FEATURE_DCDC_BOOST` in the target device header file, for example [`efr32bg2bb312f1016im48.h`].