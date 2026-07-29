# PSA Crypto Symmetric Key

## High-Level Overview

Demonstrates how to generate, import, export, copy, and destroy symmetric keys using the PSA Crypto API, in a platform security SoC example with plain and Secure Vault wrapped key storage.

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the PSA Crypto API to exercise the full symmetric-key **management lifecycle** on the supported device: generate, import, export, copy, and destroy keys, across multiple key types, sizes, storage locations, intended algorithms, and usage policies. The example focuses on key management rather than on running the underlying cipher/MAC/KDF operations themselves — those are covered by the dedicated **PSA Crypto Cipher**, **PSA Crypto MAC**, and **PSA Crypto KDF** examples. The example redirects standard I/O to the kit's VCOM port and, on devices that support it, counts the number of clock cycles spent in each key operation and prints the results on the console. Cycle measurement can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is `1`) in the project's preprocessor settings.

### Key Storage

- Volatile plain key in RAM
- Persistent plain key in [NVM3](https://docs.silabs.com/gecko-platform/latest/driver/api/group-nvm3)
- Volatile wrapped key in RAM (Secure Vault High only)
- Persistent wrapped key in NVM3 (Secure Vault High only)

### Key Sizes

- 128-bit
- 192-bit
- 256-bit

### Key Usage

- `PSA_KEY_USAGE_EXPORT`
- `PSA_KEY_USAGE_COPY`

Note: `PSA_KEY_USAGE_COPY` does **not** apply to wrapped keys — wrapped keys cannot be copied across slots by design, even if the policy bit is set.

### Intended Algorithms

Each generated or imported key is created with an intended algorithm so the example can verify that the policy attribute round-trips correctly through export / copy / destroy. The example selects from:

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

These algorithms are used as **policy attributes** on the key — the example does not run the corresponding cipher/MAC/KDF operations against the keys it manages.

### PSA Crypto APIs Used

`psa_crypto_init`, `psa_key_attributes_init`, `psa_set_key_type`, `psa_set_key_bits`, `psa_set_key_usage_flags`, `psa_set_key_algorithm`, `psa_set_key_id`, `psa_set_key_lifetime`, `psa_generate_key`, `psa_import_key`, `psa_copy_key`, `psa_reset_key_attributes`, `psa_export_key`, `psa_destroy_key`, `mbedtls_psa_crypto_free`.

### Entropy and PRNG

`psa_generate_key` is the only operation that consumes randomness in this sample. The example uses CTR-DRBG (from [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/)) as its PRNG. On devices with a TRNG hardware module, the TRNG seeds CTR-DRBG; on devices without a TRNG, the seed comes from [RAIL](https://docs.silabs.com/rail/latest/) or an NV (non-volatile) seed stored in NVM3.

### Buffer Management

`SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** by default to optimize for memory and performance. This is NOT the most secure configuration — it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries, allowing the implementation to skip local copies.

When the macro is disabled, PSA functions make defensive `malloc`/`memcpy`/`free` copies of input and output buffers. This protects against TOCTOU-style data tampering and buffer leakage across trust boundaries at the cost of additional RAM and runtime overhead.

- **Disable** `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` when security is critical and buffers may be shared across trust boundaries.
- **Enable** it for performance-critical applications where buffers are guaranteed to be exclusive.

### Other Notes

- If an algorithm is not implemented in the device's hardware accelerator, PSA Crypto falls back to the Mbed TLS software implementation transparently. Since this example does not actually run the algorithms, the fallback path is rarely exercised in practice — but the *policy bits* still encode the intended algorithm correctly.
- Default optimization is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 1 or Series 2 SoC development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK. **Secure Vault High** parts are required to exercise wrapped-key storage; non-Vault parts run the plain-key paths only.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device.
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- Simplicity Commander (optional, for command-line flashing).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit.
2. **Create the project.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **Platform Security - SoC PSA Crypto Symmetric Key**, and create the project (`psa_crypto_symmetric_key`) into your workspace.
3. **(Optional) Tune the example.** Adjust `PERSISTENT_KEY_ID` / `PERSISTENT_COPY_KEY_ID` in `app_process.h`, the default intended-algorithm in `app_process.h`, or the `PSA_CRYPTO_PRINT` / `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` preprocessor defines if you need to change persistent-key slots, the default policy attribute, cycle reporting, or buffer-copy behaviour.
4. **Build.** Build the project; on success Studio produces the application image.
5. **Flash.** Use **Debug** or **Flash Programmer** in Studio, or flash the `.s37`/`.hex` with Simplicity Commander.
6. **Open VCOM.** Connect to the kit's symbol VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
7. **Run.** Reset the kit; the example iterates over every supported (key type × key size × intended-algorithm × key storage × key-usage policy) combination, performing generate / import / export / copy / destroy and (optionally) printing cycle counts on the console.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **`psa_generate_key` or `psa_open_key` returns `PSA_ERROR_ALREADY_EXISTS`** — `PERSISTENT_KEY_ID` or `PERSISTENT_COPY_KEY_ID` in `app_process.h` collides with an existing entry in NVM3. Change one or both IDs, or erase NVM3, and rebuild.
- **Wrapped-key paths return `PSA_ERROR_NOT_SUPPORTED`** — wrapped-key storage requires a **Secure Vault High** part.
- **`psa_copy_key` of a wrapped key returns `PSA_ERROR_NOT_PERMITTED`** — `PSA_KEY_USAGE_COPY` does not apply to wrapped keys; this is expected.
- **`psa_export_key` of a wrapped key returns `PSA_ERROR_NOT_PERMITTED`** — wrapped keys are not exportable in cleartext. Set the policy on a plain-key slot if you need to export the key material.
- **ChaCha20 / ChaCha20-Poly1305 with 128/192-bit key fails** — `PSA_ALG_STREAM_CIPHER` (ChaCha20) and `PSA_ALG_CHACHA20_POLY1305` require a 256-bit key.
- **`psa_copy_key` fails with `PSA_ERROR_INVALID_ARGUMENT`** — the source key was not created with `PSA_KEY_USAGE_COPY`, or the target attributes are incompatible with the source policy. Verify that the source key was generated/imported with `PSA_KEY_USAGE_COPY` and that the target's intended algorithm is the same as (or a strict subset of) the source's.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)
- [Platform Security API Documentation](https://docs.silabs.com/gecko-platform/latest/platform-security/)
- [PSA Crypto API specification (Arm)](https://arm-software.github.io/psa-api/crypto/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
