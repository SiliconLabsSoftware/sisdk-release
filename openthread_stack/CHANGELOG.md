# Fork changelog

Summary of Silicon Labs changes on top of the upstream OpenThread repositories recorded in `upstream-commits`. Paths below are relative to each repository. For the complete diff, see `openthread.patch` and `ot-br-posix.patch`.

## SiSDK 2026.6

NCP Host/NCP OTBR support, receive key validation, LLVM build fixes.

### NCP

Thread 1.4 Host/NCP OTBR support.

> **Known limitation:** DNS forwarding from Thread devices to infrastructure resolvers is not supported when OpenThread runs on the NCP. Silicon Labs adds NCP DNS-SD platform support (browse and resolver operations coordinated between the NCP and the host); this does **not** add a host-side recursive DNS forwarder for Thread clients.

<details>
<summary>Detailed list — NCP changes</summary>

#### NCP TREL and DNS-SD platform

Host-coordinated TREL on the NCP (infrastructure UDP proxy on the host) and NCP-originated DNS-SD browse/resolver handling between the NCP and the host.

**`openthread`**

- `include/openthread/trel.h`
- `src/core/api/trel_api.cpp`
- `src/core/config/trel.h`
- `src/core/crypto/crypto_platform_mbedtls.cpp`
- `src/core/radio/trel_interface.cpp`
- `src/core/radio/trel_interface.hpp`
- `src/core/radio/trel_peer.cpp`
- `src/core/radio/trel_peer.hpp`
- `src/core/radio/trel_peer_discoverer.cpp`
- `src/core/radio/trel_peer_discoverer.hpp`
- `src/lib/spinel/spinel.c`
- `src/lib/spinel/spinel.h`
- `src/lib/spinel/spinel_prop_codec.cpp`
- `src/lib/spinel/spinel_prop_codec.hpp`
- `src/ncp/changed_props_set.cpp`
- `src/ncp/ncp_base.cpp`
- `src/ncp/ncp_base.hpp`
- `src/ncp/ncp_base_dispatcher.cpp`
- `src/ncp/ncp_base_ftd.cpp`
- `src/ncp/ncp_base_mtd.cpp`
- `src/ncp/ncp_config.h`
- `src/ncp/platform/dnssd.cpp`
- `src/ncp/platform/mdns_socket.cpp`
- `src/ncp/platform/trel.cpp`
- `tests/unit/test_spinel_prop_codec.cpp`

**`ot-br-posix`**

- `src/agent/application.cpp`
- `src/agent/application.hpp`
- `src/host/ncp_host.cpp`
- `src/host/ncp_host.hpp`
- `src/host/ncp_spinel.cpp`
- `src/host/ncp_spinel.hpp`
- `src/host/posix/dnssd.hpp`
- `src/host/posix/udp_proxy.cpp`
- `src/mdns/mdns.cpp`
- `src/mdns/mdns_avahi.cpp`
- `src/mdns/mdns_mdnssd.cpp`

#### NCP NAT64 and TAYGA host path

NAT64 prefix manager control on the NCP, favored-prefix notification to the host, and TAYGA dataplane integration (`NAT64_SERVICE=tayga`).

**`openthread`**

- `etc/cmake/options.cmake`
- `include/openthread/platform/border_routing.h`
- `src/core/border_router/routing_manager.cpp`
- `src/core/border_router/routing_manager.hpp`
- `src/core/config/nat64.h`
- `src/core/config/openthread-core-config-check.h`
- `src/lib/spinel/spinel.c`
- `src/lib/spinel/spinel.h`
- `src/ncp/CMakeLists.txt`
- `src/ncp/changed_props_set.cpp`
- `src/ncp/ncp_base.hpp`
- `src/ncp/ncp_base_dispatcher.cpp`
- `src/ncp/ncp_base_ftd.cpp`
- `src/ncp/platform/border_routing.cpp`
- `src/posix/platform/firewall.cpp`
- `src/posix/platform/firewall.hpp`

**`ot-br-posix`**

- `etc/cmake/options.cmake`
- `script/_nat64`
- `script/_otbr`
- `script/bootstrap`
- `src/host/ncp_host.cpp`
- `src/host/ncp_host.hpp`
- `src/host/ncp_spinel.cpp`
- `src/host/ncp_spinel.hpp`
- `src/host/posix/CMakeLists.txt`
- `src/host/posix/firewall_ingress.cpp`
- `src/host/posix/firewall_ingress.hpp`
- `src/host/posix/nat64_tayga_host.cpp`
- `src/host/posix/nat64_tayga_host.hpp`
- `src/host/posix/netif.cpp`
- `src/host/posix/netif.hpp`

#### DHCPv6 prefix delegation on NCP

**`openthread`**

- `src/lib/spinel/spinel.c`
- `src/lib/spinel/spinel.h`
- `src/ncp/ncp_base_dispatcher.cpp`
- `src/ncp/ncp_base_ftd.cpp`

**`ot-br-posix`**

- `src/host/ncp_host.cpp`
- `src/host/ncp_host.hpp`
- `src/host/ncp_spinel.cpp`
- `src/host/ncp_spinel.hpp`
- `src/host/posix/netif.cpp`
- `src/host/posix/netif.hpp`

#### TREL and UDP proxy follow-ups

Certification, reconnect, and infrastructure-interface fixes for the host UDP proxy used by TREL (and shared with other NCP host traffic such as Border Agent).

**`openthread`**

- `src/core/config/trel.h`
- `src/core/radio/trel_interface.cpp`
- `src/core/radio/trel_peer.cpp`
- `src/core/radio/trel_peer.hpp`
- `src/core/radio/trel_peer_discoverer.cpp`
- `src/core/radio/trel_peer_discoverer.hpp`
- `src/ncp/ncp_base_mtd.cpp`
- `src/ncp/platform/trel.cpp`

**`ot-br-posix`**

- `script/_nat64`
- `src/agent/application.cpp`
- `src/agent/application.hpp`
- `src/host/ncp_spinel.cpp`
- `src/host/posix/dnssd.cpp`
- `src/host/posix/dnssd.hpp`
- `src/host/posix/udp_proxy.cpp`
- `src/host/posix/udp_proxy.hpp`

</details>

### Receive key validation

Drop received MAC frames when key material is invalid.

**`openthread`**

<details>
<summary>Detailed list — receive key validation changes</summary>

- `src/core/mac/mac.cpp`

</details>

### LLVM build fixes

Build-system and source updates so the fork compiles cleanly with LLVM-based toolchains.

**`openthread`**

<details>
<summary>Detailed list — LLVM changes</summary>

- `BUILD.gn`
- `etc/gn/toolchain/BUILD.gn`
- `examples/apps/cli/BUILD.gn`
- `examples/platforms/utils/mac_frame.cpp`
- `src/cli/BUILD.gn`
- `src/cli/cli_ping.cpp`
- `src/core/BUILD.gn`
- `src/core/net/srp_client.cpp`
- `src/lib/hdlc/BUILD.gn`
- `src/lib/platform/BUILD.gn`
- `src/lib/spinel/BUILD.gn`
- `src/ncp/BUILD.gn`
- `third_party/mbedtls/BUILD.gn`
- `third_party/tcplp/BUILD.gn`

</details>

---

If your project does not require these additions, use the upstream ancestor commits listed in `upstream-commits` instead of the patched forks.
