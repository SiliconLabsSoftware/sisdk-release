/***************************************************************************//**
 * @file
 * @brief Flash API for SMP two-page switch records (application use).
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
#ifndef BTL_SMP_SWITCH_FLASH_API_H
#define BTL_SMP_SWITCH_FLASH_API_H

#include "btl_smp_switch_record.h"
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************//**
 * @addtogroup smp_switch SMP Two-Page Switch Record
 * @brief Application-side flash helpers for the SMP switch pages.
 * @{
 ******************************************************************************/

/***************************************************************************//**
 * Erase one switch page.
 *
 * The application must not erase the page that holds the current valid record
 * until after the new record is written to the other page.
 *
 * @param[in] use_page_1  true = Page 1, false = Page 2.
 *
 * @return Returns true on MSC success, false on MSC error.
 ******************************************************************************/
bool btl_smp_switch_erase_page(bool use_page_1);

/***************************************************************************//**
 * Write a full switch record to one page.
 *
 * @note Non-validating fields are written first, then CRC, then magic last.
 *       The implementation sets magic, version (\c BTL_SMP_RECORD_VERSION),
 *       and crc32; the caller supplies \p seq and \p app_id.
 *
 * @param[in] use_page_1  true = write to Page 1, false = Page 2.
 * @param[in] seq         Sequence value for the record.
 * @param[in] app_id      Target app (\c BTL_SMP_APP_ID_1 or \c BTL_SMP_APP_ID_2).
 *
 * @return Returns true on MSC success, false on MSC error.
 ******************************************************************************/
bool btl_smp_switch_write_record(bool use_page_1,
                                 uint16_t seq,
                                 uint8_t app_id);

/***************************************************************************//**
 * Get SMP switch metadata page base addresses from the bootloader storage vtable.
 *
 * Requires \ref BOOTLOADER_CAPABILITY_SMP_SWITCH (via \c bootloader_getInfo()) and a
 * non-NULL \c getSmpSwitchPageBases pointer in \c BootloaderStorageFunctions_t.
 * The bootloader supplies bases from its layout; the app does not use \c btl_smp_cfg.h.
 *
 * @param[out] page1Base  Page 1 base if non-NULL.
 * @param[out] page2Base  Page 2 base if non-NULL.
 *
 * @return False if SMP is not supported, or the storage vtable does not expose page bases.
 ******************************************************************************/
bool get_smp_page_bases_from_storage(uint32_t *page1Base, uint32_t *page2Base);

/***************************************************************************//**
 * Request that the next boot runs the given application.
 *
 * Reads both pages, selects the other page, erases it, and writes a new
 * record (sequence incremented, @p app_id set). The application should
 * trigger a software reset after success.
 *
 * @param[in] next_app_id  Desired app for next boot (\c BTL_SMP_APP_ID_1 or
 *                         \c BTL_SMP_APP_ID_2).
 *
 * @return Returns true if the switch record was updated successfully.
 *         Returns false if \ref BOOTLOADER_CAPABILITY_SMP_SWITCH is not set, or if
 *         read/validate or erase/write failed.
 *
 * @note When the next sequence wraps in \c uint16_t (65535 + 1), \c next_seq is 0;
 *       both switch pages are erased and \c seq restarts at 1 (epoch reset). The target
 *       metadata page for the new record stays the same as the non-epoch algorithm would
 *       have chosen. Which application boots is always \p next_app_id, not the page index.
 ******************************************************************************/
bool btl_smp_switch_request_next_boot_app(uint8_t next_app_id);

/** @} (end smp_switch) */

#ifdef __cplusplus
}
#endif

#endif /* BTL_SMP_SWITCH_FLASH_API_H */
