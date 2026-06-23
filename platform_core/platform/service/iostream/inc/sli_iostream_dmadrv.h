/***************************************************************************//**
 * @file
 * @brief DMADRV API definition.
 *******************************************************************************
 * # License
 * <b>Copyright 2018 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef __SILICON_LABS_IOSTREAM_DMADRV_H__
#define __SILICON_LABS_IOSTREAM_DMADRV_H__

#include "em_device.h"

#include "sl_device_dma.h"
#include "sl_hal_ldma.h"
#include "sl_status.h"

#include "sl_code_classification.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef bool (*sl_iostream_dmadrv_callback_t)(unsigned int channel,
                                  unsigned int sequenceNo,
                                  void *userParam);

sl_status_t sli_iostream_dmadrv_allocate_channel(unsigned int *channelId);
sl_status_t sli_iostream_dmadrv_init(void);
sl_status_t sli_iostream_dmadrv_deinit(void);
sl_status_t sli_iostream_dmadrv_free_channel(unsigned int channelId);

sl_status_t sli_iostream_dmadrv_peripheral_memory(unsigned int              channelId,
                                                  sl_dma_signal_t           peripheralSignal,
                                                  void                      *dst,
                                                  void                      *src,
                                                  bool                      dstInc,
                                                  int                       len,
                                                  sl_dma_ctrl_size_t        size,
                                                  sl_iostream_dmadrv_callback_t callback,
                                                  void                      *cbUserParam);
sl_status_t sli_iostream_dmadrv_ldma_start_transfer(int                            channelId,
                                                   const sl_hal_ldma_transfer_config_t  *transfer,
                                                   const sl_hal_ldma_descriptor_t       *descriptor,
                                                   sl_iostream_dmadrv_callback_t  callback,
                                                   void                           *cbUserParam);

sl_status_t sli_iostream_dmadrv_pause_transfer(unsigned int channelId);
sl_status_t sli_iostream_dmadrv_resume_transfer(unsigned int channelId);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_TIME_CRITICAL)
sl_status_t sli_iostream_dmadrv_stop_transfer(unsigned int channelId);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_TIME_CRITICAL)
sl_status_t sli_iostream_dmadrv_transfer_done(unsigned int channelId, bool *done);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_TIME_CRITICAL)
sl_status_t sli_iostream_dmadrv_transfer_remaining_count(unsigned int channelId, int *remaining);

#ifdef __cplusplus
}
#endif

#endif /* __SILICON_LABS_IOSTREAM_DMADRV_H__ */
