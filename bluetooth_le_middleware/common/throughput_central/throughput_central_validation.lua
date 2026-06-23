-- throughput central validation script
local modify_msg = "Modify throughput_central_config.h!"

-- MTU size validation
local mtu_size = slc.config("THROUGHPUT_CENTRAL_MTU_SIZE")
local min_mtu = 23
local mtu_max = slc.config("THROUGHPUT_MAXIMUM_MTU_SIZE")

if mtu_size ~= nil and mtu_size.number ~= nil and mtu_max ~= nil and mtu_max.number ~= nil then
  if mtu_size.number < min_mtu or mtu_size.number > mtu_max then
    validation.error(
      "THROUGHPUT_CENTRAL_MTU_SIZE (" .. mtu_size.value .. ") is out of range! Valid range is "
        .. tostring(min_mtu) .. " to " .. tostring(mtu_max) .. " (THROUGHPUT_MAXIMUM_MTU_SIZE).",
      validation.target_for_defines({"THROUGHPUT_CENTRAL_MTU_SIZE"}),
      "Please set THROUGHPUT_CENTRAL_MTU_SIZE to a value between " .. tostring(min_mtu)
        .. " and " .. tostring(mtu_max) .. "! " .. modify_msg,
      nil)
  end
end

-- MAC address format validation in allowlist
local slots = {
    {
        name = "Slot 1",
        enable = "THROUGHPUT_CENTRAL_ALLOWLIST_SLOT_1_ENABLE",
        slot = "THROUGHPUT_CENTRAL_ALLOWLIST_SLOT_1"
    },
    {
        name = "Slot 2",
        enable = "THROUGHPUT_CENTRAL_ALLOWLIST_SLOT_2_ENABLE",
        slot = "THROUGHPUT_CENTRAL_ALLOWLIST_SLOT_2"
    },
    {
        name = "Slot 3",
        enable = "THROUGHPUT_CENTRAL_ALLOWLIST_SLOT_3_ENABLE",
        slot = "THROUGHPUT_CENTRAL_ALLOWLIST_SLOT_3"
    },
    {
        name = "Slot 4",
        enable = "THROUGHPUT_CENTRAL_ALLOWLIST_SLOT_4_ENABLE",
        slot = "THROUGHPUT_CENTRAL_ALLOWLIST_SLOT_4"
    }
}

local mac_pattern = "(%x%x:%x%x:%x%x:%x%x:%x%x:%x%x)"

function check_mac(address)
    local maclist = string.match(address,mac_pattern)
    if maclist ~= nil then
        if maclist == address then
            return true
        end
    end
    return false
end

local wl_enabled = slc.config("THROUGHPUT_CENTRAL_ALLOWLIST_ENABLE").number

if wl_enabled ~= nil and wl_enabled == 1 then
    for k,v in pairs(slots) do
        local slot_enabled = slc.config(v.enable).number
        if slot_enabled ~= nil and slot_enabled == 1 then
                local slot = slc.config(v.slot)
                local slot_formatted = slot.value:gsub("\""," "):gsub("%s","")
            if slot ~= nil then
                local result = check_mac(slot_formatted)
                if not result then
                    validation.error("MAC address " .. slot_formatted .. " for " .. v.name .. " is not valid! ",
                    validation.target_for_defines({v.slot}),
                    "MAC address shall be in FF:FF:FF:FF:FF:FF hexadecimal format.",
                    nil)
                end
            end
        end
    end
end
