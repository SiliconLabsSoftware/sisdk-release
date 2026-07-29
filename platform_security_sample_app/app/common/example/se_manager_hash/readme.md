# Platform Security - SoC SE Manager Hash

Demonstrates how to compute message digests with the SE Manager Hash API, exercising SHA-1 and SHA-2 in one-shot and streaming modes with test-vector verification on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example exercises the **SE Manager Hash API** on a Secure Vault device. It fills a message buffer with random data, computes a **one-shot** hash over a selected payload length, then runs a **streaming** hash over a fixed test vector and compares the result to known expected digests.
Output is on the kit **VCOM** port, with **clock-cycle counts** per operation when `SE_MANAGER_PRINT=1` (default).

### Interactive menu

- **SPACE** — cycle the current option
- **ENTER (CR)** — confirm and proceed
1. **Payload size:** 256, 1024, or 4096 bytes (`MSG_SIZE` = 4096 in `app_process.h`)
2. **Hash algorithm:** SHA-1, SHA-224, SHA-256; on **Secure Vault High** also SHA-384 and SHA-512

### Tests performed

| Phase | What it does |
|-------|----------------|
| **One-shot hash** | `sl_se_hash` over `msg_size` bytes of random data from `msg_buf`; prints digest in hex |
| **Streaming hash** | `sl_se_hash_starts` / algorithm-specific `sl_se_hash_sha*_starts`, `sl_se_hash_update`, `sl_se_hash_finish` over the standard test string `abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq` |
| **Verify** | Compare streaming digest to built-in expected values for the selected algorithm (prints **OK** or **Failed**) |
After a successful compare, the menu returns so you can run again with different settings.
**Components used:** `se_manager`, `sl_main`, `device_init`, `clock_manager`, VCOM stdio retargeting. Requires **`device_has_semailbox`**.

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_get_random`, `sl_se_hash`, `sl_se_hash_starts`, `sl_se_hash_sha1_starts`, `sl_se_hash_sha224_starts`, `sl_se_hash_sha256_starts`, `sl_se_hash_sha384_starts` (Vault High), `sl_se_hash_sha512_starts` (Vault High), `sl_se_hash_update`, `sl_se_hash_finish`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- A **Secure Vault** development kit with SE mailbox support (see board compatibility in Simplicity Studio for `se_manager_hash` / `se_manager_hash_s3`).
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
3. Create the **Platform Security - SoC SE Manager Hash** project in Simplicity Studio ([Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)).
4. Build and flash the project ([Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build), [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer)).
5. Reset the board. The example initializes SE Manager and fills the message buffer with random data.
6. Use **SPACE** / **ENTER** to choose **payload size**, then **hash algorithm**.
7. Watch the log for:
   - One-shot hash over random data (hex digest printed)
   - Streaming hash over the test vector (hex digest printed)
   - **Comparing … hash value with expected data… OK**
8. The size/hash menu reappears for another run.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM 115200 8-N-1, line terminator **None**; `SL_BOARD_ENABLE_VCOM=1` |
| SE manager init failed | Latest SE firmware; Secure Vault + SE mailbox |
| Random buffer fill failed | SE random source available |
| One-shot hash failed | Payload size within `MSG_SIZE`; supported algorithm on your Vault tier |
| Streaming compare **Failed** | Algorithm must match expected test-vector digest; retry with SHA-1/224/256 on Vault Mid |
| SHA-384/512 not in menu | Vault Mid supports SHA-1, SHA-224, SHA-256 only |
| Programming fails | AEM switch position (see Prerequisites image) |
| Slow or debug-heavy build | Default optimization is **debug (-Og)** on GCC / **None** on IAR — intentional for this example |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1271: Secure Key Storage](https://www.silabs.com/documents/public/application-notes/an1271-efr32-secure-key-storage.pdf)
- [Simplicity Studio 5 User's Guide — Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
