local changeset = {}

if slc.is_provided('ncp')
  and slc.is_provided('iostream_dummy')
  and slc.is_provided('iostream_bgapi_trace') then
  table.insert(changeset, {
    ['component'] = 'iostream_dummy',
    ['action'] = 'remove'
  })
end

return changeset
