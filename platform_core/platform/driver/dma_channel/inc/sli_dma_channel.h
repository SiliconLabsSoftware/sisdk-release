/***************************************************************************//**
 * @file
 * @brief DMA Channel Driver - Internal API
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef SLI_DMA_CHANNEL_H_
#define SLI_DMA_CHANNEL_H_

#include "sl_status.h"
#include "sl_dma_channel.h"

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************//**
 * @addtogroup dma_channel
 * @{
 ******************************************************************************/

/***************************************************************************//**
 * Process completed descriptors on a DMA channel from a non-IRQ context.
 *
 * This function performs one polling iteration of the work that the DMA channel
 * IRQ handler would normally do for a single channel:
 *  - Latches and clears the channel's done and error interrupt flags in the
 *    LDMA peripheral so they do not trigger a spurious IRQ later when the
 *    DMA interrupt is unmasked.
 *  - Records any error reported by the channel so the regular error handling
 *    path can run.
 *  - Walks the channel's descriptor list, invokes user completion callbacks for
 *    descriptors whose hardware transfer has completed, and transitions the
 *    channel to @p SL_DMA_CHANNEL_STATE_DISABLED when there is no more work.
 *
 * It is intended for drivers that need to wait for a DMA transfer to complete
 * while the DMA channel IRQ is masked (for example, a blocking transfer
 * initiated from inside a critical section). Callers typically invoke this
 * function repeatedly from a polling loop until their own completion condition
 * is satisfied.
 *
 * The function is a no-op when nothing has completed; it is safe to call
 * unconditionally inside a polling loop.
 *
 * The function is also safe to call when the channel's NVIC IRQ is NOT masked
 * (for example, when the caller's "is the IRQ masked" check is approximate,
 * such as SPIDRV checking @c LDMA0_CHNL0_IRQn on Series 3 even though it may
 * be using a different channel). The implementation uses the IF register as a
 * single-consumer hand-off and runs the descriptor-list walk inside a global
 * critical section, so the user completion callback is invoked at most once
 * per hardware completion event regardless of which path (this function or
 * the real IRQ) observes the event first.
 *
 * @param[in,out]  handle DMA channel handle.
 *
 * @note This function does NOT require the caller to be in IRQ context. Unlike
 *       the regular IRQ dispatch path, it does not rely on any
 *       interrupt-controller global state (such as the active IRQ number) to
 *       identify the channel: the channel is taken from @p handle.
 *
 * @note Only meaningful in @ref SL_DMA_CHANNEL_MODE_NORMAL. In
 *       @ref SL_DMA_CHANNEL_MODE_LOOPING the channel never disables itself and
 *       this function will only clear pending IRQ flags without invoking the
 *       looping callback (which is normally tied to IRQ context).
 *
 * @note Supports both low-range channels (0..15, via @c IF/@c IEN) and, on
 *       parts that define @c _LDMA_IFH_MASK, high-range channels (16..31, via
 *       @c IFH/@c IENH). The IF-clear / descriptor-walk pairing is the same
 *       for both ranges.
 *
 * @note Invalid handle checks are performed via assertions in debug builds only.
 ******************************************************************************/
void sli_dma_channel_process_completed(sl_dma_channel_handle_t *handle);

/** @} (end addtogroup dma_channel) */

#ifdef __cplusplus
}
#endif
#endif // SLI_DMA_CHANNEL_H_
