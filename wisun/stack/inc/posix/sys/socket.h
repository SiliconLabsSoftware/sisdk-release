/***************************************************************************//**
 * @file socket.h
 * @brief Main sockets API (POSIX <sys/socket.h>)
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

#ifndef _SYS_SOCKET_H
#define _SYS_SOCKET_H

#ifdef __cplusplus
extern "C" {
 //C++ doesn't provide restrict
#ifdef __GNUC__
#define restrict __restrict
#else
#define restrict
#endif
#endif

#include <stddef.h>
#include <stdint.h>
#include "sl_status.h"
#include "sl_common.h"

#ifndef __ssize_t_defined
typedef int ssize_t;
# define __ssize_t_defined
#endif

/// Socket API error return value
#define SOCKET_RETVAL_ERROR                   (-1L)
/// Socket API OK return value
#define SOCKET_RETVAL_OK                      (0L)
/// Invalid socket ID
#define SOCKET_INVALID_ID                     (SOCKET_RETVAL_ERROR)

/**************************************************************************//**
 * @addtogroup SL_WISUN_SOCKET_API Socket API
 * @ingroup SL_WISUN_API
 *
 * Socket API provides socket-based networking functions for IPv6 connectivity,
 * closely aligning with the POSIX.1-2024 specification.
 *
 * @{
 *****************************************************************************/

/** \name Ancillary data object information MACROS */
///@{
/** \brief Returns the length of the data with the required alignment
 *  \param len The length of the data in bytes
 *  \return The aligned length of the data, rounded up to the nearest multiple of uint32_t
 */
#define CMSG_ALIGN(len) ( ((len) + sizeof(uint32_t) - 1) & (~(sizeof(uint32_t) - 1)) )

/** \brief Returns the number of bytes an ancillary element with payload of the passed data length occupies
 *  \param len The length of the data in bytes
 *  \return The size of the control message structure plus the aligned data length
 */
#define CMSG_SPACE(len) (sizeof(struct cmsghdr) + CMSG_ALIGN(len))

/** \brief Returns the value to store in the cmsg_len member of the cmsghdr structure
 *  \param len The length of the data in bytes
 *  \return The size of the control message structure plus the data length
 */
#define CMSG_LEN(len) (sizeof(struct cmsghdr) + (len))

/** \brief Returns a pointer to the first control message header in the given msghdr structure
 *  \param mhdr A pointer to a msghdr structure that contains the control message buffer
 *  \return A pointer to the first cmsghdr structure, or NULL if the buffer is empty or invalid
 */
#define CMSG_FIRSTHDR(mhdr)                                     \
        ((mhdr)->msg_controllen >= sizeof(struct cmsghdr) ?     \
        (struct cmsghdr *)(mhdr)->msg_control :                 \
        (struct cmsghdr *) NULL)

/** \brief Returns a pointer to the next control message header in the ancillary data buffer
 *  \param mhdr A pointer to a msghdr structure that contains the control message buffer
 *  \param cmsg A pointer to the current cmsghdr structure
 *  \return A pointer to the next cmsghdr structure, or NULL if there is no more space left in the buffer
 */
#define CMSG_NXTHDR(mhdr, cmsg) cmsg_nxthdr((mhdr), (cmsg))

/** \brief Returns a pointer to the data portion of a cmsghdr
 *  \param cmsg A pointer to a cmsghdr structure
 *  \return A pointer to the data following the cmsghdr, casted to uint8_t *
 */
#define CMSG_DATA(cmsg) ((uint8_t *)(cmsg) + CMSG_ALIGN(sizeof(cmsghdr_t)))
///@}

/** \name Flags we can use with recv(), recvfrom() and recvmsg() */
///@{
#define MSG_TRUNC  0x0001  ///< Normal data truncated, to be used as msg_flags field in the msghdr structure.
#define MSG_CTRUNC 0x0002  ///< Control data truncated, to be used as msg_flags field in the msghdr structure.
#define MSG_PEEK   0x0004  ///< Leave received data in queue, to be used as the flags parameter.
///@}

/** \name Protocol levels used for socket_setsockopt. */
///@{
#define SOL_SOCKET           0   ///< Socket option level
#define SOL_APPLICATION      1   ///< Application socket option level
///@}

/// For backward compatibility
#define APP_LEVEL_SOCKET     SOL_APPLICATION

/** \name Option names for application level */

/** \name application level socket options
 *
 * application level socket options summary
 *
 * | opt_name              | data type         | set/get         | sendmsg | recvmsg |
 * | :-------------------: | :---------- ----: | :-------------: | :-----: | :-------|
 * | SO_EVENT_MODE         | uint32_t          |     Set only    |   No    | Yes     |
 * | SO_NONBLOCK           | uint32_t          |     Set only    |   Yes   | Yes     |
 */

///@{
/// Specify event mode of a socket.
/// When set, optval must point to an uint32_t.
///
/// Possible values are:
/// - #SL_WISUN_SOCKET_EVENT_MODE_INDICATION: received data is included in
///   SL_WISUN_MSG_SOCKET_DATA_IND_ID indication
///
/// - #SL_WISUN_SOCKET_EVENT_MODE_POLLING: only the amount of received data is
///   included #SL_WISUN_MSG_SOCKET_DATA_AVAILABLE_IND_ID indication. recv() or
///   recvfrom() shouldbe invoked after indication reception to retrieve data
#define SO_EVENT_MODE           10
#define SOCKET_EVENT_MODE       SO_EVENT_MODE

/// Enable/disable nonblocking mode.
/// This option takes an uint32_t value.
///
/// Possible values are:
///   - (1) enables nonblocking mode
///   - (0) disables nonblocking mode
#define   SO_NONBLOCK             11
///@}

/** \name Option names for socket level. */

/** \name socket level options
 *
 * socket level options summary
 *
 * | opt_name                | data type         | set/get         | sendmsg | recvmsg |
 * | :---------------------: | :---------- ----: | :-------------: | :-----: | :-------|
 * | SO_RCVBUF               | int32_t           |     Set/Get     |   No    | Yes     |
 * | SO_SNDBUF               | int32_t           |     Set/Get     |   Yes   | No      |
 * | SO_REUSEADDR            | int32_t           |     Set/Get     |   No    | No      |
 * | SO_SNDLOWAT             | int32_t           |     Set/Get     |   Yes   | No      |
 * | SO_WRITABLE             | int32_t           |     Get         |   No    | No      |
 * | SO_READABLE             | int32_t           |     Get         |   No    | No      |
 */

///@{
/// Specify receive buffer size in payload bytes.
/// When set, optval must point to an int32_t.
///
/// 0 means unread data are dropped, unless read in data callback.
#define SO_RCVBUF                    1

/// Specify send buffer size in payload bytes.
/// When set, optval must point to an int32_t.
///
/// Used only for stream sockets.
#define SO_SNDBUF                    2

/// Allow reuse of local addresses on bind().
/// When set, optval must point to an int32_t. Defaults to 0 (disabled).
///
/// Must be set before bind().
///
/// Behavior follows the table below
/// (socketA is already bound, socketB is calling bind() and SO_REUSEADDR is set for this latter one):
///
///     socketA (bound)     socketB (binding)   SO_REUSEADDR   Result
///     ----------------------------------------------------------------
///     [2001:db8::1]:21    [2001:db8::1]:21    ON / OFF       EADDRINUSE
///     [2001:db8::1]:21    [2001:db8::2]:21    ON / OFF       OK
///     [::]:21             [2001:db8::1]:21    OFF            EADDRINUSE
///     [2001:db8::1]:21    [::]:21             OFF            EADDRINUSE
///     [::]:21             [2001:db8::1]:21    ON             OK
///     [2001:db8::1]:21    [::]:21             ON             OK
///     [::]:21             [::]:21             ON / OFF       EADDRINUSE
///
/// For TCP, a socket in TIME_WAIT does not prevent bind() when SO_REUSEADDR is enabled.
#define SO_REUSEADDR                 3

/// Specify send low water mark in payload bytes.
/// When set, optval must point to an int32_t.
#define SO_SNDLOWAT                  4

/**
 * @brief Non-standard POSIX option SO_WRITABLE.
 *
 * This option returns a non-zero value (amount of free space in bytes) if the socket is writable.
 *
 * A socket is considered writable if:
 *  The number of bytes of available space in the socket send buffer is greater than or equal the current size
 *  of the send low-water mark and either:
 *    The socket is connected (TCP).
 *    The socket does not require a connection (e.g., UDP).
 *
 * @return Non-zero value (amount of free space in bytes) if the socket is readable, 0 otherwise.
 */
#define SO_WRITABLE     5

/**
 * @brief Non-standard POSIX option SO_READABLE.
 *
 * This option returns a non-zero value (amount of available bytes) if the socket is readable.
 * A socket is considered readable under the following conditions:
 *
 *   The number of bytes of data in the socket receive buffer is greater than or equal to the current size
 *   of the recv low-water mark. The default is 1 for TCP and UDP.
 *   The read half of the connection is closed (i.e., a TCP connection that has received a FIN).
 *   The socket is a listening socket and the number of completed connections is nonzero.
 *
 * @return Non-zero value (amount of data in bytes) if the socket is readable, 0 otherwise.
 */
#define SO_READABLE      6

///@}

/** \name Socket-level Wi-SUN extensions */
///@{
/// Enable Extended Directed Frame Exchange mode.
/// When set, optval must point to an uint32_t.
/// When set, all data from the socket will be sent using the EDFE mode
/// even if there is a single fragment.
/// Disabled by default.
#define SO_EDFE_MODE              0xfb
#define SOCKET_EDFE_MODE          SO_EDFE_MODE
///@}

/// When bitwise ored with socket's type,
/// it sets the O_NONBLOCK status flag on the opened socket file description
#define SOCK_NONBLOCK 0X00010000

/// Socket address length type definition
typedef uint32_t socklen_t;

/// Address family
typedef uint32_t sa_family_t;

/// Socket id
typedef int sl_wisun_socket_id_t;

/// Enumerations for socket event mode
typedef enum {
  /// SL_WISUN_MSG_SOCKET_DATA_IND_ID is sent to the app with the packet contained in the indication
  SL_WISUN_SOCKET_EVENT_MODE_INDICATION = 0,
  /// SL_WISUN_MSG_SOCKET_DATA_AVAILABLE_IND_ID is sent to the app indicating the amount of data received
  /// recv() or recvfrom() should be invoked after indication reception to retrieve data
  /// This is the default socket event mode option
  SL_WISUN_SOCKET_EVENT_MODE_POLLING    = 1
} sl_wisun_socket_event_mode_t;

/// Supported address families
typedef enum socket_domain {
  AF_INET6 = 0  ///< IP version 6
} sl_socket_domain_t;

/// Socket types
typedef enum socket_type {
  SOCK_INVALID  = 0,  ///< invalid socket type
  SOCK_STREAM   = 1,  ///< stream (connection) socket (TCP)
  SOCK_DGRAM    = 2,  ///< datagram (connectionless) socket (UDP)
  SOCK_RAW      = 3,  ///< raw socket
} sl_socket_type_t;

/// Socket address
struct sockaddr {
  sa_family_t sa_family;    ///< address family, AF_XXXX
  uint8_t     sa_data[26];  ///< 26 bytes of protocol address (IPv6)
};

/// The msghdr structure is used by the recvmsg() and sendmsg() functions.
typedef struct msghdr {
  void          *msg_name;        ///< ptr to socket address structure
  socklen_t      msg_namelen;     ///< size of socket address structure
  struct iovec  *msg_iov;         ///< scatter/gather array
  int            msg_iovlen;      ///< # elements in msg_iov
  void          *msg_control;     ///< ancillary data
  socklen_t      msg_controllen;  ///< ancillary data buffer length
  int            msg_flags;       ///< flags on received message
} msghdr_t;

/// Control messages
typedef struct cmsghdr {
  socklen_t  cmsg_len;    ///< Message length in bytes, including this header
  int        cmsg_level;  ///< originating protocol
  int        cmsg_type;   ///< protocol-specific type
} cmsghdr_t;

/// Structure to store scatter/gather array elements
typedef struct iovec {
    void *iov_base;  ///< Store the base address of a memory region for input or output
    size_t iov_len;  ///< Length of the memory region iov_base points to
} iovec_t;

/**************************************************************************//**
 * Create an endpoint for communication and returns an Id that refers to that
 * endpoint.
 *
 * @param[in] domain Specifies a communication domain. It selects the protocol
 *                   family which will be used for communication. Must be set
 *                   to AF_INET6 (IPv6 network socket)
 * @param[in] type The communication semantics
 *                   It can be:
 *                      - #SOCK_STREAM  - TCP stream socket type
 *                      - #SOCK_DGRAM   - UDP datagram socket type
 *                      - #SOCK_RAW     - Raw Socket type (ICMP)
 * @param[in] protocol Specifies the particular protocol to be used.
 *                   It can be:
 *                      - #IPPROTO_ICMP  - Ping
 *                      - #IPPROTO_IP and IPPROTO_TCP  - TCP stream sockets
 *                      - #IPPROTO_IP and IPPROTO_UDP  - UDP datagram sockets
 * @return The socket's id on success, (-1) on failure.
 *****************************************************************************/
int socket(int domain, int type, int protocol);

/**************************************************************************//**
 * Close a socket.
 *
 * @param[in] sockid socket id
 * @return 0 on success, -1 on failure.
 *
 * Close a socket and remove from the socket handler storage.
 *****************************************************************************/
#ifndef DOXYGEN_SHOULD_SKIP_THIS

int sl_close(int sockid);

#define close(sockid) sl_close(sockid)
#else
int close(int sockid);
#endif
/**************************************************************************//**
 * Bind a name to a socket.
 *
 * @param[in] sockid socket id
 * @param[in] addr address structure ptr
 * @param[in] addrlen address structure size
 * @return 0 on success, -1 on failure.
 *
 * Assigns the address to the socket, referred to by the socket ID, as specified
 * by addr. It is normally necessary to assign a local address using bind()
 * before a #SOCK_STREAM socket may receive connections.
 *****************************************************************************/
int bind(int sockid, const struct sockaddr *addr, socklen_t addrlen);

/**************************************************************************//**
 * Send a message on a socket.
 *
 * @param[in] sockid socket descriptor.
 * @param[in] buff pointer to data buffer to send.
 * @param[in] len length of data buffer to send.
 * @param[in] flags flags to select send options. Ignored in our implementation.
 * @return The number of bytes sent on success, -1 if an error occurred.
 *
 * Preferred with connection-oriented sockets (TCP).
 *****************************************************************************/
ssize_t send(int sockid, const void *buff, size_t len, int flags);

/**************************************************************************//**
 * Send a message to a given address.
 *
 * @param[in] sockid socket descriptor.
 * @param[in] buff pointer to data buffer to send.
 * @param[in] len length of data buffer to send.
 * @param[in] flags flags to select send options. Ignored in our implementation.
 * @param[in] dest_addr pointer to destination address buffer; Required for datagram sockets.
 * @param[in] addr_len length of  destination address buffer.
 * @return The number of bytes sent on success, -1 if an error occurred.
 *
 * Preferred in datagram mode (UDP).
 *****************************************************************************/
ssize_t sendto(int sockid, const void *buff, size_t len,
               int flags, const struct sockaddr *dest_addr, socklen_t addr_len);

/**
 * Send a message through a connection-mode or connectionless-mode socket.
 *
 * @param[in] socket  Specifies the socket file descriptor.
 * @param[in] message Points to a msghdr structure, containing both the
                      destination address and the buffers for the outgoing
                      message.
 * @param[in] flags   Specifies the type of message transmission.
 * @return            The number of bytes received on success, -1 if an error occurred.
 */
ssize_t sendmsg(int socket, const struct msghdr *message, int flags);

/**************************************************************************//**
 * Receive messages from a socket
 *
 * @param[in] sockid descriptor of socket to receive the message from.
 * @param[out] buf pointer to destination data buffer.
 * @param[in] len length of destination data buffer.
 * @param[in] flags flags to select type of message reception. Ignored in our
 *            implementation.
 * @param[in] src_addr pointer to a sockaddr structure in which the sending
 *                     address is to be stored.
 * @param[in] addrlen length of the supplied sockaddr structure.
 * @return The number of bytes received on success, -1 if an error occurred.
 *
 * Receives data on a socket whether or not it is connection-oriented.
 *****************************************************************************/
ssize_t recvfrom(int sockid, void *buf, size_t len, int flags,
                 struct sockaddr *src_addr, socklen_t *addrlen);

/**************************************************************************//**
 * Receive a message from a socket.
 *
 * @param[in] sockid descriptor of socket to receive the message from.
 * @param[out] buf pointer to destination data buffer.
 * @param[in] len length of destination data buffer.
 * @param[in] flags flags to select type of message reception. Ignored in our
 *            implementation.
 * @return The number of bytes received on success, -1 if an error occurred.
 *
 * Should be used for connection-oriented protocol (TCP)
 *****************************************************************************/
ssize_t recv(int sockid, void *buf, size_t len, int flags);

/**************************************************************************//**
 * Receive a message from a socket.
 *
 * @param[in] socket Specifies the socket file descriptor.
 * @param[in,out] message Points to a msghdr structure, containing both the
                          buffer to store the source address and the buffers
                          for the incoming message.
 * @param[in] flags Specifies the type of message reception.
 * @return The number of bytes received on success, -1 if an error occurred.
 *
 * This function is typically used with connectionless-mode sockets because
 * it permits the application to retrieve the source address of received data.
 *****************************************************************************/
ssize_t recvmsg(int socket, struct msghdr *message, int flags);

/**************************************************************************//**
 * Accept a connection on a socket.
 *
 * @param[in] sockid socket descriptor
 * @param[in,out] addr A pointer to sockaddr structure filled in with the address
 *                of the peer (remote) socket. When addr is NULL, nothing is
 *                filled in; in this case, addrlen is not used, and should also
 *                be NULL.
 * @param[in,out] addrlen The caller must initialize it to contain the size (in
 *                bytes) of the structure pointed to by addr. On return it will
 *                contain the actual size of the peer address.
 * @return The socket id of the accepted socket on success, -1 if an error occurred.
 *
 * Used with connection-based socket types (TCP).
 * It extracts the first connection request on the queue of pending connections for the
 * listening socket.
 *****************************************************************************/
int accept(int sockid, struct sockaddr *addr, socklen_t *addrlen);

/**************************************************************************//**
 * Initiate a connection on a socket.
 *
 * @param[in] sockid socket descriptor.
 * @param[in] addr If the socket sockid is of type #SOCK_DGRAM, addr is the address
 *            to which datagrams are sent by default and the only address from
 *            which datagrams are received.
 *            If the socket is of type #SOCK_STREAM, this call attempts to make a
 *            connection to the socket that is bound to the address specified by addr.
 * @param[in] addrlen length of the supplied sockaddr structure.
 * @return 0 on connection or binding success, -1 if an error occurred.
 *
 * Connects the socket referred to by the sockid to the address specified by address.
 *****************************************************************************/
int connect(int sockid, const struct sockaddr *addr, socklen_t addrlen);

/**************************************************************************//**
 * Listen for connections on a socket.
 *
 * @param[in] sockid socket id
 * @param[in] backlog Argument defines the maximum length to
 *                    which the queue of pending connections for sockid may grow.
 *                    Not implemented for Wi-SUN, the connection queue size is always 1
 * @return 0 on success, -1 if an error occurred.
 *
 * Marks the socket referred to by sockid as a passive socket, that is, as a
 * socket that will be used to accept incoming connection requests using accept.
 *****************************************************************************/
int listen(int sockid, int backlog);

/**************************************************************************//**
 * Set socket option designated by optname at a given protocol level to the
 * value pointed by optval.
 * @param[in] sockid socket ID
 * @param[in] level protocol level at which the option resides.
 *                  it could be:
 *                    - #SOL_SOCKET
 *                    - #IPPROTO_IPV6
 *                    - #SOL_APPLICATION
 * @param[in] optname option name.
 *                    it could be:
 *                      - for #SOL_SOCKET level:
 *                          - #SO_RCVBUF
 *                          - #SO_SNDBUF
 *                          - #SO_REUSEADDR
 *                          - #SO_SNDLOWAT
 *                      - for #IPPROTO_IPV6 level:
 *                          - #IPV6_UNICAST_HOPS
 *                          - #IPV6_MULTICAST_HOPS
 *                          - #IPV6_JOIN_GROUP
 *                          - #IPV6_LEAVE_GROUP
 *                          - #SO_EDFE_MODE
 *                      - for #SOL_APPLICATION:
 *                          - #SO_EVENT_MODE
 *                          - #SO_NONBLOCK
 * @param[in] optval Pointer to the socket option new value. The type
 *                   of variable pointed by optval depends level and
 *                   optname values.
 * @param[in] optlen Must be the size of the symbol pointed by optval.
 * @return 0 on success, -1 if an error occurred.
 *
 * This function can set socket properties.
 *****************************************************************************/
int setsockopt(int sockid, int level, int optname,
               const void *optval, socklen_t optlen);

/**************************************************************************//**
 * Get socket option.
 *
 * @param[in] sockid socket descriptor.
 * @param[in] level socket protocol level.
 * @param[in] optname Option name.
 *                    Supported options:
 *                      - for #SOL_SOCKET level:
 *                          - #SO_RCVBUF
 *                          - #SO_SNDBUF
 *                          - #SO_REUSEADDR
 *                          - #SO_SNDLOWAT
 *                      - for #IPPROTO_IPV6 level:
 *                          - #IPV6_UNICAST_HOPS
 *                          - #IPV6_MULTICAST_HOPS
 * @param[out] optval option value structure pointer.
 * @param[in] optlen size of the option value structure.
 * @return 0 on success, -1 if an error occurred.
 *
 * The function gets socket option by optname, and copies option data to optval ptr.
 *****************************************************************************/
int getsockopt(int sockid, int level, int optname,
               void *optval, socklen_t *optlen);

/**************************************************************************//**
 * Retrieves the local address of a socket.
 *
 * @param[in] socket The socket descriptor.
 * @param[out] address A pointer to a `struct sockaddr` where the local address
 *                     information will be stored.
 * @param[in,out] address_len A pointer to a `socklen_t` variable that specifies
 *                            the size of the `address` structure. Upon successful
 *                            completion, it contains the actual size of the address
 *                            data.
 * @return On success, returns zero. On failure, returns -1 and sets `errno`
 *         appropriately.
 *
 * This function retrieves the local address associated with a socket. It populates
 * the provided `address` structure with the local address information.
 *****************************************************************************/
int getsockname(int socket, struct sockaddr *restrict address,
                socklen_t *restrict address_len);

/**************************************************************************//**
 * Get the address of the peer connected to the socket.
 *
 * This function retrieves the address of the peer connected to the specified socket.
 * The peer's address is stored in the provided 'address' structure, and the length
 * of the address is stored in 'address_len'.
 *
 * @param[in] socket The socket file descriptor.
 * @param[out] address A pointer to a sockaddr structure where the peer's address will
 *                     be stored.
 * @param[in,out] address_len A pointer to a socklen_t variable that specifies the size
 *                            of the 'address' structure.
 * @return 0 on success, -1 on failure and sets `errno` appropriately.
 *****************************************************************************/
int getpeername(int socket, struct sockaddr *restrict address,
                socklen_t *restrict address_len);

/** @} */

/**************************************************************************//**
 * Return the next control message header in a message header structure.
 *
 * @param[in] msgh A pointer to a msghdr_t structure that contains the ancillary
 *                 data buffer.
 * @param[in] cmsg A pointer to a cmsghdr_t structure that represents the current
 *                 control message header.
 * @return A pointer to the next control message header, or NULL if there are no
 *         more control messages in the buffer.
 * @see CMSG_FIRSTHDR, CMSG_ALIGN
 *****************************************************************************/
static inline cmsghdr_t *cmsg_nxthdr(const msghdr_t *msgh, cmsghdr_t *cmsg)
{
    uint8_t *start_of_next_header = NULL;
    uint8_t *end_of_next_header = NULL;
    if (!cmsg) {
        return CMSG_FIRSTHDR(msgh);
    }
    start_of_next_header = (uint8_t *)(cmsg) + CMSG_ALIGN(cmsg->cmsg_len);
    end_of_next_header   = start_of_next_header + CMSG_ALIGN(sizeof(cmsghdr_t));
    if (end_of_next_header > (uint8_t *)(msgh->msg_control) + msgh->msg_controllen) {
        return NULL;
    }
    return (cmsghdr_t *) start_of_next_header;
}

#ifdef __cplusplus
}
#endif

#endif /* _SYS_SOCKET_H */
