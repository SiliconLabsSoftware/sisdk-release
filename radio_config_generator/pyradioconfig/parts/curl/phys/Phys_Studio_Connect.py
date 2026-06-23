from pyradioconfig.parts.lion.phys.Phys_Studio_Connect import PhysStudioConnectLion


class PhysStudioConnectCurl(PhysStudioConnectLion):

    def PHY_Connect_2_4GHz_OQPSK_2Mcps_250kbps(self, model, phy_name=None):
        phy = super().PHY_Connect_2_4GHz_OQPSK_2Mcps_250kbps(model)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy
