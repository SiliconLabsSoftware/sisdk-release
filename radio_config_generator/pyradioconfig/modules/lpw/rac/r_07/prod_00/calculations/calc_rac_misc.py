from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator

class CalcRacMisc(IPCalculator):

    def calc_wifirfselect_reg(self, model):
        modulator_select = model.vars.modulator_select.value
        rf_path = model.vars.rf_path.value
        do_not_care = (modulator_select != model.vars.modulator_select.var_enum.IQ_MOD or rf_path == model.vars.rf_path.var_enum.LPW)

        if do_not_care is True:
            self._ip_reg_write(model, 'RFMUX_WIFIRFSELECT', 0)
        else:
            self._ip_reg_write(model, 'RFMUX_WIFIRFSELECT', 1)

#        self._ip_reg_write(model, 'CTRL_BTCENABLE', 0, do_not_care=True)

    def calc_demodclkdis_reg(self, model):
        self._ip_reg_write(model, 'DEMODCLKDIS_STATEOFFDEMODCLKDIS', 0)
        self._ip_reg_write(model, 'DEMODCLKDIS_STATERXWARMDEMODCLKDIS', 0)
        self._ip_reg_write(model, 'DEMODCLKDIS_STATERXSEARCHDEMODCLKDIS', 0)
        self._ip_reg_write(model, 'DEMODCLKDIS_STATERXFRAMEDEMODCLKDIS', 0)
        self._ip_reg_write(model, 'DEMODCLKDIS_STATERXWRAPUPDEMODCLKDIS', 0)
        self._ip_reg_write(model, 'DEMODCLKDIS_STATETXWARMDEMODCLKDIS', 0)
        self._ip_reg_write(model, 'DEMODCLKDIS_STATETXDEMODCLKDIS', 0)
        self._ip_reg_write(model, 'DEMODCLKDIS_STATESHUTDOWNDEMODCLKDIS', 0)
        self._ip_reg_write(model, 'DEMODCLKDIS_STATETXWRAPUPDEMODCLKDIS', 0)


    def calc_lpwmodemsel_reg(self, model):
        is_btc = (model.vars.demod_select.value == model.vars.demod_select.var_enum.BTC)
        is_hdt = (model.vars.demod_select.value == model.vars.demod_select.var_enum.HDT)

        if is_btc:
            lpwmodemsel = 1
        elif is_hdt:
            lpwmodemsel = 2
        else:
            lpwmodemsel = 0

        self._ip_reg_write(model, 'MODEMSEL_LPWMODEMSEL',lpwmodemsel)