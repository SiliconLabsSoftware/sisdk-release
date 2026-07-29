# PSA Crypto ECDH

## High-Level Overview

Demonstrates how to perform ECDH key agreement between two peers with the PSA Crypto API, in a platform security SoC example exercising SECP and Montgomery (X25519/X448) curves.

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the PSA Crypto API to perform Elliptic Curve Diffie-Hellman (ECDH) key agreement on the supported device. ECDH is an anonymous key-agreement protocol that lets two parties, each holding an elliptic-curve private/public key pair, establish a shared secret over an insecure channel.

The example simulates two peers — **client** and **server** — on the same device. Each peer:

1. Generates an ECC key pair on a chosen curve.
2. Exports its public key.
3. Calls `psa_raw_key_agreement` with its own private key and the peer's public key to compute a shared secret.

The two computed secrets are then compared to confirm they are equal. The example redirects standard I/O to the kit's VCOM port and, on devices that support it, counts the number of clock cycles spent in each operation and prints the results on the console. Cycle measurement can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is `1`) in the project's preprocessor settings.

Note: this example exercises **raw ECDH** only (`PSA_ALG_ECDH` via `psa_raw_key_agreement`). The combined `PSA_ALG_KEY_AGREEMENT(PSA_ALG_ECDH, PSA_ALG_HKDF(hash_alg))` flow that derives a usable key from the shared secret is covered by the separate **PSA Crypto KDF** example.

### Elliptic Curve Keys

**`PSA_ECC_FAMILY_SECP_R1`**

- SECP192R1 — 192-bit
- SECP256R1 — 256-bit
- SECP384R1 — 384-bit
- SECP521R1 — 521-bit

**`PSA_ECC_FAMILY_MONTGOMERY`**

- CURVE25519 (X25519) — 255-bit
- CURVE448 (X448) — 448-bit (Secure Vault High only)

### Key Agreement Algorithm

- `PSA_ALG_ECDH` — raw ECDH key agreement (returns the shared secret directly).

### Key Storage

- Volatile plain key in RAM
- Persistent plain key in [NVM3](https://docs.silabs.com/gecko-platform/latest/driver/api/group-nvm3)
- Volatile wrapped key in RAM (Secure Vault High only)
- Persistent wrapped key in NVM3 (Secure Vault High only)

### PSA Crypto APIs Used

`psa_crypto_init`, `psa_key_attributes_init`, `psa_set_key_type`, `psa_set_key_bits`, `psa_set_key_usage_flags`, `psa_set_key_algorithm`, `psa_set_key_id`, `psa_set_key_lifetime`, `psa_generate_key`, `psa_reset_key_attributes`, `psa_export_public_key`, `psa_raw_key_agreement`, `psa_destroy_key`, `mbedtls_psa_crypto_free`.

### Entropy and PRNG

The example uses CTR-DRBG (from [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/)) as its PRNG. On devices with a TRNG hardware module, the TRNG seeds CTR-DRBG; on devices without a TRNG, the seed comes from [RAIL](https://docs.silabs.com/rail/latest/) or an NV (non-volatile) seed stored in NVM3.

### Buffer Management

`SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** by default to optimize for memory and performance. This is NOT the most secure configuration — it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries, allowing the implementation to skip local copies.

When the macro is disabled, PSA functions make defensive `malloc`/`memcpy`/`free` copies of input and output buffers. This protects against TOCTOU-style data tampering and buffer leakage across trust boundaries at the cost of additional RAM and runtime overhead.

- **Disable** `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` when security is critical and buffers may be shared across trust boundaries.
- **Enable** it for performance-critical applications where buffers are guaranteed to be exclusive.

### Other Notes

- If an algorithm is not implemented in the device's hardware accelerator, PSA Crypto falls back to the Mbed TLS software implementation transparently — **except** for `CURVE448`, which has no software fallback in PSA Crypto today.
- HSE Secure Vault Mid devices require **SE firmware v1.2.11 or higher** (EFR32xG21) and **v2.1.7 or higher** (other HSE devices) for hardware acceleration on `CURVE25519`.
- The `.slcp` ships with `SL_HEAP_SIZE = 4096`; larger curves (`SECP521R1`, `CURVE448`) push heap usage close to the limit if you add other code.
- Default optimization is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 1 or Series 2 SoC development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK. **Secure Vault High** is required to exercise wrapped-key storage and `CURVE448`; non-Vault parts run the SECP and `CURVE25519` paths only.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device (HSE Vault Mid devices: see the version floors under *Other Notes* above for `CURVE25519` hardware acceleration).
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- Simplicity Commander (optional, for command-line flashing).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit. HSE Vault Mid users: confirm the SE firmware floor for `CURVE25519` listed above.
2. **Create the project.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **Platform Security - SoC PSA Crypto ECDH**, and create the project (`psa_crypto_ecdh`) into your workspace.
3. **(Optional) Tune the example.** Adjust `CLIENT_KEY_ID` / `SERVER_KEY_ID` in `app_process.h`, `SL_HEAP_SIZE` in the project configurator, or the `PSA_CRYPTO_PRINT` / `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` preprocessor defines if you need to change persistent-key slots, heap, cycle reporting, or buffer-copy behaviour.
4. **Build.** Build the project; on success Studio produces the application image.
5. **Flash.** Use **Debug** or **Flash Programmer** in Studio, or flash the `.s37`/`.hex` with Simplicity Commander.
6. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
7. **Run.** Reset the kit; the example iterates over every supported (curve × key storage) combination for both peers, prints the public keys and shared-secret comparison result, and (optionally) prints cycle counts on the console.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **`psa_generate_key` returns `PSA_ERROR_ALREADY_EXISTS`** — `CLIENT_KEY_ID` or `SERVER_KEY_ID` in `app_process.h` collides with an existing entry in NVM3. Change one or both IDs, or erase NVM3, and rebuild.
- **Wrapped-key paths return `PSA_ERROR_NOT_SUPPORTED`** — wrapped-key storage requires a **Secure Vault High** part. Run those steps on a Vault-capable device or expect them to be skipped.
- **`CURVE448` returns `PSA_ERROR_NOT_SUPPORTED`** — `CURVE448` has no PSA Crypto software fallback and is only available on Secure Vault parts; the `.slcp` adds `psa_crypto_ecc_curve448` conditionally on `device_security_vault`.
- **`CURVE25519` fails on HSE Vault Mid** — update SE firmware to the minimum versions listed under *Other Notes* and rerun.
- **`psa_generate_key` returns `PSA_ERROR_INSUFFICIENT_MEMORY`** — raise `SL_HEAP_SIZE` in the project configurator (defaults to `4096`); `SECP521R1` and `CURVE448` are the most sensitive.
- **Client and server shared secrets do not match** — this should not happen in a clean run; if it does, suspect heap exhaustion (silent truncation) or a custom modification to the key-agreement flow. Run with `PSA_CRYPTO_PRINT=1` to inspect each operation.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)
- [Platform Security API Documentation](https://docs.silabs.com/gecko-platform/latest/platform-security/)
- [PSA Crypto API specification (Arm)](https://arm-software.github.io/psa-api/crypto/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
