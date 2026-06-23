from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
from pyradioconfig.parts.common.calculators.calc_utilities import CALC_Utilities
from pyradioconfig.parts.common.calculators.calc_frame_detect import CALC_Frame_Detect as CALC_Frame_Detect_Common
from math import ceil, floor, log
from py_2_and_3_compatibility import *
import numpy as np
from pyradioconfig.parts.common.utils.tinynumpy import tinynumpy


class CalcDac(IPCalculator):
    ### https://jira.silabs.com/browse/MCUW_RADIO_CFG-2737
    def calc_dac_freq_mod_reg(self, model):
        dac_clock_mode = model.vars.dac_clock_mode.value

        if dac_clock_mode in (model.vars.dac_clock_mode.var_enum.DISABLED,
                              model.vars.dac_clock_mode.var_enum.HFXO):
            dac_freq_val = 0
        elif dac_clock_mode == model.vars.dac_clock_mode.var_enum.HFXOx2:
            dac_freq_val = 1
        elif dac_clock_mode == model.vars.dac_clock_mode.var_enum.HFXOx4:
            dac_freq_val = 2
        else:
            raise CalculationException('Unsupported DAC clock mode for DAC frequency register calculation')

        self._ip_reg_write(model, 'TXCTRL_TXDACFREQ', dac_freq_val)

    ### https://jira.silabs.com/browse/MCUW_RADIO_CFG-2737
    ### https://jira.silabs.com/browse/MCUW_RADIO_CFG-2667
    def calc_dac_sel_mod_reg(self, model):
        rfsel = model.vars.rf_path.value
        modsel = model.vars.modulator_select.value

        # Jira MCUW_RADIO_CFG-2667: according to information from P. Blouin, the table to implement is the following:
        #   ________________________________________________________________________________________________
        #   | rf_path   | modulator_select  | TXDACSEL  | DAC_FREQ(default) | PHYs
        #   |-----------------------------------------------------------------------------------------------
        #   |           |   PHMOD           |   NA(0)   |   NA(0)           | PHYs BLE, 15.4, FSK * _phmod
        #   | LPW       |   IQMOD           |   0       |   0               | PHYs BLE, 15.4, FSK * _iqmod
        #   |           |   IQMOD_ *        |   1       |   1               | PHYs BTC, HDT
        #   |------------------------------------------------------------------------------------------------
        #   |           |   PHMOD           |   NA      |   NA              |
        #   | WIFI      |   IQMOD           |   2       |   2               | PHYs BLE, 15.4, FSK _iqmod
        #   |           |   IQMOD_ *        |   2       |   2               | PHYs BTC, HDT
        #   |------------------------------------------------------------------------------------------------

        if rfsel == model.vars.rf_path.var_enum.LPW:
            if modsel == model.vars.modulator_select.var_enum.PH_MOD or \
                    modsel == model.vars.modulator_select.var_enum.IQ_MOD:    # Modulator is on the synthetiser or IQ Mod BLE
                dacsel = 0
            elif modsel == model.vars.modulator_select.var_enum.IQ_MOD_DIRECT: # IQ Modulator
                dacsel = 1
            else:
                raise CalculationException('Unknown modulator configuration on LPW rf path')
        elif rfsel == model.vars.rf_path.var_enum.WIFI:
            if modsel == model.vars.modulator_select.var_enum.IQ_MOD or \
                    modsel == model.vars.modulator_select.var_enum.IQ_MOD_DIRECT: # IQ Modulator on WiFi RF
                dacsel = 2
            else:
                raise CalculationException('Unknown modulator configuration on Wifi rf path')
        else:
            raise CalculationException('Unknown RF selection path')

        self._ip_reg_write(model, 'TXCTRL_TXDACSEL', dacsel)

    # Method name: calc_dac_clock_mode
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_dac_clock_mode(self, model):
        '''
        MCUW_RAIO_CFG-2988:
        If PHY is for Pegasus,
            * BLE+other PHYs when using IQMOD: DAC_clk_freq = XTAL_freq
            * BTC/HDT when IQMOD (or I should say IQMOD Direct): DAC_clk_freq = 2 x XTAL_freq

        If PHY is for Corvus,
            * all PHYs must set DAC_clk_freq = 4 x XTAL_freq
        '''
        modulator_select = model.vars.modulator_select.value
        rf_path = model.vars.rf_path.value

        if rf_path == model.vars.rf_path.var_enum.WIFI:
            model.vars.dac_clock_mode.value = model.vars.dac_clock_mode.var_enum.HFXOx4
        elif rf_path == model.vars.rf_path.var_enum.LPW:
            if modulator_select == model.vars.modulator_select.var_enum.PH_MOD:
                model.vars.dac_clock_mode.value = model.vars.dac_clock_mode.var_enum.DISABLED
            elif modulator_select == model.vars.modulator_select.var_enum.IQ_MOD:
                # this is for BLE, 15.4, FSK
                model.vars.dac_clock_mode.value = model.vars.dac_clock_mode.var_enum.HFXO
            elif modulator_select == model.vars.modulator_select.var_enum.IQ_MOD_DIRECT:
                # this is for BTC, HDT
                model.vars.dac_clock_mode.value = model.vars.dac_clock_mode.var_enum.HFXOx2
            else:
                raise CalculationException('Unknown modulator select configuration on LPW rf path')
        else:
            raise CalculationException('Unsupported RF path for DAC clock mode calculation')