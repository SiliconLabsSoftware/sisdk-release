# PSA Crypto X.509

## High-Level Overview

Demonstrates how to create CSRs, build a root-and-device X.509 certificate chain, and verify it with Mbed TLS, in a platform security SoC example using opaque ECDSA keys from the PSA Crypto API.

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the PSA Crypto API together with Mbed TLS to build and verify a two-level X.509 certificate chain on the supported device. Private ECDSA keys are kept as **opaque PSA keys** — bound to a PSA key ID and accessed through `mbedtls_pk_setup_opaque()` — so Mbed TLS performs signing and verification through PSA without ever seeing the private bytes in cleartext. On HSE-equipped devices the example can also sign the device certificate with the **built-in private device (attestation) key** stored in the SE.

The CRYPTO engine in the device accelerates the X.509 API functions of Mbed TLS, and the example redirects standard I/O to the kit's VCOM port. On devices that support it, the example counts the number of clock cycles spent in each operation and prints the results on the console. Cycle measurement can be disabled by defining `PSA_CRYPTO_PRINT=0` (default is `1`) in the project's preprocessor settings, and certificate dumping can be disabled by defining `PSA_CRYPTO_PRINT_CERT=0` (default is `1`).

### Program Flow

The two-level certificate-chain flow is:

1. Initialize a **root CSR** and create an ECC key pair for it.
2. Write the root CSR in PEM format.
3. Load the root CSR and initialize a **root certificate**.
4. Set the root certificate parameters.
5. Create the root certificate (self-signed by the root private key) in PEM format.
6. Load the root certificate and store its Distinguished Name (DN) for the device certificate.
7. Initialize a **device CSR** and create an ECC key pair for it.
8. Write the device CSR in PEM format.
9. Load the device CSR and initialize a **device certificate**.
10. Set the device certificate parameters.
11. Create the device certificate (signed by the root private key — or, on HSE devices, optionally by the built-in private device key) in PEM format.
12. Load the device certificate and verify the root → device chain with `mbedtls_x509_crt_verify()`.

### Elliptic Curve Keys

`PSA_ECC_FAMILY_SECP_R1`

- SECP192R1 — 192-bit
- SECP256R1 — 256-bit
- SECP384R1 — 384-bit
- SECP521R1 — 521-bit

ECDSA (`PSA_ALG_ECDSA(hash_alg)`) is used for both CSR signing and certificate signing.

### Hash Algorithms

The Mbed TLS X.509 write API selects from:

- `MBEDTLS_MD_SHA224`
- `MBEDTLS_MD_SHA256`
- `MBEDTLS_MD_SHA384`
- `MBEDTLS_MD_SHA512`

### Key Storage

- Volatile plain key in RAM
- Persistent plain key in [NVM3](https://docs.silabs.com/gecko-platform/latest/driver/api/group-nvm3)
- Volatile wrapped key in RAM (Secure Vault High only)
- Persistent wrapped key in NVM3 (Secure Vault High only)

### Built-in Key

On HSE/SEMAILBOX-equipped devices the example can sign the device certificate with the **private device key (attestation key)** stored in the SE's secure key storage. This is the same private device key used in the device-certificate flow of AN1268. If the device key is not provisioned, the example falls back to a freshly generated device-side ECC key.

### Certificate Version

`MBEDTLS_X509_CRT_VERSION_3` is used by default (defined in `app_mbedtls_x509.h`). The following V3-only extensions are populated when this version is selected:

- `BasicConstraints`
- `KeyUsage`
- `NsCertType`
- `SubjectKeyIdentifier`
- `AuthorityKeyIdentifier`

### PSA Crypto APIs Used

`psa_crypto_init`, `psa_key_attributes_init`, `psa_set_key_type`, `psa_set_key_bits`, `psa_set_key_usage_flags`, `psa_set_key_algorithm`, `psa_set_key_id`, `psa_set_key_lifetime`, `psa_generate_key`, `psa_reset_key_attributes`, `psa_destroy_key`, `mbedtls_psa_crypto_free`.

### Mbed TLS X.509 APIs Used

CSR write/parse: `mbedtls_x509write_csr_init`, `mbedtls_x509write_csr_set_md_alg`, `mbedtls_x509write_csr_set_subject_name`, `mbedtls_x509write_csr_set_key`, `mbedtls_x509write_csr_pem`, `mbedtls_x509_csr_init`, `mbedtls_x509_csr_parse`, `mbedtls_x509_dn_gets`, `mbedtls_x509write_csr_free`, `mbedtls_x509_csr_free`.

Certificate write/parse/verify: `mbedtls_x509write_crt_init`, `mbedtls_x509write_crt_set_issuer_key`, `mbedtls_x509write_crt_set_subject_key`, `mbedtls_x509write_crt_set_issuer_name`, `mbedtls_x509write_crt_set_subject_name`, `mbedtls_x509write_crt_set_version`, `mbedtls_x509write_crt_set_md_alg`, `mbedtls_x509write_crt_set_serial_raw`, `mbedtls_x509write_crt_set_validity`, `mbedtls_x509write_crt_set_basic_constraints`, `mbedtls_x509write_crt_set_key_usage`, `mbedtls_x509write_crt_set_ns_cert_type`, `mbedtls_x509write_crt_set_subject_key_identifier`, `mbedtls_x509write_crt_set_authority_key_identifier`, `mbedtls_x509write_crt_pem`, `mbedtls_x509_crt_init`, `mbedtls_x509_crt_parse`, `mbedtls_x509_crt_verify`, `mbedtls_x509write_crt_free`, `mbedtls_x509_crt_free`.

Opaque-key glue and supporting helpers: `mbedtls_pk_init`, `mbedtls_pk_setup_opaque`, `mbedtls_pk_free`, `mbedtls_mpi_init`, `mbedtls_mpi_read_string`, `mbedtls_mpi_free`.

### Entropy and PRNG

The example uses CTR-DRBG (from [Mbed TLS](https://docs.silabs.com/mbed-tls/latest/)) as its PRNG. On devices with a TRNG hardware module, the TRNG seeds CTR-DRBG; on devices without a TRNG, the seed comes from [RAIL](https://docs.silabs.com/rail/latest/) or an NV (non-volatile) seed stored in NVM3.

### Buffer Management

`SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` is **enabled** by default to optimize for memory and performance. This is NOT the most secure configuration — it assumes that input and output buffers passed to PSA functions are exclusively owned by the PSA function and are not shared across trust boundaries, allowing the implementation to skip local copies.

When the macro is disabled, PSA functions make defensive `malloc`/`memcpy`/`free` copies of input and output buffers. This protects against TOCTOU-style data tampering and buffer leakage across trust boundaries at the cost of additional RAM and runtime overhead.

- **Disable** `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` when security is critical and buffers may be shared across trust boundaries.
- **Enable** it for performance-critical applications where buffers are guaranteed to be exclusive.

### Other Notes

- If an algorithm is not implemented in the device's hardware accelerator, PSA Crypto falls back to the Mbed TLS software implementation transparently.
- The `.slcp` ships with `SL_HEAP_SIZE = 7168`. CSR/certificate writing and PEM serialization are heap-heavy; lowering this value will cause `MBEDTLS_ERR_*_ALLOC_FAILED` errors during write or parse.
- The Mbed TLS X.509 error codes differ from the PSA Crypto error codes; both negative-`MBEDTLS_ERR_*` and `PSA_ERROR_*` codes can appear on the console in the same run.
- Default optimization is `Optimize for debugging (-Og)` on Simplicity IDE and `None` on IAR Embedded Workbench.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 1 or Series 2 SoC development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK. **Secure Vault High** is required to exercise wrapped-key storage and the built-in private device key; **HSE/SEMAILBOX**-equipped parts are needed to sign certificates with the built-in attestation key. Non-Vault, non-HSE parts run the generic plain-key chain only.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device.
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- Simplicity Commander (optional, for command-line flashing and for inspecting the SE's device certificate / public device key — see AN1268).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit.
2. **Create the project.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **Platform Security - SoC PSA Crypto X.509**, and create the project (`psa_crypto_x509`) into your workspace.
3. **(Optional) Tune the example.** Adjust `ROOT_KEY_ID` / `DEVICE_KEY_ID` in `app_process.h`, the default certificate version in `app_mbedtls_x509.h`, `SL_HEAP_SIZE` in the project configurator, or the `PSA_CRYPTO_PRINT` / `PSA_CRYPTO_PRINT_CERT` / `SL_MBEDTLS_PSA_ASSUME_EXCLUSIVE_BUFFERS` preprocessor defines if you need to change persistent-key slots, certificate version, heap, cycle reporting, certificate dumping, or buffer-copy behaviour.
4. **Build.** Build the project; on success Studio produces the application image.
5. **Flash.** Use **Debug** or **Flash Programmer** in Studio, or flash the `.s37`/`.hex` with Simplicity Commander.
6. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
7. **Run.** Reset the kit; the example walks through the program flow above for every supported (curve × hash × key storage) combination, prints each CSR and certificate in PEM, runs `mbedtls_x509_crt_verify()` on the chain, and (optionally) prints cycle counts.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **`psa_generate_key` returns `PSA_ERROR_ALREADY_EXISTS`** — `ROOT_KEY_ID` or `DEVICE_KEY_ID` in `app_process.h` collides with an existing entry in NVM3. Change one or both IDs, or erase NVM3, and rebuild.
- **`mbedtls_x509write_csr_pem` / `mbedtls_x509write_crt_pem` returns `MBEDTLS_ERR_*_ALLOC_FAILED`** — heap exhaustion. Raise `SL_HEAP_SIZE` in the project configurator (defaults to `7168`); CSR/certificate write is the most heap-heavy step in this sample.
- **`mbedtls_x509_crt_parse` returns `MBEDTLS_ERR_X509_INVALID_FORMAT`** — the PEM buffer was truncated or the writer failed silently. Re-check that `mbedtls_x509write_*_pem` returned `0` for the corresponding write step, and that the output buffer was large enough.
- **`mbedtls_x509_crt_verify` returns non-zero** — the device certificate was not signed by the root key, or the chain DN linkage is incorrect. Confirm that the root CSR/certificate ran to completion and that the device certificate's issuer name matches the root certificate's subject name.
- **Wrapped-key / built-in device-key paths return `PSA_ERROR_NOT_SUPPORTED`** — wrapped-key storage requires **Secure Vault High**; the built-in private device key requires HSE/SEMAILBOX. Non-Vault, non-HSE parts will fall back to the generic plain-key chain.
- **Built-in device key not used** — the key is not provisioned in the SE's secure key storage, or the device is not HSE-equipped. Refer to AN1268 for provisioning the device certificate and attestation key, or generate a fresh device key in the example.
- **Error codes look unfamiliar** — Mbed TLS returns negative `MBEDTLS_ERR_*` values, and PSA Crypto returns `PSA_ERROR_*` values. They share the console but come from different error spaces; treat each accordingly.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1268: Authenticating Silicon Labs Devices Using Device Certificates](https://www.silabs.com/documents/public/application-notes/an1268-efr32-secure-identity.pdf)
- [AN1311: Integrating Crypto Functionality Using PSA Crypto Compared to Mbed TLS](https://www.silabs.com/documents/public/application-notes/an1311-mbedtls-psa-crypto-porting-guide.pdf)
- [Mbed TLS X.509 module documentation](https://mbed-tls.readthedocs.io/en/latest/kb/how-to/generate-a-csr/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
