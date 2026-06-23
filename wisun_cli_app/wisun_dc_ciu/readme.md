# DC CIU - Direct Connect control interface unit

## Overview

The DC CIU (Direct Connect Control Interface Unit) is a Direct Connect
client application. It automatically scans for a DC server, connects, and
enables UDP messaging.

## Quick Start

1. **Power on** the device
2. **Press BTN0** within 60 seconds to start
3. Device scans and connects automatically
4. **Press BTN1** to send messages
5. **Press BTN0** again to stop

If no button is pressed within 60 seconds, the device enters deep sleep (EM4).

## Button Functions

| Button | Action |
|--------|--------|
| **BTN0** | Start / Stop |
| **BTN1** | Send message (when connected) |

## Display Status

The LCD shows the current state and button hints:

| Display | Meaning |
|---------|---------|
| `BTN0 or EM4` | Ready to start, will sleep if idle |
| `Scanning...` | Looking for server |
| `Connecting...` | Establishing connection |
| `OK in X.Xs` | Connected (shows connection time) |
| `TX: msg #N` | Message sent |
| `RX: ...` | Message received |

## CLI Commands

Configure the device via serial console:

```
dc get                    Show all settings
dc get <setting>          Show specific setting
dc set <setting> <value>  Change a setting
dc save                   Save to flash
dc reset                  Reset to defaults
dc status                 Show current state
```

### Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `regulatory_domain` | EU | Region (WW, NA, JP, EU, CN, IN, MX, BZ, AZ, KR) |
| `chan_plan_id` | 33 | Channel plan |
| `phy_mode_id` | 3 | PHY mode |
| `dc_id` | DC_ID_DEFAULT | Server ID to connect to |
| `pmk` | (preset) | Security key (64 hex chars) |
| `server_port` | 1234 | UDP port |
| `idle_timeout_ms` | 60000 | Sleep timeout (ms) |

### Example

```
dc set regulatory_domain NA
dc set dc_id MY_SERVER
dc save
```

Then press BTN0 to start with new settings.

## Power Management

The device enters EM4 deep sleep:
- After 60 seconds of inactivity (configurable via `idle_timeout_ms`)
- After stopping the connection

Wake the device by pressing the BTN1.
