/***************************************************************************//**
 * @file
 * @brief UniDriver for Si70xx and SHT4x Relative Humidity and Temperature sensors
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

#include "sl_rht_unidriver.h"
#include "sl_si70xx.h"
#include "sl_sht4x.h"
#include "sl_sleeptimer.h"

/*******************************************************************************
 * @note
 *   Discovery runs only in @ref sl_rht_unidriver_init, which stores the I2C bus
 *   in the module cache. Other APIs use that cached bus; @c sensor_addr is the
 *   7-bit address selected for Si70xx or SHT4x transfers.
 ******************************************************************************/

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

/** @cond DO_NOT_INCLUDE_WITH_DOXYGEN */
#define RHT_UNIDRIVER_INIT_RETRY_DELAY_MS       80U
/** Si70xx on boards such as BRD4002A (matches SI7021_ADDR). */
#define RHT_UNIDRIVER_PROBE_SI70XX_ADDR         0x40U
/** SHT4x fixed address (matches SHT4X_ADDR). */
#define RHT_UNIDRIVER_PROBE_SHT4X_ADDR          0x44U

typedef enum {
  RHT_UNIDRIVER_SENSOR_NONE = 0,
  RHT_UNIDRIVER_SENSOR_SI70XX,
  RHT_UNIDRIVER_SENSOR_SHT4X,
} rht_unidriver_sensor_type_t;

typedef struct {
  sl_i2cspm_t *i2cspm;                     /* I2C bus used when init succeeded. */
  uint8_t sensor_addr;                   /* 7-bit address for si70xx/sht4x transfers. */
  uint8_t device_id;                      /* Si70xx silicon ID, or RHT_UNIDRIVER_SHT4X_ID. */
  rht_unidriver_sensor_type_t sensor_type; /* Active backend. */
} rht_unidriver_sensor_cache_t;

static rht_unidriver_sensor_cache_t sensor_cache;

static void rht_unidriver_cache_store(sl_i2cspm_t *i2cspm,
                        rht_unidriver_sensor_type_t sensor_type,
                        uint8_t sensor_addr,
                        uint8_t dev_id);

static bool rht_unidriver_cache_valid(void);

/***************************************************************************//**
 * @brief
 *  Record which sensor is active after @ref sl_rht_unidriver_init.
 ******************************************************************************/
static void rht_unidriver_cache_store(sl_i2cspm_t *i2cspm,
                        rht_unidriver_sensor_type_t sensor_type,
                        uint8_t sensor_addr,
                        uint8_t dev_id)
{
  sensor_cache.i2cspm = i2cspm;
  sensor_cache.sensor_addr = sensor_addr;
  sensor_cache.device_id = dev_id;
  sensor_cache.sensor_type = sensor_type;
}

/**
 * @brief
 *   Whether the module cache holds an active session (init succeeded).
 */
static bool rht_unidriver_cache_valid(void)
{
  return (sensor_cache.sensor_type != RHT_UNIDRIVER_SENSOR_NONE)
         && (sensor_cache.i2cspm != NULL);
}
/** @endcond */

/***************************************************************************//**
 * @brief
 *   Initializes the RHT sensor (Si70xx or SHT4x).
 * @details
 *   Discovers hardware using @ref sl_si70xx_present at @ref RHT_UNIDRIVER_PROBE_SI70XX_ADDR
 *   and @ref sl_sht4x_present at @ref RHT_UNIDRIVER_PROBE_SHT4X_ADDR only (no @c *_init).
 *   Si70xx: two @ref sl_si70xx_present attempts with
 *   @ref RHT_UNIDRIVER_INIT_RETRY_DELAY_MS between failures.
 *   SHT4x: same flow as @ref sl_sht4x_init - @ref sl_sht4x_present (NULL serial),
 *   on failure wait @ref RHT_UNIDRIVER_INIT_RETRY_DELAY_MS and probe again.
 ******************************************************************************/
sl_status_t sl_rht_unidriver_init(sl_i2cspm_t *i2cspm)
{
  uint8_t si_id = 0U;
  uint8_t sensor_addr;
  uint8_t stored_id;
  rht_unidriver_sensor_type_t kind;
  sl_status_t status;
  bool si70xx_sensor_present;

  if (i2cspm == NULL) {
    return SL_STATUS_NULL_POINTER;
  }

  sensor_cache = (rht_unidriver_sensor_cache_t){ 0 };

  si70xx_sensor_present = sl_si70xx_present(i2cspm, RHT_UNIDRIVER_PROBE_SI70XX_ADDR, &si_id);
  if (!si70xx_sensor_present) {
    sl_sleeptimer_delay_millisecond(RHT_UNIDRIVER_INIT_RETRY_DELAY_MS);
    si70xx_sensor_present = sl_si70xx_present(i2cspm, RHT_UNIDRIVER_PROBE_SI70XX_ADDR, &si_id);
  }

  if (si70xx_sensor_present) {
    kind = RHT_UNIDRIVER_SENSOR_SI70XX;
    sensor_addr = RHT_UNIDRIVER_PROBE_SI70XX_ADDR;
    stored_id = si_id;
  } else {
    /* Same pattern as @ref sl_sht4x_init: present, then 80 ms + present if needed. */
    status = sl_sht4x_present(i2cspm, RHT_UNIDRIVER_PROBE_SHT4X_ADDR, NULL);
    if (status != SL_STATUS_OK) {
      sl_sleeptimer_delay_millisecond(RHT_UNIDRIVER_INIT_RETRY_DELAY_MS);
      status = sl_sht4x_present(i2cspm, RHT_UNIDRIVER_PROBE_SHT4X_ADDR, NULL);
    }
    if (status != SL_STATUS_OK) {
      return SL_STATUS_INITIALIZATION;
    }
    kind = RHT_UNIDRIVER_SENSOR_SHT4X;
    sensor_addr = RHT_UNIDRIVER_PROBE_SHT4X_ADDR;
    stored_id = RHT_UNIDRIVER_SHT4X_ID;
  }

  rht_unidriver_cache_store(i2cspm, kind, sensor_addr, stored_id);
  return SL_STATUS_OK;
}

/**************************************************************************//**
 * @brief
 *  Return the device ID cached during initialization.
 * @details
 *  Fails if init did not succeed.
 *****************************************************************************/
sl_status_t sl_rht_unidriver_get_device_id(uint8_t *device_id)
{
  if (device_id == NULL) {
    return SL_STATUS_NULL_POINTER;
  }
  if (!rht_unidriver_cache_valid()) {
    return SL_STATUS_FAIL;
  }
  *device_id = sensor_cache.device_id;
  return SL_STATUS_OK;
}

/**************************************************************************//**
 * @brief
 *  Measure relative humidity and temperature.
 * @details
 *  Requires prior successful @ref sl_rht_unidriver_init.
 *****************************************************************************/
sl_status_t sl_rht_unidriver_measure_rh_and_temp(uint32_t *rh_data, int32_t *t_data)
{
  if ((rh_data == NULL) || (t_data == NULL)) {
    return SL_STATUS_NULL_POINTER;
  }
  if (!rht_unidriver_cache_valid()) {
    return SL_STATUS_FAIL;
  }
  if (sensor_cache.sensor_type == RHT_UNIDRIVER_SENSOR_SHT4X) {
    return sl_sht4x_measure_rh_and_temp(sensor_cache.i2cspm, sensor_cache.sensor_addr,
                                        rh_data, t_data);
  }
  return sl_si70xx_measure_rh_and_temp(sensor_cache.i2cspm, sensor_cache.sensor_addr,
                                       rh_data, t_data);
}

/**************************************************************************//**
 * @brief
 *  Read relative humidity and temperature.
 * @details
 *  Si70xx: typically after no-hold measure. SHT4x: uses @ref sl_sht4x_measure_rh_and_temp
 *  so outputs are percent×1000 and milliCelsius (@ref sl_sht4x_read_rh_and_temp is raw-only).
 *****************************************************************************/
sl_status_t sl_rht_unidriver_read_rh_and_temp(uint32_t *rh_data, int32_t *t_data)
{
  if ((rh_data == NULL) || (t_data == NULL)) {
    return SL_STATUS_NULL_POINTER;
  }
  if (!rht_unidriver_cache_valid()) {
    return SL_STATUS_FAIL;
  }
  if (sensor_cache.sensor_type == RHT_UNIDRIVER_SENSOR_SHT4X) {
    return sl_sht4x_measure_rh_and_temp(sensor_cache.i2cspm, sensor_cache.sensor_addr,
                                        rh_data, t_data);
  }
  return sl_si70xx_read_rh_and_temp(sensor_cache.i2cspm, sensor_cache.sensor_addr,
                                    rh_data, t_data);
}

/**************************************************************************//**
 * @brief
 *  Start no-hold measurement of relative humidity and temperature.
 * @details
 *  Si70xx only; returns @ref SL_STATUS_NOT_SUPPORTED when the cached sensor is SHT4x.
 *****************************************************************************/
sl_status_t sl_rht_unidriver_start_no_hold_measure_rh_and_temp(void)
{
  if (!rht_unidriver_cache_valid()) {
    return SL_STATUS_FAIL;
  }
  if (sensor_cache.sensor_type == RHT_UNIDRIVER_SENSOR_SHT4X) {
    return SL_STATUS_NOT_SUPPORTED;
  }
  return sl_si70xx_start_no_hold_measure_rh_and_temp(sensor_cache.i2cspm,
                                                      sensor_cache.sensor_addr);
}

/**************************************************************************//**
 * @brief
 *  Read firmware revision (Si70xx only).
 * @details
 *  Not supported on SHT4x; returns @ref SL_STATUS_NOT_SUPPORTED with @p *fw_rev cleared.
 *****************************************************************************/
sl_status_t sl_rht_unidriver_get_firmware_revision(uint8_t *fw_rev)
{
  if (fw_rev == NULL) {
    return SL_STATUS_NULL_POINTER;
  }
  if (!rht_unidriver_cache_valid()) {
    return SL_STATUS_FAIL;
  }
  if (sensor_cache.sensor_type == RHT_UNIDRIVER_SENSOR_SHT4X) {
    *fw_rev = 0U;
    return SL_STATUS_NOT_SUPPORTED;
  }
  return sl_si70xx_get_firmware_revision(sensor_cache.i2cspm, sensor_cache.sensor_addr,
                                         fw_rev);
}

/**************************************************************************//**
 * @brief
 *  Measure analog voltage/thermistor (Si7013 only).
 * @details
 *  Delegates to @ref sl_si7013_measure_analog_voltage; fails for SHT4x and
 *  non-Si7013 Si70xx parts per the underlying driver.
 *****************************************************************************/
sl_status_t sl_rht_unidriver_measure_analog_voltage(int32_t *v_data)
{
  if (v_data == NULL) {
    return SL_STATUS_NULL_POINTER;
  }
  if (!rht_unidriver_cache_valid()) {
    return SL_STATUS_FAIL;
  }
  if (sensor_cache.sensor_type == RHT_UNIDRIVER_SENSOR_SHT4X) {
    return SL_STATUS_NOT_SUPPORTED;
  }
  return sl_si7013_measure_analog_voltage(sensor_cache.i2cspm, sensor_cache.sensor_addr,
                                          v_data);
}

/**************************************************************************//**
 * @brief
 *  Select SHT4x LPM vs HPM measurement command byte.
 *****************************************************************************/
sl_status_t sl_rht_unidriver_enable_low_power_mode(bool enable_low_power_mode,
                                                   uint8_t *sht4x_cmd_measure)
{
  if (sht4x_cmd_measure == NULL) {
    return SL_STATUS_NULL_POINTER;
  }
  if (!rht_unidriver_cache_valid()) {
    return SL_STATUS_FAIL;
  }
  if (sensor_cache.sensor_type != RHT_UNIDRIVER_SENSOR_SHT4X) {
    return SL_STATUS_NOT_SUPPORTED;
  }
  sl_sht4x_enable_low_power_mode(enable_low_power_mode, sht4x_cmd_measure);
  return SL_STATUS_OK;
}
