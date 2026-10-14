/***************************************************************************//**
 * @file sli_rail_mux_aux.c
 * @brief RAIL multiplexer aux (try-register): RX FIFO drain and Zigbee stack
 *        @c sli_zigbee_stack_rail_mux_aux_* bodies / default-aux state.
 *******************************************************************************
 * # License
 * <b>Copyright 2018 Silicon Laboratories Inc. www.silabs.com</b>
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
#ifdef SL_COMPONENT_CATALOG_PRESENT
#include "sl_component_catalog.h"
#endif

#include PLATFORM_HEADER

#include "sl_code_classification.h"
#include "sl_rail.h"
#include "sl_rail_ieee802154.h"
#ifdef SL_CATALOG_RAIL_MULTIPLEXER_PRESENT
#include "sl_rail_mux_rename.h"
#endif
#include "app/framework/include/sl_zigbee_rail_mux_aux_raw.h"
#include "event_queue/event-queue.h"
#include "sli_rail_mux_aux.h"
#include "stack/include/stack-info.h"

extern sli_zigbee_event_queue_t sli_zigbee_stack_event_queue;

extern void sli_zigbee_stack_rail_mux_aux_event_callback(sl_rail_handle_t rail_handle,
                                                          sl_rail_events_t events,
                                                          uint8_t *psdu,
                                                          uint16_t psdu_length,
                                                          uint8_t lqi,
                                                          int8_t rssi_dbm,
                                                          uint32_t packet_time);
extern sl_rail_status_t sli_zigbee_stack_rail_mux_aux_register_protocol(sl_rail_handle_t *out_rail_handle,
                                                                         sl_rail_config_t *rail_config,
                                                                         sl_rail_init_complete_callback_t init_complete_callback);
extern sl_rail_status_t sli_zigbee_stack_rail_mux_aux_unregister_protocol(void);

// ----- RX drain (try-register aux handle) ---------------------------------

// 802.15.4 2.4 GHz PSDU max 127 octets; RAIL may report additional bytes; cap at one PHY frame.
#define SLI_RAIL_MUX_AUX_RX_SCRATCH_BYTES 256u
// Bound work per RX callback so OT active scan / bursty RF cannot wedge the system in a tight loop.
#define SLI_RAIL_MUX_AUX_RX_MAX_DRAIN_PER_EVENT 16u

// Static scratch avoids large stack use if the events callback runs in interrupt context.
static uint8_t sli_rail_mux_aux_rx_scratch[SLI_RAIL_MUX_AUX_RX_SCRATCH_BYTES];

SL_CODE_CLASSIFY(SL_CODE_COMPONENT_RAIL_MUX_15_4, SL_CODE_CLASS_TIME_CRITICAL)
static uint32_t sli_rail_mux_aux_rx_drain(sl_rail_handle_t rail_handle,
                                             sli_rail_mux_aux_rx_packet_callback_t callback)
{
  uint32_t drained = 0U;
  for (uint32_t iter = 0U; iter < SLI_RAIL_MUX_AUX_RX_MAX_DRAIN_PER_EVENT; iter++) {
    sl_rail_rx_packet_info_t packet_info;
    sl_rail_rx_packet_handle_t packet_handle = sl_rail_get_rx_packet_info(rail_handle,
                                                                           SL_RAIL_RX_PACKET_HANDLE_NEWEST,
                                                                           &packet_info);
    if (packet_handle == SL_RAIL_RX_PACKET_HANDLE_INVALID) {
      break;
    }

    // RAIL may raise RX_PACKET_RECEIVED for READY_SUCCESS or READY_CRC_ERROR (see sl_rail_types.h).
    if (packet_info.packet_status != SL_RAIL_RX_PACKET_READY_SUCCESS
        && packet_info.packet_status != SL_RAIL_RX_PACKET_READY_CRC_ERROR) {
      (void) sl_rail_release_rx_packet(rail_handle, packet_handle);
      continue;
    }

    if (packet_info.packet_bytes > SLI_RAIL_MUX_AUX_RX_SCRATCH_BYTES) {
      (void) sl_rail_release_rx_packet(rail_handle, packet_handle);
      continue;
    }

    sl_rail_status_t cpy = sl_rail_copy_rx_packet(rail_handle,
                                                  sli_rail_mux_aux_rx_scratch,
                                                  &packet_info);
    if (cpy == SL_RAIL_STATUS_NO_ERROR) {
      if (callback != NULL) {
        sl_rail_rx_packet_details_t details;
        uint8_t lqi = 0U;
        int8_t rssi = 0;
        uint32_t t = 0U;
        if (sl_rail_get_rx_packet_details(rail_handle, packet_handle, &details) == SL_RAIL_STATUS_NO_ERROR) {
          lqi = details.lqi;
          rssi = details.rssi_dbm;
          t = (uint32_t)details.time_received.packet_time;
        }
        callback(sli_rail_mux_aux_rx_scratch, packet_info.packet_bytes, lqi, rssi, t);
      }
      drained++;
    }
    (void) sl_rail_release_rx_packet(rail_handle, packet_handle);
  }
  return drained;
}

uint32_t sli_rail_mux_aux_rx_on_event(sl_rail_handle_t rail_handle)
{
  return sli_rail_mux_aux_rx_drain(rail_handle, NULL);
}

uint32_t sli_rail_mux_aux_rx_on_event_with_packet_callback(sl_rail_handle_t rail_handle,
                                                              sli_rail_mux_aux_rx_packet_callback_t callback)
{
  return sli_rail_mux_aux_rx_drain(rail_handle, callback);
}

// ----- Zigbee stack rail-mux-aux default listen / IPC stack bodies ----------

// Per-aux-protocol TX staging for the RAIL multiplexer: when another mux context owns the
// hardware TX FIFO, sl_rail_write_tx_fifo() copies into fifo_tx_info.data_ptr (sl_rail_mux.c).
// The aux listen rail_config must supply a non-NULL buffer and tx_fifo_bytes or that memcpy
// targets NULL (EFM_ASSERT may be disabled in release → corruption, WDG, bogus SP/PC).

enum {
  SLI_RAIL_MUX_AUX_TX_FIFO_BYTES = 256
};

SL_ALIGN(4) static uint8_t sli_rail_mux_aux_tx_fifo_buffer[SLI_RAIL_MUX_AUX_TX_FIFO_BYTES] SL_ATTRIBUTE_ALIGN(4);

static volatile uint32_t sli_rail_mux_aux_rx_packets;
static sl_rail_handle_t sli_rail_mux_aux_registered_handle = NULL;

// Defer aux callback dispatch to stack event context (never directly from RAIL ISR path).
#define SLI_RAIL_MUX_AUX_DEFERRED_CB_QUEUE_LEN 8u
typedef struct {
  sl_rail_handle_t rail_handle;
  sl_rail_events_t events;
  uint16_t psdu_length;
  uint8_t lqi;
  int8_t rssi_dbm;
  uint32_t packet_time;
  uint8_t psdu[SLI_RAIL_MUX_AUX_RX_SCRATCH_BYTES];
} sli_rail_mux_aux_deferred_cb_t;

static sli_rail_mux_aux_deferred_cb_t sli_rail_mux_aux_deferred_cb_queue[SLI_RAIL_MUX_AUX_DEFERRED_CB_QUEUE_LEN];
static volatile uint8_t sli_rail_mux_aux_deferred_cb_head;
static volatile uint8_t sli_rail_mux_aux_deferred_cb_tail;
static volatile uint8_t sli_rail_mux_aux_deferred_cb_count;
static volatile uint32_t sli_rail_mux_aux_deferred_cb_dropped;

SL_WEAK void sli_rail_mux_aux_deferred_cb_drop_hook(uint32_t dropped_count)
{
  (void)dropped_count;
}

static void sli_rail_mux_aux_isr_event_handler(sli_zigbee_event_t *event);
static void sli_rail_mux_aux_deferred_event_handler(sli_zigbee_event_t *event);

static sli_zigbee_event_t sli_rail_mux_aux_isr_event = {
  {
    &sli_zigbee_stack_event_queue,
    sli_rail_mux_aux_isr_event_handler,
    sli_zigbee_isr_event_marker,
    ""
  },
  NULL,
  0,
  0,
  NULL
};

static sli_zigbee_event_t sli_rail_mux_aux_deferred_event = {
  {
    &sli_zigbee_stack_event_queue,
    sli_rail_mux_aux_deferred_event_handler,
    NULL,
    ""
  },
  NULL,
  0,
  0,
  NULL
};

static void sli_rail_mux_aux_reset_deferred_cb_queue(void)
{
  ATOMIC(
    sli_rail_mux_aux_deferred_cb_head = 0U;
    sli_rail_mux_aux_deferred_cb_tail = 0U;
    sli_rail_mux_aux_deferred_cb_count = 0U;
    sli_rail_mux_aux_deferred_cb_dropped = 0U;
    );
}

static bool sli_rail_mux_aux_enqueue_deferred_cb(sl_rail_handle_t rail_handle,
                                                 sl_rail_events_t events,
                                                 const uint8_t *psdu,
                                                 uint16_t psdu_length,
                                                 uint8_t lqi,
                                                 int8_t rssi_dbm,
                                                 uint32_t packet_time)
{
  bool queued = false;
  bool dropped = false;
  uint32_t dropped_count = 0U;
  uint16_t copy_len = psdu_length;

  if (copy_len > SLI_RAIL_MUX_AUX_RX_SCRATCH_BYTES) {
    copy_len = SLI_RAIL_MUX_AUX_RX_SCRATCH_BYTES;
  }

  ATOMIC(
    if (sli_rail_mux_aux_deferred_cb_count < SLI_RAIL_MUX_AUX_DEFERRED_CB_QUEUE_LEN) {
    sli_rail_mux_aux_deferred_cb_t *entry = &sli_rail_mux_aux_deferred_cb_queue[sli_rail_mux_aux_deferred_cb_tail];
    entry->rail_handle = rail_handle;
    entry->events = events;
    entry->psdu_length = (psdu != NULL) ? copy_len : 0U;
    entry->lqi = lqi;
    entry->rssi_dbm = rssi_dbm;
    entry->packet_time = packet_time;
    if ((psdu != NULL) && (copy_len > 0U)) {
      for (uint16_t i = 0U; i < copy_len; i++) {
        entry->psdu[i] = psdu[i];
      }
    }
    sli_rail_mux_aux_deferred_cb_tail = (uint8_t)((sli_rail_mux_aux_deferred_cb_tail + 1U)
                                                   % SLI_RAIL_MUX_AUX_DEFERRED_CB_QUEUE_LEN);
    sli_rail_mux_aux_deferred_cb_count++;
    queued = true;
  } else {
    sli_rail_mux_aux_deferred_cb_dropped++;
    dropped = true;
    dropped_count = sli_rail_mux_aux_deferred_cb_dropped;
  }
    );

  if (dropped) {
    sli_rail_mux_aux_deferred_cb_drop_hook(dropped_count);
  }

  return queued;
}

static bool sli_rail_mux_aux_dequeue_deferred_cb(sli_rail_mux_aux_deferred_cb_t *out)
{
  bool has_item = false;

  ATOMIC(
    if (sli_rail_mux_aux_deferred_cb_count > 0U) {
    *out = sli_rail_mux_aux_deferred_cb_queue[sli_rail_mux_aux_deferred_cb_head];
    sli_rail_mux_aux_deferred_cb_head = (uint8_t)((sli_rail_mux_aux_deferred_cb_head + 1U)
                                                   % SLI_RAIL_MUX_AUX_DEFERRED_CB_QUEUE_LEN);
    sli_rail_mux_aux_deferred_cb_count--;
    has_item = true;
  }
    );

  return has_item;
}

static void sli_rail_mux_aux_isr_event_handler(sli_zigbee_event_t *event)
{
  (void)event;
  sli_zigbee_event_set_active(&sli_rail_mux_aux_deferred_event);
}

static void sli_rail_mux_aux_deferred_event_handler(sli_zigbee_event_t *event)
{
  sli_rail_mux_aux_deferred_cb_t cb_event;
  (void)event;

  while (sli_rail_mux_aux_dequeue_deferred_cb(&cb_event)) {
    sli_zigbee_stack_rail_mux_aux_event_callback(cb_event.rail_handle,
                                                 cb_event.events,
                                                 (cb_event.psdu_length > 0U) ? cb_event.psdu : NULL,
                                                 cb_event.psdu_length,
                                                 cb_event.lqi,
                                                 cb_event.rssi_dbm,
                                                 cb_event.packet_time);
  }
}

static void sli_rail_mux_aux_rx_to_event_bridge(uint8_t *psdu,
                                                uint16_t psdu_length,
                                                uint8_t lqi,
                                                int8_t rssi_dbm,
                                                uint32_t packet_time)
{
  if (sli_rail_mux_aux_enqueue_deferred_cb(sli_rail_mux_aux_registered_handle,
                                           SL_RAIL_EVENT_RX_PACKET_RECEIVED,
                                           psdu,
                                           psdu_length,
                                           lqi,
                                           rssi_dbm,
                                           packet_time)) {
    sli_zigbee_event_set_active(&sli_rail_mux_aux_isr_event);
  }
}

static void sli_rail_mux_aux_rail_events_cb(sl_rail_handle_t rail_handle, sl_rail_events_t events)
{
  /* One app callback receives both RX-delivery and non-RX event notifications. */
  if (rail_handle != sli_rail_mux_aux_registered_handle) {
    return;
  }
  if ((events & SL_RAIL_EVENT_RX_PACKET_RECEIVED) != 0U) {
    sli_rail_mux_aux_rx_packets += sli_rail_mux_aux_rx_on_event_with_packet_callback(rail_handle,
                                                                                       sli_rail_mux_aux_rx_to_event_bridge);
  }
  sl_rail_events_t non_rx_events = events & ~SL_RAIL_EVENT_RX_PACKET_RECEIVED;
  if (non_rx_events != 0U) {
    if (sli_rail_mux_aux_enqueue_deferred_cb(rail_handle,
                                             non_rx_events,
                                             NULL,
                                             0U,
                                             0U,
                                             0,
                                             0U)) {
      sli_zigbee_event_set_active(&sli_rail_mux_aux_isr_event);
    }
  }
}

static sl_rail_config_t sli_rail_mux_aux_rail_cfg = {
  .events_callback = sli_rail_mux_aux_rail_events_cb,
  .p_tx_fifo_buffer = (sl_rail_fifo_buffer_align_t *)sli_rail_mux_aux_tx_fifo_buffer,
  .tx_fifo_bytes = SLI_RAIL_MUX_AUX_TX_FIFO_BYTES,
  .tx_fifo_init_bytes = 0U,
};

sl_rail_config_t *sli_zigbee_stack_rail_mux_aux_get_default_rail_config(void)
{
  return &sli_rail_mux_aux_rail_cfg;
}

uint32_t sli_zigbee_stack_rail_mux_aux_get_default_listen_rx_packet_count(void)
{
  return sli_rail_mux_aux_rx_packets;
}

void sli_rail_mux_aux_on_register_success(sl_rail_handle_t rail_handle)
{
  sli_rail_mux_aux_registered_handle = rail_handle;
  sli_rail_mux_aux_rx_packets = 0U;
  sli_rail_mux_aux_reset_deferred_cb_queue();
}

void sli_rail_mux_aux_on_unregister_success(void)
{
  sli_rail_mux_aux_registered_handle = NULL;
  sli_rail_mux_aux_rx_packets = 0U;
  sli_rail_mux_aux_reset_deferred_cb_queue();
}

sl_rail_handle_t sli_zigbee_stack_rail_mux_aux_get_default_rail_handle(void)
{
  return sli_rail_mux_aux_registered_handle;
}

uint16_t sli_zigbee_stack_rail_mux_aux_write_tx_fifo(sl_rail_handle_t rail_handle,
                                                     const uint8_t *data_ptr,
                                                     uint16_t write_length,
                                                     bool reset)
{
  return sl_rail_write_tx_fifo(rail_handle, data_ptr, write_length, reset);
}

sl_rail_status_t sli_zigbee_stack_rail_mux_aux_start_tx(sl_rail_handle_t rail_handle,
                                                        uint8_t channel,
                                                        sl_rail_tx_options_t options,
                                                        const sl_rail_scheduler_info_t *scheduler_info)
{
  return sl_rail_start_tx(rail_handle, channel, options, scheduler_info);
}

sl_rail_status_t sli_zigbee_stack_rail_mux_aux_start_cca_csma_tx(sl_rail_handle_t rail_handle,
                                                                 uint8_t channel,
                                                                 sl_rail_tx_options_t options,
                                                                 const sl_rail_csma_config_t *csma_config,
                                                                 const sl_rail_scheduler_info_t *scheduler_info)
{
  return sl_rail_start_cca_csma_tx(rail_handle, channel, options, csma_config, scheduler_info);
}

sl_rail_status_t sli_zigbee_stack_rail_mux_aux_try_register_and_start_rx(uint16_t aux_pan,
                                                                          uint8_t channel)
{
  sl_rail_handle_t out_handle = NULL;
  sl_rail_status_t st = sli_zigbee_stack_rail_mux_aux_register_protocol(&out_handle,
                                                                         sli_zigbee_stack_rail_mux_aux_get_default_rail_config(),
                                                                         NULL);

  if (st != SL_RAIL_STATUS_NO_ERROR) {
    return st;
  }

  if (aux_pan == sl_zigbee_get_pan_id()) {
    (void)sli_zigbee_stack_rail_mux_aux_unregister_protocol();
    return SL_RAIL_STATUS_INVALID_PARAMETER;
  }

  if (channel == 0U) {
    channel = sl_zigbee_get_radio_channel();
  }

  st = sl_rail_ieee802154_set_pan_id(out_handle, aux_pan, 0);
  if (st != SL_RAIL_STATUS_NO_ERROR) {
    (void)sli_zigbee_stack_rail_mux_aux_unregister_protocol();
    return st;
  }

  st = sl_rail_ieee802154_set_short_address(out_handle, 0xFFFF, 0);
  if (st != SL_RAIL_STATUS_NO_ERROR) {
    (void)sli_zigbee_stack_rail_mux_aux_unregister_protocol();
    return st;
  }

  // Aux listen uses the mux's normal 802.15.4 address filtering (like the Zigbee context),
  // not global promiscuous mode. The aux PAN id and short address registered above, together
  // with the always-enabled broadcast filter, let broadcast frames (e.g. 15.4 beacon requests)
  // and aux-PAN traffic reach the aux context. Enabling promiscuous mode here would disable
  // hardware address filtering for every mux context and cause the RX dispatch to drop
  // non-ack/non-beacon frames (beacon requests are MAC command frames) on the aux context.

  // Aux listen is a sniffer-style path for mux validation; accept on-channel traffic broadly.
  // st = sl_rail_ieee802154_set_promiscuous_mode(out_handle, true);
  // if (st != SL_RAIL_STATUS_NO_ERROR) {
  //   (void)sli_zigbee_stack_rail_mux_aux_unregister_protocol();
  //   return st;
  // }

  st = sl_rail_config_events(out_handle,
                             SL_RAIL_EVENTS_ALL,
                             (SL_RAIL_EVENT_CAL_NEEDED
                              | SL_RAIL_EVENT_RX_PACKET_RECEIVED
                              | SL_RAIL_EVENT_TX_PACKET_SENT
                              | SL_RAIL_EVENT_TX_ABORTED
                              | SL_RAIL_EVENT_TX_UNDERFLOW
                              | SL_RAIL_EVENT_TX_CHANNEL_BUSY
                              | SL_RAIL_EVENT_TX_BLOCKED
                              | SL_RAIL_EVENT_SCHEDULER_STATUS));
  if (st != SL_RAIL_STATUS_NO_ERROR) {
    (void)sli_zigbee_stack_rail_mux_aux_unregister_protocol();
    return st;
  }

  st = sl_rail_start_rx(out_handle, channel, NULL);
  if (st != SL_RAIL_STATUS_NO_ERROR) {
    (void)sli_zigbee_stack_rail_mux_aux_unregister_protocol();
    return st;
  }

  return SL_RAIL_STATUS_NO_ERROR;
}
