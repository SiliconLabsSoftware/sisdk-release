# Blink Kernel FreeRTOS

Blinks an LED using a FreeRTOS task. Illustrates creating the task with either dynamic or static memory for the task stack and TCB.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example blinks an on-board LED using a FreeRTOS task. It shows how to create a task that runs periodically (e.g. every 1000 ms) and toggles the LED. The task can be created with either dynamic or static memory allocation for the task stack and TCB (Task Control Block), which is useful for understanding memory options in FreeRTOS. You can change the blink period, LED instance, and task priority in the source (e.g. `blink.c`).

## Prerequisites / Setup Requirements

**Hardware**

- Silicon Labs kit with at least one on-board LED.

**Software**

- Simplicity Studio 5 (or later).

## Steps to Run Demo

1. Open the project in Simplicity Studio and build it.
2. Connect the kit and flash the application.
3. Run the application. The LED should blink at the configured period (e.g. 1000 ms).
4. Optionally modify `blink.c` to change the period, use static vs dynamic allocation, or adjust task priority, then rebuild and flash.

## Troubleshooting

- **LED does not blink:** Ensure the board has an on-board LED and that the LED instance (e.g. led0) is correct for your board in the project configuration.
- **Build errors:** Ensure the FreeRTOS component and the correct toolchain are selected for your target part.
- **Task not running:** Check that the FreeRTOS kernel is started and the blink task is created; verify stack size if using static allocation.

## Resources

- [FreeRTOS Documentation](https://www.freertos.org/Documentation/RTOS_book.html)
- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)

