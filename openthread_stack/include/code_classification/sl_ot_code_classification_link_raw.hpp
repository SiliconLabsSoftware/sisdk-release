/*******************************************************************************
 * @file
 * @brief Provides definitions for indirect code classification of functions
 * in link_raw API module.
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
#ifndef OT_CORE_MAC_LINK_RAW_HPP_
#define OT_CORE_MAC_LINK_RAW_HPP_

#include "openthread-core-config.h"

#if OPENTHREAD_RADIO || OPENTHREAD_CONFIG_LINK_RAW_ENABLE

#include <openthread/link_raw.h>
#include <openthread/platform/radio.h>

#include "common/locator.hpp"
// #include "common/log.hpp"
#include "common/non_copyable.hpp"
#include "mac/mac_frame.hpp"
#include "mac/sub_mac.hpp"

#include "sl_code_classification.h"

namespace ot {
namespace Mac {

/**
 * Defines the raw link-layer object.
 */
class LinkRaw : public InstanceLocator, private NonCopyable
{
    friend class ot::Instance;

public:
    /**
     * Initializes the object.
     *
     * @param[in]   aInstance   A reference to the OpenThread instance.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    explicit LinkRaw(Instance &aInstance);

    /**
     * Initializes the states of the raw link-layer.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    void Init(void);

    /**
     * Returns true if the raw link-layer is enabled.
     *
     * @returns true if enabled, false otherwise.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    bool IsEnabled(void) const { return mReceiveDoneCallback != nullptr; }

    /**
     * Enables/disables the raw link-layer.
     *
     * @param[in]  aCallback  A pointer to a function called on receipt of a IEEE 802.15.4 frame, `nullptr` to disable
     *                        raw link-layer.
     *
     *
     * @retval kErrorInvalidState    Thread stack is enabled.
     * @retval kErrorFailed          The radio could not be enabled/disabled.
     * @retval kErrorNone            Successfully enabled/disabled raw link.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error SetReceiveDone(otLinkRawReceiveDone aCallback);

    /**
     * Returns the capabilities of the raw link-layer.
     *
     * @returns The radio capability bit vector.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    otRadioCaps GetCaps(void) const { return mSubMac.GetCaps(); }

    /**
     * Starts a (recurring) Receive on the link-layer.
     *
     * @retval kErrorNone            Successfully transitioned to Receive.
     * @retval kErrorInvalidState    The radio was disabled or transmitting.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error Receive(void);

    /**
     * Invokes the mReceiveDoneCallback, if set.
     *
     * @param[in]  aFrame    A pointer to the received frame or `nullptr` if the receive operation failed.
     * @param[in]  aError    kErrorNone when successfully received a frame,
     *                       kErrorAbort when reception was aborted and a frame was not received,
     *                       kErrorNoBufs when a frame could not be received due to lack of rx buffer space.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    void InvokeReceiveDone(RxFrame *aFrame, Error aError);

    /**
     * Gets the radio transmit frame.
     *
     * @returns The transmit frame.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    TxFrame &GetTransmitFrame(void) { return mSubMac.GetTransmitFrame(); }

    /**
     * Starts a (single) Transmit on the link-layer.
     *
     * @note The callback @p aCallback will not be called if this call does not return kErrorNone.
     *
     * @param[in]  aCallback            A pointer to a function called on completion of the transmission.
     *
     * @retval kErrorNone           Successfully transitioned to Transmit.
     * @retval kErrorInvalidState   The radio was not in the Receive state.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error Transmit(otLinkRawTransmitDone aCallback);

    /**
     * Invokes the mTransmitDoneCallback, if set.
     *
     * @param[in]  aFrame     The transmitted frame.
     * @param[in]  aAckFrame  A pointer to the ACK frame, `nullptr` if no ACK was received.
     * @param[in]  aError     kErrorNone when the frame was transmitted,
     *                        kErrorNoAck when the frame was transmitted but no ACK was received,
     *                        kErrorChannelAccessFailure tx failed due to activity on the channel,
     *                        kErrorAbort when transmission was aborted for other reasons.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    void InvokeTransmitDone(TxFrame &aFrame, RxFrame *aAckFrame, Error aError);

    /**
     * Starts a (single) Energy Scan on the link-layer.
     *
     * @param[in]  aScanChannel     The channel to perform the energy scan on.
     * @param[in]  aScanDuration    The duration, in milliseconds, for the channel to be scanned.
     * @param[in]  aCallback        A pointer to a function called on completion of a scanned channel.
     *
     * @retval kErrorNone            Successfully started scanning the channel.
     * @retval kErrorBusy            The radio is performing energy scanning.
     * @retval kErrorNotImplemented  The radio doesn't support energy scanning.
     * @retval kErrorInvalidState    If the raw link-layer isn't enabled.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error EnergyScan(uint8_t aScanChannel, uint16_t aScanDuration, otLinkRawEnergyScanDone aCallback);

    /**
     * Invokes the mEnergyScanDoneCallback, if set.
     *
     * @param[in]   aEnergyScanMaxRssi  The max RSSI for energy scan.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    void InvokeEnergyScanDone(int8_t aEnergyScanMaxRssi);

    /**
     * Returns the short address.
     *
     * @returns short address.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    ShortAddress GetShortAddress(void) const { return mSubMac.GetShortAddress(); }

    /**
     * Updates short address.
     *
     * @param[in]   aShortAddress   The short address.
     *
     * @retval kErrorNone            If successful.
     * @retval kErrorInvalidState    If the raw link-layer isn't enabled.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error SetShortAddress(ShortAddress aShortAddress);

    /**
     * Sets the alternate short address.
     *
     * @param[in] aShortAddress   The short address. Use `kShortAddrInvalid` to clear it.
     *
     * @retval kErrorNone            If successful.
     * @retval kErrorInvalidState    If the raw link-layer isn't enabled.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error SetAlternateShortAddress(ShortAddress aShortAddress);

    /**
     * Returns PANID.
     *
     * @returns PANID.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    PanId GetPanId(void) const { return mPanId; }

    /**
     * Updates PANID.
     *
     * @param[in]   aPanId          The PANID.
     *
     * @retval kErrorNone            If successful.
     * @retval kErrorInvalidState    If the raw link-layer isn't enabled.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error SetPanId(PanId aPanId);

    /**
     * Gets the current receiving channel.
     *
     * @returns Current receiving channel.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    uint8_t GetChannel(void) const { return mReceiveChannel; }

    /**
     * Sets the receiving channel.
     *
     * @param[in]  aChannel     The channel to use for receiving.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error SetChannel(uint8_t aChannel);

    /**
     * Returns the extended address.
     *
     * @returns A reference to the extended address.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    const ExtAddress &GetExtAddress(void) const { return mSubMac.GetExtAddress(); }

    /**
     * Updates extended address.
     *
     * @param[in]   aExtAddress     The extended address.
     *
     * @retval kErrorNone            If successful.
     * @retval kErrorInvalidState    If the raw link-layer isn't enabled.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error SetExtAddress(const ExtAddress &aExtAddress);

    /**
     * Updates MAC keys and key index.
     *
     * @param[in]   aKeyIdMode        The key ID mode.
     * @param[in]   aKeyId            The key index.
     * @param[in]   aPrevKey          The previous MAC key.
     * @param[in]   aCurrKey          The current MAC key.
     * @param[in]   aNextKey          The next MAC key.
     *
     * @retval kErrorNone            If successful.
     * @retval kErrorFailed          Platform failed to import key.
     * @retval kErrorInvalidState    If the raw link-layer isn't enabled.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error SetMacKey(uint8_t aKeyIdMode, uint8_t aKeyId, const Key &aPrevKey, const Key &aCurrKey, const Key &aNextKey);

    /**
     * Sets the current MAC frame counter value.
     *
     * @param[in] aFrameCounter  The MAC frame counter value.
     * @param[in] aSetIfLarger   If `true`, set only if the new value @p aFrameCounter is larger than current value.
     *                           If `false`, set the new value independent of the current value.
     *
     * @retval kErrorNone            If successful.
     * @retval kErrorInvalidState    If the raw link-layer isn't enabled.
     */
    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)
    Error SetMacFrameCounter(uint32_t aFrameCounter, bool aSetIfLarger);

    SL_CODE_CLASSIFY(SL_CODE_COMPONENT_OPENTHREAD, SL_CODE_CLASS_TIME_CRITICAL)

// #if OT_SHOULD_LOG_AT(OT_LOG_LEVEL_INFO)
// Avoid including log.hpp
#if ((OPENTHREAD_CONFIG_LOG_OUTPUT != OPENTHREAD_CONFIG_LOG_OUTPUT_NONE) \
     && (OPENTHREAD_CONFIG_LOG_LEVEL >= 4))
    /**
     * Records the status of a frame transmission attempt and is mainly used for logging failures.
     *
     * Unlike `HandleTransmitDone` which is called after all transmission attempts of frame to indicate final status
     * of a frame transmission request, this method is invoked on all frame transmission attempts.
     *
     * @param[in] aFrame      The transmitted frame.
     * @param[in] aError      kErrorNone when the frame was transmitted successfully,
     *                        kErrorNoAck when the frame was transmitted but no ACK was received,
     *                        kErrorChannelAccessFailure tx failed due to activity on the channel,
     *                        kErrorAbort when transmission was aborted for other reasons.
     * @param[in] aRetryCount Indicates number of transmission retries for this frame.
     * @param[in] aWillRetx   Indicates whether frame will be retransmitted or not. This is applicable only
     *                        when there was an error in transmission (i.e., `aError` is not NONE).
     */
   void RecordFrameTransmitStatus(const TxFrame &aFrame, Error aError, uint8_t aRetryCount, bool aWillRetx);
#else
    void RecordFrameTransmitStatus(const TxFrame &, Error, uint8_t, bool) {}
#endif

private:
    uint8_t                 mReceiveChannel;
    PanId                   mPanId;
    otLinkRawReceiveDone    mReceiveDoneCallback;
    otLinkRawTransmitDone   mTransmitDoneCallback;
    otLinkRawEnergyScanDone mEnergyScanDoneCallback;

#if OPENTHREAD_RADIO
    SubMac mSubMac;
#elif OPENTHREAD_CONFIG_LINK_RAW_ENABLE
    SubMac &mSubMac;
#endif
};

} // namespace Mac
} // namespace ot

#endif // OPENTHREAD_RADIO || OPENTHREAD_CONFIG_LINK_RAW_ENABLE

#endif // OT_CORE_MAC_LINK_RAW_HPP_
