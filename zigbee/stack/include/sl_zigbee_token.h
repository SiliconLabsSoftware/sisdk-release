/***************************************************************************//**
 * @brief ZigBee token management code.
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

#ifndef SL_ZIGBEE_TOKEN_H
#define SL_ZIGBEE_TOKEN_H

#include "stack/include/sl_zigbee_types.h"

/**
 * @brief Get the total count of the tokens configured.
 * @return The token count.
 *
 * Use this to get the number of tokens configured in a node.
 */
uint32_t sl_zigbee_get_token_count(void);

/**
 * @brief Get information of a token by providing the index.
 * @param index An index to configured token array that ranges from 0 to sl_zigbee_get_token_count() - 1;
 * @param tokenInfo A pointer to hold the information in a structure provided by the caller.
 * @return Status of the call, SL_STATUS_OK upon success or SL_STATUS_INVALID_INDEX for bad index.
 *
 * @internal SL_ZIGBEE_IPC_ARGS
 * {# tokenInfo #}
 */
sl_status_t sl_zigbee_get_token_info(uint8_t index,
                                     sl_zigbee_token_info_t *tokenInfo);

/**
 * @brief Get token data by providing the token key and index for the indexed token.
 * @param token A valid token key, which may be obtained using sl_zigbee_get_token_info.
 * @param index An index in case the token is an indexed token, if token is indexed can be obtained
 *              from sl_zigbee_get_token_info.
 * @param tokenData A pointer pointing to memory storage information, must be allocated and provided by the caller.
 * @return Status of the call, SL_STATUS_OK upon success or SL_STATUS_FAIL for errors.
 *
 * @internal SL_ZIGBEE_IPC_ARGS
 * {# tokenData #}
 */
sl_status_t sl_zigbee_get_token_data(uint32_t token,
                                     uint32_t index,
                                     sl_zigbee_token_data_t *tokenData);
/**
 * @brief Set token data by providing the token key, index for an indexed token and token data.
 * @param token A valid token key, which may be obtained using sl_zigbee_get_token_info.
 * @param index An index in case the token is an indexed token, if token is indexed can be obtained
 *              from sl_zigbee_get_token_info.
 * @param tokenData A pointer pointing to memory storage holding the token data provided by the caller.
 * @return Status of the call, SL_STATUS_OK upon success or SL_STATUS_FAIL for errors.
 *
 */
sl_status_t sl_zigbee_set_token_data(uint32_t token,
                                     uint32_t index,
                                     sl_zigbee_token_data_t *tokenData);

/**
 * @brief Get the default value of the given token.
 * @param token The NVM3 key of the token, the base if an index token.
 * @param default_token_value Pointer to memory to copy value into.
 * @return status.
 *
 * Use this to get the number of tokens configured in a node.
 * @internal SL_ZIGBEE_IPC_ARGS
 * {# default_token_value | length: MAX_IPC_VEC_ARG_CAPACITY | max: MAX_IPC_VEC_ARG_CAPACITY #}
 */
sl_status_t sl_zigbee_get_token_default(uint32_t token,
                                        uint8_t *default_token_value);
/**
 * @brief Initialize a basic, non-counter, non-index token
 * (Common Token Manager Component only).
 * @param token The KLV of the token.
 * @param default_token_value Pointer to the token's default value.
 * @param token_size Size of the token being initialized.
 * @return status.
 *
 * Use this to get the number of tokens configured in a node.
 * @internal SL_ZIGBEE_IPC_ARGS
 * {# default_token_value | length: token_size | max: MAX_IPC_VEC_ARG_CAPACITY | storage_type: uint8_t #}
*/
sl_status_t sl_zigbee_initialize_basic_token(uint32_t token,
                                             void *default_token_value,
                                             uint32_t token_size);

/**
 * @brief Initialize a counter token.
 * (Common Token Manager Component only).
 * @param token The KLV of the token.
 * @param default_token_value Pointer to the token's default value.
 * @param token_size Size of the token being initialized.
 * @return status.
 *
 * Use this to get the number of tokens configured in a node.
 * @internal SL_ZIGBEE_IPC_ARGS
 * {# default_token_value | length: token_size | max: MAX_IPC_VEC_ARG_CAPACITY | storage_type: uint8_t #}
*/
sl_status_t sl_zigbee_initialize_counter_token(uint32_t token,
                                               void *default_token_value,
                                               uint32_t token_size);

/**
 * @brief Initialize an index token.
 * (Common Token Manager Component only).
 * @param token The KLV of the token.
 * @param default_token_value Pointer to the token's default value.
 * @param token_size Size of the token being initialized.
 * @param token_index_size Size of the array of tokens.
 * @return status.
 *
 * Use this to get the number of tokens configured in a node.
 * @internal SL_ZIGBEE_IPC_ARGS
 * {# default_token_value | length: token_size | max: MAX_IPC_VEC_ARG_CAPACITY | storage_type: uint8_t #}
*/
sl_status_t sl_zigbee_initialize_index_token(uint32_t token_base,
                                             void *default_token_value,
                                             uint32_t token_size,
                                             uint8_t token_index_size);

/**
 * @brief Internal use only: a utility function to fetch the token value from storage medium 
 * (NVM3 or filesystem) with a default value fallback if the token has never been written to storage. 
 * This API returns the default value if the token has been initialized using 
 * ::sl_zigbee_initialize_basic_token, ::sl_zigbee_initialize_counter_token, or 
 * ::sl_zigbee_initialize_index_token but subsequently said token has never been written 
 * to flash or filesystem (the initialization routines do not propagate the token to storage medium). 
 * In general, a user application may get and set token values using the Common Token Manager routines. 
 * This API here is provided as a utility for the EmberZNet stack to handle cases where the token 
 * is not found in storage and a default value fallback is desired. 
 * Users are encouraged to avoid calling this API, as it is subject to removal/rework in the future.
 * @param token The KLV of the token.
 * @param data Pointer to the output buffer for the token's data.
 * @param length Size of the token's data.
 * @return status.
 *
 * @internal SL_ZIGBEE_IPC_ARGS
 * {# data | length: length | max: MAX_IPC_TOKEN_MANAGER_DATA_LENGTH_ARG_CAPACITY | storage_type: uint8_t #}
 */
sl_status_t slx_zigbee_token_manager_get_data(uint32_t token,
                                              void *data,
                                              uint32_t length);

#ifndef ZNET_HEADER_SCRIPT
/**
 * @brief Internal use only: write token data in storage medium. 
 * This is just a pair to complete the ::sli_zigbee_token_manager_get_data API. 
 * Users are encouraged to avoid calling this API, as it is subject to removal/rework in the future.
 * Thread-safe via sl_token_manager_set_data; no IPC wrapper.
 * @param token The KLV of the token.
 * @param data Pointer to the input buffer for the token's data.
 * @param length Size of the token's data.
 * @return status.
 *
 * Use this to set the token's data.
 */
sl_status_t slx_zigbee_token_manager_set_data(uint32_t token,
                                              void *data,
                                              uint32_t length);
#endif // ZNET_HEADER_SCRIPT
#endif // SL_ZIGBEE_TOKEN_H
