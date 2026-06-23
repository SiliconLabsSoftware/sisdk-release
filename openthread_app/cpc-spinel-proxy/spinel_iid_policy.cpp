/*******************************************************************************
 * @file
 * @brief Spinel IID forwarding policy for cpc-spinel-proxy.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 ******************************************************************************/

#include "spinel_iid_policy.hpp"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

namespace {

uint8_t SpinelGetIid(uint8_t aHeader)
{
    return (aHeader & kSpinelHeaderIidMask) >> kSpinelHeaderIidShift;
}

uint8_t SpinelSetIid(uint8_t aHeader, uint8_t aIid)
{
    return static_cast<uint8_t>((aHeader & ~kSpinelHeaderIidMask)
                                | ((aIid << kSpinelHeaderIidShift) & kSpinelHeaderIidMask));
}

bool ParseIid(const char *aValue, const char *aOptionName, uint8_t *aIid)
{
    char *end = nullptr;
    long  value;

    if (aValue == nullptr || *aValue == '\0')
    {
        fprintf(stderr, "Invalid %s (use integer 0-%u)\n", aOptionName, kSpinelHeaderIidMax);
        return false;
    }

    errno = 0;
    value = strtol(aValue, &end, 10);
    if (errno != 0 || end == aValue || *end != '\0' || value < 0 || value > kSpinelHeaderIidMax)
    {
        fprintf(stderr, "Invalid %s (use integer 0-%u)\n", aOptionName, kSpinelHeaderIidMax);
        return false;
    }

    *aIid = static_cast<uint8_t>(value);
    return true;
}

bool ValidateSpinelHeader(const uint8_t *aFrame, size_t aLength, const char *aDirection, bool aVerbose)
{
    if (aLength == 0)
    {
        if (aVerbose)
        {
            fprintf(stderr, "%s drop: empty frame\n", aDirection);
        }
        return false;
    }

    if ((aFrame[0] & kSpinelHeaderFlag) != kSpinelHeaderFlag)
    {
        if (aVerbose)
        {
            fprintf(stderr, "%s drop: invalid Spinel header 0x%02x\n", aDirection, aFrame[0]);
        }
        return false;
    }

    return true;
}

} // namespace

SpinelIidPolicy::Action PassThroughIidPolicy::HandleHostToSecondary(uint8_t *aFrame,
                                                                    size_t   aLength,
                                                                    bool     aVerbose) const
{
    (void)aFrame;
    (void)aLength;
    (void)aVerbose;
    return Action::kForward;
}

SpinelIidPolicy::Action PassThroughIidPolicy::HandleSecondaryToHost(uint8_t *aFrame,
                                                                    size_t   aLength,
                                                                    bool     aVerbose) const
{
    (void)aFrame;
    (void)aLength;
    (void)aVerbose;
    return Action::kForward;
}

TranslationIidPolicy::TranslationIidPolicy()
    : mHostIid(0)
    , mIid(0)
    , mAcceptIids{}
{
}

bool TranslationIidPolicy::SetHostIid(const char *aValue)
{
    return ParseIid(aValue, "--host-iid", &mHostIid);
}

bool TranslationIidPolicy::SetIid(const char *aValue)
{
    return ParseIid(aValue, "--iid", &mIid);
}

bool TranslationIidPolicy::SetIidList(const char *aValue)
{
    const char *p = aValue;

    if (p == nullptr || *p == '\0')
    {
        fprintf(stderr, "Invalid --iid-list (use comma-separated IIDs 0-%u)\n", kSpinelHeaderIidMax);
        return false;
    }

    while (*p != '\0')
    {
        char *end = nullptr;
        long  value;

        errno = 0;
        value = strtol(p, &end, 10);
        if (errno != 0 || end == p || value < 0 || value > kSpinelHeaderIidMax)
        {
            fprintf(stderr, "Invalid --iid-list (use comma-separated IIDs 0-%u)\n", kSpinelHeaderIidMax);
            return false;
        }

        mAcceptIids[static_cast<uint8_t>(value)] = true;

        if (*end == '\0')
        {
            break;
        }
        if (*end != ',')
        {
            fprintf(stderr, "Invalid --iid-list (use comma-separated IIDs 0-%u)\n", kSpinelHeaderIidMax);
            return false;
        }
        p = end + 1;
        if (*p == '\0')
        {
            fprintf(stderr, "Invalid --iid-list (trailing comma)\n");
            return false;
        }
    }

    return true;
}

void TranslationIidPolicy::Finalize(void)
{
    mAcceptIids[mIid] = true;
}

SpinelIidPolicy::Action TranslationIidPolicy::HandleHostToSecondary(uint8_t *aFrame,
                                                                    size_t   aLength,
                                                                    bool     aVerbose) const
{
    if (!ValidateSpinelHeader(aFrame, aLength, "HAL->secondary", aVerbose))
    {
        return Action::kDrop;
    }

    uint8_t oldHeader = aFrame[0];
    uint8_t iid       = SpinelGetIid(oldHeader);
    if (iid != mHostIid)
    {
        if (aVerbose)
        {
            fprintf(stderr, "HAL->secondary drop: iid=%u (expected host-iid=%u)\n", iid, mHostIid);
        }
        return Action::kDrop;
    }

    aFrame[0] = SpinelSetIid(oldHeader, mIid);
    if (aVerbose && aFrame[0] != oldHeader)
    {
        fprintf(stderr,
                "HAL->secondary IID rewrite: %u -> %u (header 0x%02x -> 0x%02x)\n",
                iid,
                mIid,
                oldHeader,
                aFrame[0]);
    }

    return Action::kForward;
}

SpinelIidPolicy::Action TranslationIidPolicy::HandleSecondaryToHost(uint8_t *aFrame,
                                                                    size_t   aLength,
                                                                    bool     aVerbose) const
{
    if (!ValidateSpinelHeader(aFrame, aLength, "secondary->HAL", aVerbose))
    {
        return Action::kDrop;
    }

    uint8_t oldHeader = aFrame[0];
    uint8_t iid       = SpinelGetIid(oldHeader);
    if (!mAcceptIids[iid])
    {
        if (aVerbose)
        {
            fprintf(stderr, "secondary->HAL drop: iid=%u is not subscribed\n", iid);
        }
        return Action::kDrop;
    }

    aFrame[0] = SpinelSetIid(oldHeader, mHostIid);
    if (aVerbose && aFrame[0] != oldHeader)
    {
        fprintf(stderr,
                "secondary->HAL IID rewrite: %u -> %u (header 0x%02x -> 0x%02x)\n",
                iid,
                mHostIid,
                oldHeader,
                aFrame[0]);
    }

    return Action::kForward;
}

void TranslationIidPolicy::LogConfig(void) const
{
    fprintf(stderr, "cpc-spinel-proxy: IID translation enabled: host-iid=%u iid=%u receive-iids=", mHostIid, mIid);

    bool first = true;
    for (uint8_t iid = 0; iid <= kSpinelHeaderIidMax; iid++)
    {
        if (!mAcceptIids[iid])
        {
            continue;
        }
        fprintf(stderr, "%s%u", first ? "" : ",", iid);
        first = false;
    }
    fprintf(stderr, "\n");
}
