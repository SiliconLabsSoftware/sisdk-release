from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcLpwSynthMisc(IPCalculator):

    def calc_synth_misc(self, model):
        # : TODO FIX ME! Following register values are not being calculated.
        self._ip_reg_write_default(model, 'DSMCTRLTX_DITHERDACTX')
        self._ip_reg_write_default(model, 'DSMCTRLRX_DITHERDACRX')
        self._ip_reg_write_default(model, 'DSMCTRLRX_REQORDERRX')
        self._ip_reg_write_default(model, 'DSMCTRLTX_PHISELTX')
        self._ip_reg_write_default(model, 'DSMCTRLTX_REQORDERTX')
        self._ip_reg_write_default(model, 'QNCCTRL_QNCOFFSET')
        self._ip_reg_write_default(model, 'CTRL_GLMSOVERRIDEEN')
        self._ip_reg_write_default(model, 'CTRL_PLMSOVERRIDEEN')
        self._ip_reg_write_default(model, 'LMSOVERRIDE_PLMSOVERRIDEVAL')

        self._ip_reg_write_default(model, 'DSMCTRLTX_GLMSOVERRIDEVALTX')
        self._ip_reg_write_default(model, 'DSMCTRLTX_QNCMODETX')
        self._ip_reg_write_default(model, 'HOPPING_HCAPRETIMEEN')