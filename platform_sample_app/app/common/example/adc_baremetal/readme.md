# ADC Bare-metal

This example project shows how to sample the on-chip SAR ADC in a bare-metal configuration using `sl_hal_adc`, without an RTOS. Configure GPIO loopback and scan entry, enable ADC0, trigger a scan, discard the first result, then read the second result (recommended for successive-approximation behavior). Each sample is also printed on the kit's virtual COM port (VCOM).

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Console Output](#console-output)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

The application configures ADC0 for one immediate conversion on scan channel 0, waits for `SCANENTRYDONE`, and reads the result from the FIFO. A sleeptimer wakes the main loop periodically so each sample can be read and printed.

- Enables GPIO and ADC0 bus clocks and configures pin modes and bus allocation.
- Initializes ADC0 for immediate trigger, single action, one scan entry on channel 0.
- Uses a sleeptimer (default 500 ms) to trigger each sample; each successful sample toggles the board LED so you can verify activity without a debugger.
- Prints the running sample number and the ADC data over VCOM on every conversion.

Board-specific GPIO/ADC pin pairs are selected with the same preprocessor blocks. If the board is not listed, add a block there and in `adc_app.c` to match the schematic.

## Console Output

```text
Welcome to the ADC bare-metal example application
Sampling channel 0 every 500 ms

Sample #1
ADC data = 4095 (0x0FFF)

Sample #2
ADC data = 4095 (0x0FFF)
```

The sample counter is a `uint32_t`. At the default 500 ms sample period it wraps to zero after roughly 68 years of continuous operation; this is defined unsigned wrap-around and only the printed label restarts.

## Prerequisites / Setup Requirements

**Hardware**

- Silicon Labs kit with SAR ADC0 and the GPIO loopback wiring assumed for board definition. On-board LED for visual feedback.

**Software**

- Simplicity Studio 5 (or later). A serial terminal for VCOM output.

## Steps to Run Demo

1. Open the project in Simplicity Studio, select a compatible part, and build.
2. Connect the kit and flash the application.
3. Open a serial terminal on the kit's VCOM port at **115200 8N1** with **hardware flow control (RTS/CTS)**.
4. Run the application. The LED should toggle at the sample period (default 500 ms) and the terminal should print one block per sample (see [Console Output](#console-output)).
5. Adjust `SAMPLE_PERIOD_MS` or `LED_INSTANCE` in `adc_app.c` if needed, then rebuild and flash.

## Troubleshooting

- **Build fails with "Define pin mapping for this board":** Add a board macro branch in `adc_app.c` for the kit.
- **LED does not toggle:** Confirm `ADC_PRESENT` and ADC0 are available on the selected device; check clock and GPIO/ADC wiring for the board.
- **Unexpected conversion values:** Ensure the loopback net matches the selected board defines; noise and routing affect readings.

## Resources

- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Gecko Platform Documentation](https://docs.silabs.com/gecko-platform/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
