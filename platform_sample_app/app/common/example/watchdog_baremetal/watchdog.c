/***************************************************************************//**
 * @file
 * @brief Watchdog examples functions
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/

#include <stdio.h>
#include "sl_code_classification.h"
#include "sl_simple_button_instances.h"
#include "sl_iostream_init_instances.h"
#include "sl_udelay.h"
#include "sl_sleeptimer.h"

#include "sl_watchdog_manager.h"
#include "sl_watchdog_manager_config.h"
#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
#include "sl_power_manager.h"
#endif

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

#ifndef TOGGLE_DELAY_MS
#define TOGGLE_DELAY_MS         1000
#endif

#ifndef BUTTON_INSTANCE_0
#define BUTTON_INSTANCE_0   sl_button_btn0
#endif

#ifndef BUTTON_INSTANCE_1
#define BUTTON_INSTANCE_1   sl_button_btn1
#endif

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

sl_sleeptimer_timer_handle_t timer;
volatile bool toggle_timeout = false;

sl_watchdog_handle_t my_watchdog_0;
sl_watchdog_handle_t my_watchdog_1;
sl_status_t status;

static volatile bool btn_pressed[2] = {true, true};

static  bool watchdog_0_faulty = false;
static  bool watchdog_1_faulty = false;
/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

 SL_CODE_RAM static void on_timeout(sl_sleeptimer_timer_handle_t *handle,
                                    void *data);

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

 #if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
 /***************************************************************************//**
  * Allow sleep; log EM run configuration once (see sl_watchdog_manager_config.h).
  *
  * EMx_RUN selects whether the hardware WDOG counter runs in EM1/EM2/EM3. When
  * zero for a given mode, the counter does not run there; on parts without the
  * corresponding EMxRUN capability, the manager may disable WDOG around sleep.
  *
  ******************************************************************************/
 bool app_is_ok_to_sleep(void)
 {
   printf("[PM] Allow sleep\r\n");
   return true;
 }
 #endif

/***************************************************************************//**
 * Callback on button change.
 *
 * This function overrides a weak implementation defined in the simple_button
 * module. It is triggered when the user activates one of the buttons.
 *
 ******************************************************************************/

void sl_button_on_change(const sl_button_t *handle)
{
  // Called from GPIO interrupt context — avoid printf here; log from watchdog_process_action.
  if (sl_button_get_state(handle) == SL_SIMPLE_BUTTON_PRESSED) {
    if (&BUTTON_INSTANCE_0 == handle) {
      btn_pressed[0] = !btn_pressed[0];
    } else if (&BUTTON_INSTANCE_1 == handle) {
      btn_pressed[1] = !btn_pressed[1];
    }
  }
}

/***************************************************************************//**
 * Initialize blink example.
 ******************************************************************************/
void watchdog_init(void)
{
  printf("\r\n***************************************************\r\n");
  printf("STARTING WATCHDOG EXAMPLE\r\n");
  printf("--------------------------------------------------------\r\n");
  #if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
  printf("[PM] WDOG EM run (config): EM1=%u EM2=%u EM3=%u - "
    "1=runs in that EM, 0=stopped; without HW EMxRUN, manager may disable WDOG for sleep.\r\n",
    (unsigned int)SL_WATCHDOG_MANAGER_EM1_RUN,
    (unsigned int)SL_WATCHDOG_MANAGER_EM2_RUN,
    (unsigned int)SL_WATCHDOG_MANAGER_EM3_RUN);
  #endif
  if (watchdog_0_faulty == true) {
    printf("[WDOG] Watchdog 0 was fault last time\r\n");
  }
  if (watchdog_1_faulty == true) {
    printf("[WDOG] Watchdog 1 was fault last time\r\n");
  }
  sl_udelay_wait(50000);
  printf("--------------------------------------------------------\r\n");

  // Create a watchdog with unique ID
  status = sl_watchdog_manager_create(&my_watchdog_0, 0x12345678);
  if (status == SL_STATUS_OK) {
    // Watchdog created successfully
    sl_watchdog_manager_enable(&my_watchdog_0);
    printf("[WDOG] Watchdog 0 created\r\n");
  }

  status = sl_watchdog_manager_create(&my_watchdog_1, 0x12345679);
  if (status == SL_STATUS_OK) {
    // Watchdog created successfully
    sl_watchdog_manager_enable(&my_watchdog_1);
    printf("[WDOG] Watchdog 1 created\r\n");
  }

  // Force feed the watchdog to prevent the system from resetting in initialization phase.
  sl_watchdog_manager_force_feed();

  // Create timer for waking up the system periodically.
  sl_sleeptimer_start_periodic_timer_ms(&timer,
                                        TOGGLE_DELAY_MS,
                                        on_timeout, NULL,
                                        0,
                                        SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);
  printf("[TIMER] Timer created\r\n");

}

/***************************************************************************//**
 * Watchdog feed function.
 ******************************************************************************/
void watchdog_process_action(void)
{
  static bool prev_btn0_feed = true;
  static bool prev_btn1_feed = true;

  if (toggle_timeout == true) {
    bool cur0 = btn_pressed[0];
    if (cur0 != prev_btn0_feed) {
      prev_btn0_feed = cur0;
      printf("[BTN] Button 0 pressed - Watchdog 0 %s\r\n",
             cur0 ? "feeding enabled" : "feeding disabled");
    }
    bool cur1 = btn_pressed[1];
    if (cur1 != prev_btn1_feed) {
      prev_btn1_feed = cur1;
      printf("[BTN] Button 1 pressed - Watchdog 1 %s\r\n",
             cur1 ? "feeding enabled" : "feeding disabled");
    }

    if (btn_pressed[0] == true) {
      sl_watchdog_manager_feed(&my_watchdog_0);
      printf("[APP] Watchdog 0 fed\r\n");
    } else {
      // Do nothing
      printf("[APP][ERROR]  Watchdog 0 not fed. Waiting for Button 0 to recover...\r\n");
      while (btn_pressed[0] == false) {
        // Wait for button 0 to be pressed
        sl_udelay_wait(100000);
      }
    }
    if (btn_pressed[1] == true) {
      sl_watchdog_manager_feed(&my_watchdog_1);
      printf("[APP] Watchdog 1 fed\r\n");
    } else {
      // Do nothing
      printf("[APP][ERROR] Watchdog 1 not fed. Waiting for Button 1 to recover...\r\n");
      while (btn_pressed[1] == false) {
        // Wait for button 1 to be pressed
        sl_udelay_wait(100000);
      }
    }
    toggle_timeout = false;
  }
}

/***************************************************************************//**
 * Sleeptimer timeout callback.
 ******************************************************************************/
 static void on_timeout(sl_sleeptimer_timer_handle_t *handle,
                        void *data)
{
  (void)&handle;
  (void)&data;
  toggle_timeout = true;
}

void watchdog_retrieve_faulty(void)
{
  sl_watchdog_handle_t faulty_handle;
  sl_watchdog_manager_retrieve_faulty(&faulty_handle);
  if (faulty_handle == 1) {
    watchdog_0_faulty = true;
  } else if (faulty_handle == 2) {
    watchdog_1_faulty = true;
  }
}
