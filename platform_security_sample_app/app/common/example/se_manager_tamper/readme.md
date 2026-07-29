# Platform Security - SoC SE Manager Tamper

Demonstrates how to provision tamper OTP settings, trigger tamper via kit buttons, and temporarily disable tamper with a signed SE Manager token on Secure Vault High.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example demonstrates **anti-tamper** on **Secure Vault High** devices using SE Manager: read reset/tamper cause, inspect or **one-time provision** OTP tamper configuration, run a **normal** tamper exercise with kit buttons (**PB0** / **PB1**), and optionally submit a **signed tamper-disable token** (command key + challenge/certificate flow in `app_se_manager_tamper_disable.c`).
Tamper levels and PRS wiring in `app_se_manager_tamper.c` are **for lab demonstration only** — not a production recommendation.
Output and **clock-cycle counts** print on **VCOM** (`SE_MANAGER_PRINT=1` by default).
**Requires:** `device_security_vault` (Vault **High**), `simple_button` (PB0/PB1), PRS.

### Tamper response levels

| Level | Response |
|-------|----------|
| 0 | Ignore |
| 1 | Interrupt (`SETAMPERHOST`) |
| 2 | Filter (increment filter counter) |
| 4 | Reset |
| 7 | Erase OTP (device and wrapped secrets unrecoverable) |
Per-source default and example levels differ by **Series 2 vs Series 3** and part configuration; see **AN1247** and the tables in the legacy readme / `app_se_manager_tamper.c` for your target.

### Critical warnings

- **OTP tamper configuration** and **public command key** programming are **one-time only** and **irrevocable**.
- **Disconnect the debugger** when running tamper tests.
- This example does **not** enable secure boot when provisioning tamper OTP.
- Hard-coded **private command key** in firmware is **insecure** for production — use protected key storage and signed certificates in real products.
- Level **7** (erase OTP) can permanently destroy the device.

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_get_reset_cause`, `sl_se_get_status`, `sl_se_read_otp`, `sl_se_init_otp`, `sl_se_validate_key`, `sl_se_get_storage_size`, `sl_se_generate_key`, `sl_se_export_public_key`, `sl_se_read_pubkey`, `sl_se_init_otp_key`, `sl_se_get_serialnumber`, `sl_se_get_challenge`, `sl_se_ecc_sign`, `sl_se_disable_tamper`, `sl_se_roll_challenge`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- **Secure Vault High** kit with **two push buttons** (PB0, PB1) routed for tamper/PRS demo.
- USB for VCOM; **AEM** power when programming.
![Radio board power supply switch](image/readme_img0.png)

### Software Requirements

- **Simplicity Studio 5**, latest adapter and **SE firmware** (tamper reset-cause API needs sufficiently new SE FW on supported parts).
- VCOM: **115200** 8-N-1, line terminator **None**.
- Optional reference key: `cmd-unsafe-privkey.pem` under SE Manager pack `scripts/offline`.

### Before you run

- OTP must match this example’s expected tamper layout, or you must **provision** OTP once (irreversible) and **reset** to activate.
- If OTP has no **public command key**, the app can program the test key (matches `cmd-unsafe-privkey.pem`) or you update `private_command_key[]` in `app_se_manager_tamper_disable.c` to match your OTP key.

## Steps to Run Demo

1. Build, flash, and open VCOM (115200 8-N-1, line terminator **None**).
2. Reset and follow the log.

### Startup

- Read **tamper/reset cause** (SE tamper reset cause when supported, else EMU `RSTCAUSE`).
- Read **OTP tamper configuration**; if missing, **ENTER** twice to confirm **one-time** OTP init → **power-on or pin reset** required.
- If OTP config does not match this example’s expected levels, the app exits with a mismatch message.

### Choose test mode

| Input | Action |
|-------|--------|
| **SPACE** | Toggle **NORMAL** vs **TAMPER DISABLE** |
| **ENTER** | Run selected test |

### NORMAL tamper test

1. Console prints instructions.
2. **PB0** — filter counter / tamper status (interrupt path); PRS may issue reset when threshold reached within filter period.
3. **PB1** — tamper **reset** (per PRS mapping in firmware).
4. Tamper status registers print on interrupt.

### TAMPER DISABLE test

1. Verify or program **public command key** in OTP (same flow as secure debug example).
2. **ENTER** to build and submit **tamper disable token** (`sl_se_disable_tamper`).
3. On success: PB0/PB1 no longer cause configured resets until **power-on/pin reset** re-enables tamper.
4. Optional: **ENTER** to **roll challenge** (invalidates disable token after reset).

### Command key reference (test vector)

Public key coordinates for `cmd-unsafe-privkey.pem` (also embedded in disable source):
- X: `B1BC6F6FA56640ED522B2EE0F5B3CF7E5D48F60BE8148F0DC08440F0A4E1DCA4`
- Y: `7C04119ED6A1BE31B7707E5F9D001A659A051003E95E1B936F05C37EA793AD63`

### Optional: disable timing prints

Define **`SE_MANAGER_PRINT=0`** in preprocessor symbols.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM; line terminator **None** |
| Config does not match | OTP already provisioned with different levels — use fresh dev part or AN1247 procedure |
| Cannot init OTP | Already written (one-time) |
| Disable tamper **Failed** | Command key mismatch; challenge stale |
| Unexpected reset | NORMAL mode — expected for PB1/PRS; disable mode — reset to re-arm tamper |
| No tamper reset cause API | Upgrade SE firmware per app version check |
| Buttons no effect | Board must expose PB0/PB1 per `simple_button` config |
| Debugger attached | Disconnect for tamper testing |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1247: Anti-Tamper Protection Configuration and Use](https://www.silabs.com/documents/public/application-notes/an1247-efr32-secure-vault-tamper.pdf)
- [Key Provisioning example](https://github.com/SiliconLabs/platform-sample-apps/tree/main/app/common/example/se_manager_key_provisioning) (OTP tamper + command key)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
