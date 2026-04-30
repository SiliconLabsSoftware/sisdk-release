/***************************************************************************//**
 * @file
 * @brief Top level application functions
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 ******************************************************************************/
#include "app.h"
#include "rht_unidriver_app.h"

void app_init(void)
{
  rht_unidriver_app_init();
}

void app_process_action(void)
{
  rht_unidriver_app_process_action();
}
