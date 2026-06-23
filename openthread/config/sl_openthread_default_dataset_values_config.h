/*******************************************************************************
 * @file
 * @brief OpenThread Default Dataset Values configuration file.
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

//-------- <<< Use Configuration Wizard in Context Menu >>> -----------------
//

// <h> OpenThread Default Dataset Values

// <o SL_OPENTHREAD_DEFAULT_DATASET_CHANNEL> Default Dataset Channel <11..26:1> <f.d>
// <d> 15
#define SL_OPENTHREAD_DEFAULT_DATASET_CHANNEL 15

// <o SL_OPENTHREAD_DEFAULT_DATASET_PANID> Default Dataset PAN ID <0..65534:1> <f.h>
// <d> 0x2222
#define SL_OPENTHREAD_DEFAULT_DATASET_PANID 0x2222

// <a.16 SL_OPENTHREAD_DEFAULT_DATASET_NETWORKKEY> Default Dataset Network Key <0..255> <f.h>
// <d> { 0x12, 0x34, 0xC0, 0xDE, 0x1A, 0xB5, 0x12, 0x34, 0xC0, 0xDE, 0x1A, 0xB5, 0x12, 0x34, 0xC0, 0xDE }
#define SL_OPENTHREAD_DEFAULT_DATASET_NETWORKKEY {0x12, 0x34, 0xC0, 0xDE, 0x1A, 0xB5, 0x12, 0x34, 0xC0, 0xDE, 0x1A, 0xB5, 0x12, 0x34, 0xC0, 0xDE}

// </h>