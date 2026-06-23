/***************************************************************************//**
 * @file authenticator_stubs.c
 * @brief Authenticator stubs for when authenticator is not linked
 *******************************************************************************
 * # License
 * <b>Copyright 2025 Silicon Laboratories Inc. www.silabs.com</b>
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

#include <stddef.h>
#include <stdint.h>

struct auth_ctx {
  int dummy;  // empty stub
};

struct auth_supp_ctx {
  int dummy;  // empty stub
};

struct auth_supp_ctx *auth_fetch_supp(struct auth_ctx *auth, const uint8_t eui64[8])
{
  (void)auth;
  (void)eui64;
  return NULL;
}

void auth_recv_eapol(struct auth_ctx *auth, uint8_t kmp_id, const uint8_t eui64[8],
                     const uint8_t *buf, size_t buf_len)
{
  (void)auth;
  (void)kmp_id;
  (void)eui64;
  (void)buf;
  (void)buf_len;
}

