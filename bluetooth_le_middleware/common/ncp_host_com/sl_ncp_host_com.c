/***************************************************************************//**
 * @file
 * @brief Bluetooth Network Co-Processor (NCP) Host Communication Interface
 *******************************************************************************
 * # License
 * <b>Copyright 2020 Silicon Laboratories Inc. www.silabs.com</b>
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
#include <stdbool.h>
#include <string.h>
#include "sl_core.h"
#include "sl_bt_ncp_host.h"
#include "sl_bt_ncp_transport.h"
#include "sli_bt_ncp_transport.h"
#include "sl_ncp_host_com.h"
#include "app_assert.h"
#include "sl_component_catalog.h"
#if defined(SL_CATALOG_WAKE_LOCK_PRESENT)
#include "sl_wake_lock.h"
#endif // SL_CATALOG_WAKE_LOCK_PRESENT

#include "sl_bgapi.h"

/* Single RX buffer: [ complete_msg_1 | complete_msg_2 | ... | incomplete/garbage ]
 * ready_len = bytes at buf[0] that the upper layer may read: either a complete
 * message not yet started, or the remainder of a message currently being read in chunks.
 * We do not re-parse (and thus never expose partial frames) until the current message
 * has been fully read out (ready_len goes to 0), so blocking mode without peek is safe.
 */
typedef struct {
  uint16_t len;        // total bytes in buf
  uint16_t ready_len;  // bytes at start that are complete message(s)
  uint8_t buf[SL_NCP_HOST_COM_BUF_SIZE];
} rx_buf_t;

static volatile bool write_completed = false;
static rx_buf_t rx = { 0 };

#if defined(SL_CATALOG_BLUETOOTH_NCP_TRANSPORT_USART_PRESENT)
extern void sli_bt_ncp_transport_usart_cancel_receive(void);
#endif // SL_CATALOG_BLUETOOTH_NCP_TRANSPORT_USART_PRESENT

/******************************************************************************
 * Set ready_len to the length of leading complete BGAPI message(s) at buf[0],
 * so peek/read only expose full frames. Do not re-parse while we are still
 * delivering the current message (ready_len > 0), so chunked read by the
 * upper layer (e.g. sli_wait_for_bgapi_message: 1 byte, then 3, then payload)
 * keeps getting positive return until the message is fully consumed.
 *****************************************************************************/
static void sl_ncp_host_com_refill_ready(void)
{
  uint32_t offset = 0;
  uint32_t msg_len_bytes;

  // Still delivering current message in chunks; do not re-parse the buffer
  // (buffer front is the remainder of that message, not a new header).
  if (rx.ready_len > 0) {
    return;
  }

  while (rx.len > 0) {
    uint32_t header = 0;
    uint32_t payload_len;

    if ((uint32_t)rx.len - offset < SL_BGAPI_MSG_HEADER_LEN) {
      break;
    }
    memcpy((uint8_t *)&header, rx.buf + offset, SL_BGAPI_MSG_HEADER_LEN);

    if ((header & 0xf8) != (uint32_t)(sl_bgapi_dev_type_bt | sl_bgapi_msg_type_evt)
        && (header & 0xf8) != (uint32_t)(sl_bgapi_dev_type_bt)) {
      // Invalid header: discard one byte and resync
      CORE_DECLARE_IRQ_STATE;
      CORE_ENTER_ATOMIC();
      memmove(rx.buf + offset, rx.buf + offset + 1, (size_t)(rx.len - offset - 1));
      rx.len--;
      CORE_EXIT_ATOMIC();
      continue;
    }

    payload_len = SL_BGAPI_MSG_LEN(header);
    if (payload_len > SL_BGAPI_MAX_PAYLOAD_SIZE) {
      CORE_DECLARE_IRQ_STATE;
      CORE_ENTER_ATOMIC();
      memmove(rx.buf + offset, rx.buf + offset + 1, (size_t)(rx.len - offset - 1));
      rx.len--;
      CORE_EXIT_ATOMIC();
      continue;
    }

    msg_len_bytes = SL_BGAPI_MSG_HEADER_LEN + payload_len;
    if (offset + msg_len_bytes > (uint32_t)rx.len) {
      // Incomplete message; do not expose anything yet
      break;
    }

    rx.ready_len += (uint16_t)msg_len_bytes;
    offset += msg_len_bytes;
  }
}

/******************************************************************************
 * NCP host communication initialization.
 *****************************************************************************/
void sl_ncp_host_com_init(void)
{
  rx.len = 0;
  rx.ready_len = 0;
  // Register communication interface functions in adaptation layer
  sl_status_t sc = sl_bt_api_initialize_nonblock(sl_ncp_host_com_write,
                                                 sl_ncp_host_com_read,
                                                 sl_ncp_host_com_peek);
  app_assert(sc == SL_STATUS_OK,
             "[E: 0x%04x] Failed to init Bluetooth NCP\n",
             (int)sc);
}

/******************************************************************************
 * Transmit function
 *
 * Transmits len bytes of data from adaptation layer through transport layer.
 *
 * @param[out] len Message length
 * @param[out] data Message data
 *
 * @note After transmit the reception is automatically started.
 *****************************************************************************/
void sl_ncp_host_com_write(uint32_t len, uint8_t *data)
{
  write_completed = false;
  #if defined(SL_CATALOG_WAKE_LOCK_PRESENT)
  // Wake up other controller
  sl_wake_lock_set_remote_req();
  #endif // SL_CATALOG_WAKE_LOCK_PRESENT
  sl_bt_ncp_transport_transmit(len, data);
  while (!write_completed) {
    sli_bt_ncp_transport_step();
  }
  #if defined(SL_CATALOG_BLUETOOTH_NCP_TRANSPORT_USART_PRESENT)
  // Force finish any ongoing packet receiving
  sli_bt_ncp_transport_usart_cancel_receive();
  #endif // SL_CATALOG_BLUETOOTH_NCP_TRANSPORT_USART_PRESENT
  // Start to receive the response as soon as the transmit is completed
  sl_bt_ncp_transport_receive();
  // Execute receive request
  sli_bt_ncp_transport_step();
}

/******************************************************************************
 * Receive function
 *
 * Copies received data from transport layer to adaptation layer
 *
 * @param[out] len Message length
 * @param[out] data Message data
 *
 * @return Received message length
 *****************************************************************************/
int32_t sl_ncp_host_com_read(uint32_t len, uint8_t *data)
{
  // Handle receive
  sli_bt_ncp_transport_step();
  sl_ncp_host_com_refill_ready();
  CORE_DECLARE_IRQ_STATE;
  CORE_ENTER_ATOMIC();
  // Check if there is data in the buffer from transport layer
  if (len <= rx.ready_len) {
    memcpy((void *)data, (void *)rx.buf, (size_t)len);
    memmove(rx.buf, rx.buf + len, (size_t)(rx.len - len));
    rx.len -= (uint16_t)len;
    rx.ready_len -= (uint16_t)len;
  } else {
    len = (uint32_t)-1;
  }
  CORE_EXIT_ATOMIC();
  return (int32_t)len;
}

/******************************************************************************
 * Gives back already received message length.
 *
 * This function checks if data arrived from transport layer. This way the calls
 * can be non blocking.
 *
 * @param[out] len Message length
 * @param[out] data Message data
 *
 * @return Buffer length
 *****************************************************************************/
int32_t sl_ncp_host_com_peek(void)
{
  sli_bt_ncp_transport_step();
  sl_ncp_host_com_refill_ready();
  return (int32_t)rx.ready_len;
}

/******************************************************************************
 * Transmit completed callback
 *
 * Called after transmission is finished.
 *
 * @param[in] status Status of the transmission
 *****************************************************************************/
void sl_bt_ncp_transport_on_transmit(sl_status_t status)
{
  (void)status;

  #if defined(SL_CATALOG_WAKE_LOCK_PRESENT)
  // Signal other controller that it can go to sleep
  sl_wake_lock_clear_remote_req();
  #endif // SL_CATALOG_WAKE_LOCK_PRESENT

  write_completed = true;
}

/******************************************************************************
 * Receive completed callback
 *
 * Called after reception is finished. Puts the message to the reception
 * buffer.
 *
 * @param[in] status Status of the reception
 * @param[in] len Received message length
 * @param[in] data Data received
 *****************************************************************************/
void sl_bt_ncp_transport_on_receive(sl_status_t status,
                                    uint32_t len,
                                    uint8_t *data)
{
  (void)status;
  CORE_DECLARE_IRQ_STATE;
  CORE_ENTER_ATOMIC();
  // frame fits into command buffer; otherwise discard it
  if (len > 0 && len <= (sizeof(rx.buf) - rx.len)) {
    memcpy((void *)&rx.buf[rx.len], (void *)data, (size_t)len);
    rx.len += (uint16_t)len;
  }
  CORE_EXIT_ATOMIC();
}

bool sl_ncp_host_is_ok_to_sleep(void)
{
  if (rx.len != 0) {
    return false;
  }
  return true;
}
