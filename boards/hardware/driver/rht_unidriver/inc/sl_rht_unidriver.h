/***************************************************************************//**
 * @file
 * @brief Driver for Si70xx and SHT4x Relative Humidity and Temperature sensors
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

#ifndef SL_RHT_UNIDRIVER_H
#define SL_RHT_UNIDRIVER_H

#include <stdbool.h>
#include "sl_status.h"
#include "sl_i2cspm.h"

/***************************************************************************//**
 * @addtogroup rht_unidriver RHT UniDriver - Temperature/Humidity Sensor
 * @brief Unified driver for Si70xx (BRD4002A) and SHT4x (BRD4002B) sensors.
 *
 *        Works transparently regardless of which supported sensor is connected.
 * @details
 *   For a known board and sensor, using the si70xx_driver or sht4x_driver component
 *   alone avoids linking both sensor stacks and reduces flash. Use this module when the
 *   product or example must run on either hardware without a separate build per board.
 *
 *   Only @ref sl_rht_unidriver_init takes the I2C bus handle; it probes Si70xx then SHT4x
 *   on fixed board addresses and caches the bus plus selected part. All other functions
 *   use that cache only.
 *
 * @note
 *   The module keeps one static session. It is not re-entrant; call
 *   @ref sl_rht_unidriver_init again to re-probe or switch boards.

   @n @section rht_unidriver_backend_map Backend API mapping

   Silabs Si70xx (sl_si70xx.h):
   - @ref sl_si70xx_init is not used; discovery uses @ref sl_si70xx_present inside
     @ref sl_rht_unidriver_init only (no user calibration path from the dedicated init).
   - @ref sl_si70xx_present is internal to @ref sl_rht_unidriver_init; silicon ID is
     exposed via @ref sl_rht_unidriver_get_device_id.
   - @ref sl_si70xx_measure_rh_and_temp maps to @ref sl_rht_unidriver_measure_rh_and_temp
   - @ref sl_si70xx_read_rh_and_temp maps to @ref sl_rht_unidriver_read_rh_and_temp
   - @ref sl_si70xx_start_no_hold_measure_rh_and_temp maps to
     @ref sl_rht_unidriver_start_no_hold_measure_rh_and_temp
   - @ref sl_si70xx_get_firmware_revision maps to @ref sl_rht_unidriver_get_firmware_revision
   - @ref sl_si7013_measure_analog_voltage maps to @ref sl_rht_unidriver_measure_analog_voltage

   Sensirion SHT4x (sl_sht4x.h):
   - @ref sl_sht4x_init is not used; discovery uses @ref sl_sht4x_present with the same
     retry delay as the dedicated init (48-bit serial not cached).
   - @ref sl_sht4x_present is internal to @ref sl_rht_unidriver_init.
   - @ref sl_sht4x_measure_rh_and_temp maps to @ref sl_rht_unidriver_measure_rh_and_temp
   - @ref sl_rht_unidriver_read_rh_and_temp uses @ref sl_sht4x_measure_rh_and_temp on SHT4x
     (@ref sl_sht4x_read_rh_and_temp returns raw ADC codes only).
   - @ref sl_sht4x_enable_low_power_mode maps to @ref sl_rht_unidriver_enable_low_power_mode

   @n @section rht_unidriver_example RHT UniDriver example code

 @verbatim
 #include "sl_i2cspm_instances.h"
 #include "sl_rht_unidriver.h"

 int main(void)
 {
   uint32_t rh_pct_x1000;
   int32_t temp_mc;

   ...

   sl_rht_unidriver_init(sl_i2cspm_sensor);
   sl_rht_unidriver_measure_rh_and_temp(&rh_pct_x1000, &temp_mc);

   ...
 }
 @endverbatim
 * @{
 ******************************************************************************/

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************//**
 * @name Sensor identity
 * @{
 ******************************************************************************/
/**
 * Placeholder for @ref sl_rht_unidriver_get_device_id when the SHT4x path was
 * selected (not a Sensirion register value; distinguishes from Si70xx IDs).
 */
#define RHT_UNIDRIVER_SHT4X_ID      0x00U
/** @} */

/**************************************************************************//**
 * @brief
 *   Initialize the RHT sensor (Si70xx or SHT4x).
 * @param[in] i2cspm
 *   The I2C peripheral to use.
 * @details
 *   Probes Si70xx at the on-board RHT address (same as typical Si7021 placement), then
 *   SHT4x at its fixed address, with retries matching the dedicated drivers. Neither
 *   @ref sl_si70xx_init nor @ref sl_sht4x_init is called.
 * @retval SL_STATUS_OK A supported sensor is present on the I2C bus
 * @retval SL_STATUS_INITIALIZATION No supported sensor present
 * @retval SL_STATUS_NULL_POINTER @p i2cspm is NULL
 * @note
 *   Call @ref sl_rht_unidriver_init before any other function in this module.
 *****************************************************************************/
sl_status_t sl_rht_unidriver_init(sl_i2cspm_t *i2cspm);

/**************************************************************************//**
 * @brief
 *   Return the device ID cached during @ref sl_rht_unidriver_init.
 * @param[out] device_id
 *   Si70xx: 0x06 (Si7006), 0x0D (Si7013), 0x14 (Si7020), 0x15 (Si7021).
 *   SHT4x: @ref RHT_UNIDRIVER_SHT4X_ID.
 * @retval SL_STATUS_OK Cache is valid
 * @retval SL_STATUS_NULL_POINTER @p device_id is NULL
 * @retval SL_STATUS_FAIL Not initialized; @p *device_id is not modified
 *****************************************************************************/
sl_status_t sl_rht_unidriver_get_device_id(uint8_t *device_id);

/**************************************************************************//**
 * @brief
 *  Measure relative humidity and temperature from an Si70xx or SHT4x sensor.
 * @param[out] rh_data
 *   The relative humidity in percent (multiplied by 1000).
 * @param[out] t_data
 *   The temperature in milliCelsius.
 * @retval SL_STATUS_OK Success
 * @retval SL_STATUS_TRANSMIT I2C transmission error
 * @retval SL_STATUS_NULL_POINTER @p rh_data or @p t_data is NULL
 * @retval SL_STATUS_FAIL Not initialized
 *****************************************************************************/
sl_status_t sl_rht_unidriver_measure_rh_and_temp(uint32_t *rh_data, int32_t *t_data);

/**************************************************************************//**
 * @brief
 *  Read relative humidity and temperature from an Si70xx or SHT4x sensor.
 * @details
 *  For Si70xx devices this reads the result of a previously started no-hold
 *  measurement. For SHT4x devices this uses the same converted measurement as
 *  @ref sl_sht4x_measure_rh_and_temp (not raw @ref sl_sht4x_read_rh_and_temp).
 * @param[out] rh_data
 *   The relative humidity in percent (multiplied by 1000).
 * @param[out] t_data
 *   The temperature in milliCelsius.
 * @retval SL_STATUS_OK Success
 * @retval SL_STATUS_TRANSMIT I2C transmission error
 * @retval SL_STATUS_NULL_POINTER @p rh_data or @p t_data is NULL
 * @retval SL_STATUS_FAIL Not initialized
 *****************************************************************************/
sl_status_t sl_rht_unidriver_read_rh_and_temp(uint32_t *rh_data, int32_t *t_data);

/**************************************************************************//**
 * @brief
 *  Start a no hold measurement of relative humidity and temperature.
 * @details
 *  This mode is supported by Si70xx devices only.
 * @retval SL_STATUS_OK Success
 * @retval SL_STATUS_TRANSMIT I2C transmission error
 * @retval SL_STATUS_FAIL Not initialized
 * @retval SL_STATUS_NOT_SUPPORTED SHT4x path (no-hold not available)
 *****************************************************************************/
sl_status_t sl_rht_unidriver_start_no_hold_measure_rh_and_temp(void);

/**************************************************************************//**
 * @brief
 *  Read Firmware Revision from an Si7006/13/20/21 sensor.
 * @details
 *  SHT4x does not support this; returns @ref SL_STATUS_NOT_SUPPORTED when SHT4x is present.
 * @param[out] fw_rev
 *   The internal firmware revision. 0xFF === 1.0
 * @retval SL_STATUS_OK Success
 * @retval SL_STATUS_NULL_POINTER @p fw_rev is NULL
 * @retval SL_STATUS_FAIL Not initialized; @p *fw_rev is not modified
 * @retval SL_STATUS_NOT_SUPPORTED SHT4x path; @p *fw_rev is set to 0
 * @retval SL_STATUS_TRANSMIT I2C transmission error
 *****************************************************************************/
sl_status_t sl_rht_unidriver_get_firmware_revision(uint8_t *fw_rev);

/**************************************************************************//**
 * @brief
 *  Measure the analog voltage or thermistor temperature from the Si7013 sensor.
 * @note
 *  Analog voltage measurement only supported by Si7013.
 * @param[out] v_data
 *   The data read from the sensor.
 * @retval SL_STATUS_OK Success
 * @retval SL_STATUS_NULL_POINTER @p v_data is NULL
 * @retval SL_STATUS_FAIL Not initialized or non-Si7013 Si70xx
 * @retval SL_STATUS_NOT_SUPPORTED SHT4x path
 * @retval SL_STATUS_TRANSMIT I2C transmission error
 *****************************************************************************/
sl_status_t sl_rht_unidriver_measure_analog_voltage(int32_t *v_data);

/**************************************************************************//**
 * @brief
 *  Select the SHT4x measurement command byte for low-precision vs high-precision mode.
 * @details
 *  Wraps @ref sl_sht4x_enable_low_power_mode. Returns @ref SL_STATUS_NOT_SUPPORTED
 *  when the cached sensor is Si70xx.
 * @param[in] enable_low_power_mode
 *   True for low-precision (lower power) mode command byte; false for high-precision.
 * @param[out] sht4x_cmd_measure
 *   Receives the command byte to pass to measurement (same semantics as the SHT4x driver).
 *   Not written when the return value is not @ref SL_STATUS_OK.
 * @retval SL_STATUS_OK Success (SHT4x path)
 * @retval SL_STATUS_NULL_POINTER @p sht4x_cmd_measure is NULL
 * @retval SL_STATUS_FAIL Not initialized
 * @retval SL_STATUS_NOT_SUPPORTED Si70xx path
 *****************************************************************************/
sl_status_t sl_rht_unidriver_enable_low_power_mode(bool enable_low_power_mode,
                                                   uint8_t *sht4x_cmd_measure);

#ifdef __cplusplus
}
#endif

/** @} */

#endif /* SL_RHT_UNIDRIVER_H */
