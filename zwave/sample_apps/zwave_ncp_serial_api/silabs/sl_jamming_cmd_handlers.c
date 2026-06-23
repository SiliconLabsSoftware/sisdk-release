/**
 * @file sl_jamming_cmd_handlers.c
 * @brief Jamming detection callbacks: send unsolicited Serial API frames to host.
 * @copyright 2026 Silicon Laboratories Inc.
 */

#include "cmd_handlers.h"
#include "app.h"
#include "sl_jamming_detection.h"
#include "sl_jamming_cmd_handlers.h"
#include "SerialAPI.h"
#include "zpal_status.h"

ZW_ADD_CMD(FUNC_ID_PROP_JAMMING_DETECTION_COMMAND)
{
  zpal_status_t status = ZPAL_STATUS_FAIL;

  uint8_t subcmd = frame->payload[0];

  switch (subcmd) {
    case FUNC_ID_PROP_JAMMING_SUBCOMMAND_COLLECTION:
      /* Payload: [0]=subcmd, [1]=duration LSB, [2]=duration MSB. Duration in 100 ms periods; 0xFFFF = forever. */
      if (3 == frame_payload_len(frame)) {
        uint16_t duration = (uint16_t)(((uint16_t)frame->payload[2] << 8) | (uint16_t)frame->payload[1]);
        status = sl_jamming_detection_enable_collection(duration);
        if (ZPAL_STATUS_OK == status) {
          /* ZW_Module -> Host: 0xF1 |  0x01 | duration LSB | duration MSB | */
          compl_workbuf[0] = FUNC_ID_PROP_JAMMING_SUBCOMMAND_COLLECTION;
          compl_workbuf[1] = (uint8_t)(duration & 0xFF);
          compl_workbuf[2] = (uint8_t)(duration >> 8);
          DoRespond_workbuf(3);
        }
      }

      break;

    case FUNC_ID_PROP_JAMMING_SUBCOMMAND_CHANNEL_CONFIGURATION:
      /* Payload: [0]=subcmd, [1]=channel (0..3), [2]=RSSI threshold dBm (int8), [3]=trigger (samples above threshold). */
      if (4 == frame_payload_len(frame)) {
        uint8_t channel = frame->payload[1];
        int8_t threshold = (int8_t)frame->payload[2];
        uint8_t trigger = frame->payload[3];

        status = sl_jamming_detection_set_channel_configuration(channel, threshold, trigger);

        /* Success response: 4 bytes (subcmd, channel, nibble1, nibble2). */
        if (ZPAL_STATUS_OK == status) {
          compl_workbuf[0] = FUNC_ID_PROP_JAMMING_SUBCOMMAND_CHANNEL_CONFIGURATION;
          compl_workbuf[1] = channel;
          compl_workbuf[2] = (uint8_t)threshold;
          compl_workbuf[3] = trigger;
          DoRespond_workbuf(4);
        }
      }

      break;

    case FUNC_ID_PROP_JAMMING_SUBCOMMAND_REPORT_CONFIGURATION:
      /* Payload: [0]=subcmd, [1]=duration LSB, [2]=duration MSB. Duration in seconds */
      if (3 == frame_payload_len(frame)) {
        uint16_t interval = (uint16_t)(((uint16_t)frame->payload[2] << 8) | (uint16_t)frame->payload[1]);
        status = sl_jamming_detection_set_report_interval_sec(interval);

        if (ZPAL_STATUS_OK == status) {
          /* ZW_Module -> Host: 0xF1 |  0x03 | duration LSB | duration MSB | */
          compl_workbuf[0] = FUNC_ID_PROP_JAMMING_SUBCOMMAND_REPORT_CONFIGURATION;
          compl_workbuf[1] = (uint8_t)(interval & 0xFF);
          compl_workbuf[2] = (uint8_t)(interval >> 8);
          DoRespond_workbuf(3);
        }
      }

      break;

    default:
      /* Unknown F1 subcommand: Respond with status FAIL and DoRespond(1) */
      break;
  }

  if (ZPAL_STATUS_OK != status) {
    DoRespond(1);
  }
}
