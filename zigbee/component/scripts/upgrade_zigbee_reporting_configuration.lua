local changeset = {}

local reporting_configuration = slc.is_provided('zigbee_reporting')

if (reporting_configuration == true) then
  local config = slc.config('SL_ZIGBEE_AF_PLUGIN_REPORTING_ENABLE_RETRY')
  if (config == nil) then
    -- sisdk-2026.6.2 introduces SL_ZIGBEE_AF_PLUGIN_REPORTING_ENABLE_RETRY. Default is 1 (request an APS acknowledgement).
    table.insert(changeset, {
      ['option'] = 'SL_ZIGBEE_AF_PLUGIN_REPORTING_ENABLE_RETRY',
      ['value'] = tostring(1)
    })
  end
end

return changeset
