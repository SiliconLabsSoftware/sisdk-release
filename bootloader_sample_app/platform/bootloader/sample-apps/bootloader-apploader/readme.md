# Bluetooth AppLoader OTA DFU Bootloader

Demonstrates how to perform in-place application updates using Bluetooth AppLoader OTA DFU, in a standalone bootloader configuration over a Bluetooth connection.

This folder provides a standalone Gecko Bootloader for Silicon Labs SoCs that performs over-the-air (OTA) firmware updates over a Bluetooth LE connection using the AppLoader mechanism. In-place updates are used, so the incoming image overwrites the application region directly in flash without requiring a separate download slot. The folder ships three build variants that share this same readme:

- **`bootloader-apploader`** – the standard single-image AppLoader bootloader.
- **`bootloader-apploader-secure`** – the **Secure** part of a TrustZone-split bootloader; contains the core bootloader functionality.
- **`bootloader-apploader-nonsecure`** – the **Non-Secure** part of a TrustZone-split bootloader; contains the Bluetooth communication interfaces.

The `-secure` and `-nonsecure` projects are **companions** (linked via `companion:` tags in their `.slcp` files) and must be built and flashed together on a TrustZone-capable device.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

The AppLoader is a compact bootloader image that embeds just enough of the Bluetooth LE stack to receive a GBL upgrade image over an OTA connection. When no DFU is in progress it hands execution to the full application; when an upgrade is initiated it performs the transfer and, using the **in-place update** scheme, rewrites the application region directly with the incoming image. This keeps the bootloader footprint small and avoids reserving a separate upgrade slot in flash.

Three variants are provided in this folder:

- **Standard (`bootloader-apploader`)** – Targets any Bluetooth LE SoC supported by the Silicon Labs Bluetooth SDK. Built as a single image and flashed alongside the application.
- **TrustZone Secure (`bootloader-apploader-secure`)** – Runs in the TrustZone secure state, provides the core bootloader services, and exposes them to the non-secure side through non-secure callable (NSC) interfaces. Defines `BOOTLOADER_SUPPORT_COMMUNICATION=1` and enables VCOM for debug output (`SL_VCOM_ENABLE=1`).
- **TrustZone Non-Secure (`bootloader-apploader-nonsecure`)** – Runs in the TrustZone non-secure state and provides the Bluetooth communication interfaces used to receive the OTA image. Must be paired with the Secure variant on the same device.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs Bluetooth LE SoC development kit (for example an EFR32BG22, EFR32xG24, or EFR32xG27 radio board on a Wireless Starter Kit mainboard or Pro Kit).
- For the `-secure` / `-nonsecure` variants: a TrustZone-capable part (for example EFR32xG21B or EFR32xG24 Secure Vault devices).
- USB cable to the mainboard's board controller, which provides debug access and the VCOM UART bridge for bootloader debug output.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK and the **Silicon Labs Bluetooth SDK** installed.
- Simplicity Commander (for command-line flashing).
- A BLE-capable phone running the **Simplicity Connect** mobile app (formerly EFR Connect) to drive the OTA DFU from a smartphone.

## Steps to Run Demo

### Standard `bootloader-apploader`

1. In Simplicity Studio, create a new project from **Bootloader - SoC Bluetooth AppLoader OTA DFU** for your target part.
2. Build the project and flash the generated bootloader image to the kit.
3. Create a Bluetooth application project (for example *Bluetooth - SoC Empty*) that includes the **Application OTA DFU** component, build it, and flash it on top of the bootloader.
4. Create a GBL upgrade image of a new version of the same application using `commander gbl create`.
5. Open the Simplicity Connect app on your phone, connect to the advertising device, open the **OTA** tab, and upload the `.gbl` file.
6. When the transfer completes, the device resets into the new application.

### TrustZone variants (`-secure` + `-nonsecure`)

The Secure and Non-Secure parts are **two independent projects** that must both be created, built, and flashed together on the same TrustZone-capable device. Neither half is usable on its own.

1. In Simplicity Studio, create a project from **Bootloader - SoC Bluetooth AppLoader OTA DFU Secure part of Bootloader using TrustZone** (`bootloader-apploader-secure`) for your target part.
2. Create a second project from **Bootloader - SoC Bluetooth AppLoader OTA DFU Non-Secure part of Bootloader using TrustZone** (`bootloader-apploader-nonsecure`) for the same target. The `companion:` tag in each `.slcp` links the two in the Studio wizard, so creating one may prompt you to create its pair.
3. Build the Secure project.
4. Build the Non-Secure project.
5. Flash both images to the same device. Program them individually (Secure first, then Non-Secure), or combine them into a single image with Simplicity Commander and flash in one step.
6. Create a Bluetooth application project (for example *Bluetooth - SoC Empty*) that includes the **Application OTA DFU** component, build it, and flash it on top of the bootloader pair.
7. Perform the OTA DFU from the Simplicity Connect app exactly as in the standard flow above.

## Troubleshooting

- **No OTA service advertised / phone cannot find the device:** Confirm the Bluetooth application is built with the **Application OTA DFU** component and was flashed after the bootloader; flashing the bootloader alone will not advertise a usable device.
- **OTA transfer aborts partway and the device no longer boots an application:** AppLoader performs an **in-place** update, so an interrupted transfer can leave the device without a valid application. Recover by reconnecting over BLE — the AppLoader itself stays resident and will still advertise so a new image can be uploaded.
- **`-secure` / `-nonsecure` variant hangs at boot:** Both companion images must be flashed on the same device and must come from the same SDK version. Verify that the non-secure project was generated from the companion tag of the secure project (not hand-paired) so their NSC interfaces match.
- **No bootloader debug output on VCOM:** For the TrustZone secure variant, confirm `SL_VCOM_ENABLE` is `1` and the mainboard AEM/VCOM switch is set to AEM so the board controller forwards UART. The standard `bootloader-apploader` variant does not enable VCOM by default — add the `iostream_usart_vcom` / `bootloader_debug` plumbing if you need prints.
- **GBL rejected by the bootloader:** If secure boot is enabled, make sure the GBL is signed with the key provisioned on the device; otherwise ensure the GBL was generated by Simplicity Commander from the matching application image.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)

