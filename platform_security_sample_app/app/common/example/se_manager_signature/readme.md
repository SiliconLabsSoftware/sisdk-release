# Platform Security - SoC SE Manager Digital Signature (ECDSA and EdDSA)

Demonstrates how to sign and verify message hashes with ECDSA and Ed25519 using plain, wrapped, or volatile SE Manager keys on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This interactive example uses SE Manager to **generate** an asymmetric key pair, **sign** a hash of a random message buffer, **export** the public key, and **verify** the signature. Output and **clock-cycle counts** appear on **VCOM** (`SE_MANAGER_PRINT=1` by default).
On reset, the app fills a **4096-byte** plain-message buffer (`PLAIN_MSG_SIZE` in `app_se_manager_signature.h`) with random data, then walks through menu selections before running sign/verify once per iteration.

### Key storage (Vault High vs Mid)

| Key type | Secure Vault **High** | Secure Vault **Mid** |
|----------|----------------------|----------------------|
| **Plaintext** in RAM | Yes | Yes |
| **Wrapped** in RAM | Yes | No |
| **Volatile** in SE slot | Yes (deleted after verify) | No |

### Algorithms and curves

**ECDSA (ECC Weierstrass Prime)**
| Curve | Availability |
|-------|----------------|
| SECP192R1, SECP256R1 | All supported Secure Vault parts |
| SECP384R1, SECP521R1, SECP256K1 (custom) | Vault **High** (not on S3 `CONFIG_301` in this example) |
**EdDSA**
| Curve | Availability |
|-------|----------------|
| **Ed25519** | **HSE** devices; requires minimum SE firmware (see below) |
For **Ed25519**, hash algorithm is not selected in the menu (EdDSA path skips SHA choice).

### Hash algorithms (ECDSA only)

| Hash | Vault Mid | Vault High |
|------|-----------|------------|
| SHA-1, SHA-224, SHA-256 | Yes | Yes |
| SHA-384, SHA-512 | No | Yes |

### Message sizes (signing length)

One of:
- `PLAIN_MSG_SIZE / 16` (256 bytes default)
- `PLAIN_MSG_SIZE / 4` (1024 bytes)
- `PLAIN_MSG_SIZE` (4096 bytes)

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_get_random`, `sl_se_validate_key`, `sl_se_get_storage_size`, `sl_se_generate_key`, `sl_se_delete_key` (Vault High), `sl_se_ecc_sign`, `sl_se_ecc_verify`.
**Requires:** `device_has_semailbox`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- Secure Vault kit with SE mailbox.
- USB for programming and VCOM.
- **AEM** power when programming.

### Software Requirements

- **Simplicity Studio 5**, latest adapter and **SE firmware**.
- VCOM: **115200** 8-N-1, line terminator **None**.

### Ed25519 SE firmware (HSE)

- **EFR32xG21:** SE firmware **v1.2.11** or higher for hardware-accelerated Ed25519
- **Other HSE devices:** SE firmware **v2.1.7** or higher

## Steps to Run Demo

1. Build, flash, and open VCOM (115200 8-N-1, line terminator **None**).
2. Reset and use the serial menus:
| Input | Action |
|-------|--------|
| **SPACE** | Cycle the current option |
| **ENTER (CR)** | Confirm and go to the next step |

### Menu sequence

**Vault High**
1. **Key type:** plaintext / wrapped / volatile
2. **Algorithm:** ECC Weierstrass Prime or EdDSA (Ed25519)
3. If Weierstrass: **curve** (P192/P256/… per device)
4. If Weierstrass: **hash** (SHA-1 … SHA-512 per device)
5. **Data length** (256 / 1024 / 4096 bytes)
6. Run: generate key → sign → export public key → verify
7. If **volatile** key: delete slot and return to main menu
**Vault Mid**
1. **Algorithm** (Weierstrass or Ed25519)
2. **Curve** (P192/P256) or Ed25519 data length only
3. **Hash** (SHA-1/224/256) for ECDSA
4. **Data length** → sign/verify with **plaintext** key only
On success, the app returns to the startup menu for another run.

### Optional: disable timing prints

Define **`SE_MANAGER_PRINT=0`** in preprocessor symbols.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM settings; `SL_BOARD_ENABLE_VCOM=1` |
| Ed25519 sign/verify fails | SE firmware version (see above); HSE-only curve |
| P384/P521/secp256k1 missing | Vault **Mid** or S3 config without High curves |
| Wrapped/volatile options missing | **Vault Mid** — plaintext only |
| Verify failed | Hash/curve mismatch; message length selection |
| Volatile key errors | Slot in use; delete step after verify |
| Garbled console | Line terminator **None** in Device Console |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [SE Manager signature API](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager-signature)
- [Asymmetric Key Handling example](https://github.com/SiliconLabs/platform-sample-apps/tree/main/app/common/example/se_manager_asymmetric_key_handling) (key generate/import patterns)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
