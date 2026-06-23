# Internal Storage Bootloader (single slot, 1016 kB device)

Demonstrates how to configure the Gecko Bootloader to store firmware update images using internal main flash, in a single-slot 1016 kB layout with Slot0 at 0x78000 sized 488 kB.

This project provides a **storage-based** Gecko Bootloader for Silicon Labs Series 2 SoCs that have **1016 kB of internal main flash** (notably the EFR32xG25 / sdid 250 family). The bootloader does not itself receive the upgrade image over a communication link; instead the running application downloads the GBL upgrade image (over any transport — Wi-SUN, BLE, UART, Z-Wave, Sidewalk, etc.) and writes it into a dedicated storage slot in internal flash. On the next reboot the bootloader verifies the image in the slot and installs it over the application. A single storage slot is configured, **488 kB (0x7A000 / 499712 bytes)**, starting at `0x78000` (or `0x8078000` on parts whose flash is mapped at `0x08000000`, i.e. covering `0x08078000`–`0x080F1FFF`). The slot layout can be adjusted on the **Storage** tab of the project configurator.

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

This specific sample is configured for Silicon Labs Series 2 SoCs with **1016 kB of internal flash**. It enables exactly one storage slot (`SLOT0_ENABLE=1`) sized `499712` bytes (488 kB, `0x7A000`), starting at `0x78000` on parts with a zero-based flash map or `0x8078000` (= 134709248) on parts whose flash is mapped at `0x08000000`. The correct base address is selected automatically by the `device_sdid_250` condition in the `.slcp`, so the same project configuration builds for any 1016 kB device of that family. The `bootloader_common_storage_single` component enforces the single-slot configuration, `bootloader_aes_sha_ecdsa` provides secure-boot and authenticated-upgrade support, and `bootloader_token_management` preserves manufacturing tokens across upgrades.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs Series 2 SoC development kit with a part that has **1016 kB of internal flash** and is supported by the Gecko Platform SDK. The `hardware:device:flash:1016` tag and `device_sdid_250` condition restrict this sample to that family (typically EFR32xG25 radio boards on a Wireless Pro Kit or Wireless Starter Kit mainboard).
- USB cable to the mainboard's board controller for debug access.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- A protocol SDK appropriate for your application-side DFU transport (for example the Wi-SUN, Bluetooth, Z-Wave, or Amazon Sidewalk SDK; or just the Gecko Platform SDK if you use UART / USB).
- Simplicity Commander (for command-line flashing).

## Steps to Run Demo

1. In Simplicity Studio, create a new project from **Bootloader - SoC Internal Storage (single image on 1016kB device)** for your target Series 2 / 1016 kB SoC.
2. Build the project and flash the generated bootloader image to the kit.
3. Create the target application project (for example a Wi-SUN, Bluetooth, Z-Wave, or Sidewalk example that includes the **Application Bootloader Upgrade Image** / OTA DFU components, or any other application with a custom downloader). Build and flash it on top of the bootloader.
4. Generate a GBL upgrade image of a new version of the application using Simplicity Commander (`commander gbl create ...`).
5. From the running application, transport the GBL over your chosen link and write it into the storage slot using the bootloader API (`bootloader_eraseStorageSlot`, `bootloader_writeStorage`, `bootloader_verifyImage`).
6. Mark the slot as bootable and reboot into the bootloader (`bootloader_setImageToBootload`, `bootloader_rebootAndInstall`).
7. The bootloader installs the new image and boots into it automatically.

## Troubleshooting

- **Wrong-size part:** This sample assumes **1016 kB** of internal flash and is restricted to `device_sdid_250` parts. On any other family the bootloader will fail to build or will overlap the application. Switch to the matching size variant (`...-352k`, `...-512k`, `...-768k`, `...-single` for 1024 kB, `...-1536k`, `...-1920k`, `...-2048k`, `...-3200k`).
- **Upgrade never installs after reboot:** Confirm the application called `bootloader_setImageToBootload` followed by `bootloader_rebootAndInstall`, not just a bare reset. Without the "to be bootloaded" flag, the bootloader simply jumps back into the existing application.
- **Bootloader reports an invalid image:** Make sure the GBL was generated by Simplicity Commander from the matching application version. If secure boot is enabled, the GBL must be signed with the key provisioned on the device; if encryption is enabled, it must also be encrypted with the correct key.
- **Slot write fails at a specific offset:** Verify the slot base and size against the chip's flash page boundaries — writes must be aligned and the full slot must fit inside main flash without overlapping the bootloader or application regions. The slot must end at or before `0x080F2000` (`0x78000 + 0x7A000`).
- **Upgrade image does not fit:** The slot is 488 kB by default. If your application image plus GBL metadata exceeds that size, either enable compression (see the `-lzma` storage variant) or reduce the application footprint; on a 1016 kB part there is little room to grow the slot without shrinking the application region.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
