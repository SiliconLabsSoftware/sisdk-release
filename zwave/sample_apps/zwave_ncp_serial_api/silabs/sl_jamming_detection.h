/**
 * @file sl_jamming_detection.h
 * @copyright 2026 Silicon Laboratories Inc.
 *
 * @brief RSSI-based jamming detection.
 *
 * This module implements the jamming detection algorithm: sample RSSI per
 * channel every 100 ms over a configurable window (e.g. 150 samples = 15 s),
 * count samples above a configurable RSSI threshold, and mark a channel as
 * jammed when a configurable number of samples in the window are above the threshold.
 *
 */

#ifndef SL_JAMMING_DETECTION_H
#define SL_JAMMING_DETECTION_H

#include <stdint.h>
#include "zpal_radio.h"
#include "zpal_status.h"

#ifdef __cplusplus
extern "C" {
#endif

/** Max number of channels to monitor. */
#define SL_JAMMING_DETECTION_NUM_CHANNELS      ZPAL_RADIO_NUM_CHANNELS_LR_CH_CFG_1_2

/* statistics layout: 0..2 = classic, 3 = LRA, 4 = LRB */
#define SL_JAMMING_DETECTION_NUM_STATS_CHANNELS           (ZPAL_RADIO_NUM_CHANNELS + ZPAL_RADIO_NUM_CHANNELS_LR_CH_CFG3)

/* collection layout: 0..2 = classic, 3 = LRA, 4 = LRB */
#define SL_JAMMING_DETECTION_NUM_COLLECTION_CHANNELS      (SL_JAMMING_DETECTION_NUM_STATS_CHANNELS)

_Static_assert(SL_JAMMING_DETECTION_NUM_CHANNELS == 4, "SL_JAMMING_DETECTION_NUM_CHANNELS should be 4");

_Static_assert(SL_JAMMING_DETECTION_NUM_STATS_CHANNELS == 5, "SL_JAMMING_DETECTION_NUM_STATS_CHANNELS should be 5");
_Static_assert(SL_JAMMING_DETECTION_NUM_COLLECTION_CHANNELS == SL_JAMMING_DETECTION_NUM_STATS_CHANNELS, "collection and stats channel counts must match");

/** One collection snapshot: one RSSI sample per channel. */
typedef struct {
  struct {
    int8_t rssi;  /**< RSSI value for this channel. */
  } samples[SL_JAMMING_DETECTION_NUM_COLLECTION_CHANNELS];
} sl_jamming_detection_collection_t;

/*
 * Callback invoked when RSSI collection is enabled.
 * @param[in] collection  Struct with RSSI samples for all channels.
 * @return ZPAL_STATUS_OK on success, ZPAL_STATUS_FAIL if failure.
 */
typedef zpal_status_t (*sl_jamming_detection_collection_callback_t)(const sl_jamming_detection_collection_t *collection);

/** Statistics for jamming detection. */
typedef struct {
  uint8_t channel_bitmap;  /**< Bitmap: bit i set = channel i is jammed. */
  struct {
    int8_t  rssi_threshold_dbm;       /**< RSSI threshold in dBm for this channel. */
    uint8_t critical_number_of_samples;  /**< number of samples above threshold to trigger jamming detection. */
    uint8_t samples_above_threshold;  /**< Number of samples above threshold in the window. */
  } statistics[SL_JAMMING_DETECTION_NUM_STATS_CHANNELS];
} sl_jamming_detection_statistics_t;

/**
 * @brief Callback invoked when jamming is detected on one or more channels.
 * @param[in] statistics  Struct with channel_bitmap and per-channel statistics (threshold, counts).
 */
typedef zpal_status_t (*sl_jamming_detection_report_callback_t)(const sl_jamming_detection_statistics_t *statistics);

/**
 * @brief Configuration for the jamming detection algorithm.
 *
 * Samples are taken every 100 ms over a fixed window (e.g. 150 samples = 15 s).
 * A channel is reported jammed when at least samples_per_channel samples in the
 * window are above the RSSI threshold.
 */
typedef struct {
  struct {
    int8_t  rssi_threshold_dbm;      /**< RSSI threshold in dBm; samples above this threshold are counted as high. */
    uint8_t critical_number_of_samples;                 /**< Number of samples in the window that triggers jamming event (e.g. 95 or more samples in the 15 s window will be reported as jammed). */
  } settings[SL_JAMMING_DETECTION_NUM_STATS_CHANNELS];
  uint16_t report_interval_sec;    /**< Seconds between periodic jamming reports; 0 disables periodic reporting ([0,20]). */
  sl_jamming_detection_report_callback_t report_callback; /**< Callback invoked when jamming is detected on one or more channels. */
  sl_jamming_detection_collection_callback_t collection_callback; /**< Callback invoked when RSSI collection is ready. */
} sl_jamming_detection_config_t;

/**
 * @brief Initialize the jamming detection module.
 *
 * @param[in] config Configuration (threshold, samples, detection-callback). Must not be NULL.
 * @return ZPAL_STATUS_OK on success, ZPAL_STATUS_INVALID_ARGUMENT if config is NULL or invalid.
 */
zpal_status_t sl_jamming_detection_init(const sl_jamming_detection_config_t *config);

/**
 * @brief Fill a config with default jamming detection values.
 *
 * Call this before modifying only the fields you need (e.g. callback, threshold),
 * then pass the config to sl_jamming_detection_init().
 *
 * @param[out] config  Config to fill. Must not be NULL.
 * @return ZPAL_STATUS_OK on success, ZPAL_STATUS_INVALID_ARGUMENT if config is NULL.
 */
zpal_status_t sl_jamming_detection_default_config(sl_jamming_detection_config_t *config);

/**
 * @brief Enable the jamming detection collection.
 * Use 0 to disable collection.
 *
 * @param[in] periods Duration in periods (100 ms each) to collect samples (0xffff means forever).
 * @return ZPAL_STATUS_OK on success
 */
zpal_status_t sl_jamming_detection_enable_collection(uint16_t periods);

/**
 * @brief Set the report interval in seconds.
 *
 * Use 0 to disable periodic jamming reports (evaluation timing is skipped).
 * Values from 1 to 20 set the interval in seconds; values greater than 20 are invalid.
 *
 * @param[in] interval_sec Interval between reporting jamming detection events (in seconds).
 * @return ZPAL_STATUS_OK on success, ZPAL_STATUS_INVALID_ARGUMENT if invalid argument.
 */
zpal_status_t sl_jamming_detection_set_report_interval_sec(uint16_t interval_sec);

/**
 * @brief Set the configuration for a specific channel.
 *
 * @param[in] logical_channel index.
 * @param[in] threshold  RSSI threshold in dBm.
 * @param[in] critical_number_of_samples  Number of samples above threshold to trigger jamming detection.
 * @return ZPAL_STATUS_OK on success, ZPAL_STATUS_FAIL if failure.
 */
zpal_status_t sl_jamming_detection_set_channel_configuration(uint8_t logical_channel, int8_t threshold, uint8_t critical_number_of_samples);

#ifdef __cplusplus
}
#endif

#endif /* SL_JAMMING_DETECTION_H */
