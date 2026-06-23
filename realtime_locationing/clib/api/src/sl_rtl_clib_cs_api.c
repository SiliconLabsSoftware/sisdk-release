/***************************************************************************//**
 * @file
 * @brief Legacy CS API wrappers
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/

#ifdef SL_COMPONENT_CATALOG_PRESENT
#include "sl_component_catalog.h"
#endif
#include "sl_rtl_clib_api.h"

#if defined(SL_CATALOG_KERNEL_PRESENT) || !defined(SL_CATALOG_RTL_LIB_PRESENT)
#define SLI_RTL_CS_API_DISABLED
#endif

#ifndef SLI_RTL_CS_API_DISABLED
#include "sli_rtl_clib_cs_api.h"
#endif

enum sl_rtl_error_code sl_rtl_cs_init(sl_rtl_cs_libitem *item)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_init(item);
#endif
}

enum sl_rtl_error_code sl_rtl_cs_deinit(sl_rtl_cs_libitem *item)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_deinit(item);
#endif
}

enum sl_rtl_error_code sl_rtl_cs_set_algo_mode(sl_rtl_cs_libitem *item,
                                               const sl_rtl_cs_algo_mode mode)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  (void)mode;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_set_algo_mode(item, mode);
#endif
}

enum sl_rtl_error_code sl_rtl_cs_set_cs_mode(sl_rtl_cs_libitem *item,
                                             const sl_rtl_cs_mode main_mode,
                                             const sl_rtl_cs_mode sub_mode)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  (void)main_mode;
  (void)sub_mode;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_set_cs_mode(item, main_mode, sub_mode);
#endif
}

enum sl_rtl_error_code
sl_rtl_cs_set_cs_params(sl_rtl_cs_libitem *item,
                        const sl_rtl_cs_params *parameters)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  (void)parameters;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_set_cs_params(item, parameters);
#endif
}

enum sl_rtl_error_code sl_rtl_cs_create_estimator(sl_rtl_cs_libitem *item)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_create_estimator(item);
#endif
}

enum sl_rtl_error_code
sl_rtl_cs_set_estimator_param(sl_rtl_cs_libitem *item,
                              const sl_rtl_cs_estimator_param *param)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  (void)param;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_set_estimator_param(item, param);
#endif
}

enum sl_rtl_error_code
sl_rtl_cs_process(sl_rtl_cs_libitem *item,
                  const uint8_t num_procedures,
                  const sl_rtl_cs_procedure *procedure_data)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  (void)num_procedures;
  (void)procedure_data;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_process(item, num_procedures, procedure_data);
#endif
}

enum sl_rtl_error_code
sl_rtl_cs_get_distance_estimate(
  sl_rtl_cs_libitem *item,
  const sl_rtl_cs_distance_estimate_type estimate_type,
  const sl_rtl_cs_distance_estimate_mode estimate_mode,
  float *distance)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  (void)estimate_type;
  (void)estimate_mode;
  (void)distance;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_get_distance_estimate(item, estimate_type,
                                          estimate_mode, distance);
#endif
}

enum sl_rtl_error_code
sl_rtl_cs_get_distance_estimate_confidence(
  sl_rtl_cs_libitem *item,
  const sl_rtl_cs_distance_estimate_confidence_type confidence_type,
  const sl_rtl_cs_distance_estimate_confidence_mode confidence_mode,
  float *confidence)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  (void)confidence_type;
  (void)confidence_mode;
  (void)confidence;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_get_distance_estimate_confidence(item, confidence_type,
                                                     confidence_mode,
                                                     confidence);
#endif
}

enum sl_rtl_error_code
sl_rtl_cs_get_distance_estimate_extended_info(
  sl_rtl_cs_libitem *item,
  const sl_rtl_cs_distance_estimate_extended_info_type extended_info_type,
  float *extended_info)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  (void)extended_info_type;
  (void)extended_info;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_get_distance_estimate_extended_info(item,
                                                        extended_info_type,
                                                        extended_info);
#endif
}

enum sl_rtl_error_code sl_rtl_cs_log_enable(sl_rtl_cs_libitem *item)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_log_enable(item);
#endif
}

enum sl_rtl_error_code sl_rtl_cs_log_disable(sl_rtl_cs_libitem *item)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_log_disable(item);
#endif
}

enum sl_rtl_error_code sl_rtl_cs_log_get_instance_id(sl_rtl_cs_libitem *item,
                                                     uint8_t *instance_id)
{
#ifdef SLI_RTL_CS_API_DISABLED
  (void)item;
  (void)instance_id;
  return SL_RTL_ERROR_FEATURE_NOT_SUPPORTED;
#else
  return sli_rtl_cs_log_get_instance_id(item, instance_id);
#endif
}
