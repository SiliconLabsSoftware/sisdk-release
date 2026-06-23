# PSA Crypto DSA

Demonstrates how to sign and verify with the PSA Crypto digital-signature API (ECDSA and EdDSA), using generic and built-in ECC keys.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the PSA Crypto API to perform ECDSA and EdDSA digital-signature operations on the supported device. For each test case the example generates (or imports) an ECC key pair, signs the hash of a message buffer with the private key, then verifies the signature with the corresponding public key. On HSE-equipped devices the example can also exercise **built-in** asymmetric keys provisioned into SE OTP. The example redirects standard I/O to the kit's VCOM port and, on devices that support it, counts the number of clock cycles spent in each operation and prints the results on the console. Cycle measurement can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is `1`) in the project's preprocessor settings.

### Signature Algorithms

- `PSA_ALG_ECDSA(hash_alg)` — ECDSA with a chosen hash
- `PSA_ALG_ECDSA_ANY` — ECDSA over a pre-computed hash (used with built-in keys)
- `PSA_ALG_PURE_EDDSA` — EdDSA / Ed25519 (HSE only)

### Hash Algorithms

- `PSA_ALG_SHA_1`
- `PSA_ALG_SHA_224`
- `PSA_ALG_SHA_256`
- `PSA_ALG_SHA_384`
- `PSA_ALG_SHA_512`

### Elliptic Curve Keys

**`PSA_ECC_FAMILY_SECP_R1` (ECDSA)**

- SECP192R1 — 192-bit
- SECP256R1 — 256-bit
- SECP384R1 — 384-bit
- SECP521R1 — 521-bit

**`PSA_ECC_FAMILY_TWISTED_EDWARDS` (EdDSA)**

- Ed25519 — 255-bit (HSE only)

### Key Storage

- Volatile plain key in RAM
- Persistent plain key in [NVM3](https://docs.silabs.com/gecko-platform/latest/driver/api/group-nvm3)
- Volatile wrapped key in RAM (Secure Vault High only)
- Persistent wrapped key in NVM3 (Secure Vault High only)

### Payload Sizes

- `MSG_SIZE / 16`
- `MSG_SIZE / 4`
- `MSG_SIZE`

The default `MSG_SIZE` is `4096` and is defined in `app_process.h`.

### Built-in Keys

On HSE-equipped devices the example can exercise three categories of built-in key material:

- **Public sign key** in the SE OTP (HSE only) — verifies signatures produced by the corresponding private root-sign key.
- **Public command key** in the SE OTP (HSE only) — verifies signatures produced by the corresponding private command key.
- **Private device key** in the secure key storage (Secure Vault High only) — signs hashes inside the SE; the public half is exported for verification.

Built-in keys are used **only** with ECDSA over a pre-computed hash (`PSA_ALG_ECDSA_ANY` with `psa_sign_hash` / `psa_verify_hash`). If a public sign or command key has not been provisioned, the example skips the corresponding verification step.

The default private root-sign key (`rootsign-unsafe-privkey.pem`) and private command key (`cmd-unsafe-privkey.pem`) ship with Simplicity Studio at `C:\SiliconLabs\SimplicityStudio\v5\developer\adapter_packs\secmgr\scripts\offline`.

For reference, the public half of `rootsign-unsafe-privkey.pem` is:

- `X = C4AF4AC69AAB9512DB50F7A26AE5B4801183D85417E729A56DA974F4E08A562C`
- `Y = DE6019DEA9411332DC1A743372D170B436238A34597C410EA177024DE20FC819`

And the public half of `cmd-unsafe-privkey.pem` is:

- `X = B1BC6F6FA56640ED522B2EE0F5B3CF7E5D48F60BE8148F0DC08440F0A4E1DCA4`
- `Y = 7C04119ED6A1BE31B7707E5F9D001A659A051003E95E1B936F05C37EA793AD63`

The public sign key or public command key can be provisioned with either the **Platform - SoC SE Manager Key Provisioning** example or **Simplicity Commander** (see UG162). AN1268 documents the device-certificate / private-device-key story end-to-end.

### PSA Crypto APIs Used

`psa_crypto_init`, `psa_generate_random`, `psa_key_attributes_init`, `psa_set_key_type`, `psa_set_key_bits`, `psa_set_key_usage_flags`, `psa_set_key_algorithm`, `psa_set_key_id`, `psa_set_key_lifetime`, `psa_generate_key`, `psa_import_key`, `psa_reset_key_attributes`, `psa_export_public_key`, `psa_sign_hash`, `psa_verify_hash`, `psa_sign_message`, `psa_verify_message`, `psa_destroy_key`, `mbedtls_psa_crypto_free`.

### Entropy and PRNG

The example uses CTR-DRBG (from [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/)) as its PRNG. On devices with a TRNG hardware module, the TRNG seeds CTR-DRBG; on devices without a TRNG, the seed comes from [RAIL](https://docs.silabs.com/rail/latest/) or an NV (non-volatile) seed stored in NVM3.

### Buffer Management

`SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** by default to optimize for memory and performance. This is NOT the most secure configuration — it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries, allowing the implementation to skip local copies.

When the macro is disabled, PSA functions make defensive `malloc`/`memcpy`/`free` copies of input and output buffers. This protects against TOCTOU-style data tampering and buffer leakage across trust boundaries at the cost of additional RAM and runtime overhead.

- **Disable** `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` when security is critical and buffers may be shared across trust boundaries.
- **Enable** it for performance-critical applications where buffers are guaranteed to be exclusive.

### Other Notes

- If an algorithm is not implemented in the device's hardware accelerator, PSA Crypto falls back to the Mbed TLS software implementation transparently — **except** for `Ed25519`, which has no software fallback in PSA Crypto today.
- HSE Secure Vault Mid devices require **SE firmware v1.2.11 or higher** (EFR32xG21) and **v2.1.7 or higher** (other HSE devices) for hardware acceleration on `Ed25519`.
- The `.slcp` ships with `SL_HEAP_SIZE = 4096`; larger curves (`SECP521R1`) can push heap usage close to the limit if you add other code.
- Default optimization is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 1 or Series 2 SoC development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK. **Secure Vault High** is required to exercise wrapped-key storage and the built-in private device key; **HSE/SEMAILBOX**-equipped parts are required to exercise the built-in public sign / command keys and `Ed25519`. Non-Vault, non-HSE parts run the generic plain-key ECDSA paths only.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device (HSE Vault Mid devices: see the version floors under *Other Notes* above).
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- **Simplicity Commander** (required if you want to provision built-in public sign / command keys from the command line; otherwise optional for flashing).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit. HSE Vault Mid users: confirm the SE firmware floor for `Ed25519` listed above.
2. **(Optional) Provision built-in keys.** On HSE devices, run the **Platform - SoC SE Manager Key Provisioning** example or use Simplicity Commander to write the public sign key and / or public command key into SE OTP. Skip this step if you only want to exercise generic keys; the example will detect missing built-in keys and skip those verification cases.
3. **Create the project.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **Platform Security - SoC PSA Crypto DSA**, and create the project (`psa_crypto_dsa`) into your workspace.
4. **(Optional) Tune the example.** Adjust `MSG_SIZE` in `app_process.h`, `PERSISTENT_KEY_ID` in `app_process.h`, `SL_HEAP_SIZE` in the project configurator, or the `PSA_CRYPTO_PRINT` / `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` preprocessor defines if you need to change payload size, persistent-key slots, heap, cycle reporting, or buffer-copy behaviour.
5. **Build.** Build the project; on success Studio produces the application image.
6. **Flash.** Use **Debug** or **Flash Programmer** in Studio, or flash the `.s37`/`.hex` with Simplicity Commander.
7. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
8. **Run.** Reset the kit; the example iterates over every supported (signature algorithm × curve × hash × key storage × payload size) combination, plus built-in-key paths if provisioned, and (optionally) prints cycle counts on the console.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **Built-in public sign / command key verification is skipped** — the corresponding public key has not been provisioned into SE OTP, or the device is not HSE-equipped. Provision via the SE Manager Key Provisioning example or Simplicity Commander (see UG162).
- **`psa_open_key(builtin_id)` returns `PSA_ERROR_DOES_NOT_EXIST`** — same root cause as above; the built-in slot is empty.
- **Built-in-key signature verification fails** — the public key in SE OTP does not match the private key used to sign. If you used a custom private root-sign / command key, provision the matching public key; otherwise, re-flash the default `rootsign-unsafe-privkey.pem` / `cmd-unsafe-privkey.pem` public halves.
- **`psa_generate_key` returns `PSA_ERROR_ALREADY_EXISTS`** — `PERSISTENT_KEY_ID` collides with an existing entry in NVM3. Change `PERSISTENT_KEY_ID` in `app_process.h`, or erase NVM3, and rebuild.
- **Wrapped-key paths return `PSA_ERROR_NOT_SUPPORTED`** — wrapped-key storage requires a **Secure Vault High** part.
- **`Ed25519` returns `PSA_ERROR_NOT_SUPPORTED`** — Ed25519 has no PSA Crypto software fallback and requires an HSE-equipped device. Update SE firmware to the floors listed above if Ed25519 hardware support is missing on HSE Vault Mid.
- **`psa_generate_key` returns `PSA_ERROR_INSUFFICIENT_MEMORY`** — raise `SL_HEAP_SIZE` in the project configurator (defaults to `4096`); `SECP521R1` is the most sensitive.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)
- [AN1268: Authenticating Silicon Labs Devices Using Device Certificates](https://www.silabs.com/documents/public/application-notes/an1268-efr32-secure-identity.pdf)
- [AN1222: Production Programming of Series 2 Devices](https://www.silabs.com/documents/public/application-notes/an1222-efr32xg2x-production-programming.pdf)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
