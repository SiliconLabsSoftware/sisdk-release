from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException


class CalcBtcphyBrvitdemod(IPCalculator):

    def calc_btc_misc(self, model):
        demod_select = model.vars.demod_select.value

        value_do_not_care = demod_select != model.vars.demod_select.var_enum.BTC

        self._ip_reg_write(model, 'BRVITDEMOD_VITERBIKSI1', 260, do_not_care=value_do_not_care)
        self._ip_reg_write(model, 'BRVITDEMOD_VITERBIKSI2', 180, do_not_care=value_do_not_care)
        self._ip_reg_write(model, 'BRVITDEMOD_VITERBIKSI3', 110, do_not_care=value_do_not_care)
        self._ip_reg_write(model, 'CTRL3_TXPOLAREN', 0, do_not_care=value_do_not_care)
        # https://jira.silabs.com/browse/MCUW_RADIO_CFG-3489
        self._ip_reg_write(model, 'EDR_TX_GUARD3_EDRGUARDTX', 0x6, do_not_care=value_do_not_care)

    ### https://jira.silabs.com/browse/MCUW_RADIO_CFG-2737
    def calc_fbafcgain_reg(self, model):
        digmix_res = model.vars.digmix_res_actual.value

        fbafcgain = int(8 * 1e6 / 1608 / digmix_res)
        if 0 < fbafcgain < 4096:
            self._ip_reg_write(model, 'FREQ_COMP_FBAFCGAIN', fbafcgain)
        else:
            raise CalculationException('FBAFCGAIN Overflow (12 bits) !')