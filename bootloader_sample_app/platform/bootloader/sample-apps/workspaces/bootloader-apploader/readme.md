# Bluetooth AppLoader OTA DFU Bootloader — TrustZone Workspace

Demonstrates how to build a TrustZone-split bootloader as a unified workspace, combining the Secure and Non-Secure parts into a single dual-image build.

This folder is a **Silicon Labs Component Workspace (`.slcw`)** that ties the **Secure** and **Non-Secure** halves of the Bluetooth AppLoader OTA DFU bootloader into one buildable, flashable deliverable for TrustZone-capable Series 2 SoCs. Instead of creating, building, and flashing the two halves as independent Studio projects, the workspace lets a single create / build / flash action produce both images — with the Secure side exporting its non-secure callable (NSC) interface as a static library that the Non-Secure side links against. The packaged result is a TrustZone-aware Gecko Bootloader that performs in-place application updates over a Bluetooth LE link, suitable for Bluetooth SoC applications that require Secure Vault / TrustZone separation.

The workspace contains:

- **`bootloader-apploader.slcw`** – the workspace descriptor, listing both projects and selecting the `bootloader_tz_workspace` post-build profile that combines the Secure and Non-Secure outputs into a single deliverable.
- **`bootloader-apploader-secure.slcp`** – the **Secure** part: core bootloader services (image parsing, AppLoader secure runtime, TrustZone secure config, debug). Exports `artifact/trustzone_secure_library.o`. Built with the `bootloader_trustzone_secure` post-build profile. Defines `BOOTLOADER_SUPPORT_COMMUNICATION=1` and enables VCOM (`SL_VCOM_ENABLE=1`).
- **`bootloader-apploader-nonsecure.slcp`** – the **Non-Secure** part: AppLoader non-secure runtime, Non-Secure image / include parser, core non-secure runtime. Built with the `bootloader_trustzone_nonsecure` post-build profile.

The two `.slcp`s carry mutual `import:` directives, so the workspace is the only supported way to build them — they are not standalone projects.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This workspace targets users who need a **production**-quality TrustZone-split bootloader for a Bluetooth SoC application and want to deliver / build it as a single artifact rather than maintaining two coupled Studio projects. It is the workspace equivalent of the standalone `sample-apps/bootloader-apploader/` projects, with three differences:

1. **One create, one build, one flashable artifact.** The `.slcw` lists both `.slcp` projects and selects the `bootloader_tz_workspace` post-build profile, which runs after both halves are built and produces a combined deliverable suitable for production programming.
2. **Real build-time linking between Secure and Non-Secure.** The Secure project exports `artifact/trustzone_secure_library.o`, and both `.slcp`s declare `import:` against each other so Studio resolves the dependency graph and orders the builds correctly. The Non-Secure side links against the NSC veneers exported from Secure, instead of the `companion:`-tag-only pairing used in the standalone variant.
3. **Both halves are `quality: production`** in the workspace tree (the standalone variants are `quality: evaluation`).

At runtime the resulting bootloader behaves identically to the non-TrustZone AppLoader sample: it advertises and accepts a Bluetooth LE connection, receives a `.gbl` upgrade image, and re-flashes the application image in place. The TrustZone split keeps the cryptographic and image-validation logic in the Secure state while Bluetooth communication runs in the Non-Secure state.

## Prerequisites / Setup Requirements

**Hardware**
- A **TrustZone-capable** Silicon Labs Series 2 Bluetooth SoC kit (for example EFR32xG21B, EFR32xG24, or any Secure Vault part supported by the Gecko Platform SDK). Non-TrustZone parts will not generate the workspace.
- USB cable to the kit's mainboard for debug access; the same cable provides VCOM for the bootloader's debug log.
- A Bluetooth-capable host running the **Simplicity Connect** mobile app (or any equivalent OTA DFU client) for delivering the upgrade.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK and Bluetooth SDK installed.
- The **Simplicity Connect** mobile app (Android or iOS) for kicking off OTA DFU from a phone.
- Simplicity Commander (for command-line flashing and creating signed `.gbl` images).

## Steps to Run Demo

The Secure and Non-Secure halves are built **together as one workspace**. Do not create them as standalone projects.

1. In Simplicity Studio, create a new project from the **`bootloader-apploader-workspace`** entry (the `.slcw` shows up as a single workspace example for TrustZone-capable parts). Studio will instantiate both `bootloader-apploader-secure` and `bootloader-apploader-nonsecure` projects and link them according to the `.slcw`.
2. Confirm the target part / board is correct on both projects; UART (debug) is routed through VCOM by default (`SL_VCOM_ENABLE=1` on the Secure side).
3. Build the workspace. Studio runs the `bootloader_trustzone_secure` post-build for the Secure project, the `bootloader_trustzone_nonsecure` post-build for the Non-Secure project, and finally the `bootloader_tz_workspace` post-build to combine the two outputs into a single flashable artifact.
4. Flash the combined artifact to the device. (You can also flash the Secure and Non-Secure images individually if needed — Secure first, then Non-Secure — but the combined output is the recommended flow.)
5. Build and flash a Bluetooth SoC application that supports OTA DFU on top of the bootloader. Examples in the Bluetooth SDK that include the *In-Place OTA DFU* feature work directly with this bootloader.
6. From the **Simplicity Connect** app, scan, connect to the device, and start an OTA upload using a `.gbl` upgrade image generated by Simplicity Commander from the new application binary.
7. When the OTA transfer completes, the AppLoader bootloader installs the new application in place and reboots into it.

## Troubleshooting

- **Workspace fails to generate / target rejected:** Verify the part is TrustZone-capable. Non-TZ parts cannot consume the workspace because the Secure project depends on `bootloader_tz_secure_config`.
- **Linker error: missing `trustzone_secure_library.o`:** The Secure project must build first and export the library to its `artifact/` directory. If you opened the two `.slcp`s as standalone projects, the workspace dependency graph is bypassed — re-create the project from the **`.slcw`** workspace so Studio enforces the build order.
- **Device hangs at boot or fails secure transition:** Both halves must come from the same workspace generation and the same SDK version. A Secure built from one workspace and a Non-Secure built from another can have mismatched NSC veneers and will fail at the secure-to-non-secure handoff. Always rebuild the workspace as a whole.
- **OTA DFU never starts / device not advertising:** Confirm the application image was built against the matching Bluetooth SDK and includes the In-Place OTA DFU feature, and that `SL_VCOM_ENABLE`/debug output show the bootloader is reaching its main loop. If secure boot is enabled, ensure the `.gbl` is signed with the key provisioned on the device.
- **Device is bricked after a partial flash:** TrustZone bootloaders rely on both images being present and consistent. If only the Secure half was flashed (or vice-versa), reflash the combined workspace artifact with Simplicity Commander.
- **Tokens / NVM3 erased after re-flashing:** Use Simplicity Commander's options to preserve manufacturing tokens / NVM3 regions, or reconfigure the storage layout in the workspace's project configurator.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
