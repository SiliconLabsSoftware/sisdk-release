# Zigbee NCP + OpenThread RCP + Bluetooth RCP (CPC-SPI) Application

This concurrent multiprotocol (CMP) and dynamic multiprotocol (DMP) application runs the Zigbee NCP simultaneously with the OpenThread RCP and the Bluetooth RCP. The Bluetooth side provides a BLE controller over CPC for the host Bluetooth stack.

Communication with Zigbee, OpenThread, and Bluetooth host applications is enabled using the Co-Processor Communication Protocol, which acts as a protocol multiplexer and serial transport layer. The host applications connect to the CPC daemon, which in turn connects to the EFR via a SPI link. Note that this application cannot be used with the zigbee_z3_gateway and requires the Z3GatewayCPC as host.

The Zigbee NCP part of this application can be built as configured, or can optionally be augmented with customized extensions for initialization, main loop processing, event definition/handling, and messaging with the host.

Refer to the Silicon Labs Zigbee documentation for more information about NCP customization.

Refer to _[Running Zigbee, OpenThread, and Bluetooth Concurrently on a Linux Host with a Multiprotocol Co-processor](https://docs.silabs.com/multiprotocol/latest/multiprotocol-solution-linux/)_ for more information on running the multiprotocol co-processor with different host applications.
