from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcIQModPath(IPCalculator):
    """
    Calculation class for IQ Modulation Path.
    """
    # Method name: calc_iqmod_reg
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_iqmod_reg(self, model):
        """
        Calculate MUX selection of IQ modulator input between IQ samples from CORDIC vs. Direct IQ samples from BTC MODEM
        See architectural diagram in MCUW_RADIO_CFG-2472

        :param model:
        :return:
        """
        modulator_select = model.vars.modulator_select.value

        if modulator_select == model.vars.modulator_select.var_enum.IQ_MOD_DIRECT:
            iqmod = 1
        else:
            iqmod = 0

        self._ip_reg_write(model, 'TXCTRL_IQMOD', iqmod)

    # Method name: calc_txmod_reg
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_txmod_reg(self, model):
        modulator_select = model.vars.modulator_select.value

        if modulator_select in [model.vars.modulator_select.var_enum.IQ_MOD,
                                model.vars.modulator_select.var_enum.IQ_MOD_DIRECT]:
            modulator_select_val = 1  # : Use IQMOD
        else:
            modulator_select_val = 0  # : default to PHMOD
        self._ip_reg_write(model, 'TXCTRL_TXMOD', modulator_select_val)

    def calc_iq_mod_cic(self, model):
        demod_select = model.vars.demod_select.value
        if demod_select in [model.vars.demod_select.var_enum.HDT] :
            self._ip_reg_write(model, 'CIC_CICGAIN', 4)
            self._ip_reg_write(model, 'CIC_CICRATIO', 3)
        else:
            self._ip_reg_write_default(model, 'CIC_CICGAIN')
            self._ip_reg_write_default(model, 'CIC_CICRATIO')

    def calc_txcorrstaticoef(self, model):
        demod_select = model.vars.demod_select.value
        if demod_select in [model.vars.demod_select.var_enum.HDT]:
            self._ip_reg_write(model, 'TXCORRSTATIC_TXINVCORDICIN', 0)
            self._ip_reg_write(model, 'TXCORRSTATIC_TXIQSWAP', 1)
            self._ip_reg_write(model, 'TXCORRSTATIC_TXDACFORMAT', 1)
            self._ip_reg_write(model, 'TXCORRSTATIC_TXFREQCORR', 0)
            # MCUW_RADIO_CFG-3284
            self._ip_reg_write(model, 'TXCORRSTATIC_TXDGAIN', 273, limit_upper=511, limit_lower=0)

        else:
            if demod_select == model.vars.demod_select.var_enum.BTC:
                ### https://jira.silabs.com/browse/MCUW_RADIO_CFG-2737
                self._ip_reg_write(model, 'TXCORRSTATIC_TXDGAIN', 339, limit_upper=511, limit_lower=0)
            else:
                ### https://jira.silabs.com/browse/MCUW_RADIO_CFG-2737: for non BTC/HDT PHY, use 256 as per the previous commits by #2737 owner.
                self._ip_reg_write(model, 'TXCORRSTATIC_TXDGAIN', 256, limit_upper=511, limit_lower=0)
            self._ip_reg_write_default(model, 'TXCORRSTATIC_TXINVCORDICIN')
            self._ip_reg_write_default(model, 'TXCORRSTATIC_TXIQSWAP')
            self._ip_reg_write_default(model, 'TXCORRSTATIC_TXDACFORMAT')
            self._ip_reg_write_default(model, 'TXCORRSTATIC_TXFREQCORR')

    def calc_iq_shaping_filter(self, model):
        # writing default values for IQ shaping related registers
        # this IP block is used for setting raised cosin shaping filter and used for BTC and HDT PHYs
        demod_select = model.vars.demod_select.value
        if demod_select in [model.vars.demod_select.var_enum.HDT]:
            # TODO: can I be calculated based on shaping filter parameters by def root_raised_cosine_filter?
            self._ip_reg_write(model, 'IQSHAPING1_IQSHAPCOEFF0', 6)
            self._ip_reg_write(model, 'IQSHAPING1_IQSHAPCOEFF1', 7)

            self._ip_reg_write(model, 'IQSHAPING2_IQSHAPCOEFF2', 255)
            self._ip_reg_write(model, 'IQSHAPING2_IQSHAPCOEFF3', 243)
            self._ip_reg_write(model, 'IQSHAPING2_IQSHAPCOEFF4', 234)
            self._ip_reg_write(model, 'IQSHAPING2_IQSHAPCOEFF5', 243)

            self._ip_reg_write(model, 'IQSHAPING3_IQSHAPCOEFF6', 19)
            self._ip_reg_write(model, 'IQSHAPING3_IQSHAPCOEFF7', 67)
            self._ip_reg_write(model, 'IQSHAPING3_IQSHAPCOEFF8', 110)
            self._ip_reg_write(model, 'IQSHAPING3_IQSHAPCOEFF9', 127)
        else:
            self._ip_reg_write_default(model, 'IQSHAPING1_IQSHAPCOEFF0')
            self._ip_reg_write_default(model, 'IQSHAPING1_IQSHAPCOEFF1')

            self._ip_reg_write_default(model, 'IQSHAPING2_IQSHAPCOEFF2')
            self._ip_reg_write_default(model, 'IQSHAPING2_IQSHAPCOEFF3')
            self._ip_reg_write_default(model, 'IQSHAPING2_IQSHAPCOEFF4')
            self._ip_reg_write_default(model, 'IQSHAPING2_IQSHAPCOEFF5')

            self._ip_reg_write_default(model, 'IQSHAPING3_IQSHAPCOEFF6')
            self._ip_reg_write_default(model, 'IQSHAPING3_IQSHAPCOEFF7')
            self._ip_reg_write_default(model, 'IQSHAPING3_IQSHAPCOEFF8')
            self._ip_reg_write_default(model, 'IQSHAPING3_IQSHAPCOEFF9')

    def calc_iq_shaping_misc(self, model):
        demod_select = model.vars.demod_select.value
        if demod_select in [model.vars.demod_select.var_enum.HDT]:
            self._ip_reg_write(model, 'IQSHAPING1_IQSHAPINTERPRATIO', 3)
            self._ip_reg_write(model, 'IQSHAPING1_IQSHAPGAIN', 8)
        else:
            self._ip_reg_write_default(model, 'IQSHAPING1_IQSHAPINTERPRATIO')
            self._ip_reg_write_default(model, 'IQSHAPING1_IQSHAPGAIN')