/***************************************************************************//**
 * @file
 * @brief DMADRV API implementation.
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

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>

#include "em_device.h"
#include "sl_core.h"

#include "sl_clock_manager.h"
#include "sl_device_dma.h"
#include "sl_dma_manager.h"
#include "sl_hal_ldma.h"
#include "sl_status.h"
#include "sli_iostream_dmadrv.h"


/// @cond DO_NOT_INCLUDE_WITH_DOXYGEN

// Channel index is stored and passed around as uint8_t, so guard the count at
// build time and avoid repeated runtime range checks that cannot be hit when
// DMA_CHAN_COUNT <= 255.
static_assert(DMA_CHAN_COUNT < 256, "DMA_CHAN_COUNT must be <= 255");

typedef struct {
  sl_iostream_dmadrv_callback_t callback;
  void              *userParam;
  unsigned int      callbackCount;
  bool              allocated;
} ChTable_t;

static bool initialized = false;
static ChTable_t chTable[DMA_CHAN_COUNT];

static const sl_hal_ldma_transfer_config_t xferCfgPeripheral = SL_HAL_LDMA_TRANSFER_CFG_PERIPHERAL(0);
static const sl_hal_ldma_descriptor_t p2m = SL_HAL_LDMA_DESCRIPTOR_SINGLE_P2M(SL_HAL_LDMA_CTRL_SIZE_BYTE, NULL, NULL, 1UL);

typedef struct {
  sl_hal_ldma_descriptor_t desc[2];
} DmaXfer_t;

static DmaXfer_t dmaXfer[DMA_CHAN_COUNT];

static sl_dma_handle_t *dmadrv_dma_manager_handle;

SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel0_IRQ_handler(void);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel1_IRQ_handler(void);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel2_IRQ_handler(void);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel3_IRQ_handler(void);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel4_IRQ_handler(void);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel5_IRQ_handler(void);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel6_IRQ_handler(void);
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel7_IRQ_handler(void);
#if DMA_CHAN_COUNT > 8
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel8_IRQ_handler(void);
#endif
#if DMA_CHAN_COUNT > 9
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel9_IRQ_handler(void);
#endif
#if DMA_CHAN_COUNT > 10
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel10_IRQ_handler(void);
#endif
#if DMA_CHAN_COUNT > 11
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel11_IRQ_handler(void);
#endif
#if DMA_CHAN_COUNT > 12
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel12_IRQ_handler(void);
#endif
#if DMA_CHAN_COUNT > 13
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel13_IRQ_handler(void);
#endif
#if DMA_CHAN_COUNT > 14
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel14_IRQ_handler(void);
#endif
#if DMA_CHAN_COUNT > 15
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void ldma_channel15_IRQ_handler(void);
#endif

static sl_dma_manager_channel_irq_callback_t internalCallbacks[DMA_CHAN_COUNT] = {
  ldma_channel0_IRQ_handler,
  ldma_channel1_IRQ_handler,
  ldma_channel2_IRQ_handler,
  ldma_channel3_IRQ_handler,
  ldma_channel4_IRQ_handler,
  ldma_channel5_IRQ_handler,
  ldma_channel6_IRQ_handler,
  ldma_channel7_IRQ_handler
#if DMA_CHAN_COUNT > 8
  , ldma_channel8_IRQ_handler
#endif
#if DMA_CHAN_COUNT > 9
  , ldma_channel9_IRQ_handler
#endif
#if DMA_CHAN_COUNT > 10
  , ldma_channel10_IRQ_handler
#endif
#if DMA_CHAN_COUNT > 11
  , ldma_channel11_IRQ_handler
#endif
#if DMA_CHAN_COUNT > 12
  , ldma_channel12_IRQ_handler
#endif
#if DMA_CHAN_COUNT > 13
  , ldma_channel13_IRQ_handler
#endif
#if DMA_CHAN_COUNT > 14
  , ldma_channel14_IRQ_handler
#endif
#if DMA_CHAN_COUNT > 15
  , ldma_channel15_IRQ_handler
#endif
};

static sl_status_t start_transfer(unsigned int              channelId,
                                  sl_dma_signal_t           peripheralSignal,
                                  void                      *buf0,
                                  void                      *buf1,
                                  bool                      bufInc,
                                  int                       len,
                                  sl_dma_ctrl_size_t        size,
                                  sl_iostream_dmadrv_callback_t callback,
                                  void                      *cbUserParam);

SL_CODE_CLASSIFY(SL_CODE_COMPONENT_DMA_CHANNEL, SL_CODE_CLASS_DMA_CHANNEL_PERFORMANCE)
static void LDMA_IRQHandlerDefault(uint8_t chnum);

/// @endcond

/***************************************************************************//**
 * @brief
 *  Allocate (reserve) a DMA channel.
 *
 * @param[out] channelId
 *  The channel ID assigned by DMADRV.
 *
 * @return
 *  @ref SL_STATUS_OK on success. On failure, an appropriate
 *  sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_allocate_channel(unsigned int *channelId)
{
  sl_status_t status;
  CORE_DECLARE_IRQ_STATE;

  if ( !initialized ) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if ( channelId == NULL ) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  *channelId = 0;

  status = sl_dma_manager_allocate_channel(NULL, (uint8_t *)channelId);
  if (status != SL_STATUS_OK) {
    return SL_STATUS_NO_MORE_RESOURCE;
  }

  CORE_ENTER_ATOMIC();
  chTable[*channelId].allocated = true;
  chTable[*channelId].callback  = NULL;
  CORE_EXIT_ATOMIC();

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief
 *  Deinitialize DMADRV.
 *
 * @details
 *  If DMA channels are not currently allocated, it will disable DMA hardware
 *  and mask associated interrupts.
 *
 * @return
 *  @ref SL_STATUS_OK on success. On failure, an appropriate
 *  sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_deinit(void)
{
  bool inUse;
  CORE_DECLARE_IRQ_STATE;

  inUse = false;

  CORE_ENTER_ATOMIC();
  for (unsigned int i = 0; i < DMA_CHAN_COUNT; i++ ) {
    if ( chTable[i].allocated ) {
      inUse = true;
      break;
    }
  }

  if ( !inUse ) {
    initialized = false;
    CORE_EXIT_ATOMIC();
    return SL_STATUS_OK;
  }
  CORE_EXIT_ATOMIC();

  return SL_STATUS_BUSY;
}

/***************************************************************************//**
 * @brief
 *  Free an allocated (reserved) DMA channel.
 *
 * @param[in] channelId
 *  The channel ID to free.
 *
 * @return
 *  @ref SL_STATUS_OK on success. On failure, an appropriate
 *  sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_free_channel(unsigned int channelId)
{
  CORE_DECLARE_IRQ_STATE;

  if ( !initialized ) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if ( channelId >= DMA_CHAN_COUNT ) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  sl_dma_manager_free_channel(dmadrv_dma_manager_handle, (uint8_t)channelId);

  CORE_ENTER_ATOMIC();
  chTable[channelId].allocated = false;
  CORE_EXIT_ATOMIC();

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief
 *  Initialize DMADRV.
 *
 * @details
 *  The DMA hardware is initialized.
 *
 * @return
 *  @ref SL_STATUS_OK on success. On failure, an appropriate
 *  sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_init(void)
{
  CORE_DECLARE_IRQ_STATE;
  sl_status_t status;

  CORE_ENTER_ATOMIC();
  if ( initialized ) {
    CORE_EXIT_ATOMIC();
    return SL_STATUS_ALREADY_INITIALIZED;
  }
  initialized = true;
  CORE_EXIT_ATOMIC();

  for (unsigned int i = 0; i < DMA_CHAN_COUNT; i++ ) {
    chTable[i].allocated = false;
  }

  status = sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_LDMA0);
  EFM_ASSERT(status == SL_STATUS_OK);

  status = sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_LDMAXBAR0);
  EFM_ASSERT(status == SL_STATUS_OK);

  sl_dma_manager_get_default_handle(&dmadrv_dma_manager_handle);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief
 *  Start an LDMA transfer.
 *
 * @details
 *  This function is similar to the emlib LDMA function.
 *
 * @param[in] channelId
 *  The channel ID to use.
 *
 * @param[in] transfer
 *  A DMA transfer configuration data structure.
 *
 * @param[in] descriptor
 *  A DMA transfer descriptor, can be an array of descriptors linked together.
 *
 * @param[in] callback
 *  An optional callback function for signalling completion. May be NULL if not
 *  needed.
 *
 * @param[in] cbUserParam
 *  An optional user parameter to feed to the callback function. May be NULL if
 *  not needed.
 *
 * @return
 *   @ref SL_STATUS_OK on success. On failure, an appropriate
 *   sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_ldma_start_transfer(int                            channelId,
                                                    const sl_hal_ldma_transfer_config_t  *transfer,
                                                    const sl_hal_ldma_descriptor_t       *descriptor,
                                                    sl_iostream_dmadrv_callback_t  callback,
                                                    void                           *cbUserParam)
{
  ChTable_t *ch;

  if ( !initialized ) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if ( (unsigned int)channelId >= DMA_CHAN_COUNT ) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  ch = &chTable[channelId];
  if ( ch->allocated == false ) {
    return SL_STATUS_INVALID_HANDLE;
  }

  ch->callback      = callback;
  ch->userParam     = cbUserParam;
  ch->callbackCount = 0;

  sl_hal_ldma_init_transfer(LDMA0, channelId, transfer, descriptor);

  if (channelId < 16) {
    sl_hal_ldma_enable_interrupts(LDMA0, (1 << channelId));
  }
  #if defined(_LDMA_IFH_MASK)
  else {
    sl_hal_ldma_enable_high_interrupts(LDMA0, (1 << (channelId - 16)));
  }
  #endif

  sl_dma_manager_register_channel_irq_callback(dmadrv_dma_manager_handle, (uint8_t)channelId, internalCallbacks[channelId]);

  sl_hal_ldma_start_transfer(LDMA0, channelId);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief
 *  Start a peripheral to memory DMA transfer.
 *
 * @param[in] channelId
 *  The channel ID to use for the transfer.
 *
 * @param[in] peripheralSignal
 *  Selects which peripheral/peripheralsignal to use.
 *
 * @param[in] dst
 *  A destination memory address.
 *
 * @param[in] src
 *  A source memory (peripheral register) address.
 *
 * @param[in] dstInc
 *  Set to true to enable destination address increment (increments according
 *  to @a size parameter).
 *
 * @param[in] len
 *  A number of items (of @a size size) to transfer.
 *
 * @param[in] size
 *  An item size, byte, halfword or word.
 *
 * @param[in] callback
 *  A function to call on DMA completion, use NULL if not needed.
 *
 * @param[in] cbUserParam
 *  An optional user parameter to feed to the callback function. Use NULL if
 *  not needed.
 *
 * @return
 *   @ref SL_STATUS_OK on success. On failure, an appropriate
 *   sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_peripheral_memory(unsigned int          channelId,
                                                  sl_dma_signal_t       peripheralSignal,
                                                  void                  *dst,
                                                  void                  *src,
                                                  bool                  dstInc,
                                                  int                   len,
                                                  sl_dma_ctrl_size_t    size,
                                                  sl_iostream_dmadrv_callback_t     callback,
                                                  void                  *cbUserParam)
{
  return start_transfer(channelId,
                        peripheralSignal,
                        dst,
                        src,
                        dstInc,
                        len,
                        size,
                        callback,
                        cbUserParam);
}

/***************************************************************************//**
 * @brief
 *  Pause an ongoing DMA transfer.
 *
 * @param[in] channelId
 *  The channel ID of the transfer to pause.
 *
 * @return
 *  @ref SL_STATUS_OK on success. On failure, an appropriate
 *  sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_pause_transfer(unsigned int channelId)
{
  if ( !initialized ) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if ( channelId >= DMA_CHAN_COUNT ) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  if ( chTable[channelId].allocated == false ) {
    return SL_STATUS_INVALID_HANDLE;
  }

  sl_hal_ldma_disable_channel_request(LDMA0, channelId);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief
 *  Resume an ongoing DMA transfer.
 *
 * @param[in] channelId
 *  The channel ID of the transfer to resume.
 *
 * @return
 *  @ref SL_STATUS_OK on success. On failure, an appropriate
 *  sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_resume_transfer(unsigned int channelId)
{
  if ( !initialized ) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if ( channelId >= DMA_CHAN_COUNT ) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  if ( chTable[channelId].allocated == false ) {
    return SL_STATUS_INVALID_HANDLE;
  }

  sl_hal_ldma_enable_channel_request(LDMA0, channelId);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief
 *  Stop an ongoing DMA transfer.
 *
 * @param[in] channelId
 *  The channel ID of the transfer to stop.
 *
 * @return
 *  @ref SL_STATUS_OK on success. On failure, an appropriate
 *  sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_stop_transfer(unsigned int channelId)
{
  if ( !initialized ) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if ( channelId >= DMA_CHAN_COUNT ) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  if ( chTable[channelId].allocated == false ) {
    return SL_STATUS_INVALID_HANDLE;
  }

  sl_hal_ldma_stop_transfer(LDMA0, channelId);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief
 *  Check if a transfer has completed.
 *
 * @note
 *  This function should be used in a polled environment.
 *  Will only work reliably for transfers NOT using the completion interrupt.
 *
 * @param[in] channelId
 *  The channel ID of the transfer to check.
 *
 * @param[out] done
 *  True if a transfer has completed, false otherwise.
 *
 * @return
 *  @ref SL_STATUS_OK on success. On failure, an appropriate
 *  sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_transfer_done(unsigned int channelId, bool *done)
{
  if ( !initialized ) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if ( (channelId >= DMA_CHAN_COUNT)
       || (done == NULL) ) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  if ( chTable[channelId].allocated == false ) {
    return SL_STATUS_INVALID_HANDLE;
  }

  *done = sl_hal_ldma_transfer_is_done(LDMA0, channelId);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * @brief
 *  Get number of items remaining in a transfer.
 *
 * @note
 *  This function does not take into account that a DMA transfer with
 *  a chain of linked transfers might be ongoing. It will only check the
 *  count for the current transfer.
 *
 * @param[in] channelId
 *  The channel ID of the transfer to check.
 *
 * @param[out] remaining
 *  A number of items remaining in the transfer.
 *
 * @return
 *  @ref SL_STATUS_OK on success. On failure, an appropriate
 *  sl_status_t is returned.
 ******************************************************************************/
sl_status_t sli_iostream_dmadrv_transfer_remaining_count(unsigned int channelId, int *remaining)
{
  if ( !initialized ) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if ( (channelId >= DMA_CHAN_COUNT)
       || (remaining == NULL) ) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  if ( chTable[channelId].allocated == false ) {
    return SL_STATUS_INVALID_HANDLE;
  }

  *remaining = sl_hal_ldma_transfer_remaining_count(LDMA0, channelId);

  return SL_STATUS_OK;
}

/// @cond DO_NOT_INCLUDE_WITH_DOXYGEN

/***************************************************************************//**
 * @brief
 *  Default interrupt handler for LDMA common to all interrupt channel lines.
 *
 * @param[in] chnum
 *  The channel ID responsible for the interrupt signal trigger.
 ******************************************************************************/
static void LDMA_IRQHandlerDefault(uint8_t chnum)
{
  ChTable_t *ch;

  uint32_t pending_errors = sl_dma_manager_get_pending_errors(chnum);
  if (pending_errors) {
    /* Loop to enable debugger to see what has happened. */
    while (true) {
      /* Wait forever. */
    }
  }

  /* Callback called if it was provided for the given channel. */
  ch = &chTable[chnum];
  if ( ch->callback != NULL ) {
    ch->callbackCount++;
    ch->callback(chnum, ch->callbackCount, ch->userParam);
  }
}

/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 0.
 ******************************************************************************/
static void ldma_channel0_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(0);
}

/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 1.
 ******************************************************************************/
static void ldma_channel1_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(1);
}

/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 2.
 ******************************************************************************/
static void ldma_channel2_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(2);
}

/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 3.
 ******************************************************************************/
static void ldma_channel3_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(3);
}

/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 4.
 ******************************************************************************/
static void ldma_channel4_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(4);
}

/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 5.
 ******************************************************************************/
static void ldma_channel5_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(5);
}

/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 6.
 ******************************************************************************/
static void ldma_channel6_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(6);
}

/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 7.
 ******************************************************************************/
static void ldma_channel7_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(7);
}

#if (DMA_CHAN_COUNT > 8)
/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 8.
 ******************************************************************************/
static void ldma_channel8_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(8);
}
#endif

#if (DMA_CHAN_COUNT > 9)
/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 9.
 ******************************************************************************/
static void ldma_channel9_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(9);
}
#endif

#if (DMA_CHAN_COUNT > 10)
/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 10.
 ******************************************************************************/
static void ldma_channel10_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(10);
}
#endif

#if (DMA_CHAN_COUNT > 11)
/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 11.
 ******************************************************************************/
static void ldma_channel11_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(11);
}
#endif

#if (DMA_CHAN_COUNT > 12)
/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 12.
 ******************************************************************************/
static void ldma_channel12_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(12);
}
#endif

#if (DMA_CHAN_COUNT > 13)
/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 13.
 ******************************************************************************/
static void ldma_channel13_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(13);
}
#endif

#if (DMA_CHAN_COUNT > 14)
/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 14.
 ******************************************************************************/
static void ldma_channel14_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(14);
}
#endif

#if (DMA_CHAN_COUNT > 15)
/***************************************************************************//**
 * @brief
 *  Root interrupt handler for LDMA channel 15.
 ******************************************************************************/
static void ldma_channel15_IRQ_handler(void)
{
  LDMA_IRQHandlerDefault(15);
}
#endif

/***************************************************************************//**
 * @brief
 *  Start an LDMA transfer.
 ******************************************************************************/
static sl_status_t start_transfer(unsigned int          channelId,
                                  sl_dma_signal_t       peripheralSignal,
                                  void                  *buf0,
                                  void                  *buf1,
                                  bool                  bufInc,
                                  int                   len,
                                  sl_dma_ctrl_size_t    size,
                                  sl_iostream_dmadrv_callback_t callback,
                                  void                  *cbUserParam)
{
  ChTable_t *ch;
  sl_hal_ldma_transfer_config_t xfer;
  sl_hal_ldma_descriptor_t *desc;

  if ( !initialized ) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if ( (channelId >= DMA_CHAN_COUNT)
       || (buf0 == NULL)
       || (buf1 == NULL)
       || (len < 0)
       || ((unsigned long)len > SL_HAL_LDMA_DESCRIPTOR_MAX_XFER_SIZE) ) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  ch = &chTable[channelId];
  if ( ch->allocated == false ) {
    return SL_STATUS_INVALID_HANDLE;
  }

  xfer = xferCfgPeripheral;
  desc = &dmaXfer[channelId].desc[0];

  // peripheral to mem
  *desc = p2m;
  if ( !bufInc ) {
    desc->xfer.dst_inc = SL_HAL_LDMA_CTRL_DST_INC_NONE;
  }

  xfer.request_sel      = *peripheralSignal;
  desc->xfer.xfer_count = len - 1;
  desc->xfer.dst_addr   = (uint32_t)(uint8_t *)buf0;
  desc->xfer.src_addr   = (uint32_t)(uint8_t *)buf1;
  desc->xfer.size       = size;

  /* Whether an interrupt is needed. */
  if (callback == NULL) {
    desc->xfer.done_ifs = 0;
  }

  ch->callback      = callback;
  ch->userParam     = cbUserParam;
  ch->callbackCount = 0;

  sl_dma_manager_register_channel_irq_callback(dmadrv_dma_manager_handle, (uint8_t)channelId, internalCallbacks[channelId]);

  sl_hal_ldma_init_transfer(LDMA0, channelId, &xfer, desc);
  sl_hal_ldma_start_transfer(LDMA0, channelId);
  if (channelId < 16) {
    sl_hal_ldma_enable_interrupts(LDMA0, (0x1UL << channelId));
  }
#if defined(_LDMA_IFH_MASK)
  else {
    sl_hal_ldma_enable_high_interrupts(LDMA0, (0x1UL << (channelId - 16)));
  }
#endif

  return SL_STATUS_OK;
}
