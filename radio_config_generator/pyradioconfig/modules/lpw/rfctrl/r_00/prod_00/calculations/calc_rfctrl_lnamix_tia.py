from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcRfctrlLnamixTia(IPCalculator):

    def calc_tiaenlatch_reg(self, model):
        self._ip_reg_write(model,'TIAEN_TIAENLATCHI', 1)
        self._ip_reg_write(model,'TIAEN_TIAENLATCHQ', 1)

    def calc_ifpkdthr_reg(self, model):
        self._ip_reg_write(model,'TIACTRL1_TIATHRPKDHISEL', 6)
        self._ip_reg_write(model,'TIACTRL1_TIATHRPKDLOSEL', 2)

    def calc_rfpkdthr_reg(self, model):
        self._ip_reg_write(model,'LNAMIXCTRL1_LNAMIXRFPKDTHRESHSELHI', 3)
        self._ip_reg_write(model,'LNAMIXCTRL1_LNAMIXRFPKDTHRESHSELLO', 1)

    # Method name: calc_mxrlosel_reg
    # Defined in: lpwh72000\calculators\calc_radio.py
    def calc_mxrlosel_reg(self, model):
        # rx_rdm_state = model.vars.rx_rdm_state.value
        #
        # # Default to 0, poke to 1 in HADM PHYs
        # if rx_rdm_state in [model.vars.rx_rdm_state.var_enum.RX_HADM_RFPKD, model.vars.rx_rdm_state.var_enum.RX_HADM]:
        #     self._ip_reg_write(model,'LNAMIXEN1_LNAMIXMXRLOSEL', 1)
        # else:
        #     self._ip_reg_write(model,'LNAMIXEN1_LNAMIXMXRLOSEL', 0)
        pass
