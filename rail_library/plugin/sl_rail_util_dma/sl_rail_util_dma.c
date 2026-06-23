/***************************************************************************//**
 * @file
 * @brief
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
#include "em_device.h"
#include "sl_hal_ldma.h"

#include "sl_dma_manager.h"
#include "sl_status.h"
#include "sl_rail.h"
#include "sl_rail_util_dma.h"
#include "sl_rail_util_dma_config.h"

void sl_rail_util_dma_init(void)
{
#if SL_RAIL_UTIL_DMA_ENABLE
#if SL_RAIL_UTIL_DMA_DMADRV_ENABLE
  sl_status_t dma_status = sl_dma_manager_init(NULL, NULL);
  if ((dma_status == SL_STATUS_OK)
      || (dma_status == SL_STATUS_ALREADY_INITIALIZED)) {
    uint8_t channel;
    dma_status = sl_dma_manager_allocate_channel(NULL, &channel);
    if (dma_status == SL_STATUS_OK) {
      (void) sl_rail_use_dma(SL_RAIL_EFR32_HANDLE, channel);
    }
  }
#else // !SL_RAIL_UTIL_DMA_DMADRV_ENABLE
  sl_hal_ldma_init_t ldmaInit = SL_HAL_LDMA_INIT_DEFAULT;
#if defined(_SILICON_LABS_32B_SERIES_3)
  sl_hal_ldma_init(LDMA0, &ldmaInit);
#else
  sl_hal_ldma_init(LDMA, &ldmaInit);
#endif
  (void) sl_rail_use_dma(SL_RAIL_EFR32_HANDLE, SL_RAIL_UTIL_DMA_CHANNEL);
#endif // SL_RAIL_UTIL_DMA_DMADRV_ENABLE
#endif // SL_RAIL_UTIL_DMA_ENABLE
}
