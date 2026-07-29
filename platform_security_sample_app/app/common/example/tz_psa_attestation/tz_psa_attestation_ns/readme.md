# TrustZone PSA Attestation (Non-secure Application)

## High-Level Overview

Demonstrates how to generate and print PSA Attestation tokens from the Non-secure side, in a TrustZone Non-secure PSA Attestation example using Secure-world PSA Crypto and Attestation services.

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This is the **Non-secure** half of the TrustZone PSA Attestation example. It must be built as part of the `tz_psa_attestation_ws` workspace alongside `tz_psa_attestation_s` (the Secure half) — see [`../readme.md`](../readme.md) for the workspace overview, Secure-side architecture, and Secure Boot signing flow.

On startup the Non-secure application:

1. Initializes the kit's clocks, IOStream/VCOM, and the Non-secure side of PSA Crypto.
2. Requests a PSA Initial Attestation Token from the Secure world by calling the attestation veneer published through the Non-secure Callable (NSC).
3. Receives the signed token (claims about the device's Secure Boot state, SE firmware version, instance ID, and challenge) back from the Secure side.
4. Prints the token in a human-readable format over VCOM, so the user can inspect each attestation claim.

All of the heavy lifting — key access, signing, claim collection — happens in the Secure world; the Non-secure side only formats and prints the result. Because the attestation key never leaves the Secure world (and is rooted in Secure Boot OTP keys), the token is trustworthy even if the Non-secure application is compromised.

### Non-secure-side Configuration

The Non-secure project (`tz_psa_attestation_ns.slcp`) brings in:

- `trustzone_nonsecure` — the TrustZone wrapper that wires NSC calls and starts the Non-secure runtime after the Secure side hands off.
- `tz_secure_key_library` — pulls in the Secure-side veneer headers so the Non-secure code can call `Attestation`, `PSA Crypto`, `PSA ITS`, `SE Manager`, etc., as plain function calls.
- `nvm3_default`, `psa_its`, and `psa_crypto_*` components for the curves used in attestation (`secp192r1`, `secp256r1`, `secp384r1`, `secp521r1`, `curve25519`, and `curve448` on Secure Vault parts).
- `printf`, `iostream_retarget_stdio`, `iostream_recommended_stream` — for the human-readable token dump on VCOM.
- A flash layout that places the Non-secure application at `0x2C000` (immediately after the Secure half), with `memory_flash_size = 0x54000` (336 KB) and `memory_ram_size = 0x5000` (20 KB) starting at `0x20003000` (just after the Secure-side RAM region).
- `SL_BOARD_ENABLE_VCOM = 1` to bring up the board-controller UART bridge for console output.

### Post-build Profile

- `tz_nonsecure_application` — produces the Non-secure half of the image and consumes the Secure-side veneer object (`artifact/trustzone_secure_library.o`). The workspace then runs `tz_application_sign` to combine + sign the two halves.

## Prerequisites / Setup Requirements

### Hardware

- The same Series 2 Secure Vault kit used by the workspace — see [`../readme.md#hardware`](../readme.md#hardware) for the full hardware list and the AEM-switch reminder.

### Software

- The same software requirements as the workspace — see [`../readme.md#software`](../readme.md#software).
- This Non-secure project must be **created and built from the workspace**, not standalone. Studio's project picker exposes the workspace; selecting just this `.slcp` will fail to link because the Secure-side veneer object will not be available.

## Steps to Run Demo

Build and run this project as part of the workspace; see [`../readme.md#steps-to-run-demo`](../readme.md#steps-to-run-demo) for the full Update Firmware → Provision Secure Boot → Create projects → Build Secure → Build Non-secure → Flash combined image → Open VCOM → Run sequence.

The Non-secure project specifically is the one you press **Build** / **Debug** / **Flash** on; the workspace orchestration ensures the Secure half is already built and that the combined image is signed by `tz_application_sign`.

## Troubleshooting

- **Linker errors about `trustzone_secure_library.o` or missing veneers** — the Secure project (`tz_psa_attestation_s`) was not built before this Non-secure project, or its build failed. Build the Secure project first.
- **Attestation veneer call returns `PSA_ERROR_INVALID_SIGNATURE` or `PSA_ERROR_INVALID_ARGUMENT`** — the device's Secure Boot public key does not match `example_signing_key.pem`, or `SECURE_BOOT_ENABLE` is not set in SE OTP. PSA Attestation refuses to operate without a verified Secure Boot chain — see the workspace troubleshooting in [`../readme.md`](../readme.md).
- **Token prints but the contents look wrong** — confirm 115200 baud, 8-N-1, line terminator `None`. Garbled UART output frequently looks like corrupted CBOR/COSE-Sign1 to readers.
- **Stack overflow in Non-secure** — raise the Non-secure project's stack (`SL_STACK_SIZE`) in the project configurator; large attestation tokens (many software-component claims) push usage if you add to the demo.
- **Non-secure project not visible in the Studio picker** — Studio exposes this `.slcp` through the workspace; pick **TrustZone PSA Attestation** from the workspace list and Studio will create both projects together.
- For any issue that isn't Non-secure-specific (Secure Boot provisioning, SE firmware version, programming the radio board, etc.), see [`../readme.md#troubleshooting`](../readme.md#troubleshooting).

## Resources

- [`../readme.md`](../readme.md) — workspace and Secure-side architecture, Secure Boot signing flow.
- [AN1374: Series 2 TrustZone](https://www.silabs.com/documents/public/application-notes/an1374-trustzone.pdf)
- [PSA Attestation API specification (Arm)](https://arm-software.github.io/psa-api/attestation/)
- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).

