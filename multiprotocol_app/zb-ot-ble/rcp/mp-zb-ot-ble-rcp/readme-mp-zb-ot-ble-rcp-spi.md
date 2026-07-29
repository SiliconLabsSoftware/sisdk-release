# Zigbee RCP + OpenThread RCP + Bluetooth RCP (CPC-SPI) Application

This concurrent multiprotocol (CMP) and dynamic multiprotocol (DMP) application runs Zigbee, OpenThread, and Bluetooth as radio co-processors (RCPs) on the same device. It uses CMP / multi-PAN functionality to run the 802.15.4 networks on the same channel, and DMP to run the Bluetooth link layer simultaneously. The Bluetooth side provides a BLE controller over CPC for the host Bluetooth stack.

Communication with Zigbee, OpenThread, and Bluetooth host applications is enabled using the Co-Processor Communication Protocol, which acts as a protocol multiplexer and serial transport layer. The host applications connect to the CPC daemon, which in turn connects to the EFR via a SPI link.

Refer to _[Running Zigbee, OpenThread, and Bluetooth Concurrently on a Linux Host with a Multiprotocol Co-processor](https://docs.silabs.com/multiprotocol/latest/multiprotocol-solution-linux/)_ for more information on running the multiprotocol RCP with different host applications.
