# EZSP SPI Bootloader

Demonstrates how to perform firmware updates using the EZSP protocol over SPI, in a standalone bootloader recommended for EmberZNet and Connect protocol stacks.

This folder provides a standalone Gecko Bootloader for Silicon Labs NCP devices running the EmberZNet or Silicon Labs Connect protocol stacks. The bootloader uses the same SPI interface that the host MCU uses for EZSP communication, and performs firmware transfers with XMODEM-CRC framed inside the EZSP bootloader protocol. GPIO activation (`bootloader_ezsp_gpio_activation`) allows the host to force the NCP into bootloader mode through a dedicated activation line. The folder ships three build variants that share this same readme:

- **`bootloader-spi-ezsp`** – the standard single-image EZSP SPI bootloader.
- **`bootloader-spi-ezsp-secure`** – the **Secure** part of a TrustZone-split bootloader; contains the core bootloader functionality.
- **`bootloader-spi-ezsp-nonsecure`** – the **Non-Secure** part of a TrustZone-split bootloader; contains the SPI / EZSP communication interfaces.

The `-secure` and `-nonsecure` projects are **companions** (linked via `companion:` tags in their `.slcp` files) and must be built and flashed together on a TrustZone-capable device.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

An EZSP NCP exchanges commands and packets with a host MCU over a SPI link (MOSI, MISO, SCLK, CS, plus `nHOST_INT` and `nWAKE` sideband lines). When the NCP needs a firmware update, the host asserts the activation line or sends an EZSP `launchStandaloneBootloader` command; the NCP resets into this standalone bootloader, which reuses the same SPI wiring to receive a GBL upgrade image using the XMODEM-CRC protocol framed in EZSP bootloader messages. On completion the NCP reboots back into the application image. Secure boot support (AES/SHA/ECDSA) and CRC-integrity checking are included, and token management is enabled so manufacturing tokens are preserved across upgrades.

Three variants are provided in this folder:

- **Standard (`bootloader-spi-ezsp`)** – Targets any Silicon Labs NCP supported by the Gecko Platform SDK. Built as a single image and flashed alongside the NCP application.
- **TrustZone Secure (`bootloader-spi-ezsp-secure`)** – Runs in the TrustZone secure state, provides the core bootloader services (image parsing, crypto, token management, CRC), and exposes them to the non-secure side through non-secure callable (NSC) interfaces. Defines `BOOTLOADER_SUPPORT_COMMUNICATION=1`.
- **TrustZone Non-Secure (`bootloader-spi-ezsp-nonsecure`)** – Runs in the TrustZone non-secure state and provides the SPI peripheral, EZSP protocol, and XMODEM parser used to receive the firmware image. Must be paired with the Secure variant on the same device.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs NCP development kit (for example an EFR32MG-series radio board on a Wireless Starter Kit mainboard or Pro Kit) supported by the Gecko Platform SDK.
- A host MCU or PC acting as the EZSP host, wired to the NCP over SPI: MOSI, MISO, SCLK, nSSEL (CS), plus `nHOST_INT` and `nWAKE`. The specific pins are configured in the SPI peripheral / EZSP components of the project.
- For the `-secure` / `-nonsecure` variants: a TrustZone-capable NCP part (for example EFR32xG21B or EFR32xG24 Secure Vault devices).
- USB cable to the NCP mainboard's board controller, providing debug access.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- The **EmberZNet** or **Silicon Labs Connect** stack / SDK on the host, including its EZSP host-side utilities used to launch the bootloader and drive the XMODEM transfer.
- Simplicity Commander (for command-line flashing).

## Steps to Run Demo

### Standard `bootloader-spi-ezsp`

1. In Simplicity Studio, create a new project from **Bootloader - NCP EZSP SPI** for your target NCP part.
2. Open the project configurator and verify the SPI peripheral, CS/INT/WAKE pin assignments, and GPIO activation pin match your board / host wiring; adjust if needed.
3. Build the project and flash the generated bootloader image to the NCP.
4. Build the NCP application (for example an EmberZNet or Connect NCP image with EZSP over SPI) and flash it on top of the bootloader.
5. Wire the host MCU to the NCP over SPI as described above and power both boards.
6. From the host, either assert the GPIO activation line at reset or send the EZSP `launchStandaloneBootloader` command to put the NCP into bootloader mode.
7. From the host, initiate an XMODEM-CRC transfer of the signed/unsigned `.gbl` upgrade image over the same SPI link using the EmberZNet/Connect host bootloader utility.
8. When the transfer completes the NCP reboots into the new application.

### TrustZone variants (`-secure` + `-nonsecure`)

The Secure and Non-Secure parts are **two independent projects** that must both be created, built, and flashed together on the same TrustZone-capable NCP device. Neither half is usable on its own.

1. In Simplicity Studio, create a project from **Bootloader - NCP EZSP SPI Secure part of Bootloader using TrustZone** (`bootloader-spi-ezsp-secure`) for your target part.
2. Create a second project from **Bootloader - NCP EZSP SPI Non-Secure part of Bootloader using TrustZone** (`bootloader-spi-ezsp-nonsecure`) for the same target. The `companion:` tag in each `.slcp` links the two in the Studio wizard, so creating one may prompt you to create its pair.
3. Build the Secure project.
4. Build the Non-Secure project.
5. Flash both images to the same device. Program them individually (Secure first, then Non-Secure), or combine them into a single image with Simplicity Commander and flash in one step.
6. Flash the NCP application built against the matching SDK on top.
7. Trigger and drive the EZSP SPI upgrade from the host exactly as in the standard flow above.

## Troubleshooting

- **Host cannot trigger the bootloader:** Confirm the NCP application was built with EZSP SPI support and the host is using the correct SPI mode, bit rate, and nSSEL/nHOST_INT/nWAKE wiring. If `launchStandaloneBootloader` is not recognized, verify the bootloader is actually installed (not just the application).
- **Device always stays in the bootloader:** Check the EZSP GPIO activation pin — if it is asserted at reset (for example pulled by the host or an external circuit) the bootloader will stay in menu mode instead of jumping to the application. Confirm the activation pin / polarity in the `bootloader_ezsp_gpio_activation` component matches your wiring.
- **XMODEM transfer fails or stalls over SPI:** Verify the host-side utility is using **XMODEM-CRC** (not checksum) framed in the EZSP bootloader protocol, and that the SPI timing and CS handling match the settings in `bootloader_spi_peripheral_driver`. Check for loose wiring on nHOST_INT — missed interrupts are a common cause of mid-transfer stalls.
- **GBL rejected:** If secure boot is enabled, ensure the GBL is signed with the key provisioned on the device; otherwise confirm the GBL was generated by Simplicity Commander from the matching application image.
- **`-secure` / `-nonsecure` variant hangs at boot:** Both companion images must be flashed on the same device and must come from the same SDK version. Verify the two projects were generated from each other's `companion:` tag so their NSC interfaces match, and that manufacturing tokens were preserved across flashing.
- **Application does not start after upgrade:** Confirm the application is built with the matching bootloader interface and, if token management is in use, that the tokens were not inadvertently erased when re-flashing.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
