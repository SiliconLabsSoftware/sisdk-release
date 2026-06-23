from pyradioconfig.calculator_model_framework.decorators.phy_decorators import do_not_inherit_phys
from pyradioconfig.parts.bobcat.phys.Phys_RAIL_Base_Standard_BLE import PHYS_Bluetooth_LE_Bobcat
from py_2_and_3_compatibility import *

@do_not_inherit_phys
class PHYS_Bluetooth_LE_Bobcat_HADM(PHYS_Bluetooth_LE_Bobcat):

    def _set_xtal_frequency(self, phy, xtal_freq=None):
        """
        HADM PHYs are defined for 40Mhz XTAL only
        """
        if xtal_freq is None:
            phy.profile_inputs.xtal_frequency_hz.value = 40000000
        else:
            phy.profile_inputs.xtal_frequency_hz.value = xtal_freq

    def PHY_Bluetooth_1M_HADM(self, model, phy_name=None):
        # https://confluence.silabs.com/display/BGHADM/Bobcat#Bobcat-PHYStrategy
        # Only valid for 40 MHz
        phy = super().PHY_Bluetooth_LE_Viterbi_noDSA_fullrate(model, phy_name=phy_name)
        model.vars.ble_feature.value_forced = model.vars.ble_feature.var_enum.HADM_1M
        self._set_xtal_frequency(phy=phy, xtal_freq=40000000)
        model.vars.adc_clock_mode.value_forced = model.vars.adc_clock_mode.var_enum.HFXOMULT

        phy.profile_inputs.target_osr.value = 5

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
        phy.profile_outputs.MODEM_AFCADJRX_AFCSCALEM.override = 0  # disable feedback to avoid updates during tracking cycle
        phy.profile_outputs.MODEM_AFCADJRX_AFCSCALEE.override = 0

        # needed for precise HADM event timing - HADM PHYs are 40 MHz only
        phy.profile_outputs.rx_sync_delay_ns.override = 24000
        phy.profile_outputs.rx_eof_delay_ns.override = 8000
        phy.profile_outputs.tx_sync_delay_ns.override = 0
        phy.profile_outputs.tx_eof_delay_ns.override = 0

        return phy

    def PHY_Bluetooth_2M_HADM(self, model, phy_name=None):
        # https://confluence.silabs.com/display/BGHADM/Bobcat#Bobcat-PHYStrategy
        # Only valid for 40 MHz
        phy = super().PHY_Bluetooth_LE_2M_Viterbi_noDSA_fullrate(model, phy_name=phy_name)
        model.vars.ble_feature.value_forced = model.vars.ble_feature.var_enum.HADM_2M
        self._set_xtal_frequency(phy=phy, xtal_freq=40000000)
        model.vars.adc_clock_mode.value_forced = model.vars.adc_clock_mode.var_enum.HFXOMULT
        phy.profile_inputs.target_osr.value = 5

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
        phy.profile_outputs.MODEM_AFCADJRX_AFCSCALEM.override = 0 # disable feedback to avoid updates during tracking cycle
        phy.profile_outputs.MODEM_AFCADJRX_AFCSCALEE.override = 0

        return phy
