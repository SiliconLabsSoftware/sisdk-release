/***************************************************************************//**
 * @file
 * @brief Bluetooth NCP Transport Layer over IO Stream source
 *******************************************************************************
 * # License
 * <b>Copyright 2025 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 * The licensor of this software is Silicon Laboratories Inc.
 *
 * This software is provided 'as-is', without any express or implied
 * warranty. In no event will the authors be held liable for any damages
 * arising from the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "sl_status.h"
#include "sl_common.h"
#include "sl_core.h"
#include "sl_bt_ncp_transport.h"
#include "sli_bt_ncp_transport.h"
#include "sl_bt_ncp_transport_iostream_config.h"
#include "app_rta.h"
#include "sl_iostream.h"
#include "sli_iostream.h"
#include "sli_iostream_uart.h"
#include "sl_iostream_handles.h"
#include "sl_component_catalog.h"
#ifdef SL_CATALOG_APP_ASSERT_PRESENT
#include "app_assert.h"
#endif // SL_CATALOG_APP_ASSERT_PRESENT

// -----------------------------------------------------------------------------
// Definitions

// TX transfer state
typedef enum {
  TRANSPORT_TX_IDLE = 0, //< Nothing handed over to the stream
  TRANSPORT_TX_ONGOING,  //< Transfer in flight
  TRANSPORT_TX_FINISHED  //< Result available, not reported yet
} transport_tx_state_t;

// How RX learns about incoming data
typedef enum {
  TRANSPORT_RX_POLLED = 0, //< The step function has to poll the stream
  TRANSPORT_RX_NOTIFIED    //< The stream signals new data
} transport_rx_mode_t;

// Internal state type for transport
typedef struct {
  uint8_t rx_buf[SL_BT_NCP_TRANSPORT_CONFIG_RX_BUF_SIZE];
  uint8_t tx_buf[SL_BT_NCP_TRANSPORT_CONFIG_TX_BUF_SIZE];
  app_rta_context_t ctx_tx;          //< Runtime context for TX
  app_rta_context_t ctx_rx;          //< Runtime context for RX
  sl_iostream_t     *stream;         //< IO Stream instance
  bool              receive_enabled; //< Enabled state of the reception
  size_t            tx_count;        //< The amount of data in the TX buffer
  volatile transport_tx_state_t tx_state;  //< State of the ongoing transfer
  volatile sl_status_t          tx_status; //< Result of the last transfer
  transport_rx_mode_t           rx_mode;   //< New data notification mode
  struct sli_iostream_write_async_op write_async_op; // IO Stream async operator
} transport_t;

// -----------------------------------------------------------------------------
// Forward declaration of private functions

// Error callback
static void on_runtime_error(app_rta_error_t error, sl_status_t result);
// RX step function
static void tx_step(void);
// TX step function
static void rx_step(void);
// iostream on transmit callback wrapper
static void on_iostream_transmit(sli_iostream_write_async_op_t *op,
                                 sl_status_t status,
                                 void *arg);
// iostream new data callback wrapper
static void on_iostream_new_data(void *arg);

// -----------------------------------------------------------------------------
// Private variables

// Internal state
static transport_t transport;

// -----------------------------------------------------------------------------
// Public functions (API implementation)

void sl_bt_ncp_transport_transmit(uint32_t len, const uint8_t *data)
{
  sl_status_t sc;
  sc = app_rta_acquire(transport.ctx_tx);
  if (sc != SL_STATUS_OK) {
    sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
    return;
  }
  if (transport.tx_count + len > SL_BT_NCP_TRANSPORT_CONFIG_TX_BUF_SIZE) {
    sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_TX_OVERFLOW,
                                 SL_STATUS_WOULD_OVERFLOW);
  } else {
    // Copy data
    memcpy(&transport.tx_buf[transport.tx_count], data, len);
    // Increase TX byte count
    transport.tx_count += len;
    // Proceed
    sc = app_rta_proceed(transport.ctx_tx);
    if (sc != SL_STATUS_OK) {
      sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
    }
  }
  sc = app_rta_release(transport.ctx_tx);
  if (sc != SL_STATUS_OK) {
    sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
  }
}

void sl_bt_ncp_transport_receive(void)
{
  sl_status_t sc;
  sc = app_rta_acquire(transport.ctx_rx);
  if (sc != SL_STATUS_OK) {
    sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
    return;
  }
  if (!transport.receive_enabled) {
    // Enable reception
    transport.receive_enabled = true;
    sc = app_rta_proceed(transport.ctx_rx);
    if (sc != SL_STATUS_OK) {
      sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
    }
  }
  sc = app_rta_release(transport.ctx_rx);
  if (sc != SL_STATUS_OK) {
    sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
  }
}

// -----------------------------------------------------------------------------
// Internal API implementation

void sli_bt_ncp_transport_init(void)
{
  sl_status_t sc;

  memset(&transport, 0, sizeof(transport));

  // Create context for TX
  app_rta_config_t config = {
    .requirement.runtime          = true,
    .requirement.runtime_separate = false,
    .requirement.guard            = true,
    .requirement.signal           = false,
    .requirement.queue            = false,
    .step                         = tx_step,
    .priority                     = SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_TX_TASK_PRIO,
    .stack_size                   = SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_TX_TASK_STACK,
    .error                        = on_runtime_error,
    .wait_for_guard               = SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_TX_WAIT_FOR_GUARD,
  };
  #if defined(SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_SEPARATE_TX) && SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_SEPARATE_TX == 1
  config.requirement.runtime_separate = true;
  #endif // defined(SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_SEPARATE_TX) && SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_SEPARATE_TX == 1
  sc = app_rta_create_context(&config, &transport.ctx_tx);
  if (sc != SL_STATUS_OK) {
    sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
  }

  // Create context for RX
  app_rta_config_t config_rx = {
    .requirement.runtime          = true,
    .requirement.runtime_separate = true, // RX can block in case of RTOS.
    .requirement.guard            = true,
    .requirement.signal           = false,
    .requirement.queue            = false,
    .step                         = rx_step,
    .priority                     = SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_RX_TASK_PRIO,
    .stack_size                   = SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_RX_TASK_STACK,
    .error                        = on_runtime_error,
    .wait_for_guard               = SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_RX_WAIT_FOR_GUARD,
  };
  sc = app_rta_create_context(&config_rx, &transport.ctx_rx);
  if (sc != SL_STATUS_OK) {
    sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
  }
}

void sli_bt_ncp_transport_rta_ready(void)
{
  char *name = SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_STREAM_INSTANCE;
  sl_iostream_type_t type = SL_BT_NCP_TRANSPORT_IOSTREAM_CONFIG_STREAM_TYPE;

  sl_iostream_t *iostream = NULL;
  sl_iostream_t *iostream_type = NULL;

  for (uint32_t i = 0; i < sl_iostream_instances_count; i++) {
    if (sl_iostream_instances_info[i]->type == type) {
      if (strcmp(sl_iostream_instances_info[i]->name, name) == 0) {
        iostream = sl_iostream_instances_info[i]->handle;
        break;
      }
      if (iostream_type == NULL) {
        iostream_type = sl_iostream_instances_info[i]->handle;
      }
    }
  }

  if (iostream == NULL) {
    // The stream is not found by name
    if (iostream_type != NULL) {
      // Stream found by type
      iostream = iostream_type;
    } else {
      // Not found stream, set to default. Its type is unknown here.
      iostream = sl_iostream_get_default();
      type = SL_IOSTREAM_TYPE_UNDEFINED;
    }
  }

  transport.stream = iostream;

  // Subscribe for new data notification if the stream is able to provide it,
  // otherwise the stream has to be polled.
  if (type == SL_IOSTREAM_TYPE_UART) {
    sl_status_t sc;
    sc = sli_iostream_uart_subscribe_to_new_data((sl_iostream_uart_t *)iostream,
                                                 on_iostream_new_data,
                                                 &transport);
    if (sc == SL_STATUS_OK) {
      transport.rx_mode = TRANSPORT_RX_NOTIFIED;
    }
  }
}

// Step function (to be called externally)
void sli_bt_ncp_transport_step(void)
{
  rx_step();
  tx_step();
}

// Step function for TX
static void tx_step(void)
{
  sl_status_t sc;
  transport_tx_state_t state;

  sc = app_rta_acquire(transport.ctx_tx);

  if (sc != SL_STATUS_OK) {
    sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
    (void)app_rta_proceed(transport.ctx_tx);
    return;
  }

  // Start a new transfer only when the previous one has finished.
  if ((transport.tx_state == TRANSPORT_TX_IDLE) && (transport.tx_count > 0)) {
    // Try sync write first (especially on streams that don't support async)
    // since there's no other way to determine iostream UART mode.
    sc = sl_iostream_write(transport.stream,
                           transport.tx_buf,
                           transport.tx_count);
    if (sc == SL_STATUS_NOT_AVAILABLE) { // Feature not available due to software configuration.
      // Try async as fallback on supported UART streams. The callback may
      // preempt this context, so mark the transfer before submitting it.
      transport.tx_state = TRANSPORT_TX_ONGOING;
      sc = sli_iostream_init_async_write_op(&transport.write_async_op,
                                            transport.tx_buf,
                                            transport.tx_count,
                                            on_iostream_transmit,
                                            &transport);
      if (sc == SL_STATUS_OK) {
        sc = sli_iostream_async_write(transport.stream,
                                      &transport.write_async_op);
      }
      if (sc != SL_STATUS_OK) {
        // Nothing reached the stream, no callback will arrive.
        on_iostream_transmit(NULL, sc, &transport);
      }
    } else {
      on_iostream_transmit(NULL, sc, &transport);
    }
  }

  // Collect the result, which may come from interrupt context.
  state = transport.tx_state;
  if (state == TRANSPORT_TX_FINISHED) {
    sc                 = transport.tx_status;
    transport.tx_count = 0;
    transport.tx_state = TRANSPORT_TX_IDLE;
  }

  (void)app_rta_release(transport.ctx_tx);

  // Notify the upper layer outside of the guard and the interrupt context.
  if (state == TRANSPORT_TX_FINISHED) {
    sl_bt_ncp_transport_on_transmit(sc);
  }
}

static void on_iostream_transmit(sli_iostream_write_async_op_t *op,
                                 sl_status_t status,
                                 void *arg)
{
  transport_t *tr = (transport_t *)arg;
  (void)op;
  tr->tx_status = status;
  tr->tx_state  = TRANSPORT_TX_FINISHED;
  (void)app_rta_proceed(tr->ctx_tx);
}

// Called from interrupt context when data arrives on an empty stream buffer.
static void on_iostream_new_data(void *arg)
{
  (void)app_rta_proceed(((transport_t *)arg)->ctx_rx);
}
// Step function for RX
static void rx_step(void)
{
  sl_status_t sc;
  size_t bytes_read = 0;

  sc = app_rta_acquire(transport.ctx_rx);

  if (sc != SL_STATUS_OK) {
    sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, sc);
    (void)app_rta_proceed(transport.ctx_rx);
    return;
  }

  if (transport.receive_enabled) {
    sc = sl_iostream_read(transport.stream,
                          transport.rx_buf,
                          sizeof(transport.rx_buf),
                          &bytes_read);
    (void)app_rta_release(transport.ctx_rx);
    if (sc == SL_STATUS_OK) {
      if (bytes_read > 0) {
        sl_bt_ncp_transport_on_receive(SL_STATUS_OK,
                                       bytes_read,
                                       transport.rx_buf);
      }
    } else if (sc == SL_STATUS_EMPTY) {
      // Empty, do nothing
    } else {
      sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RX, sc);
    }
    // Keep going while data flows. Stream that cannot notify must be polled.
    if ((bytes_read > 0) || (transport.rx_mode == TRANSPORT_RX_POLLED)) {
      (void)app_rta_proceed(transport.ctx_rx);
    }
  } else {
    (void)app_rta_release(transport.ctx_rx);
  }
}

// -----------------------------------------------------------------------------
// Weak implementation of callbacks

SL_WEAK void sl_bt_ncp_transport_on_transmit(sl_status_t status)
{
  (void)status;
}

SL_WEAK void sl_bt_ncp_transport_on_receive(sl_status_t status,
                                            uint32_t    len,
                                            uint8_t     *data)
{
  (void)status;
  (void)data;
  (void)len;
}

SL_WEAK void sl_bt_ncp_transport_on_error(sl_bt_ncp_transport_error_t error,
                                          sl_status_t                 status)
{
  (void)error;
  (void)status;
  #ifdef SL_CATALOG_APP_ASSERT_PRESENT
  app_assert_status_f(status,
                      "blutetooth_ncp_transport: Error %u occurred.",
                      error);
  #endif // SL_CATALOG_APP_ASSERT_PRESENT
}

// -----------------------------------------------------------------------------
// Private functions

// Error callback
static void on_runtime_error(app_rta_error_t error, sl_status_t result)
{
  (void)error;
  sl_bt_ncp_transport_on_error(SL_BT_NCP_TRANSPORT_ERROR_RUNTIME, result);
}
