# Watchdog Bare Metal

This example application demonstrates the use of the Software Watchdog Manager in a bare metal environment. The application registers two watchdog handles and feeds them periodically using a sleeptimer. On-board buttons allow the user to stop feeding individual watchdog handles, simulating a fault condition that triggers a system reset.

## Application Overview

The application creates **two watchdog handles** (`my_watchdog_0` and `my_watchdog_1`) and a **periodic sleeptimer** (default **1000 ms**, `TOGGLE_DELAY_MS` in `watchdog.c`) to drive feeding.

### Startup Sequence

1. **Fault detection** (`app_init_early`): Before watchdog manager initialization, the application calls `watchdog_retrieve_faulty()`, which uses `sl_watchdog_manager_retrieve_faulty()` to see whether the previous reset was caused by an unfed watchdog. If so, the faulty handle is recorded and reported on the serial console during `watchdog_init`.
2. **Watchdog manager init** (in `sl_main`, before `app_init`): The **Watchdog Manager** service initializes the hardware watchdog from `config/sl_watchdog_manager_config.h` (including EM1/EM2/EM3 run and related options where the peripheral supports them).
3. **Watchdog creation** (`watchdog_init`): When the **power manager** component is present (`SL_CATALOG_POWER_MANAGER_PRESENT`), the app prints a one-line summary of **`SL_WATCHDOG_MANAGER_EM1_RUN` / `EM2_RUN` / `EM3_RUN`** (whether the hardware WDOG is configured to run in EM1/EM2/EM3). Then any **previous-fault** messages print, followed by creation of two software watchdog handles, enable, force-feed, and starting the periodic sleeptimer.

### Energy Mode Handling

Sleep behavior depends on the **device**, **Watchdog Manager** configuration (`config/sl_watchdog_manager_config.h`), and whether the hardware exposes **EMxRUN** bits. The manager may coordinate with the power manager (for example, disabling the hardware watchdog around sleep when required).

When the power manager is included, this example implements **`app_is_ok_to_sleep()`** and returns **`true`** so the device is allowed to sleep. Each time the power manager calls this hook, the example prints **`[PM] Allow sleep`** on the serial console (this can appear often while the system is idle).

### Runtime Behavior

On each sleeptimer period, the application feeds the watchdog handles based on the current button state:

- **Default (both “feed” paths active)**: Both `my_watchdog_0` and `my_watchdog_1` are fed. The system runs indefinitely.
- **Button 0 toggled off**: `my_watchdog_0` stops being fed. After the watchdog timeout, the manager resets the system.
- **Button 1 toggled off**: `my_watchdog_1` stops being fed, with the same result.
- **After reset**: On the next boot, the application reports which handle faulted (e.g. `[WDOG] Watchdog 0 was fault last time`).

Pressing the same button again toggles feeding back on for that handle. Button toggle messages are printed from **`watchdog_process_action()`** (not from the interrupt) so they appear on the **next sleeptimer period** after a press, with text **`feeding enabled`** or **`feeding disabled`** matching `btn_pressed[]`.

### Console Output

Typical serial output (VCOM) follows the `printf` strings in `watchdog.c`. With **power manager** enabled, startup looks like:

```
***************************************************
STARTING WATCHDOG EXAMPLE
--------------------------------------------------------
[PM] WDOG EM run (config): EM1=0 EM2=0 EM3=0 - 1=runs in that EM, 0=stopped; without HW EMxRUN, manager may disable WDOG for sleep.
--------------------------------------------------------
[WDOG] Watchdog 0 created
[WDOG] Watchdog 1 created
[TIMER] Timer created
[APP] Watchdog 0 fed
[APP] Watchdog 1 fed
...
```

The **`EM1` / `EM2` / `EM3`** values match `sl_watchdog_manager_config.h`. While running, you may see many lines of **`[PM] Allow sleep`** from `app_is_ok_to_sleep()`.

Example when a button stops feeding:

```
[BTN] Button 0 pressed - Watchdog 0 feeding disabled
[APP][ERROR]  Watchdog 0 not fed. Waiting for Button 0 to recover...
...
```

After the system resets due to an unfed watchdog, the next boot may show:

```
***************************************************
STARTING WATCHDOG EXAMPLE
--------------------------------------------------------
[PM] WDOG EM run (config): EM1=0 EM2=0 EM3=0 - ...
[WDOG] Watchdog 0 was fault last time
--------------------------------------------------------
```

(If power manager is not in the project, the `[PM]` lines are omitted.)

## Requirements

- Silicon Labs board with **2 buttons** (btn0, btn1) and Watchdog support.
- Serial console connection (VCOM) for observing output.
