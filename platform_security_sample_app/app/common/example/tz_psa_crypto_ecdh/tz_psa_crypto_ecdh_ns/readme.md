# TrustZone PSA Crypto ECDH (Non-secure Application)

Demonstrates how to perform ECDH key agreement from the Non-secure side of a TrustZone-split application via the Secure world.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This is the **Non-secure** half of the TrustZone PSA Crypto ECDH example. It must be built as part of the `tz_psa_crypto_ecdh_ws` workspace alongside `tz_psa_crypto_ecdh_s` (the Secure half) — see [`../readme.md`](../readme.md) for the workspace overview, Secure-side architecture, and the curves exercised.

On startup the Non-secure application:

1. Initializes the kit's clocks, IOStream/VCOM, and the Non-secure side of PSA Crypto.
2. Stands up two simulated peers — **client** and **server** — on the same device.
3. For each supported curve, calls the Secure-side PSA Crypto veneer to:
   - Generate a fresh ECC key pair for each peer.
   - Export each peer's public key.
   - Run `psa_raw_key_agreement` with each peer's own private key (held in the Secure world) and the other peer's public key to compute a shared secret.
4. Compares the two computed shared secrets, confirms they are equal, and prints the public keys and the agreed secret to VCOM.

The private keys for both peers live entirely in the Secure world; the Non-secure side only references them by PSA key ID and sees their public counterparts. The key-agreement primitive itself runs in the Secure world through the NSC veneer.

### Non-secure-side Configuration

The Non-secure project (`tz_psa_crypto_ecdh_ns.slcp`) brings in:

- `trustzone_nonsecure` — the TrustZone wrapper that wires NSC calls and starts the Non-secure runtime after the Secure side hands off.
- `tz_secure_key_library` — pulls in the Secure-side veneer headers so the Non-secure code can call `PSA Crypto`, `PSA ITS`, etc., as plain function calls.
- `nvm3_default`, `psa_its`, and `psa_crypto_*` components for the curves exercised — `psa_crypto_ecdh`, `psa_crypto_ecc_secp192r1`, `psa_crypto_ecc_secp256r1`, `psa_crypto_ecc_secp384r1`, `psa_crypto_ecc_secp521r1`, `psa_crypto_ecc_curve25519`, and `psa_crypto_ecc_curve448` (added conditionally on `device_security_vault`).
- `printf`, `iostream_retarget_stdio`, `iostream_recommended_stream` — for the public-key and shared-secret dump on VCOM.
- A flash layout that places the Non-secure application at `0x2C000` (immediately after the Secure half), with `memory_flash_size = 0x54000` (336 KB) and `memory_ram_size = 0x5000` (20 KB) starting at `0x20003000` (just after the Secure-side RAM region).
- `SL_BOARD_ENABLE_VCOM = 1` to bring up the board-controller UART bridge for console output.

### Post-build Profile

- `tz_nonsecure_application` — produces the Non-secure half of the image and consumes the Secure-side veneer object (`artifact/trustzone_secure_library.o`). The workspace then runs `tz_application` to combine the two halves into the final (unsigned) image.

## Prerequisites / Setup Requirements

### Hardware

- The same Series 2 kit used by the workspace — see [`../readme.md#hardware`](../readme.md#hardware) for the full hardware list, the `Curve448` / Secure Vault caveat, and the AEM-switch reminder.

### Software

- The same software requirements as the workspace — see [`../readme.md#software`](../readme.md#software).
- This Non-secure project must be **created and built from the workspace**, not standalone. Studio's project picker exposes the workspace; selecting just this `.slcp` will fail to link because the Secure-side veneer object will not be available.

## Steps to Run Demo

Build and run this project as part of the workspace; see [`../readme.md#steps-to-run-demo`](../readme.md#steps-to-run-demo) for the full Update Firmware → Create projects → Build Secure → Build Non-secure → Flash combined image → Open VCOM → Run sequence.

The Non-secure project specifically is the one you press **Build** / **Debug** / **Flash** on; the workspace orchestration ensures the Secure half is already built and that the two halves are combined by `tz_application`.

## Troubleshooting

- **Linker errors about `trustzone_secure_library.o` or missing veneers** — the Secure project (`tz_psa_crypto_ecdh_s`) was not built before this Non-secure project, or its build failed. Build the Secure project first.
- **`Curve448` path returns `PSA_ERROR_NOT_SUPPORTED`** — `Curve448` is only available on **Secure Vault** parts; the example skips that curve on non-Vault Series 2 parts. This is expected.
- **`Curve25519` fails on HSE Vault Mid** — update SE firmware via the Launcher; older SE firmware on Vault Mid parts lacks hardware acceleration for Curve25519 (the example will still run if PSA Crypto can fall back, but check the SE firmware version first).
- **Client and server shared secrets do not match** — heap exhaustion (silent truncation) or a modification to the key-agreement flow. Make sure `SL_HEAP_SIZE` and the Secure-side stack haven't been lowered, and re-run.
- **`PSA_ERROR_INSUFFICIENT_MEMORY` on `psa_generate_key` or `psa_raw_key_agreement`** — large curves (`secp521r1`, `Curve448`) push heap usage close to the limit. Raise `SL_HEAP_SIZE` on the **Secure** project (where the key-agreement work happens) in the project configurator.
- **Token / output prints in the wrong order or interleaved** — confirm 115200 baud, 8-N-1, line terminator `None`. Some terminals buffer aggressively; switch to Studio's `Device Console` to confirm the device output ordering.
- **Non-secure project not visible in the Studio picker** — Studio exposes this `.slcp` through the workspace; pick **TrustZone PSA Crypto ECDH** from the workspace list and Studio will create both projects together.
- For any issue that isn't Non-secure-specific (SE firmware version, programming the radio board, AEM switch, etc.), see [`../readme.md#troubleshooting`](../readme.md#troubleshooting).

## Resources

- [`../readme.md`](../readme.md) — workspace and Secure-side architecture, curves exercised, post-build flow.
- [AN1374: Series 2 TrustZone](https://www.silabs.com/documents/public/application-notes/an1374-trustzone.pdf)
- [PSA Crypto API specification (Arm)](https://arm-software.github.io/psa-api/crypto/)
- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://community.silabs.com/).
