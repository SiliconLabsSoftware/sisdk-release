from pyradioconfig.parts.lynx.calculators.calc_synth import CALC_Synth_lynx


class calc_synth_leopard(CALC_Synth_lynx):

    def calc_adc_clockmode_reg(self,model):
        #This function handles writes to the registers impacting ADC clock mode
        adc_clock_mode = model.vars.adc_clock_mode.value

        if( model.vars.adc_clock_mode.var_enum.HFXOMULT == adc_clock_mode ):
            self._reg_write(model.vars.RAC_IFADCTRIM0_IFADCCLKSEL, 1)
        else:
            self._reg_write(model.vars.RAC_IFADCTRIM0_IFADCCLKSEL, 0)

    def calc_sylodivrloadcclk_reg(self, model):
        adc_rate_mode = model.vars.adc_rate_mode.value

        if adc_rate_mode == model.vars.adc_rate_mode.var_enum.HALFRATE:
            reg = 1
        else:
            reg = 0

        self._reg_write(model.vars.RAC_SYTRIM1_SYLODIVRLOADCCLKSEL, reg)

    def calc_ifadcenhalfmode_reg(self, model):

        adc_rate_mode = model.vars.adc_rate_mode.value

        if adc_rate_mode == model.vars.adc_rate_mode.var_enum.HALFRATE:
            reg = 1
        else:
            reg = 0

        self._reg_write(model.vars.RAC_IFADCTRIM0_IFADCENHALFMODE, reg)

    def calc_adc_clockmode_actual(self, model):
        #This function calculates the actual value of the adc clock mode based on the register value used
        ifadc_clk_sel = model.vars.RAC_IFADCTRIM0_IFADCCLKSEL.value

        if( 1 == ifadc_clk_sel ):
            model.vars.adc_clock_mode_actual.value = model.vars.adc_clock_mode.var_enum.HFXOMULT
        else:
            model.vars.adc_clock_mode_actual.value = model.vars.adc_clock_mode.var_enum.VCODIV

    def calc_adc_clock_config(self, model):
        # This function calculates both the ADC mode (e.g. fullrate, halfrate, etc) as well as the ADC clock divider path

        # By default always use VCODIV FULLRATE

        adc_rate_mode = model.vars.adc_rate_mode.var_enum.FULLRATE
        adc_clock_mode = model.vars.adc_clock_mode.var_enum.VCODIV

        # Load local variables back into model variables
        model.vars.adc_clock_mode.value = adc_clock_mode
        model.vars.adc_rate_mode.value = adc_rate_mode

    def calc_clkmult_div_reg(self, model):
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value
        adc_mode = model.vars.adc_rate_mode.value

        if adc_clock_mode_actual == model.vars.adc_clock_mode.var_enum.HFXOMULT:
            if adc_mode == model.vars.adc_rate_mode.var_enum.FULLRATE:
                # adc_full_speed from dpll_utils.py (xo * 8); 8 = 48 / (3 * 2)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVR, 1)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVN, 48)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVX, 3)
                self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTFREQCAL, 1)
                self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTBWCAL, 1)
            else:
                # adc_half_speed from dpll_utils.py (xo * 4); 4 = 40 / (5 * 2)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVR, 1)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVN, 40)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVX, 5)
                self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTFREQCAL, 0)
                self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTBWCAL, 0)
        else:
            # reset values
            self._reg_do_not_care(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVR)
            self._reg_do_not_care(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVN)
            self._reg_do_not_care(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVX)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTFREQCAL)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTBWCAL)

    def calc_clkmulten_reg(self, model):
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value

        # To enable clkmult the following additional registers must also be set, but are handled in RAIL
        # SYXO0.INTERNALCTRL.ENCLKMULTANA = 1 # enable XO output to CLKMULT
        # RAC.SYLOEN.SYLODIVRLO2P4GENEN = 0 # disable LODIV output buffer from SYLODIV (power saving)

        if adc_clock_mode_actual == model.vars.adc_clock_mode.var_enum.HFXOMULT:
            # unless otherwise specified, the values are taken from dualbclk_mult_validation_20190516_lynx_revA0.pptx > dpll_utils.py > dualbclk_mult spec sheet
            # based on the common settings for adc_full_speed, adc_full_speed_lp, adc_half_speed, adc_half_speed_lp
            # in dpll_utils.py
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTDISICO, 0) # 0 = ENABLE ICO, 1 = DISABLE ICO
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENBBDET, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENBBXLDET, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENBBXMDET, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENCFDET, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENDITHER, 0)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVADC, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVN, 0)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVP, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVRX2P4G, 0)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVRXSUBG, 0)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVTXDUALB, 0)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENFBDIV, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENREFDIV, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENREG1, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENREG2, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENREG3, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENROTDET, 1)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTENBYPASS40MHZ, 0)

            # EFRPTE-6618 is reverted due to MCUW_RADIO_CFG-3308 (Updates by design to block)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTREG1ADJV, 2)
            # self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTREG2ADJV, 2)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTREG2ADJI, 2)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTREG3ADJV, 2)

            self._reg_write(model.vars.RAC_CLKMULTEN1_CLKMULTINNIBBLE, 8)
            self._reg_write(model.vars.RAC_CLKMULTEN1_CLKMULTLDFNIB, 0)
            self._reg_write(model.vars.RAC_CLKMULTEN1_CLKMULTLDMNIB, 0)
            self._reg_write(model.vars.RAC_CLKMULTEN1_CLKMULTRDNIBBLE, 3)
            self._reg_write(model.vars.RAC_CLKMULTEN1_CLKMULTLDCNIB, 0)
            self._reg_write(model.vars.RAC_CLKMULTEN1_CLKMULTDRVAMPSEL, 7) # based on dpll_utils.py

            self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTENRESYNC, 0)
            self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTVALID, 0)
        else:
            # when using lodiv, turn off dualbclk_mult to reset values
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTDISICO)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENBBDET)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENBBXLDET)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENBBXMDET)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENCFDET)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENDITHER)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVADC)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVN)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVP)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVRX2P4G)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVRXSUBG)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVTXDUALB)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENFBDIV)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENREFDIV)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENREG1)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENREG2)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENREG3)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENROTDET)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTENBYPASS40MHZ)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTREG1ADJV)
            # self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTREG2ADJV)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTREG2ADJI)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTREG3ADJV)

            self._reg_do_not_care(model.vars.RAC_CLKMULTEN1_CLKMULTINNIBBLE)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN1_CLKMULTLDFNIB)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN1_CLKMULTLDMNIB)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN1_CLKMULTRDNIBBLE)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN1_CLKMULTLDCNIB)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN1_CLKMULTDRVAMPSEL)

            self._reg_do_not_care(model.vars.RAC_CLKMULTCTRL_CLKMULTENRESYNC)
            self._reg_do_not_care(model.vars.RAC_CLKMULTCTRL_CLKMULTVALID)

    def calc_adc_freq_actual(self,model):
        #This function calculates the actual ADC sample frequency and error based on the registers

        #Load model variables into local variables
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value
        adc_vco_div_actual = model.vars.adc_vco_div_actual.value
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        fsynth = model.vars.rx_synth_freq_actual.value
        fadc_target = model.vars.adc_target_freq.value #The target frequency is used for computing error
        ifadc_halfrate = model.vars.RAC_IFADCTRIM0_IFADCENHALFMODE.value

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

    def calc_adc_vco_div_actual(self, model):
        adc_vco_div = model.vars.adc_vco_div.value
        model.vars.adc_vco_div_actual.value = adc_vco_div

    def calc_adc_target_freq(self, model):
        #This function calculates the target sample frequency based on the ADC clock configuration

        #Load model variables into local variables
        adc_rate_mode = model.vars.adc_rate_mode.value #Use the target rate mode for now because we haven't yet chosen the exact VCODIV value
        adc_clock_mode = model.vars.adc_clock_mode.value
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value

        if (model.vars.adc_clock_mode.var_enum.HFXOMULT == adc_clock_mode):
            if (adc_rate_mode == model.vars.adc_rate_mode.var_enum.FULLRATE):
                fadc_target = 8 * xtal_frequency_hz
            elif(adc_rate_mode==model.vars.adc_rate_mode.var_enum.HALFRATE):
                fadc_target = 4 * xtal_frequency_hz
            else:
                fadc_target = xtal_frequency_hz
        else:
            #Clock mode is VCODIV
            if(adc_rate_mode==model.vars.adc_rate_mode.var_enum.HALFRATE):
                fadc_target = 152.5e6
            else:
                fadc_target = 305e6   #Target full rate

        #Load local variables back into model variables
        model.vars.adc_target_freq.value = int(fadc_target)

    def calc_adc_vco_div(self, model):
        adc_rate_mode_actual = model.vars.adc_rate_mode_actual.value

        if adc_rate_mode_actual == model.vars.adc_rate_mode.var_enum.FULLRATE:
            adc_vco_div = 8
        elif adc_rate_mode_actual == model.vars.adc_rate_mode.var_enum.HALFRATE:
            adc_vco_div = 16
        else:
            adc_vco_div = 32

        model.vars.adc_vco_div.value = adc_vco_div

    def calc_lo_target_freq(self,model):
        #This function calculates the target LO frequency baed on RF, IF, and injection side

        #Load model variables into local variables
        lo_injection_side = model.vars.lo_injection_side.value
        rf_freq = model.vars.base_frequency_hz.value
        if_freq = model.vars.if_frequency_hz.value #We don't yet know the actual synth frequency to get the true IF

        if lo_injection_side == model.vars.lo_injection_side.var_enum.HIGH_SIDE:
            lo_freq = rf_freq + if_freq
        else:
            lo_freq = rf_freq - if_freq

        #Load local variables back into model variables
        model.vars.lo_target_freq.value = lo_freq

    def calc_clkmult_div_reg(self, model):
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value
        adc_mode = model.vars.adc_rate_mode.value

        if adc_clock_mode_actual == model.vars.adc_clock_mode.var_enum.HFXOMULT:
            if adc_mode == model.vars.adc_rate_mode.var_enum.FULLRATE:
                # adc_full_speed from dpll_utils.py (xo * 8); 8 = 48 / (3 * 2)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVR, 1)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVN, 48)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVX, 3)
                self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTFREQCAL, 1)
                self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTBWCAL, 1)
            else:
                # adc_half_speed from dpll_utils.py (xo * 4); 4 = 40 / (5 * 2)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVR, 1)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVN, 40)
                self._reg_write(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVX, 5)
                self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTFREQCAL, 0)
                self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTBWCAL, 0)
        else:
            # reset values
            self._reg_do_not_care(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVR)
            self._reg_do_not_care(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVN)
            self._reg_do_not_care(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVX)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTFREQCAL)
            self._reg_do_not_care(model.vars.RAC_CLKMULTEN0_CLKMULTBWCAL)