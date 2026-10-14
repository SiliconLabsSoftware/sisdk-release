/***************************************************************************//**
 * @file rail_mux_aux_cli.c
 * @brief CLI commands for RAIL multiplexer auxiliary-protocol tests (rail-mux-aux group).
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
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

#include "app/framework/include/af.h"
#include "app/framework/include/sl_zigbee_rail_mux_aux_cli.h"
#include "app/framework/include/sl_zigbee_rail_mux_aux_raw.h"
#include "app/util/serial/sl_zigbee_command_interpreter.h"
#include "sl_rail.h"
#ifdef SL_CATALOG_RAIL_MULTIPLEXER_PRESENT
#include "sl_rail_mux_rename.h"
#include "sl_rail_mux.h"
#endif

#if defined(SL_CATALOG_CLI_PRESENT)

/** Persistent: print every aux RX PSDU while @c aux-rx-callback-on is active. */
static volatile uint8_t sli_rail_mux_aux_cli_rx_print_enabled;
/** One-shot: print next TX completion from @c tx-fixed-psdu. */
static volatile uint8_t sli_rail_mux_aux_cli_observe_tx;
/** One-shot after local @c tx-fixed-psdu: skip one loopback of the fixed sample. */
static volatile uint8_t sli_rail_mux_aux_cli_suppress_local_fixed_psdu_echo;

static void sli_rail_mux_aux_cli_clear_observers(void)
{
  sli_rail_mux_aux_cli_rx_print_enabled = 0U;
  sli_rail_mux_aux_cli_observe_tx = 0U;
  sli_rail_mux_aux_cli_suppress_local_fixed_psdu_echo = 0U;
}

static void sli_rail_mux_aux_cli_print_rx_psdu(const uint8_t *psdu, uint16_t psdu_length)
{
  uint16_t i;
  uint16_t nprint = psdu_length;
  if (nprint > 48U) {
    nprint = 48U;
  }
  sl_zigbee_af_cli_print("aux_raw_rx_psdu:%u:", psdu_length);
  for (i = 0U; i < nprint; i++) {
    sl_zigbee_af_cli_print(" %02X", psdu[i]);
  }
  if (psdu_length > nprint) {
    sl_zigbee_af_cli_print(" ...");
  }
  sl_zigbee_af_cli_println("");
}

void sl_zigbee_cli_rail_mux_aux_try_register(sl_cli_command_arg_t *arguments)
{
  uint16_t aux_pan = sl_cli_get_argument_uint16(arguments, 0);
  uint8_t channel = sl_cli_get_argument_uint8(arguments, 1);
  sl_rail_handle_t out_handle;
  sl_rail_status_t st;

  sli_rail_mux_aux_cli_clear_observers();

  st = sl_zigbee_rail_mux_aux_try_register_and_start_rx(aux_pan, channel);
  sl_zigbee_af_cli_println("mux_reg:0x%04X", (unsigned int)st);
  if (st != SL_RAIL_STATUS_NO_ERROR) {
    if (aux_pan == sl_zigbee_get_pan_id()) {
      sl_zigbee_af_cli_println("mux_aux_pan:error_same_as_stack");
    } else {
      sl_zigbee_af_cli_println("mux_aux_pan:skipped");
    }
    sl_zigbee_af_cli_println("aux_rx_listen:skipped");
    return;
  }

  out_handle = sl_zigbee_rail_mux_aux_get_default_rail_handle();
  sl_zigbee_af_cli_println("mux_handle:%08lX", (unsigned long)(uintptr_t)out_handle);
  sl_zigbee_af_cli_println("mux_aux_pan:0x%04X", aux_pan);
  sl_zigbee_af_cli_println("aux_rx_listen:ok");
}

void sl_zigbee_cli_rail_mux_aux_unregister_aux(sl_cli_command_arg_t *arguments)
{
  (void)arguments;
  sl_rail_status_t st = sl_zigbee_rail_mux_aux_unregister_protocol();
  if (st == SL_RAIL_STATUS_NO_ERROR) {
    sli_rail_mux_aux_cli_clear_observers();
  }
  sl_zigbee_af_cli_println("mux_aux_tear:0x%04X", (unsigned int)st);
}

// Zigbee stack MAC counter (sl_zigbee_read_counters), not mux/RAIL RX delivered to the
// try-register handle. For that path use rail-mux-aux auxcount (packets copied+released for aux handle).
void sl_zigbee_cli_rail_mux_aux_mac_rx_unicast(sl_cli_command_arg_t *arguments)
{
  (void)arguments;
  uint16_t counters[SL_ZIGBEE_COUNTER_TYPE_COUNT];

  sl_zigbee_read_counters(counters, SL_ZIGBEE_COUNTER_TYPE_COUNT);
  sl_zigbee_af_cli_println("mac_rx_unicast:%u",
                           counters[SL_ZIGBEE_COUNTER_MAC_RX_UNICAST]);
}

void sl_zigbee_cli_rail_mux_aux_rx_count(sl_cli_command_arg_t *arguments)
{
  uint32_t n = sl_zigbee_rail_mux_aux_get_default_listen_rx_packet_count();
  (void)arguments;
  sl_zigbee_af_cli_println("mux_aux:%lu", (unsigned long)n);
}

/** Fixed PSDU for rail-mux-aux tx-fixed-psdu (802.15.4-style bytes; CRC added by RAIL). */
// static const uint8_t rail_mux_aux_cli_tx_fixed_psdu_sample[] = {
//   0x0F, 0x0A, 0x03, 0x08, 0x20, 0xFF, 0xFF, 0xFF, 0xFF,
//   0x07, 0x58, 0xAC, 0xFD, 0x0D, 0x05, 0x01
// };

// Beacon request (802.15.4 command; RAIL appends CRC on TX).
static const uint8_t rail_mux_aux_cli_tx_fixed_psdu_sample[] = {
  0x0A,                         // PHR: length = 10 (8 MAC + 2 CRC)
  0x03, 0x08,                   // FCF: command, dest short, no source
  0x01,                         // Sequence number
  0xFF, 0xFF,                   // Dest PAN broadcast
  0xFF, 0xFF,                   // Dest short broadcast
  0x07                          // Command ID: Beacon Request
};

#define RAIL_MUX_AUX_CLI_TX_FIXED_PSDU_LEN ((uint16_t)sizeof(rail_mux_aux_cli_tx_fixed_psdu_sample))

static bool sli_rail_mux_aux_cli_is_tx_fixed_psdu_echo(const uint8_t *psdu, uint16_t psdu_length)
{
  return (psdu != NULL)
         && (psdu_length == RAIL_MUX_AUX_CLI_TX_FIXED_PSDU_LEN)
         && (memcmp(psdu, rail_mux_aux_cli_tx_fixed_psdu_sample, RAIL_MUX_AUX_CLI_TX_FIXED_PSDU_LEN) == 0);
}

/* Observers for rail-mux-aux tx-fixed-psdu only. */
#define RAIL_MUX_AUX_CLI_TX_COMPLETE_EVENTS (SL_RAIL_EVENT_TX_PACKET_SENT       \
                                             | SL_RAIL_EVENT_TX_ABORTED          \
                                             | SL_RAIL_EVENT_TX_UNDERFLOW        \
                                             | SL_RAIL_EVENT_TX_CHANNEL_BUSY     \
                                             | SL_RAIL_EVENT_TX_BLOCKED)

void sl_zigbee_rail_mux_aux_event_callback(sl_rail_handle_t rail_handle,
                                           sl_rail_events_t events,
                                           uint8_t *psdu,
                                           uint16_t psdu_length,
                                           uint8_t link_quality,
                                           int8_t rssi_dbm,
                                           uint32_t pkt_rx_timestamp)
{
  sl_rail_events_t tx_events = events & RAIL_MUX_AUX_CLI_TX_COMPLETE_EVENTS;

  (void)rail_handle;
  (void)link_quality;
  (void)rssi_dbm;
  (void)pkt_rx_timestamp;

  if ((tx_events != 0U) && (sli_rail_mux_aux_cli_observe_tx != 0U)) {
    sl_zigbee_af_cli_println("aux_tx_complete:0x%08lX", (unsigned long)(uintptr_t)tx_events);
    sli_rail_mux_aux_cli_observe_tx = 0U;
  }

  if (((events & SL_RAIL_EVENT_RX_PACKET_RECEIVED) != 0U)
      && (sli_rail_mux_aux_cli_rx_print_enabled != 0U)
      && (psdu != NULL)) {
    if ((sli_rail_mux_aux_cli_suppress_local_fixed_psdu_echo != 0U)
        && sli_rail_mux_aux_cli_is_tx_fixed_psdu_echo(psdu, psdu_length)) {
      sli_rail_mux_aux_cli_suppress_local_fixed_psdu_echo = 0U;
    } else {
      sli_rail_mux_aux_cli_print_rx_psdu(psdu, psdu_length);
    }
  }
}

/**
 * CLI/task context only.
 *
 * Arms a one-shot TX-complete print, then writes the fixed PSDU and starts TX/CSMA.
 * Does not enable RX printing — use @c aux-rx-callback-on for that.
 */
void sl_zigbee_cli_rail_mux_aux_tx_fixed_psdu(sl_cli_command_arg_t *arguments)
{
  sl_rail_handle_t h = sl_zigbee_rail_mux_aux_get_default_rail_handle();
  uint8_t channel = sl_cli_get_argument_uint8(arguments, 0);
  uint8_t use_csma = sl_cli_get_argument_uint8(arguments, 1);
  uint16_t written;
  sl_rail_status_t st;
  sl_rail_csma_config_t csma = SL_RAIL_CSMA_CONFIG_802_15_4_2003_2P4_GHZ_OQPSK_CSMA;

  if (h == NULL) {
    sl_zigbee_af_cli_println("aux_tx:need_try_register");
    return;
  }

  if (channel == 0U) {
    channel = sl_zigbee_get_radio_channel();
  }

  // Arm before start_tx so async TX-complete is observed.
  sli_rail_mux_aux_cli_observe_tx = 1U;
  if (sli_rail_mux_aux_cli_rx_print_enabled != 0U) {
    sli_rail_mux_aux_cli_suppress_local_fixed_psdu_echo = 1U;
  }

  written = sl_zigbee_rail_mux_aux_write_tx_fifo(h,
                                                 rail_mux_aux_cli_tx_fixed_psdu_sample,
                                                 RAIL_MUX_AUX_CLI_TX_FIXED_PSDU_LEN,
                                                 true);
  sl_zigbee_af_cli_println("aux_tx:fifo_written:%u_of_%u", written, RAIL_MUX_AUX_CLI_TX_FIXED_PSDU_LEN);
  if (written != RAIL_MUX_AUX_CLI_TX_FIXED_PSDU_LEN) {
    sli_rail_mux_aux_cli_observe_tx = 0U;
    sli_rail_mux_aux_cli_suppress_local_fixed_psdu_echo = 0U;
    sl_zigbee_af_cli_println("aux_tx:abort");
    return;
  }

  if (use_csma != 0U) {
    st = sl_zigbee_rail_mux_aux_start_cca_csma_tx(h,
                                                  channel,
                                                  SL_RAIL_TX_OPTIONS_DEFAULT,
                                                  &csma,
                                                  NULL);
  } else {
    st = sl_zigbee_rail_mux_aux_start_tx(h,
                                        channel,
                                        SL_RAIL_TX_OPTIONS_DEFAULT,
                                        NULL);
  }
  sl_zigbee_af_cli_println("aux_tx:tx_st:0x%04X ch:%u csma:%u", (unsigned int)st, channel, use_csma);
  if (st != SL_RAIL_STATUS_NO_ERROR) {
    sli_rail_mux_aux_cli_observe_tx = 0U;
    sli_rail_mux_aux_cli_suppress_local_fixed_psdu_echo = 0U;
  } else {
    sl_zigbee_af_cli_println("aux_tx:tx_complete_cb_armed");
  }
}

void sl_zigbee_cli_rail_mux_aux_raw_rx_on(sl_cli_command_arg_t *arguments)
{
  (void)arguments;
  sli_rail_mux_aux_cli_rx_print_enabled = 1U;
  sli_rail_mux_aux_cli_suppress_local_fixed_psdu_echo = 0U;
  sl_zigbee_af_cli_println("aux_raw_rx_cb:on");
}

void sl_zigbee_cli_rail_mux_aux_raw_rx_off(sl_cli_command_arg_t *arguments)
{
  (void)arguments;
  sli_rail_mux_aux_cli_rx_print_enabled = 0U;
  sli_rail_mux_aux_cli_suppress_local_fixed_psdu_echo = 0U;
  sl_zigbee_af_cli_println("aux_raw_rx_cb:off");
}

void sl_zigbee_cli_rail_mux_aux_rxdc_phy_select_get(sl_cli_command_arg_t *arguments)
{
  (void)arguments;
#if defined(SL_CATALOG_SL_RAIL_UTIL_IEEE802154_RX_DUTY_CYCLING_PRESENT) \
  && defined(SL_CATALOG_SL_RAIL_UTIL_IEEE802154_FAST_CHANNEL_SWITCHING_PRESENT)
  sl_zigbee_af_cli_println("mux_rxdc_phy_select:%u",
                           sl_rail_mux_get_rx_duty_cycling_phy_select_enabled() ? 1U : 0U);
#else
  sl_zigbee_af_cli_println("mux_rxdc_phy_select:unsupported");
#endif
}

void sl_zigbee_cli_rail_mux_aux_rxdc_phy_select_set(sl_cli_command_arg_t *arguments)
{
  uint8_t enable = sl_cli_get_argument_uint8(arguments, 0);
#if defined(SL_CATALOG_SL_RAIL_UTIL_IEEE802154_RX_DUTY_CYCLING_PRESENT) \
  && defined(SL_CATALOG_SL_RAIL_UTIL_IEEE802154_FAST_CHANNEL_SWITCHING_PRESENT)
  sl_rail_mux_set_rx_duty_cycling_phy_select_enabled(enable != 0U);
  sl_zigbee_af_cli_println("mux_rxdc_phy_select:%u",
                           sl_rail_mux_get_rx_duty_cycling_phy_select_enabled() ? 1U : 0U);
#else
  (void)enable;
  sl_zigbee_af_cli_println("mux_rxdc_phy_select:unsupported");
#endif
}

#endif // SL_CATALOG_CLI_PRESENT
