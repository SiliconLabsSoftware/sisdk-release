# Platform Security - SoC SE Manager Secure Debug

Demonstrates how to enable secure debug, apply debug lock, and unlock the interface with a signed access certificate using SE Manager APIs on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example walks through **Secure Vault secure debug** using SE Manager: read debug/lock status, optionally provision the **public command key** in SE OTP, **enable secure debug**, **lock** the debug port, and **unlock** with a challenge-response **access certificate** signed by the matching private command key.
Output is on the kit **VCOM** port. **Clock-cycle counts** print when `SE_MANAGER_PRINT=1` (default).

### What the demo does

After initialization, the app prints **SE firmware version**, **debug lock**, **device erase**, **secure debug**, **secure boot**, and TrustZone-related **debug option** config/state. It then branches based on current device state:
| State | Console behavior |
|-------|------------------|
| **Normal**, secure debug **disabled** | Compare or program public command key → optionally **enable secure debug** → **lock** device |
| **Normal**, secure debug **enabled** | Verify OTP public command key matches embedded test key → **lock** device |
| **Secure debug lock** | Build signed **unlock token** (certificate + challenge signature) → **open debug** |
| **Secure debug unlock** | Prompt for reset to re-lock; optional **challenge roll** |
| **Standard debug lock** | Offer **mass erase** debug unlock (not certificate-based) |
| **Permanent debug lock** | Device cannot be unlocked — exit |
For lab use only, a **hard-coded private command key** in `app_se_manager_secure_debug.c` signs the access certificate. Production systems must **import** a properly protected private key and certificate (not store the private key in firmware).
Default test key pair matches `cmd-unsafe-privkey.pem` from the SE Manager pack offline scripts (`secmgr` → `scripts/offline` in Simplicity Studio).
**TrustZone debug options** (see `app_se_manager_secure_debug.h`):
- `DEBUG_OPTIONS` = `0x0c` — lock secure invasive/non-invasive debug when applying lock
- `DEBUG_MODE_REQUEST` = `0x3e` — unlock request for secure and non-secure debug/trace

### Critical warnings

- Programming the **public command key** to SE OTP is **one-time only** and **irrevocable**.
- **Disable device erase** is a **one-time, permanent** operation when confirmed.
- **Disconnect the debugger** before locking or unlocking the debug interface.
- Use **development boards** only; incorrect lock/erase settings can brick units for debug.
**Requires:** `device_has_semailbox` (Secure Vault).

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_get_status`, `sl_se_get_debug_lock_status`, `sl_se_validate_key`, `sl_se_get_storage_size`, `sl_se_generate_key`, `sl_se_export_public_key`, `sl_se_read_pubkey`, `sl_se_init_otp_key`, `sl_se_apply_debug_lock`, `sl_se_erase_device`, `sl_se_enable_secure_debug`, `sl_se_disable_secure_debug`, `sl_se_disable_device_erase`, `sl_se_set_debug_options`, `sl_se_get_serialnumber`, `sl_se_get_challenge`, `sl_se_ecc_sign`, `sl_se_open_debug`, `sl_se_roll_challenge`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- Secure Vault kit with SE mailbox (see template board compatibility).
- **AEM** power when programming.

### Software Requirements

- **Simplicity Studio 5**, latest adapter and **SE firmware**.
- VCOM: **115200** 8-N-1, line terminator **None**.
- Optional: `cmd-unsafe-privkey.pem` from `secmgr` offline scripts for reference.

### Before you run

- If OTP has **no** public command key, the app can offer to program the test public key (matches `cmd-unsafe-privkey.pem`).
- To test unlock on a device with a **different** OTP command key, update `private_command_key[]` in `app_se_manager_secure_debug.c` to match.
- For certificate unlock tests, complete the **enable secure debug → lock** path first, or start from **secure debug lock** state.

## Steps to Run Demo

1. Build, flash, and open VCOM (115200 8-N-1, line terminator **None**).
2. Reset and read the printed **SE status** block.
3. Follow prompts for your device state (**ENTER** = confirm, **SPACE** = skip/exit).

### Typical “green field” flow (secure debug disabled)

1. App verifies or offers to **program public command key** to OTP (double ENTER to confirm — **irreversible**).
2. **ENTER** to **enable secure debug**.
3. **ENTER** to **lock** the device (sets `DEBUG_OPTIONS`, applies debug lock).
4. Optionally **ENTER** to **disable device erase** (permanent — skip with SPACE if only testing).
5. Reset; when in **secure debug lock**, **ENTER** to run **secure debug unlock** (certificate + challenge signing, `sl_se_open_debug`).
6. On success, reconnect debugger; status shows **secure debug unlock** until power-on/pin reset.

### Secure debug unlock sub-flow

When locked with secure debug enabled, the app:
1. Generates an ephemeral **certificate key pair**
2. Builds an **access certificate** (serial number, authorizations, public cert key) signed with the **private command key**
3. Fetches and signs the **challenge** with the certificate private key
4. Submits the **unlock token** with `DEBUG_MODE_REQUEST`

### Challenge roll

In **secure debug unlock** state, **ENTER** requests and rolls the challenge; perform a **power-on or pin reset** to activate the new challenge (invalidates the prior unlock token).

### Optional: disable timing prints

Set **`SE_MANAGER_PRINT=0`** in preprocessor symbols.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM 115200 8-N-1; terminator **None**; `SL_BOARD_ENABLE_VCOM=1` |
| Public key compare **Failed** | OTP key does not match `private_command_key[]` — update source or reprovision OTP (one-time) |
| Unlock **Failed** | Wrong command key, stale challenge, or debugger still attached |
| **Permanent debug lock** | Device erase disabled and locked — cannot unlock |
| Standard lock path only | Secure debug not enabled — certificate unlock not applicable |
| Cannot program command key | Slot already provisioned |
| Lock/unlock hangs or errors | Disconnect debugger during lock/unlock operations |
| TrustZone debug partial | Adjust `DEBUG_OPTIONS` / `DEBUG_MODE_REQUEST` per AN1190 |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1190: Series 2 Secure Debug](https://www.silabs.com/documents/public/application-notes/an1190-efr32-secure-debug.pdf)
- [Key Provisioning example](https://github.com/SiliconLabs/platform-sample-apps/tree/main/app/common/example/se_manager_key_provisioning) (OTP public command/sign keys)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
