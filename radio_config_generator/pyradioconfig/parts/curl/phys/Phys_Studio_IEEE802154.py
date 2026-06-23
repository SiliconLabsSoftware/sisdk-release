from pyradioconfig.parts.lion.phys.Phys_Studio_IEEE802154 import PhysStudioIEEE802154Lion


class PhysStudioIEEE802154Curl(PhysStudioIEEE802154Lion):

    def PHY_IEEE802154_2p4GHz_prod(self, model, phy_name=None):
        phy = super().PHY_IEEE802154_2p4GHz_prod(model, phy_name)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy
