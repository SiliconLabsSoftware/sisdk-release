/**
 * @file
 * @copyright 2026 Silicon Laboratories Inc.
 */

#ifndef _COMMANDCLASSWAKEUPONCRITICALMESSAGE_H_
#define _COMMANDCLASSWAKEUPONCRITICALMESSAGE_H_

/****************************************************************************/
/*                              INCLUDE FILES                               */
/****************************************************************************/

#include <ZW_TransportEndpoint.h>
#include <ZW_application_transport_interface.h>
#include "ZW_wake_on_critical_message.h"

/**
 * @addtogroup CC
 * @{
 * @addtogroup WakeOnCriticalMessage
 * @{
 */

/****************************************************************************/
/*                     EXPORTED TYPES and DEFINITIONS                       */
/****************************************************************************/

/****************************************************************************/
/*                              EXPORTED DATA                               */
/****************************************************************************/

/****************************************************************************/
/*                           EXPORTED FUNCTIONS                             */
/****************************************************************************/

/**
 * @brief Returns the currently configured severity threshold.
 * @return Severity threshold value (0-15).
 */
uint8_t CC_WakeOnCriticalMessage_getSeverityThreshold(void);

/**
 * @}
 * @}
 */

#endif /* _COMMANDCLASSWAKEUPONCRITICALMESSAGE_H_ */
