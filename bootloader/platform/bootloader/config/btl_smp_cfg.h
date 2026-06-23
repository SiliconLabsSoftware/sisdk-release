/***************************************************************************//**
 * @file
 * @brief Configuration header of Bootloader SMP two-page switch (SDK reference copy)
 * @note Project copies are generated from device_series_2/ or device_sdid_205/ variants
 *       per bootloader_core config_file rules. This file matches device_series_2 content.
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
#ifndef BTL_SMP_CONFIG_H
#define BTL_SMP_CONFIG_H

// <<< Use Configuration Wizard in Context Menu >>>
// <h> SMP Two-Page Switch Configuration
//
// Switch metadata uses TWO separate flash erase pages:
// - BTL_SMP_PAGE_1_BASE and BTL_SMP_PAGE_2_BASE must be two different addresses (never equal).
// - Each must be aligned to the device FLASH_PAGE_SIZE (see em_device.h).
// - The two regions must not overlap. Typical layout: PAGE_2_BASE = PAGE_1_BASE + FLASH_PAGE_SIZE.
// - On many EFR32 Series 2 parts internal flash page size is 8192 bytes (8 KiB); in that case the
//   bases are 8 KiB apart. Always match your part's actual FLASH_PAGE_SIZE — do not assume 8 KiB
//   if the datasheet / em_device.h says otherwise.

// <o BTL_SMP_PAGE_1_BASE> Switch record page 1 base address (flash) <f.h>
// <i> First switch-record page: start of a dedicated flash erase page (see FLASH_PAGE_SIZE).
// <i> Must differ from BTL_SMP_PAGE_2_BASE; must not overlap apps, bootloader, NVM3, OTA, tokens.
// <i> Default: 0
#ifndef BTL_SMP_PAGE_1_BASE
#define BTL_SMP_PAGE_1_BASE  0x0UL
#endif

// <o BTL_SMP_PAGE_2_BASE> Switch record page 2 base address (flash) <f.h>
// <i> Second switch-record page: start of a different erase page than page 1 (no overlap).
// <i> Recommended: PAGE_1_BASE + FLASH_PAGE_SIZE (often +8192 / 8 KiB on Series 2 — verify device).
// <i> Must not overlap page 1, apps, bootloader, NVM3, OTA, tokens.
// <i> Default: 0
#ifndef BTL_SMP_PAGE_2_BASE
#define BTL_SMP_PAGE_2_BASE  0x0UL
#endif

// App 1 image base is the primary application slot (same as BTL_APPLICATION_BASE from
// btl_interface.h / linker). Not configurable here so it stays aligned with the bootloader.
#include "api/btl_interface.h"
#ifndef BTL_SMP_APP_1_BASE
#define BTL_SMP_APP_1_BASE          BTL_APPLICATION_BASE
#endif

// <o BTL_SMP_APP_2_BASE> Application 2 base address (flash) <f.h>
// <i> Start address of application 2 image (vector table) in flash.
// <i> Default: 0
#ifndef BTL_SMP_APP_2_BASE
#define BTL_SMP_APP_2_BASE          0x0UL
#endif

// <o BTL_SMP_DEFAULT_APP_ID> Default app when both switch records invalid
// <1=> App 1
// <2=> App 2
// <i> Application to boot when neither switch record is valid (e.g. first boot).
// <i> Default: 1
#ifndef BTL_SMP_DEFAULT_APP_ID
#define BTL_SMP_DEFAULT_APP_ID      1
#endif

// </h>

// <<< end of configuration section >>>

#endif // BTL_SMP_CONFIG_H
