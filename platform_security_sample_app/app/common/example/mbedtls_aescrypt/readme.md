# Platform Security - SoC mbedTLS AES

Demonstrates how to perform interactive AES-256 encryption and decryption with mbedTLS, using SHA-256 for IV/key setup and HMAC for integrity, with hardware acceleration.

## Table of Contents

- [Purpose / Scope](#purpose--scope)
- [Prerequisites / Setup Requirements](#prerequisites--setup-requirements)
- [Steps to Run Demo](#steps-to-run-demo)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Report Bugs & Get Support](#report-bugs--get-support)

## Purpose / Scope

This example runs on the device as an interactive **AESCRYPT** demo over the kit virtual COM port. After reset, you choose **encryption** or **decryption** mode from the serial terminal.
In **encryption** mode, the application:
- Prompts for a short phrase (up to 16 bytes) used with the message length to derive a 16-byte **initialization vector (IV)** via SHA-256.
- Accepts a plaintext message (terminated by Enter), up to **1024 bytes** (`MAX_MESSAGE_SIZE_ENCRYPTION`).
- Encrypts the message with **AES-256** in 16-byte blocks (mbedTLS AES-ECB with IV chaining).
- Computes a **32-byte HMAC-SHA-256** digest over the ciphertext.
- Prints **IV (16 bytes) | ciphertext | HMAC tag (32 bytes)** as hexadecimal text on the serial port.
In **decryption** mode, you paste the hex output from a prior encryption (same format), terminated by carriage return (CR). The application verifies the HMAC, decrypts, and prints the recovered plaintext.
**Hardware acceleration:** On Series 2 **HSE** and Series 3 **HSE** devices, crypto is accelerated in the **Secure Engine (SE)**. On Series 2 **VSE** devices, acceleration uses the **CRYPTOACC** peripheral. You can disable acceleration in the **Mbed TLS common functionality** component to compare performance.
**Components used:** `mbedtls_aes`, `mbedtls_hash`, `mbedtls_sha`, `mbedtls_ccm`, plus `sl_system`, `device_init`, `clock_manager`, and USART VCOM retargeting for stdio.

## Prerequisites / Setup Requirements

### Hardware Requirements

- A supported Silicon Labs development kit (see board compatibility in Simplicity Studio for `mbedtls_aescrypt` / `mbedtls_aescrypt_s3`).
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
3. Create the **Platform Security - SoC mbedTLS AES** project in Simplicity Studio ([Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)).
4. Build and flash the project ([Simple Build](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/building#simple-build), [Flash Programmer](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-building-and-flashing/flashing#flash-programmer)).
5. Reset the board. When prompted, type **`e`** for encrypt or **`d`** for decrypt.

### Encryption mode

1. Type a short phrase (Enter ends input; max 16 bytes) to help generate the IV.
2. Type the message to encrypt, then press **Enter** (max 1024 bytes).
3. Copy the hex line printed on the terminal: **IV (16 bytes) | ciphertext | HMAC tag (32 bytes)**.
4. Reset the board before running decryption.

### Decryption mode

1. After reset, choose **`d`**.
2. Paste the full hex string from encryption, ending with **CR** (carriage return, ASCII 13).
3. Confirm the decrypted plaintext appears on the serial port.

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| No serial output | VCOM port, 115200 8-N-1, line terminator **None**; `SL_BOARD_ENABLE_VCOM` enabled in project |
| Garbled or no input in Device Console | Line terminator must be **None**, not LF/CRLF |
| Decryption fails / "File too short" | Input must include full hex IV + ciphertext + 32-byte tag; end decryption input with **CR** |
| Encrypt then decrypt without reset | Reset required between encrypt and decrypt sessions |
| Crypto errors after SE update | Reflash latest SE firmware from Studio **General Device Information** |
| Programming fails | AEM switch position (see Prerequisites image) |

## Resources

- [Simplicity Studio 5 User's Guide — Examples](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-getting-started/start-a-project#examples)
- [UG103.5: mbed TLS Support in Silicon Labs SDK](https://www.silabs.com/documents/public/user-guides/ug103-05-fundamentals-mbedtls.pdf)
- [AN1311: Integrating Crypto Functionality into Applications](https://www.silabs.com/documents/public/application-notes/an1311-crypto-functionality-into-applications.pdf)

## Report Bugs & Get Support

You are always encouraged and welcome to report any issues you found to us via [Silicon Labs Community](https://www.silabs.com/community).
