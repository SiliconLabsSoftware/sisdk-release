/***************************************************************************//**
 * @file
 * @brief SMP two-page switch record for dual-application boot selection.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc.  Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement.  This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/
#ifndef BTL_SMP_SWITCH_RECORD_H
#define BTL_SMP_SWITCH_RECORD_H

#include <stdint.h>
#ifdef BOOTLOADER_ENABLE 
#include "core/btl_bootload.h"
#endif

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************//**
 * @addtogroup smp_switch SMP Two-Page Switch Record
 * @brief Bootloader support for selecting application 1 or 2 from a two-page
 *        switch record (no NVM3).
 * @details
 *   Requires \c BTL_SMP_SUPPORT and the address symbols in \c btl_smp_cfg.h:
 *   switch page bases, app 2 base, optional default app id.
 *   App 1 base defaults to \c BTL_APPLICATION_BASE.
 * @{
 ******************************************************************************/

/// Magic value identifying a valid switch record ("SMPP" in ASCII).
#define BTL_SMP_RECORD_MAGIC       0x534D5050UL

/// Record format version.
#define BTL_SMP_RECORD_VERSION      1U

/// Application ID: app 1 (first application region).
#define BTL_SMP_APP_ID_1            1U
/// Application ID: app 2 (second application region).
#define BTL_SMP_APP_ID_2            2U

/// Minimum valid app_id (inclusive).
#define BTL_SMP_APP_ID_MIN          BTL_SMP_APP_ID_1
/// Maximum valid app_id (inclusive). Extend if more apps are added.
#define BTL_SMP_APP_ID_MAX          BTL_SMP_APP_ID_2

/***************************************************************************//**
 * @brief Switch record stored at the beginning of each switch page.
 *
 * CRC32 is computed over magic, seq, app_id, and version (first 8 bytes).
 ******************************************************************************/
typedef struct {
  uint32_t magic;   ///< Must be \c BTL_SMP_RECORD_MAGIC.
  uint16_t seq;     ///< Monotonic sequence counter (higher = newer). \c uint16_t wrap handled via epoch reset in the Flash API.
  uint8_t  app_id;  ///< Target application ID (e.g. app 1 or app 2).
  uint8_t  version; ///< Record format version (\c BTL_SMP_RECORD_VERSION).
  uint32_t crc32;   ///< CRC32 over (magic, seq, app_id, version).
} btl_smp_switch_record_t;

 
/// Byte length of (magic, seq, app_id, version) used as input to \c btl_crc32Stream.
#define BTL_SMP_RECORD_HEADER_CRC_LEN  (sizeof(uint32_t) + sizeof(uint16_t) + sizeof(uint8_t) + sizeof(uint8_t))
#ifdef BOOTLOADER_ENABLE
/***************************************************************************//**
 * Read switch records from both pages, validate, select the newest valid
 * record, and return the application base address for the selected app_id.
 * The bootloader uses this value as @c startOfAppSpace (read-only; no write).
 *
 * @param[out] out_app_base  Selected application base address.
 *
 * @return Returns \c BTL_TRUE if @p out_app_base is non-NULL and was filled with
 *         the selected app base, or with the default app base when both pages are
 *         invalid. Returns \c BTL_FALSE if @p out_app_base is NULL.
 ******************************************************************************/
btl_ret_t btl_smp_switch_get_selected_app_base(uint32_t *out_app_base);

/***************************************************************************//**
 * Get the alternate application base when the current base is one of the two
 * SMP slots. Used when the bootloader must try the other image after
 * verification fails for the SMP-selected application.
 *
 * @param[in]  current_app_base   Application base that was selected but failed.
 * @param[out] out_alternate_base Filled with the other SMP app base
 *                                (\c BTL_SMP_APP_2_BASE if \p current_app_base
 *                                is \c BTL_SMP_APP_1_BASE, and vice versa).
 *
 * @return Returns \c BTL_TRUE if @p out_alternate_base is non-NULL and
 *         @p current_app_base matches one of the two SMP app bases.
 *         Returns \c BTL_FALSE if @p out_alternate_base is NULL or @p current_app_base
 *         is not an SMP app slot.
 ******************************************************************************/
btl_ret_t btl_smp_switch_get_alternate_app_base(uint32_t current_app_base, uint32_t *out_alternate_base);
#endif
/** @} (end smp_switch) */

#ifdef __cplusplus
}
#endif

#endif /* BTL_SMP_SWITCH_RECORD_H */
