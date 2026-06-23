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

#pragma once

#include <stddef.h>
#include <stdint.h>

static constexpr uint8_t kSpinelHeaderFlag     = 0x80;
static constexpr uint8_t kSpinelHeaderIidShift = 4;
static constexpr uint8_t kSpinelHeaderIidMask  = 3 << kSpinelHeaderIidShift;
static constexpr uint8_t kSpinelHeaderIidMax   = 3;

class SpinelIidPolicy
{
public:
    enum class Action
    {
        kForward,
        kDrop,
    };

    virtual ~SpinelIidPolicy() {}

    virtual Action HandleHostToSecondary(uint8_t *aFrame, size_t aLength, bool aVerbose) const = 0;
    virtual Action HandleSecondaryToHost(uint8_t *aFrame, size_t aLength, bool aVerbose) const = 0;
    virtual bool   RequiresSecondaryToHostCopy(void) const                                     = 0;
    virtual void   LogConfig(void) const                                                       = 0;
};

class PassThroughIidPolicy : public SpinelIidPolicy
{
public:
    Action HandleHostToSecondary(uint8_t *aFrame, size_t aLength, bool aVerbose) const override;
    Action HandleSecondaryToHost(uint8_t *aFrame, size_t aLength, bool aVerbose) const override;
    bool   RequiresSecondaryToHostCopy(void) const override { return false; }
    void   LogConfig(void) const override {}
};

class TranslationIidPolicy : public SpinelIidPolicy
{
public:
    TranslationIidPolicy();

    bool SetHostIid(const char *aValue);
    bool SetIid(const char *aValue);
    bool SetIidList(const char *aValue);

    Action HandleHostToSecondary(uint8_t *aFrame, size_t aLength, bool aVerbose) const override;
    Action HandleSecondaryToHost(uint8_t *aFrame, size_t aLength, bool aVerbose) const override;
    bool   RequiresSecondaryToHostCopy(void) const override { return true; }
    void   LogConfig(void) const override;

    void Finalize(void);

private:
    uint8_t mHostIid;
    uint8_t mIid;
    bool    mAcceptIids[kSpinelHeaderIidMax + 1];
};
