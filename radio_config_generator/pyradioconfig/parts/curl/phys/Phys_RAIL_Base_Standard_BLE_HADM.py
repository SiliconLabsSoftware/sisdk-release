from pyradioconfig.parts.curl.phys.Phys_RAIL_Base_Standard_BLE import PhysRailBaseStandardBluetoothLeCurl
from pyradioconfig.calculator_model_framework.interfaces.iphy import IPhy


class PhysRailBaseStandardBluetoothHadmCurl(IPhy):

    def _set_xtal_frequency(self, phy, xtal_freq=None):
        if xtal_freq is None:
            phy.profile_inputs.xtal_frequency_hz.value = 40000000
        else:
            phy.profile_inputs.xtal_frequency_hz.value = xtal_freq

    # New HADM PHYs
    def PHY_Bluetooth_1M_HADM(self, model, phy_name='PHY_Bluetooth_1M_HADM'):
        phy = PhysRailBaseStandardBluetoothLeCurl().PHY_Bluetooth_LE_Viterbi_noDSA_fullrate(model, phy_name=phy_name)
        self._set_xtal_frequency(phy, 40000000)
        phy.profile_inputs.bandwidth_hz.value = 1100000
        phy.profile_inputs.hadm_enable.value = model.vars.hadm_enable.var_enum.ENABLED
        model.vars.adc_clock_mode.value_forced = model.vars.adc_clock_mode.var_enum.HFXOMULT

        # Packet Inputs
        phy.profile_inputs.frame_bitendian.value = model.vars.frame_bitendian.var_enum.LSB_FIRST
        phy.profile_inputs.frame_length_type.value = model.vars.frame_length_type.var_enum.FIXED_LENGTH
        phy.profile_inputs.payload_white_en.value = False
        phy.profile_inputs.payload_crc_en.value = False

        # Variable length includes header
        phy.profile_inputs.header_en.value = False

        # NOTE: Currently the 'header_include_crc' variable is not part of the
        # profile inputs, so we can't set it here, instead we need to force the
        # output for both FCDs (TX/RX).
        phy.profile_outputs.FRC_FCD0_INCLUDECRC.override = 0
        phy.profile_outputs.FRC_FCD2_INCLUDECRC.override = 0

        # AFC at syncword via VTAFCFRAME. Disable feedback to SYNTH as frequency estimates may not be valid with UCAS
        phy.profile_outputs.MODEM_REALTIMCFE_VTAFCFRAME.override = 1  # estimate from syncword
        phy.profile_outputs.MODEM_AFC_AFCONESHOT.override = 0
        phy.profile_outputs.MODEM_AFC_AFCRXMODE.override = 0  # no estimate from DSA
        phy.profile_outputs.MODEM_AFC_AFCSCALEM.override = 0  # disable feedback to avoid updates during tracking cycle
        phy.profile_outputs.MODEM_AFC_AFCSCALEE.override = 0

        # needed for precise HADM event timing - HADM PHYs are 40 MHz only
        phy.profile_outputs.rx_sync_delay_ns.override = 24000
        phy.profile_outputs.rx_eof_delay_ns.override = 8000
        phy.profile_outputs.tx_sync_delay_ns.override = 0
        phy.profile_outputs.tx_eof_delay_ns.override = 0

        phy.profile_outputs.HADM_CTRL0_PHYSEL.override = 0

        return phy

    def PHY_Bluetooth_2M_HADM(self, model, phy_name='PHY_Bluetooth_2M_HADM'):
        phy = PhysRailBaseStandardBluetoothLeCurl().PHY_Bluetooth_LE_2M_Viterbi_noDSA_fullrate(model, phy_name=phy_name)
        self._set_xtal_frequency(phy, 40000000)
        phy.profile_inputs.hadm_enable.value = model.vars.hadm_enable.var_enum.ENABLED
        model.vars.adc_clock_mode.value_forced = model.vars.adc_clock_mode.var_enum.HFXOMULT

        # Packet Inputs
        phy.profile_inputs.frame_bitendian.value = model.vars.frame_bitendian.var_enum.LSB_FIRST
        phy.profile_inputs.frame_length_type.value = model.vars.frame_length_type.var_enum.FIXED_LENGTH
        phy.profile_inputs.payload_white_en.value = False
        phy.profile_inputs.payload_crc_en.value = False

        # Variable length includes header
        phy.profile_inputs.header_en.value = False

        # NOTE: Currently the 'header_include_crc' variable is not part of the
        # profile inputs, so we can't set it here, instead we need to force the
        # output for both FCDs (TX/RX).
        phy.profile_outputs.FRC_FCD0_INCLUDECRC.override = 0
        phy.profile_outputs.FRC_FCD2_INCLUDECRC.override = 0

        # AFC at syncword via VTAFCFRAME. Disable feedback to SYNTH as frequency estimates may not be valid with UCAS
        phy.profile_outputs.MODEM_REALTIMCFE_VTAFCFRAME.override = 1 # estimate from syncword
        phy.profile_outputs.MODEM_AFC_AFCONESHOT.override = 0
        phy.profile_outputs.MODEM_AFC_AFCRXMODE.override = 0 # no estimate from DSA
        phy.profile_outputs.MODEM_AFC_AFCSCALEM.override = 0  # disable feedback to avoid updates during tracking cycle
        phy.profile_outputs.MODEM_AFC_AFCSCALEE.override = 0

        phy.profile_outputs.HADM_CTRL0_PHYSEL.override = 1

        return phy

    def PHY_Bluetooth_2M_HADM_2BT(self, model, phy_name='PHY_Bluetooth_2M_HADM_2BT'):
        phy = self.PHY_Bluetooth_2M_HADM(model, phy_name)

        # this has no effect as of now but will reflect correct shaping coeff in cfg
        phy.profile_inputs.shaping_filter_param.value = 2.0
        phy.profile_outputs.HADM_CTRL0_PHYSEL.override = 2
        phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI1.override = 64
        phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI2.override = 53
        phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI3.override = 41

        return phy


    ##########################
    # HADM PHYs for each XTAL Frequency for design
    # since design can not have xtal_freq as override, they need a PHY to run RTL sim for each XTAL frequency
    ##########################

    def PHY_Bluetooth_1M_HADM_38MHz(self, model, phy_name='PHY_Bluetooth_1M_HADM_38MHz'):
        phy = self.PHY_Bluetooth_1M_HADM(model, phy_name)
        self._set_xtal_frequency(phy, 38000000)

        return phy

    def PHY_Bluetooth_1M_HADM_38p4MHz(self, model, phy_name='PHY_Bluetooth_1M_HADM_38p4MHz'):
        phy = self.PHY_Bluetooth_1M_HADM(model, phy_name)
        self._set_xtal_frequency(phy, 38400000)

        return phy

    def PHY_Bluetooth_1M_HADM_39MHz(self, model, phy_name='PHY_Bluetooth_1M_HADM_39MHz'):
        phy = self.PHY_Bluetooth_1M_HADM(model, phy_name)
        self._set_xtal_frequency(phy, 39000000)

        return phy

    def PHY_Bluetooth_1M_HADM_40MHz(self, model, phy_name='PHY_Bluetooth_1M_HADM_40MHz'):
        phy = self.PHY_Bluetooth_1M_HADM(model, phy_name)
        self._set_xtal_frequency(phy, 40000000)

        return phy

    def PHY_Bluetooth_2M_HADM_38MHz(self, model, phy_name='PHY_Bluetooth_2M_HADM_38MHz'):
        phy = self.PHY_Bluetooth_2M_HADM(model, phy_name)
        self._set_xtal_frequency(phy, 38000000)

        return phy

    def PHY_Bluetooth_2M_HADM_38p4MHz(self, model, phy_name='PHY_Bluetooth_2M_HADM_38p4MHz'):
        phy = self.PHY_Bluetooth_2M_HADM(model, phy_name)
        self._set_xtal_frequency(phy, 38400000)

        return phy

    def PHY_Bluetooth_2M_HADM_39MHz(self, model, phy_name='PHY_Bluetooth_2M_HADM_39MHz'):
        phy = self.PHY_Bluetooth_2M_HADM(model, phy_name)
        self._set_xtal_frequency(phy, 39000000)

        return phy

    def PHY_Bluetooth_2M_HADM_40MHz(self, model, phy_name='PHY_Bluetooth_2M_HADM_40MHz'):
        phy = self.PHY_Bluetooth_2M_HADM(model, phy_name)
        self._set_xtal_frequency(phy, 40000000)

        return phy

    def PHY_Bluetooth_2M_HADM_2BT_38MHz(self, model, phy_name='PHY_Bluetooth_2M_HADM_2BT_38MHz'):
        phy = self.PHY_Bluetooth_2M_HADM_2BT(model, phy_name)
        self._set_xtal_frequency(phy, 38000000)

        return phy

    def PHY_Bluetooth_2M_HADM_2BT_38p4MHz(self, model, phy_name='PHY_Bluetooth_2M_HADM_2BT_38p4MHz'):
        phy = self.PHY_Bluetooth_2M_HADM_2BT(model, phy_name)
        self._set_xtal_frequency(phy, 38400000)

        return phy

    def PHY_Bluetooth_2M_HADM_2BT_39MHz(self, model, phy_name='PHY_Bluetooth_2M_HADM_2BT_39MHz'):
        phy = self.PHY_Bluetooth_2M_HADM_2BT(model, phy_name)
        self._set_xtal_frequency(phy, 39000000)

        return phy

    def PHY_Bluetooth_2M_HADM_2BT_40MHz(self, model, phy_name='PHY_Bluetooth_2M_HADM_2BT_40MHz'):
        phy = self.PHY_Bluetooth_2M_HADM_2BT(model, phy_name)
        self._set_xtal_frequency(phy, 40000000)

        return phy

