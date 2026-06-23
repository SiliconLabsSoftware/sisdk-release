# PSA Crypto AEAD

Demonstrates how to perform AEAD operations (AES-CCM, AES-GCM, ChaCha20-Poly1305) using the PSA Crypto API, with hardware acceleration on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the PSA Crypto API to perform Authenticated Encryption with Associated Data (AEAD) operations on the supported device. The example redirects standard I/O to the kit's VCOM port and, on devices that support it, counts the number of clock cycles spent in each operation and prints the results on the console. Cycle measurement can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is `1`) in the project's preprocessor settings.

### AEAD Algorithms

The following AEAD algorithms are exercised (single-part):

- `PSA_ALG_CCM` — AES-CCM
- `PSA_ALG_GCM` — AES-GCM
- `PSA_ALG_CHACHA20_POLY1305` — ChaCha20-Poly1305 (256-bit key only)

When an algorithm is not implemented in the device's hardware accelerator, PSA Crypto falls back to the Mbed TLS software implementation transparently.

### Key Storage

- Volatile plain key in RAM
- Persistent plain key in [NVM3](https://docs.silabs.com/gecko-platform/latest/driver/api/group-nvm3)
- Volatile wrapped key in RAM (Secure Vault High only)
- Persistent wrapped key in NVM3 (Secure Vault High only)

### Key Sizes

- 128-bit
- 192-bit (not supported on Series 1)
- 256-bit

### Payload Sizes

- `PLAIN_MSG_SIZE / 16`
- `PLAIN_MSG_SIZE / 4`
- `PLAIN_MSG_SIZE`

The default `PLAIN_MSG_SIZE` is `4096` and is defined in `app_psa_crypto_aead.h`.

### PSA Crypto APIs Used

`psa_crypto_init`, `psa_key_attributes_init`, `psa_set_key_type`, `psa_set_key_bits`, `psa_set_key_usage_flags`, `psa_set_key_algorithm`, `psa_set_key_id`, `psa_set_key_lifetime`, `psa_generate_key`, `psa_get_key_attributes`, `psa_get_key_algorithm`, `psa_reset_key_attributes`, `psa_destroy_key`, `psa_generate_random`, `psa_hash_compute`, `psa_hash_compare`, `psa_aead_encrypt`, `psa_aead_decrypt`, `mbedtls_psa_crypto_free`.

### Entropy and PRNG

The example uses CTR-DRBG (from [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/)) as its PRNG. On devices with a TRNG hardware module, the TRNG seeds CTR-DRBG; on devices without a TRNG, the seed comes from [RAIL](https://docs.silabs.com/rail/latest/) or an NV (non-volatile) seed stored in NVM3.

### Buffer Management

`SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** by default to optimize for memory and performance. This is NOT the most secure configuration — it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries, allowing the implementation to skip local copies.

When the macro is disabled, PSA functions make defensive `malloc`/`memcpy`/`free` copies of input and output buffers. This protects against TOCTOU-style data tampering and buffer leakage across trust boundaries at the cost of additional RAM and runtime overhead.

- **Disable** `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` when security is critical and buffers may be shared across trust boundaries.
- **Enable** it for performance-critical applications where buffers are guaranteed to be exclusive.

### Other Notes

- Multi-part AEAD is not exercised by this example.
- Default optimization is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 1 or Series 2 SoC development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK. **Secure Vault High** parts are required to exercise wrapped-key storage; non-Vault parts run the plain-key paths only.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device (both reachable from the Launcher's General Device Information panel).
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- Simplicity Commander (optional, for command-line flashing).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit.
2. **Create the project.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **Platform Security - SoC PSA Crypto AEAD**, and create the project (`psa_crypto_aead`) into your workspace.
3. **(Optional) Tune the example.** Adjust `PLAIN_MSG_SIZE` in `app_psa_crypto_aead.h`, `PERSISTENT_KEY_ID` in `app_process.h`, or the `PSA_CRYPTO_PRINT` / `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` preprocessor defines if you need to change cycle reporting, persistent-key slots, or buffer-copy behaviour.
4. **Build.** Build the project; on success Studio produces the application image.
5. **Flash.** Use **Debug** or **Flash Programmer** in Studio, or flash the `.s37`/`.hex` with Simplicity Commander.
6. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
7. **Run.** Reset the kit; the example iterates over every supported (algorithm × key size × key storage × payload size) combination, prints results and (optionally) cycle counts on the console.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **`psa_generate_key` or `psa_open_key` returns `PSA_ERROR_ALREADY_EXISTS`** — the example's `PERSISTENT_KEY_ID` collides with an existing entry in NVM3. Change `PERSISTENT_KEY_ID` in `app_process.h`, or erase NVM3, and rebuild.
- **Wrapped-key paths return `PSA_ERROR_NOT_SUPPORTED`** — wrapped-key storage requires a **Secure Vault High** part. Run those steps on a Vault-capable device or expect them to be skipped.
- **192-bit key tests are skipped on Series 1** — Series 1 hardware does not support 192-bit AEAD keys; this is expected.
- **ChaCha20-Poly1305 with 128/192-bit key fails** — ChaCha20-Poly1305 is defined only for 256-bit keys; the example will only exercise it at 256 bits.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)
- [Platform Security API Documentation](https://docs.silabs.com/gecko-platform/latest/platform-security/)
- [PSA Crypto API specification (Arm)](https://arm-software.github.io/psa-api/crypto/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).

The example redirects standard I/O to the virtual serial port (VCOM) of the kit. By default, the serial port setting is 115200 bps and 8-N-1 configuration.

Except for the Series 1 Cortex-M0+ device, the example is written in such a way as to count the number of clock cycles spent in different operations. The results are printed on the VCOM serial port console. This feature can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is 1) in the IDE setting (`Preprocessor->Defined symbols`).

## Getting Started

1. Upgrade the kit’s firmware to the latest version (see `Adapter Firmware` under [General Device Information](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-about-the-launcher/welcome-and-device-tabs#general-device-information) in the Simplicity Studio 5 User's Guide).
2. Upgrade the device’s SE firmware to the latest version (see `Secure Firmware` under [General Device Information](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-about-the-launcher/welcome-and-device-tabs#general-device-information) in the Simplicity Studio 5 User's Guide).
3. Open any terminal program and connect to the kit’s VCOM port (if using `Device Console` in Simplicity Studio 5, `Line terminator:` must be set to `None`).
4. Create this platform example project in the Simplicity IDE (see [Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples) in the Simplicity Studio 5 User's Guide).
5. Build the example and download it to the kit (see [Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build) and [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer) in the Simplicity Studio 5 User's Guide).
6. Run the example and follow the instructions shown on the console.

## Additional Information

### Notes

1. The example uses the CTR-DRBG, a pseudo-random number generator (PRNG) included in [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/) to generate the random number. If the example is running on a device that includes a TRNG (True Random Number Generator) hardware module, the TRNG will be used as an entropy source to seed the CTR-DRBG. If the device does not incorporate a TRNG, the example will use [RAIL](https://docs.silabs.com/rail/latest/) or NV (non-volatile) seed (requires NVM3) as the entropy source.
2. If an algorithm is not supported in the hardware accelerator of the selected device, the PSA Crypto will use the software fallback feature in Mbed TLS.
3. The Series 1 devices do not support 192-bit key on AEAD.
4. The multi-part AEAD functions are not supported yet.
5. The default optimization level is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.

### Key Storage

The following key storages are supported in this example:

* Volatile plain key in RAM
* Persistent plain key in [NVM3](https://docs.silabs.com/gecko-platform/3.1/driver/api/group-nvm3)
* Volatile wrapped key in RAM (Secure Vault High only)
* Persistent wrapped key in NVM3 (Secure Vault High only)

### Key Size

The following key sizes are supported in this example:

* 128-bit
* 192-bit
* 256-bit

### Payload Size

The following payload sizes are supported in this example:

* `PLAIN_MSG_SIZE`/16
* `PLAIN_MSG_SIZE`/4
* `PLAIN_MSG_SIZE`

The default `PLAIN_MSG_SIZE` is `4096`, it is defined in `app_psa_crypto_aead.h`.

### AEAD Algorithm

The following AEAD algorithms are supported in this example:

* `PSA_ALG_CCM` (single-part)
* `PSA_ALG_GCM` (single-part)
* `PSA_ALG_CHACHA20_POLY1305` (single-part)

The `PSA_ALG_CHACHA20_POLY1305` can only use a 256-bit key.

### PSA Crypto API

The following PSA Crypto APIs are used in this example:

* `psa_crypto_init`
* `psa_key_attributes_init`
* `psa_set_key_type`
* `psa_set_key_bits`
* `psa_set_key_usage_flags`
* `psa_set_key_algorithm`
* `psa_set_key_id`
* `psa_set_key_lifetime`
* `psa_generate_key`
* `psa_get_key_attributes`
* `psa_get_key_algorithm`
* `psa_reset_key_attributes`
* `psa_destroy_key`
* `psa_generate_random`
* `psa_hash_compute`
* `psa_hash_compare`
* `psa_aead_encrypt`
* `psa_aead_decrypt`
* `mbedtls_psa_crypto_free`

### Buffer Management

By default, the macro `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** in this example to optimize for memory and performance. This is NOT the most secure configuration as it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries. This allows the implementation to avoid making local copies of the buffers, reducing memory usage and allocation overhead, and improving performance.

#### Performance Considerations:
When `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is disabled, additional memory allocations (`malloc` calls) are made to create local copies of input and output buffers. This ensures that the original input data remain unaltered and secure, and that the output buffers (if used for intermediate data) are not touched during the operation which may leak info to an attacker. However, this can lead to:
- **Increased Memory Usage**: Temporary buffers are allocated for each operation.
- **Performance Degradation**: The overhead of `malloc`, `memcpy` and `free` calls can impact performance, especially in memory-constrained environments or during frequent cryptographic operations.

#### Use Case:
- **Disable `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS`**: Recommended for applications where security is critical, and buffers may be shared across trust boundaries.
- **Enable `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS`**: Suitable for performance-critical applications where buffers are guaranteed to be exclusive and not shared.

## Troubleshooting
### Serial Port Settings
Be sure to select the following settings to see the serial output of this example:

* 115200 Baud Rate 
* 8-N-1 configuration
* Line terminator should be set to "None" if using Device Console in Simplicity Studio

### Key ID Change
Make sure to change the `PERSISTENT_KEY_ID` value in `app_process.h` if this key ID had already existed in NVM3.

### Programming the Radio Board
Before programming the radio board mounted on the mainboard, make sure the power supply switch is in the AEM position (right side) as shown below.

![Radio board power supply switch](image/readme_img0.png)

## Resources

[AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS Guide](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)

[Platform Security API Documentation] (https://docs.silabs.com/gecko-platform/4.3/platform-security/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://community.silabs.com/).
