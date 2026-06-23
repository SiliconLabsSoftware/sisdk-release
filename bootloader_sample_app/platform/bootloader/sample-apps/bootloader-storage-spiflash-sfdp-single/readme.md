# External SPI Flash Storage Bootloader (SFDP, single slot)

Demonstrates how to configure the Gecko Bootloader to store firmware update images using external SPI flash auto-detected via SFDP, in a single-slot setup with a 512 kB slot at 0x0.

This project provides a **storage-based** Gecko Bootloader for Silicon Labs Series 2 SoCs that use **external SPI flash** to hold upgrade images, with the SPI flash chip identified at boot through its **SFDP** (Serial Flash Discoverable Parameters, JEDEC JESD216) parameter table rather than a hardcoded chip ID list. Unlike the internal-storage variants, the bootloader does not consume any of the MCU's internal flash for upgrade staging — the entire main flash region is available to the application. The bootloader does not itself receive the upgrade image over a communication link; the running application downloads the GBL upgrade image (over any transport — BLE, Wi-SUN, OpenThread, Zigbee, UART, etc.) and writes it into the **single 512 kB storage slot** at offset `0x0` of the external SPI flash. On the next reboot the bootloader auto-detects the SPI flash via SFDP, verifies the image in the slot, and installs it over the application. The slot layout can be adjusted on the **Storage** tab of the project configurator.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

A storage bootloader decouples the **transport** of the upgrade image from the **installation** of the upgrade image. The application is fully responsible for getting the GBL bytes from a remote source into a reserved region — in this case, a *storage slot* in an external SPI flash chip on the board. Once the slot contains a complete image, the application calls into the bootloader API to mark the image as "to be bootloaded" and reboots. The bootloader then:

1. Initializes the on-board SPI controller and reads the connected SPI flash's **SFDP** parameter table to derive its capacity, page size, sector/block sizes, and erase opcodes — so the build works with any SFDP-compliant chip without code changes.
2. Reads the GBL header from slot 0, verifies the GBL structure, CRC, and (if enabled) signature/decryption of the image.
3. Streams the contents out of the slot in SPI flash and into the application region of internal flash.
4. Updates any preserved manufacturing tokens.
5. Resets into the newly installed application.

This specific sample is configured for Silicon Labs Series 2 SoCs that have an **external SPI flash** present on the development kit (the `hardware:component:memory:spi` tag enforces this). Exactly one storage slot is enabled (`SLOT0_ENABLE=1`) sized `524288` bytes (`0x80000`, 512 kB), starting at SPI-flash offset `0x0`. `BTL_STORAGE_BASE_ADDRESS=0` indicates that the offset is relative to the start of the SPI flash, not to MCU memory. The `bootloader_spiflash_storage_sfdp` component implements the SFDP-driven SPI-flash storage backend, `bootloader_spi_controller_driver` provides the SPI master, `bootloader_common_storage_single` enforces the single-slot configuration, `bootloader_aes_sha_ecdsa` provides secure-boot and authenticated-upgrade support, and `bootloader_token_management` preserves manufacturing tokens across upgrades.

Use this sample (instead of the chip-list-based `bootloader-storage-spiflash`) when you want the same bootloader image to work across boards that have different SPI flash parts, or when the on-board SPI flash is not in the curated supported-chip list of the non-SFDP storage backend. Any JEDEC-compliant SPI flash that exposes a valid SFDP parameter table will be picked up automatically.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs Series 2 SoC development kit with an **on-board external SPI flash chip that supports SFDP** (JEDEC JESD216). Most modern parts from Macronix, Winbond, Micron, ISSI, and Cypress / Spansion comply. The `hardware:component:memory:spi` tag restricts this sample to boards with a SPI flash present.
- USB cable to the mainboard's board controller for debug access.
- Power to the SPI flash. On Wireless Starter Kits the SPI flash is powered automatically when the mainboard is on; on some Pro Kit boards it is gated by a power-enable GPIO that must be asserted by the application or bootloader.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- A protocol SDK appropriate for your application-side DFU transport (for example the Bluetooth, Wi-SUN, OpenThread, EmberZNet, Z-Wave, or Amazon Sidewalk SDK; or just the Gecko Platform SDK if you use UART / USB).
- Simplicity Commander (for command-line flashing, for creating signed GBL upgrade images, and for direct SPI-flash inspection via `commander extflash`).

## Steps to Run Demo

1. In Simplicity Studio, create a new project from **Bootloader - SoC SPI Flash Storage using SFDP (single image)** for your target Series 2 SoC kit with on-board SFDP-compliant SPI flash.
2. Open the project configurator and verify the SPI peripheral, MOSI/MISO/SCLK/CS pin assignments, and any SPI-flash power-enable pin match your board. 
3. Build the project and flash the generated bootloader image to the kit.
4. Create the target application project (for example a Bluetooth, Wi-SUN, OpenThread, or Zigbee example that includes the **Application Bootloader Upgrade Image** / OTA DFU components, or any other application with a custom downloader). Build and flash it on top of the bootloader.
5. Generate a GBL upgrade image of a new version of the application using Simplicity Commander (`commander gbl create ...`).
6. From the running application, transport the GBL over your chosen link and write it into the storage slot using the bootloader API (`bootloader_eraseStorageSlot`, `bootloader_writeStorage`, `bootloader_verifyImage`).
7. Mark the slot as bootable and reboot into the bootloader (`bootloader_setImageToBootload`, `bootloader_rebootAndInstall`).
8. The bootloader auto-detects the SPI flash, installs the new image, and boots into it automatically.

## Troubleshooting

- **Bootloader reports "no SPI flash detected" / SFDP read fails:** Confirm the kit actually has an on-board SPI flash and that the SPI peripheral / pin assignments / CS pin in the project configurator match the board schematic. On Pro Kit boards check that any SPI-flash power-enable GPIO is asserted before the bootloader tries to access the chip. Verify SPI clock polarity / phase (CPOL/CPHA) match the chip's expectations.
- **Chip does not expose SFDP:** Some older or low-cost SPI flash devices do not implement the SFDP table, or implement only an incomplete subset. If SFDP read returns invalid parameters, fall back to the chip-list-based variant (`bootloader-storage-spiflash` / `bootloader-storage-spiflash-single`).
- **Slot write succeeds but install fails with a CRC / parser error:** Make sure the GBL was generated by Simplicity Commander from the matching application version. If secure boot is enabled, the GBL must be signed with the key provisioned on the device; if encryption is enabled, it must also be encrypted with the correct key. Use `commander extflash dump` to read the slot back and compare with the locally generated GBL.
- **Upgrade never installs after reboot:** Confirm the application called `bootloader_setImageToBootload` followed by `bootloader_rebootAndInstall`, not just a bare reset. Without the "to be bootloaded" flag, the bootloader simply jumps back into the existing application.
- **Slot does not fit in SPI flash:** Verify the slot end (`SLOT0_START + SLOT0_SIZE`, default `0x80000`) is within the size reported by SFDP for the on-board SPI flash. With the default 512 kB layout, the chip needs to be at least 512 kB.
- **SPI clock / wiring issues:** Storage corruption or intermittent install failures often trace back to SPI clock speed too high for the board layout, missing pull-ups on CS, or shared-bus contention. Lower the SPI baudrate in the project configurator and re-test.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
