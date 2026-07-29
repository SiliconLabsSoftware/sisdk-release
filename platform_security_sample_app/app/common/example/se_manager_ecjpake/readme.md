# Platform Security - SoC SE Manager Key Agreement (ECJPAKE)

Demonstrates how to perform ECJPAKE password-authenticated key agreement between client and server peers with the SE Manager API on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example runs a full **Elliptic Curve Password Authenticated Key Exchange by Juggling (ECJPAKE)** handshake on one device, simulating a **client** and a **server** that share a known password. Both peers use the **SE Manager ECJPAKE API**; after the two-round exchange, the example **compares** the derived pre-master secrets and expects them to match.
ECJPAKE derives a shared secret without transmitting the password in the clear. This sample uses:
- **Curve:** ECC **P-256** (`SL_SE_KEY_TYPE_ECC_P256`)
- **Hash:** **SHA-256** (`SL_SE_HASH_SHA256`) — the only pair allowed by the ECJPAKE standard as used here
- **Pre-shared password:** `threadjpaketest` (15 bytes), hard-coded in `app_process.c`
The application runs **automatically** after reset (no serial menu). Output is on the kit **VCOM** port, with **clock-cycle counts** per step when `SE_MANAGER_PRINT=1` (default).

### Handshake sequence

1. Initialize and set up **client** and **server** ECJPAKE contexts (`sl_se_ecjpake_init`, `sl_se_ecjpake_setup`, `sl_se_ecjpake_check`)
2. **Round 1:** client write → server read → server write → client read
3. **Round 2:** server write → client read → client derive secret → client write → server read → server derive secret
4. Clear contexts (`sl_se_ecjpake_free`) and **compare** client and server pre-master secrets
**Components used:** `se_manager`, `sl_main`, `device_init`, `clock_manager`, VCOM stdio retargeting. Requires **`device_has_semailbox`**.

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_ecjpake_init`, `sl_se_ecjpake_setup`, `sl_se_ecjpake_check`, `sl_se_ecjpake_write_round_one`, `sl_se_ecjpake_write_round_two`, `sl_se_ecjpake_read_round_one`, `sl_se_ecjpake_read_round_two`, `sl_se_ecjpake_derive_secret`, `sl_se_ecjpake_free`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- A **Secure Vault** development kit with SE mailbox support (see board compatibility in Simplicity Studio for `se_manager_ecjpake` / `se_manager_ecjpake_s3`).
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
3. Create the **Platform Security - SoC SE Manager Key Agreement (ECJPAKE)** project in Simplicity Studio ([Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)).
4. Build and flash the project ([Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build), [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer)).
5. Reset the board. The example runs the full client/server ECJPAKE handshake without further input.
6. Confirm the log ends with **Compare client and server derived secrets… OK**, then SE Manager deinitialization.

### Optional: change the password

Edit the `password[]` array in `app_process.c`. Client and server contexts must use the **same** pre-shared secret length and value.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM 115200 8-N-1, line terminator **None**; `SL_BOARD_ENABLE_VCOM=1` |
| SE manager init failed | Latest SE firmware; Secure Vault + SE mailbox |
| Handshake fails mid-round | SE firmware supports ECJPAKE; do not change curve/hash unless the standard allows it |
| Compare derived secrets **Failed** | Rebuild and rerun; ensure `password[]` unchanged between client and server setup |
| Example stops early | Read the last `[ERROR]` or `Failed` line in the serial log for the failing API step |
| Programming fails | AEM switch position (see Prerequisites image) |
| Slow or debug-heavy build | Default optimization is **debug (-Og)** on GCC / **None** on IAR — intentional for this example |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1271: Secure Key Storage](https://www.silabs.com/documents/public/application-notes/an1271-efr32-secure-key-storage.pdf)
- [Simplicity Studio 5 User's Guide — Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)

## Report Bugs & Get Support
You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
