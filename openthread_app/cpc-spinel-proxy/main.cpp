/*******************************************************************************
 * @file
 * @brief cpc-spinel-proxy application logic.
 * @details Relays spinel frames between Unix socket and CPCd endpoint.
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

#include "cpc_transport.hpp"
#include "spinel_iid_policy.hpp"

#include <errno.h>
#include <getopt.h>
#include <limits.h>
#include <poll.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>

#define BUF_SIZE 4096
/** Max bytes printed per direction at `dump`/`trace` log levels (remainder summarized). */
#define PAYLOAD_HEX_MAX 256

enum
{
    kOptionHostIid = 1000,
    kOptionIid,
    kOptionIidList,
};

enum class ProxyLogLevel : uint8_t
{
    kError = 0,
    kInfo,
    kDebug,
    kDump,
    kTrace,
};

static bool log_enabled(ProxyLogLevel current, ProxyLogLevel required)
{
    return static_cast<uint8_t>(current) >= static_cast<uint8_t>(required);
}

static const char *log_level_to_string(ProxyLogLevel level)
{
    switch (level)
    {
    case ProxyLogLevel::kError:
        return "error";
    case ProxyLogLevel::kInfo:
        return "info";
    case ProxyLogLevel::kDebug:
        return "debug";
    case ProxyLogLevel::kDump:
        return "dump";
    case ProxyLogLevel::kTrace:
        return "trace";
    }

    return "unknown";
}

static bool parse_log_level(const char *value, ProxyLogLevel *level)
{
    if (value == nullptr)
    {
        return false;
    }

    if (strcmp(value, "error") == 0 || strcmp(value, "0") == 0)
    {
        *level = ProxyLogLevel::kError;
    }
    else if (strcmp(value, "info") == 0 || strcmp(value, "1") == 0)
    {
        *level = ProxyLogLevel::kInfo;
    }
    else if (strcmp(value, "debug") == 0 || strcmp(value, "2") == 0)
    {
        *level = ProxyLogLevel::kDebug;
    }
    else if (strcmp(value, "dump") == 0 || strcmp(value, "3") == 0)
    {
        *level = ProxyLogLevel::kDump;
    }
    else if (strcmp(value, "trace") == 0 || strcmp(value, "4") == 0)
    {
        *level = ProxyLogLevel::kTrace;
    }
    else
    {
        fprintf(stderr, "Invalid --log-level (use error, info, debug, dump, or trace)\n");
        return false;
    }

    return true;
}

static void log_payload(const char *tag, const uint8_t *data, size_t len, ProxyLogLevel log_level)
{
    if (!log_enabled(log_level, ProxyLogLevel::kDebug))
    {
        return;
    }

    if (!log_enabled(log_level, ProxyLogLevel::kDump))
    {
        fprintf(stderr, "%s: %zu bytes\n", tag, len);
        return;
    }

    size_t nshow = len > PAYLOAD_HEX_MAX ? PAYLOAD_HEX_MAX : len;
    fprintf(stderr, "%s: %zu bytes:", tag, len);
    for (size_t i = 0; i < nshow; i++)
    {
        fprintf(stderr, " %02x", data[i]);
    }
    if (len > PAYLOAD_HEX_MAX)
    {
        fprintf(stderr, " ... (+%zu byte%s not shown)\n", len - nshow, (len - nshow) == 1 ? "" : "s");
    }
    else
    {
        fprintf(stderr, "\n");
    }
}

static volatile sig_atomic_t g_running = 1;

static void signal_handler(int sig);

static bool install_signal_handlers(void)
{
    struct sigaction sa;
    struct sigaction sa_pipe;

    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = signal_handler;
    sigemptyset(&sa.sa_mask);

    // Disable SA_RESTART so signal doesn't restart syscall and block until connection completes.
    sa.sa_flags = 0;

    if (sigaction(SIGINT, &sa, nullptr) != 0)
    {
        perror("sigaction(SIGINT)");
        return false;
    }
    if (sigaction(SIGTERM, &sa, nullptr) != 0)
    {
        perror("sigaction(SIGTERM)");
        return false;
    }

    memset(&sa_pipe, 0, sizeof(sa_pipe));
    sa_pipe.sa_handler = SIG_IGN;
    sigemptyset(&sa_pipe.sa_mask);
    sa_pipe.sa_flags = 0;
    if (sigaction(SIGPIPE, &sa_pipe, nullptr) != 0)
    {
        perror("sigaction(SIGPIPE,SIG_IGN)");
        return false;
    }

    return true;
}

static void signal_handler(int sig)
{
    (void)sig;
    g_running = 0;
}

static void usage(const char *prog)
{
    fprintf(stderr,
            "Usage: %s -s PATH -i NAME -e ID [-l LEVEL] "
            "[--iid N [--host-iid N] [--iid-list LIST]]\n",
            prog);
    fprintf(stderr, "  -s, --socket PATH       Unix socket path for HAL connection (required)\n");
    fprintf(stderr, "  -i, --cpc-instance NAME CPCd instance, e.g. cpcd_0 (required)\n");
    fprintf(stderr, "  -e, --endpoint ID       CPC endpoint id 0-255 (required)\n");
    fprintf(stderr, "      --host-iid N        HAL-side Spinel IID when translation is enabled (default 0)\n");
    fprintf(stderr, "      --iid N             Secondary-side Spinel IID; enables IID translation\n");
    fprintf(stderr, "      --iid-list LIST     Additional secondary-side IIDs to forward to HAL, comma-separated\n");
    fprintf(stderr, "  -l, --log-level LEVEL   error, info, debug, dump, or trace (default info)\n");
}

static int create_listen_socket(const char *path)
{
    int                fd;
    struct sockaddr_un addr;

    unlink(path);

    fd = socket(AF_UNIX, SOCK_SEQPACKET, 0);
    if (fd < 0)
    {
        perror("socket");
        return -1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, path, sizeof(addr.sun_path) - 1);

    if (bind(fd, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("bind");
        close(fd);
        return -1;
    }

    if (listen(fd, 1) < 0)
    {
        perror("listen");
        close(fd);
        return -1;
    }

    /* Owner/group read-write only; widen in init scripts if HAL runs as another user. */
    if (chmod(path, 0660) < 0)
    {
        perror("chmod");
    }

    return fd;
}

/**
 * Decide whether to keep listening after accept(2) returned -1.
 * Applies backoff on resource-type errors to avoid a tight spin and log flood.
 *
 * Call immediately after accept() returns -1 (no intervening library calls), so errno still reflects accept.
 *
 * @param[in,out] aFailStreak  consecutive recoverable failures; caller resets to 0 after a successful accept.
 *
 * @return true to continue the accept loop, false to stop (fatal listener state or failure budget exhausted).
 */
static bool should_retry_accept_listen(unsigned int &aFailStreak)
{
    const int accept_err = errno;

    enum : unsigned int
    {
        kFailSleepMs   = 100,
        kFailStreakMax = 100,
    };

    if (accept_err == EINTR)
    {
        return true;
    }

    if (accept_err == EBADF || accept_err == ENOTSOCK)
    {
        errno = accept_err;
        perror("accept");
        return false;
    }

    if (accept_err == ECONNABORTED)
    {
        return true;
    }

    errno = accept_err;
    perror("accept");
    (void)poll(NULL, 0, static_cast<int>(kFailSleepMs));

    if (++aFailStreak >= kFailStreakMax)
    {
        fprintf(stderr, "accept: exceeded %u consecutive failures; giving up\n", kFailStreakMax);
        return false;
    }

    return true;
}

struct ProxyContext
{
    int                   *client_fd_ptr;
    ProxyLogLevel          log_level;
    CpcTransport          *transport;
    const SpinelIidPolicy *iid_policy;
    const char           **session_exit_reason;
};

struct CpcLogContext
{
    ProxyLogLevel log_level;
};

static void CpcTransportLogToStderr(CpcTransportLogLevel aLevel, const char *aMessage, void *aContext)
{
    const char   *tag       = "warn";
    auto         *ctx       = static_cast<CpcLogContext *>(aContext);
    ProxyLogLevel log_level = ctx != nullptr ? ctx->log_level : ProxyLogLevel::kInfo;

    if (aLevel == CpcTransportLogLevel::kCrit)
    {
        tag = "crit";
    }
    else if (!log_enabled(log_level, ProxyLogLevel::kInfo))
    {
        return;
    }

    fprintf(stderr, "cpc-spinel-proxy [CpcTransport,%s]: %s\n", tag, aMessage);
}

static void on_cpc_frame(const uint8_t *frame, uint16_t len, void *ctx)
{
    struct ProxyContext *ctxp         = static_cast<struct ProxyContext *>(ctx);
    int                  fd           = ctxp->client_fd_ptr ? *ctxp->client_fd_ptr : -1;
    uint8_t             *policy_frame = nullptr;
    const uint8_t       *write_buf    = frame;
    if (fd < 0 || len == 0)
    {
        return;
    }

    if (ctxp->iid_policy != nullptr && ctxp->iid_policy->RequiresSecondaryToHostCopy())
    {
        if (len > 0)
        {
            policy_frame = static_cast<uint8_t *>(malloc(len));
            if (policy_frame == nullptr)
            {
                perror("malloc");
                if (ctxp->session_exit_reason != nullptr && *ctxp->session_exit_reason == nullptr)
                {
                    *ctxp->session_exit_reason = "failed to allocate secondary->HAL policy frame";
                }
                close(fd);
                *ctxp->client_fd_ptr = -1;
                return;
            }

            memcpy(policy_frame, frame, len);
            write_buf = policy_frame;
        }

        if (ctxp->iid_policy->HandleSecondaryToHost(policy_frame,
                                                    len,
                                                    log_enabled(ctxp->log_level, ProxyLogLevel::kDebug))
            == SpinelIidPolicy::Action::kDrop)
        {
            free(policy_frame);
            return;
        }
    }

    /* HAL socket is SOCK_SEQPACKET: one write() must deliver exactly one Spinel frame as a single
     * message. Retrying with the remainder after a short write would split one frame into two. */
    ssize_t written;
    do
    {
        written = write(fd, write_buf, len);
    } while (written < 0 && errno == EINTR);

    if (written < 0)
    {
        if (errno == EPIPE || errno == ECONNRESET)
        {
            if (ctxp->session_exit_reason != nullptr && *ctxp->session_exit_reason == nullptr)
            {
                *ctxp->session_exit_reason = "HAL client disconnected while forwarding CPC frame";
            }
        }
        else
        {
            perror("write");
            if (ctxp->session_exit_reason != nullptr && *ctxp->session_exit_reason == nullptr)
            {
                *ctxp->session_exit_reason = "write to HAL socket failed (CPC->HAL)";
            }
        }
        if (ctxp->client_fd_ptr != nullptr && *ctxp->client_fd_ptr >= 0)
        {
            close(*ctxp->client_fd_ptr);
            *ctxp->client_fd_ptr = -1;
        }
        free(policy_frame);
        return;
    }
    if (static_cast<size_t>(written) != static_cast<size_t>(len))
    {
        fprintf(stderr,
                "write: unexpected partial or zero write on SEQPACKET HAL socket (%zd of %u bytes)\n",
                written,
                len);
        if (ctxp->session_exit_reason != nullptr && *ctxp->session_exit_reason == nullptr)
        {
            *ctxp->session_exit_reason = "incomplete write to HAL socket (CPC->HAL)";
        }
        if (ctxp->client_fd_ptr != nullptr && *ctxp->client_fd_ptr >= 0)
        {
            close(*ctxp->client_fd_ptr);
            *ctxp->client_fd_ptr = -1;
        }
        free(policy_frame);
        return;
    }

    log_payload("CPC->HAL", write_buf, len, ctxp->log_level);

    free(policy_frame);
}

static void on_cpc_reset(void *ctx)
{
    struct ProxyContext *ctxp = static_cast<struct ProxyContext *>(ctx);
    if (ctxp == nullptr || ctxp->client_fd_ptr == nullptr)
    {
        return;
    }

    int fd = *ctxp->client_fd_ptr;
    if (fd >= 0)
    {
        close(fd);
        *ctxp->client_fd_ptr = -1;
    }

    if (ctxp->session_exit_reason != nullptr)
    {
        *ctxp->session_exit_reason = "CPC secondary reset (HAL socket closed by proxy)";
    }

    if (log_enabled(ctxp->log_level, ProxyLogLevel::kInfo))
    {
        fprintf(stderr, "cpc-spinel-proxy: CPC secondary reset; HAL session dropped, waiting for next HAL client\n");
    }
}

/**
 * Sends queued client-to-CPC data from @p aBuffer; shortens @p aLength as bytes are accepted.
 *
 * @p aClientFd  Optional pointer to the HAL socket fd; if `Send` runs `CheckAndReconnect`, `on_cpc_reset` may set it
 *               to `-1` while still returning a successful write for this chunk — remaining queued bytes must be
 *               dropped so stale Spinel is not written to a freshly-reset CPC secondary.
 */
static bool sendStoredDataToCpc(uint8_t      *aBuffer,
                                size_t       &aLength,
                                CpcTransport &aTransport,
                                int          *aClientFd,
                                ProxyLogLevel aLogLevel,
                                const char  **aSessionExit)
{
    while (aLength > 0)
    {
        uint16_t chunk = (aLength > static_cast<size_t>(USHRT_MAX)) ? USHRT_MAX : static_cast<uint16_t>(aLength);
        ssize_t  sent  = aTransport.Send(aBuffer, chunk);
        if (sent < 0)
        {
            if (sent == -EAGAIN || sent == -EWOULDBLOCK || sent == -EINVAL || sent == -EINTR)
            {
                return true;
            }
            (void)aTransport.CheckAndClearDisconnectStatus();
            errno = (sent == -1) ? EIO : -static_cast<int>(sent);
            perror("cpc-spinel-proxy: CPC send");
            if (aSessionExit != nullptr)
            {
                *aSessionExit = "CPC send failed (fatal error while sending HAL data)";
            }
            return false;
        }
        if (sent == 0)
        {
            // A return value of zero is undefined behavior. Setting errno to invalid error.
            errno = EINVAL;
            perror("cpc-spinel-proxy: CPC send (invalid zero return)");
            if (aSessionExit != nullptr)
            {
                *aSessionExit = "CPC send returned zero (invalid)";
            }
            return false;
        }
        log_payload("HAL->CPC", aBuffer, static_cast<size_t>(sent), aLogLevel);
        memmove(aBuffer, aBuffer + static_cast<size_t>(sent), aLength - static_cast<size_t>(sent));
        aLength -= static_cast<size_t>(sent);

        // Drop bytes if file descriptor is in process of a reset
        if (aClientFd != nullptr && *aClientFd < 0)
        {
            aLength = 0;
            return true;
        }
    }
    return true;
}

static void run_relay_session(int                    aClientFd,
                              CpcTransport          &aTransport,
                              const SpinelIidPolicy *aIidPolicy,
                              ProxyLogLevel          aLogLevel)
{
    int                 client_fd    = aClientFd;
    const char         *session_exit = nullptr;
    struct ProxyContext ctx          = {&client_fd, aLogLevel, &aTransport, aIidPolicy, &session_exit};
    uint8_t             storedTxBuf[BUF_SIZE];
    size_t              storedTxLen = 0;
    struct pollfd       pfd[2];
    int                 reconnect_status;

    aTransport.SetResetCallback(nullptr, nullptr);
    aTransport.SetReceiveCallback(nullptr, nullptr);
    reconnect_status = aTransport.CheckAndReconnect();
    if (reconnect_status != 0)
    {
        errno = (reconnect_status == -1) ? EIO : -reconnect_status;
        perror("cpc-spinel-proxy: CPC reconnect before session");
        session_exit = "CPC reconnect failed before relay session start";
        goto exit;
    }

    aTransport.SetResetCallback(on_cpc_reset, &ctx);
    aTransport.SetReceiveCallback(on_cpc_frame, &ctx);

    while (g_running && client_fd >= 0)
    {
        int ret;

        pfd[0].fd      = client_fd;
        pfd[0].events  = POLLIN;
        pfd[0].revents = 0;
        pfd[1].fd      = aTransport.GetFd();
        pfd[1].events  = POLLIN;
        if (storedTxLen > 0)
        {
            pfd[1].events |= POLLOUT;
        }
        pfd[1].revents = 0;

        ret = poll(pfd, 2, 100);
        if (ret < 0)
        {
            if (errno == EINTR)
            {
                continue;
            }
            perror("poll");
            if (session_exit == nullptr)
            {
                session_exit = "poll() failed";
            }
            break;
        }

        if (!sendStoredDataToCpc(storedTxBuf, storedTxLen, aTransport, &client_fd, aLogLevel, &session_exit))
        {
            if (session_exit == nullptr)
            {
                session_exit = "CPC send path failed (see errors above)";
            }
            break;
        }

        // Do not read while CPC write incomplete
        if ((client_fd >= 0) && (pfd[0].revents & POLLIN) && (storedTxLen == 0))
        {
            ssize_t n = read(client_fd, storedTxBuf + storedTxLen, BUF_SIZE - storedTxLen);
            if (n <= 0)
            {
                if (n == 0)
                {
                    if (session_exit == nullptr)
                    {
                        session_exit = "HAL client disconnected (read returned EOF)";
                    }
                    break;
                }
                if (errno == EINTR)
                {
                    continue;
                }
                if (errno == ECONNRESET || errno == EPIPE)
                {
                    if (session_exit == nullptr)
                    {
                        session_exit = "HAL client disconnected (connection reset/broken pipe)";
                    }
                    break;
                }
                perror("read");
                if (session_exit == nullptr)
                {
                    session_exit = "HAL socket read error";
                }
                break;
            }

            if (aIidPolicy->HandleHostToSecondary(storedTxBuf,
                                                  static_cast<size_t>(n),
                                                  log_enabled(aLogLevel, ProxyLogLevel::kDebug))
                == SpinelIidPolicy::Action::kDrop)
            {
                storedTxLen = 0;
                continue;
            }

            storedTxLen += static_cast<size_t>(n);
            if (!sendStoredDataToCpc(storedTxBuf, storedTxLen, aTransport, &client_fd, aLogLevel, &session_exit))
            {
                if (session_exit == nullptr)
                {
                    session_exit = "CPC send failed after HAL read (see errors above)";
                }
                break;
            }
        }

        // Always tick CPC transport: a secondary reset may set reconnect pending from libcpc's
        // callback thread; CheckAndReconnect() runs at the start of Process() / Send().
        // Do not gate Process() on POLLIN or a reset with no CPC traffic stalls forever.
        {
            int pr = aTransport.Process();
            if (pr != 0)
            {
                errno = (pr == -1) ? EIO : -pr;
                perror("cpc-spinel-proxy: CPC error");
                if (session_exit == nullptr)
                {
                    session_exit = "CPC transport Process() failed";
                }
                break;
            }
        }
    }

    if (log_enabled(aLogLevel, ProxyLogLevel::kInfo))
    {
        if (session_exit != nullptr)
        {
            fprintf(stderr, "cpc-spinel-proxy: relay session ended: %s\n", session_exit);
        }
        else if (!g_running)
        {
            fprintf(stderr, "cpc-spinel-proxy: relay session ended: signal (SIGINT/SIGTERM)\n");
        }
        else if (client_fd < 0)
        {
            fprintf(stderr, "cpc-spinel-proxy: relay session ended: HAL socket closed (no further detail)\n");
        }
        else
        {
            fprintf(stderr, "cpc-spinel-proxy: relay session ended: exited relay loop (unexpected)\n");
        }
    }

exit:
    // Context points to stack variables in this function; clear callbacks before returning.
    aTransport.SetResetCallback(nullptr, nullptr);
    aTransport.SetReceiveCallback(nullptr, nullptr);

    if (client_fd >= 0)
    {
        close(client_fd);
    }
}

int main(int argc, char *argv[])
{
    const char   *socket_path   = nullptr;
    const char   *cpc_instance  = nullptr;
    int           endpoint_id   = 0;
    bool          have_endpoint = false;
    ProxyLogLevel log_level     = ProxyLogLevel::kInfo;
    bool          have_iid      = false;
    bool          have_iid_opt  = false;

    int                  listen_fd = -1;
    int                  ret;
    PassThroughIidPolicy passthrough_policy;
    TranslationIidPolicy translation_policy;
    SpinelIidPolicy     *iid_policy = &passthrough_policy;

    static struct option long_opts[] = {{"socket", required_argument, 0, 's'},
                                        {"cpc-instance", required_argument, 0, 'i'},
                                        {"endpoint", required_argument, 0, 'e'},
                                        {"host-iid", required_argument, 0, kOptionHostIid},
                                        {"iid", required_argument, 0, kOptionIid},
                                        {"iid-list", required_argument, 0, kOptionIidList},
                                        {"log-level", required_argument, 0, 'l'},
                                        {"help", no_argument, 0, 'h'},
                                        {0, 0, 0, 0}};

    int c;
    while ((c = getopt_long(argc, argv, "s:i:e:l:h", long_opts, NULL)) != -1)
    {
        switch (c)
        {
        case 's':
            socket_path = optarg;
            break;
        case 'i':
            cpc_instance = optarg;
            break;
        case 'e':
        {
            char *end = nullptr;
            long  v   = strtol(optarg, &end, 10);
            if (end == optarg || *end != '\0' || v < 0 || v > 255)
            {
                fprintf(stderr, "Invalid --endpoint (use integer 0-255)\n");
                return 1;
            }
            endpoint_id   = static_cast<int>(v);
            have_endpoint = true;
            break;
        }
        case 'l':
            if (!parse_log_level(optarg, &log_level))
            {
                return 1;
            }
            break;
        case kOptionHostIid:
            have_iid_opt = true;
            if (!translation_policy.SetHostIid(optarg))
            {
                return 1;
            }
            break;
        case kOptionIid:
            have_iid_opt = true;
            have_iid     = true;
            if (!translation_policy.SetIid(optarg))
            {
                return 1;
            }
            break;
        case kOptionIidList:
            have_iid_opt = true;
            if (!translation_policy.SetIidList(optarg))
            {
                return 1;
            }
            break;
        case 'h':
            usage(argv[0]);
            return 0;
        default:
            usage(argv[0]);
            return 1;
        }
    }

    if (socket_path == nullptr || cpc_instance == nullptr || !have_endpoint)
    {
        fprintf(stderr, "Missing required option(s):");
        if (socket_path == nullptr)
        {
            fprintf(stderr, " --socket");
        }
        if (cpc_instance == nullptr)
        {
            fprintf(stderr, " --cpc-instance");
        }
        if (!have_endpoint)
        {
            fprintf(stderr, " --endpoint");
        }
        fprintf(stderr, "\n");
        usage(argv[0]);
        return 1;
    }

    if (have_iid_opt && !have_iid)
    {
        fprintf(stderr, "IID translation options require --iid\n");
        usage(argv[0]);
        return 1;
    }

    if (have_iid)
    {
        translation_policy.Finalize();
        iid_policy = &translation_policy;
    }

    CpcLogContext cpc_log_context = {log_level};
    CpcTransport  transport;
    transport.SetLogHandler(CpcTransportLogToStderr, &cpc_log_context);
    ret =
        transport.Init(cpc_instance, static_cast<uint8_t>(endpoint_id), log_enabled(log_level, ProxyLogLevel::kTrace));
    if (ret != 0)
    {
        fprintf(stderr, "CpcTransport init failed: %d (ensure CPCd is running)\n", ret);
        return 1;
    }

    listen_fd = create_listen_socket(socket_path);
    if (listen_fd < 0)
    {
        return 1;
    }

    if (log_enabled(log_level, ProxyLogLevel::kInfo))
    {
        fprintf(stderr,
                "cpc-spinel-proxy: listening on %s, CPC instance=%s endpoint=%d log-level=%s\n",
                socket_path,
                cpc_instance,
                endpoint_id,
                log_level_to_string(log_level));
    }

    if (log_enabled(log_level, ProxyLogLevel::kInfo))
    {
        iid_policy->LogConfig();
    }

    if (!install_signal_handlers())
    {
        close(listen_fd);
        return 1;
    }

    unsigned int accept_fail_streak = 0;
    int          accept_exit_status = 0;

    while (g_running)
    {
        int client_fd = accept(listen_fd, NULL, NULL);
        if (client_fd < 0)
        {
            if (!should_retry_accept_listen(accept_fail_streak))
            {
                accept_exit_status = 1;
                break;
            }
            continue;
        }

        accept_fail_streak = 0;

        if (log_enabled(log_level, ProxyLogLevel::kInfo))
        {
            fprintf(stderr, "HAL connected, relaying Spinel frames\n");
        }

        run_relay_session(client_fd, transport, iid_policy, log_level);
    }

    close(listen_fd);
    return accept_exit_status;
}
