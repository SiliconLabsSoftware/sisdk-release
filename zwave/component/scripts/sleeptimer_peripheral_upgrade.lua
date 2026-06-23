-- Upgrade helper: migrate sleeptimer peripheral to SYSRTC (DEFAULT) for Z-Wave 8.1+.

local changeset = {}

local device_series_2 = slc.is_provided("device_series_2")

if slc.is_selected("zw_core") and device_series_2 then
  local sleeptimer_peripheral = slc.config("SL_SLEEPTIMER_PERIPHERAL")
  if sleeptimer_peripheral ~= nil and sleeptimer_peripheral.value ~= "SL_SLEEPTIMER_PERIPHERAL_DEFAULT" then
    table.insert(changeset, {
      ["option"] = "SL_SLEEPTIMER_PERIPHERAL",
      ["value"] = "SL_SLEEPTIMER_PERIPHERAL_DEFAULT",
      ["description"] =
        "Use SYSRTC for the platform sleeptimer (BURTC is reserved for Z-Wave power management).",
      ["status"] = "automatic",
    })
  end
end

return changeset
