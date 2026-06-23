from pyradioconfig.modules.lpw.hadm.r_02.lpw74010.calculations.calc_hadm import CalcHadmMisc
from enum import Enum
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from pyradioconfig.modules.lpw.hadm.r_02.lpw74010.reg_fields import HadmRegFields

class CalcHADM_r02(CalcHadmMisc):

    def __init__(self, peripheral_name='HADM'):
        self._reg_field_list = HadmRegFields().reg_field_list
        super().__init__(peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)
        var = self._addModelVariable(model, 'hadm_enable', Enum, ModelVariableFormat.DECIMAL, units='',
                               desc='Enables HADM settings')

        member_data = [
            ['DISABLED', 0, 'HADM Disabled'],
            ['ENABLED', 1, 'HADM Enabled'],
        ]

        var.var_enum = CreateModelVariableEnum(
            'HADMEnableEnum',
            'HADM Enable/Disable Selection',
            member_data)

        self._addModelVariable(model, 'hadm_do_not_care', bool, ModelVariableFormat.BINARY,
                               desc='Enable dont care for HADM')