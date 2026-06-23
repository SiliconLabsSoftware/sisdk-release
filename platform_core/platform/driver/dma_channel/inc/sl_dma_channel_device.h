/***************************************************************************//**
 * @file
 * @brief DMA Channel Driver (Device Specific)
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

#ifndef SL_DMA_CHANNEL_DEVICE_H
#define SL_DMA_CHANNEL_DEVICE_H

#include "em_device.h"
#include "sl_hal_ldma.h"
#include "sl_dma_channel.h"

#ifdef __cplusplus
extern "C" {
#endif

/*******************************************************************************
 ******************************   DEFINES   ************************************
 ******************************************************************************/

#ifdef _LDMA_CH_XCTRL_XFERCNT_MASK
#define SL_DMA_CHANNEL_HAS_EXTENDED_DESCRIPTORS
#endif

/// Maximum transfer unit count per descriptor (compile-time constant)
#if defined(SL_DMA_CHANNEL_HAS_EXTENDED_DESCRIPTORS)
#define SL_DMA_CHANNEL_MAX_XFER_UNIT_COUNT SL_HAL_LDMA_DESCRIPTOR_EXTEND_MAX_XFER_SIZE
#else
#define SL_DMA_CHANNEL_MAX_XFER_UNIT_COUNT SL_HAL_LDMA_DESCRIPTOR_MAX_XFER_SIZE
#endif

/*******************************************************************************
 *****************************   DATA TYPES   *********************************
 ******************************************************************************/

/// Opaque channel transfer descriptor
struct sl_dma_channel_xfer_descriptor {
  uint32_t content[4];  ///< Underlying descriptor storage
#if defined(SL_DMA_CHANNEL_HAS_EXTENDED_DESCRIPTORS)
  uint32_t extended[3];    ///< Extended descriptor storage
#endif
  sl_dma_channel_xfer_descriptor_flags_t flags;      ///< Descriptor flags
};

#ifdef __cplusplus
}
#endif
#endif // SL_DMA_CHANNEL_DEVICE_H
