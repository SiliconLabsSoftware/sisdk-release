/***************************************************************************//**
 * @file
 * @brief Shared logic for host communication (common).
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
 ******************************************************************************/

#include "host_comm_common.h"
#include "host_comm_config.h"
#include "host_comm_ringbuf.h"
#include "uart.h"
#include "app_log.h"
#include "app_sleep.h"
#include <pthread.h>
#include <stdio.h>
#include <stddef.h>
#include <stdbool.h>

// Shared RX and TX buffer initialization
void host_comm_buffers_init(host_comm_ringbuf_t *rx_buffer,
                            host_comm_ringbuf_t *tx_buffer)
{
  host_comm_ringbuf_init(rx_buffer);
  host_comm_ringbuf_init(tx_buffer);
}

int32_t host_comm_uart_finish_open(void *uart_handle,
                                   uint32_t flow_control,
                                   host_comm_ringbuf_t *rx_buffer,
                                   pthread_mutex_t *rx_mutex,
                                   pthread_cond_t *rx_cond,
                                   bool *data_available)
{
  uint8_t buf[256];
  bool wrote = false;

  for (;; ) {
    int32_t pending = uartRxPeek(uart_handle);
    if (pending <= 0) {
      break;
    }

    uint32_t chunk = (uint32_t)pending;
    if (chunk > sizeof(buf)) {
      chunk = (uint32_t)sizeof(buf);
    }

    pthread_mutex_lock(rx_mutex);
    size_t free_ringbuf_size = host_comm_ringbuf_get_max_size(rx_buffer)
                               - host_comm_ringbuf_data_size(rx_buffer);
    pthread_mutex_unlock(rx_mutex);

    // Avoid reading more from the driver than fits in the RX ring
    if (free_ringbuf_size == 0) {
      break;
    } else if (chunk > free_ringbuf_size) {
      chunk = (uint32_t)free_ringbuf_size;
    }

    int32_t n = uartRxNonBlocking(uart_handle, chunk, buf);
    if (n <= 0) {
      break;
    }

    pthread_mutex_lock(rx_mutex);
    size_t written = host_comm_ringbuf_write(rx_buffer, buf, (size_t)n);
    if (written > 0) {
      wrote = true;
      if (data_available != NULL) {
        *data_available = true;
      }
    }
    pthread_mutex_unlock(rx_mutex);

    if (written < (size_t)n) {
      app_log_error("RX buffer overflow during UART drain, data lost." APP_LOG_NL);
      break;
    }
  }

  if (wrote && rx_cond != NULL) {
    pthread_mutex_lock(rx_mutex);
    pthread_cond_signal(rx_cond);
    pthread_mutex_unlock(rx_mutex);
  }

  return uartFinishOpen(uart_handle, flow_control);
}

// Shared thread creation logic
sl_status_t host_comm_threads_create(pthread_t *thread_rx,
                                     pthread_t *thread_tx,
                                     host_comm_recv_ctx_t *recv_ctx,
                                     host_comm_send_ctx_t *send_ctx)
{
  int iret;

  iret = pthread_create(thread_rx, NULL, recv_ctx->start_routine, recv_ctx);
  if (iret) {
    app_log_error("pthread_create() for RX thread return code: %d" APP_LOG_NL,
                  iret);
    return SL_STATUS_FAIL;
  }

  iret = pthread_create(thread_tx, NULL, send_ctx->start_routine, send_ctx);
  if (iret) {
    app_log_error("pthread_create() for TX thread return code: %d" APP_LOG_NL,
                  iret);
    (void)pthread_cancel(*thread_rx);
    return SL_STATUS_FAIL;
  }

  return SL_STATUS_OK;
}

// Shared RX and TX buffer logic
void *msg_recv_func_shared(void *ctx)
{
  host_comm_recv_ctx_t *c = (host_comm_recv_ctx_t *)ctx;
  int32_t ret = 0;
  // Reduced temporary buffer size for memory efficiency, but may need
  // to be increased if the warning below for the input buffer size is triggered
  // in the particular application context.
  uint8_t temp_buf[DEFAULT_HOST_BUFLEN >> 3];

  if (c == NULL) {
    return NULL;
  }

  while (c->run == NULL || *c->run) {
    if (c->wait_for_data != NULL) {
      c->wait_for_data(c->wait_ctx);
      if (c->run != NULL && !*c->run) {
        break;
      }
    }

    int32_t len = c->host_comm_pk(c->handle_ptr);

    if (len < 0) {
      // Try to read at least one byte anyway, because a negative value may
      // indicate that peek is unsupported on the system
      len = 1;
    }

    const size_t max_chunk = sizeof(temp_buf);

    pthread_mutex_lock(c->rx_mutex);
    size_t occupied_size = host_comm_ringbuf_data_size(c->rx_buffer);
    pthread_mutex_unlock(c->rx_mutex);
    size_t free_ringbuf_size = host_comm_ringbuf_get_max_size(c->rx_buffer)
                               - occupied_size;

    if ((size_t)len > max_chunk) {
      len = (int32_t)max_chunk;
      app_log_warning("Input buffer size may be low, please consider increasing it."
                      APP_LOG_NL);
    }

    // Never read more from the transport than fits in the RX ring;
    // otherwise host_comm_input consumes bytes we cannot store.
    if (free_ringbuf_size == 0) {
      len = 0;
    } else if ((size_t)len > free_ringbuf_size) {
      len = (int32_t)free_ringbuf_size;
    }

    if (len > 0) {
      ret = c->host_comm_input(c->handle_ptr, (uint32_t)len, temp_buf);
    } else {
      ret = 0;
    }

    if (ret > 0) {
      pthread_mutex_lock(c->rx_mutex);
      size_t written = host_comm_ringbuf_write(c->rx_buffer, temp_buf, (size_t)ret);
      if (c->data_available != NULL) {
        *c->data_available = true;
        pthread_cond_signal(c->rx_cond);
      }
      pthread_mutex_unlock(c->rx_mutex);

      if (written < (size_t)ret) {
        app_log_error("RX buffer overflow, data lost." APP_LOG_NL);
      }
    } else {
      app_sleep_us(RECV_FUNC_US_SLEEP);
    }
  }

  return NULL;
}

void *msg_send_func_shared(void *ctx)
{
  uint8_t temp_buf[DEFAULT_HOST_BUFLEN >> 3]; // Reduced size for memory efficiency
  host_comm_send_ctx_t *c = (host_comm_send_ctx_t *)ctx;

  if (c == NULL) {
    return NULL;
  }

  while (1) {
    pthread_mutex_lock(c->tx_mutex);
    size_t len = host_comm_ringbuf_read(c->tx_buffer, temp_buf, sizeof(temp_buf));
    pthread_mutex_unlock(c->tx_mutex);

    if (len > 0) {
      int32_t ret = c->host_comm_output(c->handle_ptr, (uint32_t)len, temp_buf);
      if (ret < 0) {
        app_log_error("TX failed with return value: %d" APP_LOG_NL, ret);
      }
    } else {
      app_sleep_us(100 * RECV_FUNC_US_SLEEP);
    }
  }

  return NULL;
}
