# Platform Security - SoC SE Manager Stream Cipher

Demonstrates how to run streaming AES-CMAC, AES-GCM, and ChaCha20 self-tests with SE Manager starts/update/finish APIs and known test vectors on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example exercises **multi-part (streaming)** symmetric operations through SE Manager using **fixed test vectors**. It runs **automatically** on reset (no serial menu). Each step compares SE output to expected tags or ciphertext/plaintext and prints **OK** or **Failed** on VCOM. **Clock-cycle counts** print when `SE_MANAGER_PRINT=1` (default).
After SE Manager init, the app creates a **256-bit AES plaintext key** in RAM, then runs:
| Test | API pattern | What is verified |
|------|-------------|------------------|
| **AES-CMAC** | `sl_se_cmac_starts` / `update` / `finish` | 16-byte CMAC tag (NIST-style vector, 40-byte message in 16-byte chunks) |
| **AES-GCM encrypt** | `sl_se_gcm_starts` / `update` / `finish` | Ciphertext + 16-byte tag (with IV and AAD) |
| **AES-GCM decrypt** | Same streaming decrypt path | Recovered plaintext + tag check |
| **ChaCha20 encrypt/decrypt** | `sl_se_chacha20_crypt` (block-wise) | Ciphertext then plaintext (RFC-style vector) |

### Algorithm availability

| Algorithm | Secure Vault **Mid** | Secure Vault **High** |
|-----------|---------------------|----------------------|
| AES-CMAC (streaming) | Yes | Yes |
| AES-GCM (streaming encrypt/decrypt) | Yes | Yes |
| ChaCha20 (streaming) | No | Yes (not built for **Series 3 CONFIG_301** in this example) |
Keys and payloads are embedded in `app_process.c` (CMAC/GCM/ChaCha20 test vectors).
**Requires:** `device_has_semailbox`.
**Note:** For **interactive** AES modes, AEAD, and ChaCha20-Poly1305 menus, see `se_manager_block_cipher`.

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_validate_key`, `sl_se_get_storage_size`, `sl_se_generate_key`, `sl_se_cmac_starts`, `sl_se_cmac_update`, `sl_se_cmac_finish`, `sl_se_gcm_starts`, `sl_se_gcm_update`, `sl_se_gcm_finish`, `sl_se_chacha20_crypt` (Vault High, when enabled).

## Prerequisites / Setup Requirements

### Hardware Requirements

- Secure Vault kit with SE mailbox.
- USB for programming and VCOM.
- **AEM** power when programming.

### Software Requirements

- **Simplicity Studio 5**, latest adapter and **SE firmware**.
- VCOM: **115200** 8-N-1, line terminator **None** (Device Console).

## Steps to Run Demo

1. Create the project for your Secure Vault target and build.
2. Flash to the kit and open VCOM (115200 8-N-1, line terminator **None**).
3. Reset the board and watch the log.

### Expected console flow

1. SE Manager initialization and symmetric key setup
2. **AES CMAC streaming test** → tag compare → `OK`
3. **AES GCM encryption streaming test** → ciphertext + tag → `OK`
4. **AES GCM decryption streaming test** → plaintext → `OK`
5. On supported Vault High targets: **ChaCha20 encryption** then **decryption** → `OK`
6. SE Manager deinitialization
No user input is required. Any `Failed` line indicates a mismatch with the embedded vector.

### Optional: disable timing prints

Define **`SE_MANAGER_PRINT=0`** in preprocessor symbols.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM settings; `SL_BOARD_ENABLE_VCOM=1` |
| CMAC or GCM **Failed** | SE firmware version; key/vector mismatch after local edits |
| No ChaCha20 section | **Vault Mid**, or **S3 CONFIG_301** build (ChaCha20 omitted in firmware) |
| ChaCha20 **Failed** | Counter/nonce handling; do not modify test vectors without updating expected ciphertext |
| Garbled console | Line terminator **None** in Device Console |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [SE Manager cipher API](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager-cipher)
- [Block Cipher example](https://github.com/SiliconLabs/platform-sample-apps/tree/main/app/common/example/se_manager_block_cipher) (interactive AES/AEAD/ChaCha20-Poly1305)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).

