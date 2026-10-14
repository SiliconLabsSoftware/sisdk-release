-- Warns when a flashless part has no explicit external flash size selected.
-- ext_flash_none is only pulled in by the part's default recommendation, so
-- its presence reliably means "no size chosen"; picking a real external_flash_<size>_s3
-- component removes it via conflict and clears the warning.
if slc.is_provided("external_flash_none_s3") then
  validation.error(
    "[EXTFLASH] No external flash size selected; selecting a flash size for external flash part is mandatory.",
    validation.target_for_project(),
    "This part executes from external flash. Add an External Flash size component "
      .. "(Platform > Device > Flash) that matches your board's external flash so the "
      .. "memory map reflects the real device.",
    nil)
end
