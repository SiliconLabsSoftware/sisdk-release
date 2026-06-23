/***************************************************************************//**
 * @file
 * @brief Real-Time Locationing Service API
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

#ifndef SL_RTL_SERVICE_H
#define SL_RTL_SERVICE_H

/**
 * @defgroup sl_rtl_service Real-Time Locationing Service
 * @brief Thread-safe service layer for Bluetooth CS distance estimation
 *        in bare-metal and RTOS environments.
 *
 * The Real-Time Locationing (RTL) Service wraps the RTL library behind
 * an app_rta-based context/instance model. It manages a dedicated
 * processing context with a mutex guard, signal, and optional RTOS task,
 * so applications can submit Channel Sounding (CS) or Ranging Service
 * (RAS) procedure data from any thread and receive distance
 * estimates asynchronously through a result callback.
 *
 * Only one service context may exist at a time. Within that context,
 * multiple instances can be created to track different peer connections
 * concurrently, all sharing the same processing task.
 *
 * **Typical usage sequence:**
 * 1. sl_rtl_service_init_cs() -- create the service context with a
 *    result callback.
 * 2. sl_rtl_service_create_cs_instance() -- create one instance per
 *    peer connection.
 * 3. Configure the instance (must be called in this order):
 *    - sl_rtl_service_set_cs_algo_mode()
 *    - sl_rtl_service_set_cs_mode()
 *    - sl_rtl_service_set_cs_params()
 *    - sl_rtl_service_create_cs_estimator()
 *    - sl_rtl_service_set_cs_estimator_param() (optional, repeatable)
 * 4. sl_rtl_service_process_cs() or sl_rtl_service_process_ras() --
 *    submit procedure data for processing.
 * 5. In the result callback, query the result with
 *    sl_rtl_service_get_cs_distance_estimate() and related getters.
 * 6. sl_rtl_service_destroy_cs_instance() -- tear down the instance.
 * 7. sl_rtl_service_deinit_cs() -- tear down the context.
 *
 * **Threading:** All public API functions are thread-safe. The result
 * callback is invoked from the RTL processing task in RTOS mode, or
 * synchronously from within the process submission call in bare-metal
 * mode.
 *
 * @see sl_rtl_service_config.h for configurable parameters (task
 *      priority, stack size, guard timeout, max instances).
 * @{
 */

#include "sl_rtl_clib_api.h"

/// Opaque handle representing a Real-Time Locationing Service processing context.
typedef struct sl_rtl_service_cs_ctx sl_rtl_service_cs_ctx_t;

/// Opaque handle representing a single CS measurement instance within a context.
typedef struct sl_rtl_service_cs_inst sl_rtl_service_cs_inst_t;

/// Opaque result handle, valid only during the result callback invocation.
typedef struct sl_rtl_service_cs_result sl_rtl_service_cs_result_t;

/**************************************************************************//**
 * Result callback type.
 *
 * Invoked after RTL processing completes for a given instance. The
 * application can query distance estimates using @p result and the
 * sl_rtl_service_get_cs_* family of functions from within this callback.
 *
 * @param[in] inst           Instance that produced this result
 * @param[in] result         Opaque result handle for querying estimates.
 *                           Valid only for the duration of this callback.
 * @param[in] process_status Return value from sl_rtl_cs_process /
 *                           sl_rtl_ras_process
 * @param[in] user_data      Opaque pointer passed at context init
 *
 * @note In RTOS this is called from the RTL task context.
 *       In bare-metal this is called synchronously from the super-loop step.
 *****************************************************************************/
typedef void (*sl_rtl_service_cs_result_cb_t)(
  sl_rtl_service_cs_inst_t *inst,
  const sl_rtl_service_cs_result_t *result,
  enum sl_rtl_error_code process_status,
  void *user_data);

/**************************************************************************//**
 * Configuration for the RTL service CS context.
 *****************************************************************************/
typedef struct {
  sl_rtl_service_cs_result_cb_t result_cb; ///< Mandatory result callback.
  void *user_data;                           ///< Opaque pointer forwarded to result_cb.
} sl_rtl_service_cs_config_t;

// -----------------------------------------------------------------------------
// RTA contributor init (called by generated app_rta_init.c)

/**************************************************************************//**
 * @internal
 * RTA contributor initialization.
 *
 * Registers the RTL service CS processing context with app_rta. This
 * function is called automatically by the generated
 * @c app_rta_init_contributors() code (via the @c app_rta_init template
 * contribution declared in the rtl_service SLCC component). It runs
 * before the RTOS scheduler starts and before @c app_init.
 *
 * This is not part of the application API. Do not call it directly;
 * the SLCC code generator handles the invocation.
 *****************************************************************************/
void sl_rtl_service_rta_init_cs(void);

// -----------------------------------------------------------------------------
// Context lifecycle

/**************************************************************************//**
 * Initialize the RTL service CS context.
 *
 * Allocates a service context backed by an app_rta processing context
 * with a dedicated thread (RTOS) or super-loop step (bare-metal), a
 * mutex guard for thread-safe access, and a per-instance request slot.
 * If the backing app_rta context is not currently present, it is
 * created automatically.
 *
 * @note Only one service context may exist at a time. Call
 *       sl_rtl_service_deinit_cs() before creating a new one. After
 *       deinit, this function may be called again to create a new
 *       service context.
 *
 * @param[in]  config  Configuration (must include a non-NULL result_cb).
 * @param[out] ctx     Receives the allocated context pointer.
 *
 * @return SL_RTL_ERROR_SUCCESS        Context created successfully.
 * @return SL_RTL_ERROR_ARGUMENT       @p config or @p ctx is NULL, or
 *                                     @p config->result_cb is NULL.
 * @return SL_RTL_ERROR_INTERNAL       A context already exists.
 * @return SL_RTL_ERROR_OUT_OF_MEMORY  Memory allocation failed.
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_init_cs(
  const sl_rtl_service_cs_config_t *config,
  sl_rtl_service_cs_ctx_t **ctx);

/**************************************************************************//**
 * Deinitialize and free the RTL service CS context.
 *
 * Destroys all remaining instances, cancels any pending requests, and
 * tears down the underlying RTA context.
 *
 * @warning Must not be called from within a result callback. Doing so
 *          returns SL_RTL_ERROR_INTERNAL and leaves the context intact.
 *
 * @param[in] ctx  Context to tear down.
 *
 * @return SL_RTL_ERROR_SUCCESS   Context torn down and freed.
 * @return SL_RTL_ERROR_ARGUMENT  @p ctx is NULL or does not match the
 *                                active context.
 * @return SL_RTL_ERROR_INTERNAL  Guard acquisition failed, or a result
 *                                callback is currently in progress.
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_deinit_cs(
  sl_rtl_service_cs_ctx_t *ctx);

// -----------------------------------------------------------------------------
// Instance lifecycle

/**************************************************************************//**
 * Create an RTL service CS instance within a context.
 *
 * Allocates an instance from the context's internal pool and initializes
 * the underlying RTL library item. Multiple instances can share a
 * single context (and thus a single processing task). The maximum
 * number of instances per context is bounded by
 * @c SL_RTL_SERVICE_CS_MAX_INSTANCES.
 *
 * @param[in]  ctx   Parent RTL service CS context.
 * @param[out] inst  Receives the allocated instance pointer.
 *
 * @return SL_RTL_ERROR_SUCCESS       Instance created successfully.
 * @return SL_RTL_ERROR_ARGUMENT      @p ctx or @p inst is NULL, or
 *                                    @p ctx is not the active context.
 * @return SL_RTL_ERROR_INTERNAL      Guard acquisition failed.
 * @return SL_RTL_ERROR_OUT_OF_MEMORY Instance pool is full.
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_create_cs_instance(
  sl_rtl_service_cs_ctx_t *ctx,
  sl_rtl_service_cs_inst_t **inst);

/**************************************************************************//**
 * Destroy an RTL service CS instance.
 *
 * Deinitializes the underlying RTL library item and returns the instance
 * slot to the pool. Any pending processing request for this instance is
 * cancelled.
 *
 * @warning Must not be called from within this instance's result
 *          callback. Doing so returns SL_RTL_ERROR_INTERNAL.
 *
 * @param[in] inst  Instance to destroy.
 *
 * @return SL_RTL_ERROR_SUCCESS   Instance destroyed.
 * @return SL_RTL_ERROR_ARGUMENT  @p inst is NULL or not in use.
 * @return SL_RTL_ERROR_INTERNAL  Called from within the result callback,
 *                                or guard acquisition failed.
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_destroy_cs_instance(
  sl_rtl_service_cs_inst_t *inst);

// -----------------------------------------------------------------------------
// Instance configuration (call before processing)

/**************************************************************************//**
 * Set the estimation algorithm mode for an instance.
 *
 * Thread-safe: acquires the parent context's RTA guard internally.
 *
 * @param[in] inst  RTL service CS instance.
 * @param[in] mode  Algorithm mode to use for distance estimation.
 *
 * @return SL_RTL_ERROR_SUCCESS   Mode set successfully.
 * @return SL_RTL_ERROR_ARGUMENT  @p inst is NULL or not in use.
 * @return SL_RTL_ERROR_INTERNAL  Guard acquisition failed.
 * @return Other values forwarded from the underlying RTL library.
 *
 * @see sl_rtl_service_create_cs_estimator
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_set_cs_algo_mode(
  sl_rtl_service_cs_inst_t *inst,
  sl_rtl_cs_algo_mode mode);

/**************************************************************************//**
 * Set the CS mode (main and sub) for an instance.
 *
 * Thread-safe: acquires the parent context's RTA guard internally.
 *
 * @param[in] inst       RTL service CS instance.
 * @param[in] main_mode  Main CS mode.
 * @param[in] sub_mode   Sub CS mode (SL_RTL_CS_MODE_NONE if unused).
 *
 * @return SL_RTL_ERROR_SUCCESS   Mode set successfully.
 * @return SL_RTL_ERROR_ARGUMENT  @p inst is NULL or not in use.
 * @return SL_RTL_ERROR_INTERNAL  Guard acquisition failed.
 * @return Other values forwarded from the underlying RTL library.
 *
 * @see sl_rtl_service_create_cs_estimator
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_set_cs_mode(
  sl_rtl_service_cs_inst_t *inst,
  sl_rtl_cs_mode main_mode,
  sl_rtl_cs_mode sub_mode);

/**************************************************************************//**
 * Set the CS parameters for an instance.
 *
 * Thread-safe: acquires the parent context's RTA guard internally.
 *
 * @param[in] inst    RTL service CS instance.
 * @param[in] params  CS parameters (e.g. channel map, timing).
 *
 * @return SL_RTL_ERROR_SUCCESS   Parameters set successfully.
 * @return SL_RTL_ERROR_ARGUMENT  @p inst is NULL or not in use, or
 *                                @p params is NULL.
 * @return SL_RTL_ERROR_INTERNAL  Guard acquisition failed.
 * @return Other values forwarded from the underlying RTL library.
 *
 * @see sl_rtl_service_create_cs_estimator
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_set_cs_params(
  sl_rtl_service_cs_inst_t *inst,
  const sl_rtl_cs_params *params);

/**************************************************************************//**
 * Create the estimator for an instance.
 *
 * Thread-safe: acquires the parent context's RTA guard internally.
 * Must be called after sl_rtl_service_set_cs_algo_mode(),
 * sl_rtl_service_set_cs_mode(), and sl_rtl_service_set_cs_params().
 *
 * @param[in] inst  RTL service CS instance.
 *
 * @return SL_RTL_ERROR_SUCCESS   Estimator created successfully.
 * @return SL_RTL_ERROR_ARGUMENT  @p inst is NULL or not in use.
 * @return SL_RTL_ERROR_INTERNAL  Guard acquisition failed.
 * @return Other values forwarded from the underlying RTL library.
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_create_cs_estimator(
  sl_rtl_service_cs_inst_t *inst);

/**************************************************************************//**
 * Set an estimator parameter for an instance.
 *
 * Thread-safe: acquires the parent context's RTA guard internally.
 * May be called at any time after the estimator is created, including
 * while processing is in progress.
 *
 * @param[in] inst   RTL service CS instance.
 * @param[in] param  Estimator parameter to set.
 *
 * @return SL_RTL_ERROR_SUCCESS   Parameter set successfully.
 * @return SL_RTL_ERROR_ARGUMENT  @p inst is NULL or not in use, or
 *                                @p param is NULL.
 * @return SL_RTL_ERROR_INTERNAL  Guard acquisition failed.
 * @return Other values forwarded from the underlying RTL library.
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_set_cs_estimator_param(
  sl_rtl_service_cs_inst_t *inst,
  const sl_rtl_cs_estimator_param *param);

/**************************************************************************//**
 * Enable RTL library structured logging for an instance.
 *
 * Thread-safe: acquires the parent context's RTA guard internally.
 * Must be called after sl_rtl_service_create_cs_instance() and
 * before sl_rtl_service_create_cs_estimator(). Has no effect unless
 * sl_rtl_log_init() and sl_rtl_log_configure() have been called first.
 *
 * @param[in] inst  RTL service CS instance.
 *
 * @return SL_RTL_ERROR_SUCCESS   Logging enabled for this instance.
 * @return SL_RTL_ERROR_ARGUMENT  @p inst is NULL or not in use.
 * @return SL_RTL_ERROR_INTERNAL  Guard acquisition failed.
 * @return Other values forwarded from the underlying RTL library
 *         (e.g. SL_RTL_ERROR_ESTIMATOR_ALREADY_CREATED if called
 *         after sl_rtl_service_create_cs_estimator).
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_enable_cs_log(
  sl_rtl_service_cs_inst_t *inst);

// -----------------------------------------------------------------------------
// Processing

/**************************************************************************//**
 * Submit CS procedure data for processing on an instance.
 *
 * Thread-safe: may be called from any task context.
 * The request is queued internally and processed by the RTL processing
 * task. The caller must keep @p procedure valid until the result
 * callback fires for this instance.
 *
 * At most one request per instance may be pending at a time. Requests
 * for different instances are independent and may be submitted
 * concurrently.
 *
 * @note In bare-metal mode the callback fires synchronously before this
 *       function returns, so stack-allocated procedure data is safe.
 *       In RTOS mode the callback fires asynchronously from the RTL
 *       task; the data must remain valid beyond the caller's stack frame.
 *
 * @param[in] inst       RTL service CS instance.
 * @param[in] procedure  CS procedure data (referenced by pointer, not
 *                       copied).
 *
 * @return SL_RTL_ERROR_SUCCESS    Request accepted and queued.
 * @return SL_RTL_ERROR_ARGUMENT   @p inst is NULL or not in use, or
 *                                 @p procedure is NULL.
 * @return SL_RTL_ERROR_INTERNAL   Guard acquisition failed.
 * @return SL_RTL_ERROR_QUEUE_FULL This instance already has a pending
 *                                 request.
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_process_cs(
  sl_rtl_service_cs_inst_t *inst,
  const sl_rtl_cs_procedure *procedure);

/**************************************************************************//**
 * Submit RAS procedure data for processing on an instance.
 *
 * Thread-safe: may be called from any task context.
 * Behaves identically to sl_rtl_service_process_cs() but accepts
 * Ranging Service (RAS) procedure data. The caller must keep
 * @p procedure valid until the result callback fires. At most one
 * request per instance may be pending at a time.
 *
 * @note In bare-metal mode the callback fires synchronously before this
 *       function returns. In RTOS mode the callback fires
 *       asynchronously from the RTL task.
 *
 * @param[in] inst       RTL service CS instance.
 * @param[in] procedure  RAS procedure data (referenced by pointer, not
 *                       copied).
 *
 * @return SL_RTL_ERROR_SUCCESS    Request accepted and queued.
 * @return SL_RTL_ERROR_ARGUMENT   @p inst is NULL or not in use, or
 *                                 @p procedure is NULL.
 * @return SL_RTL_ERROR_INTERNAL   Guard acquisition failed.
 * @return SL_RTL_ERROR_QUEUE_FULL This instance already has a pending
 *                                 request.
 *
 * @see sl_rtl_service_process_cs
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_process_ras(
  sl_rtl_service_cs_inst_t *inst,
  const sl_rtl_ras_procedure *procedure);

// -----------------------------------------------------------------------------
// Result queries (call from result callback only)

/**************************************************************************//**
 * Get distance estimate from a processing result.
 *
 * @warning Must only be called from within the result callback.
 *          The @p result handle is valid only for the duration of that
 *          callback invocation; behaviour is undefined if called outside.
 *
 * @param[in]  result        Opaque result handle from the callback.
 * @param[in]  estimate_type Type of distance estimate to retrieve.
 * @param[in]  estimate_mode Mode of distance estimate to retrieve.
 * @param[out] distance      Receives the distance value in meters.
 *
 * @return SL_RTL_ERROR_SUCCESS   Estimate retrieved successfully.
 * @return SL_RTL_ERROR_ARGUMENT  @p result or @p distance is NULL.
 * @return Other values forwarded from the underlying RTL library.
 *
 * @see sl_rtl_service_cs_result_cb_t
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_get_cs_distance_estimate(
  const sl_rtl_service_cs_result_t *result,
  sl_rtl_cs_distance_estimate_type estimate_type,
  sl_rtl_cs_distance_estimate_mode estimate_mode,
  float *distance);

/**************************************************************************//**
 * Get distance estimate confidence.
 *
 * @warning Must only be called from within the result callback.
 *          The @p result handle is valid only for the duration of that
 *          callback invocation; behaviour is undefined if called outside.
 *
 * @param[in]  result          Opaque result handle from the callback.
 * @param[in]  confidence_type Type of confidence estimate to retrieve.
 * @param[in]  confidence_mode Mode of confidence estimate to retrieve.
 * @param[out] confidence      Receives a confidence value between 0.0
 *                             (lowest) and 1.0 (highest).
 *
 * @return SL_RTL_ERROR_SUCCESS   Confidence retrieved successfully.
 * @return SL_RTL_ERROR_ARGUMENT  @p result or @p confidence is NULL.
 * @return Other values forwarded from the underlying RTL library.
 *
 * @see sl_rtl_service_cs_result_cb_t
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_get_cs_distance_estimate_confidence(
  const sl_rtl_service_cs_result_t *result,
  sl_rtl_cs_distance_estimate_confidence_type confidence_type,
  sl_rtl_cs_distance_estimate_confidence_mode confidence_mode,
  float *confidence);

/**************************************************************************//**
 * Get distance estimate extended information.
 *
 * @warning Must only be called from within the result callback.
 *          The @p result handle is valid only for the duration of that
 *          callback invocation; behaviour is undefined if called outside.
 *
 * @param[in]  result             Opaque result handle from the callback.
 * @param[in]  extended_info_type Type of extended information to retrieve.
 * @param[out] extended_info      Receives the extended information value.
 *
 * @return SL_RTL_ERROR_SUCCESS   Information retrieved successfully.
 * @return SL_RTL_ERROR_ARGUMENT  @p result or @p extended_info is NULL.
 * @return Other values forwarded from the underlying RTL library.
 *
 * @see sl_rtl_service_cs_result_cb_t
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_service_get_cs_distance_estimate_extended_info(
  const sl_rtl_service_cs_result_t *result,
  sl_rtl_cs_distance_estimate_extended_info_type extended_info_type,
  float *extended_info);

/** @} */ // sl_rtl_service

#endif // SL_RTL_SERVICE_H
