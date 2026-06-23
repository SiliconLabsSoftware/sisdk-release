from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
from math import ceil
from collections import OrderedDict

class CalcRadioMisc(IPCalculator):
    # table from section 10.0 in rx_iffilt_stop.docx
    # maps register enum to IFFILT bandwidth and IF frequency
    iffilt_bw = OrderedDict()
    iffilt_bw[0] = 570000
    iffilt_bw[1] = 630000
    iffilt_bw[2] = 790000
    iffilt_bw[3] = 890000
    iffilt_bw[4] = 1040000
    iffilt_bw[5] = 1140000
    iffilt_bw[6] = 1250000
    iffilt_bw[7] = 1400000
    iffilt_bw[8] = 1585000
    iffilt_bw[9] = 1660000
    iffilt_bw[10] = 1820000
    iffilt_bw[11] = 2140000
    iffilt_bw[12] = 2280000
    iffilt_bw[13] = 2600000
    iffilt_bw[14] = 2800000
    iffilt_bw[15] = 3040000

    iffilt_ratio = OrderedDict()
    iffilt_ratio[0] = 0.0
    iffilt_ratio[1] = 0.385
    iffilt_ratio[2] = 0.5
    iffilt_ratio[3] = 0.55
    iffilt_ratio[4] = 0.6
    iffilt_ratio[5] = 0.65
    iffilt_ratio[6] = 0.675
    iffilt_ratio[7] = 0.7

    def calc_bb_btc_ctrl_registers(self, model):
        # FIXME: This is a band-aid solution to get the BB BTC DAC registers set for the BTC and HDT PHYs.
        """
        BB BTC DAC registers should be turned on only for BTC and HDT PHYs.
        For all other PHYs, they should be zero.
        Eventually, they shall be controlled by FW, but for testing we need to add them here
        """

        demod_select = model.vars.demod_select.value
        if demod_select == model.vars.demod_select.var_enum.BTC or demod_select == model.vars.demod_select.var_enum.HDT:
            self._ip_reg_write(model, 'BBBTCCTRL_BBBTCENDACI', 1)
            self._ip_reg_write(model, 'BBBTCCTRL_BBBTCENDACQ', 1)
        else:
            self._ip_reg_write(model, 'BBBTCCTRL_BBBTCENDACI', 0)
            self._ip_reg_write(model, 'BBBTCCTRL_BBBTCENDACQ', 0)

    # Method name: calc_analog_misc
    # Defined in: panther\calculators\calc_radio.py
    def calc_analog_misc(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_bandsel_reg
    # Defined in: panther\calculators\calc_radio.py
    def calc_bandsel_reg(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_demen
    # Defined in: panther\calculators\calc_radio.py
    def calc_demen(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_if_center_analog_hz_actual
    # Defined in: panther\calculators\calc_radio.py
    def calc_if_center_analog_hz_actual(self, model):
        """
        given analog filter bandwidths and ration calculated actual IF \n
        center frequency for analog filters.
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        bw_analog = model.vars.iffilt_bandwidth_actual.value
        ratio = model.vars.iffilt_ratio_actual.value
        model.vars.if_center_analog_hz_actual.value = int(bw_analog * ratio)

    # Method name: calc_if_frequency_hz_value
    # Defined in: ocelot\calculators\calc_radio.py
    def calc_if_frequency_hz_value(self, model):
        # The IF frequency calculation is now in the calc_synth file for Ocelot
        pass

    # Method name: calc_iffilt_bw_actual
    # Defined in: panther\calculators\calc_radio.py
    def calc_iffilt_bw_actual(self, model):
        # The Panther calculations use the analog IF filter bandwidth calculation, even though it doesn't actually
        # exist any more on the part. It is too late to change this, so just calculate the filter bandwidth
        # as if the filter existed.
        bw_dig = model.vars.bandwidth_hz.value  # Can not use actual bandwidth here, because it depends on fxo or fdec8
        # find smallest bandwidth setting that is larger than bw_dig
        for bw_reg, bw_ana in self.iffilt_bw.items():
            if bw_ana > bw_dig:
                break
        model.vars.iffilt_bandwidth_actual.value = self.iffilt_bw[bw_reg]

    # Method name: calc_iffilt_bw_reg
    # Defined in: panther\calculators\calc_radio.py
    def calc_iffilt_bw_reg(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_iffilt_ratio_actual
    # Defined in: panther\calculators\calc_radio.py
    def calc_iffilt_ratio_actual(self, model):
        # The Panther calculations use the analog IF filter ratio calculation, even though it doesn't actually
        # exist any more on the part. It is too late to change this, so just calculate the filter ratio
        # as if the filter existed.
        bw_analog = model.vars.iffilt_bandwidth_actual.value
        f_if = float(model.vars.if_frequency_hz.value)
        ratio_target = f_if / bw_analog
        best_error = 99
        # loop over all ratios and find best closest to target ratio
        for ratio_reg, ratio in self.iffilt_ratio.items():
            error = abs(ratio - ratio_target)
            if error < best_error:
                best_error = error
                best_ratio_reg = ratio_reg
        model.vars.iffilt_ratio_actual.value = self.iffilt_ratio[best_ratio_reg]

    # Method name: calc_iffilt_ratio_reg
    # Defined in: panther\calculators\calc_radio.py
    def calc_iffilt_ratio_reg(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_iffilt_ratio_value
    # Defined in: common\calculators\calc_radio.py
    def calc_iffilt_ratio_value(self, model):
        """
        given already decided center (IF) frequency and IFFILT bandwidth
        find ratio value that would center the IFFILT around the IF frequency.
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        fc = model.vars.if_frequency_hz_actual.value
        bw_ana = model.vars.iffilt_bandwidth_actual.value
        # calculate IF (center) frequency to BW ratio
        target_ratio = float(fc) / bw_ana
        model.vars.iffilt_ratio.value = target_ratio

    # Method name: calc_lnamix_reg
    # Defined in: lpwh72000\calculators\calc_radio.py
    def calc_lnamix_reg(self, model):
        pass

    # Method name: calc_lpfbwrx
    # Defined in: ocelot\calculators\calc_radio.py
    def calc_lpfbwrx(self, model):
        pass

    # Method name: calc_lpfbwrx_reg
    # Defined in: ocelot\calculators\calc_radio.py
    def calc_lpfbwrx_reg(self, model):
        pass

    # Method name: calc_lpfbwtx
    # Defined in: ocelot\calculators\calc_radio.py
    def calc_lpfbwtx(self, model):
        pass

    # Method name: calc_lpfbwtx_reg
    # Defined in: rainier\calculators\calc_radio.py
    def calc_lpfbwtx_reg(self, model):
        pass

    # Method name: calc_realmode_reg
    # Defined in: panther\calculators\calc_radio.py
    def calc_realmode_reg(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_reg_ifadcctrl
    # Defined in: panther\calculators\calc_radio.py
    def calc_reg_ifadcctrl(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_reg_iffiltctrl
    # Defined in: panther\calculators\calc_radio.py
    def calc_reg_iffiltctrl(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_reg_ifpgactrl
    # Defined in: panther\calculators\calc_radio.py
    def calc_reg_ifpgactrl(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_reg_lnamixctrl1
    # Defined in: panther\calculators\calc_radio.py
    def calc_reg_lnamixctrl1(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_reg_lpfbwtx_lpfbwrx
    # Defined in: panther\calculators\calc_radio.py
    def calc_reg_lpfbwtx_lpfbwrx(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_reg_vcoctrl
    # Defined in: panther\calculators\calc_radio.py
    def calc_reg_vcoctrl(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_reg_vcodetamplitude
    # Defined in: ocelot\calculators\calc_radio.py
    def calc_reg_vcodetamplitude(self, model):
        pass

    # Method name: calc_txtrimdregbleed_reg
    # Defined in: bobcat\calculators\calc_radio.py
    def calc_txtrimdregbleed_reg(self, model):
        pass