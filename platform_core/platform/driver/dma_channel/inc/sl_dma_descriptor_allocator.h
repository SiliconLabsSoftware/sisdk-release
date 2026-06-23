/***************************************************************************//**
 * @file
 * @brief DMA Descriptor Allocator API
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

#ifndef SL_DMA_DESCRIPTOR_ALLOCATOR_H
#define SL_DMA_DESCRIPTOR_ALLOCATOR_H

#include <stdbool.h>
#include <stdint.h>
#include "sl_status.h"
#include "sl_device_peripheral.h"

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************//**
 * @addtogroup dma_descriptor_allocator DMA Descriptor Allocator
 * @brief Configurable DMA descriptor allocator abstraction layer.
 * @details
 *  The DMA Descriptor Allocator provides an abstraction layer for allocating
 *  and freeing DMA descriptors. This allows different allocation strategies to
 *  be used depending on the platform (e.g., memory manager for SiSDK, custom
 *  allocators for other platforms like Zephyr).
 *
 *  The allocator is initialized per DMA peripheral and channel, and provides
 *  APIs to allocate and free descriptors. Descriptors can be either regular
 *  or extended depending on the transfer requirements.
 *
 *  @ingroup dma
 ******************************************************************************/

/*******************************************************************************
 *****************************   API PROTOTYPES  ******************************
 ******************************************************************************/

/***************************************************************************//**
 * @brief Initialize the DMA descriptor allocator for a specific DMA peripheral
 *        and channel.
 *
 * @param[in] dma_peripheral DMA peripheral instance.
 * @param[in] channel_nbr    Channel number.
 *
 * @note This function should be called once per DMA peripheral/channel
 *       combination before using the allocator.
 ******************************************************************************/
void sl_dma_descriptor_allocator_init(sl_peripheral_t dma_peripheral,
                                      uint8_t channel_nbr);

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
 * @return SL_STATUS_NULL_POINTER if @p descriptor is NULL.
 ******************************************************************************/
sl_status_t sl_dma_descriptor_allocator_allocate(sl_peripheral_t dma_peripheral,
                                                 uint8_t channel_nbr,
                                                 bool is_extended,
                                                 void **descriptor);

/***************************************************************************//**
 * @brief Free a previously allocated DMA descriptor.
 *
 * @param[in] dma_peripheral DMA peripheral instance.
 * @param[in] channel_nbr    Channel number.
 * @param[in] descriptor     Pointer to descriptor to free.
 ******************************************************************************/
void sl_dma_descriptor_allocator_free(sl_peripheral_t dma_peripheral,
                                      uint8_t channel_nbr,
                                      void *descriptor);

#ifdef __cplusplus
}
#endif

#endif // SL_DMA_DESCRIPTOR_ALLOCATOR_H
