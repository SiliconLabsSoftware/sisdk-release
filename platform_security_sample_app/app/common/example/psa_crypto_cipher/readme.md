# PSA Crypto Cipher

Demonstrates how to encrypt and decrypt with unauthenticated ciphers (AES-ECB/CBC/CFB/CTR, ChaCha20) using the PSA Crypto API, with generic and built-in AES-128 keys.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the PSA Crypto API to perform unauthenticated cipher operations on the supported device, exercising AES (ECB/CBC/CFB/CTR) and ChaCha20 across single-part and (where applicable) multi-part flows. Both generic keys (generated or imported at run-time) and a built-in AES-128 key provisioned into SE OTP are demonstrated. The example redirects standard I/O to the kit's VCOM port and, on devices that support it, counts the number of clock cycles spent in each operation and prints the results on the console. Cycle measurement can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is `1`) in the project's preprocessor settings.

### Cipher Algorithms

- `PSA_ALG_ECB_NO_PADDING` — AES-ECB (single-part only)
- `PSA_ALG_CBC_NO_PADDING` — AES-CBC (single-part only)
- `PSA_ALG_CFB` — AES-CFB (single-part and multi-part)
- `PSA_ALG_CTR` — AES-CTR (single-part and multi-part)
- `PSA_ALG_STREAM_CIPHER` — ChaCha20 (single-part and multi-part; **256-bit key only**)

If an algorithm is not implemented in the device's hardware accelerator, PSA Crypto falls back to the Mbed TLS software implementation transparently. On Secure Vault parts the SE only accelerates **one-shot** ChaCha20, so multi-part ChaCha20 runs through the software fallback enabled by the `mbedtls_chachapoly` component (added conditionally in the `.slcp`).

### Key Storage

- Volatile plain key in RAM
- Persistent plain key in [NVM3](https://docs.silabs.com/gecko-platform/latest/driver/api/group-nvm3)
- Volatile wrapped key in RAM (Secure Vault High only)
- Persistent wrapped key in NVM3 (Secure Vault High only)

### Key Sizes

- 128-bit
- 192-bit (not supported on Series 1 unauthenticated ciphers)
- 256-bit

### Payload Sizes

- `PLAIN_MSG_SIZE / 16`
- `PLAIN_MSG_SIZE / 4`
- `PLAIN_MSG_SIZE`

The default `PLAIN_MSG_SIZE` is `4096` and is defined in `app_psa_crypto_cipher.h`.

### Built-in AES-128 Key

On HSE-equipped devices the example can also exercise the **built-in AES-128 key** stored in SE OTP. The default key (`encrypt-unsafe-key.prv`) is shipped with Simplicity Studio at:

*C:\SiliconLabs\SimplicityStudio\v5\developer\adapter_packs\secmgr\scripts\offline


In text form the key bytes are `81a5e21fa15286f1df445c2cc120fa3f`. The default algorithm associated with this built-in key is `PSA_ALG_CTR` (defined in `sli_se_opaque_types.h`).

The key can be provisioned with either:

- the **Platform - SoC SE Manager Key Provisioning** example, or
- **Simplicity Commander** (`commander manufacturing init --aes-key …` — see UG162).

If the built-in AES-128 key has not been provisioned, the example skips the cipher operations that use it.

### PSA Crypto APIs Used

`psa_crypto_init`, `psa_key_attributes_init`, `psa_set_key_type`, `psa_set_key_bits`, `psa_set_key_usage_flags`, `psa_set_key_algorithm`, `psa_set_key_id`, `psa_set_key_lifetime`, `psa_generate_key`, `psa_import_key`, `psa_get_key_attributes`, `psa_get_key_algorithm`, `psa_reset_key_attributes`, `psa_destroy_key`, `psa_generate_random`, `psa_hash_compute`, `psa_hash_compare`, `psa_cipher_operation_init`, `psa_cipher_encrypt_setup`, `psa_cipher_decrypt_setup`, `psa_cipher_generate_iv`, `psa_cipher_set_iv`, `psa_cipher_update`, `psa_cipher_finish`, `mbedtls_psa_crypto_free`.

### Entropy and PRNG

The example uses CTR-DRBG (from [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/)) as its PRNG. On devices with a TRNG hardware module, the TRNG seeds CTR-DRBG; on devices without a TRNG, the seed comes from [RAIL](https://docs.silabs.com/rail/latest/) or an NV (non-volatile) seed stored in NVM3.

### Buffer Management

`SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** by default to optimize for memory and performance. This is NOT the most secure configuration — it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries, allowing the implementation to skip local copies.

When the macro is disabled, PSA functions make defensive `malloc`/`memcpy`/`free` copies of input and output buffers. This protects against TOCTOU-style data tampering and buffer leakage across trust boundaries at the cost of additional RAM and runtime overhead.

- **Disable** `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` when security is critical and buffers may be shared across trust boundaries.
- **Enable** it for performance-critical applications where buffers are guaranteed to be exclusive.

### Other Notes

- Default optimization is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.
- `psa_cipher_set_iv` is exercised for deterministic test vectors; `psa_cipher_generate_iv` is used elsewhere.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 1 or Series 2 SoC development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK. **Secure Vault High** parts are required to exercise wrapped-key storage; **HSE/SEMAILBOX**-equipped parts are required to exercise the built-in AES-128 key. Non-Vault, non-HSE parts run the generic plain-key AES and ChaCha20 paths only.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device.
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- **Simplicity Commander** (required if you want to provision the built-in AES-128 key from the command line; otherwise optional for flashing).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit.
2. **(Optional) Provision the built-in AES-128 key.** On HSE devices, run the **Platform - SoC SE Manager Key Provisioning** example or use Simplicity Commander to write `encrypt-unsafe-key.prv` (or your own key) into SE OTP. Skip this step if you only want to exercise generic keys; the example will detect the missing built-in key and skip those test cases.
3. **Create the project.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **Platform Security - SoC PSA Crypto Cipher**, and create the project (`psa_crypto_cipher`) into your workspace.
4. **(Optional) Tune the example.** Adjust `PLAIN_MSG_SIZE` in `app_psa_crypto_cipher.h`, `PERSISTENT_KEY_ID` in `app_process.h`, or the `PSA_CRYPTO_PRINT` / `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` preprocessor defines if you need to change cycle reporting, persistent-key slots, or buffer-copy behaviour.
5. **Build.** Build the project; on success Studio produces the application image.
6. **Flash.** Use **Debug** or **Flash Programmer** in Studio, or flash the `.s37`/`.hex` with Simplicity Commander.
7. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
8. **Run.** Reset the kit; the example iterates over every supported (algorithm × key size × key storage × payload size) combination, plus the built-in AES-128 path if provisioned, and (optionally) prints cycle counts on the console.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **Built-in AES-128 path is skipped** — the key has not been provisioned into SE OTP, or the device is not HSE-equipped. Provision via the SE Manager Key Provisioning example or Simplicity Commander (`commander manufacturing init …`, see UG162).
- **`psa_open_key(builtin_id)` returns `PSA_ERROR_DOES_NOT_EXIST`** — same root cause as above; the built-in slot is empty.
- **`psa_generate_key` returns `PSA_ERROR_ALREADY_EXISTS`** — `PERSISTENT_KEY_ID` collides with an existing entry in NVM3. Change `PERSISTENT_KEY_ID` in `app_process.h`, or erase NVM3, and rebuild.
- **Wrapped-key paths return `PSA_ERROR_NOT_SUPPORTED`** — wrapped-key storage requires a **Secure Vault High** part.
- **192-bit AES is skipped on Series 1** — Series 1 hardware does not support 192-bit keys for unauthenticated ciphers; this is expected.
- **ChaCha20 with 128/192-bit key fails** — `PSA_ALG_STREAM_CIPHER` (ChaCha20) requires a 256-bit key.
- **Multi-part ChaCha20 fails on Secure Vault parts without `mbedtls_chachapoly`** — the SE only accelerates one-shot ChaCha20. The `.slcp` adds `mbedtls_chachapoly` conditionally on Vault devices; do not remove it or multi-part ChaCha20 will return `PSA_ERROR_NOT_SUPPORTED`.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)
- [AN1222: Production Programming of Series 2 Devices](https://www.silabs.com/documents/public/application-notes/an1222-efr32xg2x-production-programming.pdf)
- [UG162: Simplicity Commander Reference Guide](https://www.silabs.com/documents/public/user-guides/ug162-simplicity-commander-reference-guide.pdf)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
