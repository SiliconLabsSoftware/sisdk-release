local changeset = {}

if slc.is_selected('toolchain_gcc_lto') then
  table.insert(changeset, {
    ['component'] = 'toolchain_gcc_lto',
    ['action'] = 'remove',
  })
  if not slc.is_selected('toolchain_lto') then
    table.insert(changeset, {
      ['component'] = 'toolchain_lto',
      ['action'] = 'add',
    })
  end
end

return changeset
