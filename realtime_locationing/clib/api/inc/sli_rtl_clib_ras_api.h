/***************************************************************************//**
 * @file
 * @brief Internal RAS API declarations
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

#ifndef SLI_RTL_CLIB_RAS_API_H
#define SLI_RTL_CLIB_RAS_API_H

#ifdef __cplusplus
extern "C" {
#endif

enum sl_rtl_error_code sli_rtl_ras_process(
  sl_rtl_cs_libitem *item,
  const uint8_t num_procedures,
  const sl_rtl_ras_procedure *procedure_data);

#ifdef __cplusplus
}
#endif

#endif /* SLI_RTL_CLIB_RAS_API_H */
