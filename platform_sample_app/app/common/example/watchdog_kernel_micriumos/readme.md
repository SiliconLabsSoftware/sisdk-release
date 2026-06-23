# Watchdog Kernel Micrium OS

This example application demonstrates the use of the Software Watchdog Manager with **Micrium OS**. It mirrors the [Watchdog Kernel FreeRTOS](../watchdog_kernel_freertos/readme.md) behavior: two software watchdog handles, two periodic tasks, and two buttons to stop feeding each handle and trigger a reset.

## Micrium OS integration

- The Watchdog Manager registers **`OSIdleEnterHook`** and (when **`OS_CFG_APP_HOOKS_EN`** is `1` in `os_cfg.h`) **`OS_AppTaskSwHookPtr`** for platform feeding — see `platform/service/watchdog_manager` README.
- For task-switch feeding, enable **Application hooks** in the Micrium configuration (`os_cfg.h` / Project Configurator) so `sl_watchdog_manager_start()` can assign the task switch hook.

## Application overview

The application creates **two watchdog handles** (`my_watchdog_0` and `my_watchdog_1`) and **two Micrium OS tasks** (`wdog_task_1` and `wdog_task_2`) that feed them every **200 ms** using `OSTimeDlyHMSM()`.

### Startup sequence

1. **Fault detection** (`app_init_early`): Calls `sl_watchdog_manager_retrieve_faulty()` before service init to detect a prior watchdog reset.
2. **Task creation** (`sample_init`): Creates two tasks with `OSTaskCreate()`. Each task creates its watchdog handle, enables it, and calls `sl_watchdog_manager_force_feed()` after creation.

### Runtime behavior

Same as the FreeRTOS example:

- **Both buttons unpressed (default)**: Both watchdogs are fed; the system runs indefinitely.
- **Button 0 pressed**: Stops feeding watchdog 0 → reset after timeout.
- **Button 1 pressed**: Stops feeding watchdog 1 → reset after timeout.
- **After reset**: Boot prints which handle faulted (e.g. `[WDOG] Watchdog 0 was fault last time`).

### Console output

Status messages on VCOM match the FreeRTOS example, with the banner:

`STARTING WATCHDOG EXAMPLE (Micrium OS)`

**Serial output and multiple tasks:** `printf` is not automatically serialized across Micrium tasks. Without protection, two tasks writing at once interleave bytes on the UART (random `*` / `R` / `j` characters). This example wraps stdout `printf` sequences with `OSSchedLock()` / `OSSchedUnlock()` so each line completes atomically. Do not call `printf` from ISRs while a task holds the scheduler lock for long periods.

## Requirements

- Silicon Labs board with **2 buttons** (btn0, btn1) and Watchdog support.
- Serial console (VCOM) for output.
