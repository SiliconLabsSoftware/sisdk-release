from enum import Enum
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from pyradioconfig.modules.lpw.mod.r_01.prod_00.calculations.calc_mod_misc import CalcModMisc
from pyradioconfig.modules.lpw.mod.r_01.prod_00.calculations.calc_modulator import CalcModulator
from pyradioconfig.modules.lpw.mod.r_01.prod_00.calculations.calc_shaping import CalcShaping
from pyradioconfig.modules.lpw.mod.r_01.prod_00.calculations.calc_dac import CalcDac
from pyradioconfig.modules.lpw.mod.r_01.prod_00.calculations.calc_iq_mod_path import CalcIQModPath

from py_2_and_3_compatibility import *
from pyradioconfig.modules.lpw.mod.r_01.prod_00.reg_fields import ModRegFields


class CalcMod_r01(CalcModMisc, CalcModulator, CalcShaping, CalcDac, CalcIQModPath):

    def __init__(self, peripheral_name='MOD'):
        self._reg_field_list = ModRegFields().reg_field_list
        super().__init__(peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)

        # : Modulation Type
        var = self._addModelVariable(model, 'tx_modulation_type', Enum, ModelVariableFormat.DECIMAL,
                                     'Defines the TX modulation type.')
        member_data = [
            ['FSK2', 0, 'Frequency Shift Keying on two frequencies'],
            ['FSK4', 1, 'Frequency Shift Keying on four frequencies'],
            ['BPSK', 2,
             'Binary Phase Shift Keying: the 2 symbols are represented by 0 or 180 degree phase shifts wrt the carrier'],
            ['DBPSK', 3,
             'Differential Binary Phase Shift Keying: the 2 symbols are represented by 0 or 180 degree phase shifts wrt the preceding symbol'],
            ['OOK', 4, 'On Off Keying: the 2 symbols are represented by the presence / absence of the carrier'],
            ['ASK', 5,
             'Amplitude Shift Keying: the 2 symbols are represented by two different power levels of the carrier'],
            ['MSK', 6,
             'Minimum Shift Keying: Special case of FSK2 where the phase shift in one symbol is +/- 90 degree'],
            ['OQPSK', 7,
             'Offset Quadrature Phase Shift Keying: 4 state phase modulation with 0, 90, 180 and 270 degrees wrt the carrier. Only +/-90 degree changes are allowed at any one transition that take place at twice the symbol rate.'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'ModModeEnum',
            'Defines the TX modulation type.',
            member_data)

        # : Manchester mapping
        var = self._addModelVariable(model, 'tx_manchester_mapping', Enum, ModelVariableFormat.DECIMAL,
                                     'Manchester Code Mapping Options for packet payload')
        member_data = [
            ['Default', 0, '0-bit corresponds to a 0 to 1 transition and 1-bit corresponds to 1 to 0 transition'],
            ['Inverted', 1, '0-bit corresponds to a 1 to 0 transition and 1-bit corresponds to 0 to 1 transition'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'ManchesterMappingEnum',
            'List of supported Manchester Code options',
            member_data)

        # : TX FSK MAP
        var = self._addModelVariable(model, 'tx_fsk_symbol_map', Enum, ModelVariableFormat.DECIMAL,
                                     'List of FSK symbol mappings')
        member_data = [
            ['MAP0', 0, '4FSK: 11, 10, 00, 01 in decreasing frequency, 2FSK: 1 high, 0 low frequency'],
            ['MAP1', 1, '4FSK: 01, 00, 10, 11 in decreasing frequency, 2FSK: 0 high, 1 low frequency'],
            ['MAP2', 2, '4FSK: 10, 11, 01, 00 in decreasing frequency, 2FSK: undefined'],
            ['MAP3', 3, '4FSK: 00, 01, 11, 10 in decreasing frequency, 2FSK: undefined'],
            ['MAP4', 4, '4FSK: 11, 01, 00, 10 in decreasing frequency, 2FSK: undefined'],
            ['MAP5', 5, '4FSK: 10, 00, 01, 11 in decreasing frequency, 2FSK: undefined'],
            ['MAP6', 6, '4FSK: 01, 11, 10, 00 in decreasing frequency, 2FSK: undefined'],
            ['MAP7', 7, '4FSK: 00, 10, 11, 01 in decreasing frequency, 2FSK: undefined'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'FskSymbolMapEnum',
            'List of supported FSK symbol mappings',
            member_data)

        # : TX Symbol encoding
        var = self._addModelVariable(model, 'tx_symbol_encoding', Enum, ModelVariableFormat.DECIMAL,
                                     'Symbol Encoding Options')
        member_data = [
            ['NRZ', 0, 'Non Return Zero Coding'],
            ['Manchester', 1, 'Manchester Coding'],
            ['Inv_Manchester', 4, 'Inverted Manchester Coding'],
            ['DSSS', 2, 'Direct Sequence Spread Spectrum Coding'],
            ['LINECODE', 3, 'Maps 0 to 0011 symbol and 1 to 1100 symbol'],
            ['MBUS_3OF6', 5, 'Mbus 3 of 6 coding'],
            ['UART_NO_VAL', 6, 'UART Frame Coding without start/stop bit validation'],
            ['UART_VAL', 7, 'UART Frame Coding with start/stop bit validation']
        ]
        var.var_enum = CreateModelVariableEnum(
            'SymbolEncodingEnum',
            'List of supported symbol encoding options',
            member_data)

        # DIFFENCMODE
        var = self._addModelVariable(model, 'tx_diff_encoding_mode', Enum, ModelVariableFormat.DECIMAL,
                                     'Differential encoding mode options')
        member_data = [
            ['DISABLED', 0, 'Differential encoding is disabled'],
            ['RR0', 1, 'Transmit the xor-ed value of the Raw symbol and the last Raw symbol. Initial Raw symbol is 0.'],
            ['RE0', 2,
             'Transmit the xor-ed value of the Raw symbol and the last Encoded symbol. Initial Encoded symbol is 0.'],
            ['RR1', 3, 'Transmit the xor-ed value of the Raw symbol and the last Raw symbol. Initial Raw symbol is 1.'],
            ['RE1', 4,
             'Transmit the xor-ed value of the Raw symbol and the last Encoded symbol. Initial Encoded symbol is 1.'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'DiffEncModeEnum',
            'List of supported Differential Encoding Modes',
            member_data)

        self._addModelVariable(model, 'tx_dsss_shifts', int, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'tx_dsss_shifts', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'tx_dsss_len', int, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'tx_dsss_len', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'tx_dsss_chipping_code', long, ModelVariableFormat.HEX, desc='DSSS chipping code')

        self._addModelVariable(model, 'tx_preamble_pattern', int, ModelVariableFormat.DECIMAL,
                               desc='Minimum repeated portion of the preamble such as binary 01 or 10. ')
        self._addModelVariable(model, 'tx_preamble_pattern_len', int, ModelVariableFormat.DECIMAL, units='bits',
                               desc='Length of the preamble pattern in bits. This will be set to 2 for a simple 01 or 10 preamble pattern.')
        self._addModelActual(model, 'tx_preamble_pattern_len', int, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'tx_syncword_0', long, ModelVariableFormat.HEX,
                               desc="Default sync word.  Stored with the last bit transmitted in the LSB.")
        self._addModelVariable(model, 'tx_syncword_1', long, ModelVariableFormat.HEX,
                               desc="Alternative sync word for dual sync word cases.  Stored with the last bit transmitted in the LSB.")
        self._addModelVariable(model, 'tx_syncword_length', int, ModelVariableFormat.DECIMAL, units='bits',
                               desc="Length of the sync word in bits.")

        ### https://jira.silabs.com/browse/MCUW_RADIO_CFG-2737
        # TODO: update these names
        self._addModelVariable(model, 'rf_path', Enum, ModelVariableFormat.DECIMAL,
                               'List the different Modulator RF Path')
        model.vars.rf_path.var_enum = CreateModelVariableEnum('RfPathEnum', 'List of supported RF TX paths', [
            ['LPW', 0, 'RF path using LPW transceiver'],
            ['WIFI', 1, 'RF path using WIFI transceiver'],
        ])

        self._addModelVariable(model, 'dac_clock_mode', Enum, ModelVariableFormat.DECIMAL,
                               desc='determines dac clocking mode')
        model.vars.dac_clock_mode.var_enum = CreateModelVariableEnum(
            'ModSelEnum',
            'List of supported dac clock modes',
            [['DISABLED', 0, 'CLKMULT not used in TX mode'],
             ['HFXO', 1, 'DAC runs at HFXO frequency'],
             ['HFXOx2', 2, 'DAC runs at 2 x multiple of HFXO frequency'],
             ['HFXOx4', 3, 'DAC runs at 4 x multiple of HFXO frequency']
             ])

        var = self._addModelVariable(model, 'symbol_encoding', Enum, ModelVariableFormat.DECIMAL,
                                     'Symbol Encoding Options')
        member_data = [
            ['NRZ', 0, 'Non Return Zero Coding'],
            ['Manchester', 1, 'Manchester Coding'],
            ['Inv_Manchester', 4, 'Inverted Manchester Coding'],
            ['DSSS', 2, 'Direct Sequence Spread Spectrum Coding'],
            ['LINECODE', 3, 'Maps 0 to 0011 symbol and 1 to 1100 symbol'],
            ['MBUS_3OF6', 5, 'Mbus 3 of 6 coding'],
            ['UART_NO_VAL', 6, 'UART Frame Coding without start/stop bit validation'],
            ['UART_VAL', 7, 'UART Frame Coding with start/stop bit validation']
        ]
        var.var_enum = CreateModelVariableEnum(
            'SymbolEncodingEnum',
            'List of supported symbol encoding options',
            member_data)

        self._addModelVariable(model, 'modulator_select', Enum, ModelVariableFormat.DECIMAL,
                               desc='determines modulator path')
        model.vars.modulator_select.var_enum = CreateModelVariableEnum(
            'ModSelEnum',
            'List of supported modulator paths',
            [
                ['PH_MOD', 0, 'Phase modulator'],
                ['IQ_MOD', 1, 'IQ modulator (use upconverted I/Q from bit stream)'],
                ['IQ_MOD_DIRECT', 2, 'IQ modulator (use direct I/Q from modem)'],
            ])
        self._addModelVariable(model, 'br2m', int, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'synchronous_mixdac_clk', bool, ModelVariableFormat.DECIMAL,
                               desc='Flag used treat clk_dac as synchronous to clk_mod and bypass afifo')
        self._addModelVariable(model, 'am_low_ramplev', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'tx_grp_delay_us', float, ModelVariableFormat.DECIMAL,
                               desc='TX group delay in us')
        var = self._addModelVariable(model, 'manchester_mapping', Enum, ModelVariableFormat.DECIMAL, 'Manchester Code Mapping Options for packet payload')
        member_data = [
            ['Default',  0, '0-bit corresponds to a 0 to 1 transition and 1-bit corresponds to 1 to 0 transition'],
            ['Inverted', 1, '0-bit corresponds to a 1 to 0 transition and 1-bit corresponds to 0 to 1 transition'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'ManchesterMappingEnum',
            'List of supported Manchester Code options',
            member_data)

        """
        Shaping Coeff
        """
        self._addModelVariable(model, 'shaping_filter_taps', int, ModelVariableFormat.DECIMAL,
                               desc='Number of taps in the shaping filter')
        var = self._addModelVariable(model, 'shaping_filter', Enum, ModelVariableFormat.DECIMAL, desc='Defines the shaping filter to be used in the TX side.')
        member_data = [
            ['NONE',  0, 'No shaping filter is applied'],
            ['Gaussian',  1, 'Gaussian shaping filter - BT is defined at entry field Shaping Filter Parameter'],
            ['Raised_Cosine',  2, 'Raised Cosine shaping filter - R is defined at entry field Shaping Filter Parameter'],
            ['Root_Raised_Cosine',  3, 'Filter for 802.15.4 250 kbps DSSS OQPSK PHY'],
            ['Custom_OQPSK',  4, 'Filter for 802.15.4 250 kbps DSSS OQPSK PHY'],
            ['Custom_PSK', 5, 'Legacy 3rd party MSK filter']
        ]
        var.var_enum = CreateModelVariableEnum(
            'ShapingFilterEnum',
            'Defines the shaping filter to be used in the TX side.',
            member_data)

        self._addModelVariable(model, 'max_filter_taps', int, ModelVariableFormat.DECIMAL, 'Maximum Filter Taps available in Shaping filter')
        self._addModelVariable(model, 'shaping_filter_coeffs', int, ModelVariableFormat.DECIMAL, is_array=True)

        """
        Error calc
        """
        self._addModelVariable(model, 'tx_bitrate_error',   float, ModelVariableFormat.DECIMAL )
        self._addModelVariable(model, 'tx_deviation_error', float, ModelVariableFormat.DECIMAL )

