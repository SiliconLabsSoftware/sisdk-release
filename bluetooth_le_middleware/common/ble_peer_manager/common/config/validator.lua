-- validation script for proper component configuration
local peer_manager_max_conn = slc.config("BLE_PEER_MANAGER_COMMON_MAX_ALLOWED_CONN_COUNT")
local bt_config_max_conn = slc.config("SL_BT_CONFIG_MAX_CONNECTIONS")

if peer_manager_max_conn == nil or bt_config_max_conn == nil then
  return
end

if peer_manager_max_conn.number > bt_config_max_conn.number then
    validation.error(
      "The Peer Manager " .. peer_manager_max_conn.value .. " shall be lower than or equal to the Bluetooth specific " .. bt_config_max_conn.value .. "",
      validation.target_for_defines({"BLE_PEER_MANAGER_COMMON_MAX_ALLOWED_CONN_COUNT", "SL_BT_CONFIG_MAX_CONNECTIONS"}),
      "Please set these values properly!",
      nil)
end
