# Platform Security - SoC SE Manager Key Provisioning

Demonstrates how to provision SE OTP keys (AES-128, public sign/command) and secure-boot or tamper configuration with the SE Manager APIs on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example demonstrates **one-time programming** of Secure Engine **OTP** content using SE Manager provisioning APIs. Output is on the kit **VCOM** port, with **clock-cycle counts** when `SE_MANAGER_PRINT=1` (default).
After reset, the application:
1. Reads the **SE firmware version**
2. Reads current **OTP configuration** (and **tamper** settings on Secure Vault High)
3. Optionally programs (in order, each step skippable with **SPACE**):
   - **128-bit AES key** in OTP (**HSE** devices only — not VSE)
   - **Public sign key** (boot immutable key)
   - **Public command key** (auth immutable key)
   - **OTP initialization** for **secure boot** (and **tamper** on Vault High)
Embedded test keys match the Silicon Labs offline provisioning scripts (`encrypt-unsafe-key.prv`, `rootsign-unsafe-privkey.pem`, `cmd-unsafe-privkey.pem` under the SE Manager pack `scripts/offline` folder in Simplicity Studio).

### What can be provisioned

| Item | Device support |
|------|----------------|
| **Tamper + secure boot OTP config** | Secure Vault **High** |
| **Secure boot OTP config** (no tamper) | Secure Vault **Mid** |
| **AES-128 OTP key** | **HSE** only |
| **Public sign key** | HSE / VSE |
| **Public command key** | HSE / VSE |

### Critical warning

Programming OTP keys and OTP configuration is **one-time only** and **irrevocable** for the life of the device. Provisioning **fails** if the slot was already written. Use **development boards** only, with a recovery plan.
On **VSE** (`CRYPTOACC_PRESENT`), several operations trigger a **device reset**; results are read after reset via `sl_se_read_executed_command` and `sl_se_ack_command`.
**Components used:** `se_manager`, `sl_main`, `device_init`, `clock_manager`, VCOM stdio retargeting.

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_get_se_version`, `sl_se_read_otp`, `sl_se_read_pubkey`, `sl_se_init_otp_key`, `sl_se_init_otp`, `sl_se_aes_crypt_ecb`, and on VSE: `sl_se_read_executed_command`, `sl_se_ack_command`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- A **Secure Vault** development kit (see board compatibility for `se_manager_key_provisioning` / `se_manager_key_provisioning_s3`).
- **AEM** power when programming (see image below).
- USB for programming and VCOM.


### Software Requirements

- **Simplicity Studio 5** with SE Manager offline scripts (optional reference keys under `secmgr` pack `scripts/offline`).
- VCOM: **115200** 8-N-1, line terminator **None** (Device Console).
- Latest **adapter** and **SE firmware**.

### Before you run

- Understand which items are already provisioned (read-only steps show current OTP state).
- **Disconnect the debugger** if your flow requires it for OTP programming on your target.
- Do **not** run full provisioning on units you cannot afford to brick or misconfigure.

## Steps to Run Demo

1. Flash this example on a **development** Secure Vault board.
2. Open VCOM (115200 8-N-1, line terminator **None**).
3. Reset and follow the serial log.

### Interactive flow

- **ENTER (CR)** — confirm the next provisioning step (after warning text).
- **SPACE** — skip the current optional step.
Typical sequence:
1. View SE version and read OTP/tamper configuration.
2. **AES-128 key (HSE):** ENTER twice to confirm, or SPACE to skip → verify with AES-ECB encrypt vs. expected ciphertext.
3. **Public sign key:** ENTER to provision, or SPACE to skip → read back public key bytes.
4. **Public command key:** same pattern.
5. **OTP init:** ENTER to apply secure boot (and tamper on Vault High), or SPACE to exit.
On **VSE**, expect **reset** between program/read operations; continue from post-reset log messages.

### Reference key material (offline scripts)

Example AES-128 key (hex): `81a5e21fa15286f1df445c2cc120fa3f`
Public coordinates for sign/command keys are embedded in `app_process.c` and documented in the original readme; match your `rootsign-unsafe-privkey.pem` / `cmd-unsafe-privkey.pem` when regenerating firmware.

### Optional: disable timing prints

Define **`SE_MANAGER_PRINT=0`** in preprocessor symbols.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM settings; `SL_BOARD_ENABLE_VCOM=1` |
| Init OTP / key **failed** | Slot may already be provisioned (one-time only) |
| Cannot read public key | Key not provisioned yet — run init step first |
| Secure boot enable blocked | Public sign key must be provisioned first |
| AES key step missing | **HSE** only — not available on VSE path |
| Tamper config missing | **Secure Vault High** only |
| Unexpected reset | Normal on **VSE** during program operations |
| AES verify **Failed** | Wrong key already in OTP or wrong device family |
| Programming fails | AEM switch position |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1222: Production Programming of Series 2 Devices](https://www.silabs.com/documents/public/application-notes/an1222-efr32xg2x-production-programming.pdf)
- [AN1218: Series 2 Secure Boot with RTSL](https://www.silabs.com/documents/public/application-notes/an1218-secure-boot-with-rtsl.pdf)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
