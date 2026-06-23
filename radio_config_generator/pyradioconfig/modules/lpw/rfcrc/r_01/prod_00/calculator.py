from pyradioconfig.modules.lpw.rfcrc.r_01.prod_00.calculations.calc_crc import CalcCrc
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from enum import Enum
from py_2_and_3_compatibility import *
from pyradioconfig.modules.lpw.rfcrc.r_01.prod_00.reg_fields import RfcrcRegFields


class CalcRfcrc_r01(CalcCrc):
    """
    the CRC is now dual-configurable.
    There are 2 banks of configuration registers; CTRL, POLY, INIT for bank0 and CTRL1, POLY1, INIT1 for bank1.
    """

    def __init__(self, peripheral_name='RFCRC'):
        self._reg_field_list = RfcrcRegFields().reg_field_list
        super().__init__(peripheral_name=peripheral_name)

    # Method name: buildVariables
    # Defined in: ocelot\calculators\calc_crc.py
    def buildVariables(self, model):
        super().buildVariables(model)

        # CRC POLY
        member_data = [
            ['NONE', 0, 'No CRC'],
            ['CRC_8', 1, 'X8+X2+X+1'],
            ['CRC_16', 2, 'X16+X15+X2+1'],
            ['CCITT_16', 3, 'X16+X12+X5+1'],
            ['DNP_16', 4, 'X16+X13+X12+X11+X10+X8+X6+X5+X2+1'],
            ['BLE_24', 5, 'X24+X10+X9+X6+X4+X3+X+1'],
            ['CRC_32Q', 6, 'X32+X31+X24+X22+X16+X14+X8+X7+X5+X3+X+1'],
            ['ANSIX366_1979', 7, 'X32+X26+X23+X22+X16+X12+X11+X10+X8+X7+X5+X4+X2+X+1'],
            ['ZWAVE', 8, 'X8+1'],
            ['BCH15_11', 9, 'X4+X+1'],
            ['ANT_TYPE2', 10, 'X24+X22+X21+X20+X19+X17+X16+X8+X7+X5+X4+X3+X2+1'],
            ['CRC_24_HDT', 11, 'X24+X10+X9+X6+X4+X3+X+1'],
            ['CRC_32_HDT', 12, 'X32+X26+X23+X22+X16+X12+X11+X10+X8+X7+X5+X4+X2+X+1'],
        ]
        var = self._addModelVariable(model, 'crc_poly', Enum, ModelVariableFormat.DECIMAL,
                                     'List of supported CRC Polynomials')
        var.var_enum = CreateModelVariableEnum(
            'CrcPolyEnum',
            'List of supported CRC Polynomials',
            member_data)

        var = self._addModelVariable(model, 'crc_poly_1', Enum, ModelVariableFormat.DECIMAL,
                                     'List of supported CRC Polynomials for bank 1')
        var.var_enum = CreateModelVariableEnum(
            'CrcPolyEnum',
            'List of supported CRC Polynomials for bank 1',
            member_data)

        # CRC INIT
        self._addModelVariable(model, 'crc_seed', long, ModelVariableFormat.HEX, 'CRC Initialization Value')

        self._addModelVariable(model, 'crc_seed_1', long, ModelVariableFormat.HEX, 'CRC Initialization Value for bank 1')

        # CRC_BYTE_ENDIAN
        member_data = [
            ['LSB_FIRST', 0, 'Least significant byte of the CRC is transmitted first.'],
            ['MSB_FIRST', 1, 'Most significant byte of the CRC is transmitted first.'],
        ]
        var = self._addModelVariable(model, 'crc_byte_endian', Enum, ModelVariableFormat.DECIMAL, 'CRC Byte Endianness')
        var.var_enum = CreateModelVariableEnum(
            'CrcByteEndian',
            'Define how the CRC bytes are transmitted over the air',
            member_data)

        var = self._addModelVariable(model, 'crc_byte_endian_1', Enum, ModelVariableFormat.DECIMAL, 'CRC Byte Endianness for bank 1')
        var.var_enum = CreateModelVariableEnum(
            'CrcByteEndian',
            'Define how the CRC bytes are transmitted over the air',
            member_data)

        # CRC_BIT_ENDIAN
        member_data = [
            ['LSB_FIRST', 0, 'Over the air CRC bit order is sent least significant bit first.'],
            ['MSB_FIRST', 1, 'Over the air CRC bit order is sent most significant bit first'],
        ]
        var = self._addModelVariable(model, 'crc_bit_endian', Enum, ModelVariableFormat.DECIMAL, 'CRC Bit Endianness')
        var.var_enum = CreateModelVariableEnum(
            'CrcBitEndian',
            'Define how the CRC bits are transmitted over the air',
            member_data)

        var = self._addModelVariable(model, 'crc_bit_endian_1', Enum, ModelVariableFormat.DECIMAL, 'CRC Bit Endianness for bank 1')
        var.var_enum = CreateModelVariableEnum(
            'CrcBitEndian',
            'Define how the CRC bits are transmitted over the air',
            member_data)

        # CRC_PAD_INPUT
        self._addModelVariable(model, 'crc_pad_input', bool, ModelVariableFormat.ASCII,
                               'Set to true to enable zero padding of the CRC input data.')

        self._addModelVariable(model, 'crc_pad_input_1', bool, ModelVariableFormat.ASCII,
                               'Set to true to enable zero padding of the CRC input data for bank 1.')

        # CRC_INPUT_BIT_ORDER
        member_data = [
            ['LSB_FIRST', 0, 'The least significant data bit is first input to the CRC generator'],
            ['MSB_FIRST', 1, 'The most significant data bit is first input to the CRC generator'],
        ]

        var = self._addModelVariable(model, 'crc_input_order', Enum, ModelVariableFormat.DECIMAL,
                                     'Define the order data bits are fed into the CRC generator.')
        var.var_enum = CreateModelVariableEnum(
            'CrcInputOrderEnum',
            'Define the order data bits are fed into the CRC generator',
            member_data)

        var = self._addModelVariable(model, 'crc_input_order_1', Enum, ModelVariableFormat.DECIMAL,
                                     'Define the order data bits are fed into the CRC generator for bank 1.')
        var.var_enum = CreateModelVariableEnum(
            'CrcInputOrderEnum',
            'Define the order data bits are fed into the CRC generator',
            member_data)

        # CRC_INVERT
        self._addModelVariable(model, 'crc_invert', bool, ModelVariableFormat.ASCII,
                               'Set to true if the CRC result is inverted')
        self._addModelVariable(model, 'crc_invert_1', bool, ModelVariableFormat.ASCII,
                               'Set to true if the CRC result is inverted for bank 1')

        # The CRC periperal is now named RFCRC

        """
        #Outputs
        """

        self._addModelVariable(model, 'crc_polynomial', long, ModelVariableFormat.HEX, 'CRC polynomial')
        self._addModelVariable(model, 'crc_polynomial_1', long, ModelVariableFormat.HEX, 'CRC polynomial for bank 1')
        self._addModelVariable(model, 'crc_size', int, ModelVariableFormat.HEX, 'Size of CRC in bytes')
        self._addModelVariable(model, 'crc_size_1', int, ModelVariableFormat.HEX, 'Size of CRC in bytes for bank 1')

        # 802154 FCS Type
        self._addModelVariable(model, 'fcs_type_802154', Enum, ModelVariableFormat.DECIMAL,
                               desc='FCS type for 802154 PHYs')
        model.vars.fcs_type_802154.var_enum = CreateModelVariableEnum(
            enum_name='FcsTypeEnum',
            enum_desc='802154 FCS Type',
            member_data=[
                ['TWO_BYTE', 1, '16-bit ITU-T CRC'],
                ['FOUR_BYTE', 0, '32-bit ANSI X3.66-1979 CRC'],
            ])
