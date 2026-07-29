/***************************************************************************//**
 * @file
 * @brief ESL Access Point NCP advertisement report filter.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
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

#include "esl_ap_ncp_adv_filter.h"
#include "esl_ap_ncp_adv_filter_config.h"
#include <stdint.h>

// ESL Service UUID 0x1857 (little-endian over the air)
#define ESL_AP_NCP_ESL_SERVICE_UUID            0x1857u
#define ESL_AP_NCP_AD_TYPE_INCOMPLETE_UUID16   0x02u
#define ESL_AP_NCP_AD_TYPE_COMPLETE_UUID16     0x03u
#define ESL_AP_NCP_AD_TYPE_SERVICE_DATA_UUID16 0x16u

static bool esl_ap_ncp_adv_filter_has_esl_uuid(uint8_t *data, uint8_t len)
{
  uint16_t i = 0;
  const uint8_t head_len = 2 * sizeof(uint8_t);
  const uint8_t uuid_len = sizeof(uint16_t);
  uint8_t ad_field_length;
  uint8_t ad_field_type;

  if (data == NULL || len < (head_len + uuid_len)) {
    return false;
  }

  while (i < (uint16_t)len) {
    ad_field_length = data[i];
    if (ad_field_length == 0) {
      break;
    }
    if (i + 1 + ad_field_length > len) {
      break;
    }

    ad_field_type = data[i + 1];
    if (ad_field_type == ESL_AP_NCP_AD_TYPE_INCOMPLETE_UUID16
        || ad_field_type == ESL_AP_NCP_AD_TYPE_COMPLETE_UUID16) {
      uint16_t field_end = i + 1 + ad_field_length;

      for (uint16_t j = i + head_len; j + uuid_len <= field_end && j + uuid_len <= len; j += uuid_len) {
        uint16_t uuid = *((uint16_t *)&data[j]);
        if (uuid == ESL_AP_NCP_ESL_SERVICE_UUID) {
          return true;
        }
      }
    } else if (ad_field_type == ESL_AP_NCP_AD_TYPE_SERVICE_DATA_UUID16) {
      if (ad_field_length >= (1 + uuid_len)) {
        uint16_t uuid = *((uint16_t *)&data[i + head_len]);
        if (uuid == ESL_AP_NCP_ESL_SERVICE_UUID) {
          return true;
        }
      }
    }

    i = i + 1 + ad_field_length;
  }

  return false;
}

static bool esl_ap_ncp_adv_filter_report(uint8_t *data, uint8_t len)
{
  return esl_ap_ncp_adv_filter_has_esl_uuid(data, len);
}

static bool esl_ap_ncp_adv_filter_allow_connectable(uint8_t event_flags)
{
#if ESL_AP_NCP_ADV_FILTER_NON_CONNECTABLE_ENABLE
  return (event_flags & SL_BT_SCANNER_EVENT_FLAG_CONNECTABLE) != 0u;
#else
  (void)event_flags;
  return true;
#endif
}

bool esl_ap_ncp_adv_filter_on_event(sl_bt_msg_t *evt)
{
#if !ESL_AP_NCP_ADV_FILTER_ENABLE
  (void)evt;
  return true;
#else
  uint8_t *data;
  uint8_t len;

  switch (SL_BT_MSG_ID(evt->header)) {
    case sl_bt_evt_scanner_legacy_advertisement_report_id:
      if (!esl_ap_ncp_adv_filter_allow_connectable(
            evt->data.evt_scanner_legacy_advertisement_report.event_flags)) {
        return false;
      }
#if ESL_AP_NCP_ADV_FILTER_LEGACY_ENABLE
      data = evt->data.evt_scanner_legacy_advertisement_report.data.data;
      len = evt->data.evt_scanner_legacy_advertisement_report.data.len;
      return esl_ap_ncp_adv_filter_report(data, len);
#else
      return true;
#endif

    case sl_bt_evt_scanner_extended_advertisement_report_id:
      if (!esl_ap_ncp_adv_filter_allow_connectable(
            evt->data.evt_scanner_extended_advertisement_report.event_flags)) {
        return false;
      }
#if ESL_AP_NCP_ADV_FILTER_EXTENDED_ENABLE
      // Complete reports only; fragment chains dropped due to the lack of reassembly
      if (evt->data.evt_scanner_extended_advertisement_report.data_completeness
          != sl_bt_scanner_data_status_complete) {
        return false;
      }
      data = evt->data.evt_scanner_extended_advertisement_report.data.data;
      len = evt->data.evt_scanner_extended_advertisement_report.data.len;
      return esl_ap_ncp_adv_filter_report(data, len);
#else
      return true;
#endif

    default:
      return true;
  }
#endif
}
