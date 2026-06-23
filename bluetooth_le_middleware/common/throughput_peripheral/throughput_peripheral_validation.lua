-- throughput peripheral validation script
local modify_msg = "Modify throughput_peripheral_config.h!"

-- MTU size validation
local mtu_size = slc.config("THROUGHPUT_PERIPHERAL_MTU_SIZE")
local min_mtu = 23
local mtu_max = slc.config("THROUGHPUT_MAXIMUM_MTU_SIZE")

if mtu_size ~= nil and mtu_size.number ~= nil and mtu_max ~= nil and mtu_max.number ~= nil then
  if mtu_size.number < min_mtu or mtu_size.number > mtu_max then
    validation.error(
      "THROUGHPUT_PERIPHERAL_MTU_SIZE (" .. mtu_size.value .. ") is out of range! Valid range is "
        .. tostring(min_mtu) .. " to " .. tostring(mtu_max) .. " (THROUGHPUT_MAXIMUM_MTU_SIZE).",
      validation.target_for_defines({"THROUGHPUT_PERIPHERAL_MTU_SIZE"}),
      "Please set THROUGHPUT_PERIPHERAL_MTU_SIZE to a value between " .. tostring(min_mtu)
        .. " and " .. tostring(mtu_max) .. "! " .. modify_msg,
      nil)
  end
end
