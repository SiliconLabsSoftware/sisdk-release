/***************************************************************************//**
 * @file
 * @brief USB Device Battery Charging Detection (BCD) API
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc.  Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement.
 * The software is governed by the sections of the MSLA applicable to Micrium
 * Software.
 *
 ******************************************************************************/

#ifndef SL_USBD_DRIVER_DWC_BCD_H
#define SL_USBD_DRIVER_DWC_BCD_H

#include <stdbool.h>
#include "sl_enum.h"
#include "sl_status.h"

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************//**
 * @brief USB BCD detection result/events.
 ******************************************************************************/
SL_ENUM(sl_usbd_bcd_type_t) {
  SL_USBD_BCD_DATA_CONTACT_DETECTION = 0x0,   ///< Data contact detection completed.
  SL_USBD_BCD_STD_DOWNSTREAM_PORT = 0x1,      ///< Standard downstream port (SDP).
  SL_USBD_BCD_CHARGING_DOWNSTREAM_PORT = 0x2, ///< Charging downstream port (CDP).
  SL_USBD_BCD_DEDICATED_CHARGING_PORT = 0x3,  ///< Dedicated charging port (DCP).
  SL_USBD_BCD_DETECTION_COMPLETED = 0x4,      ///< Detection state machine completed.
  SL_USBD_BCD_DETECTION_DCD_TIMEOUT,          ///< DCD timed out.
  SL_USBD_BCD_DETECTION_ERROR                 ///< Detection error reported by hardware.
};

/***************************************************************************//**
 * @brief Callback invoked on BCD state changes/results.
 ******************************************************************************/
typedef void (*sl_usbd_bcd_callback_t)(sl_usbd_bcd_type_t detection_type);

sl_status_t sl_usbd_bcd_register_callback(sl_usbd_bcd_callback_t callback);

void sl_usbd_bcd_unregister_callback(void);

/***************************************************************************//**
 * @brief Activates BCD hardware and clears pending BCD state.
 ******************************************************************************/
void sl_usbd_bcd_activate(void);

/***************************************************************************//**
 * @brief Deactivates BCD detection and masks BCD interrupts.
 ******************************************************************************/
void sl_usbd_bcd_deactivate(void);

/***************************************************************************//**
 * @brief Starts a full BCD detection sequence.
 ******************************************************************************/
void sl_usbd_bcd_detect(void);

/***************************************************************************//**
 * @brief Internal helper used by the DWC OTG FS ISR.
 ******************************************************************************/
void sli_usbd_bcd_trigger_event(sl_usbd_bcd_type_t detection_type);

/***************************************************************************//**
 * @brief Returns true if sl_usbd_bcd_deactivate() was called from the last
 *        BCD callback. Used by the ISR to avoid re-enabling detection after
 *        a termination request.
 ******************************************************************************/
bool sli_usbd_bcd_is_deactivated(void);

#ifdef __cplusplus
}
#endif

#endif // SL_USBD_DRIVER_DWC_BCD_H
