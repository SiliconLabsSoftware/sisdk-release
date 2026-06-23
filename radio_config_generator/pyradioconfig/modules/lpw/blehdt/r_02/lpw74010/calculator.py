from pyradioconfig.modules.lpw.blehdt.r_02.lpw74010.calculations.calc_blehdt import CalcBlehdtMisc
from pyradioconfig.modules.lpw.blehdt.r_02.lpw74010.reg_fields import BlehdtRegFields
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from enum import Enum

class CalcBlehdt_r02(CalcBlehdtMisc):

    def __init__(self, peripheral_name='BLEHDT'):
        self._reg_field_list = BlehdtRegFields().reg_field_list
        super().__init__(peripheral_name=peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)

        self._addModelVariable(model, 'hdt_do_not_care', bool, ModelVariableFormat.BINARY,
                               desc='Enable dont care for HADM')