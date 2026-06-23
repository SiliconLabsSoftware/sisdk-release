from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcAgcMode(IPCalculator):
    def calc_agc_mode_reg(self, model):

        demod_sel = model.vars.demod_select.value
        preamsch = model.vars.MODEM_TRECPMDET_PREAMSCH.value

        # we like AGC to freeze once timing is detected (MODE=1) to avoid AGC changes while receiving data
        # the only exception to this is the case where we are directly searching for the sync word when using Viterbi
        # Or using BLE Longrange demod path,
        # in this case we need to set the MODE=2 to freeze the AGC when frame is detected
        if (
                demod_sel == model.vars.demod_select.var_enum.TRECS_VITERBI or demod_sel == model.vars.demod_select.var_enum.TRECS_SLICER):
            if preamsch:
                mode = 1
            else:
                mode = 2
        elif demod_sel == model.vars.demod_select.var_enum.LONGRANGE:
            mode = 2
        else:
            mode = 1

        self._ip_reg_write(model, 'CTRL0_MODE', mode)

    def calc_agc_decision_matrix_reg(self, model):
        dualrfpkddec_val = 240296
        self._ip_reg_write(model, 'CTRL6_DUALRFPKDDEC', dualrfpkddec_val)

    def calc_agc_rfpkd_enable(self, model):
        model.vars.rfpkd_mode.value = model.vars.rfpkd_mode.var_enum.DUAL  # Set default RFPKD dual mode
        rfpkd_mode = model.vars.rfpkd_mode.value

        if rfpkd_mode == model.vars.rfpkd_mode.var_enum.DUAL:
            disrfpkd = 0
            rfpkdcnten = 1
            rfpkdsel = 1
            rfpkdsyncsel = 1
            endualrfpkd = 1
        else:
            disrfpkd = 1
            rfpkdcnten = 0
            rfpkdsel = 0
            rfpkdsyncsel = 0
            endualrfpkd = 0

        self._ip_reg_write(model, 'CTRL2_DISRFPKD', disrfpkd)
        self._ip_reg_write(model, 'CTRL4_RFPKDCNTEN', rfpkdcnten)
        self._ip_reg_write(model, 'CTRL4_RFPKDSEL', rfpkdsel)
        self._ip_reg_write(model, 'CTRL4_RFPKDSYNCSEL', rfpkdsyncsel)
        self._ip_reg_write(model, 'CTRL6_ENDUALRFPKD', endualrfpkd)
