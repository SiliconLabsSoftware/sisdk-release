from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcRfctrlClkmult(IPCalculator):

    def calc_clkmulten_reg(self, model):
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value

        # To enable clkmult the following additional registers must also be set, but are handled in RAIL
        # SYXO0.INTERNALCTRL.ENCLKMULTANA = 1 # enable XO output to CLKMULT
        # RAC.SYLOEN.SYLODIVRLO2P4GENEN = 0 # disable LODIV output buffer from SYLODIV (power saving)

        if adc_clock_mode_actual == model.vars.adc_clock_mode.var_enum.HFXOMULT:
            # unless otherwise specified, the values are taken from dualbclk_mult_validation_20190516_lynx_revA0.pptx > dpll_utils.py > dualbclk_mult spec sheet
            # based on the common settings for adc_full_speed, adc_full_speed_lp, adc_half_speed, adc_half_speed_lp
            # in dpll_utils.py
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTDISICO', 0) # 0 = ENABLE ICO, 1 = DISABLE ICO
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENBBDET', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENBBXLDET', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENBBXMDET', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENCFDET', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENDITHER', 0)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENDRVADC', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENDRVN', 0)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENDRVP', 1)
            # self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENDRVRX2P4G', 0)
            # self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENDRVRXSUBG', 0)
            # self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENDRVTXDUALB', 0)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENFBDIV', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENREFDIV', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENREG1', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENREG2', 1)
            # self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENREG3', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENROTDET', 1)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTENBYPASS40MHZ', 0)

            # regulators set to max voltage, current for hot temp performance EFRPTE-6618
            # self._ip_reg_write(model,'CLKMULTEN0_CLKMULTREG1ADJV', 3)
            # self._ip_reg_write(model,'CLKMULTEN0_CLKMULTREG2ADJV', 3)
            # self._ip_reg_write(model,'CLKMULTEN0_CLKMULTREG2ADJI', 3)
            # self._ip_reg_write(model,'CLKMULTEN0_CLKMULTREG3ADJV', 3)

            self._ip_reg_write(model,'CLKMULTEN1_CLKMULTINNIBBLE', 8)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTLDFNIB', 0)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTLDMNIB', 0)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTRDNIBBLE', 3)
            self._ip_reg_write(model,'CLKMULTEN0_CLKMULTLDCNIB', 0)
            self._ip_reg_write(model,'CLKMULTEN1_CLKMULTDRVAMPSEL', 7) # based on dpll_utils.py

            self._ip_reg_write(model,'CLKMULTCTRL_CLKMULTENRESYNC', 0)
            self._ip_reg_write(model,'CLKMULTCTRL_CLKMULTVALID', 0)
        else:
            # when using lodiv, turn off dualbclk_mult to reset values
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTDISICO')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENBBDET')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENBBXLDET')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENBBXMDET')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENCFDET')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENDITHER')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENDRVADC')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENDRVN')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENDRVP')
            # self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENDRVRX2P4G')
            # self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENDRVRXSUBG')
            # self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENDRVTXDUALB')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENFBDIV')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENREFDIV')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENREG1')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENREG2')
            # self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENREG3')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENROTDET')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTENBYPASS40MHZ')
            # self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTREG1ADJV')
            # self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTREG2ADJV')
            # self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTREG2ADJI')
            # self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTREG3ADJV')

            self._ip_reg_write_default(model, 'CLKMULTEN1_CLKMULTINNIBBLE')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTLDFNIB')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTLDMNIB')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTRDNIBBLE')
            self._ip_reg_write_default(model, 'CLKMULTEN0_CLKMULTLDCNIB')
            self._ip_reg_write_default(model, 'CLKMULTEN1_CLKMULTDRVAMPSEL')

            self._ip_reg_write_default(model, 'CLKMULTCTRL_CLKMULTENRESYNC')
            self._ip_reg_write_default(model, 'CLKMULTCTRL_CLKMULTVALID')

    def calc_clkmult_div_reg(self, model):
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value
        ifadc_halfrate = model.vars.RFCTRL_ADCCTRL1_ADCENHALFMODE.value

        if adc_clock_mode_actual == model.vars.adc_clock_mode.var_enum.HFXOMULT:
            if ifadc_halfrate == 0:
                # adc_full_speed from dpll_utils.py (xo * 8); 8 = 48 / (3 * 2)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTDIVR', 1)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTDIVN', 48)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTDIVX', 3)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTFREQCAL', 1)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTBWCAL', 1)
            else:
                # adc_half_speed from dpll_utils.py (xo * 4); 4 = 40 / (5 * 2)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTDIVR', 1)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTDIVN', 40)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTDIVX', 5)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTFREQCAL', 0)
                self._ip_reg_write(model, 'CLKMULTEN1_CLKMULTBWCAL', 0)
        else:
            # reset values
            self._ip_reg_write_default(model, 'CLKMULTEN1_CLKMULTDIVR')
            self._ip_reg_write_default(model, 'CLKMULTEN1_CLKMULTDIVN')
            self._ip_reg_write_default(model, 'CLKMULTEN1_CLKMULTDIVX')
            self._ip_reg_write_default(model, 'CLKMULTEN1_CLKMULTFREQCAL')
            self._ip_reg_write_default(model, 'CLKMULTEN1_CLKMULTBWCAL')

    def calc_clkmulten_tx_reg(self, model):
        # issue here is that the dpll does not have TX/RX registers for all settings (en_bbdet, etc)
        # HFXOBYP still has the DPLL loop running, but just bypasses in the final R divider, causing
        # higher current. Acceptable for Rainier, but needs to be optimized in Everest
        # fout=fxtal/divr*divn/divx
        dac_clock_mode_actual = model.vars.dac_clock_mode.value

        if dac_clock_mode_actual == model.vars.dac_clock_mode.var_enum.DISABLED:
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTENBYPASS40MHZTX', 0)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVNTX', 0)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVRTX', 0)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVXTX', 0)
        elif dac_clock_mode_actual == model.vars.dac_clock_mode.var_enum.HFXO:
            # need to confirm implementation, but as of today this is not used at all
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTENBYPASS40MHZTX', 1)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVNTX', 1)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVRTX', 1)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVXTX', 0)
        elif dac_clock_mode_actual == model.vars.dac_clock_mode.var_enum.HFXOx2:
            # https://jira.silabs.com/browse/MCUW_RADIO_CFG-3520
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTENBYPASS40MHZTX', 0)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVNTX', 40)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVRTX', 1)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVXTX', 5) 
        elif dac_clock_mode_actual == model.vars.dac_clock_mode.var_enum.HFXOx4:
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTENBYPASS40MHZTX', 0)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVNTX', 32)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVRTX', 1)
            self._ip_reg_write(model, 'CLKMULTEN2_CLKMULTDIVXTX', 4)
        else:
            raise RuntimeError(f"Invalid dac clock mode {dac_clock_mode_actual}")