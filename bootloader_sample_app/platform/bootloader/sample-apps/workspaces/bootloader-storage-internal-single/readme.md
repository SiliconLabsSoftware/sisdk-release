# Internal Storage Bootloader (Single Image, 1 MB) — Workspace Bootloader Half

Demonstrates how to configure the Gecko Bootloader to store firmware update images using internal main flash, in a single-slot setup with a 448 kB slot starting at 0x84000.

This folder is the **bootloader half of a bootloader+application workspace** for Silicon Labs Series 2 SoCs with 1 MB main flash. Unlike the TrustZone workspaces in this `workspaces/` tree, there is **no `.slcw` here** — instead the `.slcp` declares `import: application` and tags itself `companion:workspace_application`, so an application sample's workspace can pull this bootloader in, generate both projects against the same flash layout, build them together, and produce a single combined deliverable.

The configured layout is identical to the standalone `sample-apps/bootloader-storage-internal-single/` variant: one storage slot (`SLOT0`) of **448 kB (0x70000 / 458752 bytes)** placed at `0x84000` on parts that use `SDID_200` / `SDID_205`, or at `0x8084000` on parts that use `SDID_210` / `_215` / `_220` / `_225` / `_235` (which have a `0x08000000` flash base). The application stored in main flash performs an in-place update by writing a downloaded `.gbl` into Slot 0 and rebooting; the Gecko Bootloader on next reset validates the GBL, applies it to the application region, and jumps back into the new application.

Differences vs. the standalone `sample-apps/bootloader-storage-internal-single/`:

- **Same project name (`bootloader-storage-internal-single`)** and **same description** — the workspace `.slcp` is a parallel "presentation" of the same bootloader, tuned for workspace consumption rather than standalone consumption.
- Adds `tag: companion:workspace_application` and `import: application`, so an application-side `.slcw` can resolve this bootloader as a peer project in the same workspace.
- Drops the `SDID_240` / `_250` / `_260` device conditions that the standalone variant carries. **Confirm with the bootloader team** whether that is intentional — if you target a `SDID_240`/`_250`/`_260` part, this workspace bootloader will not configure `BTL_STORAGE_BASE_ADDRESS` / `SLOT0_START` correctly without a manual override.
- Both variants are `quality: production` and use the `bootloader_series_2` post-build profile.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This sample exists for users who want to ship an SoC application together with its matching internal-storage Gecko Bootloader as **one workspace deliverable** instead of maintaining two unrelated Studio projects with manually-aligned slot configuration. The application's `.slcw` references this `.slcp` via the `application` import id, so the same workspace generation:

1. Picks the bootloader's `SLOT0_SIZE` / `SLOT0_START` / `BTL_STORAGE_BASE_ADDRESS` from this `.slcp`.
2. Builds the application against an application-region layout that does not collide with Slot 0.
3. Runs the `bootloader_series_2` post-build for the bootloader and the application's own post-build for the app, then bundles both outputs.

The bootloader configuration itself is identical to the standalone single-image / internal-storage variant:

- **Storage**: internal main flash, single slot.
- **Slot 0**: enabled, **`SLOT0_SIZE = 458752` (448 kB)**.
- **Slot 0 start / `BTL_STORAGE_BASE_ADDRESS`**:
  - `SDID_200`, `SDID_205` parts → **`0x84000`** (`540672` bytes).
  - `SDID_210`, `_215`, `_220`, `_225`, `_235` parts → **`0x8084000`** (`134758400` bytes; flash base `0x08000000`).
- **Components**: `bootloader_core`, `bootloader_crc`, `bootloader_aes_sha_ecdsa`, `bootloader_internal_storage`, `bootloader_storage_slots`, `bootloader_image_parser`, `bootloader_common_storage_single`, `bootloader_token_management`, `bootloader_debug`.
- **Tags**: `hardware:device:flash:1024` (filters this sample to 1 MB-flash parts), and `companion:workspace_application` (signals to Studio that this `.slcp` lives in a workspace whose other project supplies the `application` import id).

The bootloader does **not** include any UART, SPI, or Bluetooth communication components — application-triggered updates are the only update path. The application is expected to download the `.gbl` over whatever protocol it natively uses (Bluetooth, Zigbee, Wi-Fi, Connect, etc.), write it into Slot 0 using the bootloader interface (`btl_storage` API), set the install flag, and reboot.

## Prerequisites / Setup Requirements

**Hardware**
- A Silicon Labs Series 2 SoC development kit with **1 MB of internal main flash** (the `hardware:device:flash:1024` tag filters the sample to those parts in Studio). Examples include the EFR32xG21 (with a 1 MB flash variant), EFR32xG22, EFR32xG23, EFR32xG24, EFR32xG28, etc., as long as the SDID matches one of the supported `device_sdid_*` conditions in this `.slcp`.
- USB cable to the kit's mainboard for debug access; UART debug output (if enabled by the application) is routed through VCOM.

**Software**
- Simplicity Studio 5 (or later) with the Gecko Platform SDK installed.
- The application sample whose `.slcw` references this bootloader (the application provides the workspace; this folder only provides the bootloader half).
- Simplicity Commander (for command-line flashing and creating signed `.gbl` images of the application).

## Steps to Run Demo

This `.slcp` cannot be built standalone from this folder. The workspace flow lives in the **application** project; the steps below describe how to consume the bootloader half from there.

1. In Simplicity Studio, create a new project from the **application sample** whose `.slcw` references the `application` ↔ `bootloader-storage-internal-single` companion pair (the application sample is filtered to 1 MB-flash Series 2 SoC parts to match the bootloader's `hardware:device:flash:1024` tag).
2. Studio resolves the workspace, instantiates both the application project and **`bootloader-storage-internal-single`**, and ensures their flash layouts are consistent (the application linker file places the application image below Slot 0; Slot 0 sits at the configured `SLOT0_START`).
3. Build the workspace. Studio runs the application's post-build and the bootloader's `bootloader_series_2` post-build, then bundles the outputs.
4. Flash the combined output to the kit. Alternatively, flash the bootloader image first (with Simplicity Commander or the IDE's Flash Programmer), then flash the application on top.
5. Run the application. When the application receives a new `.gbl` (over whatever transport it implements), it writes the image into **Slot 0** at the configured address using the `btl_storage` / `btl_application_interface` APIs, calls `bootloader_rebootAndInstall()`, and resets.
6. On the next reset, the Gecko Bootloader inspects Slot 0, validates the GBL, copies it into the application region, and jumps into the new application.

To validate the storage layout independently from the application, you can also generate a `.gbl` from a known-good application binary with Simplicity Commander, write it into Slot 0 with `commander flash --address <SLOT0_START>`, set the install flag (`commander flash --address <metadata-address> ...` or via the application), and reboot.

## Troubleshooting

- **Workspace fails to generate / target rejected:** Verify the part has 1 MB main flash (matches the `hardware:device:flash:1024` tag) and that its SDID is one of `200`, `205`, `210`, `215`, `220`, `225`, or `235`. If it is `240` / `250` / `260`, override `BTL_STORAGE_BASE_ADDRESS` and `SLOT0_START` manually in the project configurator (these conditions are present in the standalone `.slcp` but not in the workspace variant).
- **Application does not start after upgrade:** Confirm the application image was built against the matching workspace generation (Slot 0 at the same address and size as the bootloader expects). If secure boot is enabled, ensure the `.gbl` is signed with the key provisioned on the device.
- **Bootloader rejects the GBL:** Verify the GBL was generated by Simplicity Commander from the matching application image, that the application's image-version metadata is greater than (or equal to) the running version where required, and that AES/SHA/ECDSA keys are provisioned consistently.
- **Slot 0 overlaps the application region:** This is a configuration mistake — re-check that `SLOT0_START + SLOT0_SIZE ≤ flash_end - manufacturing_token_region`, and that the application's linker file places the app below `SLOT0_START`. The workspace flow normally guarantees this; if you imported the bootloader into a custom `.slcw`, verify the imports match.
- **Tokens / NVM3 erased after re-flashing:** Use Simplicity Commander's options to preserve manufacturing tokens / NVM3 regions, or reconfigure the storage layout in the project configurator to leave room for them.
- **`btl_storage_*` API calls return error from the application:** Ensure the application's bootloader interface library matches this bootloader's SDK version. A mismatch between application-side `btl_application_interface` and the running bootloader is the most common cause.

## Resources

- [Gecko Bootloader User's Guide](https://docs.silabs.com/shared-content/latest/bootloader-user-guide-gsdk-4/)
- [Silicon Labs Community](https://www.silabs.com/community)

## Report Bugs & Get Support

You are encouraged to report issues and get help from the community:

- [Silicon Labs Community](https://www.silabs.com/community)
