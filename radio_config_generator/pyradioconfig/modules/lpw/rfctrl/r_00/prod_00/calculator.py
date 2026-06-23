from pyradioconfig.modules.lpw.rfctrl.r_00.prod_00.calculations.calc_rfctrl_adc import CalcRfctrlAdc
from pyradioconfig.modules.lpw.rfctrl.r_00.prod_00.calculations.calc_rfctrl_synth import CalcRfctrlSynth
from pyradioconfig.modules.lpw.rfctrl.r_00.prod_00.calculations.calc_rfctrl_lnamix_tia import CalcRfctrlLnamixTia
from pyradioconfig.modules.lpw.rfctrl.r_00.prod_00.calculations.calc_rfctrl_clkmult import CalcRfctrlClkmult
from pyradioconfig.modules.lpw.rfctrl.r_00.prod_00.calculations.calc_rfctrl_misc import CalcRadioMisc
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from pyradioconfig.modules.lpw.rfctrl.r_00.prod_00.reg_fields import RfctrlRegFields
from enum import Enum


class CalcRfctrl_r00(CalcRfctrlAdc, CalcRfctrlClkmult, CalcRfctrlSynth, CalcRfctrlLnamixTia, CalcRadioMisc):

    def __init__(self, peripheral_name='RFCTRL'):
        self._reg_field_list = RfctrlRegFields().reg_field_list
        super().__init__(peripheral_name=peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)
        """Populates a list of needed variables for this calculator
        Args:
            model (ModelRoot) : Builds the variables specific to this calculator
        """
        #TODO: check if these are being used anywhere in calculator?
        # self._addModelVariable(model,  'synth_lpfbw',  int,          ModelVariableFormat.DECIMAL)
        var = self._addModelVariable(model, 'pll_bandwidth_rx', Enum, ModelVariableFormat.DECIMAL,
                                     'PLL bandwidth in KHz in RX')
        member_data = [
            ['BW_100KHz', 0, 'PLL loop filter bandwidth is approximately 100 KHz'],
            ['BW_150KHz', 1, 'PLL loop filter bandwidth is approximately 150 KHz'],
            ['BW_200KHz', 2, 'PLL loop filter bandwidth is approximately 200 KHz'],
            ['BW_250KHz', 3, 'PLL loop filter bandwidth is approximately 250 KHz'],
            ['BW_300KHz', 6, 'PLL loop filter bandwidth is approximately 300 KHz'],
            ['FASTSWITCH', 7, 'PLL loop filter bandwidth setting for 802154 fast switching'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'PLLBandwdithEnum',
            'List of supported PLL bandwidth settings',
            member_data)
        var = self._addModelVariable(model, 'pll_bandwidth_tx', Enum, ModelVariableFormat.DECIMAL,
                                     'PLL bandwidth in KHz in TX')
        member_data = [
            ['BW_750KHz', 0, 'PLL loop filter bandwidth is approximately 750 KHz'],
            ['BW_1000KHz', 1, 'PLL loop filter bandwidth is approximately 1000 KHz'],
            ['BW_1200KHz', 2, 'PLL loop filter bandwidth is approximately 1200 KHz'],
            ['BW_1500KHz', 3, 'PLL loop filter bandwidth is approximately 1500 KHz'],
            ['BW_2000KHz', 6, 'PLL loop filter bandwidth is approximately 2000 KHz'],
            ['BW_2500KHz', 7, 'PLL loop filter bandwidth is approximately 2500 KHz'],
            ['BW_3000KHz', 8, 'PLL loop filter bandwidth is approximately 3000 KHz'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'PLLBandwdithEnum',
            'List of supported PLL bandwidth settings',
            member_data)
        self._addModelVariable(model, 'pll_bandwidth_miracle_mode', bool, ModelVariableFormat.ASCII,
                               'Set to force the synth pll into miracle mode (whatever that means).')

        self._addModelVariable(model, 'adc_clock_mode', Enum, ModelVariableFormat.DECIMAL)
        model.vars.adc_clock_mode.var_enum = CreateModelVariableEnum(
            enum_name = 'AdcClockModeEnum',
            enum_desc = 'Defines how the ADC clock is derived',
            member_data = [
                ['HFXOMULT',0,  'Multiply HFXO for ADC Clock'],
                ['VCODIV',   1,  'Divide VCO for ADC Clock'],
            ])
        self._addModelActual(model, 'adc_clock_mode', Enum, ModelVariableFormat.DECIMAL)
        model.vars.adc_clock_mode_actual.var_enum = model.vars.adc_clock_mode.var_enum

        self._addModelVariable(model, 'adc_target_freq', int, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'adc_vco_div', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'adc_vco_div', int, ModelVariableFormat.DECIMAL)
