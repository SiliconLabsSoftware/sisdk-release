# EZSP SPI Bootloader — TrustZone Workspace

Demonstrates how to build a TrustZone-split bootloader as a unified workspace, combining the Secure and Non-Secure parts into a single dual-image build.

This folder is a **Silicon Labs Component Workspace (`.slcw`)** that ties the **Secure** and **Non-Secure** halves of the EZSP SPI bootloader into one buildable, flashable deliverable for TrustZone-capable Series 2 NCPs. Instead of creating, building, and flashing the two halves as independent Studio projects, the workspace lets a single create / build / flash action produce both images — with the Secure side exporting its non-secure callable (NSC) interface as a static library that the Non-Secure side links against. The packaged result is a TrustZone-aware Gecko Bootloader for an NCP that receives `.gbl` upgrade images over SPI using the **EZSP** protocol, intended for EmberZNet (Zigbee) and Silicon Labs Connect host-driven systems.

The workspace contains:

- **`bootloader-spi-ezsp.slcw`** – the workspace descriptor, listing both projects and selecting the `bootloader_tz_workspace` post-build profile that combines the Secure and Non-Secure outputs into a single deliverable.
- **`bootloader-spi-ezsp-secure.slcp`** – the **Secure** part: core bootloader services (image parsing, AES/SHA/ECDSA, CRC, token management, delay driver, debug) **plus** the SPI/EZSP transport components (`bootloader_spi_peripheral_driver`, `bootloader_ezsp_spi`, `bootloader_ezsp_gpio_activation`). Defines `BOOTLOADER_SUPPORT_COMMUNICATION=1`. Exports `artifact/trustzone_secure_library.o`. Built with the `bootloader_trustzone_secure` post-build profile.
- **`bootloader-spi-ezsp-nonsecure.slcp`** – the **Non-Secure** part: core non-secure runtime, Non-Secure SPI peripheral driver, Non-Secure EZSP SPI, Non-Secure image / xmodem / include parsers, delay driver, debug. Built with the `bootloader_trustzone_nonsecure` post-build profile.

Only the Non-Secure project carries an `import:` against the Secure project; the Secure side is the producer of the NSC veneer object.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This workspace targets users who need a **production**-quality TrustZone-split EZSP SPI bootloader for an NCP and want to deliver / build it as a single artifact rather than maintaining two coupled Studio projects. It is the workspace equivalent of the standalone `sample-apps/bootloader-spi-ezsp/` projects, with three differences:

1. **One create, one build, one flashable artifact.** The `.slcw` lists both `.slcp` projects and selects the `bootloader_tz_workspace` post-build profile, which runs after both halves are built and produces a combined deliverable suitable for production programming.
2. **Real build-time linking between Secure and Non-Secure.** The Secure project exports `artifact/trustzone_secure_library.o`, and the Non-Secure `.slcp` declares `import: bootloader-spi-ezsp-secure` so Studio resolves the dependency graph and orders the builds correctly. The Non-Secure side links against the NSC veneers exported from Secure, instead of the `companion:`-tag-only pairing used in the standalone variant.
3. **Both halves are `quality: production`** in the workspace tree (the standalone `-secure` / `-nonsecure` `.slcp`s are `quality: evaluation`).

At runtime the resulting bootloader behaves identically to the non-TrustZone EZSP SPI sample: a Bluetooth / Zigbee / Connect host on the other side of the SPI bus drives the EZSP frames that deliver the GBL upgrade image, and the bootloader installs the new application into flash. The TrustZone split keeps the cryptographic and image-validation logic (and, in this workspace, the SPI/EZSP transport itself) running in the Secure state, while a Non-Secure helper layer brokers SPI traffic from Non-Secure context.

## Prerequisites / Setup Requirements

**Hardware**
- A **TrustZone-capable** Silicon Labs Series 2 NCP development kit (for example EFR32xG21B, EFR32xG24, or any Secure Vault part supported by the Gecko Platform SDK) running as the NCP target.
- A separate host MCU (or a PC running the EmberZNet / Connect host CLI) connected to the NCP over SPI:
  - SPI MOSI / MISO / SCLK / `nSSEL`,
  - `nHOST_INT` (NCP → host) and `nWAKE` (host → NCP) for EZSP flow control.
- USB cable to the kit's mainboard for debug access; UART debug output (if enabled) goes through VCOM.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- The matching EmberZNet / Silicon Labs Connect SDK on the host side, plus the corresponding `bootload-*` host utility for delivering the GBL.
- Simplicity Commander (for command-line flashing and creating signed `.gbl` images).

## Steps to Run Demo

The Secure and Non-Secure halves are built **together as one workspace**. Do not create them as standalone projects.

1. In Simplicity Studio, create a new project from the **`bootloader-spi-ezsp-workspace`** entry (the `.slcw` shows up as a single workspace example for TrustZone-capable NCP parts). Studio will instantiate both `bootloader-spi-ezsp-secure` and `bootloader-spi-ezsp-nonsecure` and link them according to the `.slcw`.
2. Confirm the target part / board is correct on both projects, and that the SPI peripheral pinout (MOSI, MISO, SCLK, `nSSEL`, `nHOST_INT`, `nWAKE`) matches your host wiring. Adjust in the project configurator's pin / peripheral views if needed.
3. Build the workspace. Studio runs the `bootloader_trustzone_secure` post-build for the Secure project, the `bootloader_trustzone_nonsecure` post-build for the Non-Secure project, and finally the `bootloader_tz_workspace` post-build to combine the two outputs into a single flashable artifact.
4. Flash the combined artifact to the NCP. (You can also flash the Secure and Non-Secure images individually if needed — Secure first, then Non-Secure — but the combined output is the recommended flow.)
5. Build and flash a matching **NCP application** (EmberZNet NCP or Silicon Labs Connect NCP) on top of the bootloader.
6. Connect the NCP to the host over SPI and bring up the host-side stack as usual. To trigger an upgrade, the host commands the NCP into bootloader mode (or holds the EZSP GPIO activation pin asserted at reset) and then drives the EZSP-bootload protocol to push the `.gbl` image.
7. When the transfer completes, the bootloader installs the new application and reboots into it; the host stack sees the NCP come back on the new firmware version.

## Troubleshooting

- **Workspace fails to generate / target rejected:** Verify the part is TrustZone-capable. Non-TZ NCP parts cannot consume the workspace because the Secure project relies on the TZ-secure post-build profile.
- **Linker error: missing `trustzone_secure_library.o`:** The Secure project must build first and export the library to its `artifact/` directory. If you opened the two `.slcp`s as standalone projects, the workspace dependency graph is bypassed — re-create the project from the **`.slcw`** workspace so Studio enforces the build order.
- **Device hangs at boot or fails secure transition:** Both halves must come from the same workspace generation and the same SDK version. A Secure built from one workspace and a Non-Secure built from another can have mismatched NSC veneers and will fail at the secure-to-non-secure handoff. Always rebuild the workspace as a whole.
- **No EZSP frames seen by the host:** Check the SPI wiring (especially `nSSEL`, `nHOST_INT`, `nWAKE`), the SPI mode (CPOL/CPHA) and bit order, and the host's expected EZSP version. Confirm the GPIO activation pin in `bootloader_ezsp_gpio_activation` matches the host's reset / wake sequence; a polarity or pin-mux mismatch keeps the bootloader from entering bootload mode.
- **Bootload starts but image is rejected:** If secure boot is enabled, ensure the `.gbl` is signed with the key provisioned on the NCP. Otherwise confirm the GBL was generated by Simplicity Commander from the matching application image and is suitable for the bootloader's flash layout.
- **Tokens / NVM3 erased after re-flashing:** Use Simplicity Commander's options to preserve manufacturing tokens / NVM3 regions, or reconfigure the storage layout in the workspace's project configurator.
- **Device is bricked after a partial flash:** TrustZone bootloaders rely on both images being present and consistent. If only the Secure half was flashed (or vice-versa), reflash the combined workspace artifact with Simplicity Commander.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
