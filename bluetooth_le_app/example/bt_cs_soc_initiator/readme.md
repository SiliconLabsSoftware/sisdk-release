# SoC - CS Initiator

The Bluetooth SoC-CS Initiator is a project that can be used to test the Channel Sounding (CS) feature. In the provided CS setup, the application establishes connection to a reflector (Running on the host or SoC), measures in the phase based ranging (PBR) or round trip time (RTT) CS measurement modes and estimates the distance. The reflector data is obtained using the Ranging Service (RAS). The RAS Real-time mode enabled real-time data reception from the RAS Server. In on-demand mode the RAS client included in the initiator will ask for the ranging data after the data reception is finished. Tracking accuracy optimized, Tracking latency optimized, and Stationary algorithm modes are also supported for the measurement process. In Tracking accuracy optimized and Tracking latency optimized modes distance will be calculated for every CS procedure while in Stationary mode the calculation requires multiple CS procedures data. Tracking accuracy optimized (suitable for moving targets) uses medium filtering, medium response and medium CPU cost. Tracking latency optimized (suitable for fast moving targets) uses low filtering, low CPU and RAM cost and provides basic accuracy. In Stationary (suitable for stationary targets) mode during measurement the percentage of the progress is displayed on the LCD (if the device has LCD) and logged to the console. Once all required CS procedure data is received for the distance measurement, the estimated result will arrive and it will be displayed on the LCD (if the device has LCD) and logged to the console. In order to select different algorithm modes the push button can be pressed during device RESET. The push button BTN1 will change the object tracking mode to Stationary. Default values can be found and modified in the component configuration file (config/cs_initiator_config.h).
If the configuration is changed to create more than 1 initiator instances, SL_BT_CONFIG_BUFFER_SIZE shall be increased.

> Note: this example does not include Device Firmware Update (DFU) functionality by default. For details see the [Device Firmware Update](#device-firmware-update) section.


## Usage

- Build and flash the sample application.

- The default object tracking mode is Tracking latency optimized (suitable for fast moving targets). Pressing BTN1 while resetting the device selects Stationary (suitable for stationary targets) algorithm mode.

- After startup the CS initiator will scan for a device running the "CS RFLCT" sample application.

- When found, the initiator will establish connection to the CS reflector device and will start the distance measurement process. By default the CS initiator can create 4 connections.

- The initiator will calculate the distance, display it on the LCD (if the device has LCD) and also send them via UART. Note: in case of Stationary mode multiple CS procedure data will be required. Until the distance measurement is in progress the progress percentage will be displayed on the LCD (if the device has LCD) and logged to the console.


![](./image/cs_lcd.png)

## Multiconnection

- Default setup is optimized for 1-1 connection, multiconnection setup requires modification of the timing parameters to operate as expected. Timing can be adjusted by the procedure_interval and connection_interval parameters.
- Use the following calculation for 1-N connection: procedure_time_1_N[ms] = connection_interval[ms] * procedure_interval * N
- Note that setting CS_INITIATOR_DEFAULT_MIN/MAX_CONNECTION_INTERVAL and CS_INITIATOR_DEFAULT_MIN/MAX_PROCEDURE_INTERVAL will only take effect if CS_INITIATOR_DEFAULT_PROCEDURE_SCHEDULING is set to CS_PROCEDURE_SCHEDULING_CUSTOM. Otherwise these parameters are managed by the application.
- If getting frequent measurement results is not priority, it's safe to use procedure_interval = 120 and connection_interval = 24 even with the maximum number of connections (4).
- If more than 1 initiator instances are created increase SL_BT_CONFIG_BUFFER_SIZE. With maximum number of instances (4) it's safe to use 22000.

## Resource optimization

- Flash usage can be reduced by
  - removing "Bluetooth controller anchor selection" component if no multiple reflector connection is required,
  - turning off "Logging"-"Initiator component" feature in "CS Initiator" component, CS_INITIATOR_UART_LOG in application config (app_config.h) or application logging in "Application"- "Utility" -"Log" component configuration.
- RAM usage can be reduced by
  - decreasing the "Maximum initiator connections" in "CS Initiator" component configuration to the required amount,
  - decreasing "Maximum ranging data size" in "CS Initiator" component configuration. Note that "Maximum ranging data size" should be enough to store Ranging Data in format defined in RAS specification,
  - reducing "Buffer memory size for Bluetooth stack" in "Bluetooth Core" component configuration if the "Maximum initiator connections" is changed to create less than 4 initiator instances.

### Calculating the size of "Maximum ranging data size"

The optimal value of "Maximum ranging data size" is dependent on several configuration values, and can be calculated by the following equation:

ranging_max_size = 4 + (subevents * 8) + (subevents * mode0_steps * mode0_size) + channels * ( ( 1 + ( antenna_paths + 1 ) * 4) + 1 )

where
- subevents is the number of CS subevents per procedure (range: 1..32), determined by the
controller based on CS_INITIATOR_DEFAULT_MIN_SUBEVENT_LEN and CS_INITIATOR_DEFAULT_MAX_SUBEVENT_LEN.
Shorter subevent lengths allow more subevents per procedure.
- mode0_size is
  - 4 for Reflector and
  - 6 for Initiator,
- mode0_steps value is the configuration "Mode 0 steps",
- channels value means the number of channels from the channel mask that can be derived from the "Channel map preset" settings:
  - "High"   - 72 (default),
  - "Medium" - 37,
  - "Custom" - Number of 1s in channel mask,
- antenna_paths value is controlled by the "Antenna configuration", and limited by number of antennas presented on each board (capabilities). Maximum can be calculated using the product of used Initiator and Reflector antennae. The default maximum value for antenna_paths is 4.

These settings were selected by assuming that the controller creates the maximum number of subevents (32), and the measuring mode is PBR. In RTT mode, far less data is created.

If you use submode, you should add the following to the sum:

(1 + mode1_size) * channels / main_mode_steps

where
- mode1_size is 6
- main_mode_steps is the value of min_main_mode_steps ranging from to 2. This can be changed in cs_initiator_client.h.

The default is calculated by using the constants and settings above using the worst case scenario, which gives 2672 bytes.
RAM consumption can be reduced by changing the affected settings and reducing "Procedure maximum length" accordingly.

### Subevents

A CS procedure consists of one or more subevents (range: 1..32), each containing a set of CS steps. Subevent count is based on CS_INITIATOR_DEFAULT_MIN_SUBEVENT_LEN (default: 1250 us) and CS_INITIATOR_DEFAULT_MAX_SUBEVENT_LEN (default: 3999999 us), but the controller determines the actual subevent count and scheduling at runtime and it may differ from these configured values based on resource constraints and scheduling feasibility. With the default maximum of ~4 s, all steps fit in a single subevent. Reducing the maximum causes the controller to split steps across multiple shorter subevents. More subevents require a larger RAS buffer and therefore more RAM.

When using multiple subevents:
- Ensure that the effective procedure interval is at least the number of created subevents, plus additional connection events for RAS data transfer.
  The effective procedure interval is determined by CS_INITIATOR_DEFAULT_PROCEDURE_SCHEDULING, or by CS_INITIATOR_DEFAULT_MAX_PROCEDURE_INTERVAL when custom scheduling is used.
- The minimum subevent length must fit within the procedure time window: max_procedure_interval * max_connection_interval * 1250 us.
- As each subevent contains Mode 0 steps followed by main mode steps, the subevent length must be large enough to accommodate their combined duration.

The following table shows example scenarios with other configuration parameters left at their defaults.

| Scenario | MIN subevent length | MAX subevent length | Subevents (approx.)| Effective procedure interval |
|---|---|---|---|---|
| Single subevent (default) | 1250 us | 3999999 us | 1 | All steps fit in one subevent |
| Few subevents | 1250 us | 15000 us | 3 | 3 + RAS overhead |
| Many subevents | 1250 us | 4000 us | 18 | 18 + RAS overhead |
| Maximum subevents | 1250 us | 2000 us | 32 | 32 + RAS overhead |

## Known issues and limitations

* In case RTT mode used with Stationary algorithm mode the behavior will be the same as RTT with Tracking accuracy optimized or Tracking latency optimized mode.
* CS main mode RTT and CS algo mode Tracking latency optimized combination is not supported.
* CS algo mode Tracking latency optimized and synchronized procedure execution (max procedure count == 1) combination is not supported.

## Device Firmware Update

This example project does not include Device Firmware Update (DFU) functionality by default, but it can be added easily.
SoC applications can use one of Silicon Labs' Over-the-Air (OTA) DFU implementations. The table below summarizes the options:

|                           | In-place OTA DFU                 | Application OTA DFU                 |
|---------------------------|----------------------------------|-------------------------------------|
| **Component to add**      | In-place OTA DFU                 | Application OTA DFU                 |
| **Compatible bootloader** | Bluetooth Apploader OTA DFU      | Bootloader - SoC Internal Storage (Series 2) <br> Bootloader - SoC Storage (Series 3) |
| **Reference solution**    | Bluetooth - SoC In-Place OTA DFU | Bluetooth - SoC Application OTA DFU |
| **Supported devices**     | Supports Series 2 devices only and requires a smaller flash size | Supports Series 2 and Series 3 devices with enough flash to store firmware images in 2 instances |

To add DFU to an existing project:
- Add the appropriate DFU component to your project using Simplicity Studio’s Software Component browser.
- Add a post-build step to generate the GBL (Gecko Bootloader) file using Simplicity Studio’s Post Build Editor.
- Rebuild the project.
- Flash a compatible bootloader to the device.

For more information on bootloaders, see [UG103.6: Bootloader Fundamentals](https://www.silabs.com/documents/public/user-guides/ug103-06-fundamentals-bootloading.pdf) and [UG489: Silicon Labs Gecko Bootloader User's Guide for GSDK 4.0 and Higher](https://www.silabs.com/documents/public/user-guides/ug489-gecko-bootloader-user-guide-gsdk-4.pdf).

## Troubleshooting

## Resources

[Bluetooth Documentation](https://docs.silabs.com/bluetooth/latest/)

[UG103.14: Bluetooth LE Fundamentals](https://www.silabs.com/documents/public/user-guides/ug103-14-fundamentals-ble.pdf)

[QSG169: Bluetooth SDK v3.x Quick Start Guide](https://www.silabs.com/documents/public/quick-start-guides/qsg169-bluetooth-sdk-v3x-quick-start-guide.pdf)

[UG434: Silicon Labs Bluetooth ® C Application Developer's Guide for SDK v3.x](https://www.silabs.com/documents/public/user-guides/ug434-bluetooth-c-soc-dev-guide-sdk-v3x.pdf)

[Bluetooth Training](https://www.silabs.com/support/training/bluetooth)

[Ranging Service](https://www.bluetooth.com/specifications/specs/ranging-service-1-0/)
