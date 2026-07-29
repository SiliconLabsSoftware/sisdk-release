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

#define OTBR_LOG_TAG "NAT64_TAYGA"

#include "nat64_tayga_host.hpp"

#include <openthread/ip6.h>

#include <net/if.h>

#include <fstream>
#include <string>
#include <unistd.h>
#include <vector>

#include "common/code_utils.hpp"
#include "common/logging.hpp"
#include "utils/system_utils.hpp"

#if OTBR_ENABLE_NAT64 && OTBR_ENABLE_NAT64_TAYGA && defined(__linux__)

namespace otbr {

namespace {

// Paths and defaults aligned with OTBR script/_nat64 (tayga_install / sync-tayga-nat64-prefix.sh).
constexpr char kTaygaConfPath[]         = "/etc/tayga.conf";
constexpr char kTaygaConfTmpPath[]      = "/etc/tayga.conf.tmp";
constexpr char kTaygaServiceUnit[]      = "tayga";
constexpr char kTunDevice[]             = "nat64";
constexpr char kWpanInterface[]         = "wpan0";
constexpr char kTaygaIpv6Addr[]         = "fdaa:bb:1::1";
constexpr char kTaygaIpv4Addr[]         = "192.168.255.1";
constexpr char kTaygaDynamicPool[]      = "192.168.255.0/24";
constexpr char kConfKeyPrefix[]         = "prefix ";
constexpr char kConfKeyTunDevice[]      = "tun-device";
constexpr char kConfKeyIpv6Addr[]       = "ipv6-addr";
constexpr char kConfKeyIpv4Addr[]       = "ipv4-addr";
constexpr char kConfKeyDynamicPool[]    = "dynamic-pool";
constexpr char kSysctlRpFilterDisable[] = "0";

constexpr uint8_t kNat64PrefixLength = 96;

constexpr uint8_t    kTunDevicePollMaxAttempts = 50;
constexpr useconds_t kTunDevicePollIntervalUs  = 50000;

constexpr const char *kRpFilterInterfaces[] = {kWpanInterface, kTunDevice};

class TaygaHostCommands
{
public:
    static void InstallRoutes(const char *aNat64Prefix, bool aTaygaWasRestarted);
    static void ConfigureRpFilter(void);
    static void RestartTaygaService(void);

private:
    static bool IsTunDevicePresent(void);
    static bool WaitForTunDeviceReady(bool aTaygaWasRestarted);
    static void SetTunDeviceUp(void);
    static void SetRpFilter(const char *aIpVersion, const char *aInterface);
};

bool TaygaHostCommands::IsTunDevicePresent(void)
{
    return if_nametoindex(kTunDevice) != 0;
}

bool TaygaHostCommands::WaitForTunDeviceReady(bool aTaygaWasRestarted)
{
    bool ready = false;

    if (!aTaygaWasRestarted)
    {
        ready = IsTunDevicePresent();
        ExitNow();
    }

    for (uint8_t attempt = 0; attempt < kTunDevicePollMaxAttempts; attempt++)
    {
        if (IsTunDevicePresent())
        {
            ready = true;
            ExitNow();
        }

        usleep(kTunDevicePollIntervalUs);
    }

exit:
    return ready;
}

void TaygaHostCommands::SetTunDeviceUp(void)
{
    SystemUtils::ExecuteCommand("ip link set dev %s up", kTunDevice);
}

void TaygaHostCommands::InstallRoutes(const char *aNat64Prefix, bool aTaygaWasRestarted)
{
    if (!WaitForTunDeviceReady(aTaygaWasRestarted))
    {
        otbrLogWarning("NAT64 TAYGA: %s not present, skipping route install", kTunDevice);
        ExitNow();
    }

    SetTunDeviceUp();
    SystemUtils::ExecuteCommand("ip -6 route replace %s dev %s", aNat64Prefix, kTunDevice);
    SystemUtils::ExecuteCommand("ip route replace %s dev %s", kTaygaDynamicPool, kTunDevice);

exit:
    return;
}

void TaygaHostCommands::SetRpFilter(const char *aIpVersion, const char *aInterface)
{
    SystemUtils::ExecuteCommand("sysctl -w net.%s.conf.%s.rp_filter=%s >/dev/null 2>&1", aIpVersion, aInterface,
                                kSysctlRpFilterDisable);
}

void TaygaHostCommands::ConfigureRpFilter(void)
{
    for (const char *iface : kRpFilterInterfaces)
    {
        SetRpFilter("ipv4", iface);
        SetRpFilter("ipv6", iface);
    }
}

void TaygaHostCommands::RestartTaygaService(void)
{
    SystemUtils::ExecuteCommand("systemctl try-restart %s", kTaygaServiceUnit);
}

bool ConfLineHasKey(const std::string &aLine, const char *aKey)
{
    return aLine.rfind(aKey, 0) == 0;
}

bool EnsureConfLine(std::vector<std::string> &aLines, const char *aKey, const char *aValue)
{
    const std::string want = std::string(aKey) + " " + aValue;

    for (std::string &line : aLines)
    {
        if (ConfLineHasKey(line, aKey))
        {
            if (line != want)
            {
                line = want;
                return true;
            }
            return false;
        }
    }

    aLines.emplace_back(want);
    return true;
}

bool HasPrefixLine(const std::vector<std::string> &aLines)
{
    for (const std::string &line : aLines)
    {
        if (ConfLineHasKey(line, kConfKeyPrefix))
        {
            return true;
        }
    }

    return false;
}

bool UpdateTaygaConf(const char *aPrefix)
{
    std::vector<std::string> lines;
    std::string              line;
    std::ifstream            in(kTaygaConfPath);
    bool                     changed = false;

    if (!in.is_open())
    {
        return false;
    }

    while (std::getline(in, line))
    {
        if (ConfLineHasKey(line, kConfKeyPrefix))
        {
            std::string newLine = std::string(kConfKeyPrefix) + aPrefix;

            if (line != newLine)
            {
                changed = true;
            }
            lines.push_back(newLine);
        }
        else
        {
            lines.push_back(line);
        }
    }
    in.close();

    changed |= EnsureConfLine(lines, kConfKeyTunDevice, kTunDevice);
    changed |= EnsureConfLine(lines, kConfKeyIpv6Addr, kTaygaIpv6Addr);
    changed |= EnsureConfLine(lines, kConfKeyIpv4Addr, kTaygaIpv4Addr);
    changed |= EnsureConfLine(lines, kConfKeyDynamicPool, kTaygaDynamicPool);

    if (!HasPrefixLine(lines))
    {
        lines.emplace_back(std::string(kConfKeyPrefix) + aPrefix);
        changed = true;
    }

    if (!changed)
    {
        return false;
    }

    {
        std::ofstream out(kTaygaConfTmpPath);

        if (!out.is_open())
        {
            return false;
        }

        for (const std::string &outLine : lines)
        {
            out << outLine << '\n';
        }
    }

    return std::rename(kTaygaConfTmpPath, kTaygaConfPath) == 0;
}

} // namespace

void SyncNat64Tayga(const otIp6Prefix &aPrefix)
{
    char prefixBuf[OT_IP6_PREFIX_STRING_SIZE];
    bool confChanged;

    VerifyOrExit(aPrefix.mLength == kNat64PrefixLength,
                 otbrLogWarning("Ignoring NAT64 prefix with invalid length %u", aPrefix.mLength));

    TaygaHostCommands::ConfigureRpFilter();

    otIp6PrefixToString(&aPrefix, prefixBuf, sizeof(prefixBuf));

    confChanged = UpdateTaygaConf(prefixBuf);

    if (confChanged)
    {
        TaygaHostCommands::RestartTaygaService();
    }

    // Install routes after tayga is up. Routes added before restart are lost when the TUN is recreated.
    TaygaHostCommands::InstallRoutes(prefixBuf, confChanged);

    otbrLogInfo("NAT64 TAYGA synced prefix %s", prefixBuf);

exit:
    return;
}

} // namespace otbr

#else

namespace otbr {

void SyncNat64Tayga(const otIp6Prefix &aPrefix)
{
    OTBR_UNUSED_VARIABLE(aPrefix);
}

} // namespace otbr

#endif
