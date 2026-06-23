from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcRfctrlSynth(IPCalculator):

    def calc_synth_rfctrl_misc(self, model):
        self._ip_reg_write(model,'SYLOCTRL0_SYLODIVDSMDACCLKDIVRATIO', 0)     #RX 150MHz
        self._ip_reg_write(model,'SYLOCTRLTX0_SYLODIVDSMDACCLKDIVRATIOTX', 1) #TX 300MHz

    def calc_syctrl_reg(self, model):
        """
        Copied from Rainier
        """
        is_hadm = 'HADM' in model.vars.ble_feature.value.name.upper()

        if is_hadm:
            syvcotrimbiastx_val = 5
        else:
            syvcotrimbiastx_val = 4

        self._ip_reg_write(model, 'SYCTRL0_SYVCOTRIMIPTAT', 13)
        self._ip_reg_write(model, 'SYCTRLTX0_SYVCOTRIMIPTATTX', 13)

        self._ip_reg_write(model, 'SYCTRL0_SYVCOTRIMIBIAS', 4)
        self._ip_reg_write(model, 'SYCTRLTX0_SYVCOTRIMIBIASTX', syvcotrimbiastx_val)

        self._ip_reg_write(model, 'SYCTRL0_SYDSMDACTRIMLOADBALDLF', 4)
        self._ip_reg_write(model, 'SYCTRLTX0_SYDSMDACTRIMLOADBALDLFTX', 4)

        self._ip_reg_write(model, 'SYCTRL0_SYDSMDACTRIMLOADBALDSM', 2)

        self._ip_reg_write(model, 'SYCTRL0_SYENMMDREGREPLICA', 0)
        self._ip_reg_write(model, 'SYCTRLTX0_SYENMMDREGREPLICATX', 1)