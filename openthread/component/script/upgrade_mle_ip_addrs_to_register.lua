-- OPENTHREAD_CONFIG_MLE_IP_ADDRS_TO_REGISTER was removed upstream (openthread PR #12997).
-- MTDs now register all valid unicast/multicast addresses unconditionally.
-- If a project overrides this config it will fail to compile; remove it here.

local changeset = {}

if slc.config('OPENTHREAD_CONFIG_MLE_IP_ADDRS_TO_REGISTER') ~= nil then
  table.insert(changeset, {
    ['option'] = 'OPENTHREAD_CONFIG_MLE_IP_ADDRS_TO_REGISTER',
    ['action'] = 'remove'
  })
end

return changeset
