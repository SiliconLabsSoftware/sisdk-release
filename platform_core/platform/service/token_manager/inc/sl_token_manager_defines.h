/***************************************************************************//**
 * @file sl_token_manager_defines.h
 * @brief Header file for generic token manager defines
 * @version 1.0.0
 *******************************************************************************
 * # License
 * <b>Copyright 2025 Silicon Laboratories, Inc, www.silabs.com</b>
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
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/
#ifndef SL_TOKEN_MANAGER_DEFINES_H
#define SL_TOKEN_MANAGER_DEFINES_H

/***************************************************************************//**
 * @addtogroup common_token_manager Common Token Manager (CTM)
 * @{
 ******************************************************************************/
/***************************************************************************//**
 * @addtogroup defines Common Token Manager Defines
 * @brief This module provides defines for the Common Token Manager (CTM).
 * @{
 * @details
 * The defines in this module are used for creating 32-bit token identifier
 * to identify static device tokens, static secure tokens and dynamic tokens in the CTM.
 *
 * @note For more information on tokens and CTM refer to silabs application note
 * @ref 'AN1154: Using Tokens for Non-Volatile Data Storage'
 ******************************************************************************/
/** @cond DO_NOT_INCLUDE_WITH_DOXYGEN */
// MACRO's for mask values to identify token as
// NVM3 or STATIC DEVICE or STATIC SECURE
#define SL_TOKEN_DYNAMIC_MASK                     (0xF8000000)
#define SL_TOKEN_STATIC_MASK                      (0xE0000000)

/*
 * The new 32-bit token identifier used for creating the key-length-value chain.
 * To differentiate between different objects we utilize the
 * upper 5 bits of the key identifier:
 *
 * bit (31:27) Maps to:
 *
 * 0b00000 NVM3 (Default instance)
 * 0b00001 NVM3 (Secondary instance - Zwave usage)
 * 0b0001x Reserved for additional NVM3 instances
 * 0b110xx Static device tokens
 * 0b111xx Static secure tokens
 * 0b100xx Reserved for future use
 * 0b101xx Reserved for future use
 *
 * The Key-Length-Value system works as a chain of KLV objects.
 * A KLV object is identified in the following way:
 *
 * 31:29 | 28:16    | 15:0
 * 0b1xx | Reserved | Key
 *
 * */
#define SL_TOKEN_TYPE_NVM3                        (0x00000000U)
#define SL_TOKEN_TYPE_NVM3_SECONDARY              (0x08000000U)
#define SL_TOKEN_TYPE_STATIC_DEVICE               (0xC0000000U)
#define SL_TOKEN_TYPE_STATIC_SECURE               (0xE0000000U)
/** @endcond */

/**
 * @defgroup NVM3 NVM3 key space regions
 * @brief MACRO's for NVM3 Default Instance Key Space Regions.
 * The NVM3 default instance is used for storing dynamic tokens.
 *
 * NVM3 is used for Non-Volatile storage across all our device types (zigbee, Bluetooth, MCU...).
 * Each object in the NVM3 is addressed by a 20-bit key. These keys need to be unique within an NVM3 instance
 * to avoid collisions. Such collisions can for instance occur if a user application writes to an object
 * that the RF stack is using for a different purpose.
 * For multi-protocol applications we also risk collisions when where two stacks inadvertently use the
 * same object key in a non compatible way. By default an NVM3 default instance will be shared among
 * all stacks and application code.
 * To avoid collisions it is proposed to use the 4 MSBs of the default instance NVM3 key to split
 * the NVM3 ID space into the regions in the table below. Each stack team is responsible for
 * managing the keys within their regions. A user should be able to use the keys in the User region as they wish.
 * If any configurator tools use any keys in the User region these keys should be made clearly
 * visible to the user so they can avoid using the same keys for NVM3 objects created manually in
 * the application code. Refer application note 'AN1135: Using Third Generation Non-Volatile Memory (NVM3) Data Storage' for more details.
 *
 * @note The key regions from 0xC0000 to 0xFFFFF are reserved.
 */

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for User.
 */
#define SL_TOKEN_NVM3_REGION_USER                 (0x00000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Zigbee EmberZnet Stack.
 */
#define SL_TOKEN_NVM3_REGION_ZIGBEE               (0x10000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for OpenThread Stack.
 */
#define SL_TOKEN_NVM3_REGION_THREAD               (0x20000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Connect Stack.
 */
#define SL_TOKEN_NVM3_REGION_CONNECT              (0x30000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Bluetooth Stack.
 */
#define SL_TOKEN_NVM3_REGION_BT                   (0x40000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Z-Wave Stack.
 */
#define SL_TOKEN_NVM3_REGION_ZWAVE                (0x50000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Bluetooth Mesh Stack.
 */
#define SL_TOKEN_NVM3_REGION_BTMESH               (0x60000)

/** @ingroup NVM3 key space regions
 *  @brief Reserved.
 */
#define SL_TOKEN_NVM3_REGION_RESERVED0            (0x70000)

// NVM3 Common region
/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Apple Homekit.
 */
#define SL_TOKEN_NVM3_REGION_APPLE_HK             (0x80000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Zigbee Cluster Library (ZCL).
 */
#define SL_TOKEN_NVM3_REGION_ZCL                  (0x81000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for DotDot.
 */
#define SL_TOKEN_NVM3_REGION_DOTDOT               (0x82000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Platform CLI SM.
 */
#define SL_TOKEN_NVM3_REGION_PLT_CLISM            (0x83000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Platform Crypto.
 */
#define SL_TOKEN_NVM3_REGION_PLT_CRYPTO           (0x83100)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Bootloader.
 */
#define SL_TOKEN_NVM3_REGION_BTL                  (0x87100)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Matter.
 */
#define SL_TOKEN_NVM3_REGION_MATTER               (0x87200)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for AWS Late Provisioning.
 */
#define SL_TOKEN_NVM3_REGION_AWS_LATE_PRN         (0x88000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for KNX IoT.
 */
#define SL_TOKEN_NVM3_REGION_KNX_IOT              (0x89000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Antenna Calibration (Platform).
 */
#define SL_TOKEN_NVM3_REGION_ANT_CAL_PLT          (0x89800)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Antenna Calibration (RAIL).
 */
#define SL_TOKEN_NVM3_REGION_ANT_CAL_RAIL         (0x89880)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Aliro.
 *  @note A total of 1536 key ids are allocated for Aliro.
 */
#define SL_TOKEN_NVM3_REGION_ALIRO                (0x89a00)

/** @ingroup NVM3 key space regions
*   @brief NVM3 Key Region for All the platform specific tokens.
*   This region allocates keys from 0x8DC00 to 0x8FFFF.
*   Below are the keys that are used within this region:
*   - 0x8DC00: Crash log token
*   - 0x8DC01 - 0x8DFFF: Unused keys
*   - 0x8E000 - 0x8EFFF: Static device override tokens
*   - 0x8F000 - 0x8FFFF: Static secure override tokens
*/
#define SL_TOKEN_NVM3_REGION_PLATFORM            (0x8DC00)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Wi-SUN.
 */
#define SL_TOKEN_NVM3_REGION_WISUN                (0x90000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Sidewalk.
 */
#define SL_TOKEN_NVM3_REGION_SW                   (0xA0000)

/** @ingroup NVM3 key space regions
 *  @brief NVM3 Key Region for Wi-Fi.
 */
#define SL_TOKEN_NVM3_REGION_WIFI                 (0xB0000)

/**
 * @defgroup StaticToken Static Token Key Space Regions
 * @brief MACRO's for Static Token Key Space Regions. Applicable for both static device and static secure tokens for series 3 devices.
 *
 * CTM has reserved dedicated token key ranges for each domain, with a total of 128 token keys allocated per domain.
 * The token key ranges are defined as follows:
 * - 0x000 to 0x07F used for defining tokens for the Common domain.
 * - 0x080 to 0x0FF used for defining tokens for the Zigbee domain.
 * - 0x100 to 0x17F used for defining tokens for the Thread domain.
 * - 0x180 to 0x1FF used for defining tokens for the Connect domain.
 * - 0x200 to 0x27F used for defining tokens for the Bluetooth domain.
 * - 0x280 to 0x2FF used for defining tokens for the Z-Wave domain.
 * - 0x300 to 0x37F used for defining tokens for the Bluetooth Mesh domain.
 * - 0x380 to 0x3FF used for defining tokens for the Matter domain.
 * - 0x400 to 0x47F used for defining tokens for the Wi-Sun domain.
 * - 0x480 to 0x4FF used for defining tokens for the Sidewalk domain.
 * - 0x500 to 0x57F used for defining tokens for the Wi-Fi domain.
 * - 0x580 to 0x5FF reserved for future use.
 * - 0x600 to 0x67F used for defining tokens for the User domain.
 * - 0x680 to 0xFFF reserved for future use.
 *
 * A new token added for series 3 devices must follow the domain-specific token Id ranges mentioned above.
 * And the new tokens must not conflict with the existing tokens. Below is an example of how to define a new token:
 *       
 *       @code{.c}
 *       // Defining a new static device token for the Matter domain:
 *       #define TOKEN_MFG_MATTER_NEW_STATIC_DEVICE_TOKEN          (SL_TOKEN_STATIC_DEVICE_TOKENS | SL_TOKEN_DOMAIN_STATIC_MATTER | 0x0)
 *       #define TOKEN_MFG_MATTER_NEW_STATIC_DEVICE_TOKEN_SIZE     (2u)                //   2 bytes
 *
 *       // Defining a new static secure token for the Matter domain:
 *       #define TOKEN_MFG_MATTER_NEW_STATIC_SECURE_TOKEN          (SL_TOKEN_STATIC_SECURE_DATA_TOKENS | SL_TOKEN_DOMAIN_STATIC_MATTER | 0x0)
 *       #define TOKEN_MFG_MATTER_NEW_STATIC_SECURE_TOKEN_SIZE     (2u)                //   2 bytes
 *       @endcode
 *
 * @note The token IDs listed below are reserved and must not be used to define tokens for any specific domain.
 *       For example, the token @ref TOKEN_MFG_CTUNE (a static device token) is reserved with Id 0x100 and must not be 
 *       reused to define a static device token for the Thread domain. Similarly, the token 
 *       @ref TOKEN_MFG_CBKE_DATA (a static secure token) is reserved with Id 0x204 and must not be reused to define 
 *       a static secure token for the Bluetooth domain. These reservations exist because there are already deployed 
 *       devices using these token Id values, which are distributed across the overall token Id space. 
 *       Reusing these Id's would create compatibility issues with existing devices. 
 * @note Reserved token IDs by type (do not use below IDs for defining new tokens for the respective domains):
 *    | Static device token (Domain : Token IDs)                  | Static secure token (Domain : Token IDs)     |
 *    |-----------------------------------------------------------|----------------------------------------------|
 *    | Common : 0x002, 0x00C, 0x020, 0x030, 0x034, 0x038, 0x064  | Bluetooth : 0x204, 0x260, 0x270              |
 *    | Zigbee : 0x09C                                            | Z-Wave : 0x298                               |
 *    | Thread : 0x100                                            |                                              |
 *    | Connect : 0x1f0                                           |                                              |
 * 
 */
 /** @ingroup StaticToken
 *  @brief Static Token Domain for Common tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_COMMON       (0x000)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Zigbee tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_ZIGBEE       (0x080)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Thread tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_THREAD       (0x100)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Connect tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_CONNECT      (0x180)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Bluetooth tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_BT           (0x200)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Z-Wave tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_ZWAVE        (0x280)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Bluetooth Mesh tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_BT_MESH      (0x300)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Matter tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_MATTER       (0x380)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Wi-Sun tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_WI_SUN       (0x400)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Sidewalk tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_SIDEWALK     (0x480)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for Wi-Fi tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_WI_FI        (0x500)

 /** @ingroup StaticToken
 *  @brief Static Token Domain for User tokens. 
 */
#define SL_TOKEN_DOMAIN_STATIC_USER         (0x600)

/** @cond DO_NOT_INCLUDE_WITH_DOXYGEN */
#ifndef SL_TOKEN_NVM3_OVERRIDE
//To store a static token in NVM3 region we shall follow NVM3 key format.
//Each object in the NVM3 is addressed by a 20-bit key
//4MSB bits(19:16) of the NVM3 key are used to identify the static tokens
//that are stored in NVM3 memory space. The values used for representing static tokens in NVM3 region are
//0x8E->for static device tokens
//0x8F->for static secure tokens is used along with the existing static token ID to form a 20bit NVM3 key.
#define SL_TOKEN_STATIC_TOKEN_KEY_MASK                      (0x0FFF)
#define SL_TOKEN_STATIC_TOKEN_RANGE_MASK                    (0xFF000)
#define SL_TOKEN_STATIC_TOKEN_BASE_TYPE_KEY_MASK            (0x3000)
#define SL_TOKEN_NVM3_REGION_STATIC_TOKEN_RANGE_OFFSET      (0xC)
#define SL_TOKEN_NVM3_REGION_STATIC_DEVICE_TOKEN_RANGE_ID   (0x8E)
#define SL_TOKEN_NVM3_REGION_STATIC_SECURE_TOKEN_RANGE_ID   (0x8F)
#define SL_TOKEN_NVM3_REGION_STATIC_DEVICE_TOKEN_RANGE      (SL_TOKEN_NVM3_REGION_STATIC_DEVICE_TOKEN_RANGE_ID \
                                                             << SL_TOKEN_NVM3_REGION_STATIC_TOKEN_RANGE_OFFSET)

#define SL_TOKEN_NVM3_REGION_STATIC_SECURE_TOKEN_RANGE      (SL_TOKEN_NVM3_REGION_STATIC_SECURE_TOKEN_RANGE_ID \
                                                             << SL_TOKEN_NVM3_REGION_STATIC_TOKEN_RANGE_OFFSET)

#endif

//The bits 28:16 has the size of the static token embedded
#define SL_TOKEN_STATIC_TOKEN_SIZE_OFFSET                (0x10)
#define SL_TOKEN_STATIC_TOKEN_SIZE_MASK                  (0x1FFF)
//The bit 20 defines if the NVM3 token is a counter object or a data object
#define SL_TOKEN_NVM3_OBJ_TYPE_COUNTER_TOKEN             (1)
#define SL_TOKEN_NVM3_OBJ_TYPE_OFFSET                    (0x14)
#define SL_TOKEN_NVM3_OBJ_TYPE_BIT_MASK                  (SL_TOKEN_NVM3_OBJ_TYPE_COUNTER_TOKEN << SL_TOKEN_NVM3_OBJ_TYPE_OFFSET)
/** @endcond */

/**
 * @brief Helper MACRO to get the size of a predefined token.
 *
 * @param[in] token_name  Name of the static token.
 *
 * @note The size MACRO's should be predefined to use this helper macro.
 */

#define SL_TOKEN_GET_STATIC_TOKEN_SIZE(token_name)       token_name##_SIZE

/**
 * @brief Helper MACRO to create a new static device token in 32-bit identifier format,
 *        the tokens created are stored in secure memory region and are mass erase protected,
 *        this MACRO can be used with `sl_token_get_data()` or `sl_token_set_data()` functions,
 *        for more information @ref `sl_token_manager_defines.h`.
 *
 * @param[in] token  16-bit unique key @ref sl_token_manager_manufacturing.h file
 *                   or sl_custom_manufacturing_token_header.h.
 * Key format  :
 *    | 31:30 | 29                 | 28:16       | 15:0 |
 *    |-------|--------------------|-------------|------|
 *    | type  | static token type  | Data length | key  |
 *
 *    - type              : Static Token.
 *    - static token type : 0 - Static device token region (secure memory region)
 *    - key               : 16-bit unique key.
 *
 */
#define SL_TOKEN_GET_STATIC_DEVICE_TOKEN(token)    (SL_TOKEN_TYPE_STATIC_DEVICE \
                                                    | token                     \
                                                    | (token##_SIZE << SL_TOKEN_STATIC_TOKEN_SIZE_OFFSET))

/**
 * @brief Helper MACRO to create a new static secure token in 32-bit identifier format,
 *        the tokens created are stored in dedicated flash region, with additional security measures
 *        and are not protected by mass/device erase,
 *        this MACRO can be used with `sl_token_get_data()` or `sl_token_set_data()` functions,
 *        for more information @ref `sl_token_manager_defines.h`.
 *
 * @param[in] token  16-bit unique key @ref sl_token_manager_manufacturing.h file
 *                   or sl_custom_manufacturing_token_header.h.
 * Key format  :
 *    | 31:30 | 29                 | 28:16       | 15:0 |
 *    |-------|--------------------|-------------|------|
 *    | type  | static token type  | Data length | key  |
 *
 *    - type              : Static Token.
 *    - static token type : 1 - Static secure token region (dedicated flash region)
 *    - key               : 16-bit unique key.
 *
 */
#define SL_TOKEN_GET_STATIC_SECURE_TOKEN(token)    (SL_TOKEN_TYPE_STATIC_SECURE \
                                                    | token                     \
                                                    | (token##_SIZE << SL_TOKEN_STATIC_TOKEN_SIZE_OFFSET))

/**
 * @brief Helper MACRO to create dynamic token, user has to take care of providing the unique
 *        token for each NVM3 token created, the tokens created are stored in NVM3 region and are
 *        not protected by mass/device/nvm3 erase,
 *        this MACRO can be used with `sl_token_get_data()` or `sl_token_set_data()` functions,
 *        for more information @ref `sl_token_manager_defines.h`.
 *
 * @param[in] token 20-bit NVM3 key (it has both NVM3 domain and NVM3 key combined).
 * @param[in] IsCounterObj should be set to 1, if a token is created for counter objects.
 *
 * Key format  :
 *    | 31:27 | 26:21    | 20               |19:16        | 15:0     |
 *    |-------|----------|------------------|-------------|----------|
 *    | type  | reserved | NVM3 object type | NVM3 domain | NVM3 key |
 *
 *    - NVM3 object type : 0 - Data object
 *                         1 - Counter object
 *    - NVM3 domain      : NVM3 Default Instance Key Space Regions @ref NVM3 key space regions
 *    - NVM3 key         : 16-bit unique key.
 *
 */
#define SL_TOKEN_GET_DYNAMIC_TOKEN(token, IsCounterObj)   (SL_TOKEN_TYPE_NVM3 \
                                                           | token            \
                                                           | (IsCounterObj << SL_TOKEN_NVM3_OBJ_TYPE_OFFSET))

/**
 * @brief Helper MACRO to create dynamic token for NVM3 secondary instance, user has to take
 *        care of providing the unique token for each NVM3 token created, the tokens created are
 *        stored in NVM3 region and are not protected by mass/device/nvm3 erase,
 *        this MACRO can be used with `sl_token_get_data()` or `sl_token_set_data()` functions,
 *        for more information @ref `sl_token_manager_defines.h`.
 *
 * @param[in] token 20-bit NVM3 key (it has both NVM3 domain and NVM3 key combined).
 * @param[in] IsCounterObj should be set to 1, if a token is created for counter objects.
 * Key format  :
 *    | 31:27 | 26:21    | 20               |19:16        | 15:0     |
 *    |-------|----------|------------------|-------------|----------|
 *    | type  | reserved | NVM3 object type | NVM3 domain | NVM3 key |
 *    - NVM3 object type : 0 - Data object
 *                         1 - Counter object
 *    - NVM3 domain      : @ref NVM3 key space regions
 *    - NVM3 key         : 16-bit unique key.
 *
 * @note This is specifically used for Z-Wave usage, where the secondary instance of NVM3 is utilized.
 *
 */
#define SL_TOKEN_GET_DYNAMIC_SECONDARY_INSTANCE_TOKEN(token, IsCounterObj)   (SL_TOKEN_TYPE_NVM3_SECONDARY \
                                                                              | token                      \
                                                                              | (IsCounterObj << SL_TOKEN_NVM3_OBJ_TYPE_OFFSET))

/**
 * @brief Helper MACRO to create a NVM3 override key for static token,
 *        this MACRO can be used with `sl_token_get_data()` or `sl_token_set_data()` functions,
 *        the range for NVM3 Domain region for a static token override key is predefined
 *        for more information @ref `sl_token_manager_defines.h`.
 *
 * @param[in] token 16-bit unique key @ref sl_token_manager_manufacturing.h file
 *                  or sl_custom_manufacturing_token_header.h.
 * Key format  :
 *    | 31:27 | 26:21    | 20       |19:16        | 15:12                  | 11:0                   |
 *    |-------|----------|----------|-------------|------------------------|------------------------|
 *    | type  | reserved | reserved | NVM3 region | NVM3 key (high nibble) | NVM3 key (low 12 bits) |
 *
 *    - type                  : NVM3 Override Token.
 *    - NVM3 region           : The region 0x80000 is used for static override tokens.
 *    - NVM3 key (high nibble): Most significant 4 bits of the NVM3 key.
 *                              0xE000 for static device tokens.
 *                              0xF000 for static secure tokens.
 *    - NVM3 key (low 12 bits): Least significant 12 bits of the NVM3 key.
 *                              The static token key is a 16-bit unique value.
 *                              For override tokens, the high nibble identifies
 *                              the key type(NVM3 key (high nibble)), and the remaining 12 bits are reused.
 */
#ifndef SL_TOKEN_GET_DYNAMIC_OVER_RIDE_TOKEN
#define SL_TOKEN_GET_DYNAMIC_OVER_RIDE_TOKEN(token)   (SL_TOKEN_TYPE_NVM3                                                                       \
                                                       | (token & SL_TOKEN_STATIC_TOKEN_KEY_MASK)                                               \
                                                       | (((token & SL_TOKEN_STATIC_TOKEN_BASE_TYPE_KEY_MASK) == SL_TOKEN_STATIC_DEVICE_TOKENS) \
                                                          ? SL_TOKEN_NVM3_REGION_STATIC_DEVICE_TOKEN_RANGE                                      \
                                                          : SL_TOKEN_NVM3_REGION_STATIC_SECURE_TOKEN_RANGE))
#endif

/** @} (end addtogroup defines) */
/** @} (end addtogroup common_token_manager) */

#endif // SL_TOKEN_MANAGER_DEFINES_H
