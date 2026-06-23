# Internal Storage Bootloader (Single Image, 3 MB) — Series 3

Demonstrates how to configure the Gecko Bootloader to store firmware update images in flash, in a single-slot setup with a 1180 kB slot starting at 0x01168000.

This sample provides a standalone Gecko Bootloader for **Series 3** SoCs with **3 MB main flash**, configured to hold **one** firmware update image at a time in internal flash. The bootloader is application-triggered: an application running on the device receives a `.gbl` upgrade image over whatever transport it natively uses (Bluetooth, Wi-Fi, Connect, custom, etc.), writes it into the storage slot using the Gecko Bootloader interface, sets the install flag, and reboots. On the next reset the bootloader inspects the slot, validates the GBL, applies it to the application region, and jumps into the new application. The single-slot layout maximizes the size of the image you can stage on a 3 MB device — useful when application size is the dominant constraint and rollback / A-B updates are not required.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This is the single-image internal-storage variant for Series 3 SoCs with 3 MB main flash. It targets users who want to deliver firmware updates without an external SPI flash, who do not need to keep more than one image on the device at a time, and who want as much room as possible for the staged GBL on a mid-sized-flash part — typical for OTA / DFU schemes that can re-download on failure but cannot afford to halve the available storage by carrying a second slot.

The configured layout is:

- **Storage**: internal main flash, **single slot**.
- **Slot 0**: enabled, **1180 kB (0x127000 / 1208320 bytes)**, starting at **`0x01168000`** and ending at **`0x0128F000`**.
- The application image runs from the lower portion of the same flash; the application linker file must place code below `0x01168000`, leaving room for the application proper, manufacturing tokens, and any NVM3 region.

The bootloader does **not** include any UART, SPI, or Bluetooth communication components — application-triggered updates via the Bootloader Application Interface (`btl_storage` / `btl_application_interface` APIs) are the only update path. Whatever protocol your application uses to download the GBL is up to you.

How this variant fits in with the other Series 3 storage samples:

- **`bootloader-storage-single-2048k`** — single 792 kB slot for 2 MB-flash parts.
- **`bootloader-storage-single-3072k`** (this sample) — single 1180 kB slot for 3 MB-flash parts.
- **`bootloader-storage-single`** — single 1024 kB slot for 4 MB-flash parts.
- **`bootloader-storage-multi-4096k`** — two 756 kB slots for 4 MB-flash parts (rollback / A-B style updates).

Use the project configurator's *Storage* tab to verify the slot start / size match your application's linker layout — if your application linker file places code above `0x01168000`, the slot will collide with the application image.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs **Series 3** SoC development kit with **3 MB main flash** (radio board + mainboard, or a pro kit) supported by the Gecko Platform SDK.
- USB cable to the kit's mainboard for debug access; UART debug output (if enabled by the application) is routed through VCOM.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- The application sample / firmware that will trigger the update through the Bootloader Application Interface.
- Simplicity Commander (for command-line flashing and creating signed `.gbl` images of the application).

## Steps to Run Demo

1. In Simplicity Studio, create a new project from the **Bootloader - SoC Storage (single OTA image of size 1180kB for 3MB flash)** entry for your target Series 3 part.
2. Open the *Storage* tab in the project configurator and verify the slot configuration:
   - Slot 0 → start `0x01168000`, size `0x127000` (1180 kB), end `0x0128F000`.
   Adjust if your application's linker layout requires it; the application region must end below `0x01168000`.
3. Build the project and flash the generated bootloader image to the SoC.
4. Build your application, ensuring its linker script reserves the application region below `0x01168000` and that it includes the Bootloader Application Interface so it can call `bootloader_eraseStorageSlot()` / `bootloader_writeStorage()` / `bootloader_setImageToBootload()` / `bootloader_rebootAndInstall()`.
5. Flash the application on top of the bootloader.
6. Run the application. When it has a new `.gbl` image to apply, it writes the image into Slot 0, marks the slot as the install target, and reboots.
7. On the next reset, the Gecko Bootloader validates the GBL in Slot 0, copies it into the application region, and jumps into the new application.

To validate the storage layout independently from the application, you can also generate a `.gbl` from a known-good application binary with Simplicity Commander, write it into Slot 0 with `commander flash --address 0x01168000`, and reboot.

## Troubleshooting

- **Build errors / target rejected:** Verify the part has 3 MB main flash. Smaller-flash variants in the same family will not have a valid memory range at `0x0128F000` (the end of Slot 0).
- **Application linker errors / overlapping regions:** The application region must end below `0x01168000`. If the linker reports overlap with the storage region, either shrink the application or move the slot — but make sure the application region and Slot 0 do not overlap, and that there is room reserved for manufacturing tokens at the top of flash.
- **Application does not start after upgrade:** Confirm the application image was built against the same bootloader interface (matching SDK version) and, if secure boot is enabled, that the GBL is signed with the key provisioned on the device.
- **Bootloader rejects the GBL:** Verify the GBL was generated by Simplicity Commander from the matching application image. If anti-rollback / image-version metadata is enforced, ensure the new image's version is greater than (or equal to) the running version where required.
- **`bootloader_setImageToBootload()` fails:** With a single-slot layout the only valid `slot_id` is `0`. Calling the API with any other value returns an error.
- **Tokens / NVM3 erased after re-flashing:** Use Simplicity Commander's options to preserve manufacturing tokens / NVM3 regions, or reconfigure the storage layout in the project configurator to leave room for them.
- **`btl_storage_*` API calls return error from the application:** Ensure the application's bootloader interface library matches this bootloader's SDK version. A mismatch between application-side `btl_application_interface` and the running bootloader is the most common cause.
- **Need a different flash size:** Use `bootloader-storage-single-2048k` (792 kB slot, 2 MB parts), `bootloader-storage-single` (1024 kB slot, 4 MB parts), or `bootloader-storage-multi-4096k` (dual 756 kB slots, 4 MB parts) — those variants are tuned for their respective flash address ranges.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
