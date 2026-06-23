/***************************************************************************//**
 * @file
 * @brief SMP switch record Flash API implementation.
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

#include "btl_smp_switch_record.h"
#include "btl_smp_switch_flash_api.h"
#include "api/btl_interface.h"
#include "core/flash/btl_internal_flash.h"
#include "em_device.h"
#include <stddef.h>
#include <stdint.h>

#if defined(__GNUC__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Warray-bounds"
#endif

/* Same GPCRC CRC32 as security/btl_crc32.c (btl_crc32Stream) so records match bootloader
 * validation in btl_smp_switch_record.c. File-local to avoid duplicate btl_crc32Stream when
 * bootloader_crc is linked. */
#define SMP_RECORD_CRC32_INIT  (0xFFFFFFFFUL)

static uint32_t smp_record_crc32_stream(const uint8_t *buffer, size_t length, uint32_t prevResult)
{
#if defined(_CMU_CLKEN0_MASK)
  CMU->CLKEN0_SET = CMU_CLKEN0_GPCRC;
#endif
#if defined(_SILICON_LABS_32B_SERIES_2)
  GPCRC->EN = GPCRC_EN_EN;
  GPCRC->CTRL = GPCRC_CTRL_POLYSEL_CRC32;
  GPCRC->INIT = prevResult;
  GPCRC->CMD = GPCRC_CMD_INIT;

  while (length--) {
    GPCRC->INPUTDATABYTE = *buffer++;
  }

  return GPCRC->DATA;
#else
  CMU->HFBUSCLKEN0 |= CMU_HFBUSCLKEN0_GPCRC;

  GPCRC->CTRL = GPCRC_CTRL_POLYSEL_CRC32 | GPCRC_CTRL_EN_ENABLE;
  GPCRC->INIT = prevResult;
  GPCRC->CMD = GPCRC_CMD_INIT;

  while (length--) {
    GPCRC->INPUTDATABYTE = *buffer++;
  }

  return GPCRC->DATA;
#endif
}

static bool smp_switch_page_addresses_ok(uint32_t page1, uint32_t page2)
{
#if (FLASH_BASE > 0x0UL)
  if ((page1 < (uint32_t)FLASH_BASE) || (page2 < (uint32_t)FLASH_BASE)) {
    return false;
  }
#endif
  if ((page1 >= (uint32_t)(FLASH_BASE + FLASH_SIZE))
      || (page2 >= (uint32_t)(FLASH_BASE + FLASH_SIZE))) {
    return false;
  }
  return true;
}

/**
 * Get SMP switch page bases from the bootloader storage vtable.
 * No btl_smp_cfg.h — addresses come only from
 * mainBootloaderTable->storage->getSmpSwitchPageBases when non-NULL.
 */
bool get_smp_page_bases_from_storage(uint32_t *page1Base, uint32_t *page2Base)
{
  BootloaderInformation_t info = { .type = SL_BOOTLOADER, .version = 0U, .capabilities = 0U };
  bootloader_getInfo(&info);
  if ((info.capabilities & BOOTLOADER_CAPABILITY_SMP_SWITCH) == 0U) {
    return false;
  }

  if (bootloader_pointerValid(mainBootloaderTable)
      && (mainBootloaderTable->storage != NULL)
      && (mainBootloaderTable->storage->getSmpSwitchPageBases != NULL)) {
    mainBootloaderTable->storage->getSmpSwitchPageBases(page1Base, page2Base);
    /* When both outputs are requested, reject NULL map and garbage (invalid to dereference as rec). */
    if ((page1Base != NULL) && (page2Base != NULL)
        && !smp_switch_page_addresses_ok(*page1Base, *page2Base)) {
      return false;
    }
    return true;
  }

  return false;
}

static bool get_page_base_for_write(bool use_page_1, uint32_t *out_base)
{
  uint32_t p1;
  uint32_t p2;
  if (!get_smp_page_bases_from_storage(&p1, &p2)) {
    return false;
  }
  *out_base = use_page_1 ? p1 : p2;
  return true;
}

static bool record_crc_ok(const btl_smp_switch_record_t *rec)
{
  if (rec == NULL) {
    return false;
  }
  if (rec->magic != BTL_SMP_RECORD_MAGIC) {
    return false;
  }
  if (rec->app_id < BTL_SMP_APP_ID_MIN || rec->app_id > BTL_SMP_APP_ID_MAX) {
    return false;
  }
  if (rec->version != BTL_SMP_RECORD_VERSION) {
    return false;
  }
  return smp_record_crc32_stream((const uint8_t *)rec, BTL_SMP_RECORD_HEADER_CRC_LEN, SMP_RECORD_CRC32_INIT) == rec->crc32;
}

bool btl_smp_switch_erase_page(bool use_page_1)
{
  uint32_t base;
  if (!get_page_base_for_write(use_page_1, &base)) {
    return false;
  }
  return flash_erasePage(base);
}

/* Erase both switch pages for sequence epoch reset (uint16 seq wrap). */
static bool smp_switch_epoch_reset_both_pages(void)
{
  return btl_smp_switch_erase_page(true) && btl_smp_switch_erase_page(false);
}

/* Erase page, then write full record (payload, CRC, magic last). */
bool btl_smp_switch_write_record(bool use_page_1,
                                 uint16_t seq,
                                 uint8_t app_id)
{
  uint32_t base;
  if (!get_page_base_for_write(use_page_1, &base)) {
    return false;
  }
  if (!flash_erasePage(base)) {
    return false;
  }

  btl_smp_switch_record_t rec;
  rec.magic   = BTL_SMP_RECORD_MAGIC;
  rec.seq     = seq;
  rec.app_id  = app_id;
  rec.version = (uint8_t)BTL_SMP_RECORD_VERSION;
  rec.crc32   = smp_record_crc32_stream((const uint8_t *)&rec, BTL_SMP_RECORD_HEADER_CRC_LEN, SMP_RECORD_CRC32_INIT);

  /* Flash write order: payload words first, then CRC, then magic last. */
  const uint32_t word4 = (uint32_t)seq | ((uint32_t)app_id << 16) | ((uint32_t)rec.version << 24);

  if (!flash_writeBuffer(base + 4U, &word4, sizeof(word4))) {
    return false;
  }
  if (!flash_writeBuffer(base + 8U, &rec.crc32, sizeof(rec.crc32))) {
    return false;
  }
  return flash_writeBuffer(base, &rec.magic, sizeof(rec.magic));
}

static bool btl_smp_switch_capability_ok(void)
{
  BootloaderInformation_t info = { .type = SL_BOOTLOADER, .version = 0U, .capabilities = 0U };
  bootloader_getInfo(&info);
  return (info.capabilities & BOOTLOADER_CAPABILITY_SMP_SWITCH);
}

bool btl_smp_switch_request_next_boot_app(uint8_t next_app_id)
{
  if (!btl_smp_switch_capability_ok()) {
    return false;
  }
  if (next_app_id < BTL_SMP_APP_ID_MIN || next_app_id > BTL_SMP_APP_ID_MAX) {
    return false;
  }

  uint32_t page1;
  uint32_t page2;
  if (!get_smp_page_bases_from_storage(&page1, &page2)) {
    return false;
  }

  const btl_smp_switch_record_t *rec_1 = (const btl_smp_switch_record_t *)(uintptr_t)page1;
  const btl_smp_switch_record_t *rec_2 = (const btl_smp_switch_record_t *)(uintptr_t)page2;

  const bool v1 = record_crc_ok(rec_1);
  const bool v2 = record_crc_ok(rec_2);

  uint16_t next_seq;
  bool write_p1;

  if (!v1 && !v2) {
    next_seq  = 1;
    write_p1  = true;
  } else if (v1 && !v2) {
    next_seq  = (uint16_t)(rec_1->seq + 1U);
    write_p1  = false;
  } else if (!v1 && v2) {
    next_seq  = (uint16_t)(rec_2->seq + 1U);
    write_p1  = true;
  } else {
    /* Both valid: write to the page that is not newer so next boot sees higher seq on one page. */
    if (rec_2->seq >= rec_1->seq) {
      next_seq = (uint16_t)(rec_2->seq + 1U);
      write_p1 = true;
    } else {
      next_seq = (uint16_t)(rec_1->seq + 1U);
      write_p1 = false;
    }
  }

  /* 65535 + 1 wraps to 0 in uint16_t: planned epoch — wipe both pages, seq restarts at 1. */
  if (next_seq == 0U) {
    /* Keep write_p1 (which metadata page receives the write). */
    if (!smp_switch_epoch_reset_both_pages()) {
      return false;
    }
    next_seq = 1U;
  }

  return btl_smp_switch_write_record(write_p1, next_seq, next_app_id);
}

#if defined(__GNUC__)
#pragma GCC diagnostic pop
#endif
