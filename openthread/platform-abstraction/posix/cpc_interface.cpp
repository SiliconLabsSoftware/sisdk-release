/*******************************************************************************
 * @file
 * @brief This file includes the implementation for the CPCd interface to radio (RCP).
 *******************************************************************************
 * # License
 * <b>Copyright 2024 Silicon Laboratories Inc. www.silabs.com</b>
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

#include "cpc_interface.hpp"

#include "cpc_transport.hpp"
#include "platform-posix.h"
#include "vendor_interface.hpp"

#include <assert.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "common/code_utils.hpp"
#include "common/debug.hpp"
#include "common/encoding.hpp"
#include "common/logging.hpp"
#include "common/new.hpp"
#include "lib/spinel/spinel.h"

#if OPENTHREAD_POSIX_CONFIG_SPINEL_VENDOR_INTERFACE_ENABLE

using ot::Spinel::SpinelInterface;

namespace ot {
namespace Posix {

namespace {
void DieIfNegativeErrno(int aRet)
{
    if (aRet >= 0)
    {
        return;
    }
    errno = (aRet == -1) ? EIO : -aRet;
    DieNow(OT_EXIT_ERROR_ERRNO);
}

void OnCpcReconnectFailed(int aErr, void *aContext)
{
    OT_UNUSED_VARIABLE(aContext);
    DieIfNegativeErrno(aErr);
}

void OnCpcTransportLog(CpcTransportLogLevel aLevel, const char *aMessage, void *aContext)
{
    OT_UNUSED_VARIABLE(aContext);

    switch (aLevel)
    {
    case CpcTransportLogLevel::kCrit:
        otLogCritPlat("%s", aMessage);
        break;
    case CpcTransportLogLevel::kWarning:
        otLogWarnPlat("%s", aMessage);
        break;
    }
}
} // namespace

// ----------------------------------------------------------------------------
// `CpcInterfaceImpl` - delegates to CpcTransport
// ----------------------------------------------------------------------------

bool CpcInterfaceImpl::sIsCpcInitialized = false;

void OnCpcFrame(const uint8_t *aFrame, uint16_t aLength, void *aContext)
{
    auto *ctx = static_cast<CpcInterfaceImpl::TransportContext *>(aContext);
    bool  ok  = true;

    for (uint16_t i = 0; ok && i < aLength; i++)
    {
        if (!ctx->frameBuffer->CanWrite(1) || (ctx->frameBuffer->WriteByte(aFrame[i]) != OT_ERROR_NONE))
        {
            ctx->frameBuffer->DiscardFrame();
            ok = false;
        }
    }

    if (ok)
    {
        ctx->callback(ctx->context);
    }
}

CpcInterfaceImpl::CpcInterfaceImpl(const Url::Url &aRadioUrl)
    : mReceiveFrameCallback(nullptr)
    , mReceiveFrameContext(nullptr)
    , mReceiveFrameBuffer(nullptr)
    , mRadioUrl(aRadioUrl)
{
    memset(&mInterfaceMetrics, 0, sizeof(mInterfaceMetrics));
    mInterfaceMetrics.mRcpInterfaceType = kSpinelInterfaceTypeVendor;
    mCpcBusSpeed                        = kCpcBusSpeed;
}

otError CpcInterfaceImpl::Init(ReceiveFrameCallback aCallback, void *aCallbackContext, RxFrameBuffer &aFrameBuffer)
{
    otError     error = OT_ERROR_NONE;
    const char *value;

    VerifyOrExit(!mTransport.IsEndpointOpen(), error = OT_ERROR_ALREADY);

    mTransport.SetLogHandler(OnCpcTransportLog, nullptr);

    mTransportContext.callback    = aCallback;
    mTransportContext.context     = aCallbackContext;
    mTransportContext.frameBuffer = &aFrameBuffer;

    mTransport.SetReconnectFailedCallback(OnCpcReconnectFailed, nullptr);

    if (!sIsCpcInitialized)
    {
        int ret = mTransport.Init(mRadioUrl.GetPath(), mId, false);
        if (ret != 0)
        {
            otLogCritPlat("CPC init failed Error: %d. Ensure radio-url argument has the form "
                          "'spinel+cpc://cpcd_0?iid=<1..3>'",
                          ret);
            DieNow(OT_EXIT_FAILURE);
        }
    }
    else
    {
        DieIfNegativeErrno(mTransport.Reconnect());
    }
    mTransport.SetReceiveCallback(OnCpcFrame, &mTransportContext);

    if ((value = mRadioUrl.GetValue("cpc-bus-speed")))
    {
        mCpcBusSpeed = static_cast<uint32_t>(atoi(value));
    }

    sIsCpcInitialized     = true;
    mReceiveFrameCallback = aCallback;
    mReceiveFrameContext  = aCallbackContext;
    mReceiveFrameBuffer   = &aFrameBuffer;

exit:
    return error;
}

CpcInterfaceImpl::~CpcInterfaceImpl(void)
{
    Deinit();
}

void CpcInterfaceImpl::Deinit(void)
{
    mTransport.Deinit();
    mReceiveFrameCallback = nullptr;
    mReceiveFrameContext  = nullptr;
    mReceiveFrameBuffer   = nullptr;
    sIsCpcInitialized     = false;
}

void CpcInterfaceImpl::Read(uint64_t aTimeoutUs)
{
    DieIfNegativeErrno(mTransport.ReadEndpoint(aTimeoutUs));
}

otError CpcInterfaceImpl::SendFrame(const uint8_t *aFrame, uint16_t aLength)
{
    otError error = OT_ERROR_NONE;

    if (IsSpinelResetCommand(aFrame, aLength))
    {
        SendResetResponse();
        ExitNow();
    }

    ssize_t n;

    do
    {
        n = mTransport.Send(aFrame, aLength);
    } while (n == -EINTR);

    // CPC endpoint writes do not send partial frames. Only completed writes or errors are valid.
    if (n != static_cast<ssize_t>(aLength))
    {
        VerifyOrDie(n < 0, OT_EXIT_FAILURE);
        VerifyOrExit(((n != -EAGAIN) && (n != -EWOULDBLOCK) && (n != -EINVAL)), error = OT_ERROR_NO_BUFS);
        VerifyOrExit(!mTransport.CheckAndClearDisconnectStatus(), error = OT_ERROR_FAILED);
    }

exit:
    return error;
}

otError CpcInterfaceImpl::WaitForFrame(uint64_t aTimeoutUs)
{
    Read(aTimeoutUs);
    return OT_ERROR_NONE;
}

void CpcInterfaceImpl::UpdateFdSet(void *aMainloopContext)
{
    otSysMainloopContext *context = reinterpret_cast<otSysMainloopContext *>(aMainloopContext);
    OT_ASSERT(context != nullptr);

    if (mTransport.IsEndpointOpen())
    {
        int fd = mTransport.GetFd();
        FD_SET(fd, &context->mReadFdSet);
        if (context->mMaxFd < fd)
        {
            context->mMaxFd = fd;
        }
    }
}

void CpcInterfaceImpl::Process(const void *aMainloopContext)
{
    OT_UNUSED_VARIABLE(aMainloopContext);
    DieIfNegativeErrno(mTransport.Process());
}

void CpcInterfaceImpl::SendResetResponse(void)
{
    for (int i = 0; i < kResetCMDSize; ++i)
    {
        if (mReceiveFrameBuffer->CanWrite(sizeof(uint8_t)))
        {
            IgnoreError(mReceiveFrameBuffer->WriteByte(mResetResponse[i]));
        }
    }
    mReceiveFrameCallback(mReceiveFrameContext);
}

// ----------------------------------------------------------------------------
// `VendorInterface` API
// ----------------------------------------------------------------------------

static OT_DEFINE_ALIGNED_VAR(sCpcInterfaceImplRaw, sizeof(CpcInterfaceImpl), uint64_t);

VendorInterface::VendorInterface(const Url::Url &aRadioUrl)
{
    new (&sCpcInterfaceImplRaw) CpcInterfaceImpl(aRadioUrl);
}

otError VendorInterface::Init(ReceiveFrameCallback aCallback, void *aCallbackContext, RxFrameBuffer &aFrameBuffer)
{
    return reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->Init(aCallback, aCallbackContext, aFrameBuffer);
}

uint32_t VendorInterface::GetBusSpeed(void) const
{
    return reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->GetBusSpeed();
}

VendorInterface::~VendorInterface(void)
{
    reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->Deinit();
}

void VendorInterface::Deinit(void)
{
    reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->Deinit();
}

otError VendorInterface::SendFrame(const uint8_t *aFrame, uint16_t aLength)
{
    return reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->SendFrame(aFrame, aLength);
}

otError VendorInterface::WaitForFrame(uint64_t aTimeoutUs)
{
    return reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->WaitForFrame(aTimeoutUs);
}

void VendorInterface::UpdateFdSet(void *aMainloopContext)
{
    reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->UpdateFdSet(aMainloopContext);
}

void VendorInterface::Process(const void *aMainloopContext)
{
    reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->Process(aMainloopContext);
}

otError VendorInterface::HardwareReset(void)
{
    return reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->HardwareReset();
}

const otRcpInterfaceMetrics *VendorInterface::GetRcpInterfaceMetrics(void) const
{
    return reinterpret_cast<CpcInterfaceImpl *>(&sCpcInterfaceImplRaw)->GetRcpInterfaceMetrics();
}

} // namespace Posix
} // namespace ot
#endif // OPENTHREAD_POSIX_CONFIG_SPINEL_VENDOR_INTERFACE_ENABLE
