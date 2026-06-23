/**
 * @file ZW_wake_on_critical_message.h
 * @brief Common wire-format definitions for Command Class Wake On Critical Message (0x8D).
 *
 * This file is used while the ZW_classcmd.h file is not yet updated.
 *
 * @copyright 2026 Silicon Laboratories Inc.
 */

#ifndef ZW_WAKE_ON_CRITICAL_MESSAGE_H_
#define ZW_WAKE_ON_CRITICAL_MESSAGE_H_

#include <stdint.h>

/****************************************************************************/
/*                     CC ID and VERSION                                    */
/****************************************************************************/

#define COMMAND_CLASS_WAKE_ON_CRITICAL_MESSAGE            0x8D
#define COMMAND_CLASS_WAKE_ON_CRITICAL_MESSAGE_VERSION_V1 0x01

/****************************************************************************/
/*                     COMMAND IDENTIFIERS                                  */
/****************************************************************************/

#define COMMAND_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_SET    0x01
#define COMMAND_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_GET    0x02
#define COMMAND_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_REPORT 0x03
#define COMMAND_WAKE_ON_CRITICAL_MESSAGE_NOTIFY               0x04

/****************************************************************************/
/*                     FIELD MASKS / LIMITS                                 */
/****************************************************************************/

#define WAKE_ON_CRITICAL_MESSAGE_SEVERITY_MASK    0x0F
#define WAKE_ON_CRITICAL_MESSAGE_SEVERITY_MAX     15
#define WAKE_ON_CRITICAL_MESSAGE_SEVERITY_DEFAULT 0
#define WAKE_ON_CRITICAL_MESSAGE_NOTIFY_HEADER_SIZE 4

/****************************************************************************/
/*                     FRAME STRUCTURES                                     */
/****************************************************************************/

/** Configuration Set frame: [CC][Cmd][Reserved(4) | Severity(4)] */
typedef struct _ZW_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_SET_FRAME_ {
  uint8_t cmdClass;
  uint8_t cmd;
  uint8_t properties1;  /* bits 7-4: Reserved, bits 3-0: Severity */
} ZW_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_SET_FRAME;

/** Configuration Get frame: [CC][Cmd] */
typedef struct _ZW_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_GET_FRAME_ {
  uint8_t cmdClass;
  uint8_t cmd;
} ZW_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_GET_FRAME;

/** Configuration Report frame: [CC][Cmd][Reserved(4) | Severity(4)] */
typedef struct _ZW_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_REPORT_FRAME_ {
  uint8_t cmdClass;
  uint8_t cmd;
  uint8_t properties1;  /* bits 7-4: Reserved (0), bits 3-0: Severity */
} ZW_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_REPORT_FRAME;

typedef struct _wocm_context_t_ {
  uint16_t node_id;
  uint8_t severity_level;
} wocm_context_t;

#endif /* ZW_WAKE_ON_CRITICAL_MESSAGE_H_ */
