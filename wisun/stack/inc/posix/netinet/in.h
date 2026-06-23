/***************************************************************************//**
 * @file in.h
 * @brief Internet address family (POSIX <netinet/in.h>)
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

#ifndef NETINET_IN_H
#define NETINET_IN_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include "sys/socket.h"

/**************************************************************************//**
 * @addtogroup SL_WISUN_SOCKET_API Socket API
 * @ingroup SL_WISUN_API
 *
 * @{
 *****************************************************************************/

/// Transport layer port
typedef uint16_t in_port_t;

/// IP protocols (used as `protocol` argument to socket() and as `level`
/// argument to setsockopt()/getsockopt() for protocol-level options).
typedef enum socket_protocol {
  IPPROTO_IP   = 0,    ///< Dummy protocol
  IPPROTO_ICMP = 1,    ///< Internet Control Message Protocol
  IPPROTO_TCP  = 2,    ///< Transmission Control Protocol
  IPPROTO_UDP  = 3,    ///< User Datagram Protocol
  IPPROTO_IPV6 = 41,   ///< IPv6 socket option level
} sl_socket_protocol_t;

/// Size of an IPv6 address
#define IPV6_ADDR_SIZE 16

/// Length of the string form for IPv6
#define INET6_ADDRSTRLEN 46

/// Initialization value for IPv6 wildcard address
#define IN6ADDR_ANY_INIT { { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 } }

/// IPv6 Internet address.
typedef struct in6_addr {
  uint8_t address[IPV6_ADDR_SIZE];  ///< IPv6 address (network byte order)
} in6_addr_t;

/// IPv6 wildcard address
extern const in6_addr_t in6addr_any;

/// IPv6 address format
typedef struct sockaddr_in6 {
    sa_family_t sin6_family;    ///< AF_INET6
    in_port_t   sin6_port;      ///< Transport layer port
    uint32_t    sin6_flowinfo;  ///< IPv6 flow information
    in6_addr_t  sin6_addr;      ///< IPv6 address
    uint32_t    sin6_scope_id;  ///< Scope ID
} sockaddr_in6_t;

/// Structure to store the IPv6 packet information
typedef struct in6_pktinfo {
    in6_addr_t ipi6_addr;     ///< src/dst IPv6 address
    int        ipi6_ifindex;  ///< arrival interface index
} in6_pktinfo_t;

/// Structure to store the IPv6 MTU (Maximum Transmission Unit) information
typedef struct ip6_mtuinfo {
  /// IPv6 address
  struct sockaddr_in6 ip6m_addr;
  /// MTU size
  uint32_t ip6m_mtu;
} ip6_mtuinfo_t;

/// Structure to specify the multicast group and the interface
typedef struct ipv6_mreq {
  /// IPv6 multicast address of group
  struct in6_addr ipv6mr_multiaddr;
  /// Local IPv6 address of interface
  int ipv6mr_ifindex;
} ipv6_mreq_t;

/**  \name IPv6 socket options
 * IPv6 socket options summary
 *
 * | opt_name              | Data type         | set/getsockopt  | sendmsg | recvmsg |
 * | :-------------------: | :---------- ----: | :-------------: | :-----: | :-------|
 * | IPV6_TCLASS           | int               |     Set/Get     |   Yes   | No      |
 * | IPV6_UNICAST_HOPS     | int               |     Set/Get     |   No    | No      |
 * | IPV6_MULTICAST_HOPS   | int               |     Set/Get     |   No    | No      |
 * | IPV6_USE_MIN_MTU      | int               |     Set/Get     |   Yes   | No      |
 * | IPV6_HOPLIMIT         | int               |     None        |   Yes   | Yes     |
 * | IPV6_RECVHOPLIMIT     | int               |     Set/Get     |   No    | No      |
 * | IPV6_MULTICAST_LOOP   | int               |     Set/Get     |   Yes   | No      |
 * | IPV6_JOIN_GROUP       | ipv6_mreq_t       |     Set only    |   No    | No      |
*  | IPV6_ADD_MEMBERSHIP   | ipv6_mreq_t       |     Set only    |   No    | No      |
 * | IPV6_LEAVE_GROUP      | ipv6_mreq_t       |     Set only    |   No    | No      |
 * | IPV6_DROP_MEMBERSHIP  | ipv6_mreq_t       |     Set only    |   No    | No      |
 * | IPV6_PKTINFO          | in6_pktinfo_t     |     None        |   Yes   | Yes     |
 * | IPV6_RCVPKTINFO       | int               |     Set/Get     |   No    | No      |
 * | IPV6_RECVTCLASS       | int               |     Set/Get     |   No    | No      |
 * | IPV6_DONTFRAG         | int               |     Set/Get     |   Yes   | No      |
 */

///@{

/// Sets or reads the full 8-bit IPv6 Traffic Class (RFC 3542 section 6.5), as int.
#define IPV6_TCLASS                  1
/// Set the unicast hop limit for the socket, as int.
/// Valid values 0 and 255, -1 for using the route default.
#define IPV6_UNICAST_HOPS            2
/// Set the multicast hop limit for the socket, as int.
/// Valid values 0 and 255, -1 for using the route default.
#define IPV6_MULTICAST_HOPS          3
/// Specify PMTU preference, as int;
/// Valid values -1 (PMTUD for unicast, default), 0 (PMTUD always), 1 (PMTUD off).
#define IPV6_USE_MIN_MTU             5
/// Ancillary data option on sendmsg()/recvmsg(), value to be used for single ongoing packet, as int;
/// Valid values 0-255, -1 for default
#define IPV6_HOPLIMIT                8
/// Ancillary data option on recvmsg(), specifies hop-limit for the single received ongoing packet, as int;
/// A nonzero value enables the option; a value of 0 disables the option.
#define IPV6_RECVHOPLIMIT           11
/// Specify whether outgoing multicast packets are looped back, as int.
/// A nonzero value enables the option; a value of 0 disables the option.
#define IPV6_MULTICAST_LOOP         14
/// Join a multicast group. Only valid for SOCK_DGRAM or SOCK_RAW sockets.
/// When set, optval is a pointer to a struct ipv6_mreq.
#define IPV6_ADD_MEMBERSHIP         15
#define IPV6_JOIN_GROUP             IPV6_ADD_MEMBERSHIP
/// Leave a multicast group. Only valid for SOCK_DGRAM or SOCK_RAW sockets.
/// When set, optval is a pointer to a struct ipv6_mreq.
#define IPV6_DROP_MEMBERSHIP        16
#define IPV6_LEAVE_GROUP            IPV6_DROP_MEMBERSHIP
/// Specify control messages packet info for recvmsg() as struct in6_pktinfo.
#define IPV6_PKTINFO                 9
/// Set delivery of the IPV6_PKTINFO control message on incoming datagrams, as int.
/// Such control messages contain a struct in6_pktinfo, as per RFC 3542.
/// Allowed only for SOCK_DGRAM or SOCK_RAW sockets.
#define IPV6_RECVPKTINFO            10
/// Enables the application to receive the value of the traffic class field from the IPv6 header, as int;
/// A nonzero value enables the option; a value of 0 disables the option.
#define IPV6_RECVTCLASS             12
/// Specify not to fragment datagrams, as int;
/// For Wi-SUN, direct neighbors can receive frames up to 1504 bytes,
/// while the other nodes can receive frames up to 1280 bytes.
/// 0 (fragment to path MTU). 1 (no fragmentation, TX fails if bigger than PMTU).
#define IPV6_DONTFRAG                6
///@}

/** @} */

#ifdef __cplusplus
}
#endif

#endif /* NETINET_IN_H */
