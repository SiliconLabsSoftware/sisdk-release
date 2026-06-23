# UART XMODEM Bootloader

Demonstrates how to perform firmware updates using XMODEM-CRC over UART, in a standalone bootloader with a menu where '1' starts an XMODEM transfer and '2' launches the app, for EmberZNet and Connect.

This folder provides a standalone Gecko Bootloader for Silicon Labs Series 2 NCP devices. The bootloader prints a menu over the serial port; sending ASCII `'1'` starts an XMODEM-CRC transfer of a GBL upgrade image, and sending ASCII `'2'` boots the application image stored in flash. Secure boot (AES/SHA/ECDSA), CRC integrity checking, and manufacturing-token preservation are included. UART output is routed through the kit's VCOM bridge by default (`SL_VCOM_ENABLE=1`), so a single USB cable provides both debug access and the XMODEM transport. GPIO activation (`bootloader_gpio_activation`) lets a host force the NCP into bootloader menu mode through a dedicated activation pin. The folder ships three build variants that share this same readme:

- **`bootloader-uart-xmodem`** – the standard single-image UART XMODEM bootloader.
- **`bootloader-uart-xmodem-secure`** – the **Secure** part of a TrustZone-split bootloader; contains the core bootloader functionality.
- **`bootloader-uart-xmodem-nonsecure`** – the **Non-Secure** part of a TrustZone-split bootloader; contains the UART / XMODEM communication interfaces.

The `-secure` and `-nonsecure` projects are **companions** (linked via `companion:` tags in their `.slcp` files) and must be built and flashed together on a TrustZone-capable device.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This sample is the recommended UART bootloader to pair with EmberZNet and Silicon Labs Connect NCP applications, and it can also be used as a generic standalone UART bootloader for any Series 2 application. On reset the bootloader presents a small menu on the configured UART; the user (or an automated host script) chooses to upload a new image or jump straight into the existing application:

1. Send `'1'` over the UART to start an **XMODEM-CRC** transfer; the bootloader receives a signed/unsigned `.gbl` upgrade image and installs it into the application region of flash.
2. Send `'2'` over the UART to skip the upload and boot whatever application is currently programmed.

GPIO activation extends this with a hardware path: holding the configured activation pin at the configured polarity at reset forces the bootloader to stay in menu mode even if a valid application is present.

Three variants are provided in this folder:

- **Standard (`bootloader-uart-xmodem`)** – Targets any Silicon Labs Series 2 NCP supported by the Gecko Platform SDK. Built as a single image and flashed alongside the NCP application.
- **TrustZone Secure (`bootloader-uart-xmodem-secure`)** – Runs in the TrustZone secure state, provides the core bootloader services (image parsing, crypto, token management, CRC, GPIO activation), and exposes them to the non-secure side through non-secure callable (NSC) interfaces. Defines `BOOTLOADER_SUPPORT_COMMUNICATION=1` and enables VCOM (`SL_VCOM_ENABLE=1`).
- **TrustZone Non-Secure (`bootloader-uart-xmodem-nonsecure`)** – Runs in the TrustZone non-secure state and provides the UART serial driver and XMODEM-CRC parser used to receive the firmware image. Must be paired with the Secure variant on the same device.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs Series 2 NCP development kit (for example an EFR32MG-series or EFR32xG-series radio board on a Wireless Starter Kit mainboard or Pro Kit) supported by the Gecko Platform SDK.
- USB cable to the mainboard's board controller for debug access. By default the bootloader UART is routed through the board controller's VCOM bridge, so the same USB cable also carries the XMODEM transport.
- For the `-secure` / `-nonsecure` variants: a TrustZone-capable NCP part (for example EFR32xG21B or EFR32xG24 Secure Vault devices).

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- A serial terminal that supports XMODEM-CRC transfers (for example Tera Term on Windows, or `sx` / `lrzsz` on Linux).
- For EmberZNet / Connect host workflows: the corresponding host-side bootloader utility from the Silicon Labs Zigbee or Connect SDK.
- Simplicity Commander (for command-line flashing and for creating signed GBL upgrade images).

## Steps to Run Demo

### Standard `bootloader-uart-xmodem`

1. In Simplicity Studio, create a new project from **Bootloader - NCP UART XMODEM** for your target Series 2 NCP part.
2. Open the project configurator and verify the USART peripheral, baud rate, and any GPIO activation pin match your board / host wiring; adjust if needed. By default UART is routed through VCOM at the kit's standard baud (typically 115200 8-N-1).
3. Build the project and flash the generated bootloader image to the NCP.
4. Build your target NCP application (for example an EmberZNet or Silicon Labs Connect NCP image) and flash it on top of the bootloader.
5. Open a serial terminal on the kit's VCOM port (or your external UART), then reset the board. The bootloader menu is printed on the terminal.
6. Press `1` to start the XMODEM-CRC transfer, then use the terminal to send the `.gbl` file.
7. When the transfer completes successfully, press `2` to boot into the newly uploaded application.

### TrustZone variants (`-secure` + `-nonsecure`)

The Secure and Non-Secure parts are **two independent projects** that must both be created, built, and flashed together on the same TrustZone-capable NCP device. Neither half is usable on its own.

1. In Simplicity Studio, create a project from **Bootloader - NCP UART XMODEM Secure part of Bootloader using TrustZone** (`bootloader-uart-xmodem-secure`) for your target part.
2. Create a second project from **Bootloader - NCP UART XMODEM Non-Secure part of Bootloader using TrustZone** (`bootloader-uart-xmodem-nonsecure`) for the same target. The `companion:` tag in each `.slcp` links the two in the Studio wizard, so creating one may prompt you to create its pair.
3. Build the Secure project.
4. Build the Non-Secure project.
5. Flash both images to the same device. Program them individually (Secure first, then Non-Secure), or combine them into a single image with Simplicity Commander and flash in one step.
6. Flash the NCP application built against the matching SDK on top.
7. Reset the board, open the serial terminal, and drive the menu and XMODEM transfer exactly as in the standard flow above.

## Troubleshooting

- **No menu printed on reset:** Verify the terminal is connected to the correct VCOM COM port and uses the matching baud, parity, stop bits, and flow control. Confirm `SL_VCOM_ENABLE` is `1` and the mainboard AEM/VCOM switch is set to AEM so the board controller forwards UART.
- **XMODEM transfer fails or times out:** Use XMODEM-**CRC** (not checksum) and disable flow control in the terminal; make sure the file being sent is a valid `.gbl` generated by Simplicity Commander. On long cables or noisy lines, lower the baud or shorten the wiring.
- **Device always stays in the bootloader:** Check the GPIO activation pin — if it is asserted at reset (for example pulled by a host or an external circuit) the bootloader stays in menu mode instead of jumping to the application. Confirm the activation pin / polarity in the `bootloader_gpio_activation` component matches your wiring.
- **Application does not start after upgrade:** Ensure the application is built with the matching bootloader interface and, if secure boot is enabled, that the GBL is signed with the correct key provisioned on the device. If token management is in use, check that tokens were not inadvertently erased when re-flashing.
- **`-secure` / `-nonsecure` variant hangs at boot:** Both companion images must be flashed on the same device and must come from the same SDK version. Verify the two projects were generated from each other's `companion:` tag so their NSC interfaces match, and that manufacturing tokens were preserved across flashing.
- **GBL rejected by the bootloader:** If secure boot is enabled, ensure the GBL is signed with the key provisioned on the device; otherwise confirm the GBL was generated by Simplicity Commander from the matching application image.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
