from pyradioconfig.parts.lion.phys.Phys_RAIL_Base_Standard_BLE import PhysRailBaseStandardBluetoothLeLion


class PhysRailBaseStandardBluetoothLeCurl(PhysRailBaseStandardBluetoothLeLion):

    # Lion BLE PHYs
    def PHY_Bluetooth_1M(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_1M(model, phy_name)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_1M_AOX(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='BLE 1Mbps AOX PHY for Panther', phy_name=phy_name)
        self.Bluetooth_LE_base(phy, model)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_1M_Concurrent(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_1M_Concurrent(model, phy_name)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LE_2M_Viterbi_noDSA_fullrate(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_LE_2M_Viterbi_noDSA_fullrate(model, phy_name)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LE_Viterbi_noDSA(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_LE_Viterbi_noDSA(model, phy_name)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LE_Viterbi_noDSA_fullrate(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_LE_Viterbi_noDSA_fullrate(model, phy_name)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LR_125k(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='Production BLE LongRange 125kbps PHY for Panther', phy_name=phy_name)
        self.Bluetooth_LongRange_base(phy, model)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LR_500k(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='Production BLE LongRange 500kbps PHY for Panther', phy_name=phy_name)
        self.Bluetooth_LongRange_500kbps_base(phy, model)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LongRange_dsa_125kbps(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_LongRange_dsa_125kbps(model, phy_name)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LongRange_dsa_500kbps(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_LongRange_dsa_500kbps(model, phy_name)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LongRange_nodsa_125kbps(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_LongRange_nodsa_125kbps(model, phy_name)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    def PHY_Bluetooth_LongRange_nodsa_500kbps(self, model, phy_name=None):
        phy = super().PHY_Bluetooth_LongRange_nodsa_500kbps(model, phy_name)
        phy.profile_inputs.xtal_frequency_hz.value = 40000000

        return phy

    # Curl overrides: Calculate TXBR and frequencies based on xtal

    @staticmethod
    def _remove_xtal_overrides(phy):
        # Setting to None so that these variables are calculated
        phy.profile_outputs.MODEM_TXBR_TXBRDEN.override = None
        phy.profile_outputs.MODEM_TXBR_TXBRNUM.override = None
        phy.profile_outputs.MODEM_DIGMIXCTRL_DIGMIXFREQ.override = None
        phy.profile_outputs.SYNTH_CHSP_CHSP.override = None
        phy.profile_outputs.SYNTH_FREQ_FREQ.override = None
        phy.profile_outputs.SYNTH_IFFREQ_IFFREQ.override = None

    def Bluetooth_LE_Viterbi_BLEIQDSA_base(self, phy, model):
        super().Bluetooth_LE_Viterbi_BLEIQDSA_base(phy, model)
        self._remove_xtal_overrides(phy)

    def Bluetooth_LE_Viterbi_base(self, phy, model):
        super().Bluetooth_LE_Viterbi_base(phy, model)
        self._remove_xtal_overrides(phy)

    def Bluetooth_LE_2M_Viterbi_base(self, phy, model):
        super().Bluetooth_LE_2M_Viterbi_base(phy, model)
        self._remove_xtal_overrides(phy)

    def Bluetooth_LongRange_base(self, phy, model):
        super().Bluetooth_LongRange_base(phy, model)
        self._remove_xtal_overrides(phy)

