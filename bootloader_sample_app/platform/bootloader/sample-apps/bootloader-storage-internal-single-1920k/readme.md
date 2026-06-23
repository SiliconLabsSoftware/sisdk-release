# Internal Storage Bootloader (single slot, 1920 kB device)

Demonstrates how to configure the Gecko Bootloader to store firmware update images using internal main flash, in a single-slot setup with a 944 kB slot starting at 0x80E8000.

This project provides a **storage-based** Gecko Bootloader for Silicon Labs Series 2 SoCs that have **1920 kB of internal main flash**. The bootloader does not itself receive the upgrade image over a communication link; instead the running application downloads the GBL upgrade image (over any transport — BLE, Wi-SUN, OpenThread, Zigbee, UART, etc.) and writes it into a dedicated storage slot in internal flash. On the next reboot the bootloader verifies the image in the slot and installs it over the application. A single storage slot is configured, sized `966656` bytes (944 kB / `0xEC000`) starting at `0x80E8000`, covering `0x080E8000`–`0x081D3FFF`. The slot layout can be adjusted on the **Storage** tab of the project configurator.

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

This specific sample is configured for Silicon Labs Series 2 SoCs with **1920 kB of internal flash**. It enables exactly one storage slot (`SLOT0_ENABLE=1`) sized `966656` bytes (`0xEC000`, 944 kB), starting at `0x80E8000` (= 135168000). The base address is selected automatically by the `device_sdid_220` and `device_sdid_225` conditions in the `.slcp`, so the same project configuration builds for any 1920 kB Series 2 device of those families. The `bootloader_common_storage` component provides the storage-slot bookkeeping, `bootloader_aes_sha_ecdsa` provides secure-boot and authenticated-upgrade support, and `bootloader_token_management` preserves manufacturing tokens across upgrades.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs Series 2 SoC development kit with a part that has **1920 kB of internal flash** and is supported by the Gecko Platform SDK. The `hardware:device:flash:1920` tag and `device_sdid_220 / device_sdid_225` conditions restrict this sample to those families (typically EFR32xG23 / EFR32xG24 1.92 MB radio boards on a Wireless Pro Kit or Wireless Starter Kit mainboard).
- USB cable to the mainboard's board controller for debug access.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- A protocol SDK appropriate for your application-side DFU transport (for example the Bluetooth, Wi-SUN, OpenThread, EmberZNet, Z-Wave, or Amazon Sidewalk SDK; or just the Gecko Platform SDK if you use UART / USB).
- Simplicity Commander (for command-line flashing).

## Steps to Run Demo

1. In Simplicity Studio, create a new project from **Bootloader - SoC Internal Storage (single image on 1920kB device)** for your target Series 2 / 1920 kB SoC.
2. Build the project and flash the generated bootloader image to the kit.
3. Create the target application project (for example a Bluetooth, Wi-SUN, OpenThread, or Zigbee example that includes the **Application Bootloader Upgrade Image** / OTA DFU components, or any other application with a custom downloader). Build and flash it on top of the bootloader.
4. Generate a GBL upgrade image of a new version of the application using Simplicity Commander (`commander gbl create ...`).
5. From the running application, transport the GBL over your chosen link and write it into the storage slot using the bootloader API (`bootloader_eraseStorageSlot`, `bootloader_writeStorage`, `bootloader_verifyImage`).
6. Mark the slot as bootable and reboot into the bootloader (`bootloader_setImageToBootload`, `bootloader_rebootAndInstall`).
7. The bootloader installs the new image and boots into it automatically.

## Troubleshooting

- **Wrong-size part:** This sample assumes **1920 kB** of internal flash and is restricted to `device_sdid_220 / device_sdid_225` parts. On any other family the bootloader will fail to build or will overlap the application. Switch to the matching size variant (`...-352k`, `...-512k`, `...-768k`, `...-1016k`, `...-single` for 1024 kB, `...-1536k`, `...-2048k`, `...-3200k`).
- **Upgrade never installs after reboot:** Confirm the application called `bootloader_setImageToBootload` followed by `bootloader_rebootAndInstall`, not just a bare reset. Without the "to be bootloaded" flag, the bootloader simply jumps back into the existing application.
- **Bootloader reports an invalid image:** Make sure the GBL was generated by Simplicity Commander from the matching application version. If secure boot is enabled, the GBL must be signed with the key provisioned on the device; if encryption is enabled, it must also be encrypted with the correct key.
- **Slot write fails at a specific offset:** Verify the slot base and size against the chip's flash page boundaries — writes must be aligned and the full slot must fit inside main flash without overlapping the bootloader or application regions. The slot must end at or before `0x081D4000` (`0x80E8000 + 0xEC000`).
- **Upgrade image does not fit:** The slot is `0xEC000` bytes (944 kB) by default. If your application image plus GBL metadata exceeds that size, either enable compression (see the `-lzma` storage variant) or reduce the application footprint; on a 1920 kB part you can grow the slot somewhat by trimming the application region in the linker.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
