/***************************************************************************//**
 * @file
 * @brief DMA examples functions
 *******************************************************************************
 * # License
 * <b>Copyright 2020 Silicon Laboratories Inc. www.silabs.com</b>
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
#include <stdarg.h>
#include "sl_sleeptimer.h"
#include "em_device.h"
#include "sl_dma_manager.h"
#include "sl_dma_channel.h"
#include "sl_assert.h"

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

// Max length of one DMA transfer is defined by the DMA channel driver.
#define RX_BUFFER_SIZE (8)
//
#define TX_BUFFER_SIZE (RX_BUFFER_SIZE + 64)

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

static uint8_t tx_channel, rx_channel;
static sl_dma_channel_handle_t tx_handle, rx_handle;

// Transfer and reception buffers
static char tx_buffer[TX_BUFFER_SIZE + 1]; // An extra character for the NULL character
static char rx_buffer[RX_BUFFER_SIZE + 1]; // An extra character for the NULL character

// Flag indicating that the DMA data transfer is completed on reception channel
static volatile bool rx_transfer_complete;

/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

static void rx_callback(sl_dma_channel_handle_t *handle,
                        void *user_data,
                        bool error,
                        bool aborted);
static void transmit_data(void);

/*******************************************************************************
 ***************************  LOCAL FUNCTIONS   ********************************
 ******************************************************************************/

// Callback triggered when DMA transfer on reception channel is complete.
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
  rx_transfer_complete = true;
}

// Function to transfer transmission buffer to USART via DMA.
static void transmit_data(void)
{
  sl_dma_channel_status_t status;

  sl_dma_channel_get_status(&tx_handle, &status);

  // Wait for any active transfers to finish.
  while (status.active) {
    sl_sleeptimer_delay_millisecond(1);
    sl_dma_channel_get_status(&tx_handle, &status);
  }

  // Transfer data from tx buffer to USART peripheral.
  sl_dma_channel_submit_transfer_m2p(&tx_handle,
                                     tx_buffer,
                                     (void *)&(USART0->TXDATA),
                                     strlen(tx_buffer),
                                     SL_DMA_CTRL_SIZE_BYTE,
                                     NULL);
}

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize example.
 ******************************************************************************/
void dmadrv_app_init(void)
{
  // DMA Manager is auto-initialized via SL Main — no manual init call needed.
  sl_status_t status;

  // Allocate channels for transmission and reception.
  status = sl_dma_manager_allocate_channel(NULL, &tx_channel);
  EFM_ASSERT(status == SL_STATUS_OK);
  status = sl_dma_manager_allocate_channel(NULL, &rx_channel);
  EFM_ASSERT(status == SL_STATUS_OK);

  // Initialize per-channel driver instances.
  // Signature: sl_dma_channel_init(handle*, peripheral, channel_number, callback, user_data)
  // TX channel: no callback — transfer completion is polled via sl_dma_channel_get_status.
  status = sl_dma_channel_init(&tx_handle, SL_PERIPHERAL_LDMA0, tx_channel, NULL, NULL);
  EFM_ASSERT(status == SL_STATUS_OK);
  status = sl_dma_channel_init(&rx_handle, SL_PERIPHERAL_LDMA0, rx_channel, rx_callback, NULL);
  EFM_ASSERT(status == SL_STATUS_OK);

  // Set peripheral signals once; these do not change between transfers.
  // Verify exact signal names against sl_dma_signals.h for the target device.
  sl_dma_channel_set_peripheral_signal(&tx_handle, SL_DMA_SIGNAL_USART0_TXBL);
  sl_dma_channel_set_peripheral_signal(&rx_handle, SL_DMA_SIGNAL_USART0_RXDATAV);

  // Initialise transfer complete flag.
  rx_transfer_complete = false;

  snprintf(tx_buffer, sizeof(tx_buffer), "Welcome to the DMA sample application\r\nEnter data\r\n");
  transmit_data();
}

/***************************************************************************//**
 * Ticking function.
 ******************************************************************************/
void dmadrv_app_process_action(void)
{
  sl_dma_channel_status_t status;

  if (rx_transfer_complete) {
    rx_transfer_complete = false;
    snprintf(tx_buffer, sizeof(tx_buffer), "You wrote: %s\r\nEnter data\r\n", rx_buffer);
    transmit_data();
  }

  sl_dma_channel_get_status(&rx_handle, &status);

  if (!status.active) {
    // Start data transfer from USART peripheral to rx buffer.
    sl_dma_channel_submit_transfer_p2m(&rx_handle,
                                       (void *)&(USART0->RXDATA),
                                       rx_buffer,
                                       RX_BUFFER_SIZE,
                                       SL_DMA_CTRL_SIZE_BYTE,
                                       NULL);
  }
}
