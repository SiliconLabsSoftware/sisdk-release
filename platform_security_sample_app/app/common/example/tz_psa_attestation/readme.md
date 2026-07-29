# TrustZone PSA Attestation (Workspace and Secure Application)

## High-Level Overview

Demonstrates how to build a TrustZone-split PSA Attestation application, in a platform security TrustZone SoC workspace combining the Secure and Non-secure halves into one signed image.

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example splits a PSA Attestation application across the TrustZone security boundary on Series 2 Secure Vault devices. The Simplicity IDE uses the `tz_psa_attestation_ws` workspace to generate two paired projects:

- **`tz_psa_attestation_s`** (Secure application) — builds a TrustZone secure library that runs PSA Crypto and the Attestation service in the Secure world and exposes them to Non-secure code through Non-secure Callable (NSC) veneers. Services published include `Attestation`, `MSC`, `NVM3`, `PSA Crypto`, `PSA ITS`, `SE Manager`, and `SYSCFG`. The Secure half owns trust-anchor material and operations that must stay private to the Secure world.
- **`tz_psa_attestation_ns`** (Non-secure application) — drives the demo, calls the attestation veneer to generate a PSA Initial Attestation Token, and prints the resulting token in a human-readable format over VCOM. See [`tz_psa_attestation_ns/readme.md`](tz_psa_attestation_ns/readme.md) for the Non-secure-side details.

After both projects build, the workspace's `tz_application_sign` post-build action:

1. Combines the Secure and Non-secure binaries into a single image.
2. Signs the combined image with `example_signing_key.pem` (located in the Secure project's `autogen/` folder).

The image must be signed because PSA Attestation uses **Secure Boot** as the root of trust — the device will refuse to attest if `SECURE_BOOT_ENABLE` in SE OTP is disabled, or if the public key on the device does not match the signing key.

### Secure-side Components

The Secure project (`tz_psa_attestation_s.slcp`) brings in:

- `trustzone_secure` and `tz_secure_key_library` — the TrustZone secure-library wrapper that exposes NSC veneers and links the secure-side PSA Crypto and Attestation services.
- A flash layout that places the Secure application at the start of flash (`0x0` on Series 2 xG21/xG24, `0x08000000` on memory-mapped parts), with a `memory_flash_size` of `0x2C000` (176 KB) and `memory_ram_size` of `0x3000` (12 KB).
- Stack/heap defaults of `SL_STACK_SIZE = 3072` and `SL_HEAP_SIZE = 4096`, sized for the attestation + PSA Crypto + SE Manager service surface.
- `BOOTLOADER_DISABLE_OLD_BOOTLOADER_MITIGATION = 1` to opt out of the legacy bootloader compatibility hop on Series 2.
- `application_type = APPLICATION_TYPE_MCU` when `bootloader_app_properties` is present, so a Gecko Bootloader can identify the image.

### Post-build Profiles

- Secure project: `tz_secure_application` — emits the secure-library object (`artifact/trustzone_secure_library.o`) that the Non-secure project consumes.
- Non-secure project: `tz_nonsecure_application` — links against the Secure-side veneer object.
- Workspace: `tz_application_sign` — combines + signs the two halves into the final image.

## Prerequisites / Setup Requirements

### Hardware

- A Silicon Labs Series 2 **Secure Vault** development kit (radio board + mainboard, or a Pro Kit). Series 2 TrustZone support is required.
- USB cable from the kit's board controller to the host PC (provides debug access and the VCOM UART bridge).
- The mainboard's power-supply switch must be in the **AEM** position when programming.

### Software

- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- Up-to-date **Adapter Firmware** on the kit and up-to-date **SE Firmware** on the device (both reachable from the Launcher's General Device Information panel).
- A serial terminal (Tera Term, PuTTY, or Studio's built-in `Device Console`) configured for **115200 baud, 8-N-1**, line terminator `None`.
- Simplicity Commander (optional, for command-line flashing and Secure Boot key provisioning).

## Steps to Run Demo

1. **Update firmware.** From the Simplicity Studio Launcher, update **Adapter Firmware** and **Secure Firmware** to the latest versions for your kit.
2. **Provision Secure Boot.** Confirm that `SECURE_BOOT_ENABLE` is set in SE OTP, and that the Secure Boot public key on the device matches the private key in `tz_psa_attestation_s/autogen/example_signing_key.pem`. Refer to **AN1218: Series 2 Secure Boot with RTSL** for first-time provisioning.
3. **Create the projects from the workspace.** In Studio, open the **Example Projects & Demos** picker, select your kit, find **TrustZone PSA Attestation** (the `tz_psa_attestation_ws` workspace), and create both projects (`tz_psa_attestation_s` and `tz_psa_attestation_ns`) into your workspace.
4. **Build the Secure project.** Build `tz_psa_attestation_s` first; this produces the secure library object (`artifact/trustzone_secure_library.o`) that the Non-secure project consumes.
5. **Build the Non-secure project.** Build `tz_psa_attestation_ns`. The workspace dependency pulls in the Secure library, and the `tz_application_sign` post-build profile combines and signs both halves into a single image.
6. **Flash the combined image.** Use the **Debug** or **Flash Programmer** action on the Non-secure project, or flash the combined `.s37`/`.hex` from `tz_psa_attestation_ns/artifact/` with Simplicity Commander.
7. **Open VCOM.** Connect to the kit's VCOM port at **115200 baud, 8-N-1**, line terminator `None`.
8. **Run.** Reset the kit; the example prints the generated PSA Attestation token over VCOM. Follow the on-screen prompts.

## Troubleshooting

- **No console output / garbled output** — confirm 115200 baud, 8-N-1, and line terminator `None` (especially in Studio's Device Console).
- **Programming fails / kit not detected** — make sure the mainboard's power switch is in the **AEM** position and the USB cable is connected to the board-controller port.
- **Device resets at boot / Secure Boot rejection** — the combined image's signature does not match the Secure Boot public key in SE OTP, or `SECURE_BOOT_ENABLE` is not set. Re-provision per AN1218, or rebuild with a signing key that matches the device.
- **Attestation veneer returns an error** — same root cause as the Secure Boot rejection (attestation refuses to run if the device cannot prove its identity), or the SE firmware is too old for the attestation service. Update Secure Firmware from the Launcher.
- **Secure project build fails with linker errors about `trustzone_secure_library.o`** — the Secure project did not finish building, or the `tz_secure_application` post-build profile failed. Build the Secure project standalone first to surface the underlying error.
- **Non-secure project cannot find the veneer object** — same root cause; the Secure-side `export: library: - path: artifact/trustzone_secure_library.o` was not produced.
- **`tz_application_sign` post-build fails** — `example_signing_key.pem` was deleted or replaced, or the signing tool is missing from your Simplicity Commander installation. Re-create the project or reinstall Commander.
- **Stack overflow in the Secure world** — raise `SL_STACK_SIZE` in `tz_psa_attestation_s.slcp` (default `3072`); the attestation flow exercises several PSA Crypto services in sequence.
- **SE firmware too old** — update Secure Firmware from the Launcher and rerun.

## Resources

- [AN1374: Series 2 TrustZone](https://www.silabs.com/documents/public/application-notes/an1374-trustzone.pdf)
- [AN1218: Series 2 Secure Boot with RTSL](https://www.silabs.com/documents/public/application-notes/an1218-secure-boot-with-rtsl.pdf)
- [Simplicity Studio 5 User's Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you find via the [Silicon Labs Community](https://community.silabs.com/).
