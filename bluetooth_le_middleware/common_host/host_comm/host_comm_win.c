/***************************************************************************//**
 * @file
 * @brief Host communication application module (windows).
 *******************************************************************************
 * # License
 * <b>Copyright 2023 Silicon Laboratories Inc. www.silabs.com</b>
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

#include <errno.h>
#include <stdint.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include <winsock2.h>
#include <windows.h>
#include <stddef.h>
#include "uart.h"
#include "tcp.h"
#include "app_assert.h"
#include "app_log.h"
#include "host_comm.h"
#include "app_sleep.h"
#include "host_comm_config.h"
#include "host_comm_ringbuf.h"
#include "host_comm_common.h"

// Default parameter values.
#define DEFAULT_UART_PORT             ""
#define DEFAULT_UART_BAUD_RATE        115200
#define DEFAULT_UART_FLOW_CONTROL     1
#define DEFAULT_UART_TIMEOUT          100
#define DEFAULT_TCP_ADDRESS           ""
#define DEFAULT_TCP_PORT              "4901"
#define MAX_OPT_LEN                   255
#define DEFAULT_CPC_INST_NAME         "cpcd_0"

#define IS_EMPTY_STRING(s)            ((s)[0] == '\0')
#define HANDLE_VALUE_MIN              0

// Define global HOST_COMM_API_DEFINE library.
HOST_COMM_API_DEFINE();

// Define global variables
static volatile bool run = true;
static bool comm_channel_selected = false;

static host_comm_ringbuf_t rx_buffer;
static host_comm_ringbuf_t tx_buffer;

// UART serial port options.
static char uart_port[MAX_OPT_LEN] = DEFAULT_UART_PORT;
static uint32_t uart_baud_rate = DEFAULT_UART_BAUD_RATE;
static uint32_t uart_flow_control = DEFAULT_UART_FLOW_CONTROL;

// TCP/IP address.
static char tcp_address[MAX_OPT_LEN] = DEFAULT_TCP_ADDRESS;

SOCKET socket_handle;
void *handle_ptr;

// UART callback mode: wake RX thread when data is available (no poll/sleep).
static bool use_uart_rx_callback = false;
static HANDLE rx_wake_event = NULL;

typedef struct {
  HANDLE event;
  volatile bool *run;
} host_comm_rx_wake_ctx_win_t;
static host_comm_rx_wake_ctx_win_t rx_wake_ctx_win;

static void uart_rx_wake_callback(void *handle, void *user_ctx);
static void wait_for_uart_data_win(void *ctx);

// Static receive function
void *msg_recv_func(void *ptr);
void *msg_send_func(void *ptr);

pthread_t thread_rx;
pthread_t thread_tx;

static pthread_mutex_t rx_mutex = PTHREAD_MUTEX_INITIALIZER;
static pthread_mutex_t tx_mutex = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t  rx_cond  = PTHREAD_COND_INITIALIZER;
static bool data_available      = false;

static host_comm_recv_ctx_t recv_ctx = { 0 };
static host_comm_send_ctx_t send_ctx = { 0 };

/******************************************************************************
 * UART RX callback: signal RX thread that data is available (event-driven).
 *****************************************************************************/
static void uart_rx_wake_callback(void *handle, void *user_ctx)
{
  (void)handle;
  host_comm_rx_wake_ctx_win_t *ctx = (host_comm_rx_wake_ctx_win_t *)user_ctx;
  if (ctx != NULL && ctx->event != NULL) {
    SetEvent(ctx->event);
  }
}

/******************************************************************************
 * Block until UART callback signals or timeout (for run check). Used when
 * uartSetRxCallback is active instead of poll/sleep.
 *****************************************************************************/
static void wait_for_uart_data_win(void *ctx)
{
  host_comm_rx_wake_ctx_win_t *c = (host_comm_rx_wake_ctx_win_t *)ctx;
  if (c == NULL || c->event == NULL) {
    return;
  }
  while (c->run != NULL && *c->run) {
    DWORD w = WaitForSingleObject(c->event, 200);  // 200 ms
    if (w == WAIT_OBJECT_0) {
      break;
    }
  }
}

/******************************************************************************
 * Close UART port and worker started by host_comm_uart_finish_open().
 *****************************************************************************/
static void host_commuart_abort_open(void)
{
  if (use_uart_rx_callback && handle_ptr != NULL) {
    uartSetRxCallback(handle_ptr, NULL, NULL);
  }
  if (rx_wake_event != NULL) {
    SetEvent(rx_wake_event);
    CloseHandle(rx_wake_event);
    rx_wake_event = NULL;
  }
  use_uart_rx_callback = false;
  if (handle_ptr != NULL) {
    uartClose(handle_ptr);
    uartHandleFree(handle_ptr);
    handle_ptr = NULL;
  }
}

/******************************************************************************
 * Initialize low level connection.
 *****************************************************************************/
sl_status_t host_comm_init(void)
{
  int32_t status;

  if (!comm_channel_selected) {
    app_log_error("No communication channel provided, "
                  "but exactly one is expected!" APP_LOG_NL);
    return SL_STATUS_INVALID_PARAMETER;
  }

  if (!IS_EMPTY_STRING(uart_port)) {
    // Initialise UART serial connection - the handle will be allocated by UART API.
    handle_ptr = uartHandleAlloc();
    if (handle_ptr == NULL) {
      app_log_error("Failed to allocate UART handle." APP_LOG_NL);
      exit(EXIT_FAILURE);
    }
    HOST_COMM_API_INITIALIZE_NONBLOCK(uartTx, uartRx, uartRxPeek);
    status = uartOpen(handle_ptr, (int8_t *)uart_port, uart_baud_rate,
                      uart_flow_control, DEFAULT_UART_TIMEOUT);
    if (status < HANDLE_VALUE_MIN) {
      app_log_error("Failed to open serial connection (%d)"
                    APP_LOG_NL, status);
      uartHandleFree(handle_ptr);
      exit(EXIT_FAILURE);
    }
    uartFlush(handle_ptr);
    // Event-driven RX: register callback so RX thread blocks on event instead of poll/sleep.
    // Auto-reset, so each WaitForSingleObject consumes the signal. Next wait() blocks until callback signals again.
    rx_wake_event = CreateEventA(NULL, FALSE, FALSE, NULL);
    if (rx_wake_event != NULL) {
      rx_wake_ctx_win.event = rx_wake_event;
      rx_wake_ctx_win.run = &run;
      if (uartSetRxCallback(handle_ptr, uart_rx_wake_callback, &rx_wake_ctx_win) == 0) {
        use_uart_rx_callback = true;
      }
    }
  } else if (!IS_EMPTY_STRING(tcp_address)) {
    // Initialise TCP/IP connection.
    handle_ptr = &socket_handle;
    HOST_COMM_API_INITIALIZE_NONBLOCK(tcp_tx, tcp_rx, tcp_rx_peek);
    status = tcp_open(handle_ptr, tcp_address, DEFAULT_TCP_PORT);
    app_assert(status == HANDLE_VALUE_MIN,
               "[E: %d] Failed to open TCP/IP connection" APP_LOG_NL,
               status);
  } else {
    return SL_STATUS_INVALID_PARAMETER;
  }

  host_comm_buffers_init(&rx_buffer, &tx_buffer);

  if (!IS_EMPTY_STRING(uart_port)) {
    status = host_comm_uart_finish_open(handle_ptr,
                                        uart_flow_control,
                                        &rx_buffer,
                                        &rx_mutex,
                                        &rx_cond,
                                        &data_available);
    if (status != 0) {
      app_log_error("Failed to finish UART open (%d)" APP_LOG_NL, status);
      host_commuart_abort_open();
      exit(EXIT_FAILURE);
    }
  }

  recv_ctx.start_routine   = msg_recv_func;
  recv_ctx.rx_buffer       = &rx_buffer;
  recv_ctx.rx_mutex        = &rx_mutex;
  recv_ctx.rx_cond         = &rx_cond;
  recv_ctx.data_available  = &data_available;
  recv_ctx.host_comm_pk    = host_comm_pk;
  recv_ctx.host_comm_input = host_comm_input;
  recv_ctx.handle_ptr      = handle_ptr;
  recv_ctx.run             = &run;
  recv_ctx.wait_for_data   = use_uart_rx_callback ? wait_for_uart_data_win : NULL;
  recv_ctx.wait_ctx        = use_uart_rx_callback ? (void *)&rx_wake_ctx_win : NULL;

  send_ctx.start_routine    = msg_send_func;
  send_ctx.tx_buffer        = &tx_buffer;
  send_ctx.tx_mutex         = &tx_mutex;
  send_ctx.host_comm_output = host_comm_output;
  send_ctx.handle_ptr       = handle_ptr;

  sl_status_t sc = host_comm_threads_create(&thread_rx, &thread_tx, &recv_ctx, &send_ctx);
  if (sc != SL_STATUS_OK) {
    if (!IS_EMPTY_STRING(uart_port)) {
      host_commuart_abort_open();
    }
    return sc;
  }

  return SL_STATUS_OK;
}

/******************************************************************************
 * Set low level host communication connection options.
 *****************************************************************************/
sl_status_t host_comm_set_option(char option, char *value)
{
  sl_status_t sc = SL_STATUS_OK;

  switch (option) {
    // TCP/IP address.
    case 't':
      if (!comm_channel_selected) {
        if (strlen(value) >= MAX_OPT_LEN - 1) {
          app_log_error("Value for option '%c' is too long, truncating to %d characters." APP_LOG_NL, option, MAX_OPT_LEN - 1);
        }
        strncpy(tcp_address, value, MAX_OPT_LEN - 1);
        tcp_address[MAX_OPT_LEN - 1] = '\0'; // Ensure null-termination
        comm_channel_selected = true;
      } else {
        app_log_error("More than one communication channel "
                      "provided, but exactly one is expected!" APP_LOG_NL);
        sc = SL_STATUS_INVALID_PARAMETER;
      }
      break;
    // UART serial port.
    case 'u':
      if (!comm_channel_selected) {
        if (strlen(value) >= MAX_OPT_LEN - 1) {
          app_log_error("Value for option '%c' is too long, truncating to %d characters." APP_LOG_NL, option, MAX_OPT_LEN - 1);
        }
        strncpy(uart_port, value, MAX_OPT_LEN - 1);
        uart_port[MAX_OPT_LEN - 1] = '\0'; // Ensure null-termination
        comm_channel_selected = true;
      } else {
        app_log_error("More than one communication channel "
                      "provided, but exactly one is expected!" APP_LOG_NL);
        sc = SL_STATUS_INVALID_PARAMETER;
      }
      break;
    // UART baud rate.
    case 'b':
      uart_baud_rate = atol(value);
      break;
    // UART flow control disable.
    case 'f':
      uart_flow_control = 0;
      break;
    // Unknown option.
    default:
      sc = SL_STATUS_NOT_FOUND;
      break;
  }
  return sc;
}

/******************************************************************************
 * Deinitialize low level connection.
 *****************************************************************************/
void host_comm_deinit(void)
{
  run = false;
  if (use_uart_rx_callback && rx_wake_event != NULL) {
    uartSetRxCallback(handle_ptr, NULL, NULL);
    SetEvent(rx_wake_event);
  }
  pthread_cancel(thread_rx);
  pthread_cancel(thread_tx);

  if (!IS_EMPTY_STRING(uart_port)) {
    uartClose(handle_ptr);
    uartHandleFree(handle_ptr);
    handle_ptr = NULL;
    if (rx_wake_event != NULL) {
      CloseHandle(rx_wake_event);
      rx_wake_event = NULL;
    }
  } else if (!IS_EMPTY_STRING(tcp_address)) {
    tcp_close(handle_ptr);
  }
}

/******************************************************************************
 * Write data to NCP through low level drivers.
 *****************************************************************************/
int32_t host_comm_tx(uint32_t len, uint8_t* data)
{
  pthread_mutex_lock(&tx_mutex);
  size_t written = host_comm_ringbuf_write(&tx_buffer, data, (size_t)len);
  pthread_mutex_unlock(&tx_mutex);
  if (written < (size_t)len) {
    app_log_error("TX buffer overflow, data lost." APP_LOG_NL);
  }
  return (int32_t)written;
}

/******************************************************************************
 * Read data from NCP.
 *****************************************************************************/
int32_t host_comm_rx(uint32_t len, uint8_t* data)
{
  int32_t ret = -1;
  pthread_mutex_lock(&rx_mutex);
  ret = (int32_t)host_comm_ringbuf_read(&rx_buffer, data, (size_t)len);
  pthread_mutex_unlock(&rx_mutex);
  return ret;
}

/******************************************************************************
 * Peek if readable data exists.
 *****************************************************************************/
int32_t host_comm_peek_(void)
{
  int32_t len = 0;
  pthread_mutex_lock(&rx_mutex);
  len = (int32_t)host_comm_ringbuf_data_size(&rx_buffer);
  pthread_mutex_unlock(&rx_mutex);

  return len;
}

int32_t host_comm_peek(void)
{
  // 2 ms wait per iteration; deadline computed under rx_mutex so it cannot
  // expire before pthread_cond_timedwait runs; this avoids spurious empty peek.
  const unsigned cond_wait_ms = 2;

  pthread_mutex_lock(&rx_mutex);

  int32_t len = (int32_t)host_comm_ringbuf_data_size(&rx_buffer);
  if (len > 0) {
    data_available = true;
    pthread_mutex_unlock(&rx_mutex);
    return len;
  }

  while (!data_available) {
    struct timespec ts;
    FILETIME ft;
    ULARGE_INTEGER uli;

    GetSystemTimePreciseAsFileTime(&ft);
    uli.LowPart  = ft.dwLowDateTime;
    uli.HighPart = ft.dwHighDateTime;

    uint64_t ns = (uli.QuadPart - 116444736000000000ULL) * 100ULL;
    ns += (uint64_t)cond_wait_ms * 1000000ULL;

    ts.tv_sec  = (time_t)(ns / 1000000000ULL);
    ts.tv_nsec = (long)(ns % 1000000000ULL);

    int rc;
    do {
      rc = pthread_cond_timedwait(&rx_cond, &rx_mutex, &ts);
    } while (rc == EINTR);

    if (rc == ETIMEDOUT) {
      len = (int32_t)host_comm_ringbuf_data_size(&rx_buffer);
      data_available = !!len;
      pthread_mutex_unlock(&rx_mutex);
      return len;
    }
    if (rc != 0) {
      len = (int32_t)host_comm_ringbuf_data_size(&rx_buffer);
      data_available = !!len;
      pthread_mutex_unlock(&rx_mutex);
      return len;
    }
  }

  len = (int32_t)host_comm_ringbuf_data_size(&rx_buffer);
  data_available = !!len;

  pthread_mutex_unlock(&rx_mutex);
  return len;
}

/******************************************************************************
 * Read data from low level drivers.
 *****************************************************************************/
void *msg_recv_func(void *ptr)
{
  // unused variable
  (void)ptr;

  return msg_recv_func_shared(ptr);
}

/******************************************************************************
 * Write data to low level drivers.
 *****************************************************************************/
void *msg_send_func(void *ptr)
{
  // unused variable
  (void)ptr;

  return msg_send_func_shared(ptr);
}
