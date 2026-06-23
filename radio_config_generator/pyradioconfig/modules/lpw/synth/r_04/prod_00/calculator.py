from pyradioconfig.modules.lpw.synth.r_04.prod_00.calculations.calc_lpw_synth import CalcLpwSynth
from pyradioconfig.modules.lpw.synth.r_04.prod_00.calculations.calc_lpw_synth_misc import CalcLpwSynthMisc
from py_2_and_3_compatibility import *
from enum import Enum
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from pyradioconfig.modules.lpw.synth.r_04.prod_00.reg_fields import SynthRegFields


class CalcSynth_r04(CalcLpwSynth, CalcLpwSynthMisc):

    def __init__(self, peripheral_name='SYNTH'):
        self._reg_field_list = SynthRegFields().reg_field_list
        super().__init__(peripheral_name=peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)
        self._addModelVariable(model, 'adc_constrain_xomult', bool, ModelVariableFormat.DECIMAL,
                               desc='Flag used internally to constrain ADC clock to multiple of HFXO')

        # : Modify tx synth modes from Bobcat
        self._addModelVariable(model, 'synth_tx_mode', Enum, ModelVariableFormat.DECIMAL)
        model.vars.synth_tx_mode.var_enum = CreateModelVariableEnum(
            enum_name='SynthTxModeEnum',
            enum_desc='Defined Synth TX Mode',
            member_data=[
                ['MODE1', 0, 'TX Mode 1'],  # 750KHz one side
                ['MODE2', 1, 'TX Mode 2'],  # 1MHZ, one side
                ['MODE3', 2, 'TX Mode 3'],  # 1.5MHZ, one side
                ['MODE4', 3, 'TX Mode 4'],  # 2.5MHz, one side
                ['MODE_IQMOD', 0, 'TX IQMOD Mode'],  # IQMOD
                ['MODE_BLE', 0, 'TX BLE Mode'],  # BLE1M
                ['MODE_BLE_FULLRATE', 4, 'TX BLE Fullrate Mode'],  # BLE2M
                ['MODE_IEEE802154', 2, 'TX IEEE802154 Mode'],  # Zigbee
            ])
        self._addModelActual(model, 'synth_tx_mode', Enum, ModelVariableFormat.DECIMAL)
        model.vars.synth_tx_mode_actual.var_enum = model.vars.synth_tx_mode.var_enum

        # : Modify synth RX modes from Ocelot
        self._addModelVariable(model, 'synth_rx_mode', Enum, ModelVariableFormat.DECIMAL)
        model.vars.synth_rx_mode.var_enum = CreateModelVariableEnum(
            enum_name='SynthRxModeEnum',
            enum_desc='Defined Synth RX Mode',
            member_data=[
                ['MODE1', 0, 'RX Mode 1'],
                ['MODE2', 1, 'RX Mode 2'],
                ['MODE_HOP', 2, 'RX Mode Hopping'],
            ])
        self._addModelActual(model, 'synth_rx_mode', Enum, ModelVariableFormat.DECIMAL)
        model.vars.synth_rx_mode_actual.var_enum = model.vars.synth_rx_mode.var_enum

        var = self._addModelVariable(model, 'hop_enable', Enum, ModelVariableFormat.DECIMAL, units='',
                                     desc='Enables Hopping')

        member_data = [
            ['DISABLED', 0, 'Hopping Disabled'],
            ['ENABLED', 1, 'Hopping Enabled'],
        ]

        var.var_enum = CreateModelVariableEnum(
            'HopEnableEnum',
            'HOP Enable/Disable Selection',
            member_data)

        # : Modify synth settling modes from Ocelot
        self._addModelVariable(model, 'synth_settling_mode', Enum, ModelVariableFormat.DECIMAL)
        model.vars.synth_settling_mode.var_enum = CreateModelVariableEnum(
            enum_name='SynthSettlingMode',
            enum_desc='Synth Settling Mode',
            member_data=[
                ['NORMAL', 0, 'Normal Operation Mode (Recommended)'],
                ['BLE_LR', 1, 'BLE Longrange Mode'],
                ['FAST', 2, 'Fast Settling Mode'],
            ])

        #Deprecated variable (needs to stay around as we have a deprecated Profile Input)
        self._addModelVariable(model, 'max_tx_power_dbm', int, ModelVariableFormat.DECIMAL,
                               desc='Maximum transmit power expected from this device (DEPRECATED)')

        self._addModelVariable(model, 'rf_band', Enum, ModelVariableFormat.DECIMAL)
        model.vars.rf_band.var_enum = CreateModelVariableEnum(
            enum_name='RFBandEnum',
            enum_desc='RF Band',
            member_data=[
                ['BAND_169', 0, '169 MHz Band'],
                ['BAND_315', 1, '315 MHz Band'],
                ['BAND_434', 2, '434 MHz Band'],
                ['BAND_490', 3, '490 MHz Band'],
                ['BAND_868', 4, '868 MHz Band'],
                ['BAND_915', 5, '915 MHz Band'],
                ['BAND_1432', 6, '1432 MHz Band'],
                ['BAND_2400', 7, '2400 MHz Band'],
            ])

        # for HFXO/HFRCO retiming
        self._addModelVariable(model, 'lut_table_index', int, ModelVariableFormat.DECIMAL, is_array=True)
        self._addModelVariable(model, 'lut_freq', int, ModelVariableFormat.DECIMAL, is_array=True)
        self._addModelVariable(model, 'lut_freq_upper', int, ModelVariableFormat.DECIMAL, is_array=True)
        self._addModelVariable(model, 'lut_valid', int, ModelVariableFormat.DECIMAL, is_array=True)
        self._addModelVariable(model, 'lut_smuxdiv', int, ModelVariableFormat.DECIMAL, is_array=True)
        self._addModelVariable(model, 'lut_limitl', int, ModelVariableFormat.DECIMAL, is_array=True)
        self._addModelVariable(model, 'lut_limith', int, ModelVariableFormat.DECIMAL, is_array=True)
        self._addModelVariable(model, 'lut_dpll_freq_hz', int, ModelVariableFormat.DECIMAL, is_array=True)

        self._addModelVariable(model, 'channel_spacing_hz', int, ModelVariableFormat.DECIMAL, units='Hz',
                               desc='Channel raster used for relative frequency configuration')
        self._addModelActual(model, 'channel_spacing', int, ModelVariableFormat.DECIMAL)

        # Tuning limits for the given LODIV setting
        self._addModelVariable(model, 'tuning_limit_min', long, ModelVariableFormat.DECIMAL, units='Hz',
                               desc='Minimum center frequency allowed for the current configuration.')
        self._addModelVariable(model, 'tuning_limit_max', long, ModelVariableFormat.DECIMAL, units='Hz',
                               desc='Maximum center frequency allowed for the current configuration.')

        # A proper flag to determine sub-GHz
        self._addModelVariable(model, 'subgig_band', bool, ModelVariableFormat.DECIMAL, desc="Flag for sub-GHz")

        var = self._addModelVariable(model, 'lo_injection_side', Enum, ModelVariableFormat.DECIMAL,
                                     'Possible LO injection sides')
        member_data = [
            ['HIGH_SIDE', 0, 'The local oscillator (LO) is higher in frequency than the receive RF channel'],
            ['LOW_SIDE', 1, 'The local oscillator (LO) is lower in frequency than the receive RF channel.'],

        ]
        var.var_enum = CreateModelVariableEnum(
            'LoInjectionSideEnum',
            'List of supported LO injection side configurations',
            member_data)
