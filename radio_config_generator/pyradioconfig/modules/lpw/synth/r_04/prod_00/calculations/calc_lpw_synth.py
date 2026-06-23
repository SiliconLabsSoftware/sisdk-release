from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
from py_2_and_3_compatibility import *
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
import numpy as np


class CalcLpwSynth(IPCalculator):
    fvcomin = 4450e6
    fvcomax = 5950e6
    synth_freq_min_limit = 2300000000
    synth_freq_max_limit = 2900000000

    def __init__(self, peripheral_name):
        super().__init__(peripheral_name)

    # Defined in: lpwh72000\calculators\calc_synth.py
    def calc_rx_mode_lpfgear01_reg(self, model):
        self._ip_reg_write(model, 'DSMCTRLRX_RXLOCKLPFBWGEAR0', 15)
        self._ip_reg_write(model, 'DSMCTRLRX_RXLOCKLPFBWGEAR1', 15)

    # Defined in: lpwh72000\calculators\calc_synth.py
    def calc_tx_mode_lpfgear01_reg(self, model):
        self._ip_reg_write(model, 'DSMCTRLTX_TXLOCKLPFBWGEAR0', 15)
        self._ip_reg_write(model, 'DSMCTRLTX_TXLOCKLPFBWGEAR1', 15)

    # Method name: _get_synth_min_max
    # Defined in: panther\calculators\calc_synth.py
    def _get_synth_min_max(self):
        # Panther supports a wider frequency range: https://jira.silabs.com/browse/MCUW_RADIO_CFG-710
        synth_min = (4.0e3 / 2.0) * 1000000
        synth_max = (6.5e3 / 2.0) * 1000000
        return synth_min, synth_max


    # Method name: calc_base_frequency_actual
    # Defined in: common\calculators\calc_synth.py
    def calc_base_frequency_actual(self, model):
        """
        calculate the actual base (RF) frequency
        Equation (5.34) of EFR32 Reference Manual (internal.pdf)
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        chan0_freq_reg = model.vars.SYNTH_FREQ_FREQ.value
        res = model.vars.synth_res_actual.value
        ch0_freq_hz = py2round(chan0_freq_reg * res)
        model.vars.base_frequency_actual.value = long(ch0_freq_hz)


    # Method name: calc_chan_spacing_actual
    # Defined in: common\calculators\calc_synth.py
    def calc_chan_spacing_actual(self, model):
        """
        calculate the actual channel spacing
        Equation (5.35) of EFR32 Reference Manual (internal.pdf)
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        chsp = model.vars.SYNTH_CHSP_CHSP.value
        res = model.vars.synth_res_actual.value
        ch_spacing = py2round(chsp * res)
        model.vars.channel_spacing_actual.value = int(ch_spacing)

    # Method name: calc_check_synth_limits
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_check_synth_limits(self, model):
        # Overriding limit check from Common
        # TODO: add in limits if we want to check on Ocelot
        pass

    # Method name: calc_chsp_freq_reg
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_chsp_freq_reg(self, model):
        # This function was ported due to a variable name mismatch
        ch_spacing = model.vars.channel_spacing_hz.value * 1.0
        f0 = model.vars.base_frequency_hz.value * 1.0
        res = model.vars.synth_res_actual.value
        # channel spacing in terms of res
        chsp = py2round(ch_spacing / res)
        self._ip_reg_write(model, 'CHSP_CHSP', int(chsp))
        # frequency in terms of res
        freq = math.floor(f0 / res)
        self._ip_reg_write(model, 'FREQ_FREQ', long(freq))


    # Method name: calc_dlf_ctrl
    # Defined in: lpwh72000\calculators\calc_synth.py
    def calc_dlf_ctrl(self, model):
        self._ip_reg_write(model, 'DLFCTRL_LOCKLPFBWGEARSLOT', 3)
        self._ip_reg_write(model, 'DLFCTRL_LPFBWLOADDEL', 1)
        self._ip_reg_write(model, 'HOPPING_LPFBWDURINGHOP', 15)
        self._ip_reg_write(model, 'HOPPING_LPFBWAFTERHOP', 8)
        self._ip_reg_write(model, 'HOPPING_HOPLPFBWGEARSLOT', 7)
        self._ip_reg_write(model, 'HOPPING_HOPHCAPDELAY', 3)
        self._ip_reg_write(model, 'HOPPING_HCAPRETIMESEL', 2)

    # Method name: calc_fcal_reg
    # Defined in: rainier\calculators\calc_synth.py
    def calc_fcal_reg(self, model):
        ## NUMCYCLE
        self._ip_reg_write(model, 'LOCNTCTRL_NUMCYCLE', 5)
        self._ip_reg_write(model, 'LOCNTCTRL_NUMCYCLE1', 5)
        self._ip_reg_write(model, 'LOCNTCTRL_NUMCYCLE2', 5)
        self._ip_reg_write(model, 'LOCNTCTRL_NUMCYCLE3', 4)
        self._ip_reg_write(model, 'LOCNTCTRL_NUMCYCLE4', 4)
        self._ip_reg_write(model, 'LOCNTCTRL_NUMCYCLE5', 4)
        self._ip_reg_write(model, 'FCALCTRL_NUMCYCLE6', 4)
        self._ip_reg_write(model, 'FCALCTRL_NUMCYCLE7', 4)
        self._ip_reg_write(model, 'FCALCTRL_NUMCYCLE8', 3)
        self._ip_reg_write(model, 'FCALCTRL_NUMCYCLE9', 3)
        self._ip_reg_write(model, 'FCALCTRL_NUMCYCLE10', 2)
        ## COMPANION
        self._ip_reg_write(model, 'COMPANION_COMPANION0', 1)
        self._ip_reg_write(model, 'COMPANION_COMPANION1', 1)
        self._ip_reg_write(model, 'COMPANION_COMPANION2', 2)
        self._ip_reg_write(model, 'COMPANION_COMPANION3', 2)
        self._ip_reg_write(model, 'COMPANION_COMPANION4', 2)
        self._ip_reg_write(model, 'COMPANION_COMPANION5', 4)
        self._ip_reg_write(model, 'COMPANION_COMPANION6', 4)
        self._ip_reg_write(model, 'COMPANION_COMPANION7', 5)
        ## STEPWAIT
        self._ip_reg_write(model, 'FCALCTRL_STEPWAIT', 0)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT1', 0)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT2', 0)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT3', 1)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT4', 1)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT5', 2)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT6', 2)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT7', 3)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT8', 3)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT9', 4)
        self._ip_reg_write(model, 'FCALSTEPWAIT_STEPWAIT10', 4)

    # Method name: calc_hfxo_retiming_table
    # Defined in: bobcat\calculators\calc_synth.py
    def calc_hfxo_retiming_table(self, model):
        # Inherit Ocelot retiming
        # Initialize Table
        model.vars.lut_table_index.value = [0]
        model.vars.lut_freq.value = []
        model.vars.lut_freq_upper.value = []
        model.vars.lut_valid.value = []
        model.vars.lut_smuxdiv.value = []
        model.vars.lut_limitl.value = []
        model.vars.lut_limith.value = []
        model.vars.lut_dpll_freq_hz.value = []

        # setting for 1x HFXO frequency
        self.retime_print("calculating 1x HFXO freq")
        self.retime_main(model, model.vars.xtal_frequency_hz.value, 0, 0)

        # setting for 2x HFXO frequency
        self.retime_print("calculating 2x HFXO freq")
        model.vars.lut_table_index.value.append(0)
        self.retime_main(model, model.vars.xtal_frequency_hz.value * 2, 1, model.vars.lut_table_index.value[0])

    # Method name: calc_hop_enable
    # Defined in: rainier\calculators\calc_synth.py
    def calc_hop_enable(self, model):
        # Disable by default
        model.vars.hop_enable.value = model.vars.hop_enable.var_enum.DISABLED

    # Method name: calc_if_frequency_actual
    # Defined in: jumbo\calculators\calc_synth.py
    def calc_if_frequency_actual(self, model):
        """calculate the actual IF frequency (IF frequency)
        Equation (5.14) of EFR32 Reference Manual (internal.pdf)
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        iffreq = model.vars.SYNTH_IFFREQ_IFFREQ.value
        res = model.vars.synth_res_actual.value
        model.vars.if_frequency_hz_actual.value = int(iffreq * res)

    # Method name: calc_if_frequency_target
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_if_frequency_target(self, model):
        # This function calculates the target IF frequency
        # The lower bound for signal content is determined by the lowest usable frequency range of the ADC (DC filtering produces noise near DC, varies based on sample rate)
        # This upper bound for signal content is determined by the highest usable frequency range of the ADC (noise shaping, varies based on sample rate)
        # Load model variables into local variables
        bandwidth_hz = model.vars.bandwidth_hz.value
        adc_rate_mode = model.vars.adc_rate_mode.value  # We can't use the actual rate mode, because the IF goes into calculating the actual VCO, which goes into final ADC divider
        if adc_rate_mode == model.vars.adc_rate_mode.var_enum.EIGHTHRATE:
            bandwidth_adc_hz = 150e3
            band_edge_min = 50e3
        elif adc_rate_mode == model.vars.adc_rate_mode.var_enum.HALFRATE:
            bandwidth_adc_hz = 1.25e6
            band_edge_min = 50e3
        else:
            bandwidth_adc_hz = 2.50e6
            band_edge_min = 100e3
        if_frequency_min = 80e3
        if_frequency_hz = max(if_frequency_min, band_edge_min + bandwidth_hz / 2)
        if ((if_frequency_hz + bandwidth_hz / 2) > bandwidth_adc_hz):
            LogMgr.Warning("WARNING: IF + BW/2 > ADC Bandwidth")
        # Load local variables back into model variables
        model.vars.if_frequency_hz.value = int(if_frequency_hz)

    # Method name: calc_iffreq_reg
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_iffreq_reg(self, model):
        # This calculation writes the IF frequency to the register
        # Load model variables into local variables
        if_frequency_hz = model.vars.if_frequency_hz.value
        synth_res_actual = model.vars.synth_res_actual.value
        iffreq_reg = int(if_frequency_hz / synth_res_actual)
        # Load local variables back into model variables
        self._ip_reg_write(model, 'IFFREQ_IFFREQ', iffreq_reg)

    # Method name: calc_lms_reg
    # Defined in: rainier\calculators\calc_synth.py
    def calc_lms_reg(self, model):
        self._ip_reg_write(model, 'GLMS_GLMSENABLEDELAY', 7)
        self._ip_reg_write(model, 'GLMS_GLMSGEAR0', 4)
        self._ip_reg_write(model, 'GLMS_GLMSGEAR1', 4)
        self._ip_reg_write(model, 'GLMS_GLMSGEAR2', 4)
        self._ip_reg_write(model, 'GLMS_GLMSGEAR3', 4)
        self._ip_reg_write(model, 'GLMS_GLMSGEAR4', 4)
        self._ip_reg_write(model, 'GLMS_GLMSGEARSLOT', 0)
        self._ip_reg_write(model, 'PLMS_PLMSENABLEDELAY', 7)
        self._ip_reg_write(model, 'PLMS_PLMSGEAR0', 11)
        self._ip_reg_write(model, 'PLMS_PLMSGEAR1', 10)
        self._ip_reg_write(model, 'PLMS_PLMSGEAR2', 9)
        self._ip_reg_write(model, 'PLMS_PLMSGEAR3', 8)
        self._ip_reg_write(model, 'PLMS_PLMSGEAR4', 6)
        self._ip_reg_write(model, 'PLMS_PLMSGEARSLOT', 0)

    # Method name: calc_lo_adc_dividers
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_lo_adc_dividers(self, model):
        # TODO: check if DIVCTRL_LODIVFREQCTRL is still used, also do we need to calculate adcvcodiv this way anymore?
        # This function calculates A,B,C, ADC dividers
        # Load model variables into local variables
        adc_clock_mode = model.vars.adc_clock_mode_actual.value
        flo = model.vars.lo_target_freq.value  # We don't know the LO frequency yet, this is based on the center freq and target IF
        fadc_target = model.vars.adc_target_freq.value  # We don't know the ADC frequency yet
        # Define VCO pull range constants
        # fvcomin = 4450e6
        # fvcomax = 5950e6
        # These array variables store all valid divider sets
        # lodiv_codes[div-1] is the combined divider code for divider A, B, C
        #    div_m_1  [0,1,2,3,4,5,6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        lodiv_codes = [1, 2, 3, 4, 5, 6, 7, 20, 27, 21, 0, 22, 0, 23, 29, 36, 0, 30, 0, 37, 31, 0, 0, 38]
        fosc = []
        lodiv = []
        # Loop through all C,B,A divider possibilities
        for div_m_1 in range(24):
            fvco = flo * (2 * (div_m_1 + 1))
            if (lodiv_codes[div_m_1] > 0) and (fvco < self.fvcomax) and (fvco > self.fvcomin):
                # If this is a valid value for the VCO, add to the list of valid divider combinations
                lodiv.append(div_m_1 + 1)
                fosc.append(fvco)
        # Now go through all of the possible solutions and pick the best one
        if (len(fosc) == 0):
            raise CalculationException('ERROR: no valid solution for VCO frequency in calc_lo_adc_dividers()')
        else:
            # If the ADC is based directly on the HFXO, then don't worry about the ADC divider and pick the first valid LO divider set
            if (adc_clock_mode == model.vars.adc_clock_mode.var_enum.HFXOMULT):
                adcdivfinal = 0  # This is a don't care, but make it 1 so that any calculations using the value don't divide by zero
                lodivfinal = lodiv[0]
            else:
                # Find target freq for ADC from potential candidates
                # Start with some initial values
                fadcerr = 1e20
                adcdivfinal = 1
                lodivfinal = 1
                for index in range(0, len(fosc)):
                    adcdiv = int(round(fosc[index] / 2.0 / fadc_target))
                    fadc = fosc[index] / (2 * adcdiv)
                    error = abs(fadc - fadc_target)
                    if (error < fadcerr):
                        # If the current divider set yields the lowest ADC error, then make that the final for now
                        fadcerr = error
                        adcdivfinal = adcdiv
                        lodivfinal = lodiv[index]
        # Calculate the A,B,C dividers from lodiv_reg and its 3 fields
        lodiv_reg = lodiv_codes[lodivfinal - 1]
        # Load local variables back into model variables
        # model.vars.adc_vco_div.value = adcdivfinal
        model.vars.lodiv.value = lodivfinal
        # Write register
        self._ip_reg_write(model, 'DIVCTRL_LODIVFREQCTRL', lodiv_reg)
        # calculate proper variable flag to determine sub-GHz
        model.vars.subgig_band.value = bool(model.vars.lodiv_actual.value > 1)

    # Method name: calc_lo_side_regs
    # Defined in: lpwh72000\calculators\calc_synth.py
    def calc_lo_side_synth_regs(self, model):
        # Separate implentation between Panther and Ocelot to differentiate SubG and 2.4G implementation of low-side
        model.vars.lo_injection_side.value = model.vars.lo_injection_side.var_enum.HIGH_SIDE  # default to high-side
        lo_injection_side = model.vars.lo_injection_side.value
        if lo_injection_side == model.vars.lo_injection_side.var_enum.HIGH_SIDE:
            loside = 1
        else:
            loside = 0
        # Write the registers
        self._ip_reg_write(model, 'IFFREQ_LOSIDE', loside)

    # Method name: calc_lo_target_freq
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_lo_target_freq(self, model):
        # This function calculates the target LO frequency baed on RF, IF, and injection side
        # Load model variables into local variables
        lo_injection_side = model.vars.lo_injection_side.value
        rf_freq = model.vars.base_frequency_hz.value
        if_freq = model.vars.if_frequency_hz.value  # We don't yet know the actual synth frequency to get the true IF
        if lo_injection_side == model.vars.lo_injection_side.var_enum.HIGH_SIDE:
            lo_freq = rf_freq + if_freq
        else:
            lo_freq = rf_freq - if_freq
        # Load local variables back into model variables
        model.vars.lo_target_freq.value = lo_freq

    # Method name: calc_lodividers_actual
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_lodividers_actual(self, model):
        lodiv_reg = model.vars.SYNTH_DIVCTRL_LODIVFREQCTRL.value
        a_divider = 7 & lodiv_reg
        b_divider = 7 & (lodiv_reg >> 3)
        if b_divider == 0:
            b_divider = 1
        c_divider = 7 & (lodiv_reg >> 6)
        if c_divider == 0:
            c_divider = 1
        model.vars.a_divider_actual.value = a_divider
        model.vars.b_divider_actual.value = b_divider
        model.vars.c_divider_actual.value = c_divider
        model.vars.lodiv_actual.value = a_divider * b_divider * c_divider

    # Method name: calc_pulsepairing_reg
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_pulsepairing_reg(self, model):
        fsynth = model.vars.rx_synth_freq_actual.value  # fsynth =  fvco / 2
        fif = model.vars.if_frequency_hz_actual.value
        lo_injection_side = model.vars.lo_injection_side.value
        lodiv = model.vars.lodiv_actual.value
        if lo_injection_side == model.vars.lo_injection_side.var_enum.LOW_SIDE:
            fif = - fif
        model.vars.ppnd_0.value = 0
        model.vars.ppnd_1.value = 0
        model.vars.ppnd_2.value = 0
        model.vars.ppnd_3.value = 0
        if (lodiv >= 5):
            # only allow DCDC retiming for low frequency band
            # calculate 4 freqs equaly spaced over synth range
            # divide by 2 is to convert vco range to synth range
            fvcorange = self.fvcomax - self.fvcomin
            fvcostep = fvcorange / 4.0
            fsynth_list = np.arange(self.fvcomin + fvcostep / 2, self.fvcomax - fvcostep / 4, fvcostep) / 2
            model.vars.ppnd_0.value = self.return_ppnd(fsynth_list[0], fif, lodiv)
            model.vars.ppnd_1.value = self.return_ppnd(fsynth_list[1], fif, lodiv)
            model.vars.ppnd_2.value = self.return_ppnd(fsynth_list[2], fif, lodiv)
            model.vars.ppnd_3.value = self.return_ppnd(fsynth_list[3], fif, lodiv)

    # Method name: calc_reg_ditherdsmoutput
    # Defined in: panther\calculators\calc_synth.py
    def calc_reg_ditherdsmoutput(self, model):
        # Removed because these registers no longer appear in the Profile Outputs
        pass

    # Method name: calc_rf_band
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_rf_band(self, model):
        ### revised to include BAND_315
        rf_freq = model.vars.base_frequency_hz.value
        if (rf_freq > 2.0e9):
            model.vars.rf_band.value = model.vars.rf_band.var_enum.BAND_2400
        elif (rf_freq > 1.2e9):
            model.vars.rf_band.value = model.vars.rf_band.var_enum.BAND_1432
        elif (rf_freq > 885e6):
            model.vars.rf_band.value = model.vars.rf_band.var_enum.BAND_915
        elif (rf_freq > 700e6):
            model.vars.rf_band.value = model.vars.rf_band.var_enum.BAND_868
        elif (rf_freq > 455e6):
            model.vars.rf_band.value = model.vars.rf_band.var_enum.BAND_490
        elif (rf_freq > 400e6):
            model.vars.rf_band.value = model.vars.rf_band.var_enum.BAND_434
        elif (rf_freq > 300e6):
            model.vars.rf_band.value = model.vars.rf_band.var_enum.BAND_315
        else:
            model.vars.rf_band.value = model.vars.rf_band.var_enum.BAND_169

    # Method name: calc_rx_mode
    # Defined in: rainier\calculators\calc_synth.py
    def calc_synth_rx_mode(self, model):
        synth_settling_mode = model.vars.synth_settling_mode.value
        if synth_settling_mode == model.vars.synth_settling_mode.var_enum.FAST:
            model.vars.synth_rx_mode.value = model.vars.synth_rx_mode.var_enum.MODE_HOP
        elif synth_settling_mode == model.vars.synth_settling_mode.var_enum.BLE_LR:
            model.vars.synth_rx_mode.value = model.vars.synth_rx_mode.var_enum.MODE1
        else:
            model.vars.synth_rx_mode.value = model.vars.synth_rx_mode.var_enum.MODE2

    # Method name: calc_rx_mode_reg
    # Defined in: rainier\calculators\calc_synth.py
    def calc_rx_mode_reg(self, model):
        rx_mode = model.vars.synth_rx_mode.value
        ind = rx_mode.value
        # Synth settings https://jira.silabs.com/browse/MCUW_RADIO_CFG-1529
        # Settings copied over from Lynx Assert
        # {workspace}\shared_files\lynx\radio_validation\ASSERTS
        # BLK_SYNTH_RX_LP_BW_200KHZ.csv (BLE_LR mode)
        # BLK_SYNTH_RX_LP_BW_250KHZ.csv (NORMAL mode)
        rx_mode_settings = {
            'SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR2': [15, 15, 15],
            'SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR3': [11, 11, 12],
            'SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR4': [11, 11, 12],
            'SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR5': [11, 11, 12],
            'SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR6': [7, 7, 10],
            'SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR7': [7, 7, 10],
            'SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR8': [7, 7, 10],
            'SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR9': [6, 6, 8],
            'SYNTH.DSMCTRLRX.LSBFORCERX': [1, 1, 1],
            'SYNTH.DSMCTRLRX.DEMMODERX': [1, 1, 1],
            'SYNTH.DSMCTRLRX.QNCMODERX': [0, 0, 1],
            'SYNTH.DSMCTRLRX.GLMSOVERRIDEVALRX': [840, 840, 840],
            # 'RAC.SYMMDCTRL.SYMMDMODERX': [4, 4],
            # 'RAC.SYTRIM1.SYLODIVLDOTRIMNDIORX': [1, 1],
        }
        self._ip_reg_write(model, 'DLFCTRLRX_RXLOCKLPFBWGEAR2',
                        rx_mode_settings['SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR2'][ind])
        self._ip_reg_write(model, 'DLFCTRLRX_RXLOCKLPFBWGEAR3',
                        rx_mode_settings['SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR3'][ind])
        self._ip_reg_write(model, 'DLFCTRLRX_RXLOCKLPFBWGEAR4',
                        rx_mode_settings['SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR4'][ind])
        self._ip_reg_write(model, 'DLFCTRLRX_RXLOCKLPFBWGEAR5',
                        rx_mode_settings['SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR5'][ind])
        self._ip_reg_write(model, 'DLFCTRLRX_RXLOCKLPFBWGEAR6',
                        rx_mode_settings['SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR6'][ind])
        self._ip_reg_write(model, 'DLFCTRLRX_RXLOCKLPFBWGEAR7',
                        rx_mode_settings['SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR7'][ind])
        self._ip_reg_write(model, 'DLFCTRLRX_RXLOCKLPFBWGEAR8',
                        rx_mode_settings['SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR8'][ind])
        self._ip_reg_write(model, 'DLFCTRLRX_RXLOCKLPFBWGEAR9',
                        rx_mode_settings['SYNTH.DLFCTRLRX.RXLOCKLPFBWGEAR9'][ind])
        self._ip_reg_write(model, 'DSMCTRLRX_QNCMODERX',
                        rx_mode_settings['SYNTH.DSMCTRLRX.QNCMODERX'][ind])
        self._ip_reg_write(model, 'DSMCTRLRX_GLMSOVERRIDEVALRX',
                        rx_mode_settings['SYNTH.DSMCTRLRX.GLMSOVERRIDEVALRX'][ind])
        # : Following registers are PTE Set & Forget but needs to be set by RC since they are different from reset value
        # : See https://jira.silabs.com/browse/MCUW_RADIO_CFG-1610
        self._ip_reg_write(model, 'DSMCTRLRX_LSBFORCERX', rx_mode_settings['SYNTH.DSMCTRLRX.LSBFORCERX'][ind])
        self._ip_reg_write(model, 'DSMCTRLRX_DEMMODERX', rx_mode_settings['SYNTH.DSMCTRLRX.DEMMODERX'][ind])

    # Method name: calc_rx_synth_freq_actual
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_rx_synth_freq_actual(self, model):
        """
        calculate synthesizer frequency for RX
        Equation (5.31) of EFR32 Reference Manual (internal.pdf)
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        chan0_freq = model.vars.SYNTH_FREQ_FREQ.value
        chno = 0
        chan_spacing = model.vars.SYNTH_CHSP_CHSP.value
        cal_offset = 0
        if_freq = model.vars.SYNTH_IFFREQ_IFFREQ.value
        loside = model.vars.SYNTH_IFFREQ_LOSIDE.value
        res = model.vars.synth_res_actual.value
        lodiv = model.vars.lodiv_actual.value
        if loside:
            rx_synth_freq = (chan0_freq + chno * chan_spacing + cal_offset + if_freq) * res * lodiv
        else:
            rx_synth_freq = (chan0_freq + chno * chan_spacing + cal_offset - if_freq) * res * lodiv
        model.vars.rx_synth_freq_actual.value = long(round(rx_synth_freq))

    # Method name: calc_s3_reg
    # Defined in: rainier\calculators\calc_synth.py
    def calc_s3_reg(self, model):
        denominit0 = 63
        denominit1 = 64
        self._ip_reg_write(model, 'MMDDENOMINIT_DENOMINIT0', denominit0)
        self._ip_reg_write(model, 'MMDDENOMINIT_DENOMINIT1', denominit1)
        self._ip_reg_write(model, 'QNCCTRL_ENABLEDQNCTIME', 5)


    # Method name: calc_synth_res_actual
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_synth_res_actual(self, model):
        # This function was ported due to a variable name mismatch
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value * 1.0
        lodiv = model.vars.lodiv_actual.value
        # Calculate frequency resolution
        # Correct reference clock to use here is the xtal
        res = xtal_frequency_hz / lodiv / pow(2, 19)
        model.vars.synth_res_actual.value = res

    # Method name: calc_synth_settling_mode
    # Defined in: rainier\calculators\calc_synth.py
    def calc_synth_settling_mode(self, model):
        hop_enable = model.vars.hop_enable.value  # Disable by default
        if hop_enable == model.vars.hop_enable.var_enum.ENABLED:
            model.vars.synth_settling_mode.value = model.vars.synth_settling_mode.var_enum.FAST
        else:  # FastSw Disabled
            model.vars.synth_settling_mode.value = model.vars.synth_settling_mode.var_enum.NORMAL

    # Method name: calc_tuning_range_limits
    # Defined in: common\calculators\calc_synth.py
    def calc_tuning_range_limits(self, model):
        model.vars.tuning_limit_min.value = long(self.synth_freq_min_limit / model.vars.lodiv_actual.value)
        model.vars.tuning_limit_max.value = long(self.synth_freq_max_limit / model.vars.lodiv_actual.value)

    # Method name: calc_tx_mode
    # Defined in: lpwh72000\calculators\calc_synth.py
    def calc_synth_tx_mode(self, model):
        modulator_select = model.vars.modulator_select.value
        baudrate = model.vars.baudrate.value
        modulation_index = model.vars.modulation_index.value

        if modulator_select == model.vars.modulator_select.var_enum.IQ_MOD_DIRECT:
            model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE1  # 750KHz,one side
        elif modulator_select == model.vars.modulator_select.var_enum.IQ_MOD:
            model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE1  # 750KHz,one side
        # Set FSK and OQPSK settings based on baudrate
        else:
            if baudrate > 1500e3 and modulation_index > 0.5:
                # to fix eye diagram for 2mbps1Mhz datasheet PHY - https://jira.silabs.com/browse/MCUW_RADIO_CFG-2548
                model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE4  # 2.5MHz, one side
            elif baudrate > 1000e3:
                model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE3  # 1.5MHz, one side
            elif baudrate > 500e3:
                model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE2  # 1 MHz, one side
            else:
                model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE1  # 750KHz, one side

    # Method name: calc_tx_mode_reg
    # Defined in: rainier\calculators\calc_synth.py
    def calc_tx_mode_reg(self, model):
        ind = model.vars.synth_tx_mode.value
        # Synth settings coming from
        # file://silabs.com/design/projects/ip_em_22nm/tsmc22ull/modules/blesy_all/docs/specs/blesy_all.pdf
        # 750KHz one side (MODE 1), to be used for IQMOD and BLE1M PHY inband requirements
        # 1MHz one side (MODE 2)
        # 1.5MHz one side (MODE 3)
        # 2.5MHz one side (MODE 4)
        # 2 MHz one side (MODE 5), to be used for BLE2M PHY due to inband requirements
        tx_mode_settings = {
            'SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR2': [15, 15, 15, 15, 15],
            'SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR3': [12, 12, 14, 14, 14],
            'SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR4': [12, 12, 14, 14, 14],
            'SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR5': [12, 12, 14, 14, 14],
            'SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR6': [10, 10, 13, 13, 13],
            'SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR7': [10, 10, 13, 13, 13],
            'SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR8': [10, 10, 13, 13, 13],
            'SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR9': [9, 10, 11, 13, 12],
            'SYNTH.DLFCTRL.LOCKLPFBWGEARSLOT': [1, 1, 1, 1, 1],
            'SYNTH.DLFCTRL.LPFBWLOADDEL': [1, 1, 1, 1, 1],
            'SYNTH.DSMCTRLTX.LSBFORCETX': [1, 1, 1, 1, 1],
            'SYNTH.DSMCTRLTX.DEMMODETX': [1, 1, 1, 1, 1],
            #   'RAC_SYCTRL1_SYLODIVSELFP4G82G4TX': [1, 0, 0, 0],   #fp select, depend on TX power, move to rail code
            #   'RAC_SYMMDCTRL_SYMMDSEL56STGTX': [1, 0, 0, 0],   #TX IQMOD select 6 stage
        }
        self._ip_reg_write(model, 'DLFCTRLTX_TXLOCKLPFBWGEAR2',
                        tx_mode_settings['SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR2'][ind])
        self._ip_reg_write(model, 'DLFCTRLTX_TXLOCKLPFBWGEAR3',
                        tx_mode_settings['SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR3'][ind])
        self._ip_reg_write(model, 'DLFCTRLTX_TXLOCKLPFBWGEAR4',
                        tx_mode_settings['SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR4'][ind])
        self._ip_reg_write(model, 'DLFCTRLTX_TXLOCKLPFBWGEAR5',
                        tx_mode_settings['SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR5'][ind])
        self._ip_reg_write(model, 'DLFCTRLTX_TXLOCKLPFBWGEAR6',
                        tx_mode_settings['SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR6'][ind])
        self._ip_reg_write(model, 'DLFCTRLTX_TXLOCKLPFBWGEAR7',
                        tx_mode_settings['SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR7'][ind])
        self._ip_reg_write(model, 'DLFCTRLTX_TXLOCKLPFBWGEAR8',
                        tx_mode_settings['SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR8'][ind])
        self._ip_reg_write(model, 'DLFCTRLTX_TXLOCKLPFBWGEAR9',
                        tx_mode_settings['SYNTH.DLFCTRLTX.TXLOCKLPFBWGEAR9'][ind])
        # : Following registers are PTE Set & Forget but needs to be set by RC since they are different from reset value
        # : See https://jira.silabs.com/browse/MCUW_RADIO_CFG-1610
        self._ip_reg_write(model, 'DSMCTRLTX_LSBFORCETX', tx_mode_settings['SYNTH.DSMCTRLTX.LSBFORCETX'][ind])
        self._ip_reg_write(model, 'DSMCTRLTX_DEMMODETX', tx_mode_settings['SYNTH.DSMCTRLTX.DEMMODETX'][ind])

    # Method name: calc_tx_synth_freq_actual
    # Defined in: panther\calculators\calc_synth.py
    def calc_tx_synth_freq_actual(self, model):
        # Overriding this method as SYNTH_CHCTRL_CHNO and SYNTH_CALOFFSET_CALOFFSET no longer exist in the Profile Outputs
        chan0_freq = model.vars.SYNTH_FREQ_FREQ.value
        chno = 0
        chan_spacing = model.vars.SYNTH_CHSP_CHSP.value
        cal_offset = 0
        res = model.vars.synth_res_actual.value
        lodiv = model.vars.lodiv_actual.value
        tx_synth_freq = (1.0 * chan0_freq + chno * chan_spacing + cal_offset) * res * lodiv
        model.vars.tx_synth_freq_actual.value = int(tx_synth_freq)

    # Method name: calc_txramp_txmodephaseflip_reg
    # Defined in: bobcat\calculators\calc_synth.py
    def calc_txramp_txmodephaseflip_reg(self, model):
        pass

    # Method name: retime_calc_catchup_duration
    # Defined in: lynx\calculators\calc_synth.py
    def retime_calc_catchup_duration(self, sysclk_freq, freq, smuxdiv, num_clks):
        float_freq = (float)(freq / 1.0)
        min_sys_period = (float)(num_clks * (smuxdiv / float_freq))
        lag_time = (float)(smuxdiv / float_freq) * NUM_LAG_CATCHUP_CLKS
        delta = (float)((1.0 / sysclk_freq) - min_sys_period)
        self.retime_print("lag_time: %f, delta: %f" % (lag_time, delta))
        if (delta == 0):
            delta = (2.2250738585072014e-308)
        catchup_clocks = (float)(lag_time / delta)  # should probably round up..oh well
        catchup_duration = catchup_clocks * min_sys_period
        return (catchup_duration)

    # Method name: retime_calc_min_synth_freq
    # Defined in: lynx\calculators\calc_synth.py
    def retime_calc_min_synth_freq(self, sysclk_freq, smuxdiv, num_clks):
        global NUM_LAG_CATCHUP_CLKS
        global MAX_CATCHUP_DURATION
        NUM_LAG_CATCHUP_CLKS = 4.0  # max number of smart mux clock periods to catch up
        MAX_CATCHUP_DURATION = 10.0  # us
        # Dur = CATCHUP_DURATION =catchup_period * (Time_Lag / delta_period)
        # lag_time = NUM_LAG_CATCHUP_CLKS * lo_period;
        # L = NUM_LAG_CATCHUP_CLKS  = 4 ....this is approximately 4 lo clocks of delay that we need to catch up
        # cp = catchup_period = (smuxdiv  * num_clks) / freq
        # delta_period = sysclk_period - catchup_period;  ....the incremental time that we catch up per clock
        # Dur = cp * lagtime / delta
        # Dur = cp * (cp * L/N) / (sp - cp)
        # Dur = (L/N)*cp^2 / (sp - cp)
        # (L/N)*cp^2 + Dur * cp - Dur * sp = 0
        # cp = (-Dur +/- sqrt(Dur^2 + (4 * L * Dur * sp / N ) )/ (2 * (L/N) )
        # 1/cp = cf = (2 * (L/N) )  /    (-Dur +/- sqrt(Dur^2 + (4 * L * Dur * sp / N) )
        # freq = cf * (smuxdiv * N)
        # freq = (2 * smuxdiv * L )  / (-Dur +/- sqrt(Dur^2 + (4 * L * Dur * sp / N) )
        # =(2*L*smux)/((-1*Dur)+SQRT((Dur)^2 + 4*L*Dur*sp/num_clks))
        tmp = (float)(4.0 * NUM_LAG_CATCHUP_CLKS * MAX_CATCHUP_DURATION / sysclk_freq)
        tmp1 = (float)(num_clks)
        tmp = (float)(tmp / tmp1)
        tmp = math.sqrt((MAX_CATCHUP_DURATION * MAX_CATCHUP_DURATION) + tmp)
        tmp = ((-1.0 * MAX_CATCHUP_DURATION) + tmp)
        freq = ((2.0 * smuxdiv * NUM_LAG_CATCHUP_CLKS) / tmp)
        return (freq)

    # Method name: retime_calc_smuxdiv
    # Defined in: lynx\calculators\calc_synth.py
    def retime_calc_smuxdiv(self, freq):
        global SMUX_MAX_FREQ
        SMUX_MAX_FREQ = 625  # Define the maximum frequency in MHz that the smart mux can run
        # Calculate LO frequency divider
        if (freq <= SMUX_MAX_FREQ):
            # less than 625 MHz
            smuxdiv = 1
        elif (freq <= (2 * SMUX_MAX_FREQ)):
            # less than 1250 MHz
            smuxdiv = 2
        else:
            smuxdiv = 4
        return (smuxdiv)

    # Method name: retime_check_table
    # Defined in: lynx\calculators\calc_synth.py
    def retime_check_table(self, count, sysclk_freq, synth_low_freq, synth_high_freq, valid_freq, model,
                           table_idx_start):
        # /Make sure table is properly built
        start_checking = 0
        valid = 1
        sticky_valid = 1
        if (valid_freq <= sysclk_freq):
            self.retime_print(
                "ERROR: valid frequency %6.1f is less than system frequency %6.1f" % (valid_freq, sysclk_freq))
            return 0
        if (not count):
            self.retime_print("invalid: no table generated")
            return 0
        if (model.vars.lut_freq.value[table_idx_start] > synth_low_freq):
            sticky_valid = 0
            self.retime_print("ERROR : first entry frequency > lower limit %6.1f %6.1f" % (
                model.vars.lut_freq.value[table_idx_start], synth_low_freq))
            return 0
        if (model.vars.lut_freq_upper.value[table_idx_start + count - 1] < synth_high_freq):
            sticky_valid = 0
            self.retime_print("ERROR : last entry frequency < upper limit %6.1f %6.1f" % (
                model.vars.lut_freq_upper.value[table_idx_start + count - 1], synth_high_freq))
            return 0
        # Check each entry
        for k in range(count):
            valid = 1
            # Checks against previous entries
            num_clks = model.vars.lut_limitl.value[table_idx_start + k] + model.vars.lut_limith.value[
                table_idx_start + k]
            # print("k: %d" % (k))
            if ((k > 0) and (start_checking == 1)):
                # Check LimitL vs LimitH
                if (model.vars.lut_limitl.value[table_idx_start + k] < model.vars.lut_limith.value[
                    table_idx_start + k]):
                    valid = 0
                    self.retime_print("ERROR: LimitL: {} is less than LimitH: {}".format(
                        model.vars.lut_limitl.value[table_idx_start + k],
                        model.vars.lut_limith.value[table_idx_start + k]))
                if model.vars.lut_limitl.value[table_idx_start + k] > 7:
                    valid = 0
                    self.retime_print("Warning: LimitL: {}, LimitH: {}  is bigger than range".format(
                        model.vars.lut_limitl.value[table_idx_start + k],
                        model.vars.lut_limith.value[table_idx_start + k]))
                # Check frequency sorted
                if (model.vars.lut_freq.value[table_idx_start + k] <= model.vars.lut_freq.value[
                    table_idx_start + k - 1]):
                    valid = 0
                    self.retime_print("ERROR: Frequency not sorted: {}".format(table_idx_start + k))
                # Check that there is no consecutive invalids (except for first invalid)
                if ((not model.vars.lut_valid.value[table_idx_start + k]) and (
                        not model.vars.lut_valid.value[table_idx_start + k - 1])):
                    valid = 0
                    self.retime_print("ERROR: Consecutive invalids: {}".format(table_idx_start + k))
                # Check that range is continuous across all entries
                if (model.vars.lut_freq.value[table_idx_start + k] != model.vars.lut_freq_upper.value[
                    table_idx_start + k - 1]):
                    valid = 0
                    self.retime_print("ERROR: Range not contiguous: {}".format(table_idx_start + k))
                # Check entry frequency is increasing in the table
                if (model.vars.lut_freq.value[table_idx_start + k] <= model.vars.lut_freq.value[
                    table_idx_start + k - 1]):
                    valid = 0
                    self.retime_print("ERROR: Not increasing in frequency: %f %f" % (
                        model.vars.lut_freq.value[table_idx_start + k],
                        model.vars.lut_freq.value[table_idx_start + k - 1]))
                # Check entry number of clocks (limitl+limith) is incrementing in the table
                if (model.vars.lut_smuxdiv.value[table_idx_start + k] == prev_smuxdiv):
                    #                    print("prev_smuxdiv: %d" % (prev_smuxdiv))
                    if (num_clks != (prev_num_clks + 1)):
                        valid = 0
                        self.retime_print("ERROR: Num_clks not incrementing: %d %d" % (num_clks, prev_num_clks + 1))
            # Check num_clks increments between multiples
            if (model.vars.lut_valid.value[table_idx_start + k]):
                start_checking = 1
                prev_num_clks = num_clks
                prev_smuxdiv = model.vars.lut_smuxdiv.value[table_idx_start + k]
                #                print("k: %d, prev_smuxdiv: %d" % (k, prev_smuxdiv))
                if (model.vars.lut_freq_upper.value[table_idx_start + k] / num_clks / model.vars.lut_smuxdiv.value[
                    table_idx_start + k] > valid_freq):
                    valid = 0
                    self.retime_print("ERROR: exceed max frequency %6.1f %6.1f: lut_freq[k]/num_clks" %
                                      (model.vars.lut_freq_upper.value[table_idx_start + k] / num_clks /
                                       model.vars.lut_smuxdiv.value[table_idx_start + k],
                                       valid_freq))
                catchup_duration = self.retime_calc_catchup_duration(sysclk_freq,
                                                                     model.vars.lut_freq.value[table_idx_start + k],
                                                                     model.vars.lut_smuxdiv.value[table_idx_start + k],
                                                                     model.vars.lut_limitl.value[table_idx_start + k] +
                                                                     model.vars.lut_limith.value[table_idx_start + k])
                if ((catchup_duration > MAX_CATCHUP_DURATION * 1.001) or (catchup_duration < 0)):
                    valid = 0
                    self.retime_print("ERROR: Catchup time failure: %6.1f exceeds %6.1f" %
                                      (catchup_duration, MAX_CATCHUP_DURATION))
        return sticky_valid

    # Method name: retime_main
    # Defined in: lynx\calculators\calc_synth.py
    def retime_main(self, model, dpll_frequency_hz, table_idx, start_table_idx):
        sysclk_freq = dpll_frequency_hz / 1000000
        lo_low_freq = math.floor(self.fvcomin / 2 / model.vars.lodiv_actual.value / 1000000)
        lo_high_freq = math.ceil(self.fvcomax / 2 / model.vars.lodiv_actual.value / 1000000)
        self.retime_print(
            "sysclk_freq: %f, lo_low_freq: %f, lo_high_freq: %f" % (sysclk_freq, lo_low_freq, lo_high_freq))
        model.vars.lut_dpll_freq_hz.value.append(int(sysclk_freq * 1000000))
        if (sysclk_freq <= 40):
            # Max frequency in MHz @ 1.0V
            valid_freq = 46.0
        else:
            valid_freq = 89.4  # Max frequency in MHz @ 1.1V
        # Get starting multiple
        smuxdiv = self.retime_calc_smuxdiv(lo_low_freq)
        multiple = math.floor(lo_low_freq / smuxdiv / valid_freq)
        multiple = multiple * smuxdiv
        # Generate Table
        while ((valid_freq * multiple) < lo_high_freq):
            (multiple) = self.return_retime_gen_entry(sysclk_freq, valid_freq, multiple, model, table_idx,
                                                      start_table_idx)
        status = self.retime_check_table(model.vars.lut_table_index.value[table_idx], sysclk_freq, lo_low_freq,
                                         lo_high_freq,
                                         valid_freq, model, start_table_idx)
        if (not status):
            self.retime_print("!!!! ERRORs Found !!!!!! in calc_hfxo_retiming_table")
        self.retime_print(
            "Sysclk Freq = %4.1f. Internal Max Freq = %4.1f, Lower Synth Limit= %6.1f, Upper Synth Limit = %6.1f, Table count = %d" % (
                model.vars.lut_dpll_freq_hz.value[table_idx] / 1000000.0, valid_freq, lo_low_freq, lo_high_freq,
                model.vars.lut_table_index.value[table_idx]))
        self.retime_print("Entry Synth Range  Valid SMUXDIV LIMITL LIMITH sysclk range Catchup(us)")
        for i in range(model.vars.lut_table_index.value[table_idx]):
            if (model.vars.lut_valid.value[start_table_idx + i]):
                min_freq = model.vars.lut_freq.value[start_table_idx + i] / (
                        (model.vars.lut_limitl.value[start_table_idx + i] + model.vars.lut_limith.value[
                            start_table_idx + i]) * 1.0) / \
                           model.vars.lut_smuxdiv.value[start_table_idx + i]
                max_freq = model.vars.lut_freq_upper.value[start_table_idx + i] / (
                        (model.vars.lut_limitl.value[start_table_idx + i] + model.vars.lut_limith.value[
                            start_table_idx + i]) * 1.0) / \
                           model.vars.lut_smuxdiv.value[start_table_idx + i]
            else:
                max_freq = 0
                min_freq = 0
            self.retime_print("%5d %6.1f %6.1f %5d %6d %6d %6d %6.1f %6.1f %7.3f" %
                              (start_table_idx + i, model.vars.lut_freq.value[start_table_idx + i],
                               model.vars.lut_freq_upper.value[start_table_idx + i],
                               model.vars.lut_valid.value[start_table_idx + i],
                               model.vars.lut_smuxdiv.value[start_table_idx + i],
                               model.vars.lut_limitl.value[start_table_idx + i],
                               model.vars.lut_limith.value[start_table_idx + i], min_freq,
                               max_freq, self.retime_calc_catchup_duration(sysclk_freq, model.vars.lut_freq.value[
                                  start_table_idx + i],
                                                                           model.vars.lut_smuxdiv.value[
                                                                               start_table_idx + i], (
                                                                                   model.vars.lut_limitl.value[
                                                                                       start_table_idx + i] +
                                                                                   model.vars.lut_limith.value[
                                                                                       start_table_idx + i]))))

    # Method name: retime_print
    # Defined in: lynx\calculators\calc_synth.py
    def retime_print(self, *arg):
        hide = True
        if (hide == False):
            print(arg)

    # Method name: return_ppnd
    # Defined in: ocelot\calculators\calc_synth.py
    def return_ppnd(self, fsynth, fif, lodiv):
        dcdcdiv = 13  # assuming constant 13 for now
        Tdmin = 0.8e-6
        Tdmax = 0.95e-6
        Ndmin = int(math.ceil(Tdmin * fsynth / dcdcdiv))
        Ndmax = int(math.floor(Tdmax * fsynth / dcdcdiv))
        best_error = 9e9
        for Nd in range(Ndmin, Ndmax + 1):
            val = Nd * dcdcdiv * (1 / lodiv - fif / fsynth) + 0.5
            error = abs(val - round(val))
            if error < best_error:
                best_error = error
                best_Nd = Nd
        ppnd = best_Nd if best_Nd < 512 else 511
        return (ppnd - 1)

    # Method name: return_retime_gen_entry
    # Defined in: lynx\calculators\calc_synth.py
    def return_retime_gen_entry(self, sysclk_freq, valid_freq, multiple, model, table_idx, start_table_idx):
        synth_freq_low = valid_freq * multiple
        smuxdiv = self.retime_calc_smuxdiv(synth_freq_low)
        next_multiple = multiple + smuxdiv
        synth_freq_high = valid_freq * next_multiple
        smuxdiv_high = self.retime_calc_smuxdiv(synth_freq_high)
        if ((smuxdiv_high > smuxdiv) and (not (multiple % smuxdiv_high))):
            next_multiple = multiple + smuxdiv_high
            synth_freq_high = valid_freq * next_multiple
        num_clks = round(multiple / smuxdiv) + 1
        limith = math.floor(
            num_clks / 2)  # round(num_clks / 2); C tend to round down, while python tend to round up odd number
        limitl = num_clks - limith
        synth_freq_min_catchup = self.retime_calc_min_synth_freq(sysclk_freq, smuxdiv, num_clks)
        # If low end frequency is less than allowable catchup limit frequency
        # then add an invalid entry region (from low to min_catchup)
        if (synth_freq_min_catchup > synth_freq_low):
            model.vars.lut_freq.value.append(int(synth_freq_low))
            if (synth_freq_min_catchup > (smuxdiv * SMUX_MAX_FREQ)):
                model.vars.lut_freq_upper.value.append(int(smuxdiv * SMUX_MAX_FREQ))
            else:
                model.vars.lut_freq_upper.value.append(int(round(synth_freq_min_catchup)))
            model.vars.lut_valid.value.append(0)
            model.vars.lut_smuxdiv.value.append(0)
            model.vars.lut_limitl.value.append(0)
            model.vars.lut_limith.value.append(0)
            model.vars.lut_table_index.value[table_idx] += 1
            model.vars.lut_freq.value.append(
                model.vars.lut_freq_upper.value[start_table_idx + model.vars.lut_table_index.value[table_idx] - 1])
        else:
            model.vars.lut_freq.value.append(int(synth_freq_low))
        # If smuxdiv the same, add the final valid entry
        # from either low or catchup limit (see above) to final frequency
        if (smuxdiv_high == smuxdiv):
            model.vars.lut_freq_upper.value.append(int(synth_freq_high))
            model.vars.lut_valid.value.append(1)
            model.vars.lut_smuxdiv.value.append(smuxdiv_high)
            model.vars.lut_limitl.value.append(int(limitl))
            model.vars.lut_limith.value.append(int(limith))
            model.vars.lut_table_index.value[table_idx] += 1
        else:
            if (synth_freq_min_catchup < (smuxdiv * SMUX_MAX_FREQ)):
                model.vars.lut_freq_upper.value.append(int(smuxdiv * SMUX_MAX_FREQ))
                model.vars.lut_valid.value.append(1)
                model.vars.lut_smuxdiv.value.append(smuxdiv)
                model.vars.lut_limitl.value.append(int(limitl))
                model.vars.lut_limith.value.append(int(limith))
                model.vars.lut_table_index.value[table_idx] += 1
            # If smuxdiv changes within a multiple, then recalculate the low limits
            num_clks = round(next_multiple / smuxdiv_high)
            limith = math.floor(
                num_clks / 2)  # round(num_clks / 2); C tend to round down, while python tend to round up odd number
            limitl = num_clks - limith
            synth_freq_low = smuxdiv * SMUX_MAX_FREQ
            synth_freq_min_catchup = self.retime_calc_min_synth_freq(sysclk_freq, smuxdiv_high, num_clks)
            if (synth_freq_min_catchup > synth_freq_low):
                if (model.vars.lut_valid.value[start_table_idx - 1] == 0):
                    model.vars.lut_freq_upper.value[start_table_idx - 1] = int(synth_freq_min_catchup)
                    model.vars.lut_freq.value.append(int(synth_freq_min_catchup))
                else:
                    model.vars.lut_freq.value.append(int(synth_freq_low))
                    model.vars.lut_freq_upper.value.append(int(synth_freq_min_catchup))
                    model.vars.lut_valid.value.append(0)
                    model.vars.lut_smuxdiv.value.append(0)
                    model.vars.lut_limitl.value.append(0)
                    model.vars.lut_limith.value.append(0)
                    model.vars.lut_table_index.value[table_idx] += 1
                    model.vars.lut_freq.value.append(int(synth_freq_min_catchup))
            else:
                model.vars.lut_freq.value.append(int(synth_freq_low))
            model.vars.lut_freq_upper.value.append(int(synth_freq_high))
            model.vars.lut_valid.value.append(1)
            model.vars.lut_smuxdiv.value.append(smuxdiv_high)
            model.vars.lut_limitl.value.append(int(limitl))
            model.vars.lut_limith.value.append(int(limith))
            model.vars.lut_table_index.value[table_idx] += 1
        return (next_multiple)

    # Method name: calc_reg_synthctrl
    # Defined in: lpwh72000\calculators\calc_radio.py
    def calc_reg_synthctrl(self, model):
        self._ip_reg_write(model, 'DLFTHRESH_LOCKTHRESHOLD', 3)