/***************************************************************************//**
 * @file
 * @brief Top level application functions
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
#include "watchdog.h"

/***************************************************************************//**
 * Early app init hook (called before sl_watchdog_manager_init).
 *
 * This overrides the SL_WEAK default in sl_main_init.c. It runs after clock
 * and power manager init but before any service init, which is exactly the
 * window where sl_watchdog_manager_retrieve_faulty() must be called.
 ******************************************************************************/
void app_init_early(void)
{
  watchdog_retrieve_faulty();
}

/***************************************************************************//**
 * Initialize application.
 ******************************************************************************/
void app_init(void)
{
  watchdog_init();
}

/***************************************************************************//**
 * App ticking function.
 ******************************************************************************/
void app_process_action(void)
{
  watchdog_process_action();
}
