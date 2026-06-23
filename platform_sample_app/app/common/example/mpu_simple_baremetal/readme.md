# MPU Simple Bare-metal

Shows how the Memory Protection Unit (MPU) blocks code execution from RAM to prevent code injection attacks. Demonstrates enable/disable behavior.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example demonstrates the Simple MPU module. The MPU is used to block execution of code from RAM, which helps prevent code injection attacks. The application shows the difference in behavior when the MPU is disabled versus enabled: it copies sample code to RAM and attempts to run it; with the MPU enabled, execution from RAM is blocked. This illustrates how the MPU can protect the system from malicious or unintended code execution from RAM.

## Prerequisites / Setup Requirements

**Hardware**
- Silicon Labs kit with MPU support (e.g. EFR32, EFM32 with MPU).
- USB cable for serial output (if the example prints status over VCOM).

**Software**
- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and flash the application.
3. Run the application. Observe the behavior: with MPU disabled, the code in RAM may execute; with MPU enabled, execution from RAM is blocked and a fault or protection response occurs as designed.
4. If the example prints to VCOM, open a terminal to see status messages.

## Troubleshooting

- **Unexpected fault or reset:** This may be expected when the MPU is enabled and code in RAM tries to execute. The example is designed to show this behavior.
- **No output:** If the demo uses VCOM for status, ensure the terminal is connected to the correct port and baud rate.
- **Board not supported:** Ensure your part has an MPU; check the project's part compatibility.

## Resources

- [MPUs with an RTOS](https://www.silabs.com/documents/public/white-papers/mpu_with_rtos.pdf)
- [How MPUs Can Help You Make Products Safer and More Secure](https://www.silabs.com/whitepapers/how-mpus-can-help-you-make-products-safer-and-more-secure)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
