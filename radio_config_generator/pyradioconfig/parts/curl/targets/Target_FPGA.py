from pyradioconfig.calculator_model_framework.interfaces.itarget import ITarget
from os.path import join
from pyradioconfig.calculator_model_framework.CalcManager import CalcManager
from copy import deepcopy


class Target_FPGA_Curl(ITarget):

    _targetName = "FPGA"
    _description = "Supports the OTA FPGA"
    _store_config_output = False
    _cfg_location = join('target_fpga','curl')
    _tag = "FPGA"

    def target_calculate(self, model):

        #FPGA can only run in full rate mode
        model.vars.adc_rate_mode.value_forced = model.vars.adc_rate_mode.var_enum.FULLRATE
        model.vars.adc_clock_mode.value_forced = model.vars.adc_clock_mode.var_enum.HFXOMULT

        # Use Zero-IF
        model.vars.if_frequency_hz.value_forced = 0

        #Disable IQ swap
        model.vars.MODEM_MIXCTRL_DIGIQSWAPEN.value_forced = 0

        #Disable DCCOMP
        model.vars.MODEM_DCCOMP_DCCOMPEN.value_forced = 0

        #38.4 MHz XO Frequency
        model.vars.xtal_frequency_hz.value_forced = int(38.4e6)

        # MCUW_RADIO_CFG-3330 - add shaping filter overrides

        # First, pre-calculate the PHY in IC target once to see model variables are set
        calc_manager = CalcManager(part_family=model.part_family, part_rev='ANY', target='IC')
        IC_model_instance_copy = deepcopy(model)
        IC_model_instance_copy.target = 'IC'
        calc_manager.calculate(IC_model_instance_copy)

        # : PHY-specific rules (to be replaced globally once we figure out how calculate where they need to apply)
        # : shaping filter specific overrides
        self.modem_shaping_overrides(model, IC_model_instance_copy)

    def modem_shaping_overrides(self, model, IC_model_instance_copy):

        # Usually BLE PHYs use PLL compensated shaping filters for Gaussian shapes. We need to override them for
        # FPGA target to use uncompensated shaping filter coefficient.
        if (
                IC_model_instance_copy.vars.shaping_filter.value == IC_model_instance_copy.vars.shaping_filter.var_enum.Gaussian
                and IC_model_instance_copy.vars.shaping_filter_param.value == 0.5
        ):
            # covers all BLE PHYs (including AOX, HADM and LR)
            self.GAUSSIAN_BT_0p5_MODEM_SHAPING_OVERRIDE(model)
        if (
                IC_model_instance_copy.vars.shaping_filter.value == IC_model_instance_copy.vars.shaping_filter.var_enum.Gaussian
                and float(IC_model_instance_copy.vars.shaping_filter_param.value) == 2.0
                and IC_model_instance_copy.vars.hadm_enable.value == IC_model_instance_copy.vars.hadm_enable.var_enum.ENABLED
        ):
            # covers the HADM 2BT case
            self.GAUSSIAN_BT_2_MODEM_SHAPING_OVERRIDE(model)
        return

    def modem_reg_override(self, model, register_name, override_value=None, disable_override=False):
        if disable_override:
            # just force the value_forced to be same as its value in profile_output.override
            # is profile_output.override = None, the value will be eventually set by calculator
            model.vars.get_var(register_name).value_forced = model.profile.outputs.get_output(register_name).override
        else:
            if override_value is None:
                print('Setting {0} as None'.format(register_name))
            else:
                model.vars.get_var(register_name).value_forced = override_value

    def GAUSSIAN_BT_0p5_MODEM_SHAPING_OVERRIDE(self, model, disable_override=False):
        # this shaping coeff give uncompensated Gaussian Shape with BT = 0.5
        # these coeffs are what radio calculator generated for given shaping_filter and shaping_filter_param
        # using more taps here now because of MCUW_RADIO_CFG-3073

        self.modem_reg_override(model, 'MODEM_CTRL0_SHAPING', 3, disable_override)

        self.modem_reg_override(model, 'MODEM_SHAPING0_COEFF0', 1, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING0_COEFF1', 2, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING0_COEFF2', 6, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING0_COEFF3', 15, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING1_COEFF4', 30, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING1_COEFF5', 51, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING1_COEFF6', 76, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING1_COEFF7', 97, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING2_COEFF8', 112, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING2_COEFF9', 119, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING2_COEFF10', 119, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING2_COEFF11', 112, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING3_COEFF12', 97, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING3_COEFF13', 76, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING3_COEFF14', 51, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING3_COEFF15', 30, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING4_COEFF16', 15, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING4_COEFF17', 6, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING4_COEFF18', 2, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING4_COEFF19', 1, disable_override)

        # override other shaping coeff to zero
        self.modem_reg_override(model, 'MODEM_SHAPING5_COEFF20', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING5_COEFF21', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING5_COEFF22', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING5_COEFF23', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING6_COEFF24', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING6_COEFF25', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING6_COEFF26', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING6_COEFF27', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING7_COEFF28', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING7_COEFF29', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING7_COEFF30', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING7_COEFF31', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING8_COEFF32', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING8_COEFF33', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING8_COEFF34', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING8_COEFF35', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING9_COEFF36', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING9_COEFF37', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING9_COEFF38', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING9_COEFF39', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING10_COEFF40', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING10_COEFF41', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING10_COEFF42', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING10_COEFF43', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING11_COEFF44', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING11_COEFF45', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING11_COEFF46', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING11_COEFF47', 0, disable_override)

    def GAUSSIAN_BT_2_MODEM_SHAPING_OVERRIDE(self, model, disable_override=False):
        # this shaping coeff give uncompensated Gaussian Shape with BT = 2.0
        # these coeffs are what radio calculator generated for given shaping_filter and shaping_filter_param
        # using more taps here now because of MCUW_RADIO_CFG-3073

        self.modem_reg_override(model, 'MODEM_CTRL0_SHAPING', 3, disable_override)

        self.modem_reg_override(model, 'MODEM_SHAPING0_COEFF0', 16, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING0_COEFF1', 111, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING0_COEFF2', 127, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING0_COEFF3', 127, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING1_COEFF4', 127, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING1_COEFF5', 127, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING1_COEFF6', 127, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING1_COEFF7', 127, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING2_COEFF8', 111, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING2_COEFF9', 16, disable_override)
        # override other shaping coeff to zero
        self.modem_reg_override(model, 'MODEM_SHAPING2_COEFF10', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING2_COEFF11', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING3_COEFF12', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING3_COEFF13', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING3_COEFF14', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING3_COEFF15', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING4_COEFF16', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING4_COEFF17', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING4_COEFF18', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING4_COEFF19', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING5_COEFF20', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING5_COEFF21', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING5_COEFF22', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING5_COEFF23', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING6_COEFF24', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING6_COEFF25', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING6_COEFF26', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING6_COEFF27', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING7_COEFF28', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING7_COEFF29', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING7_COEFF30', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING7_COEFF31', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING8_COEFF32', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING8_COEFF33', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING8_COEFF34', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING8_COEFF35', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING9_COEFF36', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING9_COEFF37', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING9_COEFF38', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING9_COEFF39', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING10_COEFF40', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING10_COEFF41', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING10_COEFF42', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING10_COEFF43', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING11_COEFF44', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING11_COEFF45', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING11_COEFF46', 0, disable_override)
        self.modem_reg_override(model, 'MODEM_SHAPING11_COEFF47', 0, disable_override)