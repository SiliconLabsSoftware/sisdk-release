# Platform Security - SoC mbedTLS ECDH

Demonstrates how to perform ECDH key agreement between two peers with mbedTLS on SECP256R1 or SECP192R1, reporting hardware-accelerated key generation and shared-secret timing over UART.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example simulates a **client** and **server** performing Elliptic-Curve Diffie-Hellman (ECDH) key agreement on a single device, using the mbedTLS ECDH API. Output is printed on the kit virtual COM port, including **timing measurements** for each major step.
After reset, you choose one of two hardware-accelerated curves:
- **SECP256R1** (`MBEDTLS_ECP_DP_SECP256R1`) — press **`1`**
- **SECP192R1** (`MBEDTLS_ECP_DP_SECP192R1`) — press **`2`**
The application then:
1. Seeds **CTR-DRBG** from the mbedTLS entropy module (TRNG when available, otherwise RAIL, otherwise dummy entropy on devices without TRNG).
2. Generates a **client key pair** and a **server key pair** (`mbedtls_ecdh_gen_public`).
3. Exchanges public keys between client and server contexts.
4. Computes the **shared secret** on both sides (`mbedtls_ecdh_compute_shared`).
5. Verifies both secrets match and prints the shared secret in hex.
**Hardware acceleration:** ECC, AES (CTR-DRBG), and SHA-256 (entropy accumulator) are accelerated by the device crypto hardware (Secure Engine on HSE devices, CRYPTOACC on VSE devices). You can disable acceleration in **Mbed TLS common functionality** to compare performance.
**Components used:** `mbedtls_ecdh`, `mbedtls_random`, `mbedtls_slcrypto`, `mbedtls_ecc_secp256r1`, `mbedtls_ecc_secp192r1`, plus `sl_system`, `sleeptimer`, `device_init`, and VCOM stdio retargeting.

## Prerequisites / Setup Requirements

### Hardware Requirements

- A supported Silicon Labs development kit (see board compatibility in Simplicity Studio for `mbedtls_ecdh` / `mbedtls_ecdh_s3`).
- **AEM** power selected on the radio/mainboard switch when programming (see image below).
- USB connection for programming and virtual COM (VCOM).

### Software Requirements

- **Simplicity Studio 5** (current SDK matching the example).
- A serial terminal (or **Device Console** in Studio) on the kit **VCOM** port:
  - **115200** baud, **8-N-1**
  - **Line terminator: None** (required for Device Console)
- Latest **adapter firmware** and **Secure Engine (SE) firmware** on the kit (see Simplicity Studio **General Device Information**).

## Steps to Run Demo

1. Update the kit **adapter firmware** and device **SE firmware** to the latest versions ([General Device Information](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-about-the-launcher/welcome-and-device-tabs#general-device-information)).
2. Open a serial terminal on the kit **VCOM** port (115200 8-N-1; line terminator **None** if using Device Console).
3. Create the **Platform Security - SoC mbedTLS ECDH** project in Simplicity Studio ([Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)).
4. Build and flash the project ([Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build), [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer)).
5. Reset the board. When prompted, type **`1`** for SECP256R1 or **`2`** for SECP192R1.
6. Watch the serial log for each step:
   - Random number generator seeding
   - Client and server key-pair generation (with key size, tick count, and milliseconds)
   - Server and client shared-secret computation (with timing)
   - Secret equality check and printed **Shared Secret** hex value

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM port, 115200 8-N-1, line terminator **None**; `SL_BOARD_ENABLE_VCOM` enabled |
| Invalid curve prompt repeats | Only **`1`** or **`2`** are accepted |
| `mbedtls_ctr_drbg_seed` failed | SE firmware up to date; on devices without TRNG, ensure RAIL entropy or `dummy_entropy.c` is included (Series 2 uses dummy entropy path when needed) |
| ECDH compute_shared failed | Board/part supports selected curve; try the other curve option |
| Timings much slower than expected | Confirm hardware acceleration is enabled in Mbed TLS common functionality |
| Programming fails | AEM switch position (see Prerequisites image) |

## Resources

- [Simplicity Studio 5 User's Guide — Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)
- [UG103.5: mbed TLS Support in Silicon Labs SDK](https://www.silabs.com/documents/public/user-guides/ug103-05-fundamentals-mbedtls.pdf)
- [AN1311: Integrating Crypto Functionality into Applications](https://www.silabs.com/documents/public/application-notes/an1311-crypto-functionality-into-applications.pdf)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
