# Platform Security - SoC SE Manager Key Agreement (ECDH)

Demonstrates how to perform ECDH key agreement between client and server peers with the SE Manager API, using plain, wrapped, or volatile ECC keys on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the **SE Manager ECDH API** to simulate a **client** and **server** performing Elliptic-Curve Diffie-Hellman (ECDH) key agreement on one device. Each peer generates an ECC key pair, exchanges public keys, computes a shared secret with its private key and the peer’s public key, and the example **compares** the two secrets to confirm they match.
Output is printed on the kit **VCOM** port, including **clock-cycle counts** per operation when `SE_MANAGER_PRINT=1` (default).

### Interactive menu

- **SPACE** — cycle the current menu option
- **ENTER (CR)** — confirm and proceed
**Secure Vault High** — configure in order:
1. **Key storage:** plaintext, wrapped, or volatile SE slot
2. **Curve family:** ECC Weierstrass Prime or ECC Montgomery
3. **Specific curve** (see table below)
**Secure Vault Mid** — select curve family and curve only; keys are **plaintext in RAM**.

### Supported curves

| Family | Curves |
|--------|--------|
| **ECC Weierstrass Prime** | P192, P256; on Vault High also P384, P521, custom **secp256k1** |
| **ECC Montgomery** | X25519 (HSE); on Vault High also X448 |

### ECDH flow (per run)

1. **Client:** generate key → export public key  
2. **Server:** generate key → export public key  
3. **Client:** `sl_se_ecdh_compute_shared_secret` using client private key + server public key  
4. **Server:** `sl_se_ecdh_compute_shared_secret` using server private key + client public key  
5. **Compare** client and server shared secrets (expect **OK**)
On **volatile** keys (Vault High), volatile slots are deleted after a successful compare before returning to the startup menu.
**Components used:** `se_manager`, `sl_main`, `device_init`, `clock_manager`, VCOM stdio retargeting. Requires **`device_has_semailbox`**.

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_validate_key`, `sl_se_get_storage_size`, `sl_se_generate_key`, `sl_se_export_public_key`, `sl_se_delete_key` (Vault High), `sl_se_ecdh_compute_shared_secret`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- A **Secure Vault** development kit with SE mailbox support (see board compatibility in Simplicity Studio for `se_manager_ecdh` / `se_manager_ecdh_s3`).
- **AEM** power selected on the radio/mainboard switch when programming (see image below).
- USB connection for programming and VCOM.

### Software Requirements

- **Simplicity Studio 5** (current SDK matching the example).
- A serial terminal (or **Device Console** in Studio) on the kit **VCOM** port:
  - **115200** baud, **8-N-1**
  - **Line terminator: None** (required for Device Console)
- Latest **adapter firmware** and **Secure Engine (SE) firmware** on the kit ([General Device Information](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-about-the-launcher/welcome-and-device-tabs#general-device-information)).
- For **X25519** on HSE Secure Vault Mid: SE firmware **v1.2.11+** (EFR32xG21) or **v2.1.7+** (other HSE devices).

## Steps to Run Demo

1. Update kit **adapter firmware** and device **SE firmware** to the latest versions.
2. Open a serial terminal on the kit **VCOM** port (115200 8-N-1; line terminator **None** if using Device Console).
3. Create the **Platform Security - SoC SE Manager Key Agreement (ECDH)** project in Simplicity Studio ([Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)).
4. Build and flash the project ([Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build), [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer)).
5. Reset the board and follow the console prompts:
   - **Vault High:** choose key type (plaintext / wrapped / volatile), then curve family and curve.
   - **Vault Mid:** choose Weierstrass (P192/P256) or Montgomery (X25519).
6. Watch the log for client and server key generation, public-key export, shared-secret computation, and **Compare shared secret… OK**.
7. The startup menu reappears so you can run again with different settings.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM 115200 8-N-1, line terminator **None**; `SL_BOARD_ENABLE_VCOM=1` |
| SE manager init failed | Latest SE firmware; Secure Vault + SE mailbox |
| Wrapped / volatile options missing | Expected on **Secure Vault Mid** — use Vault High for full key-storage paths |
| X25519 failures on Mid HSE | SE firmware version (see Prerequisites) |
| Compare shared secret **Failed** | Rebuild and rerun; matching curve and key type on both peers |
| Volatile key cleanup errors | Prior run may have left a slot occupied — reset and retry |
| Programming fails | AEM switch position (see Prerequisites image) |
| Slow or debug-heavy build | Default optimization is **debug (-Og)** on GCC / **None** on IAR — intentional for this example |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1271: Secure Key Storage](https://www.silabs.com/documents/public/application-notes/an1271-efr32-secure-key-storage.pdf)
- [Simplicity Studio 5 User's Guide — Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).

