# Watchdog Kernel FreeRTOS

This example application demonstrates the use of the Software Watchdog Manager in a FreeRTOS environment. The application registers two watchdog handles, each managed by a dedicated FreeRTOS task that feeds its watchdog periodically. On-board buttons allow the user to stop feeding individual watchdog handles, simulating a fault condition that triggers a system reset.

## Application Overview

The application creates **two watchdog handles** (`my_watchdog_0` and `my_watchdog_1`) and **two FreeRTOS tasks** (`wdog_task_1` and `wdog_task_2`) that feed them every 200 ms.

### Startup Sequence

1. **Fault detection** (`app_init_early`): Before any service initialization, the application calls `sl_watchdog_manager_retrieve_faulty()` to check whether the previous reset was caused by an unfed watchdog. If so, the faulty handle is identified and reported on the serial console.
2. **Task creation** (`sample_init`): Two FreeRTOS tasks are created (using static allocation by default). Each task creates its own watchdog handle, enables it, starts the watchdog manager, and issues a force-feed to prevent a premature reset during initialization.

### Runtime Behavior

Each FreeRTOS task runs an infinite loop, feeding its assigned watchdog handle every 200 ms based on the current button state:

- **Both buttons unpressed (default)**: Both `my_watchdog_0` and `my_watchdog_1` are fed normally. The system runs indefinitely.
- **Button 0 pressed**: `my_watchdog_0` stops being fed. After the watchdog timeout period elapses, the watchdog manager detects the unfed handle and resets the system.
- **Button 1 pressed**: `my_watchdog_1` stops being fed, triggering a reset in the same manner.
- **After reset**: On the next boot, the application detects which watchdog handle caused the reset and prints a message (e.g., `[WDOG] Watchdog 0 was fault last time`).

Pressing the same button again re-enables feeding for that handle (toggle behavior).

### Console Output

Status messages are printed to the serial console (VCOM) at each feeding cycle:

```
***************************************************
STARTING WATCHDOG EXAMPLE (FreeRTOS)
--------------------------------------------------------
[WDOG] Watchdog 0 created
[WDOG] Watchdog 1 created
[APP] Watchdog 0 fed
[APP] Watchdog 1 fed
[BTN] Button 0 pressed - Watchdog 0 feeding disabled
[APP][ERROR] Watchdog 0 not fed. Waiting for Button 0 to recover...
...
```

After the system resets due to an unfed watchdog, the next boot will show:

```
***************************************************
STARTING WATCHDOG EXAMPLE (FreeRTOS)
--------------------------------------------------------
[WDOG] Watchdog 0 was fault last time
--------------------------------------------------------
```

## Requirements

- Silicon Labs board with **2 buttons** (btn0, btn1) and Watchdog support.
- Serial console connection (VCOM) for observing output.
