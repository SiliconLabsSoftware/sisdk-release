from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from py_2_and_3_compatibility import *
class CalcCrc(IPCalculator):

    # Method name: calc_crc_settings
    # Defined in: panther\calculators\calc_crc.py
    def calc_crc_settings(self, model):
        """
        calc_crc_settings for bank 0
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # This is a dictionary lookup of each of the supported CRC Polynomials
        # Each dictionary entry is a tuple which contains the poly and the CRC size
        CRC_POLY_LOOKUP = {
            model.vars.crc_poly.var_enum.NONE.value: (long(0), 0),
            model.vars.crc_poly.var_enum.CRC_8.value: (long(0x107), 1),
            model.vars.crc_poly.var_enum.CRC_16.value: (long(0x18005), 2),
            model.vars.crc_poly.var_enum.CCITT_16.value: (long(0x11021), 2),
            model.vars.crc_poly.var_enum.DNP_16.value: (long(0x13d65), 2),
            model.vars.crc_poly.var_enum.BLE_24.value: (long(0x100065b), 3),
            model.vars.crc_poly.var_enum.CRC_32Q.value: (long(0x1814141ab), 4),
            model.vars.crc_poly.var_enum.ANSIX366_1979.value: (long(0x104c11db7), 4),
            model.vars.crc_poly.var_enum.ZWAVE.value: (long(0x101), 1),
            model.vars.crc_poly.var_enum.BCH15_11.value: (long(0x13), 1),
            model.vars.crc_poly.var_enum.ANT_TYPE2.value: (long(0x17B01BD), 3),
            model.vars.crc_poly.var_enum.CRC_24_HDT.value: (long(0x100065b), 3),
            model.vars.crc_poly.var_enum.CRC_32_HDT.value: (long(0x104c11db7), 4),
        }
        self._calc_init_bank_0(model)
        # These variables are read from the table and put into model variables here.
        # The table is never referenced again after this.  This allows us to use
        # any arbitrary polynomial or size by just forcing these variables.
        # We could expose these two variables as advanced input variables if we
        # wanted to for either lab use or for customer use.
        #
        model.vars.crc_polynomial.value = CRC_POLY_LOOKUP[model.vars.crc_poly.value.value][0]
        model.vars.crc_size.value = CRC_POLY_LOOKUP[model.vars.crc_poly.value.value][1]
        if model.vars.crc_poly.value.value != model.vars.crc_poly.var_enum.NONE.value:
            # Handle POLY and Init configuration
            poly_reg, seed_reg = self._calc_crc_poly_reg(model.vars.crc_polynomial.value, model.vars.crc_seed.value)
            self._ip_reg_write(model, 'POLY_POLY', poly_reg)
            self._ip_reg_write(model, 'INIT_INIT', seed_reg)
            # Subtract 1 from the CRC size to get the proper value
            self._ip_reg_write(model, 'CTRL_CRCWIDTH', model.vars.crc_size.value - 1)
            # Handle Endianness
            if model.vars.crc_byte_endian.value == model.vars.crc_byte_endian.var_enum.LSB_FIRST:
                self._ip_reg_write(model, 'CTRL_BYTEREVERSE', 1)
            if model.vars.frame_bitendian.value.value == model.vars.crc_bit_endian.value.value:
                self._ip_reg_write(model, 'CTRL_BITREVERSE', 1)
            # Handle Input Bit Order
            if model.vars.crc_input_order.value == model.vars.crc_input_order.var_enum.MSB_FIRST:
                self._ip_reg_write(model, 'CTRL_INPUTBITORDER', 1)
            # Handle pad crc input
            if model.vars.crc_pad_input.value is True:
                self._ip_reg_write(model, 'CTRL_PADCRCINPUT', 1)
            if model.vars.crc_invert.value is True:
                self._ip_reg_write(model, 'CTRL_OUTPUTINV', 1)
        return

    def calc_crc_settings_bank1(self, model):
        """
        calc_crc_settings for bank 1
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # This is a dictionary lookup of each of the supported CRC Polynomials
        # Each dictionary entry is a tuple which contains the poly and the CRC size
        CRC_POLY_LOOKUP = {
            model.vars.crc_poly_1.var_enum.NONE.value: (long(0), 0),
            model.vars.crc_poly_1.var_enum.CRC_8.value: (long(0x107), 1),
            model.vars.crc_poly_1.var_enum.CRC_16.value: (long(0x18005), 2),
            model.vars.crc_poly_1.var_enum.CCITT_16.value: (long(0x11021), 2),
            model.vars.crc_poly_1.var_enum.DNP_16.value: (long(0x13d65), 2),
            model.vars.crc_poly_1.var_enum.BLE_24.value: (long(0x100065b), 3),
            model.vars.crc_poly_1.var_enum.CRC_32Q.value: (long(0x1814141ab), 4),
            model.vars.crc_poly_1.var_enum.ANSIX366_1979.value: (long(0x104c11db7), 4),
            model.vars.crc_poly_1.var_enum.ZWAVE.value: (long(0x101), 1),
            model.vars.crc_poly_1.var_enum.BCH15_11.value: (long(0x13), 1),
            model.vars.crc_poly_1.var_enum.ANT_TYPE2.value: (long(0x17B01BD), 3),
            model.vars.crc_poly_1.var_enum.CRC_24_HDT.value: (long(0x100065b), 3),
            model.vars.crc_poly_1.var_enum.CRC_32_HDT.value: (long(0x104c11db7), 4),
        }
        self._calc_init_bank_1(model)
        # These variables are read from the table and put into model variables here.
        # The table is never referenced again after this.  This allows us to use
        # any arbitrary polynomial or size by just forcing these variables.
        # We could expose these two variables as advanced input variables if we
        # wanted to for either lab use or for customer use.
        #
        model.vars.crc_polynomial_1.value = CRC_POLY_LOOKUP[model.vars.crc_poly_1.value.value][0]
        model.vars.crc_size_1.value = CRC_POLY_LOOKUP[model.vars.crc_poly_1.value.value][1]
        if model.vars.crc_poly_1.value.value != model.vars.crc_poly.var_enum.NONE.value:
            # Handle POLY and Init configuration
            poly_reg, seed_reg = self._calc_crc_poly_reg(model.vars.crc_polynomial_1.value, model.vars.crc_seed_1.value)
            self._ip_reg_write(model, 'POLY1_POLY1', poly_reg)
            self._ip_reg_write(model, 'INIT1_INIT1', seed_reg)
            # Subtract 1 from the CRC size to get the proper value
            self._ip_reg_write(model, 'CTRL1_CRCWIDTH1', model.vars.crc_size_1.value - 1)
            # Handle Endianness
            if model.vars.crc_byte_endian_1.value == model.vars.crc_byte_endian_1.var_enum.LSB_FIRST:
                self._ip_reg_write(model, 'CTRL1_BYTEREVERSE1', 1)
            if model.vars.frame_bitendian.value.value == model.vars.crc_bit_endian_1.value.value:
                self._ip_reg_write(model, 'CTRL1_BITREVERSE1', 1)
            # Handle Input Bit Order
            if model.vars.crc_input_order_1.value == model.vars.crc_input_order_1.var_enum.MSB_FIRST:
                self._ip_reg_write(model, 'CTRL1_INPUTBITORDER1', 1)
            # Handle pad crc input
            if model.vars.crc_pad_input_1.value is True:
                self._ip_reg_write(model, 'CTRL1_PADCRCINPUT1', 1)
            if model.vars.crc_invert_1.value is True:
                self._ip_reg_write(model, 'CTRL1_OUTPUTINV1', 1)
        return

    # Method name: _calc_crc_poly_reg
    # Defined in: common\calculators\calc_crc.py
    def _calc_crc_poly_reg(self, polyval, seedval):
        """_calc_crc_poly_reg
        Args:
            polyval (unknown) : polyval
            seedval (unknown) : seedval
        """
        if polyval == 0:
            polyreg = long(0)
            seedreg = long(0)  # TODO: ?
        else:
            polyreg = long(0)
            seedreg = long(0)
            while polyval != 1:
                polyreg = polyreg << 1
                if polyval & 0x01:
                    polyreg = polyreg | 1
                polyval = polyval >> 1
                # print("polyval = %X   polyreg = %X" % (polyval, polyreg)
                seedreg = seedreg << 1
                if seedval & 0x01:
                    seedreg = seedreg | 1
                seedval = seedval >> 1
            # print("polyval = %X   polyreg = %X" % (polyval, polyreg)
        return polyreg, seedreg

    # Method name: _calc_crc_poly_value
    # Defined in: common\calculators\calc_crc.py
    def _calc_crc_poly_value(self, polyreg):
        """This can be used to calculate the polynomial value from the register value
        Args:
            polyreg (unknown) :polyreg
        """
        polyval = long(1)
        while polyreg != 0:
            polyval = polyval << 1
            if polyreg & 1:
                polyval |= 1
            polyreg = polyreg >> 1

        return polyval

    # Method name: _calc_init
    # Defined in: panther\calculators\calc_crc.py
    def _calc_init_bank_0(self, model):
        """_calc_init
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        self._ip_reg_write(model, 'CTRL_PADCRCINPUT', 0)
        self._ip_reg_write(model, 'CTRL_BITREVERSE', 0)
        self._ip_reg_write(model, 'CTRL_BYTEREVERSE', 0)
        self._ip_reg_write(model, 'CTRL_INPUTBITORDER', 0)
        self._ip_reg_write(model, 'CTRL_CRCWIDTH', 0)
        self._ip_reg_write(model, 'CTRL_OUTPUTINV', 0)
        self._ip_reg_write(model, 'INIT_INIT', long(0))
        self._ip_reg_write(model, 'POLY_POLY', long(0))
        # Always set BITSPERWORD to 7 because we work with bytes
        self._ip_reg_write(model, 'CTRL_BITSPERWORD', 7)

    def _calc_init_bank_1(self, model):
        """_calc_init
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        self._ip_reg_write(model, 'CTRL1_PADCRCINPUT1', 0)
        self._ip_reg_write(model, 'CTRL1_BITREVERSE1', 0)
        self._ip_reg_write(model, 'CTRL1_BYTEREVERSE1', 0)
        self._ip_reg_write(model, 'CTRL1_INPUTBITORDER1', 0)
        self._ip_reg_write(model, 'CTRL1_CRCWIDTH1', 0)
        self._ip_reg_write(model, 'CTRL1_OUTPUTINV1', 0)
        self._ip_reg_write(model, 'INIT1_INIT1', long(0))
        self._ip_reg_write(model, 'POLY1_POLY1', long(0))


    def calc_crc_model_variable_defaults_bank_1(self, model):
        """
        Set default values for model variables related to CRC for bank 1.
        These variables are not yet added to base profile inputs. Delete me if/when that happends.
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        model.vars.crc_poly_1.value = model.vars.crc_poly.var_enum.NONE
        model.vars.crc_seed_1.value = long(0x0)
        model.vars.crc_input_order_1.value = model.vars.crc_input_order.var_enum.LSB_FIRST
        model.vars.crc_bit_endian_1.value = model.vars.crc_bit_endian.var_enum.MSB_FIRST
        model.vars.crc_byte_endian_1.value = model.vars.crc_byte_endian.var_enum.MSB_FIRST
        model.vars.crc_pad_input_1.value = False
        model.vars.crc_invert_1.value = False