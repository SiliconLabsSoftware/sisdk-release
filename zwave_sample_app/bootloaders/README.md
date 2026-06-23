# Z-Wave Gecko Bootloaders

Production bootloader projects for Z-Wave sample applications and workspaces on Series 2 (EFR32ZG23 / EFR32ZG28).

| Project | Use case |
| --- | --- |
| `bootloader-storage-internal-single-zwave-ota` | SoC OTA: internal flash storage, single update slot |
| `bootloader-uart-xmodem-zwave-otw` | NCP OTW: UART XMODEM-CRC (menu: `1` = transfer, `2` = run app) |

Images are signed and may use LZMA compression. Sample signing and encryption keys ship with the Z-Wave sample app package; replace them for production products.

## Build

From the repository root:

```bash
python scripts/build_bootloader.py sample_apps/bootloaders --board <board>
```

## Flash and tokens

Flash the combined bootloader image, then flash application and Z-Wave token files (see sample app documentation). Example:

```bash
commander flash <bootloader>.s37 --device <part>
commander flash --tokengroup znet --tokenfile sample-keys/sample_encrypt.key --tokenfile sample-keys/sample_sign.key-tokens.txt --device <part>
```

## References

- [UG266: Gecko Bootloader User's Guide](https://www.silabs.com/documents/public/user-guides/ug266-gecko-bootloader-user-guide.pdf)
- Z-Wave sample application README files for OTA/OTW workspace usage
