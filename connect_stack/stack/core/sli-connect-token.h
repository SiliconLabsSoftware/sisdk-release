/***************************************************************************//**
 * @brief Stack token handling interface
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
#ifndef __SLI_CONNECT_TOKEN_H__
#define __SLI_CONNECT_TOKEN_H__

#include "sl_token_manager_defines.h"
#include "stack/config/sl_connect_token_defines.h"
#ifndef EMBER_TEST
#include "sl_token_manager_api.h"
#include "sl_token_manager_manufacturing.h"
#else
#include "sli-connect-token-manager-stubs.h"
#endif

/** @brief Initialize stack tokens.
 *
 * This API provides a compatibility layer for stack token initialization.
 * The implementation is selected by the build configuration
 * (legacy token manager behavior or common token manager behavior).
 *
 * @return A status code indicating whether token initialization completed
 * successfully.
 */
sl_status_t sli_connect_init_stack_tokens();

#endif // __SLI_CONNECT_TOKEN_H__
