# PSA Crypto Hash

Demonstrates how to compute message digests with the PSA Crypto Hash API, exercising SHA-1 and SHA-2 (SHA-224/256/384/512) in single-part and multi-part modes.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the PSA Crypto API to perform hash (message-digest) operations on the supported device. For every supported algorithm and payload size the example runs both the **single-part** flow (`psa_hash_compute` / `psa_hash_compare`) and the **multi-part** flow (`psa_hash_setup` → `psa_hash_update` → `psa_hash_finish` / `psa_hash_verify`, plus `psa_hash_clone` to fork a streaming context). The example redirects standard I/O to the kit's VCOM port and, on devices that support it, counts the number of clock cycles spent in each operation and prints the results on the console. Cycle measurement can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is `1`) in the project's preprocessor settings.

### Hash Algorithms

- `PSA_ALG_SHA_1` — single-part and multi-part
- `PSA_ALG_SHA_224` — single-part and multi-part
- `PSA_ALG_SHA_256` — single-part and multi-part
- `PSA_ALG_SHA_384` — single-part and multi-part
- `PSA_ALG_SHA_512` — single-part and multi-part

If an algorithm is not implemented in the device's hardware accelerator, PSA Crypto falls back to the Mbed TLS software implementation transparently.

Note: this example does **not** exercise SHA-3. SHA-3 is not part of the supported component set in this sample.

### Payload Sizes

- `PLAIN_MSG_SIZE / 16`
- `PLAIN_MSG_SIZE / 4`
- `PLAIN_MSG_SIZE`

The default `PLAIN_MSG_SIZE` is `4096` and is defined in `app_process.h`.

### PSA Crypto APIs Used

`psa_crypto_init`, `psa_generate_random`, `psa_hash_compute`, `psa_hash_compare`, `psa_hash_operation_init`, `psa_hash_setup`, `psa_hash_update`, `psa_hash_finish`, `psa_hash_clone`, `psa_hash_verify`, `mbedtls_psa_crypto_free`.

### Entropy and PRNG

`psa_generate_random` is exercised once per run to produce the random plaintext that gets hashed. The example uses CTR-DRBG (from [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/)) as its PRNG. On devices with a TRNG hardware module, the TRNG seeds CTR-DRBG; on devices without a TRNG, the seed comes from [RAIL](https://docs.silabs.com/rail/latest/) or an NV (non-volatile) seed stored in NVM3.

### Buffer Management

`SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** by default to optimize for memory and performance. This is NOT the most secure configuration — it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries, allowing the implementation to skip local copies.

When the macro is disabled, PSA functions make defensive `malloc`/`memcpy`/`free` copies of input and output buffers. This protects against TOCTOU-style data tampering and buffer leakage across trust boundaries at the cost of additional RAM and runtime overhead.

- **Disable** `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` when security is critical and buffers may be shared across trust boundaries.
- **Enable** it for performance-critical applications where buffers are guaranteed to be exclusive.

### Other Notes

- Default optimization is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.
- The example holds no persistent state and does not provision any keys, so no NVM3 cleanup is required between runs.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 1 or Series 2 SoC development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK. All paths exercised by this sample (SHA-1 / SHA-2) work on every supported device; no Secure Vault or HSE-specific functionality is required.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device.
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- Simplicity Commander (optional, for command-line flashing).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit.
2. **Create the project.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **Platform Security - SoC PSA Crypto Hash**, and create the project (`psa_crypto_hash`) into your workspace.
3. **(Optional) Tune the example.** Adjust `PLAIN_MSG_SIZE` in `app_process.h`, or the `PSA_CRYPTO_PRINT` / `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` preprocessor defines if you need to change the payload range, cycle reporting, or buffer-copy behaviour.
4. **Build.** Build the project; on success Studio produces the application image.
5. **Flash.** Use **Debug** or **Flash Programmer** in Studio, or flash the `.s37`/`.hex` with Simplicity Commander.
6. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
7. **Run.** Reset the kit; the example iterates over every (hash algorithm × payload size × single-/multi-part) combination, prints pass/fail for each, and (optionally) prints cycle counts on the console.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **`psa_hash_compute` or `psa_hash_finish` returns `PSA_ERROR_INSUFFICIENT_MEMORY`** — raise `SL_HEAP_SIZE` in the project configurator. The default heap is sufficient for the shipped `PLAIN_MSG_SIZE = 4096`, but larger payloads may exhaust it.
- **`PSA_ERROR_BAD_STATE` from `psa_hash_clone`, `psa_hash_update`, `psa_hash_finish`, or `psa_hash_verify`** — multi-part operations require the operation handle to be in the right state. Check that `psa_hash_setup` succeeded before calling `update`, and that `finish` / `verify` is called only once per setup.
- **Cycle counts look wrong / zero** — confirm `PSA_CRYPTO_PRINT=1` is defined and that the target is not a Cortex-M0+ (Series 1 M0+ has no DWT cycle counter, so cycle reporting is meaningless there).
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)
- [Platform Security API Documentation](https://docs.silabs.com/gecko-platform/latest/platform-security/)
- [PSA Crypto API specification (Arm)](https://arm-software.github.io/psa-api/crypto/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
Before programming the radio board mounted on the mainboard, make sure the power supply switch is in the AEM position (right side) as shown below.

![Radio board power supply switch](image/readme_img0.png)

## Resources

[AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://community.silabs.com/).
