# BGAPI UART DFU Bootloader — TrustZone Workspace

Demonstrates how to build a TrustZone-split bootloader as a unified workspace, combining the Secure and Non-Secure parts into a single dual-image build.

This folder is a **Silicon Labs Component Workspace (`.slcw`)** that ties the **Secure** and **Non-Secure** halves of the BGAPI UART DFU bootloader into one buildable, flashable deliverable for TrustZone-capable Series 2 NCPs. Instead of creating, building, and flashing the two halves as independent Studio projects, the workspace lets a single create / build / flash action produce both images — with the Secure side exporting its non-secure callable (NSC) interface as a static library that the Non-Secure side links against. The packaged result is a TrustZone-aware Gecko Bootloader for an NCP that receives `.gbl` upgrade images over **UART** using the **BGAPI** DFU protocol, intended for Bluetooth NCP host-driven systems where the host runs BGLib and drives the DFU sequence.

The workspace contains:

- **`bootloader-uart-bgapi.slcw`** – the workspace descriptor, listing both projects and selecting the `bootloader_tz_workspace` post-build profile that combines the Secure and Non-Secure outputs into a single deliverable.
- **`bootloader-uart-bgapi-secure.slcp`** – the **Secure** part: core bootloader services (image parsing, AES/SHA/ECDSA, CRC, token management, delay driver, debug) **plus** the UART transport (`bootloader_serial_driver`) and **GPIO activation** (`bootloader_gpio_activation`). Defines `BOOTLOADER_SUPPORT_COMMUNICATION=1`, enables VCOM (`SL_VCOM_ENABLE=1`). Exports `artifact/trustzone_secure_library.o`. Built with the `bootloader_trustzone_secure` post-build profile.
- **`bootloader-uart-bgapi-nonsecure.slcp`** – the **Non-Secure** part: core non-secure runtime, Non-Secure serial driver, Non-Secure image / include parsers, delay driver, debug, and the **BGAPI UART DFU** Non-Secure protocol stack (`bootloader_bgapi_uartdfu_nonsecure`). Built with the `bootloader_trustzone_nonsecure` post-build profile.

Only the Non-Secure project carries an `import:` against the Secure project; the Secure side is the producer of the NSC veneer object.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This workspace targets users who need a **production**-quality TrustZone-split BGAPI UART DFU bootloader for a Bluetooth NCP and want to deliver / build it as a single artifact rather than maintaining two coupled Studio projects. It is the workspace equivalent of the standalone `sample-apps/bootloader-uart-bgapi/` projects, with three differences:

1. **One create, one build, one flashable artifact.** The `.slcw` lists both `.slcp` projects and selects the `bootloader_tz_workspace` post-build profile, which runs after both halves are built and produces a combined deliverable suitable for production programming.
2. **Real build-time linking between Secure and Non-Secure.** The Secure project exports `artifact/trustzone_secure_library.o`, and the Non-Secure `.slcp` declares `import: bootloader-uart-bgapi-secure` so Studio resolves the dependency graph and orders the builds correctly. The Non-Secure side links against the NSC veneers exported from Secure, instead of the `companion:`-tag-only pairing used in the standalone variant.
3. **Both halves are `quality: production`** in the workspace tree (the standalone `-secure` / `-nonsecure` `.slcp`s are `quality: evaluation`).

At runtime the resulting bootloader behaves identically to the non-TrustZone BGAPI UART DFU sample: a host running **BGLib** drives the DFU command set over UART (typically the kit's VCOM bridge), pushes the `.gbl` upgrade image, and the bootloader installs the new application into flash. The TrustZone split keeps the cryptographic and image-validation logic running in the Secure state, while the BGAPI DFU protocol stack runs in Non-Secure context with help from the Secure-side serial driver and GPIO activation.

## Prerequisites / Setup Requirements

**Hardware**
- A **TrustZone-capable** Silicon Labs Series 2 Bluetooth NCP development kit (for example EFR32xG21B, EFR32xG24, or any Secure Vault part supported by the Gecko Platform SDK) running as the NCP target.
- A separate host (PC or host MCU) connected to the NCP over UART. By default UART is routed through VCOM at the kit's standard baud (typically 115200 8-N-1), so a single USB cable to the mainboard provides both debug access and the BGAPI DFU transport.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK and Bluetooth SDK installed.
- The Bluetooth host SDK on the host side, providing **BGLib** and the `uart_dfu` host utility (or an equivalent BGAPI DFU client) for delivering the `.gbl` image.
- Simplicity Commander (for command-line flashing and creating signed `.gbl` images).

## Steps to Run Demo

The Secure and Non-Secure halves are built **together as one workspace**. Do not create them as standalone projects.

1. In Simplicity Studio, create a new project from the **`bootloader-uart-bgapi-workspace`** entry (the `.slcw` shows up as a single workspace example for TrustZone-capable NCP parts). Studio will instantiate both `bootloader-uart-bgapi-secure` and `bootloader-uart-bgapi-nonsecure` and link them according to the `.slcw`.
2. Confirm the target part / board is correct on both projects, the USART peripheral and baud match your host wiring, and the GPIO activation pin (if used) matches your host's reset wiring. UART is routed through VCOM by default (`SL_VCOM_ENABLE=1` on the Secure side).
3. Build the workspace. Studio runs the `bootloader_trustzone_secure` post-build for the Secure project, the `bootloader_trustzone_nonsecure` post-build for the Non-Secure project, and finally the `bootloader_tz_workspace` post-build to combine the two outputs into a single flashable artifact.
4. Flash the combined artifact to the NCP. (You can also flash the Secure and Non-Secure images individually if needed — Secure first, then Non-Secure — but the combined output is the recommended flow.)
5. Build and flash a matching **Bluetooth NCP application** on top of the bootloader (any NCP target from the Bluetooth SDK that supports BGAPI UART DFU works).
6. Connect the NCP's UART to the host (open the kit's VCOM port, or wire to your host MCU's UART), and bring up the host-side Bluetooth stack. To trigger an upgrade, the host commands the NCP into bootloader mode (or holds the GPIO activation pin asserted at reset) and then drives the BGAPI DFU command set to push the `.gbl` image.
7. When the transfer completes, the bootloader installs the new application and reboots into it; the host stack sees the NCP come back on the new firmware version.

## Troubleshooting

- **Workspace fails to generate / target rejected:** Verify the part is TrustZone-capable. Non-TZ NCP parts cannot consume the workspace because the Secure project relies on the TZ-secure post-build profile.
- **Linker error: missing `trustzone_secure_library.o`:** The Secure project must build first and export the library to its `artifact/` directory. If you opened the two `.slcp`s as standalone projects, the workspace dependency graph is bypassed — re-create the project from the **`.slcw`** workspace so Studio enforces the build order.
- **Device hangs at boot or fails secure transition:** Both halves must come from the same workspace generation and the same SDK version. A Secure built from one workspace and a Non-Secure built from another can have mismatched NSC veneers and will fail at the secure-to-non-secure handoff. Always rebuild the workspace as a whole.
- **No menu / DFU prompt over UART:** Confirm the terminal or host utility uses the matching baud, parity, stop bits, and flow control, that the AEM/VCOM switch on the kit is set to AEM, and that `SL_VCOM_ENABLE=1` is preserved in the Secure project's configuration. On long cables or noisy lines, lower the baud or shorten the wiring.
- **Device always stays in the bootloader:** Check the GPIO activation pin — if it is asserted at reset (for example pulled by the host or an external circuit) the bootloader stays in DFU mode instead of booting the application. Confirm the activation pin / polarity in `bootloader_gpio_activation` matches your wiring.
- **DFU starts but image is rejected:** If secure boot is enabled, ensure the `.gbl` is signed with the key provisioned on the NCP. Otherwise confirm the GBL was generated by Simplicity Commander from the matching application image.
- **Tokens / NVM3 erased after re-flashing:** Use Simplicity Commander's options to preserve manufacturing tokens / NVM3 regions, or reconfigure the storage layout in the workspace's project configurator.
- **Device is bricked after a partial flash:** TrustZone bootloaders rely on both images being present and consistent. If only the Secure half was flashed (or vice-versa), reflash the combined workspace artifact with Simplicity Commander.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
