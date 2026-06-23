from pyradioconfig.modules.lpw.blehdt.r_00.prod_00.calculations.calc_blehdt import CalcBlehdtMisc
from pyradioconfig.modules.lpw.blehdt.r_00.prod_00.reg_fields import BlehdtRegFields
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from enum import Enum

class CalcBlehdt_r00(CalcBlehdtMisc):

    def __init__(self, peripheral_name='BLEHDT'):
        self._reg_field_list = BlehdtRegFields().reg_field_list
        super().__init__(peripheral_name=peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)

        self._addModelVariable(model, 'hdt_do_not_care', bool, ModelVariableFormat.BINARY,
                               desc='Enable dont care for HADM')