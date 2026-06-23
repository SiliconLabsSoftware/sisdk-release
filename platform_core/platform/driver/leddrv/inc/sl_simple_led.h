/***************************************************************************//**
 * @file
 * @brief Simple LED Driver
 *******************************************************************************
 * # License
 * <b>Copyright 2019 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef SL_SIMPLE_LED_H
#define SL_SIMPLE_LED_H

#include "sl_led.h"
#include "sl_gpio.h"

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************//**
 * @addtogroup led
 * @{
 ******************************************************************************/

/***************************************************************************//**
 * @addtogroup simple_led Simple LED Driver
 * @brief Simple LED Driver can be used to execute basic LED functionalities
 *        such as on, off, toggle, or retrive the on/off status on Silicon Labs
 *        devices. Subsequent sections provide more insight into this module.
 * @{
 ******************************************************************************/

/*******************************************************************************
 ******************************   DEFINES   ************************************
 ******************************************************************************/

#define SL_SIMPLE_LED_POLARITY_ACTIVE_LOW  0U ///< LED Active polarity Low
#define SL_SIMPLE_LED_POLARITY_ACTIVE_HIGH 1U ///< LED Active polarity High

/*******************************************************************************
 *****************************   DATA TYPES   **********************************
 ******************************************************************************/

typedef uint8_t sl_led_polarity_t;    ///< LED GPIO polarities (active high/low)

/// A Simple LED instance
typedef struct {
  sl_gpio_port_t    port;             ///< LED port
  uint8_t           pin;              ///< LED pin
  sl_led_polarity_t polarity;         ///< Initial state of LED
} sl_simple_led_context_t;

/*******************************************************************************
 *****************************   PROTOTYPES   **********************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize the simple LED driver.
 *
 * @param[in] led_handle        Pointer to simple-led specific data:
 *                                - sl_simple_led_context_t
 *
 * @return    Status Code:
 *              - SL_STATUS_OK
 ******************************************************************************/
sl_status_t sl_simple_led_init(void *led_handle);

/***************************************************************************//**
 * Turn on a simple LED.
 *
 * @param[in] led_handle        Pointer to simple-led specific data:
 *                                - sl_simple_led_context_t
 *
 ******************************************************************************/
void sl_simple_led_turn_on(void *led_handle);

/***************************************************************************//**
 * Turn off a simple LED.
 *
 * @param[in] led_handle        Pointer to simple-led specific data:
 *                                - sl_simple_led_context_t
 *
 ******************************************************************************/
void sl_simple_led_turn_off(void *led_handle);

/***************************************************************************//**
 * Toggle a simple LED.
 *
 * @param[in] led_handle        Pointer to simple-led specific data:
 *                                - sl_simple_led_context_t
 *
 ******************************************************************************/
void sl_simple_led_toggle(void *led_handle);

/***************************************************************************//**
 * Get the current state of the simple LED.
 *
 * @param[in] led_handle       Pointer to simple-led specific data:
 *                               - sl_simple_led_context_t
 *
 * @return    sl_led_state_t   Current state of simple LED. 1 for on, 0 for off
 ******************************************************************************/
sl_led_state_t sl_simple_led_get_state(void *led_handle);

/** @} (end group simple_led) */
/** @} (end group led) */

// ******** THE REST OF THE FILE IS DOCUMENTATION ONLY !***********************
/// @addtogroup simple_led Simple LED Driver
/// @{
///
///   @details
///
///   The Simple LED Driver can be used to execute basic LED functionalities such as on,
///   off, toggle, or retrieve the on/off state on Silicon Labs devices. Subsequent
///   sections provide more insight into this module.
///
///   @n @section simple_led_intro Introduction
///
///   The Simple LED driver is a module of the LED driver that provides the functionality
///   to control simple on/off LEDs.
///
///   @n @section simple_led_apis Instance pointer vs context pointer
///
///   - **Common LED API** (@c sl_led_init, @c sl_led_turn_on, @c sl_led_turn_off,
///     @c sl_led_toggle, @c sl_led_get_state): pass @c &sl_led_<instance> (e.g.
///     @c &sl_led_led0). Recommended for most application code.
///   - **Simple LED API** (@c sl_simple_led_*): expects a pointer to
///     @ref sl_simple_led_context_t (as @c void *), **not** @c &sl_led_led0. Obtain it from
///     the exported instance: @code (void *)sl_led_led0.context @endcode Replace @c led0
///     with your instance name if different. Do **not** use @c &simple_led0_context in
///     application code — that symbol is not declared in @c sl_simple_led_instances.h
///     (see configuration notes below).
///
///   @n @section simple_led_config Simple LED Configuration
///
///   Simple LEDs use the @ref sl_led_t struct and their @ref sl_simple_led_context_t
///   struct. These are automatically generated into the following files, as well as
///   instance specific headers with macro definitions in them. The samples below
///   are for a single instance called "led0".
///
///   @code{.c}
///// sl_simple_led_instances.c
///
/// #include "sl_simple_led.h"
/// #include "sl_gpio.h"
/// #include "sl_simple_led_led0_config.h"
///
/// sl_simple_led_context_t simple_led0_context = {
///   .port = SL_SIMPLE_LED_LED0_PORT,
///   .pin = SL_SIMPLE_LED_LED0_PIN,
///   .polarity = SL_SIMPLE_LED_LED0_POLARITY,
/// };
///
/// const sl_led_t sl_led_led0 = {
///   .context = &simple_led0_context,
///   .init = sl_simple_led_init,
///   .turn_on = sl_simple_led_turn_on,
///   .turn_off = sl_simple_led_turn_off,
///   .toggle = sl_simple_led_toggle,
///   .get_state = sl_simple_led_get_state,
/// };
///
/// void sl_simple_led_init_instances(void)
/// {
///   sl_led_init(&sl_led_led0);
/// }
/// @endcode
///
///   @note The sl_simple_led_instances.c file is shown with only one instance, but if more
///         were in use they would all appear in this .c file.
///
///   @code{.c}
/// // sl_simple_led_instances.h
///
/// #ifndef SL_SIMPLE_LED_INSTANCES_H
/// #define SL_SIMPLE_LED_INSTANCES_H
///
/// #include "sl_simple_led.h"
///
/// extern const sl_led_t sl_led_led0;
///
/// void sl_simple_led_init_instances(void);
///
/// #endif // SL_SIMPLE_LED_INSTANCES_H
///
///   @endcode
///
///   @note The @c .h file exports only the LED instance (@c sl_led_led0), not the underlying
///         context struct. User code must not reference @c simple_led0_context by name.
///
///   @n @section simple_led_usage Simple LED Usage
///
///   The simple LED driver is for LEDs with basic on/off functionality. There are no
///   additional functions beyond those in the common driver. Include
///   @c sl_simple_led_instances.h in application code that uses the generated instances.
///   When the Simple LED component is present, startup typically calls
///   @c sl_simple_led_init_instances(); you may omit extra @c sl_led_init unless needed.
///
///   **Recommended — common LED API** (uses @c sl_led_t *, not context):
///
///   @code{.c}
///#include "sl_simple_led_instances.h"
///
///sl_led_turn_on(&sl_led_led0);
///sl_led_turn_off(&sl_led_led0);
///sl_led_toggle(&sl_led_led0);
///
///sl_led_state_t state_led = sl_led_get_state(&sl_led_led0);
///   @endcode
///
///   **Alternative — @c sl_simple_led_* directly** (must pass context via @c .context; cast
///   to @c void * matches the API prototype and avoids toolchain warnings):
///
///   @code{.c}
///#include "sl_simple_led_instances.h"
///
///sl_simple_led_init((void *)sl_led_led0.context);
///sl_simple_led_turn_on((void *)sl_led_led0.context);
///sl_simple_led_turn_off((void *)sl_led_led0.context);
///sl_simple_led_toggle((void *)sl_led_led0.context);
///
///sl_led_state_t state_simple = sl_simple_led_get_state((void *)sl_led_led0.context);
///   @endcode
///
///   Do **not** pass @c &sl_led_led0 to @c sl_simple_led_turn_on (or similar), and do **not**
///   use @c &simple_led0_context from application code.
///
/// @} end group simple_led ********************************************************/

#ifdef __cplusplus
}
#endif

#endif // SL_SIMPLE_LED_H
