/***************************************************************************//**
 * @file
 * @brief WatchDog examples functions with FreeRTOS kernel
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
#include "FreeRTOS.h"
#include "task.h"
#include "sl_watchdog_manager.h"
#include "sl_watchdog_manager_config.h"
#include "sl_hal_wdog.h"
#include "sl_status.h"
#include "sl_iostream_init_instances.h"
#include "sl_udelay.h"
#include <stdio.h>

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

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
#define WATCHDOG_TASK_STACK_SIZE      configMINIMAL_STACK_SIZE
#endif

#ifndef WATCHDOG_TASK_PRIO
#define WATCHDOG_TASK_PRIO            20
#endif

#ifndef EXAMPLE_USE_STATIC_ALLOCATION
#define EXAMPLE_USE_STATIC_ALLOCATION      1
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

TaskHandle_t xHandle_1 = NULL;
TaskHandle_t xHandle_2 = NULL;

/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

static void wdog_task_1(void *arg);
static void wdog_task_2(void *arg);

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Callback on button change.
 *
 * This function overrides a weak implementation defined in the simple_button
 * module. It is triggered when the user activates one of the buttons.
 *
 ******************************************************************************/
void sl_button_on_change(const sl_button_t *handle)
{
  // Runs in GPIO interrupt context — do not call printf/iostream here (FreeRTOS unsafe).
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
  printf("\r\n***************************************************\r\n");
  printf("STARTING WATCHDOG EXAMPLE (FreeRTOS)\r\n");
  printf("--------------------------------------------------------\r\n");
  if (watchdog_0_faulty == true) {
    printf("[WDOG] Watchdog 0 was fault last time\r\n");
  }
  if (watchdog_1_faulty == true) {
    printf("[WDOG] Watchdog 1 was fault last time\r\n");
  }
  printf("--------------------------------------------------------\r\n");

  sl_udelay_wait(100000);

#if (EXAMPLE_USE_STATIC_ALLOCATION == 1)

  static StaticTask_t xTaskBuffer_1;
  static StackType_t  xStack_1[WATCHDOG_TASK_STACK_SIZE];

  static StaticTask_t xTaskBuffer_2;
  static StackType_t  xStack_2[WATCHDOG_TASK_STACK_SIZE];

  xHandle_1 = xTaskCreateStatic(wdog_task_1,
                              "wdog task 1",
                              WATCHDOG_TASK_STACK_SIZE,
                              ( void * ) NULL,
                              tskIDLE_PRIORITY + 2,
                              xStack_1,
                              &xTaskBuffer_1);

  // Since puxStackBuffer and pxTaskBuffer parameters are not NULL,
  // it is impossible for xHandle_1 to be null. This check is for
  // rigorous example demonstration.
  EFM_ASSERT(xHandle_1 != NULL);

  xHandle_2 = xTaskCreateStatic(wdog_task_2,
                              "wdog task 2",
                              WATCHDOG_TASK_STACK_SIZE,
                              ( void * ) NULL,
                              tskIDLE_PRIORITY + 1,
                              xStack_2,
                              &xTaskBuffer_2);

  // Since puxStackBuffer and pxTaskBuffer parameters are not NULL,
  // it is impossible for xHandle_2 to be null. This check is for
  // rigorous example demonstration.
  EFM_ASSERT(xHandle_2 != NULL);

#else

  BaseType_t xReturned = pdFAIL;

  xReturned = xTaskCreate(wdog_task_1,
                          "wdog task 1",
                          WATCHDOG_TASK_STACK_SIZE,
                          ( void * ) NULL,
                          tskIDLE_PRIORITY + 2,
                          &xHandle_1);

  // Unlike task creation using static allocation, dynamic task creation can very likely
  // fail due to lack of memory. Checking the return value is relevant.
  EFM_ASSERT(xReturned == pdPASS);

  xReturned = xTaskCreate(wdog_task_2,
                          "wdog task 2",
                          WATCHDOG_TASK_STACK_SIZE,
                          ( void * ) NULL,
                          tskIDLE_PRIORITY + 1,
                          &xHandle_2);

  EFM_ASSERT(xReturned == pdPASS);

#endif
}

/*******************************************************************************
 * Watchdog 0 feeding task.
 *
 * Pressing BTN0 toggles feeding of Watchdog 0.
 ******************************************************************************/
static void wdog_task_1(void *arg)
{
  static bool prev_btn0_feed = true;

  (void)&arg;

  const TickType_t xDelay = pdMS_TO_TICKS(TOGGLE_DELAY_MS_0);

  status = sl_watchdog_manager_create(&my_watchdog_0, 0x12345678);
  if (status == SL_STATUS_OK) {
    sl_watchdog_manager_enable(&my_watchdog_0);
    printf("[WDOG] Watchdog 0 created\r\n");
    // prevent printf error in task switch
    sl_udelay_wait(50000);
    // Force feed the watchdog to prevent it from triggering during initialization.
    sl_watchdog_manager_force_feed();
  }

  while (1) {
    bool cur0 = btn_pressed[0];
    if (cur0 != prev_btn0_feed) {
      prev_btn0_feed = cur0;
      printf("[BTN] Button 0 pressed - Watchdog 0 %s\r\n",
             cur0 ? "feeding enabled" : "feeding disabled");
    }
    if (btn_pressed[0] == true) {
      sl_watchdog_manager_feed(&my_watchdog_0);
      printf("[APP] Watchdog 0 fed\r\n");
      // prevent printf error in task switch
      sl_udelay_wait(50000);
    } else {
      printf("[APP][ERROR] Watchdog 0 not fed. Waiting for Button 0 to recover...\r\n");
      // prevent printf error in task switch
      sl_udelay_wait(50000);
    }
    vTaskDelay(xDelay);
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

  (void)&arg;

  const TickType_t xDelay = pdMS_TO_TICKS(TOGGLE_DELAY_MS_1);

  status = sl_watchdog_manager_create(&my_watchdog_1, 0x12345679);
  if (status == SL_STATUS_OK) {
    sl_watchdog_manager_enable(&my_watchdog_1);
    printf("[WDOG] Watchdog 1 created\r\n");
    // prevent printf error in task switch
    sl_udelay_wait(50000);
    // Force feed the watchdog to prevent it from triggering during initialization.
    sl_watchdog_manager_force_feed();
  }

  while (1) {
    bool cur1 = btn_pressed[1];
    if (cur1 != prev_btn1_feed) {
      prev_btn1_feed = cur1;
      printf("[BTN] Button 1 pressed - Watchdog 1 %s\r\n",
             cur1 ? "feeding enabled" : "feeding disabled");
    }
    if (btn_pressed[1] == true) {
      sl_watchdog_manager_feed(&my_watchdog_1);
      printf("[APP] Watchdog 1 fed\r\n");
      // prevent printf error in task switch
      sl_udelay_wait(50000);
    } else {
      printf("[APP][ERROR] Watchdog 1 not fed. Waiting for Button 1 to recover...\r\n");
      // prevent printf error in task switch
      sl_udelay_wait(50000);
    }
    vTaskDelay(xDelay);
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
