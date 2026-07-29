# PSA Crypto KDF

## High-Level Overview

Demonstrates how to derive keys with the PSA Crypto HKDF API, in a platform security SoC example optionally chained with ECDH key agreement, producing AES, ChaCha20, HMAC, and other derived keys.

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the PSA Crypto API to perform Key Derivation Function (KDF) operations on the supported device. A KDF is a cryptographic primitive that derives one or more secret keys from a high-entropy secret value — a master key, a password, a passphrase, or the output of a key-agreement step — through a pseudo-random function. KDFs are typically used to stretch a key into multiple sub-keys, to fit a required output format (for example, mapping an ECDH shared secret to an AES key), or to bind a derived key to a particular usage policy.

The example exercises:

- **Straight HKDF** — a base key is loaded and HKDF is applied to produce a derived key of the chosen size and intended algorithm.
- **ECDH-chained HKDF** — `PSA_ALG_KEY_AGREEMENT(PSA_ALG_ECDH, PSA_ALG_HKDF(hash_alg))` runs ECDH on SECP256R1 first, then feeds the shared secret into HKDF to produce the derived key.

The example redirects standard I/O to the kit's VCOM port and, on devices that support it, counts the number of clock cycles spent in each operation and prints the results on the console. Cycle measurement can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is `1`) in the project's preprocessor settings.

### Key Derivation Algorithms

- `PSA_ALG_HKDF(hash_alg)` — HKDF based on the selected HMAC hash.
- `PSA_ALG_KEY_AGREEMENT(PSA_ALG_ECDH, PSA_ALG_HKDF(hash_alg))` — ECDH key agreement (SECP256R1) chained into HKDF. This algorithm does **not** apply to wrapped keys.

### HKDF Hash Algorithms

- `PSA_ALG_SHA_1`
- `PSA_ALG_SHA_224`
- `PSA_ALG_SHA_256`
- `PSA_ALG_SHA_384`
- `PSA_ALG_SHA_512`

### Derived Key Sizes

- 128-bit
- 192-bit
- 256-bit

### Derived Key Algorithms

- `PSA_ALG_ECB_NO_PADDING`
- `PSA_ALG_CBC_NO_PADDING`
- `PSA_ALG_CFB`
- `PSA_ALG_CTR` (default; defined in `app_process.h`)
- `PSA_ALG_CCM`
- `PSA_ALG_GCM`
- `PSA_ALG_STREAM_CIPHER` (ChaCha20 — 256-bit key only)
- `PSA_ALG_CHACHA20_POLY1305` (256-bit key only)
- `PSA_ALG_CMAC`
- `PSA_ALG_HMAC(hash_alg)`
- `PSA_ALG_HKDF(hash_alg)`

### Key Storage

- Volatile plain key in RAM
- Persistent plain key in [NVM3](https://docs.silabs.com/gecko-platform/latest/driver/api/group-nvm3)
- Volatile wrapped key in RAM (Secure Vault High only)
- Persistent wrapped key in NVM3 (Secure Vault High only)

For wrapped-key derivation, the example uses the Silicon Labs custom API `sl_psa_key_derivation_single_shot()`. The combined `PSA_ALG_KEY_AGREEMENT` algorithm cannot be used with wrapped keys.

### PSA Crypto APIs Used

`psa_crypto_init`, `psa_key_attributes_init`, `psa_set_key_type`, `psa_set_key_bits`, `psa_set_key_usage_flags`, `psa_set_key_algorithm`, `psa_set_key_id`, `psa_set_key_lifetime`, `psa_import_key`, `psa_key_derivation_output_key`, `psa_export_key`, `psa_get_key_attributes`, `psa_get_key_algorithm`, `psa_reset_key_attributes`, `psa_destroy_key`, `psa_key_derivation_operation_init`, `psa_key_derivation_setup`, `psa_key_derivation_set_capacity`, `psa_key_derivation_input_bytes`, `psa_key_derivation_input_key`, `psa_key_derivation_key_agreement`, `psa_key_derivation_abort`, `sl_psa_key_derivation_single_shot` (Silicon Labs custom), `mbedtls_psa_crypto_free`.

### Entropy and PRNG

The example uses CTR-DRBG (from [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/)) as its PRNG. On devices with a TRNG hardware module, the TRNG seeds CTR-DRBG; on devices without a TRNG, the seed comes from [RAIL](https://docs.silabs.com/rail/latest/) or an NV (non-volatile) seed stored in NVM3.

### Buffer Management

`SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** by default to optimize for memory and performance. This is NOT the most secure configuration — it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries, allowing the implementation to skip local copies.

When the macro is disabled, PSA functions make defensive `malloc`/`memcpy`/`free` copies of input and output buffers. This protects against TOCTOU-style data tampering and buffer leakage across trust boundaries at the cost of additional RAM and runtime overhead.

- **Disable** `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` when security is critical and buffers may be shared across trust boundaries.
- **Enable** it for performance-critical applications where buffers are guaranteed to be exclusive.

### Other Notes

- If an algorithm is not implemented in the device's hardware accelerator, PSA Crypto falls back to the Mbed TLS software implementation transparently.
- Default optimization is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.
- The `.slcp` carries a hardware tag of `hardware:device:flash:256`, so the project is filtered out for parts with less than **256 KB** of flash. Make sure your target meets that floor.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 1 or Series 2 SoC development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK, with at least **256 KB of flash**. **Secure Vault High** parts are required to exercise wrapped-key storage and the `sl_psa_key_derivation_single_shot()` path; non-Vault parts run the plain-key paths only.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device.
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- Simplicity Commander (optional, for command-line flashing).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit.
2. **Create the project.** In Studio, open the **Example Projects & Demos** picker, select your kit (must have ≥ 256 KB flash), find **Platform Security - SoC PSA Crypto KDF**, and create the project (`psa_crypto_kdf`) into your workspace.
3. **(Optional) Tune the example.** Adjust `BASE_KEY_ID` / `DERIVE_KEY_ID` in `app_process.h`, the default derived-key algorithm in `app_process.h`, or the `PSA_CRYPTO_PRINT` / `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` preprocessor defines if you need to change persistent-key slots, the default derived algorithm, cycle reporting, or buffer-copy behaviour.
4. **Build.** Build the project; on success Studio produces the application image.
5. **Flash.** Use **Debug** or **Flash Programmer** in Studio, or flash the `.s37`/`.hex` with Simplicity Commander.
6. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
7. **Run.** Reset the kit; the example iterates over every supported (KDF algorithm × HKDF hash × derived-key size × derived-key algorithm × key storage) combination — including the ECDH→HKDF chained path on plain keys and the wrapped-key path via `sl_psa_key_derivation_single_shot()` — and (optionally) prints cycle counts on the console.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **Example not visible in the Studio picker for your kit** — the `.slcp` filters on `hardware:device:flash:256`; parts with less than 256 KB of flash are excluded by design.
- **`psa_import_key` returns `PSA_ERROR_ALREADY_EXISTS`** — `BASE_KEY_ID` or `DERIVE_KEY_ID` in `app_process.h` collides with an existing entry in NVM3. Change one or both IDs, or erase NVM3, and rebuild.
- **Wrapped-key paths return `PSA_ERROR_NOT_SUPPORTED`** — wrapped-key storage and `sl_psa_key_derivation_single_shot()` require a **Secure Vault High** part. Plain-key paths still run on non-Vault devices.
- **`psa_key_derivation_key_agreement` fails on wrapped keys** — the `PSA_ALG_KEY_AGREEMENT(PSA_ALG_ECDH, PSA_ALG_HKDF(…))` algorithm does not apply to wrapped keys; the example will skip those combinations on Vault devices.
- **ChaCha20 / ChaCha20-Poly1305 with 128/192-bit derived key fails** — these algorithms require a 256-bit derived key.
- **`psa_key_derivation_output_key` returns `PSA_ERROR_INSUFFICIENT_DATA`** — the derivation operation was not fed with enough input bytes; check that `psa_key_derivation_input_bytes` / `psa_key_derivation_input_key` was called for `info` and `salt` (HKDF) before requesting the derived key.
- **Heap exhaustion (`PSA_ERROR_INSUFFICIENT_MEMORY`)** — raise `SL_HEAP_SIZE` in the project configurator; the default is set per the Gecko Platform component, but larger derived keys plus the chained ECDH path can push it close to the limit if you extend the example.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)
- [Platform Security API Documentation](https://docs.silabs.com/gecko-platform/latest/platform-security/)
- [PSA Crypto API specification (Arm)](https://arm-software.github.io/psa-api/crypto/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
Before programming the radio board mounted on the mainboard, make sure the power supply switch is in the AEM position (right side) as shown below.

![Radio board power supply switch](image/readme_img0.png)
