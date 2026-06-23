/**
 * @file sl_log_backend_segger.c
 * @brief SEGGER SystemView backend implementation for Silicon Labs logging system
 *
 * This file implements the SEGGER SystemView backend for the Silicon Labs logging
 * framework. It provides integration with SEGGER SystemView for real-time
 * event visualization and debugging. The implementation handles event recording
 * with various argument counts and manages SystemView initialization and
 * configuration.
 *
 * @author Silicon Labs
 * @date October 2025
 * @version 1.0
 */

#include <stdarg.h>

#include "SEGGER_SYSVIEW.h"
#include "sl_log_platform_specific.h"
#include "sl_log_common_config.h"

extern SEGGER_SYSVIEW_CORE_CONTEXT _ContextCaptiveCore;
/**
 * @brief Global timestamp variable for SystemView events
 *
 * This variable stores the timestamp of the last recorded event.
 * It is updated each time an event is recorded to SystemView.
 * The timestamp is used for event correlation and timing analysis.
 * @todo Temporary variable used to pass logged event timestamps to SystemView
 *      It will be deprecated after the SystemView API integration is implemented.
 */
uint32_t timestamp_global;

sl_status_t sl_log_systemview_write(sl_log_event_t *buffer, uint32_t read_index, uint32_t event_count);
sl_status_t sl_log_systemview_init(void);
sl_status_t sl_log_systemview_deinit(void);
sl_status_t sl_log_systemview_record_event(sl_log_event_t *event);

sl_log_api_backend_t sl_log_api_backend={
  .backend_init = sl_log_systemview_init,
  .backend_write = sl_log_systemview_write,
  .backend_deinit = sl_log_systemview_deinit
};
/**
 * @brief Initialize the SystemView logging backend
 *
 * Initializes the SEGGER SystemView component for event recording.
 * This function must be called before any events can be recorded
 * to the SystemView backend. It configures SystemView and starts
 * the recording session.
 *
 * @note This function should be called once during system initialization.
 *       Multiple calls to this function may cause undefined behavior.
 *
 * @see sl_log_systemview_deinit()
 * @see sl_log_systemview_config()
 */
sl_status_t sl_log_systemview_init(void)
{
  SEGGER_SYSVIEW_Conf();
  SEGGER_SYSVIEW_Start();
  return SL_STATUS_OK;
}

/**
 * @brief Deinitialize the SystemView logging backend
 *
 * Performs cleanup and deinitialization of the SystemView component.
 * This function should be called when the SystemView backend is no
 * longer needed or during system shutdown.
 *
 * @note After calling this function, no events should be recorded
 *       until sl_log_systemview_init() is called again.
 *
 * @see sl_log_systemview_init()
 */
sl_status_t sl_log_systemview_deinit(void)
{
  SEGGER_SYSVIEW_Stop();
  return SL_STATUS_OK;
}

/**
 * @brief Writes (records) a sequence of log events to the SystemView backend.
 *
 * Iterates over a ring buffer of log events starting at the provided read_index and
 * attempts to record up to event_count events via sl_log_systemview_record_event().
 * The read_index wraps to 0 when it reaches SL_LOG_NUMBER_OF_EVENTS (ring buffer behavior).
 * Processing stops early if any call to sl_log_systemview_record_event() returns a status
 * different from SL_STATUS_OK.
 *
 * @param[in] buffer
 *   Pointer to the ring buffer containing log events. The buffer is expected to have
 *   at least SL_LOG_NUMBER_OF_EVENTS elements.
 *
 * @param[in] read_index
 *   Starting index within the ring buffer (0 <= read_index <= SL_LOG_NUMBER_OF_EVENTS).
 *   If equal to SL_LOG_NUMBER_OF_EVENTS, it is immediately wrapped to 0.
 *
 * @param[in] event_count
 *   Number of events to attempt to record. Iteration stops earlier if an error occurs.
 *
 * @return sl_status_t
 *   - SL_STATUS_OK if all requested events were successfully recorded.
 *   - The first non-OK status returned by sl_log_systemview_record_event() if a failure occurs.
 *
 */
sl_status_t sl_log_systemview_write(sl_log_event_t *buffer, uint32_t read_index, uint32_t event_count)
{
  sl_status_t status = SL_STATUS_OK;
  if(event_count == 0){
    return SL_STATUS_OK;
  }
  if(buffer == NULL){
    return SL_STATUS_INVALID_PARAMETER;
  }
  if(read_index >= SL_LOG_NUMBER_OF_EVENTS || event_count > SL_LOG_NUMBER_OF_EVENTS){
    return SL_STATUS_INVALID_PARAMETER;
  }
  for (uint32_t i = 0; i < event_count; i++) {
    if (read_index == SL_LOG_NUMBER_OF_EVENTS) {
      read_index = 0;
    }
    status = sl_log_systemview_record_event(&buffer[read_index]);
    if(status!=SL_STATUS_OK){
      break;
    }
    read_index++;
  }
  return status;
}

/* Maximum number of bytes prepended to the SystemView payload:
 * 2 bytes of length + 5 bytes of event_id. Defined as a macro (not a
 * block-scope enum) so that the array dimension below is a true integer
 * constant expression for IAR (avoids Pe060). */
#define SLI_LOG_SYSVIEW_MAX_PREPEND_BYTES  7

/**
 * @brief Record a log event to SystemView
 *
 * Records a log event to the SystemView backend with appropriate formatting
 * based on the number of arguments. This function handles events with 0 to
 * SL_LOG_CONFIG_ARG arguments and updates the global timestamp for event
 * correlation.
 *
 * The function dispatches to different SystemView recording functions based
 * on the argument count (0 through 10 when supported by config and SEGGER API).
 *
 * @param[in] event Pointer to the log event structure containing:
 *                  - timestamp: Event timestamp in system timer units
 *                  - event_id: Unique event identifier
 *                  - args: Array of up to SL_LOG_CONFIG_ARG 32-bit arguments
 *                  - arg_count: Number of valid arguments (0 to SL_LOG_CONFIG_ARG)
 *                  - Additional metadata (core_id, flags, version)
 */
sl_status_t sl_log_systemview_record_event(sl_log_event_t *event)
{
  sl_status_t status = SL_STATUS_OK;
  U8 *pPayload;
  U8 *pPayloadStart;
  unsigned int NumBytes;
  int i;

  if (event == NULL) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  if (event->arg_count > SL_LOG_CONFIG_ARG) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  /* Size the buffer for the worst case (every argument slot used). The
   * arg_count bound was validated above; using the compile-time maximum
   * keeps this a fixed-size array (no VLA). */
  U8 aPacket[SLI_LOG_SYSVIEW_MAX_PREPEND_BYTES
             + SEGGER_SYSVIEW_INFO_SIZE
             + ((3 + SL_LOG_CONFIG_ARG) * SEGGER_SYSVIEW_QUANTA_U32)];

  pPayloadStart = aPacket + SLI_LOG_SYSVIEW_MAX_PREPEND_BYTES;
  pPayload = pPayloadStart;

  for (i = 0; i < event->arg_count; i++) {
    pPayload = SEGGER_SYSVIEW_EncodeU32(pPayload, event->args[i]);
  }

  NumBytes = (unsigned int)(pPayload - pPayloadStart);

  if (NumBytes > 127) {
    *--pPayloadStart = (U8)(NumBytes >> 7);
    *--pPayloadStart = (U8)(NumBytes | 0x80);
  } else {
    *--pPayloadStart = (U8)NumBytes;
  }

  if (event->event_id < 127) {
    *--pPayloadStart = (U8)event->event_id;
  } else if (event->event_id < (1u << 14)) {
    *--pPayloadStart = (U8)(event->event_id >> 7);
    *--pPayloadStart = (U8)(event->event_id | 0x80);
  } else if (event->event_id < (1ul << 21)) {
    *--pPayloadStart = (U8)(event->event_id >> 14);
    *--pPayloadStart = (U8)((event->event_id >> 7) | 0x80);
    *--pPayloadStart = (U8)(event->event_id | 0x80);
  } else if (event->event_id < (1ul << 28)) {
    *--pPayloadStart = (U8)(event->event_id >> 21);
    *--pPayloadStart = (U8)((event->event_id >> 14) | 0x80);
    *--pPayloadStart = (U8)((event->event_id >> 7) | 0x80);
    *--pPayloadStart = (U8)(event->event_id | 0x80);
  } else {
    *--pPayloadStart = (U8)(event->event_id >> 28);
    *--pPayloadStart = (U8)((event->event_id >> 21) | 0x80);
    *--pPayloadStart = (U8)((event->event_id >> 14) | 0x80);
    *--pPayloadStart = (U8)((event->event_id >> 7) | 0x80);
    *--pPayloadStart = (U8)(event->event_id | 0x80);
  }

  if (event->core_id == 1) {
    SEGGER_SYSVIEW_SendPacket_Ex(&_ContextCaptiveCore,
                                 event->timestamp,
                                 pPayloadStart,
                                 pPayload);
  } else {
    SEGGER_SYSVIEW_SendPacket_Ex(SEGGER_SYSVIEW_GetMainContext(),
                                 event->timestamp,
                                 pPayloadStart,
                                 pPayload);
  }

  return status;
}

/**
 * @brief Retrieve the SEGGER logging backend API instance.
 *
 * This function returns a pointer to the statically allocated (or globally
 * defined) SEGGER logging backend API structure. It allows the logging
 * framework to access the concrete backend implementation (function pointers etc.).
 *
 *
 * @return sl_log_api_backend_t* Pointer to the SEGGER log backend API struct.
 */
sl_log_api_backend_t * sl_log_get_api_backend(void){
  return &sl_log_api_backend;
}

/**
 * @brief Print a formatted string directly to SystemView (target-side formatting).
 *
 * Formats @p fmt with the supplied variadic arguments on the target and emits the
 * resulting text packet to SystemView via SEGGER_SYSVIEW_VPrintfTargetEx().
 * The @p options value is forwarded as the SystemView message-type / option
 * flag (e.g. SEGGER_SYSVIEW_LOG, SEGGER_SYSVIEW_WARNING, SEGGER_SYSVIEW_ERROR).
 *
 * Intended as the implementation backend for the SL_PRINT_FMT_* macros.
 * Unlike the event-based SL_PRINT_STRING_* path, this routine does not store
 * the format string pointer - the host receives the already-formatted text -
 * so it works without a SystemView description / lookup file at the cost of
 * extra runtime CPU and bandwidth.
 *
 * @param[in] options Message-type / options flag. Accepts the backend-agnostic
 *                    SL_LOG_PRINT_OPT_* values from sl_log.h (numerically
 *                    identical to SEGGER_SYSVIEW_LOG / WARNING / ERROR /
 *                    FLAG_APPEND) and forwards them to SystemView as-is.
 * @param[in] fmt     printf-style format string (must not be NULL).
 * @param[in] ap      va_list previously initialised by the variadic wrapper
 *                    SL_LOG_PRINT_TARGET_EX.
 *
 * @note Must be called only after the SystemView backend has been started
 *       (sl_log_systemview_init()).
 */
void sl_log_vprint_target_ex(uint32_t options, const char *fmt, va_list ap)
{
  va_list ap_copy;

  if (fmt == NULL) {
    return;
  }

  /* ap_copy is a local va_list object so &ap_copy is valid on all ABIs (GCC
   * struct, IAR array decay, etc.). Passing &ap is unsafe when va_list is an
   * array type (IAR ARM): ap decays to a pointer and &ap is a pointer-to-pointer. */
  va_copy(ap_copy, ap);
  SEGGER_SYSVIEW_VPrintfTargetEx(fmt, (U32)options, &ap_copy);
  va_end(ap_copy);
}
