/***************************************************************************//**
 * @file sl_wisun_event_task.c
 * @brief Wi-SUN event task implementation
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

#include "sl_common.h"
#include "sl_wisun_event_task.h"
#include "sl_wisun_api.h"
#include "sl_event_system.h"
#include "sl_status.h"
#include "sl_assert.h"
#include "cmsis_os2.h"

#define SL_WISUN_EVENT_TASK_PRIORITY osPriorityAboveNormal // Lower priority than EVENT_LOOP_TASK
#define SL_WISUN_EVENT_TASK_SIZE 250 // in units of CPU_INT32U
#define SL_WISUN_EVENT_QUEUE_SIZE 16

static void sl_wisun_event_task_worker(void *argument)
{
  sl_status_t status;
  sl_event_queue_t queue;
  uint8_t event_prio = 0;
  sl_event_t *event;
  (void)argument;

  status = sl_event_queue_create(SL_WISUN_EVENT_QUEUE_SIZE, &queue);
  if (status != SL_STATUS_OK) {
    EFM_ASSERT(false);
    return;
  }

  status = sl_event_subscribe(SL_EVENT_CLASS_WISUN, SL_WISUN_EVENT_IND_MASK, queue);
  if (status != SL_STATUS_OK) {
    EFM_ASSERT(false);
    return;
  }

  while (1) {
    status = sl_event_queue_get(queue,
                                &event_prio,
                                osWaitForever,
                                &event);
    EFM_ASSERT(status == SL_STATUS_OK);
    sl_wisun_on_event((sl_wisun_evt_t *)event->event_data);
    sl_event_process(&event);
  }
}

void sl_wisun_event_task_init(void)
{
  osThreadId_t event_task_id;

  const osThreadAttr_t event_task_attribute = {
    .name = "ws_evt",
    .attr_bits = osThreadDetached,
    .stack_size = (SL_WISUN_EVENT_TASK_SIZE * sizeof(void *)) & 0xFFFFFFF8u,
    .priority = SL_WISUN_EVENT_TASK_PRIORITY
  };

  event_task_id = osThreadNew(sl_wisun_event_task_worker, NULL, &event_task_attribute);
  EFM_ASSERT(event_task_id != NULL);
}

