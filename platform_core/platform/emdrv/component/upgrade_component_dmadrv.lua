local changeset = {}

if slc.is_provided("dmadrv") then
  local dmadrv_dma_ch_priority = slc.config('EMDRV_DMADRV_DMA_CH_PRIORITY')
  local dmadrv_dma_ch_count = slc.config('EMDRV_DMADRV_DMA_CH_COUNT')

  if (dmadrv_dma_ch_priority ~= nil and dmadrv_dma_ch_count ~= nil and dmadrv_dma_ch_priority.value < dmadrv_dma_ch_count.value) then
    if not slc.is_provided('dma_manager_round_robin') then
      table.insert(changeset, {
        ['component'] = 'dma_manager_round_robin',
        ['action'] = 'add'
      })
    end
  end
end

return changeset
