/**
 * @file zw_s2_nls_support.h
 * @brief NLS support configuration API for Z-Wave applications.
 * @copyright 2025 Silicon Laboratories Inc. www.silabs.com
 */
#ifndef ZW_S2_NLS_SUPPORT_H
#define ZW_S2_NLS_SUPPORT_H

#include <stdint.h>

/**
 * @brief Configure whether NLS support is advertised during S2 inclusion.
 *
 * When enabled, the device reports NLS as available in the KEX Report frame
 * during S2 bootstrapping. Must be called before inclusion starts
 * (e.g. in ApplicationInit).
 *
 * @param supported Non-zero to advertise NLS as available, 0 otherwise.
 */
void set_nls_support(uint8_t supported);

/**
 * @brief Initialize NLS support by enabling it.
 *
 * This is a convenience wrapper called automatically via the SLC event system
 * (internal_app_init) when the zw_s2_nls_support component is installed.
 */
void zw_s2_nls_support_init(void);

#endif /* ZW_S2_NLS_SUPPORT_H */
