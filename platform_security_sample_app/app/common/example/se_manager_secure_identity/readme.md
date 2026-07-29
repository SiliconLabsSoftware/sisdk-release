# Platform Security - SoC SE Manager Secure Identity

Demonstrates how to read on-chip device certificates, verify an X.509 chain, and sign a challenge with the private device key using SE Manager and mbed TLS on Secure Vault High.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example models **device authentication** for **Secure Vault High** parts: read factory-programmed **device** and **batch** certificates from the SE, parse and verify an **X.509 certificate chain** with **mbed TLS** (accelerated by the SE crypto engine via `mbedtls_slcrypto`), then perform a **challenge–response** proof using the **private device key** in Secure Key Storage.
The demo runs **automatically** on reset (no serial menu). Progress and optional certificate dumps print on **VCOM**. **Clock-cycle counts** print when `SE_MANAGER_PRINT=1` (default).

### Flow (high level)

1. **On-chip (Vault High device)**
   - Read certificate sizes and **device** / **batch** certificates from SE OTP
   - Parse device certificate (DER); extract **public device key**
2. **Remote device (simulated in firmware)**
   - Parse embedded **factory** and **root** certificates (PEM)
   - Verify chain: device → batch → factory → root
3. **Remote authentication**
   - Generate random **challenge** (`SL_SE_CHALLENGE_SIZE` bytes)
   - **Sign** challenge with `SL_SE_APPLICATION_ATTESTATION_KEY` (private device key — never exported)
   - **Verify** signature on-chip and again using the public key from the parsed device certificate

### Configuration notes

| Symbol | Default | Effect |
|--------|---------|--------|
| `SE_MANAGER_PRINT` | `1` | Cycle counts per operation |
| `SE_MANAGER_PRINT_CERT` | `1` | Print parsed certificates on VCOM |
| `NO_CRYPTO_ACCELERATION` | undefined | Define to use software mbed TLS crypto only; increase `SL_HEAP_SIZE` to **10240** (e.g. in `sl_memory_config.h`) for IAR |
| `SL_HEAP_SIZE` | `7504` | Set in `.slcp` for accelerated path |
**Requires:** `device_security_vault` (**Secure Vault High**).
**Components:** `se_manager`, `mbedtls_core`, `mbedtls_x509`, `mbedtls_ecdsa`, `mbedtls_ccm`, `mbedtls_slcrypto`, VCOM stdio.

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_get_random`, `sl_se_read_cert_size`, `sl_se_read_cert`, `sl_se_ecc_sign`, `sl_se_read_pubkey`, `sl_se_ecc_verify`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- **Secure Vault High** development kit (device and batch certificates must be present in SE).
- USB for programming and VCOM.
- **AEM** power when programming.


### Software Requirements

- **Simplicity Studio 5**, latest adapter and **SE firmware**.
- VCOM: **115200** 8-N-1, line terminator **None** (Device Console).

### Before you run

- Use a part that ships with **Silicon Labs identity certificates** programmed (typical Vault High dev boards).
- Embedded **factory** and **root** PEM blobs in `app_mbedtls_x509.c` must match your device’s certificate hierarchy for chain verification to succeed.

## Steps to Run Demo

1. Create and build the project for a **Vault High** target.
2. Flash to the kit and open VCOM (115200 8-N-1, line terminator **None**).
3. Reset the board and watch the log through deinitialization.
Expected sections on the console:
- `Secure Vault High device:` — read/parse device and batch certs
- `Remote device:` — parse factory/root, verify chain
- `Remote authentication:` — challenge, sign, dual verify
Success ends with signature verification OK on both local and “remote” paths.

### Optional build tweaks

- **`SE_MANAGER_PRINT=0`** — disable cycle timing prints
- **`SE_MANAGER_PRINT_CERT=0`** — suppress certificate text (verification step message still prints when certs are hidden)
- **`NO_CRYPTO_ACCELERATION`** — software-only mbed TLS; increase heap as noted above

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM settings; `SL_BOARD_ENABLE_VCOM=1` |
| Read cert **failed** | Not Vault High or certificates not provisioned on device |
| Parse / chain verify **failed** | Wrong or missing on-chip certs; factory/root PEM mismatch |
| Sign or verify **failed** | Attestation key or cert/key inconsistency |
| Heap / malloc failures with `NO_CRYPTO_ACCELERATION` | Raise `SL_HEAP_SIZE` to **10240** |
| Garbled output | Line terminator must be **None** in Device Console |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1268: Authenticating Silicon Labs Devices Using Device Certificates](https://www.silabs.com/documents/public/application-notes/an1268-efr32-secure-identity.pdf)
- [mbed TLS X.509 documentation](https://tls.mbed.org/api/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
