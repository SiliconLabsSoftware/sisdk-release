from pyradioconfig.parts.lion.phys.Phys_Studio_BLE import PhysStudioBLELion


class PhysStudioBLECurl(PhysStudioBLELion):

    def PHY_Bluetooth_1M_AOX_prod(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_1M_AOX_prod(model, phy_name)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_1M_Concurrent_prod(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_1M_Concurrent_prod(model, phy_name)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_1M_prod(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_1M_prod(model, phy_name)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_2M_AOX_prod(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_2M_AOX_prod(model, phy_name)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_2M_prod(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_2M_prod(model, phy_name)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LR_125k_prod(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_LR_125k_prod(model, phy_name)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LR_500k_prod(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_LR_500k_prod(model, phy_name)

        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy
