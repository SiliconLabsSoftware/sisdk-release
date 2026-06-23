# BGAPI UART DFU Bootloader

Demonstrates how to perform firmware updates using the BGAPI protocol over UART DFU, in a standalone bootloader recommended for the Bluetooth LE protocol stack.

This folder provides a standalone Gecko Bootloader for Silicon Labs **Bluetooth LE NCP** devices. The host MCU drives the firmware update over UART using the BGAPI protocol's bootloader / DFU commands: the host issues `system_reset` with the DFU flag to push the NCP into bootloader mode, then streams the GBL upgrade image over the same UART connection. Secure boot (AES/SHA/ECDSA), CRC integrity checking, and manufacturing-token preservation are all included. GPIO activation (`bootloader_gpio_activation`) lets the host force the NCP into bootloader mode through a dedicated activation line in addition to the BGAPI command path. The folder ships three build variants that share this same readme:

- **`bootloader-uart-bgapi`** – the standard single-image BGAPI UART DFU bootloader.
- **`bootloader-uart-bgapi-secure`** – the **Secure** part of a TrustZone-split bootloader; contains the core bootloader functionality.
- **`bootloader-uart-bgapi-nonsecure`** – the **Non-Secure** part of a TrustZone-split bootloader; contains the UART / BGAPI communication interfaces.

The `-secure` and `-nonsecure` projects are **companions** (linked via `companion:` tags in their `.slcp` files) and must be built and flashed together on a TrustZone-capable device.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

A Bluetooth NCP exchanges BGAPI commands and events with a host MCU over a UART link (TX, RX, plus optional flow-control lines). When the NCP needs a firmware update, the host issues the BGAPI bootloader command (`system_reset` with the DFU flag) or asserts the GPIO activation line; the NCP resets into this standalone bootloader, which reuses the same UART wiring to receive a GBL upgrade image. On completion the NCP reboots back into the application image. The bootloader includes secure-boot support (AES/SHA/ECDSA), CRC-integrity checking, and token management so manufacturing tokens are preserved across upgrades. UART output is routed through the kit's VCOM (board-controller USB serial bridge) by default (`SL_VCOM_ENABLE=1`), so a single USB cable provides both debug access and the UART DFU transport.

Three variants are provided in this folder:

- **Standard (`bootloader-uart-bgapi`)** – Targets any Silicon Labs Bluetooth LE NCP supported by the Gecko Platform SDK and Bluetooth SDK. Built as a single image and flashed alongside the NCP application.
- **TrustZone Secure (`bootloader-uart-bgapi-secure`)** – Runs in the TrustZone secure state, provides the core bootloader services (image parsing, crypto, token management, CRC, GPIO activation), and exposes them to the non-secure side through non-secure callable (NSC) interfaces. Defines `BOOTLOADER_SUPPORT_COMMUNICATION=1` and enables VCOM (`SL_VCOM_ENABLE=1`).
- **TrustZone Non-Secure (`bootloader-uart-bgapi-nonsecure`)** – Runs in the TrustZone non-secure state and provides the UART serial driver and BGAPI UART DFU protocol used to receive the firmware image. Must be paired with the Secure variant on the same device.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs Bluetooth LE NCP development kit (for example an EFR32BG22, EFR32xG24, or EFR32xG27 radio board on a Wireless Starter Kit mainboard or Pro Kit).
- A host MCU or PC acting as the BGAPI host, wired to the NCP over UART (TX, RX, GND; optional CTS/RTS for flow control). The default project routes UART through the kit's VCOM, so a USB cable to the mainboard's board controller is sufficient when developing on a single PC host.
- For the `-secure` / `-nonsecure` variants: a TrustZone-capable NCP part (for example EFR32xG21B or EFR32xG24 Secure Vault devices).

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK and the **Silicon Labs Bluetooth SDK** installed.
- The Bluetooth NCP host application or library (provided by the Bluetooth SDK) that uses BGAPI's `system_reset` DFU flow to drive the upgrade.
- Simplicity Commander (for command-line flashing and for creating signed GBL upgrade images).

## Steps to Run Demo

### Standard `bootloader-uart-bgapi`

1. In Simplicity Studio, create a new project from **Bootloader - NCP BGAPI UART DFU** for your target NCP part.
2. Open the project configurator and verify the UART peripheral, baud rate, and any GPIO activation pin match your board / host wiring; adjust if needed. By default UART is routed through VCOM at the kit's standard baud (typically 115200 8-N-1).
3. Build the project and flash the generated bootloader image to the NCP.
4. Build the Bluetooth NCP application (for example `bt_ncp` from the Bluetooth SDK) and flash it on top of the bootloader.
5. Wire the host to the NCP over UART (or use the VCOM serial port if developing on a single PC host) and power the kit.
6. From the host, either assert the GPIO activation line at reset or send the BGAPI `system_reset` command with the DFU flag to put the NCP into bootloader mode.
7. From the host, drive the UART DFU transfer of the signed/unsigned `.gbl` upgrade image using the Bluetooth SDK's NCP host bootloader utility.
8. When the transfer completes the NCP reboots into the new application.

### TrustZone variants (`-secure` + `-nonsecure`)

The Secure and Non-Secure parts are **two independent projects** that must both be created, built, and flashed together on the same TrustZone-capable NCP device. Neither half is usable on its own.

1. In Simplicity Studio, create a project from **Bootloader - NCP BGAPI UART DFU Secure part of Bootloader using TrustZone** (`bootloader-uart-bgapi-secure`) for your target part.
2. Create a second project from **Bootloader - NCP BGAPI UART DFU Non-Secure part of Bootloader using TrustZone** (`bootloader-uart-bgapi-nonsecure`) for the same target. The `companion:` tag in each `.slcp` links the two in the Studio wizard, so creating one may prompt you to create its pair.
3. Build the Secure project.
4. Build the Non-Secure project.
5. Flash both images to the same device. Program them individually (Secure first, then Non-Secure), or combine them into a single image with Simplicity Commander and flash in one step.
6. Flash the Bluetooth NCP application built against the matching SDK on top.
7. Trigger and drive the BGAPI UART DFU upgrade from the host exactly as in the standard flow above.

## Troubleshooting

- **Host cannot trigger the bootloader:** Confirm the NCP application was built with BGAPI UART support and the host is using the matching baud rate, parity, stop bits, and flow-control configuration. If the BGAPI `system_reset` DFU command is not recognized, verify the bootloader is actually installed (not just the application).
- **No bootloader debug output on VCOM:** Confirm `SL_VCOM_ENABLE` is `1` and the mainboard AEM/VCOM switch is set to AEM so the board controller forwards UART. If the NCP and the host disagree on which serial port is used (kit VCOM vs. an external UART expansion), the bootloader will appear silent even though it is running.
- **Device always stays in the bootloader:** Check the GPIO activation pin — if it is asserted at reset (for example pulled by the host or an external circuit) the bootloader stays in DFU mode instead of jumping to the application. Confirm the activation pin / polarity in the `bootloader_gpio_activation` component matches your wiring.
- **UART DFU transfer fails or stalls:** Verify the host-side utility is using the Bluetooth SDK's BGAPI bootloader sequence and that the UART timing matches the settings in `bootloader_serial_driver`. Lower the baud rate or enable hardware flow control if there is data loss on long cables.
- **GBL rejected:** If secure boot is enabled, ensure the GBL is signed with the key provisioned on the device; otherwise confirm the GBL was generated by Simplicity Commander from the matching application image.
- **`-secure` / `-nonsecure` variant hangs at boot:** Both companion images must be flashed on the same device and must come from the same SDK version. Verify the two projects were generated from each other's `companion:` tag so their NSC interfaces match, and that manufacturing tokens were preserved across flashing.
- **Application does not start after upgrade:** Confirm the application is built with the matching bootloader interface and, if token management is in use, that tokens were not inadvertently erased when re-flashing.

## Resources

- [Gecko Bootloader User's Guide](://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
