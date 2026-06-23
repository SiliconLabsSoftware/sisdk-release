# Internal Storage Bootloader (Multiple Images, 4 MB) — Series 3

Demonstrates how to configure the Gecko Bootloader to store firmware update images in flash, in a dual-slot setup with two 756 kB slots starting at 0x011FA000 and 0x12B7000.

This sample provides a standalone Gecko Bootloader for **Series 3** SoCs with **4 MB main flash**, configured to hold **two** firmware update images side by side in internal flash. The bootloader is application-triggered: an application running on the device receives a `.gbl` upgrade image over whatever transport it natively uses (Bluetooth, Wi-Fi, Connect, custom, etc.), writes it into one of the two storage slots using the Gecko Bootloader interface, sets the install flag, and reboots. On the next reset the bootloader inspects the slot, validates the GBL, applies it to the application region, and jumps into the new application. Maintaining two slots makes A/B-style updates and rollbacks possible: the application can keep the previous image staged in the second slot while the new image runs out of the first slot, and switch back if the new image misbehaves.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This is the multi-image internal-storage variant for Series 3 SoCs with 4 MB main flash. It targets users who want to deliver firmware updates without an external SPI flash and without sacrificing the ability to keep more than one image at a time on the device — typical for OTA / DFU schemes that need to roll back to a known-good image, or that want to download a new image while the application is still running on the previous one.

The configured layout is:

- **Storage**: internal main flash, **dual-slot** (two storage slots).
- **Slot 0**: enabled, **756 kB (0xBD000 / 774144 bytes)**, starting at **`0x011FA000`**.
- **Slot 1**: enabled, **756 kB (0xBD000 / 774144 bytes)**, starting at **`0x012B7000`** (immediately after Slot 0).
- Total storage region: **1512 kB** (`Slot 0 + Slot 1`), placed in the upper portion of the 4 MB flash.

The application image runs from the lower portion of the same flash, leaving room for the application proper, manufacturing tokens, and any NVM3 region. Use the project configurator's *Storage* tab to verify the slot start / size values match your application's linker layout — if your application linker file places code above `0x011FA000`, the slots will collide with the application image.

The bootloader does **not** include any UART, SPI, or Bluetooth communication components — application-triggered updates via the Bootloader Application Interface (`btl_storage` / `btl_application_interface` APIs) are the only update path. Whatever protocol your application uses to download the GBL is up to you.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs **Series 3** SoC development kit with **4 MB main flash** (radio board + mainboard, or a pro kit) supported by the Gecko Platform SDK.
- USB cable to the kit's mainboard for debug access; UART debug output (if enabled by the application) is routed through VCOM.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- The application sample / firmware that will trigger the update through the Bootloader Application Interface.
- Simplicity Commander (for command-line flashing and creating signed `.gbl` images of the application).

## Steps to Run Demo

1. In Simplicity Studio, create a new project from the **Bootloader - SoC Storage (Multiple OTA images of size 756kB for 4MB flash)** entry for your target Series 3 part.
2. Open the *Storage* tab in the project configurator and verify the slot configuration:
   - Slot 0 → `0x011FA000`, size `0xBD000` (756 kB).
   - Slot 1 → `0x012B7000`, size `0xBD000` (756 kB).
   Adjust if your application's linker layout requires it; the application region must end below `0x011FA000`.
3. Build the project and flash the generated bootloader image to the SoC.
4. Build your application, ensuring its linker script reserves the application region below `0x011FA000` and that it includes the Bootloader Application Interface so it can call `bootloader_eraseStorageSlot()` / `bootloader_writeStorage()` / `bootloader_setImageToBootload()` / `bootloader_rebootAndInstall()`.
5. Flash the application on top of the bootloader.
6. Run the application. When it has a new `.gbl` image to apply, it writes the image into one of the two slots, marks that slot as the install target, and reboots.
7. On the next reset, the Gecko Bootloader validates the GBL in the chosen slot, copies it into the application region, and jumps into the new application.
8. To exercise rollback / A-B style updates, leave the previous `.gbl` in the second slot — the application can switch back to it via the same `bootloader_setImageToBootload()` API.

To validate the storage layout independently from the application, you can also generate a `.gbl` from a known-good application binary with Simplicity Commander, write it into Slot 0 with `commander flash --address 0x011FA000`, and reboot.

## Troubleshooting

- **Build errors / target rejected:** Verify the part has 4 MB main flash. Smaller-flash variants in the same family will not have a valid memory range at `0x012B7000` for Slot 1.
- **Application linker errors / overlapping regions:** The application region must end below `0x011FA000`. If the linker reports overlap with the storage region, either shrink the application or move the slots — but keep `Slot 0 + Slot 0_size = Slot 1_start` to keep the slots contiguous.
- **Application does not start after upgrade:** Confirm the application image was built against the same bootloader interface (matching SDK version) and, if secure boot is enabled, that the GBL is signed with the key provisioned on the device.
- **Bootloader rejects the GBL:** Verify the GBL was generated by Simplicity Commander from the matching application image. If anti-rollback / image-version metadata is enforced, ensure the new image's version is greater than (or equal to) the running version where required.
- **Wrong slot installed on reboot:** Make sure the application calls `bootloader_setImageToBootload(slot_id)` with the correct `slot_id` (0 or 1) before `bootloader_rebootAndInstall()`. Calling `rebootAndInstall()` without setting the slot leaves the bootloader looking at the previously-marked slot.
- **Tokens / NVM3 erased after re-flashing:** Use Simplicity Commander's options to preserve manufacturing tokens / NVM3 regions, or reconfigure the storage layout in the project configurator to leave room for them.
- **`btl_storage_*` API calls return error from the application:** Ensure the application's bootloader interface library matches this bootloader's SDK version. A mismatch between application-side `btl_application_interface` and the running bootloader is the most common cause.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)            
