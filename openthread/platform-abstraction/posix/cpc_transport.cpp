/*******************************************************************************
 * @file
 * @brief Standalone CPC transport implementation.
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

#include "cpc_transport.hpp"

#include <cerrno>
#include <cstdarg>
#include <cstdio>
#include <cstring>
#include <unistd.h>

/* Full library teardown; implemented in libcpc but omitted from some sl_cpc.h revisions. */
extern "C" int cpc_deinit(cpc_handle_t *handle);

namespace {
constexpr unsigned kUsPerS = 1000000;
} // namespace

std::atomic<CpcTransport *> CpcTransport::sSessionTransport{nullptr};

void CpcTransport::HandleSecondaryReset(void)
{
    CpcTransport *transport = sSessionTransport.load(std::memory_order_acquire);

    if (transport != nullptr)
    {
        transport->RequestReconnect();
    }
}

static uint16_t ReadUint16Be(const uint8_t *aPtr)
{
    return (static_cast<uint16_t>(aPtr[0]) << 8) | aPtr[1];
}

void CpcTransport::Log(CpcTransportLogLevel aLevel, const char *aFormat, ...)
{
    if (mLogHandler == nullptr)
    {
        return;
    }

    char    buf[384];
    va_list ap;

    va_start(ap, aFormat);
    (void)vsnprintf(buf, sizeof(buf), aFormat, ap);
    va_end(ap);
    buf[sizeof(buf) - 1] = '\0';

    mLogHandler(aLevel, buf, mLogContext);
}

CpcTransport::CpcTransport()
    : mReceiveCallback(nullptr)
    , mReceiveContext(nullptr)
    , mResetCallback(nullptr)
    , mResetContext(nullptr)
    , mReconnectFailedCallback(nullptr)
    , mReconnectFailedContext(nullptr)
    , mLogHandler(nullptr)
    , mLogContext(nullptr)
    , mSockFd(kInvalidSockFd)
    , mEndpointId(0)
    , mRxReassemblyLen(0)
    , mHandle{}
    , mEndpoint{}
{
    mInstanceName[0] = '\0';
}

CpcTransport::~CpcTransport()
{
    Deinit();
}

int CpcTransport::Init(const char *aInstanceName, uint8_t aEndpointId, bool aEnableCpcTrace)
{
    int retVal = 0;
    int fd;

    if (IsEndpointOpen())
    {
        retVal = -EALREADY;
        goto exit;
    }

    if (sSessionTransport.load(std::memory_order_acquire) != nullptr)
    {
        retVal = -EBUSY;
        goto exit;
    }

    strncpy(mInstanceName, aInstanceName ? aInstanceName : "cpcd_0", sizeof(mInstanceName) - 1);
    mInstanceName[sizeof(mInstanceName) - 1] = '\0';
    mEndpointId                              = aEndpointId;

    retVal = cpc_init(&mHandle, mInstanceName, aEnableCpcTrace, HandleSecondaryReset);
    if (retVal != 0)
    {
        goto exit;
    }

    mCpcLibInitialized = true;
    sSessionTransport.store(this, std::memory_order_release);

    fd = cpc_open_endpoint(mHandle, &mEndpoint, mEndpointId, 1);
    if (fd < 0)
    {
        retVal = fd;
        goto cleanup_libcpc;
    }

    mSockFd = fd;
    retVal  = 0;
    goto exit;

cleanup_libcpc:
    mSockFd = kInvalidSockFd;
    sSessionTransport.store(nullptr, std::memory_order_release);
    (void)cpc_deinit(&mHandle);
    mCpcLibInitialized = false;
    mHandle            = cpc_handle_t{};
    mEndpoint          = cpc_endpoint_t{};

exit:
    return retVal;
}

void CpcTransport::Deinit(void)
{
    mRxReassemblyLen = 0;
    mSendDisconnectPending.store(0, std::memory_order_relaxed);
    mReconnectPending.store(0, std::memory_order_relaxed);

    {
        CpcTransport *expected = this;
        (void)sSessionTransport.compare_exchange_strong(expected,
                                                        nullptr,
                                                        std::memory_order_acq_rel,
                                                        std::memory_order_acquire);
    }

    if (IsEndpointOpen())
    {
        (void)cpc_close_endpoint(&mEndpoint);
        mSockFd = kInvalidSockFd;
    }

    if (mCpcLibInitialized)
    {
        (void)cpc_deinit(&mHandle);
        mCpcLibInitialized = false;
    }

    mHandle   = cpc_handle_t{};
    mEndpoint = cpc_endpoint_t{};

    mReceiveCallback         = nullptr;
    mReceiveContext          = nullptr;
    mResetCallback           = nullptr;
    mResetContext            = nullptr;
    mReconnectFailedCallback = nullptr;
    mReconnectFailedContext  = nullptr;
    mLogHandler              = nullptr;
    mLogContext              = nullptr;
}

ssize_t CpcTransport::Send(const uint8_t *aFrame, uint16_t aLength)
{
    ssize_t send_result = 0;

    if (IsEndpointOpen())
    {
        send_result = cpc_write_endpoint(mEndpoint, aFrame, aLength, CPC_ENDPOINT_WRITE_FLAG_NON_BLOCKING);
    }
    else
    {
        send_result = -ENOTCONN;
    }

    if (send_result < 0)
    {
        // If the write failed for a fatal reason, we queue a reconnect.
        // If the errors are non-fatal instead, the caller is expected to retry:
        // EAGAIN, EWOULDBLOCK, and EINVAL usually mean the endpoint is busy or out of buffers, so retry once there is
        // room. EINTR just means the syscall was interrupted, so the caller can retry the write right away. Otherwise,
        // the error is fatal and we queue a reconnect.
        const bool needsReconnection = (send_result != -EAGAIN) && (send_result != -EWOULDBLOCK)
                                       && (send_result != -EINVAL) && (send_result != -EINTR);

        if (needsReconnection)
        {
            mSendDisconnectPending.store(1, std::memory_order_relaxed);
            RequestReconnect();
        }
    }

    return send_result;
}

bool CpcTransport::CheckAndClearDisconnectStatus(void)
{
    bool pending = (mSendDisconnectPending.load(std::memory_order_relaxed) != 0);

    mSendDisconnectPending.store(0, std::memory_order_relaxed);

    return pending;
}

void CpcTransport::FlushParsedFrames(void)
{
    while (mRxReassemblyLen >= kFrameLengthFieldSize && mReceiveCallback)
    {
        uint16_t frameLen = ReadUint16Be(mRxReassemblyBuf);

        if (frameLen > kMaxFrameSize)
        {
            Log(CpcTransportLogLevel::kWarning,
                "Dropping RX reassembly buffer (invalid frame length %u, max %u, buffered %zu)",
                static_cast<unsigned>(frameLen),
                static_cast<unsigned>(kMaxFrameSize),
                mRxReassemblyLen);
            mRxReassemblyLen = 0;
            break;
        }

        size_t need = kFrameLengthFieldSize + frameLen;
        if (mRxReassemblyLen < need)
        {
            break;
        }

        mReceiveCallback(mRxReassemblyBuf + kFrameLengthFieldSize, frameLen, mReceiveContext);
        size_t remain = mRxReassemblyLen - need;
        if (remain > 0)
        {
            memmove(mRxReassemblyBuf, mRxReassemblyBuf + need, remain);
        }
        mRxReassemblyLen = remain;
    }
}

int CpcTransport::ReadNonBlocking(void)
{
    return ReadEndpoint(0);
}

int CpcTransport::ConfigureEndpointForRead(uint64_t aTimeoutUs)
{
    int           result = 0;
    int           optRet;
    bool          block;
    cpc_timeval_t timeout;

    if (aTimeoutUs > 0)
    {
        block                = true;
        timeout.seconds      = static_cast<int>(aTimeoutUs / kUsPerS);
        timeout.microseconds = static_cast<int>(aTimeoutUs % kUsPerS);
        optRet               = cpc_set_endpoint_option(mEndpoint, CPC_OPTION_BLOCKING, &block, sizeof(block));
        if (optRet != 0)
        {
            goto fail_inval;
        }
        optRet = cpc_set_endpoint_option(mEndpoint, CPC_OPTION_RX_TIMEOUT, &timeout, sizeof(timeout));
        if (optRet != 0)
        {
            goto fail_inval;
        }
    }
    else
    {
        block  = false;
        optRet = cpc_set_endpoint_option(mEndpoint, CPC_OPTION_BLOCKING, &block, sizeof(block));
        if (optRet != 0)
        {
            goto fail_inval;
        }
    }

    goto exit;

fail_inval:
    result = -EINVAL;
exit:
    return result;
}

int CpcTransport::HandleReadEndpointResult(ssize_t aBytesRead, const uint8_t *aBuffer)
{
    int result = 0;

    if (aBytesRead > 0)
    {
        size_t add = static_cast<size_t>(aBytesRead);
        if (mRxReassemblyLen + add > kRxReassemblyCapacity)
        {
            if (add > kRxReassemblyCapacity)
            {
                Log(CpcTransportLogLevel::kCrit,
                    "Single read length %zu exceeds reassembly capacity %zu; dropping chunk",
                    add,
                    kRxReassemblyCapacity);
            }
            else
            {
                Log(CpcTransportLogLevel::kWarning,
                    "RX reassembly overflow (have %zu, adding %zu, cap %zu); buffer reset",
                    mRxReassemblyLen,
                    add,
                    kRxReassemblyCapacity);
            }
            mRxReassemblyLen = 0;

            // Drop chunk and reconnect after clearing a partial length-prefix frame to avoid corruption.
            result = Reconnect();
            goto exit;
        }
        memcpy(mRxReassemblyBuf + mRxReassemblyLen, aBuffer, add);
        mRxReassemblyLen += add;
        FlushParsedFrames();
    }
    else if (aBytesRead < 0)
    {
        if (aBytesRead == -ECONNRESET)
        {
            RequestReconnect();
        }
        else if ((aBytesRead != -EAGAIN) && (aBytesRead != -EINTR))
        {
            result = static_cast<int>(aBytesRead);
        }
    }

exit:
    return result;
}

int CpcTransport::ReadEndpoint(uint64_t aTimeoutUs)
{
    int     result;
    uint8_t buffer[kMaxFrameSize];
    ssize_t bytesRead;

    result = CheckAndReconnect();
    if (result != 0)
    {
        goto exit;
    }

    if (!IsEndpointOpen())
    {
        result = 0;
        goto exit;
    }

    result = ConfigureEndpointForRead(aTimeoutUs);
    if (result != 0)
    {
        goto exit;
    }

    bytesRead = cpc_read_endpoint(mEndpoint, buffer, sizeof(buffer), CPC_ENDPOINT_READ_FLAG_NONE);
    result    = HandleReadEndpointResult(bytesRead, buffer);

exit:
    return result;
}

int CpcTransport::Process(void)
{
    return ReadNonBlocking();
}

int CpcTransport::CheckAndReconnect(void)
{
    int      ret = 0;
    int      result;
    int      fd;
    unsigned attempts;

    if (mReconnectPending.load(std::memory_order_relaxed) == 0)
    {
        goto exit;
    }

    mReconnectPending.store(0, std::memory_order_relaxed);
    mRxReassemblyLen = 0;

    if (mResetCallback)
    {
        mResetCallback(mResetContext);
    }

    if (IsEndpointOpen())
    {
        result = cpc_close_endpoint(&mEndpoint);
        if (result != 0)
        {
            mSockFd = kInvalidSockFd;
            ret     = (result < 0) ? result : -EIO;
            goto exit;
        }
        mSockFd = kInvalidSockFd;
    }

    attempts = 0;
    do
    {
        usleep(kMaxSleepDuration);
        result = cpc_restart(&mHandle);
        attempts++;
    } while (result != 0 && attempts < kMaxRestartAttempts);

    if (result != 0)
    {
        ret = (result < 0) ? result : -EIO;
        goto exit;
    }

    attempts = 0;
    do
    {
        usleep(kMaxSleepDuration);
        fd = cpc_open_endpoint(mHandle, &mEndpoint, mEndpointId, 1);
        attempts++;
    } while (fd < 0 && attempts < kMaxRestartAttempts);

    if (fd < 0)
    {
        mSockFd = kInvalidSockFd;
        ret     = fd;
        goto exit;
    }

    mSockFd = fd;

exit:
    if (ret < 0 && mReconnectFailedCallback != nullptr)
    {
        mReconnectFailedCallback(ret, mReconnectFailedContext);
    }
    return ret;
}

int CpcTransport::Reconnect(void)
{
    RequestReconnect();
    return CheckAndReconnect();
}
