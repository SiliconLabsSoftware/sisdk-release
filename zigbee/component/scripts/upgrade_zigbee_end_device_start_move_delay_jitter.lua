local changeset = {}

local zigbee_end_device_support_configuration = slc.is_provided('zigbee_end_device_support')

if (zigbee_end_device_support_configuration == true) then
  local move_jitter_config = slc.config('SL_ZIGBEE_AF_PLUGIN_END_DEVICE_SUPPORT_START_MOVE_DELAY_JITTER_SECONDS')
  if (move_jitter_config == nil) then
    -- sisdk-2026.6.2 introduces SL_ZIGBEE_AF_PLUGIN_END_DEVICE_SUPPORT_START_MOVE_DELAY_JITTER_SECONDS. Default is 0
    table.insert(changeset, {
      ['option'] = 'SL_ZIGBEE_AF_PLUGIN_END_DEVICE_SUPPORT_START_MOVE_DELAY_JITTER_SECONDS',
      ['value'] = tostring(0)
    })
  end
end

return changeset
