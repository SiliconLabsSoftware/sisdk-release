# Platform Security - SoC SE Manager Symmetric Key Handling

Demonstrates how to generate, import, export, wrap, and transfer AES and custom-size symmetric keys with SE Manager on Secure Vault devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This interactive example demonstrates **symmetric key lifecycle** operations with SE Manager: generate keys in RAM or the SE, wrap keys for storage, import/export round-trips, and transfer keys between wrapped buffers and volatile SE slots.
Output and **clock-cycle counts** appear on **VCOM** (`SE_MANAGER_PRINT=1` by default).

### Key lengths (menu)

| Selection | Size |
|-----------|------|
| **Custom** | 28 bytes (`CUSTOM_KEY_SIZE` in `app_se_manager_symmetric_key_handling.h`) |
| **AES-128** | 16 bytes |
| **AES-192** | 24 bytes |
| **AES-256** | 32 bytes |
Use **SPACE** to cycle length, **ENTER** to run the sequence for that length.

### Operations by vault level

**Secure Vault Mid**
- Generate a **plaintext** symmetric key in RAM → return to menu
**Secure Vault High** (full sequence per run)
1. **Plain key** — `sl_se_generate_key`
2. **Import / export** — import plain → wrapped, export wrapped → plain, **memcmp** verify
3. **Wrapped key** — generate non-exportable wrapped key
4. **Volatile key** — generate in SE slot, then **delete**
5. **Transfer** — wrapped → volatile slot → wrapped, then delete volatile slot → return to menu
Plaintext, wrapped, and volatile paths match the key types described in AN1271 (Secure Key Storage).
**Requires:** `device_has_semailbox`.
**Related examples:** `se_manager_block_cipher`, `se_manager_stream_cipher` (use symmetric keys for crypto); `se_manager_asymmetric_key_handling` (ECC key patterns).

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_validate_key`, `sl_se_get_storage_size`, `sl_se_generate_key`, and on **Vault High**: `sl_se_import_key`, `sl_se_export_key`, `sl_se_delete_key`, `sl_se_transfer_key`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- Secure Vault kit with SE mailbox.
- USB for programming and VCOM.
- **AEM** power when programming.

### Software Requirements

- **Simplicity Studio 5**, latest adapter and **SE firmware**.
- VCOM: **115200** 8-N-1, line terminator **None** (Device Console).

## Steps to Run Demo

1. Build, flash, and open VCOM (115200 8-N-1, line terminator **None**).
2. Reset and use the menu:
| Input | Action |
|-------|--------|
| **SPACE** | Cycle key length (Custom / AES-128 / AES-192 / AES-256) |
| **ENTER** | Run the operation sequence for the selected length |
3. On **Vault High**, watch each subsection (plain → import/export → wrapped → volatile → transfer) complete with **OK** on the export compare step.
4. When finished, the app returns to the key-length menu for another run.

### Optional: disable timing prints

Define **`SE_MANAGER_PRINT=0`** in preprocessor symbols.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM settings; `SL_BOARD_ENABLE_VCOM=1` |
| Import/export compare **Failed** | Key type or length mismatch; buffer size (`KEY_BUF_SIZE`) |
| Volatile slot errors | Prior run left slot occupied — delete step should run first |
| Transfer failures | Vault **Mid** — transfer APIs are High-only |
| Custom size issues | Must use `SL_SE_KEY_TYPE_SYMMETRIC` with 28-byte custom path |
| Garbled console | Line terminator **None** in Device Console |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [AN1271: Secure Key Storage](https://www.silabs.com/documents/public/application-notes/an1271-efr32-secure-key-storage.pdf)
- [SE Manager key handling API](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager-key-handling)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
