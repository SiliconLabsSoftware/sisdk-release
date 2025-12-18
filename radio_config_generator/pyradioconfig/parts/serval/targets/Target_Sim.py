import os

from pyradioconfig.calculator_model_framework.interfaces.itarget import ITarget
from pyradioconfig.calculator_model_framework.decorators.target_decorators import skip_target_calc


class Target_Sim_Serval(ITarget):

    _targetName = "Sim"
    _description = "Supports the wired FPGA and other targets of sim PHYs"
    _store_config_output = True
    _cfg_location = os.path.join('target_sim', 'serval')
    _tag = "SIM"

    @skip_target_calc
    def target_calculate(self, model):
        # Always use fixed length in sim results
        model.vars.frame_length_type.value_forced = model.vars.frame_length_type.var_enum.FIXED_LENGTH
