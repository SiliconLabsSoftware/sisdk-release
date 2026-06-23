# TrustZone OpenThread BLE DMP (Workspace and Non-Secure Application)

The Simplicity IDE uses the `mp-ot-ble-soc-tz` workspace to create the secure and
non-secure applications for the TrustZone OpenThread BLE DMP example solutions.
Additionally, the workspace includes the `bootloader-storage-internal-single`
bootloader application, which will allow the following post-build actions to
process:

- Combine the secure and non-secure binaries into an `app-only` image.
- Combine the bootloader binary with the previous artifacts into a `full` image.
- Generate a GBL file of the `app-only` image to be used for firmware upgrades.

## Prerequisites

The workspace file **`mp-ot-ble-soc-tz.slcw`** references the **secure** and **bootloader**
projects under **`multiprotocol_app/ot-ble/tz/`** (vendored copies aligned with the Thread
**`openthread_app`** tree). Those directories are **checked in**; a normal multiprotocol clone
is enough to open this workspace.

If **`ot-tz-secure-app/`** or **`workspace-bootloaders/`** are missing, restore them from
upstream **`openthread_app`** as described in **`../../tz/README.md`**.

## Getting Started

Generating and building the entire workspace will build the constituent projects and produce
the post-build artifacts mentioned above. From the `artifacts/` directory, flash either the
`full` image, or the `app-only` image and a separate bootloader binary, and the OpenThread CLI
should be present when interacting with the application terminal.

See the application README file for details on how to use the OpenThread CLI.

## Keeping in sync with `openthread_app` (Thread repo)

The non-secure **`mp-ot-ble-soc-tz.slcp`** follows **`openthread_app/ot-ble-dmp/trustzone/ot-ble-dmp-tz-ns.slcp`**, with intentional multiprotocol differences: **`project_name`**, **`package`**, **`label`**, and **`include` / `source` / `readme` paths** under **`../mp-ot-ble-soc/`** (shared SoC sources). The workspace **`mp-ot-ble-soc-tz.slcw`** mirrors **`ot-ble-dmp-tz.slcw`**, with **`path:`** entries pointing at **`../../tz/...`** (vendored secure + bootloader trees under **`multiprotocol_app/ot-ble/tz/`**). Refresh those copies when bumping OpenThread — see **`../../tz/README.md`**.

## Troubleshooting

The bootloader, secure app, and non-secure app need to have coordinated flash and ram memory
segments defined which don't overlap and aren't too small for the firmware. If running into issues,
particularly when installing additional components, it is recommended to use the
Simplicity Memory Editor tool to ensure that appropriate regions are defined.

## Additional Resources

[AN1374: Series 2 TrustZone](https://www.silabs.com/documents/public/application-notes/an1374-trustzone.pdf)
