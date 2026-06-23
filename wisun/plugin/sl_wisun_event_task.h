/***************************************************************************//**
 * @file sl_wisun_event_task.h
 * @brief Wi-SUN event task API
 *******************************************************************************
 * # License
 * <b>Copyright 2025 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef SL_WISUN_EVENT_TASK_H
#define SL_WISUN_EVENT_TASK_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize the Wi-SUN event subscription task
 *
 * This function creates a task that subscribes to Wi-SUN events using
 * the event system and delivers them to sl_wisun_on_event() callback.
 */
void sl_wisun_event_task_init(void);

#ifdef __cplusplus
}
#endif

#endif // SL_WISUN_EVENT_TASK_H

