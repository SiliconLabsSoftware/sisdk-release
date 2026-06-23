from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcRfctrlAdc(IPCalculator):

    def calc_adcclksel_reg(self, model):
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value

        if adc_clock_mode_actual == model.vars.adc_clock_mode.var_enum.VCODIV:
            reg = 0
        else:
            reg = 1
        self._ip_reg_write(model,'ADCCTRL0_ADCCLKSEL', reg)

    def calc_adcsidetoneamp_reg(self, model):
        self._ip_reg_write(model,'ADCTRIM0_ADCSIDETONEAMP', 3)

    def calc_adc_rate_mode_actual(self, model):
        # This function calculates the actual value of the adc rate mode based on the reg value used
        ifadcenhalfmode = model.vars.RFCTRL_ADCCTRL1_ADCENHALFMODE.value

        if ifadcenhalfmode == 1:
            adc_rate_mode_actual = model.vars.adc_rate_mode.var_enum.HALFRATE
        else:
            adc_rate_mode_actual = model.vars.adc_rate_mode.var_enum.FULLRATE

        # Write the variable
        model.vars.adc_rate_mode_actual.value = adc_rate_mode_actual
    def calc_adc_rate_vco_div(self, model):
        adc_rate_mode = model.vars.adc_rate_mode.value
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value

        if adc_rate_mode == model.vars.adc_rate_mode.var_enum.HALFRATE:
            SYLODIVADCDIVRATIO_reg = 0
            ADCENHALFMODE_reg = 1
            adc_vco_div = 16
        else:
            SYLODIVADCDIVRATIO_reg = 1
            ADCENHALFMODE_reg = 0
            adc_vco_div = 8
        model.vars.adc_vco_div.value = adc_vco_div
        self._ip_reg_write(model, 'SYLOCTRL0_SYLODIVADCDIVRATIO', SYLODIVADCDIVRATIO_reg)
        self._ip_reg_write(model, 'ADCCTRL1_ADCENHALFMODE', ADCENHALFMODE_reg)


    def calc_adc_freq_actual(self,model):
        #This function calculates the actual ADC sample frequency and error based on the registers

        #Load model variables into local variables
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value
        adc_vco_div_actual = model.vars.adc_vco_div_actual.value
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        fsynth = model.vars.rx_synth_freq_actual.value
        fadc_target = model.vars.adc_target_freq.value #The target frequency is used for computing error
        ifadc_halfrate = model.vars.RFCTRL_ADCCTRL1_ADCENHALFMODE.value #TODO: implement IP read

        if adc_clock_mode_actual == model.vars.adc_clock_mode.var_enum.HFXOMULT:
            #the ordering of the if statements is important - keep ifadcpll_en_xo_bypass on top
            if 1 == ifadc_halfrate:
                adc_freq_actual = xtal_frequency_hz * 4
            else:
                adc_freq_actual = xtal_frequency_hz * 8
        else:
            adc_freq_actual = int(fsynth / adc_vco_div_actual)

        # Compute the final ADC frequency percent error
        ferror = 100 * (fadc_target - adc_freq_actual) / float(fadc_target)

        #Load local variables back into model variables
        model.vars.adc_freq_actual.value = adc_freq_actual
        model.vars.adc_freq_error.value = ferror

    # Method name: calc_adc_clock_config
    # Defined in: bobcat\calculators\calc_synth.py
    def calc_adc_clock_config(self, model):
        # This function calculates both the ADC mode (e.g. fullrate, halfrate, etc) as well as the ADC clock divider path
        # Load model values into local variables
        bandwidth_hz = model.vars.bandwidth_hz.value
        if (bandwidth_hz < 1.25e6):
            # 1/2 rate mode
            # Use the HFXO along with DPLL for the ADC clock
            adc_rate_mode = model.vars.adc_rate_mode.var_enum.HALFRATE
            adc_clock_mode = model.vars.adc_clock_mode.var_enum.VCODIV
        else:
            # Full rate mode
            # Use the divided down VCO for the ADC clock
            adc_rate_mode = model.vars.adc_rate_mode.var_enum.FULLRATE
            adc_clock_mode = model.vars.adc_clock_mode.var_enum.VCODIV
        # Load local variables back into model variables
        model.vars.adc_clock_mode.value = adc_clock_mode
        model.vars.adc_rate_mode.value = adc_rate_mode

    # Method name: calc_adc_clockmode_actual
    # Defined in: lpwh72000\calculators\calc_synth.py
    def calc_adc_clockmode_actual(self, model):
        adc_clock_mode = model.vars.adc_clock_mode.value
        if (model.vars.adc_clock_mode.var_enum.HFXOMULT == adc_clock_mode):
            model.vars.adc_clock_mode_actual.value = model.vars.adc_clock_mode.var_enum.HFXOMULT
        else:
            model.vars.adc_clock_mode_actual.value = model.vars.adc_clock_mode.var_enum.VCODIV

    # Method name: calc_adc_vco_div_actual
    # Defined in: bobcat\calculators\calc_synth.py
    def calc_adc_vco_div_actual(self, model):
        syloadcdivratio = model.vars.RFCTRL_SYLOCTRL0_SYLODIVADCDIVRATIO.value #todo: implement ip_read
        if syloadcdivratio == 0:
            adcvcodiv = 16
        elif syloadcdivratio == 1:
            adcvcodiv = 8
        else:
            # its either DIV4 or DIV4B
            adcvcodiv = 4
        model.vars.adc_vco_div_actual.value = adcvcodiv

    # Method name: calc_adc_target_freq
    # Defined in: ocelot\calculators\calc_synth.py
    def calc_adc_target_freq(self, model):
        # This function calculates the target sample frequency based on the ADC clock configuration
        # Load model variables into local variables
        adc_rate_mode = model.vars.adc_rate_mode.value  # Use the target rate mode for now because we haven't yet chosen the exact VCODIV value
        adc_clock_mode = model.vars.adc_clock_mode.value
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        if (model.vars.adc_clock_mode.var_enum.HFXOMULT == adc_clock_mode):
            if (adc_rate_mode == model.vars.adc_rate_mode.var_enum.FULLRATE):
                fadc_target = 8 * xtal_frequency_hz
            elif (adc_rate_mode == model.vars.adc_rate_mode.var_enum.HALFRATE):
                fadc_target = 4 * xtal_frequency_hz
            else:
                fadc_target = xtal_frequency_hz
        else:
            # Clock mode is VCODIV
            # todo: its same as HFXOMULT, so is it really a different usecase?
            if (adc_rate_mode == model.vars.adc_rate_mode.var_enum.HALFRATE):
                fadc_target = 160e6
            else:
                fadc_target = 320e6  # Target full rate
        # Load local variables back into model variables
        model.vars.adc_target_freq.value = int(fadc_target)