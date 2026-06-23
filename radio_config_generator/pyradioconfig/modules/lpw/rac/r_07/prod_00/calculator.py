from enum import Enum
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from pyradioconfig.modules.lpw.rac.r_07.prod_00.calculations.calc_rac_misc import CalcRacMisc
from pyradioconfig.modules.lpw.rac.r_07.prod_00.reg_fields import RacRegFields
from py_2_and_3_compatibility import *


class CalcRac_r07(CalcRacMisc):

    def __init__(self, peripheral_name='RAC'):
        self._reg_field_list = RacRegFields().reg_field_list
        super().__init__(peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)
