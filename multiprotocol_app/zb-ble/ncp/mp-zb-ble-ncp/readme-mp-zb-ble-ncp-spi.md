# Zigbee NCP + Bluetooth NCP (CPC-SPI) Application

This dynamic multiprotocol (DMP) application runs the Zigbee NCP simultaneously with the Bluetooth NCP.

Communication with Zigbee and Bluetooth host applications is enabled using the Co-Processor Communication Protocol, which acts as a protocol multiplexer and serial transport layer. The host applications connect to the CPC daemon, which in turn connects to the EFR via a SPI link. Note that this application cannot be used with the zigbee_z3_gateway and requires the Z3GatewayCPC as host.

The Zigbee NCP part of this application can be built as configured, or can optionally be augmented with customized extensions for initialization, main loop processing, event definition/handling, and messaging with the host.

Refer to the Silicon Labs Zigbee documentation for more information about NCP customization.
