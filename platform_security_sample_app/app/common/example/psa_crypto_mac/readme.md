# PSA Crypto MAC

## High-Level Overview

Demonstrates how to compute and verify MACs (HMAC, CMAC) with the PSA Crypto API, in a platform security SoC example in single-part and multi-part modes.

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the PSA Crypto API to perform Message Authentication Code (MAC) operations on the supported device, exercising both **HMAC** (with SHA-1 and the SHA-2 family) and **CMAC** (AES). For each test case the example runs both the **single-part** flow (`psa_mac_compute` / `psa_mac_verify`) and the **multi-part** flow (`psa_mac_sign_setup` / `psa_mac_verify_setup` → `psa_mac_update` → `psa_mac_sign_finish` / `psa_mac_verify_finish`). The example redirects standard I/O to the kit's VCOM port and, on devices that support it, counts the number of clock cycles spent in each operation and prints the results on the console. Cycle measurement can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is `1`) in the project's preprocessor settings.

### MAC Algorithms

- `PSA_ALG_HMAC(hash_alg)` — HMAC with the selected hash (single-part and multi-part)
- `PSA_ALG_CMAC` — AES-CMAC (single-part and multi-part)

If an algorithm is not implemented in the device's hardware accelerator, PSA Crypto falls back to the Mbed TLS software implementation transparently.

### HMAC Hash Algorithms

- `PSA_ALG_SHA_1`
- `PSA_ALG_SHA_224`
- `PSA_ALG_SHA_256`
- `PSA_ALG_SHA_384`
- `PSA_ALG_SHA_512`

### Key Storage

- Volatile plain key in RAM
- Persistent plain key in [NVM3](https://docs.silabs.com/gecko-platform/latest/driver/api/group-nvm3)
- Volatile wrapped key in RAM (Secure Vault High only)
- Persistent wrapped key in NVM3 (Secure Vault High only)

Note: multi-part HMAC (`PSA_ALG_HMAC` streaming via `psa_mac_*_setup` / `update` / `*_finish`) is **not yet supported with wrapped keys** — the example will skip that combination on Vault devices and fall back to single-part HMAC for wrapped keys.

### Key Sizes

- 128-bit
- 192-bit (CMAC: not supported on Series 1)
- 256-bit

### Payload Sizes

- `MSG_SIZE / 16`
- `MSG_SIZE / 4`
- `MSG_SIZE`

The default `MSG_SIZE` is `4096` and is defined in `app_process.h`.

### PSA Crypto APIs Used

`psa_crypto_init`, `psa_key_attributes_init`, `psa_set_key_type`, `psa_set_key_bits`, `psa_set_key_usage_flags`, `psa_set_key_algorithm`, `psa_set_key_id`, `psa_set_key_lifetime`, `psa_generate_key`, `psa_import_key`, `psa_get_key_attributes`, `psa_get_key_algorithm`, `psa_reset_key_attributes`, `psa_destroy_key`, `psa_generate_random`, `psa_mac_compute`, `psa_mac_verify`, `psa_mac_operation_init`, `psa_mac_sign_setup`, `psa_mac_verify_setup`, `psa_mac_update`, `psa_mac_sign_finish`, `psa_mac_verify_finish`.

### Entropy and PRNG

The example uses CTR-DRBG (from [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/)) as its PRNG. On devices with a TRNG hardware module, the TRNG seeds CTR-DRBG; on devices without a TRNG, the seed comes from [RAIL](https://docs.silabs.com/rail/latest/) or an NV (non-volatile) seed stored in NVM3.

### Buffer Management

`SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** by default to optimize for memory and performance. This is NOT the most secure configuration — it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries, allowing the implementation to skip local copies.

When the macro is disabled, PSA functions make defensive `malloc`/`memcpy`/`free` copies of input and output buffers. This protects against TOCTOU-style data tampering and buffer leakage across trust boundaries at the cost of additional RAM and runtime overhead.

- **Disable** `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` when security is critical and buffers may be shared across trust boundaries.
- **Enable** it for performance-critical applications where buffers are guaranteed to be exclusive.

### Other Notes

- Default optimization is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.
- HMAC accepts arbitrary-length keys; the example exercises 128/192/256-bit keys to align with the AES-CMAC key sizes for an apples-to-apples comparison.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 1 or Series 2 SoC development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK. **Secure Vault High** parts are required to exercise wrapped-key storage; non-Vault parts run the plain-key HMAC/CMAC paths only.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device.
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- Simplicity Commander (optional, for command-line flashing).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit.
2. **Create the project.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **Platform Security - SoC PSA Crypto MAC**, and create the project (`psa_crypto_mac`) into your workspace.
3. **(Optional) Tune the example.** Adjust `MSG_SIZE` in `app_process.h`, `PERSISTENT_KEY_ID` in `app_process.h`, or the `PSA_CRYPTO_PRINT` / `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` preprocessor defines if you need to change payload size, persistent-key slots, cycle reporting, or buffer-copy behaviour.
4. **Build.** Build the project; on success Studio produces the application image.
5. **Flash.** Use **Debug** or **Flash Programmer** in Studio, or flash the `.s37`/`.hex` with Simplicity Commander.
6. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
7. **Run.** Reset the kit; the example iterates over every supported (MAC algorithm × hash, where applicable × key size × key storage × payload size × single-/multi-part) combination, prints pass/fail per case, and (optionally) prints cycle counts on the console.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **`psa_generate_key` or `psa_import_key` returns `PSA_ERROR_ALREADY_EXISTS`** — `PERSISTENT_KEY_ID` in `app_process.h` collides with an existing entry in NVM3. Change `PERSISTENT_KEY_ID`, or erase NVM3, and rebuild.
- **Wrapped-key paths return `PSA_ERROR_NOT_SUPPORTED`** — wrapped-key storage requires a **Secure Vault High** part.
- **Multi-part HMAC fails on wrapped keys** — multi-part HMAC with wrapped keys is not yet supported in PSA Crypto; the example is expected to skip that case on Vault devices. Use single-part HMAC (`psa_mac_compute` / `psa_mac_verify`) for wrapped HMAC keys instead.
- **192-bit CMAC is skipped on Series 1** — Series 1 hardware does not support 192-bit AES-CMAC keys; this is expected.
- **`PSA_ERROR_BAD_STATE` from `psa_mac_update`, `psa_mac_sign_finish`, or `psa_mac_verify_finish`** — multi-part MAC operations require the operation handle to be in the right state. Check that the matching `psa_mac_sign_setup` / `psa_mac_verify_setup` succeeded before calling `update`, and that `finish` is paired with the matching `setup` variant.
- **`psa_mac_verify` returns `PSA_ERROR_INVALID_SIGNATURE`** — the MAC value passed to verify does not match what `psa_mac_compute` produced for the same (key, algorithm, message). Confirm that the key, algorithm, and message bytes match exactly between sign and verify.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)
- [Platform Security API Documentation](https://docs.silabs.com/gecko-platform/latest/platform-security/)
- [PSA Crypto API specification (Arm)](https://arm-software.github.io/psa-api/crypto/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
