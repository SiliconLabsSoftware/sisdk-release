# Internal Storage Bootloader (single slot, 1 MB device)

Demonstrates how to configure the Gecko Bootloader to store firmware update images using internal main flash, in a single-slot setup with a 448 kB slot starting at 0x84000.

This project provides a **storage-based** Gecko Bootloader for Silicon Labs SoCs with **1 MB of internal flash**. The bootloader does not itself receive the upgrade image over a communication link; instead the running application downloads the GBL upgrade image (over any transport — BLE, UART, Wi-Fi, Thread, etc.) and writes it into a dedicated storage slot in internal main flash. On the next reboot the bootloader verifies the image in the slot and installs it over the application. A single storage slot is configured, 448 kB in size, starting at `0x84000` (or `0x8084000` on parts whose flash is mapped at `0x08000000`). The slot layout can be adjusted on the **Storage** tab of the project configurator.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

A storage bootloader decouples the **transport** of the upgrade image from the **installation** of the upgrade image. The application is fully responsible for getting the GBL bytes from a remote source into a reserved region of flash called a *storage slot*. Once the slot contains a complete image, the application calls into the bootloader API to mark the image as "to be bootloaded" and reboots. The bootloader then:

1. Verifies the GBL structure, CRC, and (if enabled) signature/decryption of the image in the slot.
2. Copies the contents out of the slot and into the application region.
3. Updates any preserved manufacturing tokens.
4. Resets into the newly installed application.

This specific sample is configured for Silicon Labs SoCs with **1 MB of internal flash**. It enables exactly one storage slot (`SLOT0_ENABLE=1`) sized `458752` bytes (448 kB), starting at `0x84000` on parts with a zero-based flash map or `0x8084000` on parts whose flash is mapped at `0x08000000` (the correct value is selected automatically by `device_sdid_*` conditions in the `.slcp`). The `bootloader_common_storage_single` component enforces a single-slot configuration, and `bootloader_aes_sha_ecdsa` provides secure-boot and authenticated upgrade support. `bootloader_token_management` preserves manufacturing tokens across upgrades.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs SoC development kit with a part that has **1 MB of internal flash** and is supported by the Gecko Platform SDK (the project's `hardware:device:flash:1024` tag restricts it to 1 MB parts; common targets include EFR32MG12 / EFR32BG12 / EFR32xG22 / EFR32xG24 1 MB variants).
- USB cable to the mainboard's board controller for debug access.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- A protocol SDK appropriate for your application-side DFU transport (for example the Silicon Labs Bluetooth SDK, OpenThread, EmberZNet, or simply the Gecko Platform SDK if you use UART / USB).
- Simplicity Commander (for command-line flashing).

## Steps to Run Demo

1. In Simplicity Studio, create a new project from **Bootloader - SoC Internal Storage (single image on 1MB device)** for your target 1 MB SoC.
2. Build the project and flash the generated bootloader image to the kit.
3. Create the target application project (for example a Bluetooth SoC example that includes the **Application Bootloader Upgrade Image** / OTA DFU components, or any other application with a custom downloader). Build and flash it on top of the bootloader.
4. Generate a GBL upgrade image of a new version of the application using Simplicity Commander (`commander gbl create ...`).
5. From the running application, transport the GBL over your chosen link and write it into the storage slot using the bootloader API (`bootloader_eraseStorageSlot`, `bootloader_writeStorage`, `bootloader_verifyImage`).
6. Mark the slot as bootable and reboot into the bootloader (`bootloader_setImageToBootload`, `bootloader_rebootAndInstall`).
7. The bootloader installs the new image and boots into it automatically.

## Troubleshooting

- **Device is not a 1 MB part:** This sample assumes 1 MB of internal flash and will fail link-time if the slot address / size exceeds the device's flash. Use the storage-internal-single variant that matches your part's flash size (for example `...-352k`, `...-512k`, `...-768k`, `...-1016k`, `...-1536k`, `...-1920k`, `...-2048k`, `...-3200k`).
- **Upgrade never installs after reboot:** Confirm the application called `bootloader_setImageToBootload` followed by `bootloader_rebootAndInstall`, not just a bare reset. Without the "to be bootloaded" flag, the bootloader simply jumps back into the existing application.
- **Bootloader reports an invalid image:** Make sure the GBL was generated by Simplicity Commander from the matching application version. If secure boot is enabled, the GBL must be signed with the key provisioned on the device; if encryption is enabled, it must also be encrypted with the correct key.
- **Slot write fails at a specific offset:** Verify the slot base and size against the chip's flash page boundaries — writes must be aligned and the full slot must fit inside main flash without overlapping the bootloader or application regions.
- **Upgrade image does not fit:** The slot is 448 kB by default. If your application image plus GBL metadata exceeds that size, either enable compression (see the companion `bootloader-storage-internal-single-lzma` project) or switch to a part with more flash and a larger matching sample.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
