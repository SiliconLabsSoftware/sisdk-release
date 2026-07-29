# Platform Security - SoC SE Manager Key Derivation (HKDF and PBKDF2)

Demonstrates how to derive keys with the SE Manager HKDF and PBKDF2 APIs, verifying output against known test vectors on Secure Vault High devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example exercises **key derivation** with the SE Manager on a **Secure Vault High** device. It runs **HKDF** and **PBKDF2** test cases using built-in vectors, compares the derived key material to expected values, and prints **OK** or **Failed** on the kit **VCOM** port.
**HKDF** (HMAC-based Extract-and-Expand) derives output key material from input key material, with optional salt and info strings. **PBKDF2** stretches a password with a salt over many iterations.
The application runs **automatically** after reset (no serial menu). Per-operation **clock-cycle counts** are printed when `SE_MANAGER_PRINT=1` (default).

### Tests performed

| Test | Algorithm | Parameters |
|------|-----------|------------|
| **HKDF 1** | HKDF + **SHA-256** | Zero-length salt and info |
| **HKDF 2** | HKDF + **SHA-256** | Salt + info from test vectors |
| **HKDF 3** | HKDF + **SHA-512** | Same salt + info |
| **PBKDF2 1** | PBKDF2 + HMAC-SHA-256 | Password `password`, salt `salt`, **1** iteration |
| **PBKDF2 2** | PBKDF2 + HMAC-SHA-256 | Same password/salt, **2** iterations |
| **PBKDF2 3** | PBKDF2 + HMAC-SHA-256 | Same password/salt, **4096** iterations |
**Components used:** `se_manager`, `sl_main`, `device_init`, `clock_manager`, VCOM stdio retargeting. Requires **`device_security_vault`** (Secure Vault High).

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_derive_key_hkdf`, `sl_se_derive_key_pbkdf2`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- A **Secure Vault High** development kit (see board compatibility in Simplicity Studio for `se_manager_kdf` / `se_manager_kdf_s3`).
- **AEM** power selected on the radio/mainboard switch when programming (see image below).
- USB connection for programming and VCOM.

### Software Requirements

- **Simplicity Studio 5** (current SDK matching the example).
- A serial terminal (or **Device Console** in Studio) on the kit **VCOM** port:
  - **115200** baud, **8-N-1**
  - **Line terminator: None** (required for Device Console)
- Latest **adapter firmware** and **Secure Engine (SE) firmware** on the kit ([General Device Information](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-about-the-launcher/welcome-and-device-tabs#general-device-information)).

## Steps to Run Demo

1. Update kit **adapter firmware** and device **SE firmware** to the latest versions.
2. Open a serial terminal on the kit **VCOM** port (115200 8-N-1; line terminator **None** if using Device Console).
3. Create the **Platform Security - SoC SE Manager Key Derivation (HKDF and PBKDF2)** project in Simplicity Studio ([Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)).
4. Build and flash the project ([Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build), [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer)).
5. Reset the board. The example runs all six tests in sequence without user input.
6. Confirm each test reports **Comparing … OK**, then SE Manager deinitializes.

### Optional: disable timing prints

Define **`SE_MANAGER_PRINT=0`** in project preprocessor symbols to suppress cycle-count output.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM 115200 8-N-1, line terminator **None**; `SL_BOARD_ENABLE_VCOM=1` |
| SE manager init failed | Latest SE firmware; board is **Secure Vault High** (not Mid-only) |
| HKDF or PBKDF2 compare **Failed** | SE firmware version; do not modify test vectors unless updating expected arrays |
| PBKDF2 test 3 slow | **4096 iterations** is intentional — allow time to complete |
| Example not in Studio picker on Mid board | Expected — requires Secure Vault High |
| Programming fails | AEM switch position (see Prerequisites image) |
| Slow or debug-heavy build | Default optimization is **debug (-Og)** on GCC / **None** on IAR — intentional for this example |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1271: Secure Key Storage](https://www.silabs.com/documents/public/application-notes/an1271-efr32-secure-key-storage.pdf)
- [Simplicity Studio 5 User's Guide — Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
