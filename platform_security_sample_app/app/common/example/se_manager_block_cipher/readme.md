# Platform Security - SoC SE Manager Block Cipher

Demonstrates how to encrypt and decrypt data with the SE Manager Block Cipher API, exercising AES ECB/CTR/CBC/CFB/CCM/GCM, CMAC, HMAC, and ChaCha20-Poly1305 on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example exercises the **SE Manager block-cipher and MAC APIs** on a Secure Vault device. Standard I/O is redirected to the kit **VCOM** port. Each operation reports **clock-cycle counts** when `SE_MANAGER_PRINT=1` (default).
After reset, the application fills random **IV/nonce**, **associated data**, and **plaintext** buffers, then walks you through configuration menus before running a fixed sequence of encrypt/decrypt (or MAC) tests and verifying decrypted output matches the original plaintext.

### Interactive menu

- **SPACE** — cycle the current option
- **ENTER (CR)** — confirm and proceed
**Secure Vault High** — select in order:
1. **Key storage:** plaintext, wrapped, or volatile SE slot
2. **Key length:** 128, 192, or 256 bits
3. **Payload size:** 256, 1024, or 4096 bytes (`PLAIN_MSG_SIZE` = 4096 in `app_se_manager_block_cipher.h`)
4. **HMAC hash:** SHA-1, SHA-224, SHA-256, SHA-384, or SHA-512
**Secure Vault Mid** — select key length, payload size, and HMAC hash (SHA-1/224/256 only); keys are **plaintext in RAM** only.

### Algorithms exercised (automatic test sequence)

| Test | Operation |
|------|-----------|
| **AES ECB** | Encrypt / decrypt |
| **AES CTR** | Encrypt / decrypt |
| **AES CCM** | Encrypt+tag / authenticated decrypt |
| **AES GCM** | Encrypt+tag / authenticated decrypt |
| **AES CBC** | Encrypt / decrypt |
| **AES CFB8** | Encrypt / decrypt |
| **AES CFB128** | Encrypt / decrypt |
| **AES CMAC** | 16-byte MAC generation |
| **HMAC** | MAC with selected SHA variant |
| **ChaCha20-Poly1305** | Poly1305 MAC + encrypt/decrypt (**Secure Vault High only**, not on all Series 3 parts) |
**Key sizes:** AES-128, AES-192, AES-256. **ChaCha20-Poly1305** requires a **256-bit** key (the example switches automatically if needed).
**Components used:** `se_manager`, `sl_main`, `device_init`, `clock_manager`, VCOM stdio retargeting. Requires **`device_has_semailbox`**.

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_get_random`, `sl_se_validate_key`, `sl_se_get_storage_size`, `sl_se_generate_key`, `sl_se_delete_key` (Vault High), `sl_se_aes_crypt_ecb`, `sl_se_aes_crypt_ctr`, `sl_se_ccm_encrypt_and_tag`, `sl_se_ccm_auth_decrypt`, `sl_se_gcm_crypt_and_tag`, `sl_se_gcm_auth_decrypt`, `sl_se_aes_crypt_cbc`, `sl_se_aes_crypt_cfb8`, `sl_se_aes_crypt_cfb128`, `sl_se_cmac`, `sl_se_hmac`, `sl_se_poly1305_genkey_tag`, `sl_se_chacha20_poly1305_encrypt_and_tag`, `sl_se_chacha20_poly1305_auth_decrypt`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- A **Secure Vault** development kit with SE mailbox support (see board compatibility in Simplicity Studio for `se_manager_block_cipher` / `se_manager_block_cipher_s3`).
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
3. Create the **Platform Security - SoC SE Manager Block Cipher** project in Simplicity Studio ([Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)).
4. Build and flash the project ([Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build), [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer)).
5. Reset the board. The application initializes SE Manager and fills random buffers.
6. Use **SPACE** / **ENTER** to configure key type (Vault High), key length, payload size, and HMAC hash algorithm.
7. Watch the serial log as each algorithm test runs (encrypt/decrypt or MAC generation). Each test verifies decrypted plaintext matches the original buffer.
8. When the full sequence completes, the menu reappears so you can run again with different settings.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM 115200 8-N-1, line terminator **None**; `SL_BOARD_ENABLE_VCOM=1` |
| SE manager init failed | Latest SE firmware; board has Secure Vault + SE mailbox |
| Random buffer fill failed | SE random source / TRNG availability |
| Wrapped or volatile key options missing | Expected on **Secure Vault Mid** — use a Vault High board for full key-storage paths |
| ChaCha20-Poly1305 test skipped | Vault High required; not available on all Series 3 config parts |
| Decrypt compare failed | Retry with smaller payload size; confirm SE firmware is current |
| SHA-384/512 not in HMAC menu | Vault Mid supports SHA-1/224/256 only |
| Programming fails | AEM switch position (see Prerequisites image) |
| Slow or debug-heavy build | Default optimization is **debug (-Og)** on GCC / **None** on IAR — intentional for this example |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1271: Secure Key Storage](https://www.silabs.com/documents/public/application-notes/an1271-efr32-secure-key-storage.pdf)
- [Simplicity Studio 5 User's Guide — Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).

