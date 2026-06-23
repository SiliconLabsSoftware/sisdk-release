# SPI Flash Storage Bootloader (dual slot)

Demonstrates how to configure the Gecko Bootloader to store firmware update images using external SPI flash, in a dual-slot setup with two 252 kB slots starting at 0x2000 and 0x41000.

This project provides a **storage-based** Gecko Bootloader for Silicon Labs Series 2 SoCs that use **external SPI flash** to hold upgrade images. Unlike the internal-storage variants, the bootloader does not consume any of the MCU's internal flash for upgrade staging — the entire main flash region is available to the application. The bootloader does not itself receive the upgrade image over a communication link; the running application downloads the GBL upgrade image (over any transport — BLE, Wi-SUN, OpenThread, Zigbee, UART, etc.) and writes it into one of two **252 kB storage slots** in the external SPI flash. On the next reboot the bootloader verifies the image in the selected slot and installs it over the application. The two slots enable workflows such as A/B staging, dual-image fail-safe, or holding a primary image alongside a recovery image. Slot 0 starts at SPI-flash offset `0x2000` and slot 1 at `0x41000`; both are 252 kB (`0x3F000`). The slot layout can be adjusted on the **Storage** tab of the project configurator.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

A storage bootloader decouples the **transport** of the upgrade image from the **installation** of the upgrade image. The application is fully responsible for getting the GBL bytes from a remote source into a reserved region — in this case, a *storage slot* in an external SPI flash chip on the board. Once the slot contains a complete image, the application calls into the bootloader API to mark the image as "to be bootloaded" and reboots. The bootloader then:

1. Initializes the on-board SPI controller and SPI flash chip.
2. Reads the GBL header from the selected slot, verifies the GBL structure, CRC, and (if enabled) signature/decryption of the image.
3. Streams the contents out of the slot in SPI flash and into the application region of internal flash.
4. Updates any preserved manufacturing tokens.
5. Resets into the newly installed application.

This specific sample is configured for Silicon Labs Series 2 SoCs that have an **external SPI flash** present on the development kit (the `hardware:component:memory:spi` tag enforces this). Two storage slots are enabled (`SLOT0_ENABLE=1`, `SLOT1_ENABLE=1`), each `258048` bytes (`0x3F000`, 252 kB). Slot 0 starts at SPI-flash offset `0x2000` (= 8192) and slot 1 at `0x41000` (= 266240); together they occupy `0x2000`–`0x80000` (512 kB) of the external flash. `BTL_STORAGE_BASE_ADDRESS=0` indicates that the offsets are relative to the start of the SPI flash, not to MCU memory. The `bootloader_spiflash_storage` component implements the SPI-flash storage backend, `bootloader_spi_controller_driver` provides the SPI master, `bootloader_common_storage` handles the dual-slot bookkeeping, `bootloader_aes_sha_ecdsa` provides secure-boot and authenticated-upgrade support, and `bootloader_token_management` preserves manufacturing tokens across upgrades.

The dual-slot layout enables the application to stage a new image in one slot while a verified image remains in the other, supporting A/B fallback strategies. Which slot to install from is selected by the application via the bootloader API.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs Series 2 SoC development kit with an **on-board external SPI flash chip** (most Wireless Starter Kit and Wireless Pro Kit mainboards include a Macronix MX25R-series SPI flash; some Pro Kit boards do not — check the kit user guide). The `hardware:component:memory:spi` tag restricts this sample to those boards.
- USB cable to the mainboard's board controller for debug access.
- Power to the SPI flash. On Wireless Starter Kits the SPI flash is powered automatically when the mainboard is on; on some Pro Kit boards it is gated by a power-enable GPIO that must be asserted by the application or bootloader.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- A protocol SDK appropriate for your application-side DFU transport (for example the Bluetooth, Wi-SUN, OpenThread, EmberZNet, Z-Wave, or Amazon Sidewalk SDK; or just the Gecko Platform SDK if you use UART / USB).
- Simplicity Commander (for command-line flashing, for creating signed GBL upgrade images, and for direct SPI-flash inspection via `commander extflash`).

## Steps to Run Demo

1. In Simplicity Studio, create a new project from **Bootloader - SoC SPI Flash Storage (multiple images)** for your target Series 2 SoC kit with on-board SPI flash.
2. Open the project configurator and verify the SPI peripheral, MOSI/MISO/SCLK/CS pin assignments, and any SPI-flash power-enable pin match your board. 
3. Build the project and flash the generated bootloader image to the kit.
4. Create the target application project (for example a Bluetooth, Wi-SUN, OpenThread, or Zigbee example that includes the **Application Bootloader Upgrade Image** / OTA DFU components, or any other application with a custom downloader). Build and flash it on top of the bootloader.
5. Generate a GBL upgrade image of a new version of the application using Simplicity Commander (`commander gbl create ...`).
6. From the running application, transport the GBL over your chosen link and write it into a storage slot using the bootloader API, choosing the slot index (0 or 1) — typically `bootloader_eraseStorageSlot(slot)`, `bootloader_writeStorage(slot, …)`, `bootloader_verifyImage(slot)`.
7. Mark the chosen slot as bootable and reboot into the bootloader (`bootloader_setImageToBootload(slot)`, `bootloader_rebootAndInstall`).
8. The bootloader installs the new image and boots into it automatically. The other slot is left intact for fallback or future use.

## Troubleshooting

- **Bootloader fails to detect the SPI flash:** Confirm the kit actually has an on-board SPI flash and that the SPI peripheral / pin assignments / CS pin in the project configurator match the board schematic. On Pro Kit boards check that any SPI-flash power-enable GPIO is asserted before the bootloader tries to access the chip.
- **`bootloader_spiflash_storage` reports an unsupported chip ID:** The component supports a curated list of SPI-flash devices (typically Macronix MX25, Spansion / Cypress, Winbond, ISSI). If the on-board chip is not in that list it must be added manually to the SPI flash driver, or the chip swapped for a supported one.
- **Slot write succeeds but install fails with a CRC / parser error:** Make sure the GBL was generated by Simplicity Commander from the matching application version. If secure boot is enabled, the GBL must be signed with the key provisioned on the device; if encryption is enabled, it must also be encrypted with the correct key. Use `commander extflash dump` to read the slot back and compare with the locally generated GBL.
- **Upgrade never installs after reboot:** Confirm the application called `bootloader_setImageToBootload` for the correct slot followed by `bootloader_rebootAndInstall`, not just a bare reset. Without the "to be bootloaded" flag, the bootloader simply jumps back into the existing application.
- **Wrong slot installed:** The application must explicitly select which slot is staged for install. If both slots contain valid images and the wrong one is installed, double-check the slot index passed to `bootloader_setImageToBootload`.
- **Slot does not fit in SPI flash:** Verify the highest slot end address (default `0x80000`) is within the size of the SPI flash chip on the board. With the default 252 kB × 2 layout, the chip needs to be at least 512 kB.
- **SPI clock / wiring issues:** Storage corruption or intermittent install failures often trace back to SPI clock speed too high for the board layout, missing pull-ups on CS, or shared-bus contention. Lower the SPI baudrate in the project configurator and re-test.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
