/***************************************************************************//**
 * @file
 * @brief DMA Channel Driver (High-level per-channel DMA API)
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

#ifndef SL_DMA_CHANNEL_H
#define SL_DMA_CHANNEL_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "sl_status.h"
#include "sl_common.h"
#include "sl_device_peripheral.h"
#include "sl_device_dma.h"

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************//**
 * @addtogroup dma_channel DMA Channel Driver
 * @brief High-level API to perform DMA transfers on a single channel.
 * @details
 *  ## Overview
 *
 *  The DMA Channel Driver builds on top of the @ref dma_manager service. It
 *  assumes a DMA channel has already been allocated (or reserved) at the
 *  manager layer and focuses on per-channel operations: transfer submission,
 *  queuing and linking, status query, and callback notification.
 *
 *  Together, the DMA Manager and the DMA Channel Driver replace the legacy
 *  @ref dmadrv component. See the
 *  <a href="https://docs.silabs.com/gecko-platform/latest/platform-dmadrv-migration-guide/">
 *  DMADRV Migration Guide</a> for the full API mapping table when porting
 *  existing code.
 *
 *  Core responsibilities:
 *   - Provide simple memory-to-memory (M2M), memory-to-peripheral (M2P) and
 *     peripheral-to-memory (P2M) submission APIs.
 *   - Maintain a software queue (singly-linked list) mirroring the hardware
 *     descriptor link chain so that completions can be processed in batch
 *     when interrupts are delayed or masked.
 *   - Invoke a user callback once per descriptor (or per aborted descriptor
 *     when an error occurs) with explicit error / abort flags.
 *   - Automatically select an optimal transfer unit size (byte/half/word)
 *     based on alignment and length for M2M transfers, and automatically
 *     segment transfers larger than the hardware descriptor capacity.
 *
 *  ## Integration steps
 *
 *  To integrate the DMA Channel Driver in an application:
 *
 *  -# **Add the components.** Include the `dma_channel` and `dma_manager`
 *     SLC components in your `.slcp`. The DMA Manager is auto-initialized by
 *     SL Main; no manual `init()` call is required.
 *  -# **Allocate (or reserve) a channel.** Use
 *     `sl_dma_manager_allocate_channel()` (any channel) or
 *     `sl_dma_manager_reserve_channel()` (a specific channel number) from
 *     the DMA Manager.
 *  -# **Declare and initialize a channel handle.** Each active channel needs
 *     one application-owned `sl_dma_channel_handle_t`. Call
 *     @ref sl_dma_channel_init() with the channel number, the peripheral
 *     instance (or NULL for the default), the completion callback and a
 *     user-data pointer.
 *  -# **Set the peripheral signal if required.** Memory-to-peripheral and
 *     peripheral-to-memory transfers use block-handshake mode by default
 *     and need a request line from the peripheral. Call
 *     @ref sl_dma_channel_set_peripheral_signal() with the appropriate
 *     `SL_DMA_SIGNAL_*` constant before submitting M2P/P2M traffic.
 *     Memory-to-memory transfers do not need this step.
 *  -# **Submit transfers.** Pick the helper that matches your transfer
 *     pattern (see "Transfer modes" below). Pass `NULL` as the descriptor
 *     argument to let the driver allocate one, or pre-allocate via
 *     @ref sl_dma_channel_descriptor_alloc() for deterministic memory use.
 *  -# **Handle completions.** The callback registered at init time is
 *     invoked once per descriptor that requested a callback, with explicit
 *     `error` / `aborted` flags. Application code may also poll progress
 *     via @ref sl_dma_channel_get_status().
 *  -# **Tear down.** When done, call @ref sl_dma_channel_abort() if a
 *     transfer is still active, then @ref sl_dma_channel_deinit() to release
 *     the channel handle and `sl_dma_manager_free_channel()` to return the
 *     channel to the manager.
 *
 *  ## Transfer modes
 *
 *  | Helper                                              | Pattern                                      | Loops? | Peripheral signal required |
 *  | :-------------------------------------------------- | :------------------------------------------- | :----- | :------------------------- |
 *  | @ref sl_dma_channel_submit_transfer_m2m()             | Memory-to-memory                             | No     | No                         |
 *  | @ref sl_dma_channel_submit_transfer_m2p()             | Memory-to-peripheral                         | No     | Yes                        |
 *  | @ref sl_dma_channel_submit_transfer_p2m()             | Peripheral-to-memory                         | No     | Yes                        |
 *  | @ref sl_dma_channel_submit_transfer_list()            | Linked list of heterogeneous transfers       | No     | When list contains M2P/P2M |
 *  | @ref sl_dma_channel_submit_ping_pong_transfer_m2p()   | Two-buffer streaming M2P                     | Yes    | Yes                        |
 *  | @ref sl_dma_channel_submit_ping_pong_transfer_p2m()   | Two-buffer streaming P2M                     | Yes    | Yes                        |
 *  | @ref sl_dma_channel_submit_triple_buffered_transfer_m2p() | Three-buffer streaming M2P               | Yes    | Yes                        |
 *  | @ref sl_dma_channel_submit_triple_buffered_transfer_p2m() | Three-buffer streaming P2M               | Yes    | Yes                        |
 *  | @ref sl_dma_channel_update_active_transfer()          | Resize the currently-running head transfer   | -      | -                          |
 *
 *  ## Peripheral signals and block-handshake mode
 *
 *  Peripheral-attached transfers (M2P, P2M, and their ping-pong /
 *  triple-buffered variants) advance one block at a time on a request line
 *  asserted by the peripheral — this is what the API and the underlying
 *  hardware call *block-handshake mode* (see the @p block_handshake_mode
 *  field of @ref sl_dma_channel_transfer_t). The peripheral signal selected
 *  via @ref sl_dma_channel_set_peripheral_signal() identifies that request
 *  line. Without a signal set, an M2P or P2M transfer would have no
 *  hardware event to gate on. M2M transfers use full-cycle mode and ignore
 *  the peripheral signal.
 *
 *  ## Callback contract
 *
 *  The completion callback installed by @ref sl_dma_channel_init() is invoked
 *  from DMA channel IRQ context. It receives the channel handle, the
 *  user-data pointer, and two booleans:
 *
 *   - @p error    — set when the hardware reported a channel error. The
 *                   channel is automatically disabled and the remaining
 *                   queued descriptors are aborted.
 *   - @p aborted  — set when @ref sl_dma_channel_abort() was used to terminate
 *                   the descriptor (or when the descriptor was aborted as a
 *                   side-effect of an error).
 *
 *  Both `false` means a normal completion. In looping modes
 *  (ping-pong / triple-buffered) the callback is invoked on every buffer
 *  completion until the channel is aborted by the application. The callback
 *  return type is `void` — there is no way to stop a looping transfer from
 *  the callback by returning a value; call @ref sl_dma_channel_abort()
 *  instead.
 *
 *  ## Error handling
 *
 *  If the hardware sets the CHERROR bit for a channel, the driver disables
 *  the channel, aborts all queued descriptors and invokes the registered
 *  callback for each pending descriptor with @p error=true and
 *  @p aborted=true. The application is responsible for re-enabling or
 *  reinitializing the channel before submitting new work.
 *
 *  ## Performance
 *
 *  On devices with external FLASH, the component "RAM Code for DMA Channel
 *  Performance" (`ram_code_select_dma_channel_performance`) can be added to
 *  move the DMA channel ISR into RAM to improve interrupt latency at the
 *  cost of higher RAM consumption.
 *
 *  ## Typical usage
 *
 *  The example below shows a memory-to-memory transfer (`app_dma_m2m`,
 *  no peripheral signal needed) and a memory-to-peripheral transfer
 *  (`app_dma_tx`, which calls @ref sl_dma_channel_set_peripheral_signal()
 *  first because m2p uses block-handshake mode).
 *
 *  @code{.c}
 *  static sl_dma_channel_handle_t dma_handle;
 *
 *  static void dma_cb(sl_dma_channel_handle_t *handle,
 *                     void                    *user_data,
 *                     bool                     error,
 *                     bool                     aborted)
 *  {
 *    (void)handle;
 *    (void)user_data;
 *    if (!error && !aborted) {
 *      do_application_work();
 *    }
 *  }
 *
 *  void app_dma_init(void)
 *  {
 *    uint8_t ch;
 *    sl_dma_manager_allocate_channel(NULL, &ch);
 *    sl_dma_channel_init(&dma_handle, NULL, ch, dma_cb, NULL);
 *  }
 *
 *  void app_dma_m2m(void *src, void *dst, size_t len)
 *  {
 *    sl_dma_channel_submit_transfer_m2m(&dma_handle, src, dst, len, NULL);
 *  }
 *
 *  void app_dma_tx(const uint8_t *data, size_t len)
 *  {
 *    sl_dma_channel_set_peripheral_signal(&dma_handle,
 *                                         SL_DMA_SIGNAL_EUSART0_TXFL);
 *    sl_dma_channel_submit_transfer_m2p(&dma_handle,
 *                                       (void *)data,
 *                                       (void *)&EUSART0->TXDATA,
 *                                       len,
 *                                       SL_DMA_CTRL_SIZE_BYTE,
 *                                       NULL);
 *  }
 *  @endcode
 *
 *  @ingroup dma
 *  @{
 ******************************************************************************/

/*******************************************************************************
 *****************************   DATA TYPES   *********************************
 ******************************************************************************/

/// @brief Opaque DMA channel handle.
///
/// The application allocates one handle per active channel. Each handle
/// tracks the bound DMA channel number, peripheral instance, callback and
/// driver-internal state. Treat its contents as opaque; use the
/// `sl_dma_channel_*` API to manipulate the channel.
typedef struct sl_dma_channel_handle sl_dma_channel_handle_t;

/// DMA channel opaque transfer descriptor
typedef struct sl_dma_channel_xfer_descriptor sl_dma_channel_xfer_descriptor_t;

/// DMA channel transfer descriptor flags
typedef struct sl_dma_channel_xfer_descriptor_flags {
  uint32_t driver_allocated       : 1; ///< Indicates if the descriptor was internally allocated by the driver
  uint32_t callback_on_complete   : 1; ///< Indicates if a callback should be called on descriptor completion
  uint32_t reserved               : 30;
} sl_dma_channel_xfer_descriptor_flags_t;

/// DMA channel state
typedef enum {
  SL_DMA_CHANNEL_STATE_DISABLED,
  SL_DMA_CHANNEL_STATE_ENABLED,
  SL_DMA_CHANNEL_STATE_ABORTING,
} sl_dma_channel_state_t;

/// DMA channel operating mode
typedef enum {
  SL_DMA_CHANNEL_MODE_NORMAL,   ///< Normal mode: single or linked transfers with callbacks
  SL_DMA_CHANNEL_MODE_LOOPING   ///< Looping mode: circular descriptor chain (ping-pong/triple-buffered)
} sl_dma_channel_mode_t;

/***************************************************************************//**
 * Typedef for the user supplied callback function which is called on a transfer
 * complete event.
 *
 * @param handle Handle to DMA channel.
 *
 * @param user_data Pointer to user data that is passed to the tx complete
 *                  handler function.
 *
 * @param error Flag that indicates if an error occurred during transfer.
 *
 * @param aborted Flag that indicates if the transfer was aborted.
 *
 * @note In case of error, the channel will be disabled and all submitted
 *       transfers will be aborted. It is the responsibility of the user to
 *       re-enable the channel and re-submit transfers.
 ******************************************************************************/
typedef void (*sl_dma_channel_callback_t)(sl_dma_channel_handle_t *handle,
                                          void *user_data,
                                          bool error,
                                          bool aborted);

/// A DMA channel driver instance handle data structure.
/// Allocated by the application using the DMA Channel Driver.
/// Several concurrent channel handles may exist. The application must
/// not modify the contents of this handle and should not depend on its values.
struct sl_dma_channel_handle {
  /// @cond DO_NOT_INCLUDE_WITH_DOXYGEN
  uint8_t channel_number;             ///< DMA channel number.
  sl_peripheral_dma_t dma_peripheral; ///< DMA peripheral base instance.
  sl_dma_channel_callback_t callback; ///< Per-descriptor completion/error callback (optional).
  void *user_data;                    ///< User data pointer forwarded to callback.
  sl_dma_channel_xfer_descriptor_t *descriptor_list; ///< Head descriptor in current chain (active HW desc or first pending)
  sl_dma_channel_mode_t mode;         ///< Current operating mode (normal or looping)
  sl_dma_channel_state_t state;       ///< Current state (enabled, disabled or aborting)
  /// @endcond
};

/***************************************************************************//**
 * @brief Transfer specification (single element of a linked transfer list)
 *
 * This structure defines a single transfer operation in a linked transfer list.
 * It contains the source and destination addresses, the size of the transfer,
 * and flags for incrementing the source and destination pointers.
 ******************************************************************************/
typedef struct sl_dma_channel_transfer {
  void *source;                                 ///< Source address
  void *destination;                            ///< Destination address
  size_t size;                                  ///< Size in bytes
  sl_dma_ctrl_size_t unit_size;                 ///< One of SL_DMA_CTRL_SIZE_* macros
  sl_dma_ctrl_block_size_t block_size;          ///< One of SL_DMA_CTRL_BLOCKSIZE_* macros
  bool increment_source;                        ///< Increment source pointer per unit
  bool increment_destination;                   ///< Increment destination pointer per unit
  bool block_handshake_mode;                    ///< Transfer one block per DMA channel request if true
  bool callback_on_complete;                    ///< Generate callback when this transfer completes
  bool cacheable;                               ///< If requires cacheable attribute (Everest/XDMA)
  sl_dma_channel_xfer_descriptor_t *descriptor; ///< HW Descriptor buffer (Dynamically allocated if NULL)
  struct sl_dma_channel_transfer *next;         ///< Next in list (NULL = end or forms loop)
} sl_dma_channel_transfer_t;

/// Status structure returned by sl_dma_channel_get_status().
typedef struct sl_dma_channel_status {
  bool active;                  ///< A transfer list is active
  bool enabled;                 ///< Channel enabled in HW
  uint32_t bytes_completed;     ///< Cumulative bytes completed in current chain
} sl_dma_channel_status_t;

/*******************************************************************************
 *****************************   API PROTOTYPES  ******************************
 ******************************************************************************/

/***************************************************************************//**
 * Aborts all pending transfers on a given DMA channel.
 *
 * This function may be called from thread context or from within a DMA channel
 * callback (IRQ context). Re-entrant calls are safe: if the channel is already
 * in the @p SL_DMA_CHANNEL_STATE_ABORTING or @p SL_DMA_CHANNEL_STATE_DISABLED
 * state, the function returns @p SL_STATUS_OK immediately without taking any
 * action.
 *
 * @param[in,out]  handle DMA channel handle.
 *
 * @return SL_STATUS_OK on success, or if the channel was already aborting or
 *         already disabled.
 *
 * @note In normal mode, the registered callback is invoked with @p error=false
 *       and @p aborted=true for each descriptor from the currently active
 *       descriptor onwards. When called from thread context, descriptors that
 *       have already completed in hardware but not yet been processed by the
 *       IRQ handler will have their callbacks invoked normally before the
 *       abort callbacks. When called from IRQ context (i.e., from within a
 *       DMA channel callback), those already-completed descriptors are handled
 *       by the current IRQ invocation and will not receive an additional
 *       callback from the abort. In looping mode, callbacks are invoked for
 *       all descriptors in the circular chain. Callbacks are only invoked for
 *       descriptors that requested a callback on completion.
 *
 * @note Internally allocated descriptors will be freed automatically.
 *
 * @note Invalid handle checks are performed via assertions in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_abort(sl_dma_channel_handle_t *handle);

/***************************************************************************//**
 * Suspends peripheral requests for a given DMA channel.
 *
 * Suspending disables peripheral requests, preventing new transfers from being
 * triggered. Any active transfer will be allowed to complete.
 *
 * @param[in]  handle DMA channel handle.
 *
 * @return SL_STATUS_OK on success.
 *
 * @note Any active transfer will be allowed to complete, but no new transfers
 *       will be started until the channel is resumed with
 *       @ref sl_dma_channel_resume().
 *
 * @note Invalid handle checks are performed via assertions in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_suspend(const sl_dma_channel_handle_t *handle);

/***************************************************************************//**
 * Resumes peripheral requests for a previously suspended DMA channel.
 *
 * This re-enables peripheral requests that were disabled by
 * @ref sl_dma_channel_suspend(), allowing new transfers to be triggered.
 *
 * @param[in]  handle DMA channel handle.
 *
 * @return SL_STATUS_OK on success.
 *
 * @note Invalid handle checks are performed via assertions in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_resume(const sl_dma_channel_handle_t *handle);

/***************************************************************************//**
 * Gets the status of the given DMA channel.
 *
 * Retrieves the current runtime status of the DMA channel, including whether
 * it is enabled, whether a transfer is active, and progress information.
 *
 * @param[in]  handle DMA channel handle.
 *
 * @param[out] status Pointer to status structure to populate with channel status.
 *                    The following fields are populated:
 *                    - enabled: Whether the channel is enabled in hardware
 *                    - active: Whether a transfer list is currently active
 *                    - bytes_completed: Bytes completed in the current (head)
 *                      descriptor only
 *
 * @return SL_STATUS_OK on success.
 *
 * @note The bytes_completed field only reflects progress in the currently active
 *       descriptor. This does not include bytes from previously completed
 *       descriptors in a chain.
 *
 * @note Invalid handle checks are performed via assertions in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_get_status(sl_dma_channel_handle_t *handle,
                                      sl_dma_channel_status_t *status);

/***************************************************************************//**
 * Allocate a DMA channel handle structure from the heap.
 *
 * This helper allocates memory for a channel handle. The channel still needs
 * to be initialized with sl_dma_channel_init() before use. Provided mainly
 * for dynamic use cases; applications with static allocation may ignore it.
 *
 * @param[out] handle  Location where the allocated handle pointer is stored.
 *                     Set to NULL on allocation failure.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_ALLOCATION_FAILED if memory cannot be allocated.
 *
 * @note Invalid arguments (NULL pointer) trigger EFM_ASSERT in debug builds only.
 *       In release builds, passing NULL will result in undefined behavior.
 ******************************************************************************/
sl_status_t sl_dma_channel_handle_alloc(sl_dma_channel_handle_t **handle);

/***************************************************************************//**
 * Free a DMA channel handle previously allocated by sl_dma_channel_handle_alloc().
 *
 * The channel must be deinitialized with @ref sl_dma_channel_deinit() before
 * calling this function. Calling this function while transfers are in progress
 * or while descriptors are still queued results in undefined behavior.
 *
 * @param[in] handle  Channel handle pointer to free.
 *
 * @return SL_STATUS_OK on success.
 *
 * @note Invalid arguments (NULL pointer) trigger EFM_ASSERT in debug builds
 *       only. In release builds, passing NULL will result in undefined
 *       behavior.
 ******************************************************************************/
sl_status_t sl_dma_channel_handle_free(sl_dma_channel_handle_t *handle);

/***************************************************************************//**
 * Get the size in bytes of the channel handle structure.
 *
 * Useful for static allocation arrays or custom pools.
 *
 * @return Size in bytes of sl_dma_channel_handle_t.
 ******************************************************************************/
size_t sl_dma_channel_handle_get_size(void);

/***************************************************************************//**
 * Allocate a DMA channel transfer descriptor from the heap.
 *
 * This helper allocates memory for a transfer descriptor. The descriptor can
 * be used with transfer submission functions to avoid internal allocation.
 * Provided mainly for dynamic use cases; applications with static allocation
 * may ignore it.
 *
 * @param[in]  handle      DMA channel handle.
 * @param[out] descriptor  Location where the allocated descriptor pointer is
 *                         stored. Set to NULL on allocation failure.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 *       In release builds, passing NULL will result in undefined behavior.
 ******************************************************************************/
sl_status_t sl_dma_channel_descriptor_alloc(const sl_dma_channel_handle_t *handle,
                                            sl_dma_channel_xfer_descriptor_t **descriptor);

/***************************************************************************//**
 * Free a DMA channel transfer descriptor previously allocated by
 * sl_dma_channel_descriptor_alloc().
 *
 * The descriptor should not be in use by any active or pending transfer when
 * freeing.
 *
 * @param[in] handle     DMA channel handle.
 * @param[in] descriptor Descriptor pointer to free.
 *
 * @return SL_STATUS_OK on success.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 *       In release builds, passing NULL will result in undefined behavior.
 ******************************************************************************/
sl_status_t sl_dma_channel_descriptor_free(const sl_dma_channel_handle_t *handle,
                                           sl_dma_channel_xfer_descriptor_t *descriptor);

/***************************************************************************//**
 * Get the size in bytes of the channel transfer descriptor structure.
 *
 * Useful for static allocation arrays or custom pools.
 *
 * @return Size in bytes of sl_dma_channel_xfer_descriptor_t.
 ******************************************************************************/
size_t sl_dma_channel_descriptor_get_size(void);

/***************************************************************************//**
 * Initialize an allocated channel handle with peripheral instance, channel index
 * and user completion callback.
 *
 * The channel itself must already be reserved/allocated at the DMA manager
 * layer. This function initializes the channel handle and sets up the
 * channel for DMA transfers.
 *
 * @param[in,out] handle         Pointer to handle (must be allocated).
 * @param[in]     peripheral     DMA peripheral base object. If NULL, the
 *                               default dma peripheral of the target will be
 *                               used.
 * @param[in]     channel_number Hardware channel number.
 * @param[in]     callback       User callback invoked on transfer completion
 *                               or error (may be NULL if not needed).
 * @param[in]     user_data      User data pointer forwarded to callback
 *                               (may be NULL if not needed).
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_BUSY if the DMA channel is currently enabled. For DMA
 *         channels managed by this driver, an enabled channel indicates that
 *         there are transfers that are not yet completed.
 *
 * @note If you wish to force re-initialization of a DMA channel that is currently
 *       enabled, you can call @ref sl_dma_channel_abort() beforehand to abort
 *       any pending transfers and disable the channel.
 *
 * @note Invalid arguments (NULL handle pointer, invalid channel number) trigger
 *       EFM_ASSERT in debug builds only. In release builds, passing invalid
 *       arguments will result in undefined behavior.
 ******************************************************************************/
sl_status_t sl_dma_channel_init(sl_dma_channel_handle_t *handle,
                                sl_peripheral_t peripheral,
                                uint8_t channel_number,
                                sl_dma_channel_callback_t callback,
                                void *user_data);

/***************************************************************************//**
 * Deinitialize a DMA channel handle.
 *
 * The channel must not be enabled when calling this function. If the channel
 * is enabled (indicating active or pending transfers), this function will
 * return SL_STATUS_BUSY. To deinitialize a channel with active transfers,
 * first call @ref sl_dma_channel_abort() to abort pending transfers and disable
 * the channel.
 *
 * @param[in,out] handle  Pointer to the channel handle to deinitialize.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_BUSY if the DMA channel is currently enabled. The channel
 *         must be disabled (either by completing all transfers naturally or by
 *         calling @ref sl_dma_channel_abort()) before it can be deinitialized.
 *
 * @note Invalid arguments (NULL handle pointer) trigger EFM_ASSERT in debug
 *       builds only. In release builds, passing invalid arguments will result
 *       in undefined behavior.
 ******************************************************************************/
sl_status_t sl_dma_channel_deinit(sl_dma_channel_handle_t *handle);

/***************************************************************************//**
 * Set the peripheral signal routed to a DMA channel.
 *
 * The peripheral signal is necessary for transfers configured in
 * block-handshake mode (`block_handshake_mode == true` in
 * @ref sl_dma_channel_transfer_t), which pend on the signal being asserted
 * before executing each block. For instance, memory-to-peripheral or
 * peripheral-to-memory transfers shall only execute when the peripheral is
 * ready to consume or serve data, so the DMA waits on the peripheral's
 * request line between blocks.
 *
 * The peripheral signal is shared by every transfer subsequently submitted
 * on the channel, so it typically only needs to be set once during channel
 * setup. The m2p / p2m helpers
 * (@ref sl_dma_channel_submit_transfer_m2p(),
 *  @ref sl_dma_channel_submit_transfer_p2m(),
 *  @ref sl_dma_channel_submit_ping_pong_transfer_m2p(),
 *  @ref sl_dma_channel_submit_ping_pong_transfer_p2m(),
 *  @ref sl_dma_channel_submit_triple_buffered_transfer_m2p(), and
 *  @ref sl_dma_channel_submit_triple_buffered_transfer_p2m()) enable
 * block-handshake mode by default, so they all rely on this routing.
 * Memory-to-memory transfers (@ref sl_dma_channel_submit_transfer_m2m()) do
 * not use block-handshake mode and therefore do not depend on the
 * peripheral signal.
 *
 * No transfers must be active on the DMA channel when calling this API; the
 * channel must be idle so that the new routing applies cleanly to the next
 * submission.
 *
 * @param[in] handle    Pointer to handle (must be allocated and initialized).
 * @param[in] signal    Peripheral signal to route to the channel, expressed
 *                      as one of the `SL_DMA_SIGNAL_*` constants defined in
 *                      `sl_device_dma.h`.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_BUSY when the DMA channel has active transfers.
 *
 * @note Invalid signal values trigger EFM_ASSERT in debug builds only.
 *
 * @note Invalid handle checks are performed via assertions in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_set_peripheral_signal(const sl_dma_channel_handle_t *handle,
                                                 sl_dma_signal_t signal);

/***************************************************************************//**
 * Submit a memory-to-memory transfer on a channel.
 *
 * If @p descriptor is NULL, a descriptor is allocated internally and populated.
 * This function automatically selects an optimal transfer unit size based on buffer
 * alignment and transfer size.
 *
 * @param[in,out] handle       Channel handle.
 * @param[in]     source       Source address.
 * @param[in]     destination  Destination address.
 * @param[in]     size         Transfer size in bytes (must be > 0).
 * @param[in,out] descriptor   Optional pre-built descriptor pointer; if NULL
 *                              one is allocated and filled.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_INVALID_PARAMETER if size is 0, if the transfer size (in bytes)
 *         is not a multiple of the automatically selected unit size (in bytes), if
 *         source or destination buffers are misaligned for the selected unit size,
 *         or if a user-provided descriptor is too small for a transfer requiring
 *         segmentation.
 * @return SL_STATUS_INVALID_STATE if channel is in looping mode (ping-pong or
 *         triple-buffered transfer is active).
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 *
 * @note A completion callback is always requested for this transfer.
 *
 * @note Buffer alignment requirements: Both source and destination must be aligned
 *       for the selected unit size (WORD requires 4-byte alignment, HALF requires
 *       2-byte alignment, BYTE has no alignment requirement). The transfer size
 *       must be a multiple of the selected unit size.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_submit_transfer_m2m(sl_dma_channel_handle_t *handle,
                                               void *source,
                                               void *destination,
                                               size_t size,
                                               sl_dma_channel_xfer_descriptor_t *descriptor);

/***************************************************************************//**
 * Submit a memory-to-peripheral transfer on a channel.
 *
 * If @p descriptor is NULL, a descriptor is allocated internally and populated.
 * The transfer is triggered in block handshake mode with the current peripheral
 * signal set with @ref sl_dma_channel_set_peripheral_signal().
 *
 * Contrary to @ref sl_dma_channel_submit_transfer_m2m(), the destination address
 * is a peripheral register address. The source address is incremented during
 * the transfer.
 *
 * @param[in,out] handle             Channel handle.
 * @param[in]     source             Source memory address.
 * @param[in]     reg                Peripheral destination address.
 * @param[in]     size               Transfer size in bytes (must be > 0).
 * @param[in]     unit_size          Transfer unit size (SL_DMA_CTRL_SIZE_BYTE,
 *                                   SL_DMA_CTRL_SIZE_HALF, or SL_DMA_CTRL_SIZE_WORD).
 * @param[in,out] descriptor         Optional pre-built descriptor pointer; if NULL
 *                                   one is allocated and filled.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_INVALID_PARAMETER if size is 0, if the transfer size (in bytes)
 *         is not a multiple of the unit size (in bytes), if source or peripheral
 *         register address is misaligned for the specified unit size, or if a
 *         user-provided descriptor is too small for a transfer requiring
 *         segmentation.
 * @return SL_STATUS_INVALID_STATE if channel is in looping mode (ping-pong or
 *         triple-buffered transfer is active).
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 *
 * @note Transfer defaults: source increments, destination does not increment,
 *       block handshake mode is enabled, and a completion callback is always
 *       requested.
 *
 * @note Buffer alignment requirements: Both the source address and the peripheral
 *       register address must be aligned according to the unit size. For
 *       SL_DMA_CTRL_SIZE_HALF, both addresses must be 2-byte aligned. For
 *       SL_DMA_CTRL_SIZE_WORD, both addresses must be 4-byte aligned.
 *       SL_DMA_CTRL_SIZE_BYTE has no alignment requirement. In practice,
 *       peripheral registers are always naturally aligned to their access size.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_submit_transfer_m2p(sl_dma_channel_handle_t *handle,
                                               void *source,
                                               void *reg,
                                               size_t size,
                                               sl_dma_ctrl_size_t unit_size,
                                               sl_dma_channel_xfer_descriptor_t *descriptor);

/***************************************************************************//**
 * Submit a peripheral-to-memory transfer on a channel.
 *
 * If @p descriptor is NULL, a descriptor is allocated internally and populated.
 * The transfer is triggered in block handshake mode with the current peripheral
 * signal set with @ref sl_dma_channel_set_peripheral_signal().
 *
 * Contrary to @ref sl_dma_channel_submit_transfer_m2m(), the source address
 * is a peripheral register address. The destination address is incremented during
 * the transfer.
 *
 * @param[in,out] handle       Channel handle.
 * @param[in]     reg          Peripheral register address (e.g., &EUSART0->RXDATA).
 * @param[in]     destination  Memory destination address.
 * @param[in]     size         Transfer size in bytes (must be > 0).
 * @param[in]     unit_size    Transfer unit size (SL_DMA_CTRL_SIZE_BYTE,
 *                             SL_DMA_CTRL_SIZE_HALF, or SL_DMA_CTRL_SIZE_WORD).
 * @param[in,out] descriptor   Optional pre-built descriptor pointer; if NULL
 *                             one is allocated and filled.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_INVALID_PARAMETER if size is 0, if the transfer size (in bytes)
 *         is not a multiple of the unit size (in bytes), if destination or
 *         peripheral register address is misaligned for the specified unit size,
 *         or if a user-provided descriptor is too small for a transfer requiring
 *         segmentation.
 * @return SL_STATUS_INVALID_STATE if channel is in looping mode (ping-pong or
 *         triple-buffered transfer is active).
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 *
 * @note Transfer defaults: source does not increment, destination increments,
 *       block handshake mode is enabled, and a completion callback is always
 *       requested.
 *
 * @note Buffer alignment requirements: Both the destination address and the
 *       peripheral register address must be aligned according to the unit size.
 *       For SL_DMA_CTRL_SIZE_HALF, both addresses must be 2-byte aligned. For
 *       SL_DMA_CTRL_SIZE_WORD, both addresses must be 4-byte aligned.
 *       SL_DMA_CTRL_SIZE_BYTE has no alignment requirement. In practice,
 *       peripheral registers are always naturally aligned to their access size.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_submit_transfer_p2m(sl_dma_channel_handle_t *handle,
                                               void *reg,
                                               void *destination,
                                               size_t size,
                                               sl_dma_ctrl_size_t unit_size,
                                               sl_dma_channel_xfer_descriptor_t *descriptor);

/***************************************************************************//**
 * Submits a list of transfers to the specified DMA channel.
 *
 * If other transfers and/or transfer lists are already submitted, this list of
 * transfers will be appended to the list of pending transfers for the given
 * DMA channel.
 *
 * Large transfers may be automatically segmented if they exceed the maximum
 * transfer size. For multi-segment transfers, the completion callback is only
 * triggered when the last segment completes.
 *
 * @param[in,out] handle    Pointer to the DMA channel handle.
 * @param[in]     list_head Pointer to the head of the transfer list.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_INVALID_PARAMETER if any transfer in the list has size == 0,
 *         if the transfer size (in bytes) is not a multiple of the unit size
 *         (in bytes), if source or destination buffers are misaligned for the
 *         specified unit size, or if a user-provided descriptor is too small for a
 *         transfer requiring segmentation.
 * @return SL_STATUS_INVALID_STATE if channel is in looping mode (ping-pong or
 *         triple-buffered transfer is active).
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 *
 * @warning Transfer structures in the transfer list should only be freed
 * or reused after they have completed.
 *
 * @warning This function must not be used to submit looping transfers, which are
 * transfers where the transfer list forms a circular structure (the last
 * transfer's next pointer points back to an earlier transfer in the list,
 * creating a loop). Looping transfers are only supported through specialized
 * ping-pong and triple-buffered transfer APIs. The transfer list submitted to
 * this function must be linear, with the last transfer in the list having its
 * next pointer set to NULL. Submitting a looping transfer to this function will
 * result in undefined behavior that the DMA Channel Driver cannot recover from.
 *
 * @note Each transfer in the list must have size > 0. Transfers with size == 0
 *       will cause this function to return SL_STATUS_INVALID_PARAMETER.
 *
 * @note The transfer size (in bytes) must be a multiple of the unit size
 *       (in bytes). For example, if unit_size is SL_DMA_CTRL_SIZE_HALF (2 bytes),
 *       the size must be an even number. If unit_size is SL_DMA_CTRL_SIZE_WORD
 *       (4 bytes), the size must be a multiple of 4. If this requirement is not
 *       met, the function will return SL_STATUS_INVALID_PARAMETER.
 *
 * @note Buffer alignment requirements: Source and destination addresses must be
 *       aligned according to the unit size. For SL_DMA_CTRL_SIZE_HALF, buffers
 *       must be 2-byte aligned. For SL_DMA_CTRL_SIZE_WORD, buffers must be
 *       4-byte aligned. SL_DMA_CTRL_SIZE_BYTE has no alignment requirement.
 *       Misaligned buffers will cause this function to return
 *       SL_STATUS_INVALID_PARAMETER.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_submit_transfer_list(sl_dma_channel_handle_t *handle,
                                                sl_dma_channel_transfer_t *list_head);

/***************************************************************************//**
 * Submits a memory to peripheral ping pong transfer on given DMA channel.
 *
 * This function sets up a continuous ping-pong transfer between two source
 * buffers and a peripheral register. The transfer loops indefinitely,
 * alternating between the two source buffers until the channel is disabled.
 *
 * @param[in,out] handle       Channel handle.
 * @param[in]     source       First source buffer.
 * @param[in]     source_2     Second source buffer.
 * @param[in]     destination  Peripheral destination address.
 * @param[in]     size         Transfer size in bytes per buffer (must be > 0).
 * @param[in]     unit_size    Transfer unit size (SL_DMA_CTRL_SIZE_BYTE,
 *                             SL_DMA_CTRL_SIZE_HALF, or SL_DMA_CTRL_SIZE_WORD).
 * @param[in,out] descriptor   Optional pre-built descriptor pointer array;
 *                             if NULL, descriptors are allocated and filled.
 *                             If provided, must point to an array of 2 descriptors.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_INVALID_PARAMETER if size is 0, if the transfer size (in bytes)
 *         is not a multiple of the unit size (in bytes), if source buffers are
 *         misaligned for the specified unit size, or if size exceeds the maximum
 *         single descriptor capacity.
 * @return SL_STATUS_INVALID_STATE if channel is already in looping mode or has
 *         pending transfers.
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 *
 * @note The transfer loops infinitely until the channel is stopped with
 *       @ref sl_dma_channel_abort().
 *
 * @note This implementation configures the source to increment. The destination
 *       does not increment.
 *
 * @note Buffer alignment requirements: Source addresses must be aligned according
 *       to the unit size. For SL_DMA_CTRL_SIZE_HALF, sources must be 2-byte aligned.
 *       For SL_DMA_CTRL_SIZE_WORD, sources must be 4-byte aligned.
 *       SL_DMA_CTRL_SIZE_BYTE has no alignment requirement.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_submit_ping_pong_transfer_m2p(sl_dma_channel_handle_t *handle,
                                                         void *source,
                                                         void *source_2,
                                                         void *destination,
                                                         size_t size,
                                                         sl_dma_ctrl_size_t unit_size,
                                                         sl_dma_channel_xfer_descriptor_t *descriptor);

/***************************************************************************//**
 * Submits a peripheral to memory ping pong transfer on given DMA channel.
 *
 * This function sets up a continuous ping-pong transfer between a peripheral
 * register and two destination buffers. The transfer loops indefinitely,
 * alternating between the two destination buffers until the channel is disabled.
 *
 * @param[in,out] handle       Channel handle.
 * @param[in]     source       Peripheral source address.
 * @param[in]     destination  First destination buffer.
 * @param[in]     destination_2 Second destination buffer.
 * @param[in]     size         Transfer size in bytes per buffer (must be > 0).
 * @param[in]     unit_size    Transfer unit size (SL_DMA_CTRL_SIZE_BYTE,
 *                             SL_DMA_CTRL_SIZE_HALF, or SL_DMA_CTRL_SIZE_WORD).
 * @param[in,out] descriptors  Optional pre-built descriptor pointer array;
 *                             if NULL, descriptors are allocated and filled.
 *                             If provided, must point to an array of 2
 *                             descriptors.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_INVALID_PARAMETER if size is 0, if the transfer size (in bytes)
 *         is not a multiple of the unit size (in bytes), if destination buffers are
 *         misaligned for the specified unit size, or if size exceeds the maximum
 *         single descriptor capacity.
 * @return SL_STATUS_INVALID_STATE if channel is already in looping mode or has
 *         pending transfers.
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 *
 * @note The transfer loops infinitely until the channel is stopped with
 *       @ref sl_dma_channel_abort().
 *
 * @note This implementation configures the destination to increment. The source
 *       does not increment.
 *
 * @note Buffer alignment requirements: Destination addresses must be aligned according
 *       to the unit size. For SL_DMA_CTRL_SIZE_HALF, destinations must be 2-byte aligned.
 *       For SL_DMA_CTRL_SIZE_WORD, destinations must be 4-byte aligned.
 *       SL_DMA_CTRL_SIZE_BYTE has no alignment requirement.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_submit_ping_pong_transfer_p2m(sl_dma_channel_handle_t *handle,
                                                         void *source,
                                                         void *destination,
                                                         void *destination_2,
                                                         size_t size,
                                                         sl_dma_ctrl_size_t unit_size,
                                                         sl_dma_channel_xfer_descriptor_t *descriptors);

/***************************************************************************//**
 * Submits a memory to peripheral triple buffered transfer on given DMA channel.
 *
 * This function sets up a continuous triple-buffered transfer cycling through
 * three source buffers to a peripheral register. The transfer loops indefinitely,
 * cycling through the three source buffers until the channel is disabled.
 *
 * @param[in,out] handle       Channel handle.
 * @param[in]     source       First source buffer.
 * @param[in]     source_2     Second source buffer.
 * @param[in]     source_3     Third source buffer.
 * @param[in]     destination  Peripheral destination address.
 * @param[in]     size         Transfer size in bytes per buffer (must be > 0).
 * @param[in]     unit_size    Transfer unit size (SL_DMA_CTRL_SIZE_BYTE,
 *                             SL_DMA_CTRL_SIZE_HALF, or SL_DMA_CTRL_SIZE_WORD).
 * @param[in,out] descriptors  Optional pre-built descriptor pointer array;
 *                             if NULL, descriptors are allocated and filled.
 *                             If provided, must point to an array of 3
 *                             descriptors.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_INVALID_PARAMETER if size is 0, if the transfer size (in bytes)
 *         is not a multiple of the unit size (in bytes), if source buffers are
 *         misaligned for the specified unit size, or if size exceeds the maximum
 *         single descriptor capacity.
 * @return SL_STATUS_INVALID_STATE if channel is already in looping mode or has
 *         pending transfers.
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 *
 * @note The transfer loops infinitely until the channel is stopped with
 *       @ref sl_dma_channel_abort().
 *
 * @note This implementation configures the source to increment. The destination
 *       does not increment.
 *
 * @note Buffer alignment requirements: Source addresses must be aligned according
 *       to the unit size. For SL_DMA_CTRL_SIZE_HALF, sources must be 2-byte aligned.
 *       For SL_DMA_CTRL_SIZE_WORD, sources must be 4-byte aligned.
 *       SL_DMA_CTRL_SIZE_BYTE has no alignment requirement.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_submit_triple_buffered_transfer_m2p(sl_dma_channel_handle_t *handle,
                                                               void *source,
                                                               void *source_2,
                                                               void *source_3,
                                                               void *destination,
                                                               size_t size,
                                                               sl_dma_ctrl_size_t unit_size,
                                                               sl_dma_channel_xfer_descriptor_t *descriptors);

/***************************************************************************//**
 * Submits a peripheral to memory triple buffered transfer on given DMA channel.
 *
 * This function sets up a continuous triple-buffered transfer from a peripheral
 * register cycling through three destination buffers. The transfer loops
 * indefinitely, cycling through the three destination buffers until the
 * channel is disabled.
 *
 * @param[in,out] handle       Channel handle.
 * @param[in]     source       Peripheral source address.
 * @param[in]     destination  First destination buffer.
 * @param[in]     destination_2 Second destination buffer.
 * @param[in]     destination_3 Third destination buffer.
 * @param[in]     size         Transfer size in bytes per buffer (must be > 0).
 * @param[in]     unit_size    Transfer unit size (SL_DMA_CTRL_SIZE_BYTE,
 *                             SL_DMA_CTRL_SIZE_HALF, or SL_DMA_CTRL_SIZE_WORD).
 * @param[in,out] descriptor   Optional pre-built descriptor pointer array;
 *                             if NULL, descriptors are allocated and filled.
 *                             If provided, must point to an array of 3 descriptors.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_INVALID_PARAMETER if size is 0, if the transfer size (in bytes)
 *         is not a multiple of the unit size (in bytes), if destination buffers are
 *         misaligned for the specified unit size, or if size exceeds the maximum
 *         single descriptor capacity.
 * @return SL_STATUS_INVALID_STATE if channel is already in looping mode or has
 *         pending transfers.
 * @return SL_STATUS_ALLOCATION_FAILED if descriptor allocation fails.
 *
 * @note The transfer loops infinitely until the channel is stopped with
 *       @ref sl_dma_channel_abort().
 *
 * @note This implementation configures the destination to increment. The source
 *       does not increment.
 *
 * @note Buffer alignment requirements: Destination addresses must be aligned according
 *       to the unit size. For SL_DMA_CTRL_SIZE_HALF, destinations must be 2-byte aligned.
 *       For SL_DMA_CTRL_SIZE_WORD, destinations must be 4-byte aligned.
 *       SL_DMA_CTRL_SIZE_BYTE has no alignment requirement.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_submit_triple_buffered_transfer_p2m(sl_dma_channel_handle_t *handle,
                                                               void *source,
                                                               void *destination,
                                                               void *destination_2,
                                                               void *destination_3,
                                                               size_t size,
                                                               sl_dma_ctrl_size_t unit_size,
                                                               sl_dma_channel_xfer_descriptor_t *descriptor);

/***************************************************************************//**
 * Updates size of the current transfer.
 *
 * This function allows updating the size for the active transfer. This is useful
 * in cases where the expected data follows a pattern of a header that specifies
 * a payload size followed by the actual payload. When the header and the payload
 * have to be in separate buffers and zero-copy is desired, the user can parse
 * the header from the channel callback and call this function to update the size
 * matching the information read from the header.
 *
 * @param[in] handle    Channel handle.
 * @param[in] new_size  New size of the transfer, in bytes.
 *
 * @return SL_STATUS_OK on success.
 * @return SL_STATUS_INVALID_PARAMETER if new_size is 0, if new_size is not a
 *         multiple of the transfer unit size, if the transfer has already
 *         transferred more bytes than new_size, or if new_size in transfer
 *         units exceeds the maximum single-descriptor transfer count
 *         (SL_DMA_CHANNEL_MAX_XFER_UNIT_COUNT).
 * @return SL_STATUS_INVALID_STATE if no transfer is currently active.
 *
 * @note Special care must be taken by the caller to ensure that the active
 *       transfer is really the one it aims at modifying.
 *
 * @note If the current transfer has transferred more bytes than new_size, the
 *       call will fail and the transfer will continue with its original size.
 *
 * @note It is up to the caller to ensure that 'new_size' is not larger than
 *       the buffer that was submitted earlier.
 *
 * @note Invalid arguments (NULL pointers) trigger EFM_ASSERT in debug builds only.
 ******************************************************************************/
sl_status_t sl_dma_channel_update_active_transfer(sl_dma_channel_handle_t *handle,
                                                  size_t new_size);

/** @} (end addtogroup dma_channel) */

#ifdef __cplusplus
}
#endif
#endif // SL_DMA_CHANNEL_H
