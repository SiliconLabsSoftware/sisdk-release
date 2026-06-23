/*******************************************************************************
 * @file
 * @brief Standalone CPC transport for Spinel frames.
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

#ifndef CPC_TRANSPORT_HPP
#define CPC_TRANSPORT_HPP

#include <atomic>
#include <cstdint>
#include <cstdlib>

#if !defined(__linux__)
#error "CpcTransport requires Linux (libcpc is Linux-only)"
#endif

#include "cpc_transport_config.hpp"
#include "sl_cpc.h"

/**
 * Callback invoked when a Spinel frame is received from CPC.
 */
using ReceiveCallback = void (*)(const uint8_t *aFrame, uint16_t aLength, void *aContext);

/**
 * Callback invoked when CPC secondary resets (connection lost).
 */
using ResetCallback = void (*)(void *aContext);

/**
 * Optional callback when `CheckAndReconnect()` fails after retries (negative errno-style @p aErr).
 * Typically terminates the process; must not return if recovery is impossible.
 */
using ReconnectFailedCallback = void (*)(int aErr, void *aContext);

/**
 * Severity for `CpcTransportLogHandler`. Intended to map to the host logger (e.g. OpenThread `otLog*Plat`).
 */
enum class CpcTransportLogLevel : uint8_t
{
    kCrit    = 0,
    kWarning = 1,
};

/**
 * Optional diagnostic logging for `CpcTransport`. @p aMessage is NUL-terminated and truncated internally;
 * keep content single-line and free of secrets. May be invoked from the thread running `Process`/`Send` or
 * from libcpc’s reset path — handlers must be async-signal-safe only if they claim to be.
 */
using CpcTransportLogHandler = void (*)(CpcTransportLogLevel aLevel, const char *aMessage, void *aContext);

/**
 * Standalone CPC transport for Spinel frames.
 */
class CpcTransport
{
public:
    static constexpr uint16_t kMaxFrameSize = SL_CPC_READ_MINIMUM_SIZE;
    /** Big-endian uint16 length prefix (bytes) before Spinel payload in the CPC byte stream. */
    static constexpr size_t kFrameLengthFieldSize = 2;
    /** Max bytes in `mRxReassemblyBuf` (length-prefix reassembly); avoid std::vector (pulls in <new>, conflicts with OT
     * new.hpp). */
    static constexpr size_t kRxReassemblyCapacity = static_cast<size_t>(kMaxFrameSize) * 2 + 16;
    /** Stored libcpc instance name buffer size (NUL-terminated); see `cpc_transport_config.hpp`. */
    static constexpr size_t kInstanceNameMaxLen = static_cast<size_t>(CPC_TRANSPORT_CONFIG_INSTANCE_NAME_MAX_LEN);

    CpcTransport();
    ~CpcTransport();

    /**
     * @retval 0                       Success.
     * @retval -EBUSY                  Another `CpcTransport` already holds the process libcpc session.
     * @retval -EALREADY               This transport already has an open endpoint.
     * @retval other non-zero            Negative errno from libcpc (`cpc_init` or `cpc_open_endpoint` per `sl_cpc.h`).
     */
    int Init(const char *aInstanceName, uint8_t aEndpointId, bool aEnableCpcTrace);
    /**
     * Close the endpoint, end the libcpc session (`cpc_deinit` when initialized), and clear session
     * routing for libcpc’s reset callback. Clears all registered callbacks last. A later `Init()` in the same process
     * may call `cpc_init` again.
     */
    void Deinit(void);
    /**
     * Non-blocking `cpc_write_endpoint`. Per `sl_cpc.h`, a successful write returns the full requested length
     * (partial writes are not possible; `0` is not a valid success return).
     *
     * Pending reconnects are applied from `Process()` / `ReadEndpoint()`.
     *
     * On errors other than `-EAGAIN`, `-EWOULDBLOCK`, `-EINVAL`, and `-EINTR`, queues `RequestReconnect()` and
     * latches disconnect status until `CheckAndClearDisconnectStatus()` clears it.
     */
    ssize_t Send(const uint8_t *aFrame, uint16_t aLength);

    /**
     * @retval true  The last `Send()` failed with a non-transient error and `RequestReconnect()` was queued (write-path
     *               disconnect). Clears the one-shot latch.
     * @retval false Otherwise.
     */
    bool CheckAndClearDisconnectStatus(void);

    void SetReceiveCallback(ReceiveCallback aCallback, void *aContext)
    {
        mReceiveCallback = aCallback;
        mReceiveContext  = aContext;
    }

    void SetResetCallback(ResetCallback aCallback, void *aContext)
    {
        mResetCallback = aCallback;
        mResetContext  = aContext;
    }

    void SetReconnectFailedCallback(ReconnectFailedCallback aCallback, void *aContext)
    {
        mReconnectFailedCallback = aCallback;
        mReconnectFailedContext  = aContext;
    }

    void SetLogHandler(CpcTransportLogHandler aHandler, void *aContext)
    {
        mLogHandler = aHandler;
        mLogContext = aContext;
    }

    int GetFd(void) const { return mSockFd; }
    /** `true` when `cpc_open_endpoint` succeeded and the socket is not closed (`GetFd() >= 0`). */
    bool IsEndpointOpen(void) const { return mSockFd >= 0; }
    /** @returns 0 on success, or negative errno if reconnect/read failed (CPC down); see `ReadEndpoint`. */
    int Process(void);
    /**
     * Runs a pending `cpc_restart` + endpoint reopen when `RequestReconnect()` was queued (read/write errors,
     * libcpc reset, or explicit `RequestReconnect()` from the application).
     * On failure, invokes `SetReconnectFailedCallback` if set, then returns negative errno.
     */
    int CheckAndReconnect(void);
    /**
     * Queue reconnect (`RequestReconnect`) and run it immediately (`CheckAndReconnect`).
     * Intended for explicit handoff (e.g. `CpcInterfaceImpl::Init` when CPC is already initialized).
     *
     * @returns Same as `CheckAndReconnect()` (0 on success, negative errno on failure).
     */
    int Reconnect(void);
    /**
     * Queue a full CPC endpoint restart (`cpc_restart` + reopen). Safe from libcpc reset callback / async paths.
     * Use for explicit signals (e.g. vendor secondary reset, additional `Init` handoff); write/read disconnects
     * are queued inside `Send` / `HandleReadEndpointResult` / `HandleSecondaryReset` without going through the
     * Spinel interface layer.
     */
    void RequestReconnect(void) { mReconnectPending.store(1, std::memory_order_relaxed); }

    /**
     * Libcpc read path for OpenThread POSIX `CpcInterfaceImpl` (`Read` / `WaitForFrame`). Behavior
     * matches the pre-transport `cpc_interface` implementation (reference): same option flags and
     * `cpc_read_endpoint` usage.
     *
     * - @p aTimeoutUs > 0: blocking endpoint + `CPC_OPTION_RX_TIMEOUT`, `cpc_read_endpoint(..., FLAG_NONE)`.
     * - @p aTimeoutUs == 0: non-blocking endpoint, same read flags as the reference.
     *
     * Like legacy `cpc_interface::Read`, a timed read may leave `CPC_OPTION_BLOCKING` true; the next
     * `ReadEndpoint(0)` (e.g. from `Process` via `CpcInterfaceImpl`) sets non-blocking again at the start of that read.
     * `Process()` uses `ReadNonBlocking()`, which delegates here (`aTimeoutUs == 0`).
     * `cpc-spinel-proxy` does not call `ReadEndpoint`; it uses `Process()` only.
     *
     * Runs `CheckAndReconnect()` first when a reconnect is pending (same ordering as legacy
     * `CheckAndReInitCpc` before `Read` in `Process` / `WaitForFrame`).
     *
     * @returns 0 on success (data, benign empty read, `-EAGAIN` after blocking+timeout, or `-EINTR`), or `0` after
     *          an RX reassembly overflow where `Reconnect()` recovered the CPC session (no frame delivered this call).
     *          Negative errno on fatal error (including `-EINVAL` from option setup, reconnect failure, or if
     *          libcpc returns `-1`).
     */
    int ReadEndpoint(uint64_t aTimeoutUs);

    /** Same as `ReadEndpoint(0)` — non-blocking read with shared option setup and reassembly. */
    int ReadNonBlocking(void);

    CpcTransport(const CpcTransport &)            = delete;
    CpcTransport &operator=(const CpcTransport &) = delete;

private:
    void Log(CpcTransportLogLevel aLevel, const char *aFormat, ...);

    void FlushParsedFrames(void);

    /** @returns 0 on success, `-EINVAL` if `cpc_set_endpoint_option` fails. */
    int ConfigureEndpointForRead(uint64_t aTimeoutUs);
    /** Handle `cpc_read_endpoint` result for `ReadEndpoint` (reassembly, reconnect, fatal negative errno). */
    int HandleReadEndpointResult(ssize_t aBytesRead, const uint8_t *aBuffer);

    /** Routes libcpc `cpc_reset_callback_t` (no user context) to `RequestReconnect()`. */
    static void HandleSecondaryReset(void);

    /** Normalized value for `mSockFd` when no valid POSIX fd (see `mSockFd >= 0`); not a libcpc return code. */
    static constexpr int kInvalidSockFd = -1;

    /** Reconnect backoff; see `cpc_transport_config.hpp`. */
    static constexpr unsigned kMaxSleepDuration = static_cast<unsigned>(CPC_TRANSPORT_CONFIG_MAX_SLEEP_DURATION_US);
    /** Reconnect retry limits; see `cpc_transport_config.hpp`. */
    static constexpr unsigned kMaxRestartAttempts = static_cast<unsigned>(CPC_TRANSPORT_CONFIG_MAX_RESTART_ATTEMPTS);

    ReceiveCallback         mReceiveCallback;
    void                   *mReceiveContext;
    ResetCallback           mResetCallback;
    void                   *mResetContext;
    ReconnectFailedCallback mReconnectFailedCallback;
    void                   *mReconnectFailedContext;
    CpcTransportLogHandler  mLogHandler;
    void                   *mLogContext;

    int     mSockFd;
    uint8_t mEndpointId;

    char mInstanceName[kInstanceNameMaxLen];
    /** Set after successful `cpc_init`; cleared after `cpc_deinit`. Guards teardown when `Init` never ran or already
     * cleaned up. */
    bool mCpcLibInitialized = false;
    /**
     * Reconnect / disconnect latches written from libcpc’s reset callback path and read from the thread driving
     * `Process` / `Send` / `CheckAndReconnect`. Use `std::atomic` so these are well-defined across threads.
     */
    std::atomic<uint8_t> mReconnectPending{0};
    std::atomic<uint8_t> mSendDisconnectPending{0};

    uint8_t mRxReassemblyBuf[kRxReassemblyCapacity];
    size_t  mRxReassemblyLen;

    cpc_handle_t   mHandle;
    cpc_endpoint_t mEndpoint;

    /** Transport that owns the process libcpc session for reset-callback routing (at most one). */
    static std::atomic<CpcTransport *> sSessionTransport;
};

#endif // CPC_TRANSPORT_HPP
