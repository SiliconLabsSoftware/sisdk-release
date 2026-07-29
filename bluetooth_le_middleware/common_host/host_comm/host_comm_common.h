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
 *    freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 ******************************************************************************/

#ifndef HOST_COMM_COMMON_H
#define HOST_COMM_COMMON_H

#include "host_comm_ringbuf.h"
#include "sl_status.h"
#include <pthread.h>
#include <stdbool.h>
#include <stdint.h>

/**************************************************************************//**
 * @brief Context for the shared RX thread. Must be filled during init.
 *        start_routine is the pthread entry (e.g. platform msg_recv_func);
 *        the same context pointer is passed as thread argument.
 *****************************************************************************/
typedef struct host_comm_recv_ctx {
  void *                (*start_routine)(void *);
  host_comm_ringbuf_t    *rx_buffer;
  pthread_mutex_t        *rx_mutex;
  pthread_cond_t         *rx_cond;
  bool                   *data_available;
  int                   (*host_comm_pk)(void *);
  int                   (*host_comm_input)(void *, uint32_t, uint8_t *);
  void                   *handle_ptr;
  volatile bool          *run;
  void                  (*wait_for_data)(void *);
  void                   *wait_ctx;
} host_comm_recv_ctx_t;

/**************************************************************************//**
 * @brief Context for the shared TX thread. Must be filled during init.
 *        start_routine is the pthread entry (e.g. platform msg_send_func);
 *        the same context pointer is passed as thread argument.
 *****************************************************************************/
typedef struct host_comm_send_ctx {
  void *                (*start_routine)(void *);
  host_comm_ringbuf_t   *tx_buffer;
  pthread_mutex_t       *tx_mutex;
  int                  (*host_comm_output)(void *, uint32_t, uint8_t *);
  void                  *handle_ptr;
} host_comm_send_ctx_t;

/**************************************************************************//**
 * @brief Initialize shared RX and TX ring buffers.
 *
 * @param[in] rx_buffer Pointer to the RX ring buffer.
 * @param[in] tx_buffer Pointer to the TX ring buffer.
 *****************************************************************************/
void host_comm_buffers_init(host_comm_ringbuf_t *rx_buffer,
                            host_comm_ringbuf_t *tx_buffer);

/**************************************************************************//**
 * @brief Drain UART driver RX into the host ring while still in CDC bring-up
 *        line mode, then enable RTS handshake and the UART RX worker (Windows).
 *
 * @param[in] uart_handle     UART handle from uartOpen().
 * @param[in] flow_control    Non-zero if RTS/CTS is enabled.
 * @param[in] rx_buffer       Host RX ring buffer.
 * @param[in] rx_mutex        Mutex protecting rx_buffer.
 * @param[in] rx_cond         Optional condition variable to signal new data.
 * @param[in] data_available  Optional flag set when data is written.
 *
 * @return 0 on success, or a negative value if uartFinishOpen() fails.
 *****************************************************************************/
int32_t host_comm_uart_finish_open(void *uart_handle,
                                   uint32_t flow_control,
                                   host_comm_ringbuf_t *rx_buffer,
                                   pthread_mutex_t *rx_mutex,
                                   pthread_cond_t *rx_cond,
                                   bool *data_available);

/**************************************************************************//**
 * @brief Shared RX thread function for receiving data.
 *
 * All arguments are supplied via the context. When ctx->wait_for_data is
 * non-NULL (e.g. UART callback mode), the RX thread blocks on it until data
 * is signalled; when NULL, uses poll/sleep.
 *
 * @param[in] ctx Pointer to host_comm_recv_ctx_t (filled by platform).
 *            Must not be NULL.
 *
 * @return NULL.
 *****************************************************************************/
void *msg_recv_func_shared(void *ctx);

/**************************************************************************//**
 * @brief Shared TX thread function for sending data.
 *
 * All arguments are supplied via the context.
 *
 * @param[in] ctx Pointer to host_comm_send_ctx_t (filled by platform).
 *            Must not be NULL.
 *
 * @return NULL.
 *****************************************************************************/
void *msg_send_func_shared(void *ctx);

/**************************************************************************//**
 * @brief Create RX and TX threads for host communication.
 *        Uses start_routine from each context and passes the context as
 *        thread argument.
 *
 * @param[in] thread_rx Pointer to the RX thread.
 * @param[in] thread_tx Pointer to the TX thread.
 * @param[in] recv_ctx  RX context (host_comm_recv_ctx_t *).
 *                      Must not be NULL and all have set properly.
 * @param[in] send_ctx  TX context (host_comm_send_ctx_t *).
 *                      Must not be NULL and all have set properly.
 *
 * @return SL_STATUS_OK if successful, otherwise an error code.
 *****************************************************************************/
sl_status_t host_comm_threads_create(pthread_t *thread_rx,
                                     pthread_t *thread_tx,
                                     host_comm_recv_ctx_t *recv_ctx,
                                     host_comm_send_ctx_t *send_ctx);

#endif // HOST_COMM_COMMON_H
