/***************************************************************************//**
 * @file ip6.h
 * @brief IPv6 protocol-level definitions
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

#ifndef NETINET_IP6_H
#define NETINET_IP6_H

#ifdef __cplusplus
extern "C" {
#endif

/**************************************************************************//**
 * @addtogroup SL_WISUN_SOCKET_API Socket API
 * @ingroup SL_WISUN_API
 *
 * @{
 *****************************************************************************/

/** \name Differentiated Services Code Points (DSCP) — IANA assigned values
 *
 * These are the raw code-point values;
 * combine with #IPV6_TCLASS_FROM_DSCP or #IPV6_TCLASS_FROM_DSCP_AND_ECN
 * to obtain a Traffic Class octet suitable for use with #IPV6_TCLASS.
 */
///@{
#define IP_DSCP_CS0         0   ///< CS0
#define IP_DSCP_CS1         8   ///< CS1
#define IP_DSCP_AF11        10  ///< AF11
#define IP_DSCP_AF12        12  ///< AF12
#define IP_DSCP_AF13        14  ///< AF13
#define IP_DSCP_CS2         16  ///< CS2
#define IP_DSCP_AF21        18  ///< AF21
#define IP_DSCP_AF22        20  ///< AF22
#define IP_DSCP_AF23        22  ///< AF23
#define IP_DSCP_CS3         24  ///< CS3
#define IP_DSCP_AF31        26  ///< AF31
#define IP_DSCP_AF32        28  ///< AF32
#define IP_DSCP_AF33        30  ///< AF33
#define IP_DSCP_CS4         32  ///< CS4
#define IP_DSCP_AF41        34  ///< AF41
#define IP_DSCP_AF42        36  ///< AF42
#define IP_DSCP_AF43        38  ///< AF43
#define IP_DSCP_CS5         40  ///< CS5
#define IP_DSCP_VOICE_ADMIT 44  ///< VOICE-ADMIT
#define IP_DSCP_EF          46  ///< EF
#define IP_DSCP_CS6         48  ///< CS6
#define IP_DSCP_CS7         56  ///< CS7
///@}

/** \name Wi-SUN DSCP (Differentiated Services Code Point) QoS supported levels. */
///@{
/** Standard priority and it is socket default */
#define DSCP_DEFAULT IP_DSCP_CS0
/** Application high priority service: Stack priorities these messages over the default priority messages */
#define DSCP_AF11    IP_DSCP_AF11
/** Expedited Forwarding (EF) QoS level enable high priority state: low loss, low delay, and low jitter services */
#define DSCP_EF      IP_DSCP_EF
///@}

/** \name Explicit Congestion Notification (ECN) code points (RFC 3168)
 *
 * Two-bit ECN values occupying bits 1-0 of the IPv6 Traffic Class octet
 * (and the equivalent IPv4 ToS field).
 *
 */
///@{
#define IP_ECN_NOT_ECT      0  ///< Not ECN-Capable Transport
#define IP_ECN_ECT_1        1  ///< ECN-Capable Transport(1)
#define IP_ECN_ECT_0        2  ///< ECN-Capable Transport(0)
#define IP_ECN_CE           3  ///< Congestion Experienced
///@}

/** \name IPv6 Traffic Class byte (RFC 3542 section 6.5)
 *
 * The IPv6 Traffic Class is an 8-bit field placed in the IPv6 header:
 * DSCP (Differentiated Services Code Point, RFC 2474) occupies bits 7-2
 * and ECN (Explicit Congestion Notification, RFC 3168) bits 1-0.
 *
 * Use #IPV6_TCLASS_FROM_DSCP or #IPV6_TCLASS_FROM_DSCP_AND_ECN to build a
 * Traffic Class octet from a DSCP code point (0-63), and
 * #IPV6_DSCP_FROM_TCLASS for the inverse.
 *
 * These helpers are a Wi-SUN extension to RFC 3542; they live here because
 * they manipulate the Traffic Class field of the IPv6 header.
 */
///@{
#define IPV6_TCLASS_DSCP_SHIFT          2
#define IPV6_TCLASS_ECN_MASK            0x03u
/** Six-bit DSCP code point (0-63). */
#define IPV6_DSCP_CODEPOINT_MASK        0x3Fu

/** Traffic Class octet from DSCP code point and ECN Not-ECT */
#define IPV6_TCLASS_FROM_DSCP_AND_ECN(dscp, ecn) \
    ((int)((((unsigned)(dscp) & IPV6_DSCP_CODEPOINT_MASK) << IPV6_TCLASS_DSCP_SHIFT) \
           | ((unsigned)(ecn) & IPV6_TCLASS_ECN_MASK)))

/** Traffic Class octet from DSCP code point (ECN Not-ECT)*/
#define IPV6_TCLASS_FROM_DSCP(dscp) IPV6_TCLASS_FROM_DSCP_AND_ECN((dscp), IP_ECN_NOT_ECT)

/** DSCP code point (0-63) from a full RFC 3542 Traffic Class octet (inverse of #IPV6_TCLASS_FROM_DSCP). */
#define IPV6_DSCP_FROM_TCLASS(tclass) \
    ((int)((((unsigned)(tclass)) >> IPV6_TCLASS_DSCP_SHIFT) & IPV6_DSCP_CODEPOINT_MASK))
///@}

/** @} */

#ifdef __cplusplus
}
#endif

#endif /* NETINET_IP6_H */
