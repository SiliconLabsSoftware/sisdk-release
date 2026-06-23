/***************************************************************************//**
 * @file
 * @brief Internal CS API declarations
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

#ifndef SLI_RTL_CLIB_CS_API_H
#define SLI_RTL_CLIB_CS_API_H

#ifdef __cplusplus
extern "C" {
#endif

enum sl_rtl_error_code sli_rtl_cs_init(sl_rtl_cs_libitem *item);
enum sl_rtl_error_code sli_rtl_cs_deinit(sl_rtl_cs_libitem *item);
enum sl_rtl_error_code sli_rtl_cs_set_algo_mode(sl_rtl_cs_libitem *item,
                                                const sl_rtl_cs_algo_mode mode);
enum sl_rtl_error_code sli_rtl_cs_set_cs_mode(sl_rtl_cs_libitem *item,
                                              const sl_rtl_cs_mode main_mode,
                                              const sl_rtl_cs_mode sub_mode);
enum sl_rtl_error_code sli_rtl_cs_set_cs_params(sl_rtl_cs_libitem *item,
                                                const sl_rtl_cs_params *params);
enum sl_rtl_error_code sli_rtl_cs_create_estimator(sl_rtl_cs_libitem *item);
enum sl_rtl_error_code sli_rtl_cs_set_estimator_param(
  sl_rtl_cs_libitem *item,
  const sl_rtl_cs_estimator_param *param);
enum sl_rtl_error_code sli_rtl_cs_process(
  sl_rtl_cs_libitem *item,
  const uint8_t num_procedures,
  const sl_rtl_cs_procedure *procedure_data);
enum sl_rtl_error_code sli_rtl_cs_get_distance_estimate(
  sl_rtl_cs_libitem *item,
  const sl_rtl_cs_distance_estimate_type estimate_type,
  const sl_rtl_cs_distance_estimate_mode estimate_mode,
  float *distance);
enum sl_rtl_error_code sli_rtl_cs_get_distance_estimate_confidence(
  sl_rtl_cs_libitem *item,
  const sl_rtl_cs_distance_estimate_confidence_type confidence_type,
  const sl_rtl_cs_distance_estimate_confidence_mode confidence_mode,
  float *confidence);
enum sl_rtl_error_code sli_rtl_cs_get_distance_estimate_extended_info(
  sl_rtl_cs_libitem *item,
  const sl_rtl_cs_distance_estimate_extended_info_type extended_info_type,
  float *extended_info);
enum sl_rtl_error_code sli_rtl_cs_log_enable(sl_rtl_cs_libitem *item);
enum sl_rtl_error_code sli_rtl_cs_log_disable(sl_rtl_cs_libitem *item);
enum sl_rtl_error_code sli_rtl_cs_log_get_instance_id(sl_rtl_cs_libitem *item,
                                                      uint8_t *instance_id);

#ifdef __cplusplus
}
#endif

#endif /* SLI_RTL_CLIB_CS_API_H */
