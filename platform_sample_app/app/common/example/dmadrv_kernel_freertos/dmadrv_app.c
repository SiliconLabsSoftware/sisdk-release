/***************************************************************************//**
 * @file
 * @brief DMA FreeRTOS application
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

#include <stdio.h>
#include <string.h>
#include "sl_dma_manager.h"
#include "sl_dma_channel.h"
#include "dmadrv_app.h"
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

#ifndef DMADRV_TASK_STACK_SIZE
#define DMADRV_TASK_STACK_SIZE             configMINIMAL_STACK_SIZE
#endif

#ifndef DMADRV_TASK_PRIO
#define DMADRV_TASK_PRIO                   20
#endif

#ifndef EXAMPLE_USE_STATIC_ALLOCATION
#define EXAMPLE_USE_STATIC_ALLOCATION   1
#endif

#define RX_BUFFER_SIZE                     (8)
#define TX_BUFFER_SIZE                     (RX_BUFFER_SIZE + 64)

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

static uint8_t tx_channel, rx_channel;
static sl_dma_channel_handle_t tx_handle, rx_handle;

static char tx_buffer[TX_BUFFER_SIZE + 1];       // Transmit buffer
static char rx_buffer[RX_BUFFER_SIZE + 1];       // Receive buffer
static SemaphoreHandle_t dma_rx_complete;        // Semaphore for DMA completion

/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

static void dmadrv_task(void *pvParameters);
static void rx_callback(sl_dma_channel_handle_t *handle,
                        void *user_data,
                        bool error,
                        bool aborted);
static void transmit_data(const char *message);

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/*******************************************************************************
 * Initialize DMA application.
 ******************************************************************************/
void dmadrv_app_init(void)
{
  // DMA Manager is auto-initialized via SL Main — no manual init call needed.

  // Allocate DMA channels for TX and RX.
  sl_status_t status = sl_dma_manager_allocate_channel(NULL, &tx_channel);
  configASSERT(status == SL_STATUS_OK);

  status = sl_dma_manager_allocate_channel(NULL, &rx_channel);
  configASSERT(status == SL_STATUS_OK);

  // Initialize per-channel driver instances.
  // Signature: sl_dma_channel_init(handle*, peripheral, channel_number, callback, user_data)
  // TX channel: no callback — transfer completion is polled via sl_dma_channel_get_status.
  status = sl_dma_channel_init(&tx_handle, SL_PERIPHERAL_LDMA0, tx_channel, NULL, NULL);
  configASSERT(status == SL_STATUS_OK);

  status = sl_dma_channel_init(&rx_handle, SL_PERIPHERAL_LDMA0, rx_channel, rx_callback, NULL);
  configASSERT(status == SL_STATUS_OK);

  // Set peripheral signals once; not repeated per transfer.
  // Verify exact signal names in sl_dma_signals.h for the target device.
  sl_dma_channel_set_peripheral_signal(&tx_handle, SL_DMA_SIGNAL_EUSART0_TXFL);
  sl_dma_channel_set_peripheral_signal(&rx_handle, SL_DMA_SIGNAL_EUSART0_RXFL);

  // Create semaphore for DMA reception completion.
  dma_rx_complete = xSemaphoreCreateBinary();
  configASSERT(dma_rx_complete != NULL);

  // Start FreeRTOS task for DMA processing.
  BaseType_t task_status = xTaskCreate(dmadrv_task,
                                       "DMA_Task",
                                       DMADRV_TASK_STACK_SIZE,
                                       NULL,
                                       DMADRV_TASK_PRIO,
                                       NULL);
  configASSERT(task_status == pdPASS);
}

/*******************************************************************************
 ***************************  LOCAL FUNCTIONS   ********************************
 ******************************************************************************/

/*******************************************************************************
 * FreeRTOS task for DMA processing.
 ******************************************************************************/
static void dmadrv_task(void *pvParameters)
{
  (void)pvParameters;

  transmit_data("Welcome to the DMA FreeRTOS app\r\nEnter data:\r\n");

  while (1) {
    sl_dma_channel_status_t status;
    sl_dma_channel_get_status(&rx_handle, &status);
    if (!status.active) {
      sl_dma_channel_submit_transfer_p2m(&rx_handle,
                                         (void *)&(EUSART0->RXDATA),
                                         rx_buffer,
                                         RX_BUFFER_SIZE,
                                         SL_DMA_CTRL_SIZE_BYTE,
                                         NULL);
    }

    // Wait for DMA reception to complete.
    if (xSemaphoreTake(dma_rx_complete, portMAX_DELAY) == pdTRUE) {
      char response[TX_BUFFER_SIZE];
      snprintf(response, sizeof(response), "You wrote: %s\r\nEnter data:\r\n", rx_buffer);
      transmit_data(response);
    }

    vTaskDelay(pdMS_TO_TICKS(10));
  }
}

/*******************************************************************************
 * DMA RX callback function.
 ******************************************************************************/
static void rx_callback(sl_dma_channel_handle_t *handle,
                        void *user_data,
                        bool error,
                        bool aborted)
{
  (void)handle;
  (void)user_data;
  if (error || aborted) {
    return;
  }

  BaseType_t task_woken = pdFALSE;
  xSemaphoreGiveFromISR(dma_rx_complete, &task_woken);
  portYIELD_FROM_ISR(task_woken);
}

/*******************************************************************************
 * Transmit data using DMA.
 ******************************************************************************/
static void transmit_data(const char *message)
{
  sl_dma_channel_status_t status;
  sl_dma_channel_get_status(&tx_handle, &status);
  while (status.active) {
    vTaskDelay(pdMS_TO_TICKS(1));
    sl_dma_channel_get_status(&tx_handle, &status);
  }

  strncpy(tx_buffer, message, TX_BUFFER_SIZE);
  tx_buffer[TX_BUFFER_SIZE] = '\0';

  sl_dma_channel_submit_transfer_m2p(&tx_handle,
                                     tx_buffer,
                                     (void *)&(EUSART0->TXDATA),
                                     strlen(tx_buffer),
                                     SL_DMA_CTRL_SIZE_BYTE,
                                     NULL);
}
