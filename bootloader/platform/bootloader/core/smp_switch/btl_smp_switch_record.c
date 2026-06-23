/***************************************************************************//**
 * @file
 * @brief SMP two-page switch record implementation (read/validate/select).
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
 *    claim that you wrote the original software.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/

#if defined(BTL_SMP_SUPPORT)

#include "btl_smp_cfg.h"
#include "btl_smp_switch_record.h"
#include "security/btl_crc32.h"
#include "em_device.h"
#include <stddef.h>

#ifndef BTL_SMP_DEFAULT_APP_ID
#define BTL_SMP_DEFAULT_APP_ID  BTL_SMP_APP_ID_1
#endif

static bool record_valid(const btl_smp_switch_record_t *rec)
{
  if (rec == NULL) {
    return false;
  }
  if (rec->magic != BTL_SMP_RECORD_MAGIC
      || rec->app_id < BTL_SMP_APP_ID_MIN
      || rec->app_id > BTL_SMP_APP_ID_MAX
      || rec->version != BTL_SMP_RECORD_VERSION) {
    return false;
  }
  return btl_crc32Stream((const uint8_t *)rec, BTL_SMP_RECORD_HEADER_CRC_LEN, BTL_CRC32_START) == rec->crc32;
}

static uint32_t get_app_base_for_id(uint8_t app_id)
{
  switch (app_id) {
    case BTL_SMP_APP_ID_1:
      return BTL_SMP_APP_1_BASE;
    case BTL_SMP_APP_ID_2:
      return BTL_SMP_APP_2_BASE;
    default:
      /* Incorrect or invalid app id (not 1 or 2): use application 1 base. */
      return BTL_SMP_APP_1_BASE;
  }
}

/***************************************************************************//**
 * Application base to use when both switch records are invalid (first boot, etc.).
 * Uses \c BTL_SMP_DEFAULT_APP_ID from \c btl_smp_cfg.h (app 1 or app 2).
 ******************************************************************************/
static uint32_t get_default_app_base(void)
{
  return get_app_base_for_id((uint8_t)BTL_SMP_DEFAULT_APP_ID);
}

btl_ret_t btl_smp_switch_get_selected_app_base(uint32_t *out_app_base)
{
  if (out_app_base == NULL) {
    return BTL_FALSE;
  }

  if ((BTL_SMP_PAGE_1_BASE < FLASH_BASE)
      || (BTL_SMP_PAGE_1_BASE >= (FLASH_BASE + FLASH_SIZE))
      || (BTL_SMP_PAGE_2_BASE < FLASH_BASE)
      || (BTL_SMP_PAGE_2_BASE >= (FLASH_BASE + FLASH_SIZE))) {
    return BTL_FALSE;
  }

  const btl_smp_switch_record_t *rec_1 =
    (const btl_smp_switch_record_t *)BTL_SMP_PAGE_1_BASE;
  const btl_smp_switch_record_t *rec_2 =
    (const btl_smp_switch_record_t *)BTL_SMP_PAGE_2_BASE;

  const bool v1 = record_valid(rec_1);
  const bool v2 = record_valid(rec_2);

  if (!v1 && !v2) {
    *out_app_base = get_default_app_base();
    return BTL_TRUE;
  }
  if (v1 && !v2) {
    *out_app_base = get_app_base_for_id(rec_1->app_id);
    return BTL_TRUE;
  }
  if (!v1 && v2) {
    *out_app_base = get_app_base_for_id(rec_2->app_id);
    return BTL_TRUE;
  }
  /* Both valid: higher seq wins; tie -> page 2 (same as rec_2->seq >= rec_1->seq). */
  *out_app_base = (rec_2->seq >= rec_1->seq)
                  ? get_app_base_for_id(rec_2->app_id)
                  : get_app_base_for_id(rec_1->app_id);
  return BTL_TRUE;
}

btl_ret_t btl_smp_switch_get_alternate_app_base(uint32_t current_app_base, uint32_t *out_alternate_base)
{
  if (out_alternate_base == NULL) {
    return BTL_FALSE;
  }
  if (current_app_base == BTL_SMP_APP_1_BASE) {
    *out_alternate_base = BTL_SMP_APP_2_BASE;
    return BTL_TRUE;
  }
  if (current_app_base == BTL_SMP_APP_2_BASE) {
    *out_alternate_base = BTL_SMP_APP_1_BASE;
    return BTL_TRUE;
  }
  return BTL_FALSE;
}

#endif /* BTL_SMP_SUPPORT */
