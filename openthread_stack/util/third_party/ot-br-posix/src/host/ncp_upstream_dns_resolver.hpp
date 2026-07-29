/*
 *  Copyright (c) 2026, The OpenThread Authors.
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
 *   Standalone infra DNS upstream resolver for NCP border router host.
 */

#ifndef OTBR_HOST_NCP_UPSTREAM_DNS_RESOLVER_HPP_
#define OTBR_HOST_NCP_UPSTREAM_DNS_RESOLVER_HPP_

#include <openthread-br/config.h>

#include <chrono>
#include <cstdint>
#include <functional>

#include <sys/socket.h>

#include <openthread/ip6.h>

#include "common/mainloop.hpp"

namespace otbr {

/**
 * Forwards DNS wire payloads to upstream nameservers for NCP Spinel bridging.
 *
 * Does not depend on a host `otInstance` or `otPlatDns*` platform hooks.
 */
class NcpUpstreamDnsResolver : public MainloopProcessor
{
public:
    static constexpr uint16_t kMaxDnsMessageSize       = 512;
    static constexpr uint8_t  kMaxConcurrentQueries    = 32;
    static constexpr uint8_t  kMaxUpstreamServerCount  = 3;
    static constexpr uint8_t  kMaxRecursiveServerCount = 3;

    using ResponseCallback     = std::function<void(uint8_t aTxnIndex, const uint8_t *aData, uint16_t aLength)>;
    using AvailabilityCallback = std::function<void(bool aAvailable)>;

    NcpUpstreamDnsResolver(void);

    /**
     * Initializes the resolver.
     *
     * @param[in] aInfraIfName  Infrastructure interface name for UDP bind (may be nullptr).
     */
    void Init(const char *aInfraIfName);

    /**
     * Sets the callback invoked when a DNS response is received.
     *
     * @param[in] aCallback  The response callback.
     */
    void SetResponseCallback(ResponseCallback aCallback);

    /**
     * Sets the callback invoked when upstream resolver availability changes.
     *
     * @param[in] aCallback  The availability callback.
     */
    void SetAvailabilityChangedCallback(AvailabilityCallback aCallback);

    /**
     * Indicates whether at least one upstream nameserver is configured.
     */
    bool IsAvailable(void) const;

    /**
     * Reloads upstream nameservers and notifies listeners if availability changed.
     */
    void RefreshDnsServers(void);

    /**
     * Sets whether to load nameservers from `/etc/resolv.conf`.
     *
     * @param[in] aEnabled  TRUE to enable loading from resolv.conf.
     */
    void SetResolvConfEnabled(bool aEnabled);

    /**
     * Sets explicit upstream DNS servers.
     *
     * @param[in] aUpstreamDnsServers  IPv6 or IPv4-mapped IPv6 server addresses.
     * @param[in] aNumServers          Number of servers.
     */
    void SetUpstreamDnsServers(const otIp6Address *aUpstreamDnsServers, uint32_t aNumServers);

    /**
     * Sets recursive DNS servers learned from NCP Border Routing (RDNSS).
     *
     * When non-empty, queries are forwarded to these servers instead of `/etc/resolv.conf`.
     *
     * @param[in] aRecursiveDnsServers  IPv6 recursive DNS server addresses.
     * @param[in] aNumServers           Number of servers.
     */
    void SetRecursiveDnsServers(const otIp6Address *aRecursiveDnsServers, uint32_t aNumServers);

    /**
     * Forwards a DNS query to upstream nameservers.
     *
     * @param[in] aTxnIndex  Opaque transaction index from the NCP.
     * @param[in] aQuery     DNS wire query payload.
     * @param[in] aLength    DNS wire query length.
     */
    void Query(uint8_t aTxnIndex, const uint8_t *aQuery, uint16_t aLength);

    /**
     * Cancels a pending query.
     *
     * @param[in] aTxnIndex  Opaque transaction index from the NCP.
     */
    void Cancel(uint8_t aTxnIndex);

    void Update(MainloopContext &aMainloop) override;
    void Process(const MainloopContext &aMainloop) override;

private:
    struct Transaction
    {
        bool    mInUse;
        uint8_t mTxnIndex;
        int     mUdpFd4;
        int     mUdpFd6;
    };

    int          CreateUdpSocket(sa_family_t aFamily);
    void         TryRefreshDnsServerList(void);
    void         LoadDnsServerListFromConf(void);
    void         NotifyAvailabilityChanged(void);
    bool         SendQueryToServer(Transaction        *aTxn,
                                   const otIp6Address &aServerAddress,
                                   const uint8_t      *aPacket,
                                   uint16_t            aLength);
    void         ForwardResponse(Transaction *aTxn, int aFd);
    void         CloseTransaction(Transaction *aTxn);
    void         ReportQueryFailure(uint8_t aTxnIndex);
    Transaction *AllocateTransaction(uint8_t aTxnIndex);
    Transaction *GetTransaction(uint8_t aTxnIndex);

    const char                           *mInfraIfName;
    bool                                  mIsResolvConfEnabled;
    bool                                  mIsAvailable;
    uint32_t                              mRecursiveDnsServerCount;
    otIp6Address                          mRecursiveDnsServerList[kMaxRecursiveServerCount];
    uint32_t                              mUpstreamDnsServerCount;
    otIp6Address                          mUpstreamDnsServerList[kMaxUpstreamServerCount];
    std::chrono::steady_clock::time_point mUpstreamDnsServerListFreshness;
    Transaction                           mTransactions[kMaxConcurrentQueries];
    ResponseCallback                      mResponseCallback;
    AvailabilityCallback                  mAvailabilityChangedCallback;
};

} // namespace otbr

#endif // OTBR_HOST_NCP_UPSTREAM_DNS_RESOLVER_HPP_
