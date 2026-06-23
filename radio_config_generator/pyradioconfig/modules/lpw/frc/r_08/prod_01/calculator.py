from pyradioconfig.modules.lpw.frc.r_08.prod_01.calculations.calc_ber import CalcBer
from pyradioconfig.modules.lpw.frc.r_08.prod_01.calculations.calc_frc_misc import CalcFrcMisc
from pyradioconfig.modules.lpw.frc.r_08.prod_01.calculations.calc_fec import CalcFec
from pyradioconfig.modules.lpw.frc.r_08.prod_01.calculations.calc_frame import CalcFrame
from pyradioconfig.modules.lpw.frc.r_08.prod_01.calculations.calc_frame_coding import CalcFrameCoding
from pyradioconfig.modules.lpw.frc.r_08.prod_01.calculations.calc_whitening import CalcWhitening

from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from enum import Enum
from py_2_and_3_compatibility import *

from pyradioconfig.modules.lpw.frc.r_08.prod_01.reg_fields import FrcRegFields

class CalcFrc_r08(CalcBer, CalcFrcMisc, CalcFec, CalcFrame, CalcFrameCoding, CalcWhitening):

    def __init__(self, peripheral_name='FRC'):
        self._reg_field_list = FrcRegFields().reg_field_list
        super().__init__(peripheral_name)
        pass

    def buildVariables(self, model):
        super().buildVariables(model)

        """
        BER
        """

        self._addModelVariable(model, 'test_per',                   bool, ModelVariableFormat.ASCII, 'Enable to reconfigure for PER testing')
        self._addModelVariable(model, 'test_ber',                   bool, ModelVariableFormat.ASCII, 'Enable to reconfigure for BER testing')
        # Internal enables for different ber functions
        self._addModelVariable(model, 'ber_force_fdm0',             bool, ModelVariableFormat.ASCII, 'Force fdm0 mode for ber testing')
        self._addModelVariable(model, 'ber_force_sync',             bool, ModelVariableFormat.ASCII, 'Force a specific sync word for ber testing')
        self._addModelVariable(model, 'ber_force_bitorder',         bool, ModelVariableFormat.ASCII, 'Force a specific bit ordering for ber testing')
        self._addModelVariable(model, 'ber_force_whitening',        bool, ModelVariableFormat.ASCII, 'Force a specific de-whitening configuration for ber testing')
        self._addModelVariable(model, 'ber_force_infinite_length',  bool, ModelVariableFormat.ASCII, 'Force infinite length mode for ber testing')
        self._addModelVariable(model, 'ber_force_freq_comp_off',    bool, ModelVariableFormat.ASCII, 'Disable frequency compensation during BER testing')

        """
        FEC
        """

        var = self._addModelVariable(model, 'fec_en', Enum, ModelVariableFormat.DECIMAL,
                                     'List of supported FEC Configurations')
        member_data = [
            ['NONE', 0, 'No FEC'],
            ['FEC_154G_NRNSC_INTERLEAVING', 1, '15.4G FEC settings with NRNSC and interleaving'],
            ['FEC_154G_RSC_INTERLEAVING', 2, '15.4G FEC settings with RSC and interleaving'],
            ['FEC_154G_RSC_NO_INTERLEAVING', 3, '15.4G FEC settings with RSC and no interleaving'],
            ['FEC_K7_INTERLEAVING', 4, 'FEC settings with K=7 with interleaving'],
            ['FEC_BLE_HDT', 5, 'FEC settings for BLE HDT'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'FECEnum',
            'List of supported FEC Configurations',
            member_data)
        self._addModelVariable(model, 'mbus_postamble_length', int, ModelVariableFormat.DECIMAL,
                               'Mbus postamble legnth in sets of two alternating chips')
        var = self._addModelVariable(model, 'fec_tx_enable', Enum, ModelVariableFormat.DECIMAL, 'FEC enable')
        member_data = [
            ['DISABLED', 0, 'FEC Disabled'],
            ['ENABLED', 1, 'FEC Enabled'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'FECTxEnableEnum',
            'FEC TX Enable/Disable Selection',
            member_data)

        var = self._addModelVariable(model, 'dynamic_fec_enable', Enum, ModelVariableFormat.DECIMAL,
                                     'Enable dynamic FEC based on syncword')
        member_data = [
            ['DISABLED', 0, 'Dynamic FEC Disabled'],
            ['ENABLED', 1, 'Dynamic FEC Enabled'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'DynamicFecEnum',
            'Dynamic FEC Enable/Disable Selection',
            member_data)
        # Output software variables for RAIL to consume
        self._addModelVariable(model, 'frc_conv_decoder_buffer_size', int, ModelVariableFormat.DECIMAL, units='bytes', desc='Size (in bytes) of the buffer necessary for the Convolutional Decoder')
        self._addModelVariable(model, 'fec_enabled', int, ModelVariableFormat.DECIMAL, 'FEC enabled flag')

        """
        FRAME
        """

        # -------- General Frame Configurations --------
        var = self._addModelVariable(model, 'frame_bitendian', Enum, ModelVariableFormat.DECIMAL,
                                     'Define how the payload bits are transmitted over the air')
        member_data = [
            ['LSB_FIRST', 0, 'Least significant bit is transmitted first over the air'],
            ['MSB_FIRST', 1, 'Most significant bit is transmitted first over the air'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'bitEndian',
            'Define how the payload bits are transmitted over the air',
            member_data)
        self._addModelVariable(model, 'firstframe_bitsperword', int, ModelVariableFormat.DECIMAL, units='bits',
                               desc='On reception, create the first received bytes from less than 8 bits. This can be '
                                    'used to "bitshift" the frame. Upper bits are padded with 0 in the downloaded frame.')
        var = self._addModelVariable(model, 'frame_length_type', Enum, ModelVariableFormat.DECIMAL,
                                     'Possible Length Configurations')
        member_data = [
            ['FIXED_LENGTH', 0, 'The frame length is fixed and never changes'],
            ['VARIABLE_LENGTH', 1,
             'The frame length is determined by an explicit length field within the packet. Requires header to be enabled.'],
            ['FRAME_TYPE', 2,
             'The packet length is determined from an encoded set of bit that implicitly determines the length'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'FrameLengthEnum',
            'List of supported frame length configurations',
            member_data)
        # -------- Payload Configurations --------
        self._addModelVariable(model, 'payload_white_en', bool, ModelVariableFormat.ASCII,
                               'Set to true to whiten the payload')
        self._addModelVariable(model, 'payload_crc_en', bool, ModelVariableFormat.ASCII,
                               'Set to true to check/transmit crc after the payload')

        var = self._addModelVariable(model, 'crcprecalcsync_rx_mode', Enum, ModelVariableFormat.DECIMAL,
                                     'CRC pre-calculation w/syncword modes')
        member_data = [
            ['DISABLED', 0, 'Feature is disabled'],
            ['ENABLED', 1,
             'After RX init, FRC feeds SYNC bytes to RFCRC as part of initial subframe.'],
            ['ENABLEDSTORE', 2,
             'After RX init, FRC feeds SYNC bytes to RFCRC as part of initial subframe, while also storing SYNC in RX buffer.'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'CrcprecalcsyncEnum',
            'List of supported Crcprecalcsync Modes',
            member_data)

        self._addModelVariable(model, 'accept_crc_errors', bool, ModelVariableFormat.ASCII,
                               'Set to true if you want to accept invalid crcs')
        self._addModelVariable(model, 'payload_addtrailtxdata_en', bool, ModelVariableFormat.ASCII,
                               'Set to true to add Trail TX data at the end of the frame')
        self._addModelVariable(model, 'payload_excludesubframewcnt_en', bool, ModelVariableFormat.ASCII,
                               'Set to true to exclude words in the subframe from the Word Counter (WCNT), useful in Dynamic Frame Length (DFL) mode')
        # -------- Header Configurations --------
        self._addModelVariable(model, 'header_en', bool, ModelVariableFormat.ASCII,
                               'Set to true to enable a distinct header from the payload.')
        self._addModelVariable(model, 'header_size', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Define the number of bytes that make up the header. Include the variable length byte(s).')
        self._addModelVariable(model, 'header_calc_crc', bool, ModelVariableFormat.ASCII,
                               'Set to true to include the header bytes in the payload CRC.')
        self._addModelVariable(model, 'header_include_crc', bool, ModelVariableFormat.ASCII,
                               'Set to true to check/transmit crc specifically for the header')
        self._addModelVariable(model, 'header_white_en', bool, ModelVariableFormat.ASCII,
                               'Set to true to enable whitening over the header')
        self._addModelVariable(model, 'header_addtrailtxdata_en', bool, ModelVariableFormat.ASCII,
                               'Set to true to add Trail TX data at the end of the frame')
        self._addModelVariable(model, 'header_excludesubframewcnt_en', bool, ModelVariableFormat.ASCII,
                               'Set to true to exclude words in the subframe from the Word Counter (WCNT), useful in Dynamic Frame Length (DFL) mode')
        # -------- Fixed Length Configurations --------
        self._addModelVariable(model, 'fixed_length_size', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Define the number of bytes in the payload. This does not include the length of the header if used. Header + Payload must be less than 4096 bytes.')
        # -------- Variable Length Configurations --------
        self._addModelVariable(model, 'var_length_numbits', int, ModelVariableFormat.DECIMAL, units='bits',
                               desc='Define the size of the variable length field in bits.')
        var = self._addModelVariable(model, 'var_length_byteendian', Enum, ModelVariableFormat.DECIMAL,
                                     'Define the byte endianness of the variable length field')
        member_data = [
            ['LSB_FIRST', 0,
             'The least significant byte of the variable length field is transmitted over the air first.'],
            ['MSB_FIRST', 1,
             'The most significant byte of the variable length field is transmitted over the air first.'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'VarLengthByteEndian',
            'Define how the variable length byte(s) are transmitted over the air',
            member_data)
        var = self._addModelVariable(model, 'var_length_bitendian', Enum, ModelVariableFormat.DECIMAL,
                                     'Define the bit endianness of the variable length field')
        member_data = [
            ['LSB_FIRST', 0, 'The variable length field is transmitted least signficant bit first.'],
            ['MSB_FIRST', 1, 'The variable length field is transmitted most significant bit first.'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'VarLengthBitEndian',
            'Define how the variable length bits are transmitted over the air',
            member_data)
        self._addModelVariable(model, 'var_length_shift', int, ModelVariableFormat.DECIMAL,
                               'Define the location of the least significant bit of the variable length field.')
        self._addModelVariable(model, 'var_length_minlength', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Define the minimum value of the variable length field.')
        self._addModelVariable(model, 'var_length_maxlength', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Define the maximum value of the variable length field. Cannot exceed the variable '
                                    'length size.')
        self._addModelVariable(model, 'var_length_includecrc', bool, ModelVariableFormat.ASCII,
                               'Set to true if the crc bytes are included in the variable length')
        self._addModelVariable(model, 'var_length_adjust', int, ModelVariableFormat.DECIMAL,
                               'Value to add to the variable length extracted from the packet when calculating the'
                               ' total payload length to receive.  A positive number here indicates the payload will be'
                               ' larger than the length value extracted from the variable length bits.')
        # FRAME_TYPE
        self._addModelVariable(model, 'frame_type_loc', int, ModelVariableFormat.DECIMAL,
                               'Define the zero-based start location in the frame that holds the frame type encoding.')
        self._addModelVariable(model, 'frame_type_mask', int, ModelVariableFormat.HEX,
                               'Define the bitmask to extract the frame type in the byte.')
        self._addModelVariable(model, 'frame_type_bits', int, ModelVariableFormat.DECIMAL,
                               desc='Define the number of bits of the frame type field.', units='bits')
        self._addModelVariable(model, 'frame_type_lsbit', int, ModelVariableFormat.DECIMAL,
                               "Define the bit location of the frame type's least significant bit.")
        self._addModelVariable(model, 'frame_type_lengths', int, ModelVariableFormat.DECIMAL,
                               desc='Define the frame length of each frame type.', is_array=True, units='bytes')
        self._addModelVariable(model, 'frame_type_valid', bool, ModelVariableFormat.ASCII,
                               desc='Define the valid frame types.', is_array=True)
        self._addModelVariable(model, 'frame_type_filter', bool, ModelVariableFormat.ASCII,
                               desc='Define the frame types that should have address filtering applied.', is_array=True)
        # @bug https://jira.silabs.com/browse/MCUW_RADIO_CFG-37
        # This is a temporary measure to not use is_array
        self._addModelVariable(model, 'frame_type_0_length', int, ModelVariableFormat.DECIMAL,
                               desc='Define the frame length of each frame type.', units='bytes')
        self._addModelVariable(model, 'frame_type_1_length', int, ModelVariableFormat.DECIMAL,
                               desc='Define the frame length of each frame type.', units='bytes')
        self._addModelVariable(model, 'frame_type_2_length', int, ModelVariableFormat.DECIMAL,
                               desc='Define the frame length of each frame type.', units='bytes')
        self._addModelVariable(model, 'frame_type_3_length', int, ModelVariableFormat.DECIMAL,
                               desc='Define the frame length of each frame type.', units='bytes')
        self._addModelVariable(model, 'frame_type_4_length', int, ModelVariableFormat.DECIMAL,
                               desc='Define the frame length of each frame type.', units='bytes')
        self._addModelVariable(model, 'frame_type_5_length', int, ModelVariableFormat.DECIMAL,
                               desc='Define the frame length of each frame type.', units='bytes')
        self._addModelVariable(model, 'frame_type_6_length', int, ModelVariableFormat.DECIMAL,
                               desc='Define the frame length of each frame type.', units='bytes')
        self._addModelVariable(model, 'frame_type_7_length', int, ModelVariableFormat.DECIMAL,
                               desc='Define the frame length of each frame type.', units='bytes')
        self._addModelVariable(model, 'frame_type_0_valid', bool, ModelVariableFormat.ASCII,
                               desc='Define the valid frame types.')
        self._addModelVariable(model, 'frame_type_1_valid', bool, ModelVariableFormat.ASCII,
                               desc='Define the valid frame types.')
        self._addModelVariable(model, 'frame_type_2_valid', bool, ModelVariableFormat.ASCII,
                               desc='Define the valid frame types.')
        self._addModelVariable(model, 'frame_type_3_valid', bool, ModelVariableFormat.ASCII,
                               desc='Define the valid frame types.')
        self._addModelVariable(model, 'frame_type_4_valid', bool, ModelVariableFormat.ASCII,
                               desc='Define the valid frame types.')
        self._addModelVariable(model, 'frame_type_5_valid', bool, ModelVariableFormat.ASCII,
                               desc='Define the valid frame types.')
        self._addModelVariable(model, 'frame_type_6_valid', bool, ModelVariableFormat.ASCII,
                               desc='Define the valid frame types.')
        self._addModelVariable(model, 'frame_type_7_valid', bool, ModelVariableFormat.ASCII,
                               desc='Define the valid frame types.')
        self._addModelVariable(model, 'frame_type_0_filter', bool, ModelVariableFormat.ASCII,
                               desc='Define the frame types that should have address filtering applied.')
        self._addModelVariable(model, 'frame_type_1_filter', bool, ModelVariableFormat.ASCII,
                               desc='Define the frame types that should have address filtering applied.')
        self._addModelVariable(model, 'frame_type_2_filter', bool, ModelVariableFormat.ASCII,
                               desc='Define the frame types that should have address filtering applied.')
        self._addModelVariable(model, 'frame_type_3_filter', bool, ModelVariableFormat.ASCII,
                               desc='Define the frame types that should have address filtering applied.')
        self._addModelVariable(model, 'frame_type_4_filter', bool, ModelVariableFormat.ASCII,
                               desc='Define the frame types that should have address filtering applied.')
        self._addModelVariable(model, 'frame_type_5_filter', bool, ModelVariableFormat.ASCII,
                               desc='Define the frame types that should have address filtering applied.')
        self._addModelVariable(model, 'frame_type_6_filter', bool, ModelVariableFormat.ASCII,
                               desc='Define the frame types that should have address filtering applied.')
        self._addModelVariable(model, 'frame_type_7_filter', bool, ModelVariableFormat.ASCII,
                               desc='Define the frame types that should have address filtering applied.')

        self._addModelVariable(model, 'var_length_loc', int, ModelVariableFormat.DECIMAL,
                               'Define the zero-based start location in the header that holds the first byte of the variable length field.')
        self._addModelVariable(model, 'var_length_numbytes', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Define the size of the variable length field in bytes.')
        self._addModelVariable(model, 'header_size_internal', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Internal representation of header size. 0 for no header.')

        # Internal FCDX.WORDS register size
        self._addModelVariable(model, 'fcdx_words_bitwidth', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='FCD_WORDS bitwidth.')

        """
        Frame Coding
        """

        var = self._addModelVariable(model, 'frame_coding', Enum, ModelVariableFormat.DECIMAL,
                                     'List of supported frame coding methods')
        member_data = [
            ['NONE', 0, 'No Frame Coding'],
            ['UART_NO_VAL', 1, 'UART Frame Coding without start/stop bit validation'],
            ['UART_VAL', 2, 'UART Frame Coding with start/stop bit validation'],
            ['MBUS_3OF6', 3, 'Mbus 3 of 6 coding']
        ]
        var.var_enum = CreateModelVariableEnum(
            'FrameCodingEnum',
            'List of supported Frame Coding Methods',
            member_data)

        self._addModelVariable(model, 'frame_coding_array', int, ModelVariableFormat.DECIMAL, is_array=True)
        self._addModelVariable(model, 'frame_coding_message_bits', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'frame_coding_coded_bits', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'frame_coding_array_width', int, ModelVariableFormat.DECIMAL,
                               'Bytes required for coding table entries.  0=frame coding disabled, 8=one byte, 16=two bytes')
        self._addModelVariable(model, 'frame_coding_fshroutputsel_val', int, ModelVariableFormat.HEX)
        self._addModelVariable(model, 'frame_coding_poly_val', int, ModelVariableFormat.HEX)

        self._addModelVariable(model, 'frame_coding_array_packed', long, ModelVariableFormat.HEX, is_array=True)

        """
        Whitening
        """
        # WHITE_POLY
        var = self._addModelVariable(model, 'white_poly', Enum, ModelVariableFormat.DECIMAL,
                                     'List of supported Whitening Polynomials')
        member_data = [
            ['NONE', 0, 'No Whitening'],
            ['PN9', 1, 'X9+X5+1'],
            ['PN9_BYTE', 2, 'X9+X5+X1'],
            ['PN16', 3, 'X16+X14+X13+X11+1'],
            ['BLE', 4, 'X7+X4+1'],
            ['Bytewise_XOR_seed_LSB', 5, 'Each byte is XORed LSbyte of whitening seed'],
            ['PN9_802154', 6, 'PN9 sequence per IEEE 802.15.4'],
            ['ANT_TYPE1_XORINTERNAL', 7, 'ANT Type 1 poly using Silabs XOR-internal LFSR architecture'],
            ['ANT_TYPE1_XOREXTERNAL', 8, 'ANT Type 1 poly using Silabs XOR-external LFSR architecture'],
            ['ANT_TYPE2', 9, 'ANT Type 2 poly'],
            ['BLE_HDT', 10, 'BLE HDT']
        ]
        var.var_enum = CreateModelVariableEnum(
            'WhitePolyEnum',
            'List of supported Whitening Polynomials',
            member_data)
        # white_seed
        self._addModelVariable(model, 'white_seed', int, ModelVariableFormat.HEX, 'Whitening Initialization Value')
        # WHITE_OUTPUT_BIT
        self._addModelVariable(model, 'white_output_bit', int, ModelVariableFormat.HEX, 'Whitening Output Bit')
        self._addModelVariable(model, 'prewhite_en', bool, ModelVariableFormat.ASCII, 'Whitening done before CRC calculation for TX')
