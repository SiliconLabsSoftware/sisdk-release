# Internal Storage Bootloader (single slot with LZMA, 1 MB device)

Demonstrates how to configure the Gecko Bootloader to store firmware update images using internal main flash, in a single-slot setup with a 448 kB slot starting at 0x84000.

This project provides a **storage-based** Gecko Bootloader for Silicon Labs Series 2 SoCs that have **1 MB (1024 kB) of internal main flash**, with the **LZMA decompression** component enabled. The bootloader receives the upgrade image indirectly: the running application downloads an **LZMA-compressed GBL** upgrade image (over any transport — BLE, Wi-SUN, OpenThread, Zigbee, UART, etc.) and writes it into a dedicated storage slot in internal flash. On the next reboot the bootloader verifies, **decompresses on the fly**, and installs the image into the application region. Compression typically lets a larger uncompressed application fit through the same slot, which is useful when the storage slot is significantly smaller than the application image. A single storage slot is configured, sized `458752` bytes (448 kB / `0x70000`) starting at `0x84000` (or `0x8084000` on parts whose flash is mapped at `0x08000000`). The slot layout can be adjusted on the **Storage** tab of the project configurator.

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
2. **Decompresses the LZMA-compressed payload** as it copies the contents out of the slot and into the application region.
3. Updates any preserved manufacturing tokens.
4. Resets into the newly installed application.

LZMA compression is the differentiator vs. the plain `bootloader-storage-internal-single` variant: the bytes stored in the slot are typically much smaller than the resulting application image, so a comparatively small slot can carry a comparatively large application. The tradeoff is somewhat slower install time (decompression cost) and slightly larger bootloader code footprint.

This specific sample is configured for Silicon Labs Series 2 SoCs with **1 MB of internal flash**. It enables exactly one storage slot (`SLOT0_ENABLE=1`) sized `458752` bytes (`0x70000`, 448 kB), starting at `0x84000` on parts with a zero-based flash map or `0x8084000` (= 134758400) on parts whose flash is mapped at `0x08000000`. The correct base address is selected automatically by `device_sdid_*` conditions in the `.slcp`, so the same project configuration builds for any 1 MB Series 2 device of those families (sdid 200, 205, 210, 215, 220, 225, 230, 235, 240, 250, 260). The `bootloader_common_storage_single` component enforces the single-slot configuration, `bootloader_compression_lzma` adds the LZMA decompressor used during install, `bootloader_image_parser` and `bootloader_image_parser_nonenc` provide GBL parsing, `bootloader_aes_sha_ecdsa` provides secure-boot and authenticated-upgrade support, and `bootloader_token_management` preserves manufacturing tokens across upgrades.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs Series 2 SoC development kit with a part that has **1024 kB (1 MB) of internal flash** and is supported by the Gecko Platform SDK. The `hardware:device:flash:1024` tag and `device_sdid_200..260` conditions restrict this sample to those families (typically EFR32MG21 / xG22 / xG23 / xG24 / xG25 / xG27 / xG28 1 MB SKUs on a Wireless Pro Kit or Wireless Starter Kit mainboard).
- USB cable to the mainboard's board controller for debug access.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- A protocol SDK appropriate for your application-side DFU transport (for example the Bluetooth, Wi-SUN, OpenThread, EmberZNet, Z-Wave, or Amazon Sidewalk SDK; or just the Gecko Platform SDK if you use UART / USB).
- **Simplicity Commander** with LZMA compression support (used to generate `--compress lzma` GBL upgrade images).

## Steps to Run Demo

1. In Simplicity Studio, create a new project from **Bootloader - SoC Internal Storage (single image with LZMA compression, 1MB flash)** for your target Series 2 / 1 MB SoC.
2. Build the project and flash the generated bootloader image to the kit.
3. Create the target application project (for example a Bluetooth, Wi-SUN, OpenThread, or Zigbee example that includes the **Application Bootloader Upgrade Image** / OTA DFU components, or any other application with a custom downloader). Build and flash it on top of the bootloader.
4. Generate an **LZMA-compressed** GBL upgrade image of a new version of the application using Simplicity Commander, e.g. `commander gbl create app.gbl --app app.s37 --compress lzma`.
5. From the running application, transport the compressed `.gbl` over your chosen link and write it into the storage slot using the bootloader API (`bootloader_eraseStorageSlot`, `bootloader_writeStorage`, `bootloader_verifyImage`).
6. Mark the slot as bootable and reboot into the bootloader (`bootloader_setImageToBootload`, `bootloader_rebootAndInstall`).
7. The bootloader verifies the image, decompresses the payload, installs the new application, and boots into it automatically.

## Troubleshooting

- **Wrong-size part:** This sample assumes **1024 kB (1 MB)** of internal flash and is restricted to `device_sdid_200..260` parts. On any other family the bootloader will fail to build or will overlap the application. Switch to the matching size variant (`...-352k`, `...-512k`, `...-768k`, `...-1016k`, `...-single` for plain 1024 kB, `...-1536k`, `...-1920k`, `...-2048k`, `...-3200k`).
- **Bootloader rejects the image with a parser error:** Make sure the GBL was generated **with LZMA compression** (`--compress lzma` in `commander gbl create`). A plain (non-compressed) GBL is also accepted by this build, but a GBL compressed with a different scheme (e.g. raw) will be rejected.
- **Decompressed application doesn't fit:** Even though the compressed slot is only 448 kB, the **decompressed** application still has to fit inside the application region of flash (everything below the slot, minus reserved areas). If the install fails near the end with an out-of-flash error, the post-decompression image is too large for the part — either trim the application or move to a larger-flash part with the matching variant.
- **Upgrade never installs after reboot:** Confirm the application called `bootloader_setImageToBootload` followed by `bootloader_rebootAndInstall`, not just a bare reset. Without the "to be bootloaded" flag, the bootloader simply jumps back into the existing application.
- **Bootloader reports an invalid signature:** If secure boot is enabled, the GBL must be signed with the key provisioned on the device; the LZMA payload must be signed as part of the GBL, not separately. Generate the GBL with the appropriate Commander signing options.
- **Slot write fails at a specific offset:** Verify the slot base and size against the chip's flash page boundaries — writes must be aligned and the full slot must fit inside main flash without overlapping the bootloader or application regions. The slot must end at or before `0xF4000` (`0x84000 + 0x70000`), or `0x080F4000` on parts mapped at `0x08000000`.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
