--[[ For Zigbee NCP firmware on SoC: coordinator or router network device types need
    sufficient primary RAM. EFR32xG22-class targets (device_generic_family_efr32xg22)
    have 32 KB SRAM and do not meet the 64 KB minimum for FFD roles.
    Complements zigbee_soc_stack_config_validation.lua (which does not run when zigbee_ncp is used).
]]

local device_type_primary_val = slc.config("SLI_ZIGBEE_PRIMARY_NETWORK_DEVICE_TYPE").value
local device_type_secondary_val = slc.config("SLI_ZIGBEE_SECONDARY_NETWORK_DEVICE_TYPE").value
local secondary_network_enabled = slc.config("SLI_ZIGBEE_SECONDARY_NETWORK_ENABLED").value == "1"

local ffd_device_types_for_ram_check = Set(
    "SLI_ZIGBEE_NETWORK_DEVICE_TYPE_COORDINATOR_OR_ROUTER",
    "SLI_ZIGBEE_NETWORK_DEVICE_TYPE_ROUTER")
local primary_needs_min_ram = ffd_device_types_for_ram_check[device_type_primary_val] ~= nil
local secondary_needs_min_ram = secondary_network_enabled
    and ffd_device_types_for_ram_check[device_type_secondary_val] ~= nil

if slc.is_provided("zigbee_ncp")
    and slc.is_provided("device_cortexm")
    and slc.is_provided("device_generic_family_efr32xg22")
    and (primary_needs_min_ram or secondary_needs_min_ram) then
  validation.error(
      "NCP firmware: coordinator or router network device types require a target with at least 64 KB of primary RAM.",
      validation.target_for_defines({"SLI_ZIGBEE_PRIMARY_NETWORK_DEVICE_TYPE"}, {"SLI_ZIGBEE_SECONDARY_NETWORK_DEVICE_TYPE"}),
      "Choose an end device or sleepy end device type on this part, or migrate the NCP image to a device with at least 64 KB RAM (for example EFR32MG24).",
      nil)
end
