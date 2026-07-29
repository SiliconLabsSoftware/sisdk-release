# Platform Security - SoC SE Manager User Data

Demonstrates how to erase and write the SE user data region and verify the contents using SE Manager user data APIs on supported Series 2 devices.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example shows how to manage the **user data** flash region in the Secure Engine using SE Manager. The demo runs **automatically** on reset (no serial menu):
1. Initialize SE Manager
2. **Erase** the full user data section (`sl_se_erase_user_data`)
3. Verify every word reads **`0xFFFFFFFF`** (erased) via `USERDATA_BASE`
4. **Write** the section with test pattern **`0x55AA55AA`** (`sl_se_write_user_data`)
5. Read back through the memory map and confirm all words match
6. Deinitialize SE Manager
**Clock-cycle counts** print when `SE_MANAGER_PRINT=1` (default).

### Device scope

**Requires:** `device_sdid_200` in the `.slcp` (early **Series 2** parts such as EFR32xG21 / MGM21 / BGM21 class devices with a user data region).
This example is **not** listed for newer Vault-only or Series 3 templates — use only on supported parts in the Studio catalog entry.

### Data layout

| Symbol | Value | Meaning |
|--------|-------|---------|
| `BLANK_DATA` | `0xFFFFFFFF` | Expected content after erase |
| `TEST_DATA` | `0x55AA55AA` | Pattern written to entire region |
| `USERDATA_SIZE` | From device headers | Full section size (word-aligned) |
Writes must be **4-byte aligned** in length and offset (see API note in `app_se_manager_user_data.h`).

### Warning

**Erasing user data clears the entire SE user data section** on the device. Use **development kits** only; production units may store application-specific data in this region.

### SE Manager APIs exercised

`sl_se_init`, `sl_se_deinit`, `sl_se_init_command_context`, `sl_se_deinit_command_context`, `sl_se_erase_user_data`, `sl_se_write_user_data`.

## Prerequisites / Setup Requirements

### Hardware Requirements

- Supported **Series 2** kit (see `se_manager_user_data` board/part compatibility in templates — e.g. xG21-family boards).
- USB for VCOM; **AEM** power when programming.

### Software Requirements

- **Simplicity Studio 5**, latest adapter and **SE firmware**.
- VCOM: **115200** 8-N-1, line terminator **None** (Device Console).

## Steps to Run Demo

1. Create the project only for a **compatible** part (project will not resolve on unsupported devices).
2. Build, flash, and open VCOM (115200 8-N-1, line terminator **None**).
3. Reset once and read the log.

### Expected console output

- `Erasing user data section...` → `Check all data... OK`
- `Writing N x 0x55AA55AA to user data...` → `Read back... OK`
- SE Manager deinitialization
Any **Failed** on blank or readback check indicates erase/write or memory-map mismatch.

### Optional: disable timing prints

Define **`SE_MANAGER_PRINT=0`** in preprocessor symbols.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM settings; `SL_BOARD_ENABLE_VCOM=1` |
| Project unavailable | Part lacks user data region / wrong `device_sdid` |
| Erase or write API error | SE firmware; command context init |
| Blank check **Failed** | Partial erase; rerun or use fresh dev device |
| Readback **Failed** | Alignment/size; do not change `USERDATA_SIZE` without updating verify loops |
| Garbled console | Line terminator **None** in Device Console |

## Resources

- [SE Manager API documentation](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager)
- [SE Manager util API](https://docs.silabs.com/gecko-platform/latest/service/api/group-sl-se-manager-util)
- [AN1222: Production Programming of Series 2 Devices](https://www.silabs.com/documents/public/application-notes/an1222-efr32xg2x-production-programming.pdf)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
