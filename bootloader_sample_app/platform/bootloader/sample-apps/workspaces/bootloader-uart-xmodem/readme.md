# UART XMODEM Bootloader — TrustZone Workspace

Demonstrates how to build a TrustZone-split bootloader as a unified workspace, combining the Secure and Non-Secure parts into a single dual-image build.

This folder is a **Silicon Labs Component Workspace (`.slcw`)** that ties the **Secure** and **Non-Secure** halves of the UART XMODEM bootloader into one buildable, flashable deliverable for TrustZone-capable Series 2 NCPs. Instead of creating, building, and flashing the two halves as independent Studio projects, the workspace lets a single create / build / flash action produce both images — with the Secure side exporting its non-secure callable (NSC) interface as a static library that the Non-Secure side links against. The packaged result is a TrustZone-aware Gecko Bootloader for an NCP that receives `.gbl` upgrade images over **UART** using the **XMODEM-CRC** protocol, with a small interactive menu (`'1'` to start a transfer, `'2'` to boot the application). It is the recommended TrustZone UART bootloader for EmberZNet (Zigbee) and Silicon Labs Connect host-driven NCP systems.

The workspace contains:

- **`bootloader-uart-xmodem.slcw`** – the workspace descriptor, listing both projects and selecting the `bootloader_tz_workspace` post-build profile that combines the Secure and Non-Secure outputs into a single deliverable.
- **`bootloader-uart-xmodem-secure.slcp`** – the **Secure** part: core bootloader services (image parsing, AES/SHA/ECDSA, CRC, token management, delay driver, debug) **plus** the UART transport (`bootloader_serial_driver`) and **GPIO activation** (`bootloader_gpio_activation`). Defines `BOOTLOADER_SUPPORT_COMMUNICATION=1`, enables VCOM (`SL_VCOM_ENABLE=1`). Exports `artifact/trustzone_secure_library.o`. Built with the `bootloader_trustzone_secure` post-build profile.
- **`bootloader-uart-xmodem-nonsecure.slcp`** – the **Non-Secure** part: core non-secure runtime, Non-Secure serial driver, Non-Secure image / include parsers, delay driver, debug, and the **XMODEM-CRC** Non-Secure protocol stack (`bootloader_uart_xmodem_nonsecure`). Built with the `bootloader_trustzone_nonsecure` post-build profile.

Only the Non-Secure project carries an `import:` against the Secure project; the Secure side is the producer of the NSC veneer object.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This workspace targets users who need a **production**-quality TrustZone-split UART XMODEM bootloader for an NCP and want to deliver / build it as a single artifact rather than maintaining two coupled Studio projects. It is the workspace equivalent of the standalone `sample-apps/bootloader-uart-xmodem/` projects, with three differences:

1. **One create, one build, one flashable artifact.** The `.slcw` lists both `.slcp` projects and selects the `bootloader_tz_workspace` post-build profile, which runs after both halves are built and produces a combined deliverable suitable for production programming.
2. **Real build-time linking between Secure and Non-Secure.** The Secure project exports `artifact/trustzone_secure_library.o`, and the Non-Secure `.slcp` declares `import: bootloader-uart-xmodem-secure` so Studio resolves the dependency graph and orders the builds correctly. The Non-Secure side links against the NSC veneers exported from Secure, instead of the `companion:`-tag-only pairing used in the standalone variant.
3. **Both halves are `quality: production`** in the workspace tree (the standalone `-secure` / `-nonsecure` `.slcp`s are `quality: evaluation`).

At runtime the resulting bootloader behaves identically to the non-TrustZone UART XMODEM sample: on reset the bootloader prints a small menu over the configured UART (typically the kit's VCOM bridge); sending ASCII `'1'` starts an XMODEM-CRC transfer of a `.gbl` upgrade image, and sending ASCII `'2'` boots the application currently programmed in flash. The TrustZone split keeps the cryptographic and image-validation logic running in the Secure state, while the XMODEM-CRC parser runs in Non-Secure context with help from the Secure-side serial driver and GPIO activation.

## Prerequisites / Setup Requirements

**Hardware**
- A **TrustZone-capable** Silicon Labs Series 2 NCP development kit (for example EFR32xG21B, EFR32xG24, or any Secure Vault part supported by the Gecko Platform SDK) running as the NCP target.
- USB cable to the kit's mainboard for debug access. By default the bootloader UART is routed through the board controller's VCOM bridge, so the same USB cable also carries the XMODEM transport.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- A serial terminal that supports XMODEM-CRC transfers (for example Tera Term on Windows, or `sx` / `lrzsz` on Linux).
- For EmberZNet / Connect host workflows: the corresponding host-side bootloader utility from the Silicon Labs Zigbee or Connect SDK.
- Simplicity Commander (for command-line flashing and creating signed `.gbl` images).

## Steps to Run Demo

The Secure and Non-Secure halves are built **together as one workspace**. Do not create them as standalone projects.

1. In Simplicity Studio, create a new project from the **`bootloader-uart-xmodem-workspace`** entry (the `.slcw` shows up as a single workspace example for TrustZone-capable NCP parts). Studio will instantiate both `bootloader-uart-xmodem-secure` and `bootloader-uart-xmodem-nonsecure` and link them according to the `.slcw`.
2. Confirm the target part / board is correct on both projects, the USART peripheral and baud match your host wiring, and the GPIO activation pin (if used) matches your host's reset wiring. UART is routed through VCOM by default (`SL_VCOM_ENABLE=1` on the Secure side) at the kit's standard baud (typically 115200 8-N-1).
3. Build the workspace. Studio runs the `bootloader_trustzone_secure` post-build for the Secure project, the `bootloader_trustzone_nonsecure` post-build for the Non-Secure project, and finally the `bootloader_tz_workspace` post-build to combine the two outputs into a single flashable artifact.
4. Flash the combined artifact to the NCP. (You can also flash the Secure and Non-Secure images individually if needed — Secure first, then Non-Secure — but the combined output is the recommended flow.)
5. Build and flash a matching **NCP application** (EmberZNet NCP or Silicon Labs Connect NCP) on top of the bootloader.
6. Open a serial terminal on the kit's VCOM port (or your external UART), then reset the board. The bootloader menu is printed on the terminal.
7. Press `1` to start the XMODEM-CRC transfer, then use the terminal to send the `.gbl` file generated by Simplicity Commander.
8. When the transfer completes successfully, press `2` to boot into the newly uploaded application.

## Troubleshooting

- **Workspace fails to generate / target rejected:** Verify the part is TrustZone-capable. Non-TZ NCP parts cannot consume the workspace because the Secure project relies on the TZ-secure post-build profile.
- **Linker error: missing `trustzone_secure_library.o`:** The Secure project must build first and export the library to its `artifact/` directory. If you opened the two `.slcp`s as standalone projects, the workspace dependency graph is bypassed — re-create the project from the **`.slcw`** workspace so Studio enforces the build order.
- **Device hangs at boot or fails secure transition:** Both halves must come from the same workspace generation and the same SDK version. A Secure built from one workspace and a Non-Secure built from another can have mismatched NSC veneers and will fail at the secure-to-non-secure handoff. Always rebuild the workspace as a whole.
- **No menu printed on reset:** Verify the terminal is connected to the correct VCOM COM port and uses the matching baud, parity, stop bits, and flow control. Confirm `SL_VCOM_ENABLE=1` is preserved in the Secure project's configuration and the mainboard AEM/VCOM switch is set to AEM so the board controller forwards UART.
- **XMODEM transfer fails or times out:** Use XMODEM-**CRC** (not checksum) and disable flow control in the terminal; make sure the file being sent is a valid `.gbl` generated by Simplicity Commander. On long cables or noisy lines, lower the baud or shorten the wiring.
- **Device always stays in the bootloader:** Check the GPIO activation pin — if it is asserted at reset (for example pulled by a host or an external circuit) the bootloader stays in menu mode instead of jumping to the application. Confirm the activation pin / polarity in `bootloader_gpio_activation` matches your wiring.
- **Application does not start after upgrade:** Ensure the application is built with the matching bootloader interface and, if secure boot is enabled, that the `.gbl` is signed with the correct key provisioned on the device. If token management is in use, check that tokens were not inadvertently erased when re-flashing.
- **Tokens / NVM3 erased after re-flashing:** Use Simplicity Commander's options to preserve manufacturing tokens / NVM3 regions, or reconfigure the storage layout in the workspace's project configurator.
- **Device is bricked after a partial flash:** TrustZone bootloaders rely on both images being present and consistent. If only the Secure half was flashed (or vice-versa), reflash the combined workspace artifact with Simplicity Commander.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
