/***************************************************************************//**
 * @file
 * @brief ESL Host Library advertisement deduplication cache.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 ******************************************************************************/

#ifndef ESL_LIB_ADV_DEDUP_H
#define ESL_LIB_ADV_DEDUP_H

#include <stdint.h>
#include <stdbool.h>
#include "sl_status.h"
#include "esl_lib.h"
#include "esl_lib_adv_dedup_config.h"

#ifdef __cplusplus
extern "C" {
#endif

/**************************************************************************//**
 * Release advertisement deduplication resources.
 *****************************************************************************/
void esl_lib_adv_dedup_deinit(void);

/**************************************************************************//**
 * Configure advertisement deduplication.
 *
 * @param[in] config Configuration. NULL applies all compile-time defaults,
 *                   including the state from @ref ESL_LIB_ADV_DEDUP_ENABLE.
 *                   esl_lib_init() calls this with NULL when
 *                   @ref ESL_LIB_ADV_DEDUP_ENABLE is set.
 *
 * @return SL_STATUS_OK on success.
 *****************************************************************************/
sl_status_t esl_lib_adv_dedup_configure(const esl_lib_adv_dedup_config_t *config);

/**************************************************************************//**
 * Update cache for a deferred ESL service report.
 *
 * @param[in] address  Bluetooth address.
 * @param[in] rssi     RSSI of the report.
 *****************************************************************************/
void esl_lib_adv_dedup_touch(esl_lib_address_t address, int8_t rssi);

/**************************************************************************//**
 * Decide whether a tag_found event shall be sent for an ESL service report.
 *
 * Updates the cache on every call. Only ESL service advertisements shall be
 * passed in (caller responsibility).
 *
 * @param[in] address  Bluetooth address.
 * @param[in] rssi     RSSI of the report.
 *
 * @return true if tag_found shall be emitted, false to suppress.
 *****************************************************************************/
bool esl_lib_adv_dedup_should_notify(esl_lib_address_t address, int8_t rssi);

/**************************************************************************//**
 * Remove one advertiser from the deduplication cache (lib-internal).
 *
 * Called when a central connection is established or aborted before
 * establishment so the next ESL service report is treated as a new discovery.
 *****************************************************************************/
void esl_lib_adv_dedup_forget_address(esl_lib_address_t address);

#ifdef __cplusplus
};
#endif

#endif // ESL_LIB_ADV_DEDUP_H
