from pyradioconfig.modules.lpw.fefilt.r_03.prod_00.calculations.calc_fefilt_misc import CalcFefiltMisc
from pyradioconfig.modules.lpw.fefilt.r_03.prod_00.calculations.calc_fefilt_xo_spur_canceller import CalcXOSpurCanceller
from pyradioconfig.modules.lpw.fefilt.r_03.prod_00.calculations.calc_fefilt_rx import CalcFefiltRX
from pyradioconfig.modules.lpw.fefilt.r_03.prod_00.calculations.calc_fefilt_chf import CalcFefiltCHF
from pyradioconfig.modules.lpw.fefilt.r_03.prod_00.calculations.calc_fefilt_rssi import CalcFefiltRSSI
from enum import Enum
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from pyradioconfig.modules.lpw.fefilt.r_03.prod_00.reg_fields import FefiltRegFields

class CalcFefilt_r03(CalcFefiltMisc, CalcXOSpurCanceller, CalcFefiltRX, CalcFefiltCHF, CalcFefiltRSSI):

    def __init__(self, peripheral_name='FEFILT'):
        self._reg_field_list = FefiltRegFields().reg_field_list
        super().__init__(peripheral_name=peripheral_name)  # Specifies prefix for all reg fields in this IP calculator


    def buildVariables(self, model):
        super().buildVariables(model)

        # Add new model vars
        self._addModelVariable(model, 'spurcancel0_freq', int, ModelVariableFormat.DECIMAL,
                               'Spur canceller 0 frequency in Hz')
        self._addModelVariable(model, 'spurcancel1_freq', int, ModelVariableFormat.DECIMAL,
                               'Spur canceller 1 frequency in Hz')
        spurcancel0_mode_var = self._addModelVariable(model, 'spurcancel0_mode', Enum, ModelVariableFormat.DECIMAL,
                                     'Spur canceller 0 mode')
        spurcancel1_mode_var = self._addModelVariable(model, 'spurcancel1_mode', Enum, ModelVariableFormat.DECIMAL,
                                                      'Spur canceller 1 mode')
        member_data = [
            ['DISABLED', 0, 'Disabled'],
            ['CANCEL', 1, 'Estimate the spur amplitude and phase and cancel'],
            ['MEAS', 2, 'Estimate the spur only']
        ]
        spurcancel_mode_enum = CreateModelVariableEnum(
            'SpurCancellerModeEnum',
            'Select spur canceller mode',
            member_data)

        spurcancel0_mode_var.var_enum = spurcancel_mode_enum
        spurcancel1_mode_var.var_enum = spurcancel_mode_enum

        self._addModelActual(model, 'chflatency', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'channel_filter_coeffs_lock_bwsel', int, ModelVariableFormat.DECIMAL,
                               is_array=True, desc='Channel filter coeffs for lock bandwidth selection')
        self._addModelVariable(model, 'channel_filter_coeffs_acq_bwsel', int, ModelVariableFormat.DECIMAL,
                               is_array=True, desc='Channel filter coeffs for acquisition bandwidth selection')



        # rssi
        self._addModelVariable(model, 'rssi_adjust_db', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'rssi_dig_adjust_db', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'rssi_rf_adjust_db', float, ModelVariableFormat.DECIMAL)

        """
        Demodulator
        """
        # IQ/freq signals generated from FEFILT go into various demods. Hence, demod selection should happen at FEFILT IP
        self._addModelVariable(model, 'demod_select', Enum, ModelVariableFormat.DECIMAL)
        model.vars.demod_select.var_enum = CreateModelVariableEnum(
            enum_name='DemodSelectEnum',
            enum_desc='Demod Selection',
            member_data=[
                ['LEGACY', 0, 'Legacy Demod'],
                ['COHERENT', 1, 'Coherent Demod'],
                ['TRECS_VITERBI', 2, 'TRecS + Viterbi Demod'],
                ['TRECS_SLICER', 3, 'TRecS + HD Demod'],
                ['BCR', 4, 'PRO2 BCR Demod'],
                ['LONGRANGE', 5, 'BLE Long Range Demod'],
                ['ENHANCED_DSSS', 6, 'Enhanced OQPSK+DSSS Demod'],
                ['BTC', 7, 'Bluetooth Classic Demod'],
                ['HDT', 8, 'BLE Higher Data Rate Demod']
            ])
        self._addModelActual(model, 'demod_rate', float, ModelVariableFormat.DECIMAL)
        # rainier
        self._addModelVariable(model, 'synchronous_ifadc_clk', bool, ModelVariableFormat.DECIMAL,
                               desc='Flag used treat ifadc_clk as synchronous to clk_demod and bypass afifo')

    #todo: add dec model variables