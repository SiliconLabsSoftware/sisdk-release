from pyradioconfig.parts.lion.phys.Phys_RAIL_Base_Standard_IEEE802154 import PhysRailBaseStandardIEEE802154Lion


class PhysRailBaseStandardIEEE802154Curl(PhysRailBaseStandardIEEE802154Lion):

    def PHY_IEEE802154_2p4GHz(self, model, phy_name=None):
        phy = super().PHY_IEEE802154_2p4GHz(model, phy_name)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy
