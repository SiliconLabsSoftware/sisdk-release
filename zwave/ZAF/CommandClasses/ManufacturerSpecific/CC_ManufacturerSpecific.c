/**
 * @file
 * Handler for Command Class Manufacturer Specific.
 * @copyright 2022 Silicon Laboratories Inc.
 */

/****************************************************************************/
/*                              INCLUDE FILES                               */
/****************************************************************************/

#include "ZAF_types.h"
#include "ZW_TransportEndpoint.h"
#include "zaf_config_api.h"
#include "zpal_misc.h"

/****************************************************************************/
/*                      PRIVATE TYPES and DEFINITIONS                       */
/****************************************************************************/

#define DEVICE_ID_TYPE_SERIAL_NUMBER 1
#define DEVICE_ID_DATA_FORMAT_BINARY 1

/****************************************************************************/
/*                              PRIVATE DATA                                */
/****************************************************************************/

// Nothing here.

/****************************************************************************/
/*                              EXPORTED DATA                               */
/****************************************************************************/

// Nothing here.

/****************************************************************************/
/*                            PRIVATE FUNCTIONS                             */
/****************************************************************************/

static received_frame_status_t
CC_ManufacturerSpecific_handler(
  RECEIVE_OPTIONS_TYPE_EX *rxOpt,
  ZW_APPLICATION_TX_BUFFER *pFrameIn,
  __attribute__((unused)) uint8_t cmdLength,
  ZW_APPLICATION_TX_BUFFER * pFrameOut,
  uint8_t * pLengthOut
  )
{
  if (true == Check_not_legal_response_job(rxOpt)) {
    // None of the following commands support endpoint bit addressing.
    return RECEIVED_FRAME_STATUS_FAIL;
  }

  switch (pFrameIn->ZW_Common.cmd) {
    case MANUFACTURER_SPECIFIC_GET_V2:
      pFrameOut->ZW_ManufacturerSpecificReportV2Frame.cmdClass = COMMAND_CLASS_MANUFACTURER_SPECIFIC_V2;
      pFrameOut->ZW_ManufacturerSpecificReportV2Frame.cmd      = MANUFACTURER_SPECIFIC_REPORT_V2;

      uint16_t manufacturerID = zaf_config_get_manufacturer_id();
      uint16_t productID      = zaf_config_get_product_id();
      uint16_t productTypeID  = zaf_config_get_product_type_id();

      pFrameOut->ZW_ManufacturerSpecificReportV2Frame.manufacturerId1 = (uint8_t)(manufacturerID >> 8);
      pFrameOut->ZW_ManufacturerSpecificReportV2Frame.manufacturerId2 = (uint8_t)(manufacturerID &  0xFF);
      pFrameOut->ZW_ManufacturerSpecificReportV2Frame.productTypeId1  = (uint8_t)(productTypeID  >> 8);
      pFrameOut->ZW_ManufacturerSpecificReportV2Frame.productTypeId2  = (uint8_t)(productTypeID  &  0xFF);
      pFrameOut->ZW_ManufacturerSpecificReportV2Frame.productId1      = (uint8_t)(productID      >> 8);
      pFrameOut->ZW_ManufacturerSpecificReportV2Frame.productId2      = (uint8_t)(productID      &  0xFF);

      *pLengthOut = (uint8_t)sizeof(ZW_MANUFACTURER_SPECIFIC_REPORT_V2_FRAME);

      return RECEIVED_FRAME_STATUS_SUCCESS;
    case DEVICE_SPECIFIC_GET_V2:
    {
      /*
       * Spec: Device Specific Report is variable-length (Device ID Length + Device ID Data 1..N).
       * ZW_classcmd.h is auto-generated and only has fixed-size structs (1/2/3/4 bytes). We build
       * the variable-length frame in the tx buffer so the full serial is sent without truncation.
       */
      size_t serialLen = zpal_get_serial_number_length();
      /* Length field is 5 bits (max 31); frame must fit in tx buffer */
      if (serialLen > (TX_DATA_MAX_DATA_SIZE - 4)) {
        serialLen = TX_DATA_MAX_DATA_SIZE - 4;
      }
      if (serialLen > 31) {
        serialLen = 31;
      }

      /* ZW_classcmd.h has no variable-length struct; we write the frame by hand into the tx buffer
       * (same layout as ZW_DEVICE_SPECIFIC_REPORT_1BYTE_V2_FRAME header + deviceIdData1..N). */
      uint8_t *p = (uint8_t *)pFrameOut;
      p[0] = COMMAND_CLASS_MANUFACTURER_SPECIFIC_V2;         /* cmdClass */
      p[1] = DEVICE_SPECIFIC_REPORT_V2;                      /* cmd */
      p[2] = (uint8_t)(DEVICE_ID_TYPE_SERIAL_NUMBER & DEVICE_SPECIFIC_REPORT_PROPERTIES1_DEVICE_ID_TYPE_MASK_V2);   /* properties1 */
      p[3] = (uint8_t)((DEVICE_ID_DATA_FORMAT_BINARY << DEVICE_SPECIFIC_REPORT_PROPERTIES2_DEVICE_ID_DATA_FORMAT_SHIFT_V2) & DEVICE_SPECIFIC_REPORT_PROPERTIES2_DEVICE_ID_DATA_FORMAT_MASK_V2)
             | ((uint8_t)serialLen & DEVICE_SPECIFIC_REPORT_PROPERTIES2_DEVICE_ID_DATA_LENGTH_INDICATOR_MASK_V2);   /* properties2 */
      zpal_get_serial_number(&p[4]);                         /* deviceIdData1..N (variable-length) */

      *pLengthOut = 4 + (uint8_t)serialLen;
      return RECEIVED_FRAME_STATUS_SUCCESS;
    }
    default:
      return RECEIVED_FRAME_STATUS_NO_SUPPORT;
  }
}

REGISTER_CC_V2(COMMAND_CLASS_MANUFACTURER_SPECIFIC, MANUFACTURER_SPECIFIC_VERSION_V2, CC_ManufacturerSpecific_handler);
