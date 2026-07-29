# Zigbee NCP + OpenThread RCP (CPC-UART) Application

This concurrent multiprotocol (CMP) application runs the Zigbee NCP simultaneously with the OpenThread RCP.

Communication with Zigbee and OpenThread host applications is enabled using the Co-Processor Communication Protocol, which acts as a protocol multiplexer and serial transport layer. The host applications connect to the CPC daemon, which in turn connects to the EFR via a UART link.

The Zigbee NCP part of this application can be built as configured, or can optionally be augmented with customized extensions for initialization, main loop processing, event definition/handling, and messaging with the host.

Refer to the Silicon Labs Zigbee documentation for more information about NCP customization.
