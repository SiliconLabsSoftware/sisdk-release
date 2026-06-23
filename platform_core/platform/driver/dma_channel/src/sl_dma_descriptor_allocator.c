/***************************************************************************//**
 * @file
 * @brief DMA Descriptor Allocator Implementation
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
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/

#include "sl_dma_descriptor_allocator.h"
#include "sl_assert.h"
#include "sl_memory_manager.h"
#include "sl_dma_channel_device.h"

#include <stddef.h>

/***************************************************************************//**
 * @brief Initialize the DMA descriptor allocator for a specific DMA peripheral
 *        and channel.
 *
 * @param[in] dma_peripheral DMA peripheral instance.
 * @param[in] channel_nbr    Channel number.
 ******************************************************************************/
void sl_dma_descriptor_allocator_init(sl_peripheral_t dma_peripheral,
                                      uint8_t channel_nbr)
{
  (void)dma_peripheral;
  (void)channel_nbr;
  // Memory manager does not require per-channel initialization
}

/***************************************************************************//**
 * @brief Allocate a DMA descriptor.
 *
 * @param[in]  dma_peripheral DMA peripheral instance.
 * @param[in]  channel_nbr    Channel number.
 * @param[in]  is_extended    True if extended descriptor is needed, false for
 *                            regular descriptor.
 * @param[out] descriptor     Pointer to allocated descriptor. Set to NULL on
 *                            allocation failure.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 ******************************************************************************/
sl_status_t sl_dma_descriptor_allocator_allocate(sl_peripheral_t dma_peripheral,
                                                 uint8_t channel_nbr,
                                                 bool is_extended,
                                                 void **descriptor)
{
  EFM_ASSERT(descriptor != NULL);
  (void)dma_peripheral;
  (void)channel_nbr;
  (void)is_extended;

  // Allocate using short-term allocation as required
  sl_status_t status = sl_memory_calloc(1,
                                        sizeof(sl_dma_channel_xfer_descriptor_t),
                                        BLOCK_TYPE_SHORT_TERM,
                                        descriptor);

  if (status != SL_STATUS_OK) {
    *descriptor = NULL;
    return SL_STATUS_ALLOCATION_FAILED;
  }

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief Free a previously allocated DMA descriptor.
 *
 * @param[in] dma_peripheral DMA peripheral instance.
 * @param[in] channel_nbr    Channel number.
 * @param[in] descriptor     Pointer to descriptor to free.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
void sl_dma_descriptor_allocator_free(sl_peripheral_t dma_peripheral,
                                      uint8_t channel_nbr,
                                      void *descriptor)
{
  (void)dma_peripheral;
  (void)channel_nbr;

  sl_free(descriptor);
}
