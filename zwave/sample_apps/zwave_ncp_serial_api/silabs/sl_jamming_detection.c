/*******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of the Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * https://www.silabs.com/about-us/legal/master-software-license-agreement
 * By installing, copying or otherwise using this software, you agree to the
 * terms of the MSLA.
 *
 ******************************************************************************/

/**
 * @file sl_jamming_detection.c
 * @brief Sample application implementation of RSSI-based jamming detection.
 *
 */
#include <stdbool.h>
#include <string.h>
#include "FreeRTOS.h"
#include "task.h"
#include "zpal_log.h"
#include "zpal_radio.h"
#include "zpal_radio_utils.h"
#include "sl_jamming_detection.h"
#include "zw_jamming_detection_config.h"

/** Task stack size in bytes. */
#define SL_JAMMING_DETECTION_TASK_SIZE_BYTES               (256)

/** Task period in milliseconds. */
#define SL_JAMMING_DETECTION_TASK_PERIOD_MS                (100)

/** Buffer size (default value): 15 s at 100 ms = 150 samples. */
#ifndef SL_JAMMING_DETECTION_BUFFER_SIZE
  #define SL_JAMMING_DETECTION_BUFFER_SIZE                 (150)
#endif

/** Time period to wait before evaluating the buffers in seconds. */
#ifndef SL_JAMMING_DEFAULT_DETECTION_EVALUATION_DELAY_SEC
  #define SL_JAMMING_DEFAULT_DETECTION_EVALUATION_DELAY_SEC (5)
#endif

/** User Config Default Value: Trigger count. */
#define SL_JAMMING_DETECTION_DEFAULT_TRIGGER               (95)

/** User Config Default Value: RSSI threshold in dBm. */
#define SL_JAMMING_DETECTION_DEFAULT_RSSI_THRESHOLD_DBM    (-50)

/** Logical Z-Wave channel index for Long Range A */
#define SL_JAMMING_COLLECTION_ZWAVE_LR_A                   (3)

/** Logical Z-Wave channel index for Long Range B */
#define SL_JAMMING_COLLECTION_ZWAVE_LR_B                   (4)

_Static_assert(SL_JAMMING_COLLECTION_ZWAVE_LR_A == 3, "SL_JAMMING_COLLECTION_ZWAVE_LR_A must be 3");

_Static_assert(SL_JAMMING_COLLECTION_ZWAVE_LR_B == 4, "SL_JAMMING_COLLECTION_ZWAVE_LR_B must be 4");

_Static_assert(SL_JAMMING_DETECTION_TASK_SIZE_BYTES >= 256, "SL_JAMMING_DETECTION_TASK_SIZE_BYTES should be greater than or equal to 256");

_Static_assert(SL_JAMMING_DETECTION_TASK_PERIOD_MS == 100, "SL_JAMMING_DETECTION_TASK_PERIOD_MS must be 100 ms");

_Static_assert((SL_JAMMING_DEFAULT_DETECTION_EVALUATION_DELAY_SEC <= 20), "SL_JAMMING_DEFAULT_DETECTION_EVALUATION_DELAY_SEC must be 0-20 sec");

_Static_assert((SL_JAMMING_DETECTION_BUFFER_SIZE >= 150) && (SL_JAMMING_DETECTION_BUFFER_SIZE <= 255), "SL_JAMMING_DETECTION_BUFFER_SIZE must be (150, 255]");

_Static_assert((SL_JAMMING_DETECTION_DEFAULT_TRIGGER > 0) && (SL_JAMMING_DETECTION_DEFAULT_TRIGGER < SL_JAMMING_DETECTION_BUFFER_SIZE), "SL_JAMMING_DETECTION_DEFAULT_TRIGGER must be in (0, SL_JAMMING_DETECTION_BUFFER_SIZE)");

_Static_assert((SL_JAMMING_DETECTION_DEFAULT_RSSI_THRESHOLD_DBM > -127) && (SL_JAMMING_DETECTION_DEFAULT_RSSI_THRESHOLD_DBM <= 0), "SL_JAMMING_DETECTION_DEFAULT_RSSI_THRESHOLD_DBM must be in (-127, 0]");

/****************************************************************************/
/* Private data                                                             */
/****************************************************************************/

/* Structure that will hold the TCB of the task being created. */
static StaticTask_t JammingTaskBuffer;

/* Buffer that the task being created will use as its stack. */
static StackType_t JammingStackBuffer[SL_JAMMING_DETECTION_TASK_SIZE_BYTES];

/** Jamming detection configuration */
static sl_jamming_detection_config_t jamming_detection_config = { 0 };

/** Circular buffer of RSSI samples per channel (last 15 s at 100 ms). */
static int8_t rssi_buffer[SL_JAMMING_DETECTION_NUM_CHANNELS][SL_JAMMING_DETECTION_BUFFER_SIZE];

/** Index of the next sample to write in the circular buffer. */
static uint8_t indexes[SL_JAMMING_DETECTION_NUM_CHANNELS];

/** True once this physical channel has stored at least one above-threshold sample since last clear (distinguishes index 0 empty vs wrapped). */
static bool has_samples[SL_JAMMING_DETECTION_NUM_CHANNELS];

/** Number of physical channels to monitor. */
static uint8_t num_physical_channels = 0;

/** Number of remaining sample collection periods (a period is 100 ms by default; 0xffff means forever). */
static uint16_t collection_duration = 0;

/** Number of periods (100ms-ticks) elapsed since the last jamming state change. (period interval) */
static uint16_t period_counter = 0;

/****************************************************************************/
/* Private Functions                                                        */
/****************************************************************************/

/*
 * @brief Fetch the RSSI value for a given channel.
 *
 * @param[in] channel Channel index.
 * @param[out] rssi Pointer to the RSSI value.
 * @return ZPAL_STATUS_OK if successful, ZPAL_STATUS_INVALID_ARGUMENT if the arguments are invalid.
 */
static zpal_status_t jamming_fetch_rssi(uint8_t physical_channel, int8_t *rssi)
{
  zpal_status_t status = ZPAL_STATUS_FAIL;

  if (NULL == rssi) {
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  if (physical_channel >= num_physical_channels) {
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  status = zpal_radio_get_background_rssi(physical_channel, rssi);

  return status;
}

/**
 * @brief Map physical channel (0..3) index to logical index(0..4)
 * @param[in] physical_channel physical channel index.
 * @return logical index.
 */
static uint8_t jamming_phy_to_logical_channel_index(uint8_t physical_channel)
{
  zpal_radio_protocol_mode_t mode = zpal_radio_get_protocol_mode();
  uint8_t logical_channel = physical_channel;

  switch (mode) {
    case ZPAL_RADIO_PROTOCOL_MODE_4:
      /* MODE_4: two PHY channels; map 0 -> LRA (3), 1 -> LRB (4). */
      if (physical_channel < ZPAL_RADIO_NUM_CHANNELS_LR_CH_CFG3) {
        logical_channel = (uint8_t)(SL_JAMMING_COLLECTION_ZWAVE_LR_A + physical_channel);
      }
      break;

    case ZPAL_RADIO_PROTOCOL_MODE_3:
      if (physical_channel < 3u) {
        logical_channel = physical_channel;
      } else {
        zpal_radio_lr_channel_t primary = zpal_radio_get_primary_long_range_channel();
        if (ZPAL_RADIO_LR_CHANNEL_A == primary) {
          logical_channel = SL_JAMMING_COLLECTION_ZWAVE_LR_A;
        } else {
          logical_channel = SL_JAMMING_COLLECTION_ZWAVE_LR_B;
        }
      }
      break;

    case ZPAL_RADIO_PROTOCOL_MODE_2:
    case ZPAL_RADIO_PROTOCOL_MODE_1:
    default:
      /* Classic channels */
      // logical_channel = physical_channel; /* alredy done in the beggining of the function */
      break;
  }

  return logical_channel;
}

/*
 * @brief Check if a sample is considered as a jamming sample or not.
 * A sample is considered as jamming in any condition:
 * - RSSI value is above jamming threshold.
 * - INVALID value return by hardware.
 * This function only intend to sort RSSI sample. One jamming sample is not enough to detect jamming.
 *
 * @param[in] threshold  RSSI threshold in dBm.
 * @param[in] the RSSI value.
 * @return True if sample is consider as jamming, False otherwise.
 */
static bool jamming_is_jamming_sample(int8_t threshold, int8_t rssi)
{
  if (ZPAL_RADIO_INVALID_RSSI_DBM == rssi) {
    /* Some specific signals can prevent RAIL from measuring the RSSI. Whatever it's a jamming or
       not, it prevents the product from working properly. So consider it as jamming. */
    return true;
  }
  if ( (threshold < rssi) && (rssi <= ZPAL_RADIO_BACKGROUND_RSSI_VALID_MAX) ) {
    /* valid rssi value above jamming threshold is a jamming signal */
    return true;
  }
  return false;
}

/*
 * @brief Fill the buffers with the RSSI value for a given physical channel.
 *
 * @param[in] physical_channel Physical channel index.
 * @param[in] rssi Pointer to the RSSI value.
 * @return ZPAL_STATUS_OK if successful, ZPAL_STATUS_INVALID_ARGUMENT if the arguments are invalid.
 */
static zpal_status_t jamming_store_sample(uint8_t physical_channel, int8_t *rssi)
{
  zpal_status_t status = ZPAL_STATUS_FAIL;

  if (NULL == rssi) {
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  if (physical_channel >= SL_JAMMING_DETECTION_NUM_CHANNELS) {
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  uint8_t logical_channel = jamming_phy_to_logical_channel_index(physical_channel);
  int8_t threshold = jamming_detection_config.settings[logical_channel].rssi_threshold_dbm;
  if (jamming_is_jamming_sample(threshold, *rssi)) {
    uint8_t index = indexes[physical_channel];
    rssi_buffer[physical_channel][index] = *rssi;
    index = (uint8_t)((index + 1u) % SL_JAMMING_DETECTION_BUFFER_SIZE);
    indexes[physical_channel] = index;
    has_samples[physical_channel] = true;
  } else {
    if (has_samples[physical_channel]) {
      indexes[physical_channel] = 0;
      has_samples[physical_channel] = false;
      (void)memset(rssi_buffer[physical_channel], (unsigned char)(int8_t)ZPAL_RADIO_RSSI_NOT_AVAILABLE, sizeof(rssi_buffer[physical_channel]));
    }
  }

  status = ZPAL_STATUS_OK;

  return status;
}

/**
 * @brief Check if the collection is enabled.
 *   Decrement the collection duration by 1 in case of collection is enabled and duration is not set to forever.
 *   Set 0xffff to enable collection forever.
 *   Set 0x0000 to disable collection.
 * @return true if the collection is enabled, false otherwise.
 */
static bool jamming_collection_is_enabled(void)
{
  bool is_enabled = (collection_duration > 0u) || (collection_duration == 0xffffu);

  if (collection_duration > 0u && collection_duration != 0xffffu) {
    collection_duration--;
  }

  return is_enabled;
}

/**
 * @brief Check if the evaluation interval has elapsed.
 *
 * @return true if the evaluation interval has elapsed, false otherwise.
 */
static bool jamming_evaluation_interval_elapsed(void)
{
  bool is_elapsed = false;

  if (0 != jamming_detection_config.report_interval_sec) {
    uint16_t elapsed_ms = (uint16_t)(++period_counter * SL_JAMMING_DETECTION_TASK_PERIOD_MS);
    if (elapsed_ms >= (jamming_detection_config.report_interval_sec * 1000)) {
      period_counter = 0;
      is_elapsed = true;
    }
  }

  return is_elapsed;
}

/**
 * @brief Check if the logical channel is jammed.
 *
 * @param[in] logical_channel Channel index.
 * @param[in] samples Number of samples above the threshold.
 * @return true if samples >= trigger value, false otherwise.
 */
static bool jamming_is_channel_jammed(uint8_t logical_channel, uint8_t samples)
{
  bool is_jammed = false;

  if (samples >= jamming_detection_config.settings[logical_channel].critical_number_of_samples) {
    is_jammed = true;
  }

  return is_jammed;
}

/**
 * @brief Count the number of samples above the threshold.
 * @param[in] physical_channel Channel to count samples for.
 * @return Number of samples above the threshold.
 */
static uint8_t jamming_count_samples_above_threshold(uint8_t physical_channel)
{
  uint8_t samples_above_threshold = 0;
  uint8_t logical_channel = jamming_phy_to_logical_channel_index(physical_channel);
  int8_t threshold = jamming_detection_config.settings[logical_channel].rssi_threshold_dbm;

  for (uint8_t x = 0; x < SL_JAMMING_DETECTION_BUFFER_SIZE; x++) {
    if (ZPAL_RADIO_RSSI_NOT_AVAILABLE == rssi_buffer[physical_channel][x]) {
      // ignore empty value
      continue;
    }
    if ( jamming_is_jamming_sample(threshold, rssi_buffer[physical_channel][x]) ) {
      samples_above_threshold++;
    }
  }

  return samples_above_threshold;
}

/**
 * @brief Map one PHY RSSI sample into the collection snapshot (host layout: logical channels 0–4).
 */
static void jamming_collection_store_rssi(uint8_t physical_channel, int8_t rssi, sl_jamming_detection_collection_t *collection)
{
  if (NULL == collection) {
    return;
  }

  uint8_t logical_channel = jamming_phy_to_logical_channel_index(physical_channel);
  collection->samples[logical_channel].rssi = rssi;
}

/*
 * @brief Main task for jamming detection.
 */
static void jamming_detection_task(void *pvParameters)
{
  (void)pvParameters;
  uint8_t previous_jamming_bitmap = 0;
  bool is_collection_enabled = false;
  zpal_status_t status = ZPAL_STATUS_FAIL;
  sl_jamming_detection_collection_t collection = { 0 };

  num_physical_channels = zpal_radio_get_num_phy_channels(zpal_radio_get_protocol_mode());
  ZPAL_LOG_INFO(ZPAL_LOG_APP_JAMMING, "Number of channels : %u\n", num_physical_channels);

  for (;;) {
    vTaskDelay(pdMS_TO_TICKS(SL_JAMMING_DETECTION_TASK_PERIOD_MS));

    is_collection_enabled = jamming_collection_is_enabled();

    if (is_collection_enabled) {
      /* Initialize the collection to invalid RSSI. */
      for (uint8_t i = 0; i < SL_JAMMING_DETECTION_NUM_COLLECTION_CHANNELS; i++) {
        collection.samples[i].rssi = ZPAL_RADIO_RSSI_NOT_AVAILABLE;
      }
    }

    /* Step 1.1: Fetch RSSI and fill the buffers */
    for (uint8_t physical_channel = 0; physical_channel < num_physical_channels; physical_channel++) {
      int8_t rssi = ZPAL_RADIO_RSSI_NOT_AVAILABLE;
      status = jamming_fetch_rssi(physical_channel, &rssi);
      if ((ZPAL_STATUS_OK == status) || (ZPAL_STATUS_BUSY == status)) {
        /* Store samples even if they are invalid (busy). Invalid samples may be caused by jamming. */
        status = jamming_store_sample(physical_channel, &rssi);
        if (ZPAL_STATUS_OK != status) {
          ZPAL_LOG_ERROR(ZPAL_LOG_APP_JAMMING, "1. RSSI[%d] : fill failed with status %d\n", physical_channel, status);
        }
      } else {
        ZPAL_LOG_ERROR(ZPAL_LOG_APP_JAMMING, "1. RSSI[%d] : fetch failed with status %d\n", physical_channel, status);
      }

      /* Step 1.2: Store the RSSI in the collection (if enabled) */
      if (is_collection_enabled) {
        jamming_collection_store_rssi(physical_channel, rssi, &collection);
      }
    }

    /* Step 2:
       - case 1: Collect and send the collection to the user callback if enabled.
       - case 2: Evaluate buffers every task period; report immediately whenever channel_bitmap changes
         (any channel jams, any channel clears, or multiple channels change).
       - case 3: While jamming persists, invoke the callback every report_interval_sec. */
    if (is_collection_enabled) {
      if (NULL != jamming_detection_config.collection_callback) {
        status = jamming_detection_config.collection_callback(&collection);
      }
    } else {
      sl_jamming_detection_statistics_t report = { 0 };
      for (uint8_t physical_channel = 0; physical_channel < num_physical_channels; physical_channel++) {
        uint8_t logical_channel = jamming_phy_to_logical_channel_index(physical_channel);
        /* 2.1 Count the number of samples above the threshold (RSSI buffer is per PHY) */
        uint8_t samples_above_threshold = jamming_count_samples_above_threshold(physical_channel);
        ZPAL_LOG_DEBUG(ZPAL_LOG_APP_JAMMING, "2.%d physical_channel[%d] logical_channel[%d]: %u/%u above threshold\n", (physical_channel + 1), physical_channel, logical_channel, (unsigned)samples_above_threshold, (unsigned)SL_JAMMING_DETECTION_BUFFER_SIZE);

        report.statistics[logical_channel].rssi_threshold_dbm         = jamming_detection_config.settings[logical_channel].rssi_threshold_dbm;
        report.statistics[logical_channel].critical_number_of_samples = jamming_detection_config.settings[logical_channel].critical_number_of_samples;
        report.statistics[logical_channel].samples_above_threshold    = samples_above_threshold;

        /* 2.2 Jammed if number of samples above threshold >= trigger count (thresholds are per logical_channel channel) */
        if (jamming_is_channel_jammed(logical_channel, samples_above_threshold)) {
          report.channel_bitmap |= (uint8_t)(1u << logical_channel);
        }
      }

      /* Immediate report on any jamming bitmap change (per-channel or combined). */
      bool jamming_state_changed = (report.channel_bitmap != previous_jamming_bitmap);
      if (jamming_state_changed) {
        if (NULL != jamming_detection_config.report_callback) {
          status = jamming_detection_config.report_callback(&report);
          ZPAL_LOG_DEBUG(ZPAL_LOG_APP_JAMMING, "3. Callback invoked, jamming state changed (%s)\n", (status == ZPAL_STATUS_OK) ? "success" : "failure");
        }

        /* we need to reset the jamming evaluation interval at every jamming state change */
        period_counter = 0u;
      }

      /* Periodic reports while jamming continues (unchanged from last evaluation). */
      bool period_elapsed = jamming_evaluation_interval_elapsed();
      if (period_elapsed && !jamming_state_changed && (report.channel_bitmap != 0u)) {
        if (NULL != jamming_detection_config.report_callback) {
          status = jamming_detection_config.report_callback(&report);
          ZPAL_LOG_DEBUG(ZPAL_LOG_APP_JAMMING, "3. Callback invoked, periodic (%s)\n", (status == ZPAL_STATUS_OK) ? "success" : "failure");
        }
      }

      previous_jamming_bitmap = report.channel_bitmap;
    }
  } /* end of for(;;) */
}

/****************************************************************************/
/* public functions                                                         */
/****************************************************************************/
zpal_status_t sl_jamming_detection_init(const sl_jamming_detection_config_t *user_config)
{
  zpal_status_t status = ZPAL_STATUS_FAIL;

  if (user_config == NULL) {
    ZPAL_LOG_ERROR(ZPAL_LOG_APP_JAMMING, "User config is NULL\n");
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  if (user_config->report_interval_sec > 20) {
    ZPAL_LOG_ERROR(ZPAL_LOG_APP_JAMMING, "Report interval should be [0,20] seconds\n");
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  if (NULL == user_config->report_callback) {
    ZPAL_LOG_ERROR(ZPAL_LOG_APP_JAMMING, "Report callback is NULL\n");
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  if (NULL == user_config->collection_callback) {
    ZPAL_LOG_ERROR(ZPAL_LOG_APP_JAMMING, "Collection callback is NULL\n");
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  for (uint8_t logical_channel = 0; logical_channel < SL_JAMMING_DETECTION_NUM_STATS_CHANNELS; logical_channel++) {
    if (user_config->settings[logical_channel].critical_number_of_samples == 0 || user_config->settings[logical_channel].critical_number_of_samples > SL_JAMMING_DETECTION_BUFFER_SIZE) {
      ZPAL_LOG_ERROR(ZPAL_LOG_APP_JAMMING, "Logical channel %d critical number of samples is invalid\n", logical_channel);
      return ZPAL_STATUS_INVALID_ARGUMENT;
    }

    if ((user_config->settings[logical_channel].rssi_threshold_dbm <= ZPAL_RADIO_INVALID_RSSI_DBM) || (user_config->settings[logical_channel].rssi_threshold_dbm > 0)) {
      ZPAL_LOG_ERROR(ZPAL_LOG_APP_JAMMING, "Logical channel %d RSSI threshold is invalid (must be -127..0 dBm)\n", logical_channel);
      return ZPAL_STATUS_INVALID_ARGUMENT;
    }
  }

  (void)memset(indexes, 0, sizeof(indexes));
  (void)memset(has_samples, 0, sizeof(has_samples));
  (void)memset(rssi_buffer, (unsigned char)(int8_t)ZPAL_RADIO_RSSI_NOT_AVAILABLE, sizeof(rssi_buffer));

  /* Copy user configuration values */
  jamming_detection_config = *user_config;

  __attribute__((unused)) TaskHandle_t xHandle = xTaskCreateStatic(
    (TaskFunction_t)&jamming_detection_task,  // pvTaskCode
    "jamming_det",                            // pcName
    (uint16_t)SL_JAMMING_DETECTION_TASK_SIZE_BYTES, // usStackDepth
    NULL,                                     // pvParameters
    10,                                       // uxPriority
    JammingStackBuffer,                       // pxStackBuffer
    &JammingTaskBuffer                        // pxTaskBuffer
    );

  if (NULL != xHandle) {
    status = ZPAL_STATUS_OK;
  }

  return status;
}

zpal_status_t sl_jamming_detection_default_config(sl_jamming_detection_config_t *user_config)
{
  zpal_status_t status = ZPAL_STATUS_FAIL;

  if (NULL == user_config) {
    status = ZPAL_STATUS_INVALID_ARGUMENT;
  } else {
    for (uint8_t logical_channel = 0; logical_channel < SL_JAMMING_DETECTION_NUM_STATS_CHANNELS; logical_channel++) {
      user_config->settings[logical_channel].rssi_threshold_dbm = SL_JAMMING_DETECTION_DEFAULT_RSSI_THRESHOLD_DBM;
      user_config->settings[logical_channel].critical_number_of_samples = SL_JAMMING_DETECTION_DEFAULT_TRIGGER;
    }

    user_config->report_interval_sec = SL_JAMMING_DEFAULT_DETECTION_EVALUATION_DELAY_SEC;
    user_config->report_callback = NULL;
    user_config->collection_callback = NULL;
    status = ZPAL_STATUS_OK;
  }

  return status;
}

zpal_status_t sl_jamming_detection_enable_collection(uint16_t periods)
{
  collection_duration = periods;

  return ZPAL_STATUS_OK;
}

zpal_status_t sl_jamming_detection_set_report_interval_sec(uint16_t interval_sec)
{
  zpal_status_t status = ZPAL_STATUS_FAIL;

  if (interval_sec > 20) {
    status = ZPAL_STATUS_INVALID_ARGUMENT;
  } else {
    jamming_detection_config.report_interval_sec = interval_sec;
    status = ZPAL_STATUS_OK;
  }

  return status;
}

zpal_status_t sl_jamming_detection_set_channel_configuration(uint8_t logical_channel, int8_t threshold, uint8_t critical_number_of_samples)
{
  zpal_status_t status = ZPAL_STATUS_FAIL;

  if (logical_channel >= SL_JAMMING_DETECTION_NUM_STATS_CHANNELS) {
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  if (critical_number_of_samples == 0 || critical_number_of_samples > SL_JAMMING_DETECTION_BUFFER_SIZE) {
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  jamming_detection_config.settings[logical_channel].rssi_threshold_dbm = threshold;
  jamming_detection_config.settings[logical_channel].critical_number_of_samples = critical_number_of_samples;
  status = ZPAL_STATUS_OK;

  return status;
}
