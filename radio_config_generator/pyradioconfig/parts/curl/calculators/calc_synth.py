from pyradioconfig.parts.lion.calculators.calc_synth import CalcSynthLion
from pycalcmodel.core.variable import ModelVariableFormat

class CalcSynthCurl(CalcSynthLion):

    def buildVariables(self, model):
        self._addModelVariable(model, 'adc_constrain_xomult', bool, ModelVariableFormat.DECIMAL,
                               desc='Flag used internally to constrain ADC clock to multiple of HFXO')

        super().buildVariables(model)

    def calc_adc_vco_div(self, model):
        adc_rate_mode_actual = model.vars.adc_rate_mode_actual.value

        if adc_rate_mode_actual == model.vars.adc_rate_mode.var_enum.FULLRATE:
            adc_vco_div = 8
        elif adc_rate_mode_actual == model.vars.adc_rate_mode.var_enum.HALFRATE:
            adc_vco_div = 16
        else:
            adc_vco_div = 32

        model.vars.adc_vco_div.value = adc_vco_div

    def calc_clkmulten_reg(self, model):
        super().calc_clkmulten_reg(model)
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value

        # regulators set to max voltage, current for hot temp performance EFRPTE-6618
        # Bypass Lion regvals due to MCUW_RADIO_CFG-3308
        if adc_clock_mode_actual == model.vars.adc_clock_mode.var_enum.HFXOMULT:
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTREG1ADJV, 3)
            # self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTREG2ADJV, 3)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTREG2ADJI, 3)
            self._reg_write(model.vars.RAC_CLKMULTEN0_CLKMULTREG3ADJV, 3)