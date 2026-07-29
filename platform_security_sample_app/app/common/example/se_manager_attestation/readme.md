# Platform Security - SoC SE Manager Attestation

Demonstrates how to obtain and pretty-print PSA IAT and config attestation tokens (COSE_Sign1 / CBOR) with the SE Manager Attestation API on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example uses the **SE Manager Attestation API** to request cryptographically signed attestation tokens from the Secure Engine and print them in a human-readable form on the kit **VCOM** port.
An attestation token contains signed claims about the device — for example lifecycle state, implementation ID, software components, SE status, and OTP configuration. Tokens returned by the SE Manager are **COSE_Sign1** structures wrapping a **CBOR Web Token** of claims.
The example also includes an on-device **CBOR parser** that pretty-prints:
- The raw token (hex)
- The **COSE_Sign1** structure
- Individual claims with human-friendly names (PSA profile/partition/lifecycle, nonce, UEID, SE status, OTP config, tamper settings, and others)
Parsing on-device is mainly for demonstration; production systems typically verify tokens on a host or cloud service.

### Token types fetched

| Token | API | Nonce size |
|-------|-----|------------|
| **PSA Initial Attestation Token (IAT)** | `sl_se_attestation_get_psa_iat_token` | User-selectable: **32**, **48**, or **64** bytes |
| **Configuration token** | `sl_se_attestation_get_config_token` | Fixed **32** bytes |
Both tokens use a random nonce from `sl_se_get_random` before the attestation call.
The example reports **clock-cycle counts** per operation when `SE_MANAGER_PRINT=1` (default).
**Components used:** `se_manager`, `sl_main`, `device_init`, `clock_manager`, VCOM stdio retargeting. Requires **Secure Vault** (`device_security_vault`).

### SE Manager APIs exercised

- `sl_se_init` / `sl_se_deinit`
- `sl_se_init_command_context` / `sl_se_deinit_command_context`
- `sl_se_get_random`
- `sl_se_attestation_get_psa_iat_token`
- `sl_se_attestation_get_config_token`

## Prerequisites / Setup Requirements

### Hardware Requirements

- A **Secure Vault** development kit (see board compatibility in Simplicity Studio for `se_manager_attestation` / `se_manager_attestation_s3`).
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
3. Create the **Platform Security - SoC SE Manager Attestation** project in Simplicity Studio ([Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)).
4. Build and flash the project ([Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build), [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer)).
5. Reset the board. When prompted, select the **IAT token nonce size**:
   - Press **SPACE** to cycle through **32**, **48**, and **64** bytes
   - Press **ENTER (CR)** to confirm
6. The application automatically:
   - Generates a random nonce and fetches the **PSA IAT token**
   - Pretty-prints the raw token, COSE structure, and named claims
   - Fetches the **configuration token** (32-byte nonce) and pretty-prints it
   - Deinitializes SE Manager and exits to idle
7. Review the serial log for token contents and per-operation timing.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM 115200 8-N-1, line terminator **None**; `SL_BOARD_ENABLE_VCOM=1` |
| SE Manager init failed | Latest SE firmware; board is **Secure Vault** (not Vault Mid-only limitation for attestation — confirm part supports attestation) |
| Failed to generate random nonce | SE firmware version; device has working TRNG/SE random source |
| Failed to get PSA IAT or config token | SE attestation provisioning; lifecycle and security configuration on device |
| `Invalid COSE_Sign1 structure` or CBOR parse errors | Token buffer size; reflash and retry with latest SE firmware |
| Programming fails | AEM switch position (see Prerequisites image) |
| Slow or debug-heavy build | Default optimization is **debug (-Og)** on GCC / **None** on IAR — intentional for this example |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1271: Secure Key Storage](https://www.silabs.com/documents/public/application-notes/an1271-efr32-secure-key-storage.pdf)
- [Simplicity Studio 5 User's Guide — Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
