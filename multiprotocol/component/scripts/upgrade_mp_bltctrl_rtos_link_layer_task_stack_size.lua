local changeset = {}

local has_ot_ncp = slc.is_provide('ot_ncp_cpc') 
local has_freertos = slc.is_provide('freertos')
local has_lto = slc.is_provide('toolchain_gcc_lto') or slc.is_provide('toolchain_lto')

--[[
    This component directly defines SL_BTCTRL_RTOS_LINK_LAYER_TASK_STACK_SIZE configuration.
    Any other components that depend on these requirements will also be checked if this
    component is included in application (such as: bluetooth_hci_cpc, bluetooth_controller)
--]]
local has_btctrl_rtos_adaptation = slc.is_provide('bluetooth_controller_rtos_adaptation')

if has_ot_ncp and has_btctrl_rtos_adaptation and has_freertos and has_lto then
  local ll_stack = slc.config('SL_BTCTRL_RTOS_LINK_LAYER_TASK_STACK_SIZE')
  if ll_stack == nil then
    table.insert(changeset, {
      ['option'] = 'SL_BTCTRL_RTOS_LINK_LAYER_TASK_STACK_SIZE',
      ['value'] = '1100'
    })
  else
    local current = tonumber(ll_stack.value)
    if current ~= nil and current < 1100 then
      table.insert(changeset, {
        ['option'] = 'SL_BTCTRL_RTOS_LINK_LAYER_TASK_STACK_SIZE',
        ['value'] = '1100'
      })
    end
  end
end

return changeset
