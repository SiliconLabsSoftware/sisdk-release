/***************************************************************************//**
 * @brief Legacy token handling implementation
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

/**
 * @note  This file should be deleted once the legacy token manager is fully
 *        deprecated.
 */

#include "include/ember.h"
#include "sli-connect-token.h"
#if defined(SL_CATALOG_IOSTREAM_UART_COMMON_PRESENT)
#include "sl_iostream.h"
#endif

//  The legacy token manager handles token initialization,
//  no manual initialization is required.
//  Once the legacy token manager is fully deprecated,
//  this file should be deleted.
sl_status_t sli_connect_init_stack_tokens()
{
  return sl_token_init();
}

//  The legacy token manager needs these legacy hal APIs
void halInternalGetMfgTokenData(void *data, uint16_t token, uint8_t index, uint32_t len)
{
  (void) sl_token_get_manufacturing_data(token, index, data, len);
}

void halInternalSetMfgTokenData(uint16_t token, void *data, uint32_t len)
{
  (void) sl_token_set_manufacturing_data(token, data, len);
}

void halInternalAssertFailed(const char * filename, int linenumber)
{
#if defined(SL_CATALOG_IOSTREAM_UART_COMMON_PRESENT)
  sl_iostream_printf(SL_IOSTREAM_STDOUT, "\r\n[ASSERT:%s:%d]\r\n", filename, linenumber);
#else
  (void)filename;
  (void)linenumber;
#endif // SL_CATALOG_IOSTREAM_UART_COMMON_PRESENT
  NVIC_SystemReset();
}
