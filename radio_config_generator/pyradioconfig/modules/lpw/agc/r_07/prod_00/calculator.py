from enum import Enum

from pycalcmodel.core.variable import CreateModelVariableEnum, ModelVariableFormat

from pyradioconfig.modules.lpw.agc.r_07.prod_00.calculations.calc_agc_gain import CalcAgcGain
from pyradioconfig.modules.lpw.agc.r_07.prod_00.calculations.calc_agc_misc import CalcAgcMisc
from pyradioconfig.modules.lpw.agc.r_07.prod_00.calculations.calc_agc_mode import CalcAgcMode
from pyradioconfig.modules.lpw.agc.r_07.prod_00.calculations.calc_agc_response import CalcAgcResponse
from pyradioconfig.modules.lpw.agc.r_07.prod_00.calculations.calc_agc_rssi import CalcAgcRssi
from pyradioconfig.modules.lpw.agc.r_07.prod_00.reg_fields import AgcRegFields


class CalcAgc_r07(CalcAgcGain, CalcAgcMisc, CalcAgcMode, CalcAgcResponse, CalcAgcRssi):

    def __init__(self, peripheral_name='AGC'):
        self._reg_field_list = AgcRegFields().reg_field_list
        super().__init__(peripheral_name=peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)
        self._addModelActual(model, 'rssi_access_time_us', float, ModelVariableFormat.DECIMAL,
                             desc='Actual RSSI access time [us] after demod enable')
        self._addModelActual(model, 'cfloopdel_us', float, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'agcperiod', float, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'rssi_period_sym', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'agc_settling_delay', int, ModelVariableFormat.DECIMAL,
                               desc='Delay between two AGC gain adjustments in AGC clock cycles')
        self._addModelVariable(model, 'agc_clock_cycle', float, ModelVariableFormat.DECIMAL)

        var = self._addModelVariable(model, 'agc_speed', Enum, ModelVariableFormat.DECIMAL, 'AGC Speed')
        member_data = [
            ['NORMAL', 0, 'Recommended default setting'],
            ['FAST', 1, 'Aggressive AGC setting'],
            ['SLOW', 2, 'Slow AGC setting'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'AgcMode',
            'List of supported AGC Speed Modes',
            member_data)

        var = self._addModelVariable(model, 'agc_power_mode', Enum, ModelVariableFormat.DECIMAL, 'AGC power mode')
        member_data = [
            ['HP', 0, 'AGC High Performance Mode'],
            ['LP', 1, 'AGC Low Power Mode'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'AgcPowerMode',
            'List of supported AGC Lock Modes',
            member_data)

        var = self._addModelVariable(model, 'rfpkd_mode', Enum, ModelVariableFormat.DECIMAL, 'RF Peak Detector Mode')
        member_data = [
            ['DISABLE', 0, 'RFPKD Disabled'],
            ['DUAL', 1, 'Dual RFPKD mode'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'RfPeakDetectorMode',
            'List of supported RF Peak Detector Modes',
            member_data)