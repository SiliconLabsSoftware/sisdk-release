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

#define OTBR_LOG_TAG "FIREWALL_INGRESS"

#include "firewall_ingress.hpp"

#include <openthread/ip6.h>

#include <set>
#include <string>
#include <vector>

#include "common/code_utils.hpp"
#include "common/logging.hpp"

#if defined(__linux__) && OPENTHREAD_POSIX_CONFIG_FIREWALL_ENABLE
namespace ot {
namespace Posix {
void ApplyOtbrIngressAllowDstPrefixes(const char *const *aPrefixes, size_t aCount);
} // namespace Posix
} // namespace ot
#endif

namespace otbr {

void RefreshIngressAllowDstFromThreadUnicastAddrs(const std::vector<Ip6AddressInfo> &aAddrs)
{
#if defined(__linux__) && OPENTHREAD_POSIX_CONFIG_FIREWALL_ENABLE
    constexpr uint8_t         kPrefixLen64 = 64;
    std::set<std::string>     prefixes;
    std::vector<std::string>  storage;
    std::vector<const char *> cstrs;

    for (const Ip6AddressInfo &info : aAddrs)
    {
        otIp6Prefix prefix;
        char        prefixBuf[OT_IP6_PREFIX_STRING_SIZE];

        if (info.mPrefixLength != kPrefixLen64)
        {
            continue;
        }

        if (info.mAddress.mFields.m8[0] == 0xff)
        {
            continue;
        }

        if (info.mAddress.mFields.m8[0] == 0xfe && (info.mAddress.mFields.m8[1] & 0xc0) == 0x80)
        {
            continue;
        }

        memcpy(&prefix.mPrefix, &info.mAddress, sizeof(otIp6Address));
        prefix.mLength = kPrefixLen64;
        otIp6PrefixToString(&prefix, prefixBuf, sizeof(prefixBuf));
        prefixes.insert(prefixBuf);
    }

    storage.reserve(prefixes.size());
    for (const std::string &p : prefixes)
    {
        storage.push_back(p);
    }

    cstrs.reserve(storage.size());
    for (const std::string &s : storage)
    {
        cstrs.push_back(s.c_str());
    }

    ot::Posix::ApplyOtbrIngressAllowDstPrefixes(cstrs.data(), cstrs.size());
    otbrLogDebug("ingress allow-dst refreshed: %zu /64 prefix(es) (NAT64 reply path toward Thread)", cstrs.size());
#else
    OTBR_UNUSED_VARIABLE(aAddrs);
#endif
}

} // namespace otbr
