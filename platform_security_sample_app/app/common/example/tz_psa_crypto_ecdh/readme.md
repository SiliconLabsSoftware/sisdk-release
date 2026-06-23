# TrustZone PSA Crypto ECDH (Workspace and Secure Application)

Demonstrates how to build a TrustZone-split PSA Crypto ECDH key-agreement application as a unified workspace, combining the Secure and Non-secure halves into one image.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example splits a PSA Crypto ECDH key-agreement application across the TrustZone security boundary on Series 2 devices. The Simplicity IDE uses the `tz_psa_crypto_ecdh_ws` workspace to generate two paired projects:

- **`tz_psa_crypto_ecdh_s`** (Secure application) — builds a TrustZone secure library that runs PSA Crypto in the Secure world and exposes it to Non-secure code through Non-secure Callable (NSC) veneers. Services published include `Attestation`, `MSC`, `NVM3`, `PSA Crypto`, `PSA ITS`, `SE Manager`, and `SYSCFG`. ECDH private keys and the key-agreement primitive itself live behind the NSC boundary so private bytes are never exposed to the Non-secure world.
- **`tz_psa_crypto_ecdh_ns`** (Non-secure application) — drives the demo, performs ECDH key agreement between two simulated peers (client and server) by calling the PSA Crypto veneer, and prints public keys and the derived shared secret over VCOM. See [`tz_psa_crypto_ecdh_ns/readme.md`](tz_psa_crypto_ecdh_ns/readme.md) for the Non-secure-side details.

After both projects build, the workspace's `tz_application` post-build action combines the Secure and Non-secure binaries into a single image for flashing. Unlike `tz_psa_attestation`, this workspace does **not** sign the combined image — Secure Boot provisioning is not required to run it.

### Curves Exercised

The Non-secure side exercises the following curves through the Secure-side PSA Crypto veneer:

- SECP R1 — `secp192r1`, `secp256r1`, `secp384r1`, `secp521r1` (all Series 2 TrustZone parts)
- Montgomery — `Curve25519` (all Series 2 TrustZone parts), `Curve448` (Secure Vault parts only, gated via `requires: condition: [device_security_vault]`)

### Secure-side Components

The Secure project (`tz_psa_crypto_ecdh_s.slcp`) brings in:

- `trustzone_secure` and `tz_secure_key_library` — the TrustZone secure-library wrapper that exposes NSC veneers and links the secure-side PSA Crypto stack.
- A flash layout that places the Secure application at the start of flash (`0x0` on Series 2 xG21/xG24, `0x08000000` on memory-mapped parts), with a `memory_flash_size` of `0x2C000` (176 KB) and `memory_ram_size` of `0x3000` (12 KB).
- Stack/heap defaults of `SL_STACK_SIZE = 3072` and `SL_HEAP_SIZE = 4096`, sized for the PSA Crypto + ECDH service surface. Larger curves (`secp521r1`, `Curve448`) push these close to the limit if the demo is extended.
- `BOOTLOADER_DISABLE_OLD_BOOTLOADER_MITIGATION = 1` to opt out of the legacy bootloader compatibility hop on Series 2.
- `application_type = APPLICATION_TYPE_MCU` when `bootloader_app_properties` is present, so a Gecko Bootloader can identify the image.

### Post-build Profiles

- Secure project: `tz_secure_application` — emits the secure-library object (`artifact/trustzone_secure_library.o`) that the Non-secure project consumes.
- Non-secure project: `tz_nonsecure_application` — links against the Secure-side veneer object.
- Workspace: `tz_application` — combines the two halves into the final image (unsigned).

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 2 development kit (radio board + mainboard, or a Pro Kit) supported by the Gecko Platform SDK. A **Secure Vault** part is required to exercise `Curve448`; the SECP and `Curve25519` paths run on any Series 2 device with TrustZone support.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device (both reachable from the Launcher's General Device Information panel).
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- Simplicity Commander (optional, for command-line flashing).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit.
2. **Create the projects from the workspace.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **TrustZone PSA Crypto ECDH** (the `tz_psa_crypto_ecdh_ws` workspace), and create both projects (`tz_psa_crypto_ecdh_s` and `tz_psa_crypto_ecdh_ns`) into your workspace.
3. **Build the Secure project.** Build `tz_psa_crypto_ecdh_s` first; this produces the secure library object (`artifact/trustzone_secure_library.o`) that the Non-secure project consumes.
4. **Build the Non-secure project.** Build `tz_psa_crypto_ecdh_ns`. The workspace dependency pulls in the Secure library, and the `tz_application` post-build profile combines both halves into a single image.
5. **Flash the combined image.** Use the **Debug** or **Flash Programmer** action on the Non-secure project, or flash the combined `.s37`/`.hex` from `tz_psa_crypto_ecdh_ns/artifact/` with Simplicity Commander.
6. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
7. **Run.** Reset the kit; the example walks through ECDH key agreement on each supported curve, prints the public keys and the derived shared secret per peer, and confirms the two peers' secrets match. Follow the on-screen prompts.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **Secure project build fails with linker errors about `trustzone_secure_library.o`** — the Secure project did not finish building, or the `tz_secure_application` post-build profile failed. Build the Secure project standalone first to surface the underlying error.
- **Non-secure project cannot find the veneer object** — same root cause; the Secure-side `export: library: - path: artifact/trustzone_secure_library.o` was not produced.
- **`Curve448` path returns `PSA_ERROR_NOT_SUPPORTED`** — `Curve448` requires a **Secure Vault** part; the `.slcp` adds `psa_crypto_ecc_curve448` conditionally on `device_security_vault`. On non-Vault Series 2 parts the example will skip that curve.
- **`PSA_ERROR_INSUFFICIENT_MEMORY` or stack overflow** — the Secure project defaults to `SL_STACK_SIZE = 3072` and `SL_HEAP_SIZE = 4096`. Larger curves (`secp521r1`, `Curve448`) push these close to the limit if you extend the example; raise the values in the project configurator.
- **Client and server shared secrets do not match** — heap exhaustion (silent truncation) or a modification to the key-agreement flow. Run with `PSA_CRYPTO_PRINT=1` to inspect each step.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1374: Series 2 TrustZone](https://www.silabs.com/documents/public/application-notes/an1374-trustzone.pdf)
- [PSA Crypto API specification (Arm)](https://arm-software.github.io/psa-api/crypto/)
- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
