# cpc-spinel-proxy

Proxy that bridges Unix socket spinel interface to CPCd.

## Usage

```
cpc-spinel-proxy -s /path/to/socket -i cpcd_0 -e 12
```

- `-s, --socket PATH` Unix socket path for HAL connection
- `-i, --cpc-instance NAME` CPCd instance
- `-e, --endpoint ID` CPC endpoint (12 for 15.4)
- `--iid N` Secondary-side Spinel IID; enables IID translation
- `--host-iid N` HAL-side Spinel IID for translated frames (default `0`)
- `--iid-list N,N,...` additional secondary-side IIDs to forward to HAL
- `-l, --log-level LEVEL` logging detail: `error`, `info`, `debug`, `dump`, or `trace` (default `info`)

Example translating a non-multipan HAL (`host-iid=0`) to a secondary interface on IID 2, while also accepting broadcasts on IID 0:

```bash
cpc-spinel-proxy -s /data/vendor/hardware/spinel-proxy.sock -i cpcd_0 -e 12 --iid 2 --iid-list 0
```

## Behavior

- **Single HAL client:** The proxy accepts **one** connection on the Unix socket, relays Spinel/CPC traffic until the client disconnects or the process exits.
- **CPC secondary reset:** The transport reconnects to CPCd internally; the proxy **closes** the HAL socket so the client sees disconnect.
- **IID translation:** Disabled by default. When `--iid` is provided, HAL to CPC frames whose header IID matches `--host-iid` are rewritten to `--iid`. CPC to HAL frames are forwarded only when their header IID matches `--iid` or one of `--iid-list`; forwarded frames are rewritten to `--host-iid`.
- **Log levels:** `error` prints only errors, `info` adds lifecycle/session logs, `debug` adds frame sizes and IID policy decisions, `dump` adds Spinel payload hex dumps, and `trace` additionally enables libcpc tracing.
- **Socket permissions:** The listening socket is created with mode `0660`. If the Thread HAL runs as a different user/group, set ownership or permissions in the platform init policy that launches this binary.

## Build

Requires **cpc-daemon** (libcpc) and **MbedTLS** (libmbedtls-dev) as dependencies.

Generate this project with a supported host platform component, such as **OpenThread host ARM64 (Android 15, NDK r27d)**,
and import this generated project into the top level build system.
