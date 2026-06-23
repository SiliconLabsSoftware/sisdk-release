/***************************************************************************//**
 * @brief Definitions for stack tokens for Common Token Manager.
 * See @ref token_stack for documentation.
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

#include <stdint.h>
#include "sl_token_manager_defines.h"
#include "sl_token_manager_config.h"
#include "ember-types.h"

/**
 * @brief The current version number of the stack tokens.
 * MSB is the version. LSB is a complement.
 *
 * See hal/micro/token.h for a more complete explanation.
 */
#define CURRENT_STACK_TOKEN_VERSION 0x03FC //MSB is version, LSB is complement

/********************************************************************************************************************
 * @name Token types
 * @brief The types used for each stack token.
 *@{
 */
/**
 * @brief Type for COMMON_TOKEN_STACK_NVDATA_VERSION. Keeps the version number of
 * stack tokens.
 */
typedef uint16_t tokTypeStackNvdataVersion;

/**
 * @brief Type for COMMON_TOKEN_STACK_NONCE_COUNTER. Used to make sure that Nonce used
 * for security is not repeated even after unexpected reboot.
 */
typedef uint32_t tokTypeStackNonceCounter;

/**
 * @struct tokTypeStackKey
 * @brief Type for COMMON_TOKEN_STACK_SECURITY_KEY. Keeps the security key for MAC
 * layer security.
 */
typedef struct {
  uint8_t networkKey[EMBER_ENCRYPTION_KEY_SIZE]; /**< The key itself */
} tokTypeStackKey;

/**
 * @brief Type for COMMON_TOKEN_STACK_SECURITY_KEY_ID.
 */
typedef uint32_t tokTypeStackKeyID;

/**
 * @struct tokTypeStackNodeData
 * @brief Type for COMMON_TOKEN_STACK_NODE_DATA. Generic information of the node is
 * stored in this token
 */
typedef struct {
  uint16_t panId; /**< The PanId of the device */
  int16_t radioTxPower; /**< The TX power configured for the device in deci-dBm */
  uint16_t radioFreqChannel; /**< The radio channel configured for the device */
  uint8_t nodeType; /**< The @ref EmberNodeType configured for the device */
  uint16_t nodeId; /**< The NodeId (short address) of the device */
  uint16_t parentId; /**< The NodeId of the device's parent, if any */
} tokTypeStackNodeData;

/**
 * @struct tokTypeStackChildTableEntry
 * @brief Type of an element of COMMON_TOKEN_STACK_CHILD_TABLE (indexed token). Keeps
 * children information of a device, which has parent support enabled.
 */
typedef struct {
  EmberEUI64 longId; /**< The Long Id of the child */
  EmberNodeId shortId; /**< The NodeId of the child */
  uint8_t flags; /**< Flags for the child required by the stack */
} tokTypeStackChildTableEntry;

/**
 * @brief Type for COMMON_TOKEN_STACK_LAST_ASSIGNED_ID. Stores the last assigned NodeId
 * if the device is @ref EMBER_STAR_COORDINATOR.
 */
typedef uint16_t tokTypeStackLastAllocatedId;

/**
 * @brief Type for COMMON_TOKEN_STACK_BOOT_COUNTER. Increments at boot
 * (during @ref emberInit()).
 */
typedef uint32_t tokTypeStackBootCounter;

/**
 * @brief Type for COMMON_TOKEN_STACK_PARENT_LONG_ID. Stores the Long Id of the parent
 * of this device. Only used for @ref EMBER_MAC_MODE_DEVICE and
 * @ref EMBER_MAC_MODE_SLEEPY_DEVICE device types.
 */
typedef EmberEUI64 tokTypeParentLongId;
/** @} END Token types  */

/********************************************************************************************************************
 * @name Common Token Object Key IDs
 * @brief The Common Token object key is used as a distinct identifier tag for a
 * token stored in Common Token Manager.
 *
 * Every token must have a defined Dynamic Token object key ID and the object key
 * ID must be unique. The object key ID defined must be in the following
 * format:
 * COMMON_TOKEN_tokenname
 * where tokenname is the name of the token without COMMON_TOKEN_ prefix.
 *@{*/
// STACK KEYS
#define COMMON_TOKEN_STACK_NVDATA_VERSION           SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_CONNECT | 0x0001), 0)
#define COMMON_TOKEN_STACK_NVDATA_VERSION_SIZE      sizeof(tokTypeStackNvdataVersion)

#define COMMON_TOKEN_STACK_NODE_DATA                SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_CONNECT | 0x0003), 0)
#define COMMON_TOKEN_STACK_NODE_DATA_SIZE           sizeof(tokTypeStackNodeData)

#define COMMON_TOKEN_STACK_SECURITY_KEY             SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_CONNECT | 0x0004), 0)
#define COMMON_TOKEN_STACK_SECURITY_KEY_SIZE        sizeof(tokTypeStackKey)

#define COMMON_TOKEN_STACK_NONCE_COUNTER            SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_CONNECT | 0x0005), 1)
#define COMMON_TOKEN_STACK_NONCE_COUNTER_SIZE       sizeof(tokTypeStackNonceCounter)

#define COMMON_TOKEN_STACK_SECURITY_KEY_ID          SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_CONNECT | 0x009A), 0)
#define COMMON_TOKEN_STACK_SECURITY_KEY_ID_SIZE     sizeof(tokTypeStackKeyID)

// This key is used for an indexed token and the subsequent 0x7F keys are also reserved.
#define COMMON_TOKEN_STACK_CHILD_TABLE              SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_CONNECT | 0x0010), 0)
#define COMMON_TOKEN_STACK_CHILD_TABLE_ENTRY_SIZE   sizeof(tokTypeStackChildTableEntry)

#define COMMON_TOKEN_STACK_LAST_ASSIGNED_ID         SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_CONNECT | 0x0090), 0)
#define COMMON_TOKEN_STACK_LAST_ASSIGNED_ID_SIZE    sizeof(tokTypeStackLastAllocatedId)

#define COMMON_TOKEN_STACK_BOOT_COUNTER             SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_CONNECT | 0x0091), 1)
#define COMMON_TOKEN_STACK_BOOT_COUNTER_SIZE        sizeof(tokTypeStackBootCounter)

#define COMMON_TOKEN_STACK_PARENT_LONG_ID           SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_CONNECT | 0x0092), 0)
#define COMMON_TOKEN_STACK_PARENT_LONG_ID_SIZE      sizeof(tokTypeParentLongId)
/** @} END Common Token Object Key IDs  */

/********************************************************************************************************************
 * @name Default values
 * @brief Default values to be set if no value is stored for token
 *@{*/
#define STACK_NVDATA_VERSION_DEFAULT            CURRENT_STACK_TOKEN_VERSION
#define STACK_NODE_DATA_DEFAULT                 { 0xFFFF, 0, 0xFF, 0xFF, 0xFFFF, 0xFFFF }
#define STACK_SECURITY_KEY_DEFAULT              { 0, }
#define STACK_NONCE_COUNTER_DEFAULT             0x00000000
#define STACK_SECURITY_KEY_ID_DEFAULT           0x00000000
#define STACK_CHILD_TABLE_DEFAULT               { 0, }
#define STACK_LAST_ASSIGNED_ID_DEFAULT          0x0000
#define STACK_BOOT_COUNTER_DEFAULT              0x0000
#define STACK_PARENT_LONG_ID_DEFAULT            { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF }
/** @} END Default values  */

#ifdef MAC_DEBUG_TOKEN
/********************************************************************************************************************
 * @name MAC debug tokens
 * @brief Additional tokens for MAC debug
 *@{*/
#include "stack/mac/token-mac-debug.h"
/** @} END MAC debug tokens  */
#endif
