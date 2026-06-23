/***************************************************************************//**
 *  @brief Silicon Labs Real-Time Locationing library for AoA/D, CS and locationing
 *******************************************************************************
 * # License
 * <b>Copyright 2019-2020 Silicon Laboratories Inc. www.silabs.com</b>
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

/**************************************************************************//**
*
*  Information on open-source software used with the library can be found in
*  the included license.txt file.
*
******************************************************************************/

/**************************************************************************//**
 *  @file
 *  This is the API for the Silicon Labs Real-Time Locationing library.
 *  It provides an interface for estimating arrival and departure angles of
 *  signals and the positions of AoA/AoD signal transmitters. AoA stands for
 *  Angle-of-Arrival and AoD for Angle-of-Departure. AoX is used when
 *  referring to both techniques.
 *
 *  Estimators can be created individually for each locator node using the API.
 *  Even multiple estimators with different parameters can be created for a
 *  single node. An instance of the estimator is created as a libitem and the
 *  estimator is initialized. Next, the estimation parameters such as antenna
 *  array type, number of antennas, estimation mode, and so on can be set
 *  using the function calls described below.
 *
 *  One snapshot means a set of IQ-samples with exactly one sample per
 *  each antenna.
 *
 *****************************************************************************/

#ifndef SL_RTL_CLIB_API_H
#define SL_RTL_CLIB_API_H

#include <stdint.h>
#include <stdbool.h>
#include <time.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @addtogroup sl_rtl_error Error Codes
 * @{
 *
 * @brief RTL library Error Codes
 *
 */

/// RTL error code
enum sl_rtl_error_code{
  SL_RTL_ERROR_SUCCESS = 0, ///< Successful execution / estimation complete
  SL_RTL_ERROR_ARGUMENT, ///< Invalid argument
  SL_RTL_ERROR_OUT_OF_MEMORY, ///< Memory / allocation failure
  SL_RTL_ERROR_ESTIMATION_IN_PROGRESS, ///< Estimation not yet finished
  SL_RTL_ERROR_NUMBER_OF_SNAPHOTS_DO_NOT_MATCH, ///< Initialized and calculated number of snapshots do not match
  SL_RTL_ERROR_ESTIMATOR_NOT_CREATED, ///< Estimator not yet created
  SL_RTL_ERROR_ESTIMATOR_ALREADY_CREATED, ///< Estimator already created, operation is not supported
  SL_RTL_ERROR_NOT_INITIALIZED, ///< Library item not yet initialized
  SL_RTL_ERROR_INTERNAL, ///< An internal error occurred
  SL_RTL_ERROR_IQ_SAMPLE_QA, ///< IQ sample quality analysis failed
  SL_RTL_ERROR_FEATURE_NOT_SUPPORTED, ///< The requested feature is not supported by the library
  SL_RTL_ERROR_INCORRECT_MEASUREMENT, ///< The error of the last measurement for this locator was too large
  SL_RTL_ERROR_CS_CHANNEL_MAP_TOO_SPARSE, ///< Too many skipped channels in the proposed channel map
  SL_RTL_ERROR_CS_CHANNEL_MAP_TOO_FEW_CHANNELS, ///< Too few channels in the proposed channel map
  SL_RTL_ERROR_CS_CHANNEL_SPACING_TOO_LARGE, ///< Channel spacing is too large in the proposed channel map
  SL_RTL_ERROR_POOR_INPUT_DATA_QUALITY, ///< The input data quality is poor
  SL_RTL_ERROR_QUEUE_FULL, ///< The RTL task's input queue is full

  SL_RTL_ERROR_LAST ///< Number of error codes
};
/** @} */ // end addtogroup sl_rtl_error







/**
 * @addtogroup sl_rtl_log Logging
 * @{
 *
 * @brief Logging
 *
 * RTL events are logged as follows:
 *
 * 1. Initialize the logging.
 * 2. Configure the logging with the configuration parameters.
 *   - Configuration is only allowed once in a logging session.
 * 3. Enable logging for the RTL libitem(s).
 *   - The libitem(s) can be added before or after the estimator(s) are created.
 *   - Disable logging for the RTL libitem(s) to stop the logging for the given
 *     RTL libitem.
 * 5. Deinitialize logging. This will disable logging for all the remaining RTL
 *    libitems.
 */

// -----------------------------------------------------------------------------
// Definitions
// Enums, structs, typedefs
#if defined(__IAR_SYSTEMS_ICC__)
  #ifndef PACKSTRUCT
    #define PACKSTRUCT(decl)      __packed decl
  #endif
#elif defined(__GNUC__)
  #ifndef PACKSTRUCT
    #if defined(_WIN32)
      #define PACKSTRUCT(decl)    decl __attribute__((packed, gcc_struct))
    #else
      #define PACKSTRUCT(decl)    decl __attribute__((packed))
    #endif
  #endif
#else
  #ifndef PACKSTRUCT
    #define PACKSTRUCT(decl) decl
  #endif
#endif

#define SL_RTL_LOG_SDK_VERSION_CHAR_ARRAY_MAX_SIZE 64
#define SL_RTL_LOG_COMMAND_LINE_OPTIONS_CHAR_ARRAY_MAX_SIZE 64

typedef void (*sl_rtl_log_callback_function)(uint8_t *log_data,
                                             size_t log_data_len);

typedef PACKSTRUCT (struct {
  sl_rtl_log_callback_function log_callback_function; /** < Callback function
                                                            for logging. */
  char sdk_version[SL_RTL_LOG_SDK_VERSION_CHAR_ARRAY_MAX_SIZE]; /**< Unique
                                                                      version
                                                                      string */
  char command_line_options[
    SL_RTL_LOG_COMMAND_LINE_OPTIONS_CHAR_ARRAY_MAX_SIZE
  ];         /**< Optional field for debugging purpose.
                    The command line options include the command name. */
}) sl_rtl_log_params;

// -----------------------------------------------------------------------------
// Public functions

/**************************************************************************//**
 * Initiate the RTL logging.
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_log_init(void);

/**************************************************************************//**
 * Register the configuration parameters for the logging.
 *
 * @param[in] log_params Pointer to the sl_rtl_log_params
 * @return ::SL_RTL_ERROR_SUCCESS if successful
 *****************************************************************************/
enum sl_rtl_error_code
sl_rtl_log_configure(const sl_rtl_log_params *log_params);

/**************************************************************************//**
 * Deinitiate the RTL logging.
 *****************************************************************************/
enum sl_rtl_error_code sl_rtl_log_deinit(void);

/** @} */ // end addtogroup sl_rtl_log

#ifdef __cplusplus
}
#endif

#endif /*SL_RTL_CLIB_API_H*/