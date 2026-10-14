local changeset = {}

if slc.is_provided("zigbee_pro_leaf_stack_with_csl") then
  local neighbor_table_size = slc.config("SL_ZIGBEE_NEIGHBOR_TABLE_SIZE")

  -- Upgrade projects still using the old leaf default (< 16) to the CSL default.
  -- Values already in the supported CSL range [16, 26] are left unchanged.
  if neighbor_table_size == nil or tonumber(neighbor_table_size.value) < 16 then
    if neighbor_table_size ~= nil then
      table.insert(changeset, {
        ['option'] = 'SL_ZIGBEE_NEIGHBOR_TABLE_SIZE',
        ['action'] = 'remove'
      })
    end

    table.insert(changeset, {
      ['option'] = 'SL_ZIGBEE_NEIGHBOR_TABLE_SIZE',
      ['value'] = '16'
    })
  end
end

return changeset
