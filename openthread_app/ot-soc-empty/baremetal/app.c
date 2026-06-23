/*******************************************************************************
 * @file
 * @brief Core application logic.
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

#include <assert.h>
#include <openthread-core-config.h>
#include <string.h>
#include <openthread/config.h>
#include <openthread/tasklet.h>

#include "app.h"
#include "openthread-system.h"
#include "sl_memory_manager.h"

// Use this config file to edit the default dataset for this application
#include "sl_openthread_default_dataset_values_config.h"

static otInstance *sInstance = NULL;

/**
 * This functions creates the dataset used for forming/joining the OT network and sets it as active.
 * If a network with the same configuration already exists, this device will join that network.
 * Otherwise, it will create a netork with these settings.
 * NOTE: Having a hard-coded default dataset can be a security risk, and thus this function should only be used in test
 * and sample applications.
 */
static void setNetworkConfiguration(void)
{
    otError              error;
    otOperationalDataset aDataset;

    memset(&aDataset, 0, sizeof(otOperationalDataset));

    /* Set Active Timestamp */
    aDataset.mActiveTimestamp.mSeconds             = 1;
    aDataset.mComponents.mIsActiveTimestampPresent = true;

    /* Set Channel */
    aDataset.mChannel                      = SL_OPENTHREAD_DEFAULT_DATASET_CHANNEL;
    aDataset.mComponents.mIsChannelPresent = true;

    /* Set Pan ID */
    aDataset.mPanId                      = (otPanId)SL_OPENTHREAD_DEFAULT_DATASET_PANID;
    aDataset.mComponents.mIsPanIdPresent = true;

    /* Set Network Key */
    uint8_t key[OT_NETWORK_KEY_SIZE] = SL_OPENTHREAD_DEFAULT_DATASET_NETWORKKEY;
    memcpy(aDataset.mNetworkKey.m8, key, sizeof(aDataset.mNetworkKey));
    aDataset.mComponents.mIsNetworkKeyPresent = true;

    /* Set the Active Operational Dataset to this dataset */
    error = otDatasetSetActive(sInstance, &aDataset);
    assert(error == OT_ERROR_NONE);
}

/**
 * This function creates the OT Instance. It runs before app_init.
 */
void sl_ot_create_instance(void)
{
    sInstance = otInstanceInitSingle();
    assert(sInstance);
}

/******************************************************************************
 * Application Init.
 *****************************************************************************/
void app_init(void)
{
    // Set up dataset parameters
    setNetworkConfiguration();
    // Bring IPv6 interface up and start Thread
    assert(otIp6SetEnabled(sInstance, true) == OT_ERROR_NONE);
    assert(otThreadSetEnabled(sInstance, true) == OT_ERROR_NONE);
    /////////////////////////////////////////////////////////////////////////////
    // Put your additional application initialization code here!               //
    // This is called once during start-up.                                    //
    /////////////////////////////////////////////////////////////////////////////
}

/******************************************************************************
 * Application Process Action.
 *****************************************************************************/
void app_process_action(void)
{
    otTaskletsProcess(sInstance);
    otSysProcessDrivers(sInstance);
    /////////////////////////////////////////////////////////////////////////////
    // Put your additional application code here!                              //
    /////////////////////////////////////////////////////////////////////////////
}

/******************************************************************************
 * Application Exit.
 *****************************************************************************/
void app_exit(void)
{
    otInstanceFinalize(sInstance);
}
