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

#define OTBR_LOG_TAG "NcpDnsUpstream"

#include "host/ncp_upstream_dns_resolver.hpp"

#include <algorithm>
#include <arpa/inet.h>
#include <errno.h>
#include <fstream>
#include <net/if.h>
#include <string>
#include <sys/socket.h>
#include <unistd.h>

#include <openthread/nat64.h>

#include "common/code_utils.hpp"
#include "common/logging.hpp"

namespace otbr {
namespace {

constexpr char                 kResolvConfFullPath[] = "/etc/resolv.conf";
constexpr char                 kNameserverItem[]     = "nameserver";
constexpr std::chrono::minutes kDnsServerListCacheTimeout{10};
constexpr std::chrono::minutes kDnsServerListNullCacheTimeout{1};

bool TryAppendNameserver(const char   *aAddressString,
                         otIp6Address *aServerList,
                         uint32_t     &aServerCount,
                         uint32_t      aMaxServerCount)
{
    otIp4Address ip4Address;
    otIp6Address ip6Address;
    bool         appended = false;

    VerifyOrExit(aAddressString != nullptr && aAddressString[0] != '\0');
    VerifyOrExit(aServerCount < aMaxServerCount);

    if (inet_pton(AF_INET, aAddressString, &ip4Address) == 1)
    {
        otIp4ToIp4MappedIp6Address(&ip4Address, &ip6Address);
    }
    else if (inet_pton(AF_INET6, aAddressString, &ip6Address) != 1)
    {
        ExitNow();
    }

    aServerList[aServerCount] = ip6Address;
    aServerCount++;
    appended = true;

exit:
    return appended;
}

void AppendNameserversFromLine(const std::string &aLine,
                               otIp6Address      *aServerList,
                               uint32_t          &aServerCount,
                               uint32_t           aMaxServerCount)
{
    size_t start = aLine.find_first_not_of(" \t");

    VerifyOrExit(start != std::string::npos);
    VerifyOrExit(aLine[start] != '#');
    VerifyOrExit(aLine.compare(start, sizeof(kNameserverItem) - 1, kNameserverItem) == 0);

    start += sizeof(kNameserverItem) - 1;
    start = aLine.find_first_not_of(" \t", start);
    VerifyOrExit(start != std::string::npos);
    TryAppendNameserver(aLine.c_str() + start, aServerList, aServerCount, aMaxServerCount);

exit:
    return;
}

bool IsIp6AddressLinkLocal(const otIp6Address &aAddress)
{
    return (aAddress.mFields.m8[0] == 0xfe) && ((aAddress.mFields.m8[1] & 0xc0) == 0x80);
}

} // namespace

NcpUpstreamDnsResolver::NcpUpstreamDnsResolver(void)
    : mInfraIfName(nullptr)
    , mIsResolvConfEnabled(true)
    , mIsAvailable(false)
    , mRecursiveDnsServerCount(0)
    , mUpstreamDnsServerCount(0)
    , mUpstreamDnsServerListFreshness(std::chrono::steady_clock::now())
{
    for (Transaction &txn : mTransactions)
    {
        txn.mInUse    = false;
        txn.mTxnIndex = 0;
        txn.mUdpFd4   = -1;
        txn.mUdpFd6   = -1;
    }
}

void NcpUpstreamDnsResolver::Init(const char *aInfraIfName)
{
    mInfraIfName = aInfraIfName;
    LoadDnsServerListFromConf();
    NotifyAvailabilityChanged();
}

void NcpUpstreamDnsResolver::SetResponseCallback(ResponseCallback aCallback)
{
    mResponseCallback = std::move(aCallback);
}

void NcpUpstreamDnsResolver::SetAvailabilityChangedCallback(AvailabilityCallback aCallback)
{
    mAvailabilityChangedCallback = std::move(aCallback);
}

bool NcpUpstreamDnsResolver::IsAvailable(void) const
{
    return mIsAvailable;
}

void NcpUpstreamDnsResolver::RefreshDnsServers(void)
{
    LoadDnsServerListFromConf();
    NotifyAvailabilityChanged();
}

void NcpUpstreamDnsResolver::SetResolvConfEnabled(bool aEnabled)
{
    mIsResolvConfEnabled = aEnabled;
    TryRefreshDnsServerList();
    NotifyAvailabilityChanged();
}

void NcpUpstreamDnsResolver::SetUpstreamDnsServers(const otIp6Address *aUpstreamDnsServers, uint32_t aNumServers)
{
    mUpstreamDnsServerCount = std::min(aNumServers, static_cast<uint32_t>(kMaxUpstreamServerCount));
    memcpy(mUpstreamDnsServerList, aUpstreamDnsServers, mUpstreamDnsServerCount * sizeof(otIp6Address));
    mUpstreamDnsServerListFreshness = std::chrono::steady_clock::now();
    NotifyAvailabilityChanged();
}

void NcpUpstreamDnsResolver::SetRecursiveDnsServers(const otIp6Address *aRecursiveDnsServers, uint32_t aNumServers)
{
    mRecursiveDnsServerCount = std::min(aNumServers, static_cast<uint32_t>(kMaxRecursiveServerCount));
    memcpy(mRecursiveDnsServerList, aRecursiveDnsServers, mRecursiveDnsServerCount * sizeof(otIp6Address));
    NotifyAvailabilityChanged();
}

void NcpUpstreamDnsResolver::TryRefreshDnsServerList(void)
{
    const auto now = std::chrono::steady_clock::now();

    if (now > mUpstreamDnsServerListFreshness + kDnsServerListCacheTimeout ||
        (mUpstreamDnsServerCount == 0 && now > mUpstreamDnsServerListFreshness + kDnsServerListNullCacheTimeout))
    {
        LoadDnsServerListFromConf();
        NotifyAvailabilityChanged();
    }
}

void NcpUpstreamDnsResolver::LoadDnsServerListFromConf(void)
{
    std::string   line;
    std::ifstream fp;

    VerifyOrExit(mIsResolvConfEnabled);

    mUpstreamDnsServerCount = 0;

    fp.open(kResolvConfFullPath);

    while (fp.good() && std::getline(fp, line) && mUpstreamDnsServerCount < kMaxUpstreamServerCount)
    {
        AppendNameserversFromLine(line, mUpstreamDnsServerList, mUpstreamDnsServerCount, kMaxUpstreamServerCount);
    }

    if (mUpstreamDnsServerCount == 0)
    {
        otbrLogWarning("No upstream DNS servers found in %s", kResolvConfFullPath);
    }

    mUpstreamDnsServerListFreshness = std::chrono::steady_clock::now();

exit:
    return;
}

void NcpUpstreamDnsResolver::NotifyAvailabilityChanged(void)
{
    bool available = mRecursiveDnsServerCount > 0 || mUpstreamDnsServerCount > 0;

    if (available != mIsAvailable)
    {
        mIsAvailable = available;

        if (mAvailabilityChangedCallback)
        {
            mAvailabilityChangedCallback(mIsAvailable);
        }
    }
}

int NcpUpstreamDnsResolver::CreateUdpSocket(sa_family_t aFamily)
{
    int fd = -1;

    VerifyOrExit(mInfraIfName != nullptr && mInfraIfName[0] != '\0', otbrLogDebug("No infra interface configured"));
    fd = socket(aFamily, SOCK_DGRAM, IPPROTO_UDP);
    VerifyOrExit(fd >= 0, otbrLogDebug("Failed to create UDP socket: %s", strerror(errno)));
#if OTBR_ENABLE_NCP_DNS_UPSTREAM_BIND_TO_INFRA
    if (setsockopt(fd, SOL_SOCKET, SO_BINDTODEVICE, mInfraIfName, strlen(mInfraIfName)) < 0)
    {
        otbrLogDebug("Failed to bind UDP socket to %s: %s", mInfraIfName, strerror(errno));
        close(fd);
        fd = -1;
        ExitNow();
    }
#endif

exit:
    return fd;
}

bool NcpUpstreamDnsResolver::SendQueryToServer(Transaction        *aTxn,
                                               const otIp6Address &aServerAddress,
                                               const uint8_t      *aPacket,
                                               uint16_t            aLength)
{
    otIp4Address ip4Addr;
    sockaddr_in  serverAddr4  = {};
    sockaddr_in6 serverAddr6  = {};
    bool         sent         = false;
    unsigned int infraIfIndex = 0;
    char         addrStr[INET6_ADDRSTRLEN];

    if (mInfraIfName != nullptr)
    {
        infraIfIndex = if_nametoindex(mInfraIfName);
    }

    if (otIp4FromIp4MappedIp6Address(&aServerAddress, &ip4Addr) == OT_ERROR_NONE)
    {
        memcpy(&serverAddr4.sin_addr.s_addr, &ip4Addr, sizeof(otIp4Address));
        serverAddr4.sin_family = AF_INET;
        serverAddr4.sin_port   = htons(53);
        sent = (sendto(aTxn->mUdpFd4, aPacket, aLength, MSG_DONTWAIT, reinterpret_cast<sockaddr *>(&serverAddr4),
                       sizeof(serverAddr4)) > 0);
        if (!sent)
        {
            otbrLogWarning("sendto IPv4 DNS server failed: %s", strerror(errno));
        }
    }
    else
    {
        memcpy(&serverAddr6.sin6_addr, &aServerAddress, sizeof(otIp6Address));
        serverAddr6.sin6_family = AF_INET6;
        serverAddr6.sin6_port   = htons(53);
        if (IsIp6AddressLinkLocal(aServerAddress) && infraIfIndex != 0)
        {
            serverAddr6.sin6_scope_id = infraIfIndex;
        }
        sent = (sendto(aTxn->mUdpFd6, aPacket, aLength, MSG_DONTWAIT, reinterpret_cast<sockaddr *>(&serverAddr6),
                       sizeof(serverAddr6)) > 0);
        if (!sent && inet_ntop(AF_INET6, &aServerAddress, addrStr, sizeof(addrStr)) != nullptr)
        {
            otbrLogWarning("sendto [%s] scope=%u failed: %s", addrStr, serverAddr6.sin6_scope_id, strerror(errno));
        }
    }

    return sent;
}

NcpUpstreamDnsResolver::Transaction *NcpUpstreamDnsResolver::AllocateTransaction(uint8_t aTxnIndex)
{
    Transaction *ret = nullptr;

    for (Transaction &txn : mTransactions)
    {
        if (!txn.mInUse)
        {
            int fd4 = CreateUdpSocket(AF_INET);
            int fd6 = CreateUdpSocket(AF_INET6);

            if (fd4 < 0 || fd6 < 0)
            {
                if (fd4 >= 0)
                {
                    close(fd4);
                }
                if (fd6 >= 0)
                {
                    close(fd6);
                }
                break;
            }

            txn.mInUse    = true;
            txn.mTxnIndex = aTxnIndex;
            txn.mUdpFd4   = fd4;
            txn.mUdpFd6   = fd6;
            ret           = &txn;
            break;
        }
    }

    return ret;
}

NcpUpstreamDnsResolver::Transaction *NcpUpstreamDnsResolver::GetTransaction(uint8_t aTxnIndex)
{
    Transaction *ret = nullptr;

    for (Transaction &txn : mTransactions)
    {
        if (txn.mInUse && txn.mTxnIndex == aTxnIndex)
        {
            ret = &txn;
            break;
        }
    }

    return ret;
}

void NcpUpstreamDnsResolver::CloseTransaction(Transaction *aTxn)
{
    if (aTxn->mUdpFd4 >= 0)
    {
        close(aTxn->mUdpFd4);
        aTxn->mUdpFd4 = -1;
    }
    if (aTxn->mUdpFd6 >= 0)
    {
        close(aTxn->mUdpFd6);
        aTxn->mUdpFd6 = -1;
    }
    aTxn->mInUse = false;
}

void NcpUpstreamDnsResolver::ReportQueryFailure(uint8_t aTxnIndex)
{
    if (mResponseCallback != nullptr)
    {
        mResponseCallback(aTxnIndex, nullptr, 0);
    }
}

void NcpUpstreamDnsResolver::Query(uint8_t aTxnIndex, const uint8_t *aQuery, uint16_t aLength)
{
    Transaction *txn         = nullptr;
    uint32_t     serverCount = 0;
    uint32_t     i;
    bool         failed = false;

    if (aQuery == nullptr || aLength == 0 || aLength > kMaxDnsMessageSize)
    {
        failed = true;
        ExitNow();
    }

    {
        Transaction *existingTxn = GetTransaction(aTxnIndex);

        if (existingTxn != nullptr)
        {
            CloseTransaction(existingTxn);
        }
    }

    txn = AllocateTransaction(aTxnIndex);
    if (txn == nullptr)
    {
        failed = true;
        ExitNow();
    }

    if (mRecursiveDnsServerCount > 0)
    {
        for (i = 0; i < mRecursiveDnsServerCount; i++)
        {
            if (SendQueryToServer(txn, mRecursiveDnsServerList[i], aQuery, aLength))
            {
                serverCount++;
            }
        }
    }
    else
    {
        TryRefreshDnsServerList();

        for (i = 0; i < mUpstreamDnsServerCount; i++)
        {
            if (SendQueryToServer(txn, mUpstreamDnsServerList[i], aQuery, aLength))
            {
                serverCount++;
            }
        }
    }

    if (serverCount == 0)
    {
        otbrLogWarning("txn %u: failed to forward DNS query (%u RDNSS, %u resolv.conf servers configured)", aTxnIndex,
                       mRecursiveDnsServerCount, mUpstreamDnsServerCount);
        CloseTransaction(txn);
        failed = true;
    }

exit:
    if (failed)
    {
        ReportQueryFailure(aTxnIndex);
    }
}

void NcpUpstreamDnsResolver::Cancel(uint8_t aTxnIndex)
{
    Transaction *txn = GetTransaction(aTxnIndex);

    if (txn != nullptr)
    {
        CloseTransaction(txn);
    }
}

void NcpUpstreamDnsResolver::ForwardResponse(Transaction *aTxn, int aFd)
{
    uint8_t response[kMaxDnsMessageSize];
    ssize_t readSize = -1;

    VerifyOrExit((readSize = read(aFd, response, sizeof(response))) > 0);

    if (mResponseCallback)
    {
        mResponseCallback(aTxn->mTxnIndex, response, static_cast<uint16_t>(readSize));
    }

exit:
    return;
}

void NcpUpstreamDnsResolver::Update(MainloopContext &aMainloop)
{
    for (const Transaction &txn : mTransactions)
    {
        if (txn.mInUse)
        {
            aMainloop.AddFdToSet(txn.mUdpFd4, MainloopContext::kReadFdSet | MainloopContext::kErrorFdSet);
            aMainloop.AddFdToSet(txn.mUdpFd6, MainloopContext::kReadFdSet | MainloopContext::kErrorFdSet);
        }
    }
}

void NcpUpstreamDnsResolver::Process(const MainloopContext &aMainloop)
{
    for (Transaction &txn : mTransactions)
    {
        if (!txn.mInUse)
        {
            continue;
        }

        if (FD_ISSET(txn.mUdpFd4, &aMainloop.mErrorFdSet) || FD_ISSET(txn.mUdpFd4, &aMainloop.mReadFdSet))
        {
            ForwardResponse(&txn, txn.mUdpFd4);
            CloseTransaction(&txn);
        }
        else if (FD_ISSET(txn.mUdpFd6, &aMainloop.mErrorFdSet) || FD_ISSET(txn.mUdpFd6, &aMainloop.mReadFdSet))
        {
            ForwardResponse(&txn, txn.mUdpFd6);
            CloseTransaction(&txn);
        }
    }
}

} // namespace otbr
