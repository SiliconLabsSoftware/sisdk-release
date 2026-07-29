# Platform Security - SoC SE Manager Asymmetric Key Handling

Demonstrates how to generate, import, export, transfer, and delete asymmetric ECC keys with the SE Manager API, using plain, wrapped, and volatile key storage on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example exercises the **SE Manager asymmetric key handling** APIs on a Secure Vault device. Standard I/O is redirected to the kit **VCOM** port. The application reports **clock-cycle counts** per operation when `SE_MANAGER_PRINT=1` (default).
After reset, use the serial menu to choose an **ECC algorithm family** and curve, then the example runs automatically through the key-handling flows for that selection.

### Interactive menu

- **SPACE** — cycle the current menu option (algorithm family or curve)
- **ENTER (CR)** — confirm selection and proceed
**Algorithm families:**
| Family | Curves (device-dependent) |
|--------|---------------------------|
| **ECC Weierstrass Prime** | P192, P256; on Secure Vault High also P384, P521, and custom **secp256k1** |
| **ECC Montgomery** | X25519; on Secure Vault High also X448 |
| **ECC EdDSA** | Ed25519 |

### Key storage types

| Storage | Secure Vault Mid | Secure Vault High |
|---------|------------------|-------------------|
| **Plaintext key in RAM** | Yes | Yes |
| **Wrapped key in RAM** | No | Yes |
| **Volatile key in SE slot** | No | Yes |

### Operations demonstrated

**All supported devices (plain key path):**
1. Generate a **plain asymmetric key pair** (`sl_se_generate_key`)
2. Export the **public key** (`sl_se_export_public_key`)
**Secure Vault High only (additional flows):**
3. Import plain key into an **exportable wrapped** key (`sl_se_import_key`)
4. Export wrapped key back to plain (`sl_se_export_key`) and **verify** public key matches
5. Generate a **non-exportable wrapped** key and export its public key
6. Generate a **volatile SE slot** key, export public key, then delete it (`sl_se_delete_key`)
7. **Transfer** wrapped ↔ volatile keys (`sl_se_transfer_key`) and verify public key consistency
**Components used:** `se_manager`, `sl_main`, `device_init`, `clock_manager`, VCOM stdio retargeting. Requires **`device_has_semailbox`**.

## Prerequisites / Setup Requirements

### Hardware Requirements

- A **Secure Vault** development kit with SE mailbox support (see board compatibility in Simplicity Studio for `se_manager_asymmetric_key_handling` / `se_manager_asymmetric_key_handling_s3`).
- **AEM** power selected on the radio/mainboard switch when programming (see image below).
- USB connection for programming and VCOM.

### Software Requirements

- **Simplicity Studio 5** (current SDK matching the example).
- A serial terminal (or **Device Console** in Studio) on the kit **VCOM** port:
  - **115200** baud, **8-N-1**
  - **Line terminator: None** (required for Device Console)
- Latest **adapter firmware** and **Secure Engine (SE) firmware** on the kit ([General Device Information](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-about-the-launcher/welcome-and-device-tabs#general-device-information)).
- For **X25519** and **Ed25519** on HSE Secure Vault Mid: SE firmware **v1.2.11+** (EFR32xG21) or **v2.1.7+** (other HSE devices).

## Steps to Run Demo

1. Update kit **adapter firmware** and device **SE firmware** to the latest versions.
2. Open a serial terminal on the kit **VCOM** port (115200 8-N-1; line terminator **None** if using Device Console).
3. Create the **Platform Security - SoC SE Manager Asymmetric Key Handling** project in Simplicity Studio ([Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)).
4. Build and flash the project ([Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build), [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer)).
5. Reset the board and follow the console prompts:
   - Press **SPACE** to choose **ECC Weierstrass Prime**, **ECC Montgomery**, or **ECC EdDSA (Ed25519)**.
   - Press **ENTER** to open curve selection (Weierstrass / Montgomery) or run immediately (Ed25519).
   - Press **SPACE** to cycle curves, then **ENTER** to start the demo.
6. Watch the log for each step (`Generate…`, `Export…`, `Import…`, `Transfer…`, `Compare… OK`) and per-operation timing when `SE_MANAGER_PRINT` is enabled.
7. On **Secure Vault High**, the full sequence runs through plain, wrapped, volatile, and transfer paths, then returns to the startup menu. On **Secure Vault Mid**, only the plain-key path runs, then the menu reappears.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM 115200 8-N-1, line terminator **None**; `SL_BOARD_ENABLE_VCOM=1` |
| SE manager init failed | Latest SE firmware; board has Secure Vault + SE mailbox |
| Wrapped / volatile / transfer steps missing | Expected on **Secure Vault Mid** — upgrade to Secure Vault High board for full flow |
| X25519 or Ed25519 failures on Mid HSE | SE firmware version (see Prerequisites) |
| `Compare export/transfer… Failed` | Rebuild and rerun; confirm no other app holds the volatile key slot |
| Programming fails | AEM switch position (see Prerequisites image) |
| Slow or debug-heavy build | Default optimization is **debug (-Og)** on GCC / **None** on IAR — intentional for this example |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1271: Secure Key Storage](https://www.silabs.com/documents/public/application-notes/an1271-efr32-secure-key-storage.pdf)
- [Simplicity Studio 5 User's Guide — Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
