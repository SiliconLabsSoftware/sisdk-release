# BGAPI UART DFU Bootloader — Series 3

Demonstrates how to perform firmware updates using the BGAPI protocol over UART DFU, in a standalone bootloader recommended for the Bluetooth LE protocol stack.

This sample provides a standalone Gecko Bootloader for **Series 3** Bluetooth LE NCP devices that receives `.gbl` upgrade images over UART using the **BGAPI** DFU protocol. A host running **BGLib** drives the DFU command set on the other side of the UART link (typically the kit's VCOM bridge), pushes the new application image, and the bootloader installs it into flash. Secure boot (AES/SHA/ECDSA), CRC integrity checking, and manufacturing-token preservation are included via the standard `btl_*` building blocks. UART output is routed through the kit's VCOM bridge by default, so a single USB cable provides both debug access and the BGAPI DFU transport. GPIO activation lets the host force the NCP into bootloader mode at reset through a dedicated activation pin, which complements the BGAPI command path for power-on / reset workflows.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This sample is the recommended UART bootloader to pair with a Bluetooth LE NCP application running on a Series 3 SoC. The host (PC, Linux SBC, or another MCU running BGLib) communicates with the NCP over UART using BGAPI. When a firmware update is needed, the host issues the BGAPI **DFU** commands to put the NCP into bootloader mode and stream the `.gbl` upgrade image; the bootloader writes the image into the application region of flash and reboots the NCP into the new firmware.

It is the Series 3 equivalent of the Series 2 `bootloader-uart-bgapi` sample. Compared to the Series 2 version, this Series 3 folder ships only the standalone bootloader — no TrustZone Secure / Non-Secure companion variants. If your application requires a TrustZone-split BGAPI UART DFU bootloader, use the Series 2 `sample-apps/bootloader-uart-bgapi/` set or the corresponding workspace under `sample-apps/workspaces/bootloader-uart-bgapi/`.

GPIO activation is included so the host can force the NCP into bootloader mode at reset, even before a Bluetooth connection has been established or in cases where the application image is corrupted and cannot service BGAPI commands. With the configured activation pin held at the configured polarity at reset, the bootloader stays in DFU mode regardless of the state of the application image in flash.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs **Series 3** Bluetooth LE NCP development kit (radio board + mainboard, or a pro kit) supported by the Gecko Platform SDK.
- USB cable to the kit's mainboard. By default the bootloader UART is routed through the board controller's VCOM bridge, so the same USB cable also carries the BGAPI DFU transport between the host PC and the NCP.
- Optional: a discrete pin between the host and the NCP wired to the configured **GPIO activation** pin to force the NCP into bootloader mode at reset.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK and Bluetooth SDK installed.
- The Bluetooth host SDK on the host side, providing **BGLib** and the `uart_dfu` host utility (or an equivalent BGAPI DFU client) for delivering the `.gbl` image.
- Simplicity Commander (for command-line flashing and creating signed `.gbl` images).

## Steps to Run Demo

1. In Simplicity Studio, create a new project from **Bootloader - NCP BGAPI UART DFU** for your target Series 3 NCP part.
2. Open the project configurator and verify the UART peripheral, baud rate, and any GPIO activation pin match your board / host wiring; adjust if needed. By default UART is routed through VCOM at the kit's standard baud (typically 115200 8-N-1).
3. Build the project and flash the generated bootloader image to the NCP.
4. Build a matching **Bluetooth NCP application** (any NCP target from the Bluetooth SDK that supports BGAPI UART DFU) and flash it on top of the bootloader.
5. Connect the NCP's UART to the host (open the kit's VCOM port, or wire to your host MCU's UART), and bring up the host-side Bluetooth stack with BGLib.
6. To trigger an upgrade, command the NCP into bootloader mode either over BGAPI or by holding the GPIO activation pin asserted at reset. Then drive the BGAPI DFU command set from the host to push the `.gbl` image.
7. When the transfer completes, the bootloader installs the new application and reboots into it; the host stack sees the NCP come back on the new firmware version.

## Troubleshooting

- **No DFU prompt / host cannot detect the NCP:** Verify the terminal or host utility is connected to the correct VCOM COM port and uses the matching baud, parity, stop bits, and flow control. Confirm the kit's mainboard AEM/VCOM switch is set to AEM so the board controller forwards UART. On long cables or noisy lines, lower the baud or shorten the wiring.
- **Device always stays in the bootloader:** Check the GPIO activation pin — if it is asserted at reset (for example pulled by the host or an external circuit) the bootloader stays in DFU mode instead of jumping to the application. Confirm the activation pin / polarity in the GPIO activation component matches your wiring.
- **Bootloader rejects the GBL:** If secure boot is enabled, ensure the `.gbl` is signed with the key provisioned on the NCP. Otherwise confirm the GBL was generated by Simplicity Commander from the matching application image.
- **Application does not start after upgrade:** Ensure the application is built with the matching bootloader interface and, if secure boot is enabled, that the GBL is signed with the correct key provisioned on the device. If token management is in use, check that tokens were not inadvertently erased when re-flashing.
- **BGAPI DFU command fails partway through:** Slow the upload (lower baud or insert flow control), and verify there are no buffer overruns on the host side. Make sure the NCP is genuinely in bootloader mode (it will not respond to regular BGAPI host commands once in DFU).
- **Tokens / NVM3 erased after re-flashing:** Use Simplicity Commander's options to preserve manufacturing tokens / NVM3 regions, or reconfigure the storage layout in the project configurator.
- **Need a TrustZone-split version:** Use the Series 2 `sample-apps/bootloader-uart-bgapi/` projects (Secure + Non-Secure halves) or the corresponding workspace under `sample-apps/workspaces/bootloader-uart-bgapi/`. The Series 3 folder does not currently ship a TrustZone-split companion.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
