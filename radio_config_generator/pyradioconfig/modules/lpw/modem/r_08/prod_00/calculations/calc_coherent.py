from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from scipy import interpolate
import math

# todo: seems like these are all COHDSA settings now, since we don't have PHDSA anymore..
#  can we combine this with coherent_demod.py or something?
# todo: use this for dont care setup? demod_select == model.vars.demod_select.var_enum.COHERENT
class CalcCoherent(IPCalculator):

    # Method name: calc_arrthd_reg
    # Defined in: lpwh72000\calculators\calc_coherent.py
    def calc_arrthd_reg(self, model):
        pass

    # Method name: calc_cohdsa_addwndsize
    # Defined in: ocelot\calculators\calc_coherent.py
    def calc_cohdsa_addwndsize(self, model):
        demod_select = model.vars.demod_select.value
        target_osr = model.vars.target_osr.value
        dsss_len = model.vars.dsss_len_actual.value
        # : For coherent demod, advance timing window from DSA detection by half symbol
        # : This is assuming that DSA detection occured on 3rd or 4th preamble.
        # : For now, choosing to detect dsa on 3rd or 4th preamble so that the difference between peak and noise will be
        # : high. This may result in sensitivity degradation since the static DSA threshold will be set high.
        # : If DSA detection occurs on 1st or 2nd preamble, need to DELAY (negative) by 2 symbols
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            wndsize = target_osr * dsss_len / 2.0
            # wndsize = math.pow(2,10) - (target_osr * 2.0 * dsss_len)
            # wndsize = math.pow(2, 10) - (target_osr * 3.0 * dsss_len)
        else:
            wndsize = 0
        wndsize = int(wndsize)
        self._ip_reg_write(model, 'COH3_COHDSAADDWNDSIZE', wndsize)

    # Method name: calc_cohdsa_check_peak_index_length
    # Defined in: ocelot\calculators\calc_coherent.py
    def calc_cohdsa_check_peak_index_length(self, model):
        # : Disable check if difference in the indices of prefilter correlation peaks is less than dsapeakindlen
        self._ip_reg_write(model, 'COH3_DSAPEAKCHKEN', 0)
        self._ip_reg_write(model, 'COH3_DSAPEAKINDLEN', 0)

    # Method name: calc_cohdsa_dynamic_iir_filter_coefficient
    # Defined in: ocelot\calculators\calc_coherent.py
    def calc_cohdsa_dynamic_iir_filter_coefficient(self, model):
        demod_select = model.vars.demod_select.value
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            # : Set to maximum filtering
            dyniircoef = 3
        else:
            dyniircoef = 0
        self._ip_reg_write(model, 'COH3_DYNIIRCOEFOPTION', dyniircoef)

    # Method name: calc_cohdsa_dynamic_threshold
    # Defined in: ocelot\calculators\calc_coherent.py
    def calc_cohdsa_dynamic_threshold(self, model):
        demod_select = model.vars.demod_select.value
        chpwr_accumux_noise = model.vars.chpwraccu_noise.value
        base_frequency_hz = model.vars.base_frequency_hz.value
        if base_frequency_hz <= 500e6:
            static_cohdsa_threshold = 140
            baseline_dynamic_cohdsa_threshold = 140
        else:
            static_cohdsa_threshold = 100
            baseline_dynamic_cohdsa_threshold = 100
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            self._ip_reg_write(model, 'LONGRANGE6_LRSPIKETHD', static_cohdsa_threshold)
            self._ip_reg_write(model, 'COH2_FIXEDCDTHFORIIR', baseline_dynamic_cohdsa_threshold)
            self._ip_reg_write(model, 'LONGRANGE6_LRCHPWRSPIKETH', int(round(chpwr_accumux_noise + 6)))
        else:
            self._ip_reg_write(model, 'LONGRANGE6_LRCHPWRSPIKETH', 0)
            self._ip_reg_write(model, 'LONGRANGE6_LRSPIKETHD', 0)
            self._ip_reg_write(model, 'COH2_FIXEDCDTHFORIIR', 0)

    # Method name: calc_cohdsa_mode
    # Defined in: ocelot\calculators\calc_coherent.py
    def calc_cohdsa_mode(self, model):
        demod_select = model.vars.demod_select.value
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            enable_cohdsa = 1
        else:
            enable_cohdsa = 0
        self._ip_reg_write(model, 'COH3_COHDSAEN', enable_cohdsa)

    # Method name: calc_cohdsa_signal_select
    # Defined in: ocelot\calculators\calc_coherent.py
    def calc_cohdsa_signal_select(self, model):
        demod_select = model.vars.demod_select.value
        # : For coherent demod, use 4 bits from 10 bit complex multiplier output for pre filter
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            number_of_bits_from_prefilter = 4
        else:
            number_of_bits_from_prefilter = 0
        self._ip_reg_write(model, 'COH3_CDSS', number_of_bits_from_prefilter)

    # Method name: calc_dsactrl_lowduty
    # Defined in: lpwh72000\calculators\calc_coherent.py
    def calc_dsactrl_lowduty(self, model):
        pass

    # Method name: calc_dsamode_reg
    # Defined in: lpwh72000\calculators\calc_coherent.py
    def calc_dsamode_reg(self, model):
        pass

    # Method name: calc_longrange_timeout_threshold
    # Defined in: ocelot\calculators\calc_coherent.py
    def calc_longrange_timeout_threshold(self, model):
        """
        For COHDSA, wait for this time out after prefilter detect before shutting demod down.
        Args:
            model:
        Returns:
        """
        demod_select = model.vars.demod_select.value
        bitrate_gross = model.vars.bitrate_gross.value
        preamble_pattern_len = model.vars.preamble_pattern_len.value
        demod_rate = model.vars.demod_rate_actual.value
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            preamble_pattern_time_us = preamble_pattern_len * (1 / bitrate_gross) * 1e6
            # : timeout [us] = LRTIMEOUTTHD / demod_rate_MHz
            # : wait twice preamble pattern length
            demod_rate_MHz = demod_rate / 1e6
            lrtimeoutthd_reg = int(round(demod_rate_MHz * preamble_pattern_time_us * 2.0))
        else:
            lrtimeoutthd_reg = 0
        self._ip_reg_write(model, 'LONGRANGE1_LRTIMEOUTTHD', lrtimeoutthd_reg)

    # Method name: calc_phdsa_defaults
    # Defined in: lpwh72000\calculators\calc_coherent.py
    def calc_phdsa_defaults(self, model):
        pass

    def calc_dagc_channel_power_accumulator_reg(self, model):
        demod_select = model.vars.demod_select.value
        modtype = model.vars.modulation_type.value
        preamble_pattern_len = model.vars.preamble_pattern_len.value
        sens_calculated = model.vars.sensitivity.value
        target_osr = model.vars.target_osr.value
        agc_period_actual = model.vars.agcperiod_actual.value
        baudrate = model.vars.baudrate.value
        bitrate = model.vars.bitrate.value
        mod_format = model.vars.modulation_type.value

        if hasattr(model.profiles, 'Long_Range'):
            is_long_range = model.profile == model.profiles.Long_Range
        else:
            is_long_range = False

        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            # : accumulate channel power for preamble pattern duration
            # : actual avgwin period is 2^(avgwin+2)*2^pwrperiod_s*OSR
            # : agc_period_actual = 2^pwrperiod
            # : actual avgwin time is 2^(avgwin+2)*agc_period_actual/baudrate
            preamble_time_us = preamble_pattern_len * (1 / bitrate) * 1e6
            target_avgwin_time_us = 4.0 * preamble_time_us
            target_avgwin_period = (target_avgwin_time_us / 1e6) * baudrate
            target_avgwin = round(math.log2(target_avgwin_period / agc_period_actual) - 2)
            if target_avgwin < 0:
                target_avgwin = 0
            avgwin = int(target_avgwin)
            chpwraccudel = 0
        else:
            avgwin = 0
            chpwraccudel = 0

        if demod_select == model.vars.demod_select.var_enum.COHERENT and \
                mod_format == model.vars.modulation_type.var_enum.OQPSK:
            # : 0 - Channel power is locked when timing is detected
            # : 1 - Channel power is locked when DSA is detected
            self._ip_reg_write(model, 'COH0_COHCHPWRLOCK', 0)
            # : Set to enable automatic restart of channel power - needed to make sure channel power is not dependent on
            # : power of received frames
            self._ip_reg_write(model, 'COH0_COHCHPWRRESTART', 1)
        else:
            self._ip_reg_write(model, 'COH0_COHCHPWRLOCK', 0)
            self._ip_reg_write(model, 'COH0_COHCHPWRRESTART', 0)

        if demod_select == model.vars.demod_select.var_enum.COHERENT and is_long_range:
            self._ip_reg_write(model, 'LONGRANGE1_AVGWIN', avgwin)
            self._ip_reg_write(model, 'LONGRANGE1_CHPWRACCUDEL', chpwraccudel)
        else:
            self._ip_reg_write(model, 'LONGRANGE1_AVGWIN', 0)
            self._ip_reg_write(model, 'LONGRANGE1_CHPWRACCUDEL', 0)

    def calc_dagc_dynamic_bbss_reg(self, model):
        demod_select = model.vars.demod_select.value
        sens_calculated = model.vars.sensitivity.value
        bitrate = model.vars.bitrate.value
        mod_format = model.vars.modulation_type.value

        if hasattr(model.profiles, 'Long_Range'):
            is_long_range = model.profile == model.profiles.Long_Range
        else:
            is_long_range = False

        """ Model calculation range based on DUT power [dBm] """
        min_dut_power = -140 # : This is arbitrarily low power that should be below sensitivity
        max_dut_power = 10 # : This is maximum supported receive power of DUT
        if sens_calculated < min_dut_power:
            min_dut_power = round(sens_calculated) - 10
        dut_power_list = list(range(min_dut_power ,max_dut_power ,+1))

        """ Model of Q Sample vs. Dut Power """
        estimated_adc_noise_dBm = -162.8694 # This is measured value
        model_max_Q_list = []
        for dut_power in  dut_power_list:
            # : Model ADC resolution
            adc_enob = (dut_power - estimated_adc_noise_dBm - 1.76) / 6.02

            # : Model analog frontend noise
            minimum_detectable_signal_dBm = -173.9 + 10 *math.log10(bitrate) + 4.0
            if bitrate <= 2.8e3:
                analog_noise_bitwidth = 0.1938 * minimum_detectable_signal_dBm + 33.296
            elif bitrate < 67e3: # : TODO change to ADC mode.
                analog_noise_bitwidth = 0.1565 * minimum_detectable_signal_dBm + 27.928
            else:
                analog_noise_bitwidth = 0.1599 * minimum_detectable_signal_dBm + 28.119

            # : Determine signal + noise level
            signal_max_q = math.pow(2 ,adc_enob) + math.pow(2 ,analog_noise_bitwidth)
            signal_max_q_bitwidth = math.log2(signal_max_q)
            if signal_max_q_bitwidth > 17:
                signal_max_q_bitwidth = 17

            model_max_Q_list.append(signal_max_q_bitwidth)

        # : Calculate bbss shift based on the Q sample model
        bbss_model = []
        for model_max_Q in model_max_Q_list:
            bbss_at_max_Q_calc = round(model_max_Q - 5.5)
            bbss_model.append(bbss_at_max_Q_calc)

        """ Calculate chpwraccumux model """
        model_chpwraccumux_list = []
        for dut_power in dut_power_list:
            calc_chpwraccumux = dut_power + 139.0

            # : Based on measurement, chpwraccumux does not go below 14 due to noise
            if calc_chpwraccumux < 14:
                calc_chpwraccumux = 14
            # : By design, maximum chpwraccumux is 80 due signal power after AGC
            elif calc_chpwraccumux > 80:
                calc_chpwraccumux = 80

            model_chpwraccumux_list.append(calc_chpwraccumux)

        """  """
        # : Calculate chpwraccumux at sensitivity. This can be used to calculate noise level
        chpwraccumux_interp_func = interpolate.interp1d(dut_power_list, model_chpwraccumux_list)
        chpwr_accumux_noise = float(chpwraccumux_interp_func(sens_calculated))

        """ """
        bbss_interp_func = interpolate.interp1d(dut_power_list, bbss_model)
        starting_BBSS = math.ceil(bbss_interp_func(sens_calculated))

        """ Calculate BBSS transitions """
        bbss_transition = []
        bbss_transition_threshold = []
        for dut_power_index in range(len(dut_power_list)):
            bbss_val = bbss_model[dut_power_index]
            if bbss_val > starting_BBSS:
                if bbss_model[dut_power_index -1] < bbss_val:
                    bbss_transition.append(int(bbss_val))
                    bbss_transition_threshold.append(int(round(model_chpwraccumux_list[dut_power_index])))

        # : Add two bbss transitions below sensitivity
        bbss_transition.insert(0, starting_BBSS)
        bbss_transition.insert(0, starting_BBSS - 1)
        bbss_transition_threshold.insert(0, int(round(chpwr_accumux_noise -6)))

        # : fill up remaining registers
        max_bbss_shift = 12
        while len(bbss_transition_threshold) < 11:
            bbss_transition_threshold.append(80)
        while len(bbss_transition) < 12:
            bbss_transition.append(max_bbss_shift)

        """ Set calculated value """
        model.vars.chpwraccu_noise.value = chpwr_accumux_noise

        """ Set registers related to dynamic bbss mode"""
        if demod_select == model.vars.demod_select.var_enum.COHERENT and \
                mod_format == model.vars.modulation_type.var_enum.OQPSK:
            # : Enable dynamic BBSS adjustment
            self._ip_reg_write(model, 'COH0_COHDYNAMICBBSSEN', 1)

            # : BBSS hysteresis
            self._ip_reg_write(model, 'LONGRANGE1_HYSVAL', 3)
        else:
            self._ip_reg_write(model, 'COH0_COHDYNAMICBBSSEN', 0)
            self._ip_reg_write(model, 'LONGRANGE1_HYSVAL', 0)

        """ Set registers related to dynamic thresholds """
        if demod_select == model.vars.demod_select.var_enum.COHERENT and is_long_range:
            # : BBSS thresholds
            self._ip_reg_write(model, 'LONGRANGE2_LRCHPWRTH1', bbss_transition_threshold[0])
            self._ip_reg_write(model, 'LONGRANGE2_LRCHPWRTH2', bbss_transition_threshold[1])
            self._ip_reg_write(model, 'LONGRANGE2_LRCHPWRTH3', bbss_transition_threshold[2])
            self._ip_reg_write(model, 'LONGRANGE2_LRCHPWRTH4', bbss_transition_threshold[3])
            self._ip_reg_write(model, 'LONGRANGE3_LRCHPWRTH5', bbss_transition_threshold[4])
            self._ip_reg_write(model, 'LONGRANGE3_LRCHPWRTH6', bbss_transition_threshold[5])
            self._ip_reg_write(model, 'LONGRANGE3_LRCHPWRTH7', bbss_transition_threshold[6])
            self._ip_reg_write(model, 'LONGRANGE3_LRCHPWRTH8', bbss_transition_threshold[7])
            self._ip_reg_write(model, 'LONGRANGE4_LRCHPWRTH9', bbss_transition_threshold[8])
            self._ip_reg_write(model, 'LONGRANGE4_LRCHPWRTH10', bbss_transition_threshold[9])
            self._ip_reg_write(model, 'LONGRANGE6_LRCHPWRTH11', bbss_transition_threshold[10])

            # : BBSS Shifts
            self._reg_limit_write(model.vars.MODEM_LONGRANGE4_LRCHPWRSH1, bbss_transition[0], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE4_LRCHPWRSH2, bbss_transition[1], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE4_LRCHPWRSH3, bbss_transition[2], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE4_LRCHPWRSH4, bbss_transition[3], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE5_LRCHPWRSH5, bbss_transition[4], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE5_LRCHPWRSH6, bbss_transition[5], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE5_LRCHPWRSH7, bbss_transition[6], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE5_LRCHPWRSH8, bbss_transition[7], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE5_LRCHPWRSH9, bbss_transition[8], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE5_LRCHPWRSH10, bbss_transition[9], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE5_LRCHPWRSH11, bbss_transition[10], max_bbss_shift)
            self._reg_limit_write(model.vars.MODEM_LONGRANGE6_LRCHPWRSH12, bbss_transition[11], max_bbss_shift)
        else:
            self._ip_reg_write(model, 'LONGRANGE2_LRCHPWRTH1', 0)
            self._ip_reg_write(model, 'LONGRANGE2_LRCHPWRTH2', 0)
            self._ip_reg_write(model, 'LONGRANGE2_LRCHPWRTH3', 0)
            self._ip_reg_write(model, 'LONGRANGE2_LRCHPWRTH4', 0)
            self._ip_reg_write(model, 'LONGRANGE3_LRCHPWRTH5', 0)
            self._ip_reg_write(model, 'LONGRANGE3_LRCHPWRTH6', 0)
            self._ip_reg_write(model, 'LONGRANGE3_LRCHPWRTH7', 0)
            self._ip_reg_write(model, 'LONGRANGE3_LRCHPWRTH8', 0)
            self._ip_reg_write(model, 'LONGRANGE4_LRCHPWRTH9', 0)
            self._ip_reg_write(model, 'LONGRANGE4_LRCHPWRTH10', 0)
            self._ip_reg_write(model, 'LONGRANGE6_LRCHPWRTH11', 0)
            self._ip_reg_write(model, 'LONGRANGE4_LRCHPWRSH1', 0)
            self._ip_reg_write(model, 'LONGRANGE4_LRCHPWRSH2', 0)
            self._ip_reg_write(model, 'LONGRANGE4_LRCHPWRSH3', 0)
            self._ip_reg_write(model, 'LONGRANGE4_LRCHPWRSH4', 0)
            self._ip_reg_write(model, 'LONGRANGE5_LRCHPWRSH5', 0)
            self._ip_reg_write(model, 'LONGRANGE5_LRCHPWRSH6', 0)
            self._ip_reg_write(model, 'LONGRANGE5_LRCHPWRSH7', 0)
            self._ip_reg_write(model, 'LONGRANGE5_LRCHPWRSH8', 0)
            self._ip_reg_write(model, 'LONGRANGE5_LRCHPWRSH9', 0)
            self._ip_reg_write(model, 'LONGRANGE5_LRCHPWRSH10', 0)
            self._ip_reg_write(model, 'LONGRANGE5_LRCHPWRSH11', 0)
            self._ip_reg_write(model, 'LONGRANGE6_LRCHPWRSH12', 0)

    def calc_agc_baudrate_calculation_mode(self, model):
        # : TODO move out of calc_modem_dagc
        demod_select = model.vars.demod_select.value

        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            # : disable RX baudrate calculation used by AGC and instead assume OSR = 2 * RXBRFRAC
            self._ip_reg_write(model, 'CTRL6_RXBRCALCDIS', 1)
        else:
            self._ip_reg_write(model, 'CTRL6_RXBRCALCDIS', 0)