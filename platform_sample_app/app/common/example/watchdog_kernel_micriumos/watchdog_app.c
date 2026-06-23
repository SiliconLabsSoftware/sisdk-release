/***************************************************************************//**
 * @file
 * @brief WatchDog examples functions with Micrium OS kernel
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

#include "watchdog_app.h"
#include "sl_simple_button_instances.h"
#include "sl_simple_button_btn0_config.h"
#include "sl_simple_button_btn1_config.h"
#include "sl_core.h"
#include "os.h"
#include "sl_watchdog_manager.h"
#include "sl_watchdog_manager_config.h"
#include "sl_hal_wdog.h"
#include "sl_status.h"
#include "sl_iostream_init_instances.h"
#include "sl_udelay.h"
#include "sl_assert.h"
#include <stdio.h>
#include <stdbool.h>

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

/// Serialize printf to VCOM: Micrium stdio/iostream is not mutex-protected, so
/// concurrent tasks interleave bytes inside one printf (garbled lines). Hold the
/// scheduler lock only around stdout writes — not around delays or OS calls.
#define WDOG_LOG_BEGIN(p_err)   OSSchedLock((p_err))
#define WDOG_LOG_END(p_err)     OSSchedUnlock((p_err))

#ifndef BUTTON_INSTANCE_0
#define BUTTON_INSTANCE_0   sl_button_btn0
#endif

#ifndef BUTTON_INSTANCE_1
#define BUTTON_INSTANCE_1   sl_button_btn1
#endif

#ifndef TOGGLE_DELAY_MS_0
#define TOGGLE_DELAY_MS_0            200
#endif

#ifndef TOGGLE_DELAY_MS_1
#define TOGGLE_DELAY_MS_1            200
#endif

#ifndef WATCHDOG_TASK_STACK_SIZE
#define WATCHDOG_TASK_STACK_SIZE      256u
#endif

/// Lower numeric priority = higher task priority in Micrium OS.
#ifndef WATCHDOG_TASK_PRIO_HIGH
#define WATCHDOG_TASK_PRIO_HIGH       20u
#endif

#ifndef WATCHDOG_TASK_PRIO_LOW
#define WATCHDOG_TASK_PRIO_LOW        21u
#endif

#if defined(WDOG_PRESENT) && (WDOG_COUNT > 1)
  #define WATCHDOG_DEFAULT_PERIPHERAL     WDOG1
#elif defined(WDOG_PRESENT) && (WDOG_COUNT == 1)
  #define WATCHDOG_DEFAULT_PERIPHERAL     WDOG0
#else
  #warning "No WDOG peripheral available"
#endif

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

static sl_watchdog_handle_t my_watchdog_0;
static sl_watchdog_handle_t my_watchdog_1;
static sl_status_t status;

static volatile bool btn_pressed[2] = { true, true };

static bool watchdog_0_faulty = false;
static bool watchdog_1_faulty = false;

static OS_TCB wdog_tcb_1;
static OS_TCB wdog_tcb_2;
static CPU_STK wdog_stk_1[WATCHDOG_TASK_STACK_SIZE];
static CPU_STK wdog_stk_2[WATCHDOG_TASK_STACK_SIZE];

/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   *************************
 ******************************************************************************/

static void wdog_task_1(void *arg);
static void wdog_task_2(void *arg);

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   ****************************
 ******************************************************************************/

/***************************************************************************//**
 * Callback on button change.
 *
 * This function overrides a weak implementation defined in the simple_button
 * module. It is triggered when the user activates one of the buttons.
 *
 * Runs in GPIO interrupt context — do not call printf/iostream here.
 ******************************************************************************/
void sl_button_on_change(const sl_button_t *handle)
{
  if (sl_button_get_state(handle) == SL_SIMPLE_BUTTON_PRESSED) {
    if (&BUTTON_INSTANCE_0 == handle) {
      CORE_DECLARE_IRQ_STATE;
      CORE_ENTER_CRITICAL();
      btn_pressed[0] = !btn_pressed[0];
      CORE_EXIT_CRITICAL();
    } else if (&BUTTON_INSTANCE_1 == handle) {
      CORE_DECLARE_IRQ_STATE;
      CORE_ENTER_CRITICAL();
      btn_pressed[1] = !btn_pressed[1];
      CORE_EXIT_CRITICAL();
    }
  }
}

/***************************************************************************//**
 * Initialize example.
 ******************************************************************************/
void sample_init(void)
{
  RTOS_ERR err;

  WDOG_LOG_BEGIN(&err);
  EFM_ASSERT(RTOS_ERR_CODE_GET(err) == RTOS_ERR_NONE);
  printf("\r\n***************************************************\r\n");
  printf("STARTING WATCHDOG EXAMPLE (Micrium OS)\r\n");
  printf("--------------------------------------------------------\r\n");
  if (watchdog_0_faulty == true) {
    printf("[WDOG] Watchdog 0 was fault last time\r\n");
  }
  if (watchdog_1_faulty == true) {
    printf("[WDOG] Watchdog 1 was fault last time\r\n");
  }
  printf("--------------------------------------------------------\r\n");
  WDOG_LOG_END(&err);
  EFM_ASSERT(RTOS_ERR_CODE_GET(err) == RTOS_ERR_NONE);

  sl_udelay_wait(500000);

  OSTaskCreate(&wdog_tcb_1,
               "wdog task 1",
               wdog_task_1,
               DEF_NULL,
               WATCHDOG_TASK_PRIO_HIGH,
               &wdog_stk_1[0],
               (WATCHDOG_TASK_STACK_SIZE / 10u),
               WATCHDOG_TASK_STACK_SIZE,
               0u,
               0u,
               DEF_NULL,
               (OS_OPT_TASK_STK_CLR),
               &err);
  EFM_ASSERT(RTOS_ERR_CODE_GET(err) == RTOS_ERR_NONE);

  OSTaskCreate(&wdog_tcb_2,
               "wdog task 2",
               wdog_task_2,
               DEF_NULL,
               WATCHDOG_TASK_PRIO_LOW,
               &wdog_stk_2[0],
               (WATCHDOG_TASK_STACK_SIZE / 10u),
               WATCHDOG_TASK_STACK_SIZE,
               0u,
               0u,
               DEF_NULL,
               (OS_OPT_TASK_STK_CLR),
               &err);
  EFM_ASSERT(RTOS_ERR_CODE_GET(err) == RTOS_ERR_NONE);
}

/*******************************************************************************
 * Watchdog 0 feeding task.
 *
 * Pressing BTN0 toggles feeding of Watchdog 0.
 ******************************************************************************/
static void wdog_task_1(void *arg)
{
  static bool prev_btn0_feed = true;
  RTOS_ERR err;

  (void)arg;

  status = sl_watchdog_manager_create(&my_watchdog_0, 0x12345678);
  if (status == SL_STATUS_OK) {
    sl_watchdog_manager_enable(&my_watchdog_0);
    printf("[WDOG] Watchdog 0 created\r\n");
    sl_udelay_wait(50000);
    sl_watchdog_manager_force_feed();
  }

  while (DEF_TRUE) {
    bool cur0 = btn_pressed[0];
    if (cur0 != prev_btn0_feed) {
      prev_btn0_feed = cur0;
      printf("[BTN] Button 0 pressed - Watchdog 0 %s\r\n",
             cur0 ? "feeding enabled" : "feeding disabled");
    }
    if (btn_pressed[0] == true) {
      sl_watchdog_manager_feed(&my_watchdog_0);
      printf("[APP] Watchdog 0 fed\r\n");
      sl_udelay_wait(50000);
    } else {
      printf("[APP][ERROR] Watchdog 0 not fed. Waiting for Button 0 to recover...\r\n");
      sl_udelay_wait(50000);
    }
    OSTimeDlyHMSM(0u, 0u, 0u, (CPU_INT32U)TOGGLE_DELAY_MS_0, OS_OPT_TIME_DLY, &err);
    EFM_ASSERT(RTOS_ERR_CODE_GET(err) == RTOS_ERR_NONE);
  }
}

/*******************************************************************************
 * Watchdog 1 feeding task.
 *
 * Pressing BTN1 toggles feeding of Watchdog 1.
 ******************************************************************************/
static void wdog_task_2(void *arg)
{
  static bool prev_btn1_feed = true;
  RTOS_ERR err;

  (void)arg;

  status = sl_watchdog_manager_create(&my_watchdog_1, 0x12345679);
  if (status == SL_STATUS_OK) {
    sl_watchdog_manager_enable(&my_watchdog_1);
    printf("[WDOG] Watchdog 1 created\r\n");
    sl_udelay_wait(50000);
    sl_watchdog_manager_force_feed();
  }

  while (DEF_TRUE) {
    bool cur1 = btn_pressed[1];
    if (cur1 != prev_btn1_feed) {
      prev_btn1_feed = cur1;
      printf("[BTN] Button 1 pressed - Watchdog 1 %s\r\n",
             cur1 ? "feeding enabled" : "feeding disabled");
    }
    if (btn_pressed[1] == true) {
      sl_watchdog_manager_feed(&my_watchdog_1);
      printf("[APP] Watchdog 1 fed\r\n");
      sl_udelay_wait(50000);
    } else {
      printf("[APP][ERROR] Watchdog 1 not fed. Waiting for Button 1 to recover...\r\n");
      sl_udelay_wait(50000);
    }
    OSTimeDlyHMSM(0u, 0u, 0u, (CPU_INT32U)TOGGLE_DELAY_MS_1, OS_OPT_TIME_DLY, &err);
    EFM_ASSERT(RTOS_ERR_CODE_GET(err) == RTOS_ERR_NONE);
  }
}

/***************************************************************************//**
 * Retrieve faulty watchdog information from the previous reset.
 ******************************************************************************/
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
