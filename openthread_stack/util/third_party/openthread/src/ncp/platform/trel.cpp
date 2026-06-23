/*
 *  Copyright (c) 2025, The OpenThread Authors.
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. Neither the name of the copyright holder nor the
 *     names of its contributors may be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 *  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 *  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 *  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 *  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 *  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @file
 *   NCP TREL platform implementation.
 *
 *   Forwards TREL UDP datagrams between the Thread stack and the OTBR host
 *   using SPINEL_PROP_THREAD_UDP_FORWARD_STREAM.
 */

#include "openthread-core-config.h"

#if OPENTHREAD_CONFIG_RADIO_LINK_TREL_ENABLE && OPENTHREAD_CONFIG_UDP_FORWARD_ENABLE

#include <string.h>

#include <openthread/instance.h>
#include <openthread/logging.h>
#include <openthread/trel.h>
#include <openthread/udp.h>
#include <openthread/platform/trel.h>

#include "common/code_utils.hpp"

namespace {
constexpr uint16_t kMaxTrelPacketSize = 1400;

otUdpSocket sUdpForwardSocket;
bool        sUdpForwardSocketIsOpen = false;
} // namespace

static otPlatTrelCounters sCounters;

static void HandleUdpForwardReceive(void *aContext, otMessage *aMessage, const otMessageInfo *aMessageInfo)
{
    otInstance *instance = static_cast<otInstance *>(aContext);
    uint8_t     buffer[kMaxTrelPacketSize];
    uint16_t    length;
    uint16_t    readLength;
    otSockAddr  senderAddr;

    VerifyOrExit(otTrelIsEnabled(instance));

    length = otMessageGetLength(aMessage);
    VerifyOrExit(length > 0 && length <= sizeof(buffer));

    readLength = otMessageRead(aMessage, 0, buffer, length);
    VerifyOrExit(readLength == length);

    senderAddr.mAddress = aMessageInfo->mPeerAddr;
    senderAddr.mPort    = aMessageInfo->mPeerPort;

    sCounters.mRxPackets++;
    sCounters.mRxBytes += length;

    otPlatTrelHandleReceived(instance, buffer, length, &senderAddr);

exit:
    return;
}

extern "C" void otPlatTrelSend(otInstance       *aInstance,
                               const uint8_t    *aUdpPayload,
                               uint16_t          aUdpPayloadLen,
                               const otSockAddr *aDestSockAddr)
{
    otMessage        *message = nullptr;
    otMessageInfo     messageInfo;
    otMessageSettings messageSettings = {true, OT_MESSAGE_PRIORITY_NORMAL};
    otError           error           = OT_ERROR_NONE;

    VerifyOrExit(aUdpPayload != nullptr && aDestSockAddr != nullptr);
    VerifyOrExit(otTrelIsEnabled(aInstance));

    memset(&messageInfo, 0, sizeof(messageInfo));
    messageInfo.mPeerAddr        = aDestSockAddr->mAddress;
    messageInfo.mPeerPort        = aDestSockAddr->mPort;
    messageInfo.mSockPort        = otTrelGetUdpPort(aInstance);
    messageInfo.mIsHostInterface = true;

    message = otUdpNewMessage(aInstance, &messageSettings);
    VerifyOrExit(message != nullptr, error = OT_ERROR_NO_BUFS);

    SuccessOrExit(error = otMessageAppend(message, aUdpPayload, aUdpPayloadLen));

    error = otUdpSendDatagram(aInstance, message, &messageInfo);
    if (error == OT_ERROR_NONE)
    {
        message = nullptr;
        sCounters.mTxPackets++;
        sCounters.mTxBytes += aUdpPayloadLen;
    }
exit:
    if (message != nullptr)
    {
        otMessageFree(message);
    }
    return;
}

extern "C" void otPlatTrelEnable(otInstance *aInstance, uint16_t *aUdpPort)
{
    otError    error = OT_ERROR_NONE;
    otSockAddr sockAddr;

    VerifyOrExit(aInstance != nullptr && aUdpPort != nullptr);
    VerifyOrExit(!sUdpForwardSocketIsOpen);

    memset(&sockAddr, 0, sizeof(sockAddr));
    sockAddr.mPort = *aUdpPort;

    SuccessOrExit(error = otUdpOpen(aInstance, &sUdpForwardSocket, HandleUdpForwardReceive, aInstance));
    SuccessOrExit(error = otUdpBind(aInstance, &sUdpForwardSocket, &sockAddr, OT_NETIF_UNSPECIFIED));

    sUdpForwardSocketIsOpen = true;

exit:
    if (error != OT_ERROR_NONE)
    {
        otLogWarnPlat("Failed to bind TREL UDP forward socket on port %u: %s", *aUdpPort, otThreadErrorToString(error));
        IgnoreError(otUdpClose(aInstance, &sUdpForwardSocket));
        sUdpForwardSocketIsOpen = false;
    }
}

extern "C" void otPlatTrelDisable(otInstance *aInstance)
{
    if (sUdpForwardSocketIsOpen)
    {
        IgnoreError(otUdpClose(aInstance, &sUdpForwardSocket));
        sUdpForwardSocketIsOpen = false;
    }
}

extern "C" void otPlatTrelNotifyPeerSocketAddressDifference(otInstance       *aInstance,
                                                            const otSockAddr *aPeerSockAddr,
                                                            const otSockAddr *aRxSockAddr)
{
    OT_UNUSED_VARIABLE(aInstance);
    OT_UNUSED_VARIABLE(aPeerSockAddr);
    OT_UNUSED_VARIABLE(aRxSockAddr);
}

extern "C" const otPlatTrelCounters *otPlatTrelGetCounters(otInstance *aInstance)
{
    OT_UNUSED_VARIABLE(aInstance);
    return &sCounters;
}

extern "C" void otPlatTrelResetCounters(otInstance *aInstance)
{
    OT_UNUSED_VARIABLE(aInstance);
    memset(&sCounters, 0, sizeof(sCounters));
}

#endif // OPENTHREAD_CONFIG_RADIO_LINK_TREL_ENABLE && OPENTHREAD_CONFIG_UDP_FORWARD_ENABLE
