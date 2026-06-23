/***************************************************************************//**
 * @file
 * @brief Real-Time Locationing Service implementation (app_rta based)
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
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

#include "sl_assert.h"
#include "sl_memory_manager.h"
#include "sl_rtl_service.h"
#include "sli_rtl_clib_cs_api.h"
#include "sli_rtl_clib_ras_api.h"
#include "app_rta.h"
#include "sl_status.h"

#ifdef CONFIGURATION_HEADER
#include CONFIGURATION_HEADER
#else
#include "sl_rtl_service_config.h"
#endif

// Max bare-metal reentrant step depth (callback -> process -> signal -> step).
// Prevents unbounded recursion; only relevant in bare-metal / synchronous
// dispatch since RTOS signals are asynchronous.
#ifndef SLI_RTL_SERVICE_MAX_STEP_DEPTH
#define SLI_RTL_SERVICE_MAX_STEP_DEPTH  2u
#endif

// -----------------------------------------------------------------------------
// Internal types

typedef enum {
  SLI_REQUEST_CS = 0,
  SLI_REQUEST_RAS = 1,
} sli_rtl_request_type_t;

struct sl_rtl_service_cs_inst {
  sl_rtl_cs_libitem        libitem;
  sl_rtl_service_cs_ctx_t *parent;
  // Monotonic slot identity used to distinguish a destroyed instance from
  // a later instance that reuses the same slot after the guard is released.
  uint32_t                 generation;
  bool                     in_use;
  bool                     request_pending;
  bool                     in_callback;
  sli_rtl_request_type_t   request_type;
  union {
    const sl_rtl_cs_procedure  *cs;
    const sl_rtl_ras_procedure *ras;
  } pending_procedure;
};

struct sl_rtl_service_cs_ctx {
  app_rta_context_t          rta_ctx;
  sl_rtl_service_cs_config_t config;
  sl_rtl_service_cs_inst_t   instances[SL_RTL_SERVICE_CS_MAX_INSTANCES];
};

struct sl_rtl_service_cs_result {
  sl_rtl_cs_libitem libitem;
};

// -----------------------------------------------------------------------------
// Static state (single RTL RTA context; step function has no user pointer)

static sl_rtl_service_cs_ctx_t *s_service_ctx;
static app_rta_context_t s_rta_ctx_handle = APP_RTA_INVALID_CONTEXT;
static unsigned s_step_depth;

// -----------------------------------------------------------------------------
// Helpers

static void sli_rtl_service_step_cs(void);

static enum sl_rtl_error_code sli_create_rta_context(void)
{
  app_rta_config_t rta_cfg;
  memset(&rta_cfg, 0, sizeof(rta_cfg));
  rta_cfg.requirement.runtime_separate = 1;
  rta_cfg.requirement.guard = 1;
  rta_cfg.requirement.signal = 1;
  rta_cfg.step = sli_rtl_service_step_cs;
  rta_cfg.priority = (app_rta_priority_t)SL_RTL_SERVICE_CS_TASK_PRIO;
  rta_cfg.stack_size = (size_t)SL_RTL_SERVICE_CS_TASK_STACK_SIZE;
  rta_cfg.wait_for_guard = SL_RTL_SERVICE_CS_GUARD_WAIT;

  sl_status_t sc = app_rta_create_context(&rta_cfg, &s_rta_ctx_handle);
  if (sc == SL_STATUS_OK) {
    return SL_RTL_ERROR_SUCCESS;
  }

  s_rta_ctx_handle = APP_RTA_INVALID_CONTEXT;
  if (sc == SL_STATUS_ALLOCATION_FAILED) {
    return SL_RTL_ERROR_OUT_OF_MEMORY;
  }
  return SL_RTL_ERROR_INTERNAL;
}

static enum sl_rtl_error_code sli_map_sl_status(sl_status_t status)
{
  switch (status) {
    case SL_STATUS_OK:
      return SL_RTL_ERROR_SUCCESS;
    case SL_STATUS_ALLOCATION_FAILED:
      return SL_RTL_ERROR_OUT_OF_MEMORY;
    case SL_STATUS_NULL_POINTER:
      return SL_RTL_ERROR_ARGUMENT;
    default:
      return SL_RTL_ERROR_INTERNAL;
  }
}

static void sli_clear_pending_request(sl_rtl_service_cs_inst_t *inst)
{
  inst->request_pending = false;
  inst->pending_procedure.cs = NULL;
}

static void sli_clear_pending_request_if_same_instance(sl_rtl_service_cs_inst_t *inst,
                                                       uint32_t                  generation)
{
  if (inst->in_use && (inst->generation == generation)) {
    sli_clear_pending_request(inst);
  }
}

static void sli_reset_instance_state(sl_rtl_service_cs_inst_t *inst)
{
  memset(&inst->libitem, 0, sizeof(inst->libitem));
  inst->in_use = false;
  inst->request_pending = false;
  inst->in_callback = false;
  inst->request_type = SLI_REQUEST_CS;
  inst->pending_procedure.cs = NULL;
}

static void sli_activate_instance_state(sl_rtl_service_cs_inst_t *inst)
{
  sli_reset_instance_state(inst);
  inst->generation++;
  if (inst->generation == 0u) {
    inst->generation = 1u;
  }
  inst->in_use = true;
}

static enum sl_rtl_error_code sli_lock_live_instance(sl_rtl_service_cs_inst_t  *inst,
                                                     sl_rtl_service_cs_ctx_t **ctx_out)
{
  if ((inst == NULL) || (ctx_out == NULL)) {
    return SL_RTL_ERROR_ARGUMENT;
  }

  sl_rtl_service_cs_ctx_t *ctx = inst->parent;
  if ((ctx == NULL) || (ctx != s_service_ctx) || (ctx->rta_ctx == APP_RTA_INVALID_CONTEXT)) {
    return SL_RTL_ERROR_ARGUMENT;
  }

  if (app_rta_acquire(ctx->rta_ctx) != SL_STATUS_OK) {
    return SL_RTL_ERROR_INTERNAL;
  }

  if (!inst->in_use || (inst->parent != ctx)) {
    (void)app_rta_release(ctx->rta_ctx);
    return SL_RTL_ERROR_ARGUMENT;
  }

  *ctx_out = ctx;
  return SL_RTL_ERROR_SUCCESS;
}

static void sli_destroy_instance_locked(sl_rtl_service_cs_inst_t *inst)
{
  (void)sli_rtl_cs_deinit(&inst->libitem);
  sli_reset_instance_state(inst);
}

static inline sl_rtl_cs_libitem *sli_result_libitem(
  const sl_rtl_service_cs_result_t *result)
{
  // Safe: the result originates from a non-const stack variable in step_cs.
  return (sl_rtl_cs_libitem *)&(
    (const struct sl_rtl_service_cs_result *)result)->libitem;
}

// -----------------------------------------------------------------------------
// Step (runs on RTA runtime thread / bare-metal proceed)

static void sli_rtl_service_step_cs(void)
{
  sl_rtl_service_cs_ctx_t *ctx = s_service_ctx;
  if ((ctx == NULL) || !app_rta_is_enabled(ctx->rta_ctx)) {
    return;
  }

  if (s_step_depth >= SLI_RTL_SERVICE_MAX_STEP_DEPTH) {
    return;
  }
  s_step_depth++;

  while (app_rta_signal_check(ctx->rta_ctx) == SL_STATUS_OK) {
    /* drain signal tokens (RTOS builds) */
  }

  if (app_rta_acquire(ctx->rta_ctx) != SL_STATUS_OK) {
    s_step_depth--;
    return;
  }

  for (unsigned i = 0; i < SL_RTL_SERVICE_CS_MAX_INSTANCES; i++) {
    sl_rtl_service_cs_inst_t *inst = &ctx->instances[i];
    if (!inst->in_use || !inst->request_pending) {
      continue;
    }

    inst->request_pending = false;

    sl_rtl_service_cs_result_t res;
    memset(&res, 0, sizeof(res));
    res.libitem = inst->libitem;

    enum sl_rtl_error_code rc;
    if (inst->request_type == SLI_REQUEST_CS) {
      rc = sli_rtl_cs_process(&inst->libitem, 1, inst->pending_procedure.cs);
    } else {
      rc = sli_rtl_ras_process(&inst->libitem, 1, inst->pending_procedure.ras);
    }

    // Release the guard before the callback so the application can call
    // guard-acquiring APIs (e.g. process_cs) from within the callback.
    // in_callback is written without the guard, which is safe: only this
    // step function (single RTL task) writes the flag, and
    // destroy_cs_instance reads it while holding the guard — serialised
    // against the re-acquire below.
    inst->in_callback = true;
    (void)app_rta_release(ctx->rta_ctx);
    if (ctx->config.result_cb != NULL) {
      ctx->config.result_cb(inst, &res, rc, ctx->config.user_data);
    }
    inst->in_callback = false;

    if (app_rta_acquire(ctx->rta_ctx) != SL_STATUS_OK) {
      s_step_depth--;
      return;
    }
  }

  (void)app_rta_release(ctx->rta_ctx);
  s_step_depth--;
}

// -----------------------------------------------------------------------------
// RTA contributor init (called from generated app_rta_init.c)

void sl_rtl_service_rta_init_cs(void)
{
#ifndef SL_CATALOG_KERNEL_PRESENT
  // In bare-metal, app_rta_internal_init() may be called multiple times,
  // wiping ctx_list each time. Reset the handle so the context is
  // re-created and re-added to the list on every invocation.
  s_rta_ctx_handle = APP_RTA_INVALID_CONTEXT;
#else
  // In RTOS the context owns a live task; only create it once.
  if (s_rta_ctx_handle != APP_RTA_INVALID_CONTEXT) {
    return;
  }
#endif
  enum sl_rtl_error_code rc = sli_create_rta_context();
  EFM_ASSERT(rc == SL_RTL_ERROR_SUCCESS);
}

// -----------------------------------------------------------------------------
// Test helper (exposes the module-level RTA handle for host unit tests)

app_rta_context_t sli_rtl_service_get_rta_ctx(void)
{
  return s_rta_ctx_handle;
}

void sli_rtl_service_reset_rta_ctx(void)
{
  s_rta_ctx_handle = APP_RTA_INVALID_CONTEXT;
}

// -----------------------------------------------------------------------------
// Context lifecycle

enum sl_rtl_error_code sl_rtl_service_init_cs(const sl_rtl_service_cs_config_t *config,
                                              sl_rtl_service_cs_ctx_t         **ctx_out)
{
  if ((config == NULL) || (ctx_out == NULL) || (config->result_cb == NULL)) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  if (s_service_ctx != NULL) {
    return SL_RTL_ERROR_INTERNAL;
  }
  bool rta_ctx_created = false;
  if (s_rta_ctx_handle == APP_RTA_INVALID_CONTEXT) {
    enum sl_rtl_error_code rc = sli_create_rta_context();
    if (rc != SL_RTL_ERROR_SUCCESS) {
      return rc;
    }
    rta_ctx_created = true;
  }

  sl_rtl_service_cs_ctx_t *ctx = (sl_rtl_service_cs_ctx_t *)sl_calloc(1, sizeof(*ctx));
  if (ctx == NULL) {
    if (rta_ctx_created) {
      app_rta_context_t rta_ctx = s_rta_ctx_handle;
      s_rta_ctx_handle = APP_RTA_INVALID_CONTEXT;
      (void)app_rta_enable_context(rta_ctx, false);
    }
    return SL_RTL_ERROR_OUT_OF_MEMORY;
  }

  memcpy(&ctx->config, config, sizeof(ctx->config));
  ctx->rta_ctx = s_rta_ctx_handle;
  for (unsigned i = 0; i < SL_RTL_SERVICE_CS_MAX_INSTANCES; i++) {
    ctx->instances[i].parent = ctx;
  }

  s_service_ctx = ctx;
  *ctx_out = ctx;
  return SL_RTL_ERROR_SUCCESS;
}

enum sl_rtl_error_code sl_rtl_service_deinit_cs(sl_rtl_service_cs_ctx_t *ctx)
{
  if (ctx == NULL) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  if (s_service_ctx != ctx) {
    return SL_RTL_ERROR_ARGUMENT;
  }

  if (ctx->rta_ctx != APP_RTA_INVALID_CONTEXT) {
    app_rta_context_t rta_ctx = ctx->rta_ctx;

    if (app_rta_acquire(rta_ctx) != SL_STATUS_OK) {
      return SL_RTL_ERROR_INTERNAL;
    }

    for (unsigned i = 0; i < SL_RTL_SERVICE_CS_MAX_INSTANCES; i++) {
      sl_rtl_service_cs_inst_t *inst = &ctx->instances[i];
      if (inst->in_use && inst->in_callback) {
        (void)app_rta_release(rta_ctx);
        return SL_RTL_ERROR_INTERNAL;
      }
    }

    for (unsigned i = 0; i < SL_RTL_SERVICE_CS_MAX_INSTANCES; i++) {
      sl_rtl_service_cs_inst_t *inst = &ctx->instances[i];
      if (inst->in_use) {
        sli_destroy_instance_locked(inst);
      }
    }

    ctx->rta_ctx = APP_RTA_INVALID_CONTEXT;
    s_service_ctx = NULL;
    s_rta_ctx_handle = APP_RTA_INVALID_CONTEXT;
    (void)app_rta_release(rta_ctx);
    (void)app_rta_enable_context(rta_ctx, false);
  } else {
    s_service_ctx = NULL;
  }

  sl_free(ctx);
  return SL_RTL_ERROR_SUCCESS;
}

// -----------------------------------------------------------------------------
// Instance lifecycle

enum sl_rtl_error_code sl_rtl_service_create_cs_instance(sl_rtl_service_cs_ctx_t  *ctx,
                                                         sl_rtl_service_cs_inst_t **inst_out)
{
  if ((ctx == NULL) || (inst_out == NULL)) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  if ((ctx != s_service_ctx) || (ctx->rta_ctx == APP_RTA_INVALID_CONTEXT)) {
    return SL_RTL_ERROR_ARGUMENT;
  }

  if (app_rta_acquire(ctx->rta_ctx) != SL_STATUS_OK) {
    return SL_RTL_ERROR_INTERNAL;
  }

  sl_rtl_service_cs_inst_t *slot = NULL;
  for (unsigned i = 0; i < SL_RTL_SERVICE_CS_MAX_INSTANCES; i++) {
    if (!ctx->instances[i].in_use) {
      slot = &ctx->instances[i];
      break;
    }
  }
  if (slot == NULL) {
    (void)app_rta_release(ctx->rta_ctx);
    return SL_RTL_ERROR_OUT_OF_MEMORY;
  }

  sli_activate_instance_state(slot);

  enum sl_rtl_error_code rc = sli_rtl_cs_init(&slot->libitem);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    sli_reset_instance_state(slot);
    (void)app_rta_release(ctx->rta_ctx);
    return rc;
  }

  (void)app_rta_release(ctx->rta_ctx);
  *inst_out = (sl_rtl_service_cs_inst_t *)slot;
  return SL_RTL_ERROR_SUCCESS;
}

enum sl_rtl_error_code sl_rtl_service_destroy_cs_instance(sl_rtl_service_cs_inst_t *inst)
{
  sl_rtl_service_cs_ctx_t *ctx = NULL;
  enum sl_rtl_error_code rc = sli_lock_live_instance(inst, &ctx);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    return rc;
  }

  if (inst->in_callback) {
    (void)app_rta_release(ctx->rta_ctx);
    return SL_RTL_ERROR_INTERNAL;
  }
  sli_destroy_instance_locked(inst);

  (void)app_rta_release(ctx->rta_ctx);
  return SL_RTL_ERROR_SUCCESS;
}

// -----------------------------------------------------------------------------
// Configuration

enum sl_rtl_error_code sl_rtl_service_set_cs_algo_mode(sl_rtl_service_cs_inst_t *inst,
                                                       sl_rtl_cs_algo_mode        mode)
{
  sl_rtl_service_cs_ctx_t *ctx = NULL;
  enum sl_rtl_error_code rc = sli_lock_live_instance(inst, &ctx);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    return rc;
  }
  rc = sli_rtl_cs_set_algo_mode(&inst->libitem, mode);
  (void)app_rta_release(ctx->rta_ctx);
  return rc;
}

enum sl_rtl_error_code sl_rtl_service_set_cs_mode(sl_rtl_service_cs_inst_t *inst,
                                                  sl_rtl_cs_mode             main_mode,
                                                  sl_rtl_cs_mode             sub_mode)
{
  sl_rtl_service_cs_ctx_t *ctx = NULL;
  enum sl_rtl_error_code rc = sli_lock_live_instance(inst, &ctx);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    return rc;
  }
  rc = sli_rtl_cs_set_cs_mode(&inst->libitem, main_mode, sub_mode);
  (void)app_rta_release(ctx->rta_ctx);
  return rc;
}

enum sl_rtl_error_code sl_rtl_service_set_cs_params(sl_rtl_service_cs_inst_t *inst,
                                                    const sl_rtl_cs_params    *params)
{
  if (params == NULL) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  sl_rtl_service_cs_ctx_t *ctx = NULL;
  enum sl_rtl_error_code rc = sli_lock_live_instance(inst, &ctx);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    return rc;
  }
  rc = sli_rtl_cs_set_cs_params(&inst->libitem, params);
  (void)app_rta_release(ctx->rta_ctx);
  return rc;
}

enum sl_rtl_error_code sl_rtl_service_create_cs_estimator(sl_rtl_service_cs_inst_t *inst)
{
  sl_rtl_service_cs_ctx_t *ctx = NULL;
  enum sl_rtl_error_code rc = sli_lock_live_instance(inst, &ctx);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    return rc;
  }
  rc = sli_rtl_cs_create_estimator(&inst->libitem);
  (void)app_rta_release(ctx->rta_ctx);
  return rc;
}

enum sl_rtl_error_code sl_rtl_service_enable_cs_log(sl_rtl_service_cs_inst_t *inst)
{
  sl_rtl_service_cs_ctx_t *ctx = NULL;
  enum sl_rtl_error_code rc = sli_lock_live_instance(inst, &ctx);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    return rc;
  }
  rc = sli_rtl_cs_log_enable(&inst->libitem);
  (void)app_rta_release(ctx->rta_ctx);
  return rc;
}

enum sl_rtl_error_code sl_rtl_service_set_cs_estimator_param(sl_rtl_service_cs_inst_t    *inst,
                                                             const sl_rtl_cs_estimator_param *param)
{
  if (param == NULL) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  sl_rtl_service_cs_ctx_t *ctx = NULL;
  enum sl_rtl_error_code rc = sli_lock_live_instance(inst, &ctx);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    return rc;
  }
  rc = sli_rtl_cs_set_estimator_param(&inst->libitem, param);
  (void)app_rta_release(ctx->rta_ctx);
  return rc;
}

// -----------------------------------------------------------------------------
// Processing

enum sl_rtl_error_code sl_rtl_service_process_cs(sl_rtl_service_cs_inst_t    *inst,
                                                 const sl_rtl_cs_procedure *procedure)
{
  if (procedure == NULL) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  sl_rtl_service_cs_ctx_t *ctx = NULL;
  enum sl_rtl_error_code rc = sli_lock_live_instance(inst, &ctx);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    return rc;
  }
  uint32_t generation = inst->generation;

  if (inst->request_pending) {
    (void)app_rta_release(ctx->rta_ctx);
    return SL_RTL_ERROR_QUEUE_FULL;
  }
  inst->request_pending = true;
  inst->request_type = SLI_REQUEST_CS;
  inst->pending_procedure.cs = procedure;
  (void)app_rta_release(ctx->rta_ctx);

  sl_status_t sc = app_rta_signal(ctx->rta_ctx);
  if (sc != SL_STATUS_OK) {
    sl_status_t acq = app_rta_acquire(ctx->rta_ctx);
    EFM_ASSERT(acq == SL_STATUS_OK);
    sli_clear_pending_request_if_same_instance(inst, generation);
    (void)app_rta_release(ctx->rta_ctx);
    return sli_map_sl_status(sc);
  }
  return SL_RTL_ERROR_SUCCESS;
}

enum sl_rtl_error_code sl_rtl_service_process_ras(sl_rtl_service_cs_inst_t     *inst,
                                                  const sl_rtl_ras_procedure *procedure)
{
  if (procedure == NULL) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  sl_rtl_service_cs_ctx_t *ctx = NULL;
  enum sl_rtl_error_code rc = sli_lock_live_instance(inst, &ctx);
  if (rc != SL_RTL_ERROR_SUCCESS) {
    return rc;
  }
  uint32_t generation = inst->generation;

  if (inst->request_pending) {
    (void)app_rta_release(ctx->rta_ctx);
    return SL_RTL_ERROR_QUEUE_FULL;
  }
  inst->request_pending = true;
  inst->request_type = SLI_REQUEST_RAS;
  inst->pending_procedure.ras = procedure;
  (void)app_rta_release(ctx->rta_ctx);

  sl_status_t sc = app_rta_signal(ctx->rta_ctx);
  if (sc != SL_STATUS_OK) {
    sl_status_t acq = app_rta_acquire(ctx->rta_ctx);
    EFM_ASSERT(acq == SL_STATUS_OK);
    sli_clear_pending_request_if_same_instance(inst, generation);
    (void)app_rta_release(ctx->rta_ctx);
    return sli_map_sl_status(sc);
  }
  return SL_RTL_ERROR_SUCCESS;
}

// -----------------------------------------------------------------------------
// Result queries (callback only)

enum sl_rtl_error_code sl_rtl_service_get_cs_distance_estimate(
  const sl_rtl_service_cs_result_t     *result,
  sl_rtl_cs_distance_estimate_type      estimate_type,
  sl_rtl_cs_distance_estimate_mode      estimate_mode,
  float                                *distance)
{
  if ((result == NULL) || (distance == NULL)) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  return sli_rtl_cs_get_distance_estimate(sli_result_libitem(result),
                                          estimate_type,
                                          estimate_mode,
                                          distance);
}

enum sl_rtl_error_code sl_rtl_service_get_cs_distance_estimate_confidence(
  const sl_rtl_service_cs_result_t           *result,
  sl_rtl_cs_distance_estimate_confidence_type confidence_type,
  sl_rtl_cs_distance_estimate_confidence_mode confidence_mode,
  float                                      *confidence)
{
  if ((result == NULL) || (confidence == NULL)) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  return sli_rtl_cs_get_distance_estimate_confidence(sli_result_libitem(result),
                                                     confidence_type,
                                                     confidence_mode,
                                                     confidence);
}

enum sl_rtl_error_code sl_rtl_service_get_cs_distance_estimate_extended_info(
  const sl_rtl_service_cs_result_t              *result,
  sl_rtl_cs_distance_estimate_extended_info_type extended_info_type,
  float                                         *extended_info)
{
  if ((result == NULL) || (extended_info == NULL)) {
    return SL_RTL_ERROR_ARGUMENT;
  }
  return sli_rtl_cs_get_distance_estimate_extended_info(sli_result_libitem(result),
                                                        extended_info_type,
                                                        extended_info);
}
