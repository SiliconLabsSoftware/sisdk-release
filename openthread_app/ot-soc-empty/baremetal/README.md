# Thread SoC - Empty

This application demonstrates an OpenThread SoC application on a Full Thread Device (FTD), intended as a base for developing Thread applications. This application runs in a baremetal (non-RTOS) environment.

## Getting Started

For more information on building and running OpenThread on Silicon Labs hardware, see the [Silicon Labs OpenThread documentation](https://docs.silabs.com/openthread/latest/openthread-fundamentals-overview/). For OpenThread concepts, APIs, and configuration options, refer to the [OpenThread documentation](https://openthread.io/guides).

## How this application works

On startup, a Silicon Labs OpenThread device typically runs some initialization code, defined in the **app_init()** function. The application then runs a main loop that processes OpenThread tasklets and system drivers. This sample follows that flow with minimal additions. **setNetworkConfiguration()** reads dataset values from the application config (see below), fills an `otOperationalDataset`, and sets it as the active dataset. This sample's **app_init()** includes calls to **otIp6SetEnabled()** and **otThreadSetEnabled()** in order to bring up the IP interface and start Thread. All other behavior uses default OpenThread and platform behavior.

## Configuring the Thread Dataset

The **Default Dataset Values** OpenThread component contains the defines used by the application to set dataset values (channel, PAN ID, and network key). There are many ways to modify this dataset; configuring the component using Simplicity Studio, editing the component's config file (**config/sl_openthread_default_dataset_values_config.h**) directly, and directly editing the application code to use your own values instead of the ones defined by the component, to name a few.

## General steps for testing the application

This application does **not** include a CLI or any other direct way to interact with it. To verify that it is running and attached to a Thread network, use a second device. Flash the second device with an application that has a CLI (for example, **ot-cli-ftd**). In the config file above, note the channel, PAN ID, and network key used by the SoC Empty app. On the CLI device, configure the same operational dataset (e.g. via CLI commands or that app’s config), then form or join the same network. Once both devices are on the same network, use the CLI on the second device to check the neighbor table; the SoC Empty device should appear as a neighbor when it is attached and in range.

## Potential modifications

You can adapt this application for your project in two main ways:

- **Add your own logic:** The **app.c** source file includes comments that mark the most applicable places to insert code. Add one-time initialization in **app_init()** and recurring logic in **app_process_action()**.

- **Change project type or capabilities:** You can modify the project by adding, removing, or reconfiguring components in the `.slcp` file (e.g. in Simplicity Studio). For example, to turn this into a Minimal Thread Device (MTD) instead of an FTD, change the OpenThread stack component from the FTD variant to the MTD variant in the project’s component configuration and rebuild. The same approach applies to adding features such as CLI, CoAP, or other OpenThread or platform components—adjust the component list and configuration to match your requirements.
