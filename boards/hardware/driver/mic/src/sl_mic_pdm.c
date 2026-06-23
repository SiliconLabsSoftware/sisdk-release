/***************************************************************************//**
 * @file
 * @brief PDM microphone driver
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
#include <stddef.h>
#include <stdint.h>
#include <math.h>
#include "sl_clock_manager.h"
#include "sl_device_clock.h"
#include "sl_dma_manager.h"
#include "sl_hal_ldma.h"
#include "sl_hal_pdm.h"
#include "sl_hal_gpio.h"
#include "sl_gpio.h"
#include "sl_mic.h"
#include "sl_mic_pdm_config.h"
#include "sl_sleeptimer.h"
#include "sl_device_peripheral.h"

#if (defined(SL_CATALOG_POWER_MANAGER_PRESENT))
#include "sl_power_manager.h"
#endif

static bool dma_complete(uint32_t channel, uint32_t sequence_no, void *user_param);

// Local variables
static sl_mic_buffer_ready_callback_t buffer_ready_callback = NULL;
static int16_t *sample_buffer;                // Pointer to current sample buffer
static int16_t  *streaming_buffer[2];         // Buffers used to perform ping-pong operation
static uint32_t sample_index;                 // Current sample index of sample buffer
static uint32_t sample_count;                 // Number of samples to collect
static volatile bool reading_samples_to_buffer; // Flag to show whether buffer is currently filling with samples
static volatile bool streaming_in_progress;   // Flag to show if driver is running in streaming mode
static bool mic_running;                      // Flag to show if mic is running
static volatile bool mic_ready;               // Flag to show if is ready to read samples
static bool initialized;                      // Flag to show if mic is initialized
static uint8_t num_channels;                  // Number of channels
static uint32_t discard_buffer;               // DMA discard pile

#define MIC_PDM_MAX_XFER  (SL_HAL_LDMA_DESCRIPTOR_MAX_XFER_SIZE)

static sl_dma_handle_t *dma_handle;
static uint8_t dma_channel_id;
static volatile uint32_t dma_sequence_no;

static const sl_hal_ldma_transfer_init_t dma_transfer_cfg =
  SL_HAL_LDMA_TRANSFER_CFG_PERIPHERAL(SL_HAL_LDMA_PERIPHERAL_SIGNAL_PDM_RXDATAV);

static sl_hal_ldma_descriptor_t dma_descriptor[2] = {
  SL_HAL_LDMA_DESCRIPTOR_LINKREL_P2M(SL_HAL_LDMA_CTRL_SIZE_WORD, &PDM->RXDATA, &discard_buffer, (MIC_PDM_MAX_XFER - 1), 1),
  SL_HAL_LDMA_DESCRIPTOR_LINKREL_P2M(SL_HAL_LDMA_CTRL_SIZE_WORD, &PDM->RXDATA, &discard_buffer, (MIC_PDM_MAX_XFER - 1), -1)
};

static sl_sleeptimer_timer_handle_t mic_wake_up_timer;

/** @cond DO_NOT_INCLUDE_WITH_DOXYGEN */
static void pdm_dma_irq_cb(void)
{
  (void)dma_complete((uint32_t)dma_channel_id, dma_sequence_no++, NULL);
}
/** @endcond */

/***************************************************************************//**
 * @brief Callback function for sleeptimer
 ******************************************************************************/
void timeout_callback(sl_sleeptimer_timer_handle_t *handle, void *data)
{
  (void)handle;
  (void)data;
  mic_ready = true;
}
/***************************************************************************//**
 *    Initializes the microphone
 ******************************************************************************/
sl_status_t sl_mic_init(uint32_t sample_rate, uint8_t n_channels)
{
  sl_status_t status;
  sl_gpio_t mic_pdm_dat0_gpio = {
    .port = SL_MIC_PDM_DAT0_PORT,
    .pin = SL_MIC_PDM_DAT0_PIN,
  };
  sl_gpio_t mic_pdm_clk_gpio = {
    .port = SL_MIC_PDM_CLK_PORT,
    .pin = SL_MIC_PDM_CLK_PIN,
  };

  if (n_channels < 1 || n_channels > 2) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  /* Enable clocks */
  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_GPIO);
  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_PDM);

  /* Setup GPIO pins */
  sl_gpio_set_pin_mode(&mic_pdm_dat0_gpio, SL_GPIO_MODE_INPUT, 0);
  sl_gpio_set_pin_mode(&mic_pdm_clk_gpio, SL_GPIO_MODE_PUSH_PULL, 0);

  // Set fast slew rate on PDM mic CLK and DATA pins
  sl_hal_gpio_set_slew_rate(&mic_pdm_dat0_gpio, 0x7);
  sl_hal_gpio_set_slew_rate_alternate(SL_MIC_PDM_DAT0_PORT, 0x7);

  /* Configure and enable clock and data routing locations */
#ifdef _SILICON_LABS_32B_SERIES_2
  GPIO->PDMROUTE.ROUTEEN |= GPIO_PDM_ROUTEEN_CLKPEN;
  GPIO->PDMROUTE.DAT0ROUTE |= (SL_MIC_PDM_DAT0_PORT << _GPIO_PDM_DAT0ROUTE_PORT_SHIFT) | (SL_MIC_PDM_DAT0_PIN << _GPIO_PDM_DAT0ROUTE_PIN_SHIFT);
  GPIO->PDMROUTE.CLKROUTE |= (SL_MIC_PDM_CLK_PORT << _GPIO_PDM_CLKROUTE_PORT_SHIFT) | (SL_MIC_PDM_CLK_PIN << _GPIO_PDM_CLKROUTE_PIN_SHIFT);
#else
  PDM->ROUTELOC0 = (PDM->ROUTELOC0 & ~_PDM_ROUTELOC0_DAT0LOC_MASK)
                   | (SL_MIC_PDM_DAT0_LOC << _PDM_ROUTELOC0_DAT0LOC_SHIFT);
  PDM->ROUTELOC1 = SL_MIC_PDM_CLK_LOC << _PDM_ROUTELOC1_CLKLOC_SHIFT;
  PDM->ROUTEPEN |= PDM_ROUTEPEN_CLKPEN | PDM_ROUTEPEN_DAT0PEN;
#endif

  uint8_t dsr = SL_MIC_PDM_DSR;

  if (dsr < 3 || dsr > 73) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  // Calculate gain (shift value) based on DSR and filter order
  uint8_t gain = 31 - (1 + (uint32_t)(log10f(pow(dsr, 5)) / log10f(2)));

  // Calculate necessary prescaler based on desired sample rate and DSR
  uint32_t clock_freq;
  sl_clock_branch_t clock_branch;

  clock_branch = sl_device_peripheral_get_clock_branch(SL_PERIPHERAL_PDM);
  sl_clock_manager_get_clock_branch_frequency(clock_branch, &clock_freq);
  uint32_t prescaler_val = (clock_freq / (sample_rate * dsr)) - 1;

  if (prescaler_val > 1024) {
    return SL_STATUS_FAIL;
  }

  // Initialize the PDM
  sl_hal_pdm_init_t init = SL_HAL_PDM_INIT_DEFAULT;
  init.clk_prescaler = prescaler_val;
  init.down_sampling_rate = dsr;
  init.gain = gain;

  if (n_channels == 1) {
    // Right-align the 16-bit sample in FIFO
    init.data_format = SL_HAL_PDM_DATA_FORMAT_RIGHT_16;
    init.ch0ch1_stereo_enable = false;
    init.number_channels = SL_HAL_PDM_NUMBER_OF_CHANNELS_ONE;
  } else if (n_channels == 2) {
    // Pack two 16-bit samples in one 32-bit FIFO entry
    init.data_format = SL_HAL_PDM_DATA_FORMAT_DOUBLE_16;
    init.ch0ch1_stereo_enable = true;
    init.number_channels = SL_HAL_PDM_NUMBER_OF_CHANNELS_TWO;
  }

  sl_hal_pdm_init(PDM, &init);

  // Setup DMA — DMA Manager
  status = sl_dma_manager_get_default_handle(&dma_handle);
  if (status != SL_STATUS_OK) {
    return SL_STATUS_FAIL;
  }
  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_LDMAXBAR0);
  status = sl_dma_manager_allocate_channel(dma_handle, &dma_channel_id);
  if (status != SL_STATUS_OK) {
    return SL_STATUS_FAIL;
  }

  dma_sequence_no = 0;
  (void)sl_dma_manager_register_channel_irq_callback(dma_handle, dma_channel_id, pdm_dma_irq_cb);

  dma_descriptor[0].xfer.dst_inc  = SL_HAL_LDMA_CTRL_DST_INC_NONE;
  dma_descriptor[0].xfer.size     = SL_HAL_LDMA_CTRL_SIZE_WORD;
  dma_descriptor[0].xfer.done_ifs = 1;  /* Generate interrupt on completion (ping-pong) */
  dma_descriptor[1].xfer.dst_inc  = SL_HAL_LDMA_CTRL_DST_INC_NONE;
  dma_descriptor[1].xfer.size     = SL_HAL_LDMA_CTRL_SIZE_WORD;
  dma_descriptor[1].xfer.done_ifs = 1;

  if (n_channels == 1) {
    dma_descriptor[0].xfer.size = SL_HAL_LDMA_CTRL_SIZE_HALF;
    dma_descriptor[1].xfer.size = SL_HAL_LDMA_CTRL_SIZE_HALF;
  }

#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
  //Add EM1 request to use LDMA
  sl_power_manager_add_em_requirement(SL_POWER_MANAGER_EM1);
#endif

  reading_samples_to_buffer = false;
  streaming_in_progress = false;
  num_channels = n_channels;
  initialized = true;
  mic_running = false;

  return SL_STATUS_OK;
}

/***************************************************************************//**
 *    Read samples from the microphone into a buffer
 ******************************************************************************/
sl_status_t sl_mic_get_n_samples(void *buffer, uint32_t n_frames)
{
  if (!initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if (reading_samples_to_buffer || streaming_in_progress) {
    return SL_STATUS_INVALID_STATE;
  }

  if (!mic_running) {
    sl_mic_start();
  }

  while (!mic_ready) {
    // Wait until mic is ready
  }

  sample_buffer = (int16_t *)buffer;
  sample_count = n_frames;
  sample_index = 0;
  reading_samples_to_buffer = true;

  return SL_STATUS_OK;
}

/***************************************************************************//**
 *    Start streaming
 ******************************************************************************/
sl_status_t sl_mic_start_streaming(void *buffer, uint32_t n_frames, sl_mic_buffer_ready_callback_t callback)
{
  if (!initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if (reading_samples_to_buffer || streaming_in_progress) {
    return SL_STATUS_INVALID_STATE;
  }

  if (n_frames > MIC_PDM_MAX_XFER) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  if (!mic_running) {
    sl_mic_start();
  }

  while (!mic_ready) {
    // Wait until mic is ready
  }

  sample_count = n_frames;
  streaming_buffer[0] = (int16_t *)buffer;
  streaming_buffer[1] = &(((int16_t *)buffer)[n_frames * num_channels]);
  buffer_ready_callback = callback;
  streaming_in_progress = true;

  return SL_STATUS_OK;
}

/***************************************************************************//**
 *    De-initialize the microphone
 ******************************************************************************/
sl_status_t sl_mic_deinit(void)
{
  /* Stop sampling */
  sl_mic_stop();

  // DE-initialize the PDM peripheral
  sl_hal_pdm_stop(PDM);
  sl_hal_pdm_clear(PDM);
  sl_hal_pdm_fifo_flush(PDM);
  sl_hal_pdm_reset(PDM);

  sl_gpio_t mic_pdm_dat0_gpio = {
    .port = SL_MIC_PDM_DAT0_PORT,
    .pin = SL_MIC_PDM_DAT0_PIN,
  };
  sl_gpio_t mic_pdm_clk_gpio = {
    .port = SL_MIC_PDM_CLK_PORT,
    .pin = SL_MIC_PDM_CLK_PIN,
  };

  sl_gpio_set_pin_mode(&mic_pdm_clk_gpio, SL_GPIO_MODE_DISABLED, 0);
  sl_gpio_set_pin_mode(&mic_pdm_dat0_gpio, SL_GPIO_MODE_DISABLED, 0);

  /* Free resources */
  sl_dma_manager_free_channel(dma_handle, dma_channel_id);

#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
  //Remove EM1 request
  sl_power_manager_remove_em_requirement(SL_POWER_MANAGER_EM1);
#endif

  mic_running = false;
  initialized = false;

  return SL_STATUS_OK;
}

/***************************************************************************//**
 *    Starts the microphone
 ******************************************************************************/
sl_status_t sl_mic_start(void)
{
  if (!initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if (mic_running) {
    return SL_STATUS_INVALID_STATE;
  }

  // Clear and start the PDM filter
  sl_hal_pdm_clear(PDM);
  sl_hal_pdm_fifo_flush(PDM);
  sl_hal_pdm_start(PDM);

  // Reset descriptors, drop the first 4096 samples
  dma_descriptor[0].xfer.dst_inc   = SL_HAL_LDMA_CTRL_DST_INC_NONE;
  dma_descriptor[0].xfer.xfer_count = (MIC_PDM_MAX_XFER - 1);
  dma_descriptor[0].xfer.dst_addr  = (uint32_t)&discard_buffer;
  dma_descriptor[1].xfer.dst_inc   = SL_HAL_LDMA_CTRL_DST_INC_NONE;
  dma_descriptor[1].xfer.xfer_count = (MIC_PDM_MAX_XFER - 1);
  dma_descriptor[1].xfer.dst_addr  = (uint32_t)&discard_buffer;

  // Start DMA
  sl_dma_manager_register_channel_irq_callback(dma_handle, dma_channel_id, pdm_dma_irq_cb);
  sl_hal_ldma_init_transfer(LDMA0, dma_channel_id, &dma_transfer_cfg, &dma_descriptor[0]);
  sl_hal_ldma_enable_interrupts(LDMA0, 1UL << dma_channel_id);
  sl_hal_ldma_start_transfer(LDMA0, dma_channel_id);

  // Start microphone wake-up timer
  sl_sleeptimer_start_timer_ms(&mic_wake_up_timer, 15, timeout_callback, NULL, 0, 0);

  mic_running = true;

  return SL_STATUS_OK;
}

/***************************************************************************//**
 *    Stops the microphone
 ******************************************************************************/
sl_status_t sl_mic_stop(void)
{
  if (!mic_running) {
    return SL_STATUS_INVALID_STATE;
  }

  sl_hal_ldma_stop_transfer(LDMA0, dma_channel_id);

  // Stop the PDM filter
  sl_hal_pdm_stop(PDM);

  while ((sl_hal_pdm_get_status(PDM) & PDM_STATUS_ACT) == 1U) {
    // Wait until PDM is no longer running
  }

  mic_running = false;
  mic_ready = false;
  reading_samples_to_buffer = false;
  streaming_in_progress = false;

  return SL_STATUS_OK;
}

/***************************************************************************//**
 *    Checks if the sample buffer is ready
 ******************************************************************************/
bool sl_mic_sample_buffer_ready(void)
{
  return (!reading_samples_to_buffer);
}

/***************************************************************************//**
 *    Calculates the dBSPL value for a channel from a sample buffer
 ******************************************************************************/
sl_status_t sl_mic_calculate_sound_level(float *sound_level, const int16_t *buffer, uint32_t n_frames, uint8_t channel)
{
  float sample;
  float power;
  float mean;
  uint32_t i;

  if (channel >= num_channels) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  // Calculate mean
  mean = 0.0f;
  for ( i = channel; i < (n_frames * num_channels); i += num_channels) {
    mean += (float) buffer[i];
  }
  mean = mean / (float) n_frames;

  // Calculate variance
  power = 0;
  for ( i = channel; i < (n_frames * num_channels); i += num_channels) {
    sample = (((float)buffer[i] - mean) / 32767.0f);
    power += sample * sample;
  }
  power = power / (float)n_frames;

  // Convert to dBSPL
  *sound_level = 10.0f * log10f(power) + 120;
  
  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief
 *  DMA transfer completion (ping-pong) handler.
 *
 * @details
 *  Called when the DMA complete interrupt fired.
 *
 * @param[in] channel
 *  The DMA channel number.
 *
 * @param[in] sequenceNo
 *  The number of times the callback was called. Useful on long chains of
 *  linked transfers or on endless ping-pong type transfers.
 *
 * @param[in] userParam
 *  Optional user parameter supplied on DMA invocation.
 *
 * @return
 *   When doing ping-pong transfers, return true to continue or false to
 *   stop transfers.
 ******************************************************************************/
static bool dma_complete(uint32_t channel,
                         uint32_t sequenceNo,
                         void *userParam)
{
  (void)channel;
  (void)userParam;

  sl_hal_ldma_descriptor_t *next_desc;

  if (reading_samples_to_buffer) {
    if (sequenceNo & 0x01) {
      next_desc = &dma_descriptor[0];
    } else {
      next_desc = &dma_descriptor[1];
    }

    if (sample_index < sample_count) {
      next_desc->xfer.dst_inc   = SL_HAL_LDMA_CTRL_DST_INC_ONE;
      next_desc->xfer.dst_addr  = (uint32_t)&sample_buffer[sample_index];

      if ((sample_count - sample_index) > MIC_PDM_MAX_XFER) {
        next_desc->xfer.xfer_count = (MIC_PDM_MAX_XFER - 1);
        sample_index += MIC_PDM_MAX_XFER;
      } else {
        next_desc->xfer.xfer_count = (sample_count - sample_index) - 1;
        sample_index += (sample_count - sample_index);
      }
    } else {
      next_desc->xfer.dst_inc   = SL_HAL_LDMA_CTRL_DST_INC_NONE;
      next_desc->xfer.xfer_count = (MIC_PDM_MAX_XFER - 1);
      next_desc->xfer.dst_addr  = (uint32_t)&discard_buffer;
    }
    if ( (dma_descriptor[0].xfer.dst_inc == SL_HAL_LDMA_CTRL_DST_INC_NONE)
         && (dma_descriptor[1].xfer.dst_inc == SL_HAL_LDMA_CTRL_DST_INC_NONE) ) {
      reading_samples_to_buffer = false;
      sl_mic_stop();
    }
  } else if (streaming_in_progress) {
    uint32_t idx_next = 1 - (sequenceNo % 2);

    if (dma_descriptor[idx_next].xfer.dst_inc == SL_HAL_LDMA_CTRL_DST_INC_NONE) {
      // Initialize descriptor for streaming mode
      dma_descriptor[idx_next].xfer.dst_inc   = SL_HAL_LDMA_CTRL_DST_INC_ONE;
      dma_descriptor[idx_next].xfer.xfer_count = sample_count - 1;
      dma_descriptor[idx_next].xfer.dst_addr  = (uint32_t)streaming_buffer[idx_next];
    } else {
      // Buffer ready
      if (buffer_ready_callback) {
        buffer_ready_callback(streaming_buffer[idx_next], sample_count);
      }
    }
  }

  return true;
}