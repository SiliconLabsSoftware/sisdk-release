local changeset = {}

if slc.is_provided("dmadrv") then
  local dmadrv_dma_ch_priority = slc.config('EMDRV_DMADRV_DMA_CH_PRIORITY')
  local dmadrv_dma_ch_count = slc.config('EMDRV_DMADRV_DMA_CH_COUNT')

  if (dmadrv_dma_ch_priority ~= nil and dmadrv_dma_ch_count ~= nil and dmadrv_dma_ch_priority.value < dmadrv_dma_ch_count.value) then
    local round_robin_count = dmadrv_dma_ch_count.value - dmadrv_dma_ch_priority.value
    table.insert(changeset, {
      ['option'] = 'SL_DMA_MANAGER_ROUND_ROBIN_CHANNEL_COUNT',
      ['value'] = tostring(round_robin_count)
    })
  end
end

return changeset