from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator

class CalcBer(IPCalculator):

    # Method name: calc_ber_forces
    # Defined in: common\calculators\calc_ber.py
    def calc_ber_forces(self, model):
        if model.vars.test_ber.value == True:
            model.vars.ber_force_fdm0.value = True
            model.vars.ber_force_sync.value = True
            model.vars.ber_force_bitorder.value = True
            model.vars.ber_force_whitening.value = True
            model.vars.ber_force_infinite_length.value = True
            model.vars.ber_force_freq_comp_off.value = True

        else:
            model.vars.ber_force_fdm0.value = False
            model.vars.ber_force_sync.value = False
            model.vars.ber_force_bitorder.value = False
            model.vars.ber_force_whitening.value = False
            model.vars.ber_force_infinite_length.value = False
            model.vars.ber_force_freq_comp_off.value = False

    # Method name: calc_per_forces
    # Defined in: ocelot\calculators\calc_ber.py
    def calc_per_forces(self, model):
        # This function doesn't do anything anyways, so override with nothing
        pass

    # Method name: calc_test_ber
    # Defined in: ocelot\calculators\calc_ber.py
    def calc_test_ber(self, model):
        # This function sets a default value for the test_ber input
        # Set default value
        model.vars.test_ber.value = False