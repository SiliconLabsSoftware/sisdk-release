/***************************************************************************//**
 * @file
 * @brief
 *******************************************************************************
 * # License
 * <b>Copyright 2022 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef RAIL_MUX_RENAME_H
#define RAIL_MUX_RENAME_H

#include PLATFORM_HEADER
#include "sl_rail_mux.h"
#include "coexistence/protocol/ieee802154_uc/coexistence-802154.h"

#define sl_rail_util_ieee802154_config_radio sl_rail_mux_util_ieee802154_config_radio
#define sl_rail_set_state_timing  sl_rail_mux_set_state_timing
#define sl_rail_ieee802154_set_rx_to_enh_ack_tx   sl_rail_mux_ieee802154_set_rx_to_enh_ack_tx
#define sl_rail_config_rx_options   sl_rail_mux_config_rx_options
#define sl_rail_ieee802154_config_2_mbps_rx_channel sl_rail_mux_ieee802154_config_2_mbps_rx_channel
#define sl_rail_set_task_priority   sl_rail_mux_set_task_priority
#define sl_rail_ieee802154_config_2p4_ghz_radio         sl_rail_mux_ieee802154_config_2p4_ghz_radio
#define sl_rail_ieee802154_config_2p4_ghz_radio_ant_div   sl_rail_mux_ieee802154_config_2p4_ghz_radio_ant_div
#define sl_rail_ieee802154_config_2p4_ghz_radio_2_mbps    sl_rail_mux_ieee802154_config_2p4_ghz_radio_2_mbps
#define sl_rail_ieee802154_config_2p4_ghz_radio_fcs_2_mbps   sl_rail_mux_ieee802154_config_2p4_ghz_radio_fcs_2_mbps
#define sl_rail_ieee802154_config_2p4_ghz_radio_fast_channel_switching sl_rail_mux_ieee802154_config_2p4_ghz_radio_fast_channel_switching
#define sl_rail_ieee802154_config_2p4_ghz_radio_rx_duty_cycling sl_rail_mux_ieee802154_config_2p4_ghz_radio_rx_duty_cycling
#define sl_rail_config_events   sl_rail_mux_config_events
#define sl_rail_init   sl_rail_mux_init
#define sl_rail_set_pti_protocol   sl_rail_mux_set_pti_protocol
#define sl_rail_config_channels   sl_rail_mux_config_channels
#define sl_rail_ieee802154_init   sl_rail_mux_ieee802154_init
#define sl_rail_convert_lqi   sl_rail_mux_convert_lqi
#define sl_rail_calibrate   sl_rail_mux_calibrate
#define sl_rail_ieee802154_calibrate_ir_2p4_ghz   sl_rail_mux_ieee802154_calibrate_ir_2p4_ghz
#define sl_rail_get_radio_entropy   sl_rail_mux_get_radio_entropy
#define sl_rail_ieee802154_set_short_address   sl_rail_mux_ieee802154_set_short_address
#define sl_rail_ieee802154_set_long_address   sl_rail_mux_ieee802154_set_long_address
#define sl_rail_ieee802154_set_pan_id   sl_rail_mux_ieee802154_set_pan_id
#define sl_rail_ieee802154_set_pan_coordinator   sl_rail_mux_ieee802154_set_pan_coordinator
#define sl_rail_ieee802154_set_addresses sl_rail_mux_ieee802154_set_addresses
#define sl_rail_is_valid_channel   sl_rail_mux_is_valid_channel
#define sl_rail_get_rssi   sl_rail_mux_get_rssi
#define sl_rail_get_symbol_rate   sl_rail_mux_get_symbol_rate
#define sl_rail_get_bit_rate   sl_rail_mux_get_bit_rate
#define sl_rail_cancel_timer   sl_rail_mux_cancel_timer
#define sl_rail_get_pending_cal   sl_rail_mux_get_pending_cal
#define sl_rail_calibrate_temp   sl_rail_mux_calibrate_temp
#define sl_rail_get_rx_packet_info   sl_rail_mux_get_rx_packet_info
#define sl_rail_get_rx_packet_details   sl_rail_mux_get_rx_packet_details_alt
#define sl_rail_peek_rx_packet   sl_rail_mux_peek_rx_packet
#define sl_rail_ieee802154_get_address   sl_rail_mux_ieee802154_get_address
#define sl_rail_get_rx_incoming_packet_info   sl_rail_mux_get_rx_incoming_packet_info
#define sl_rail_ieee802154_toggle_frame_pending   sl_rail_mux_ieee802154_set_frame_pending
#define sl_rail_get_scheduler_status   sl_rail_mux_get_scheduler_status
#define sl_rail_is_rx_auto_ack_paused sl_rail_mux_is_rx_auto_ack_paused
#define sli_rail_get_tx_power_config   sli_rail_mux_GetTxPowerConfig
#define sl_rail_util_pa_post_init   sl_rail_mux_util_pa_post_init
#define sl_rail_get_pa_mode sl_rail_mux_get_pa_mode
#define sl_rail_config_tx_power   sl_rail_mux_config_tx_power
#define sl_rail_set_tx_power_dbm   sl_rail_mux_set_tx_power_dbm
#define sl_rail_yield_radio   sl_rail_mux_yield_radio
#define sl_rail_get_radio_state   sl_rail_mux_get_radio_state
#define sl_rail_idle   sl_rail_mux_idle
#define sl_rail_start_rx   sl_rail_mux_start_rx
#define sl_rail_set_tx_fifo   sl_rail_mux_set_tx_fifo
#define sl_rail_start_cca_csma_tx   sl_rail_mux_start_cca_csma_tx
#define sl_rail_start_tx  sl_rail_mux_start_tx
#define sl_rail_stop_tx_stream   sl_rail_mux_stop_tx_stream
#define sl_rail_ieee802154_set_promiscuous_mode   sl_rail_mux_ieee802154_set_promiscuous_mode
#define sl_rail_pause_rx_auto_ack   sl_rail_mux_pause_rx_auto_ack
#define sl_rail_set_cca_threshold   sl_rail_mux_set_cca_threshold

#define sl_rail_set_freq_offset sl_rail_mux_set_freq_offset
#define sl_rail_set_timer sl_rail_mux_set_timer

#define sl_rail_ieee802154_is_enabled   sl_rail_mux_ieee802154_is_enabled
#define sl_rail_set_rx_transitions   sl_rail_mux_set_rx_transitions
#define sl_rail_config_cal   sl_rail_mux_config_cal
#define sl_rail_write_tx_fifo   sl_rail_mux_write_tx_fifo
#define sl_rail_read_rx_fifo   sl_rail_mux_read_rx_fifo
#define sl_rail_get_rx_fifo_bytes_available   sl_rail_mux_get_rx_fifo_bytes_available
#define sl_rail_start_scheduled_tx   sl_rail_mux_start_scheduled_tx
#define sl_rail_start_scheduled_cca_csma_tx sl_rail_mux_start_scheduled_cca_csma_tx
#define sl_rail_start_scheduled_rx sl_rail_mux_rail_schedule_rx
#define sl_rail_config_sleep   sl_rail_mux_config_sleep
#define sl_rail_get_rssi_offset sl_rail_mux_get_rssi_offset

#define sl_rail_start_average_rssi   sl_rail_mux_start_average_rssi

#define sl_rail_get_tx_power_dbm   sl_rail_mux_get_tx_power_dbm
#define sli_rail_get_tx_power   sli_rail_mux_GetTxPower

#define sl_rail_ieee802154_write_enh_ack   sl_rail_mux_ieee802154_write_enh_ack

#define sl_rail_release_rx_packet   sl_rail_mux_release_rx_packet

#define sl_rail_hold_rx_packet   sl_rail_mux_hold_rx_packet

#define sl_rail_get_average_rssi   sl_rail_mux_get_average_rssi

#define sl_rail_get_rx_time_sync_word_end   sl_rail_mux_get_rx_time_sync_word_end_alt

#define sl_rail_ieee802154_get_phy_id   sl_rail_mux_ieee802154_get_pti_radio_config

#define sl_rail_ieee802154_enable_early_frame_pending   sl_rail_mux_ieee802154_enable_early_frame_pending

#define sl_rail_set_tx_fifo_threshold     sl_rail_mux_set_tx_fifo_threshold

#define sl_rail_set_next_tx_repeat sl_rail_mux_set_next_tx_repeat

#define sl_rail_get_channel sl_rail_mux_get_channel

#define sl_rail_ieee802154_enable_data_frame_pending sl_rail_mux_ieee802154_enable_data_frame_pending

#define sl_rail_get_tx_packets_remaining sl_rail_mux_get_tx_packets_remaining

#define sl_rail_reset_fifo sl_rail_mux_reset_fifo
#define sl_rail_config_rx_duty_cycle sl_rail_mux_config_rx_duty_cycle
#define sl_rail_enable_rx_duty_cycle sl_rail_mux_enable_rx_duty_cycle
#define sl_rail_get_tx_fifo_space_available sl_rail_mux_get_tx_fifo_space_available
#define sl_rail_ieee802154_accept_frames sl_rail_mux_ieee802154_accept_frames
#define sl_rail_ieee802154_config_2p4_ghz_radio_ant_div_coex sl_rail_mux_ieee802154_config_2p4_ghz_radio_ant_div_coex
#define sl_rail_ieee802154_config_2p4_ghz_radio_ant_div_coex_fem sl_rail_mux_ieee802154_config_2p4_ghz_radio_ant_div_coex_fem
#define sl_rail_ieee802154_config_2p4_ghz_radio_ant_div_fem sl_rail_mux_ieee802154_config_2p4_ghz_radio_ant_div_fem
#define sl_rail_ieee802154_config_2p4_ghz_radio_coex sl_rail_mux_ieee802154_config_2p4_ghz_radio_coex
#define sl_rail_ieee802154_config_2p4_ghz_radio_coex_fem sl_rail_mux_ieee802154_config_2p4_ghz_radio_coex_fem
#define sl_rail_ieee802154_config_2p4_ghz_radio_fem sl_rail_mux_ieee802154_config_2p4_ghz_radio_fem
#define sl_rail_ieee802154_config_cca_mode sl_rail_mux_ieee802154_config_cca_mode
#define sl_rail_ieee802154_config_e_options sl_rail_mux_ieee802154_config_e_options
#define sl_rail_ieee802154_config_g_options sl_rail_mux_ieee802154_config_g_options
#define sl_rail_ieee802154_set_phy_id sl_rail_mux_ieee802154_set_pti_radio_config
#define sl_rail_set_rssi_offset sl_rail_mux_set_rssi_offset
#define sl_rail_start_tx_stream sl_rail_mux_start_tx_stream_alt
#define sl_rail_ieee802154_config_2p4_ghz_radio_1_mbps_fec sl_rail_mux_ieee802154_config_2p4_ghz_radio_1_mbps_fec
#define sl_rail_ieee802154_config_2p4_ghz_radio_fcs_1_mbps_fec sl_rail_mux_ieee802154_config_2p4_ghz_radio_fcs_1_mbps_fec
#define sl_rail_get_rx_time_frame_end sl_rail_mux_get_rx_time_frame_end
#define sl_rail_copy_rx_packet sl_rail_mux_copy_rx_packet
#define sl_rail_config_multi_timer sl_rail_mux_config_multi_timer
#define sl_rail_set_multi_timer sl_rail_mux_set_multi_timer
#define sl_rail_cancel_multi_timer sl_rail_mux_cancel_multi_timer
#define sl_rail_is_multi_timer_running sl_rail_mux_is_multi_timer_running
#define sl_rail_get_time sl_rail_mux_get_time
#define sl_rail_prepare_channel sl_rail_mux_prepare_channel
#define sl_rail_is_next_cca_now sl_rail_mux_is_next_cca_now

#define ATOMIC_SECTION(RETURN_TYPE, yourcode, ...) \
  ({                                               \
    CORE_DECLARE_IRQ_STATE;                        \
    RETURN_TYPE result;                            \
    CORE_ENTER_ATOMIC();                           \
    {                                              \
      result = yourcode(__VA_ARGS__);              \
    }                                              \
    CORE_EXIT_ATOMIC();                            \
    result;                                        \
  })

#define sl_rail_util_coex_set_bool(...)         ATOMIC_SECTION(sl_status_t, sl_rail_util_coex_set_bool, __VA_ARGS__)
#define sl_rail_util_coex_get_options(...)      ATOMIC_SECTION(sl_rail_util_coex_options_t, sl_rail_util_coex_get_options, __VA_ARGS__)
#define sl_rail_util_coex_set_options(...)      ATOMIC_SECTION(sl_status_t, sl_rail_util_coex_set_options, __VA_ARGS__)
#define sl_rail_util_coex_set_enable(...)       ATOMIC_SECTION(sl_status_t, sl_rail_util_coex_set_enable, __VA_ARGS__)
#define sl_rail_util_coex_set_tx_request(...)   ATOMIC_SECTION(sl_status_t, sl_rail_util_coex_set_tx_request, __VA_ARGS__)
#define sl_rail_util_coex_set_rx_request(...)   ATOMIC_SECTION(sl_status_t, sl_rail_util_coex_set_rx_request, __VA_ARGS__)
#define sl_rail_util_coex_set_request_pwm(...)  ATOMIC_SECTION(sl_status_t, sl_rail_util_coex_set_request_pwm, __VA_ARGS__)

#endif //RAIL_MUX_RENAME_H
