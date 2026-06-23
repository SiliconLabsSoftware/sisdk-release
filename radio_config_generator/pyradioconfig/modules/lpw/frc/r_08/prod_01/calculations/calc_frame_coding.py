from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from py_2_and_3_compatibility import *

class CalcFrameCoding(IPCalculator):
    # Method name: _build_fecctrl_reg
    # Defined in: lpwh72000\calculators\calc_frame_coding.py
    def _build_fecctrl_reg(self, model):
        pass

    # Method name: _calc_init
    # Defined in: common\calculators\frame_coding.py
    def _calc_init(self, model):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

    # Method name: _create_content_table
    # Defined in: common\calculators\frame_coding.py
    def _create_content_table(self, message_bits, coded_bits, array_width, coding_table_is_msb_first, coding_table):
        # Notice that everything below this line could be refactored into common code.  The only
        # thing specific to a given coding scheme is the table above and parameters above
        error_value = 1 << (array_width - 1)
        # Calculate the tx table from the coded table.  It's just flipping the endianness of
        # the bits if the table was initially expressed in msb first format
        tx_map_table = dict()
        for message_value in coding_table.keys():
            coded_value = coding_table[message_value]
            # if the coding_table was entered msb first for sanity reasons,
            # flip the input and output values to match the hardware which is always lsb first
            if coding_table_is_msb_first:
                message_value = self.flip_bits(message_value, message_bits)
                coded_value = self.flip_bits(coded_value, coded_bits)
            tx_map_table[message_value] = coded_value
        # Create a receive data map from the transmit table.
        # Just flip the keys and values from the transmit table.
        rx_map_table = dict()
        # Now add the valid values from the tx map table to the rx_map_table
        for message_value in tx_map_table.keys():
            coded_value = tx_map_table[message_value]
            rx_map_table[coded_value] = message_value
        # Now create a list where we list all 64 receive values first, followed by the 16 transmit values.
        content = []
        # Receive table
        rx_table_size = 1 << coded_bits
        for rx_data in range(rx_table_size):
            if rx_data in rx_map_table.keys():
                content.append(int(rx_map_table[rx_data]))
            else:
                content.append(error_value)
        # Transmit table
        tx_table_size = 1 << message_bits
        for tx_data in range(tx_table_size):
            content.append(int(tx_map_table[tx_data]))
        if message_bits == 1 and array_width == 8:
            # Extend with zeros bytes to respect the RAM table 4 bytes boundary
            content.extend([0, 0])
        return content

    # Method name: _frame_coding_3of6
    # Defined in: common\calculators\frame_coding.py
    def _frame_coding_3of6(self):
        # List the lookup data with 4-bit sequence as keys, 6-bit sequence as values.
        coding_table = {
            0b0000: 0b010110,
            0b0001: 0b001101,
            0b0010: 0b001110,
            0b0011: 0b001011,
            0b0100: 0b011100,
            0b0101: 0b011001,
            0b0110: 0b011010,
            0b0111: 0b010011,
            0b1000: 0b101100,
            0b1001: 0b100101,
            0b1010: 0b100110,
            0b1011: 0b100011,
            0b1100: 0b110100,
            0b1101: 0b110001,
            0b1110: 0b110010,
            0b1111: 0b101001
        }
        message_bits = 4  # Later this could be pulled from the definition of the coding scheme
        coded_bits = 6  # Later this could be pulled from the definition of the coding scheme
        array_width = 8
        coding_table_is_msb_first = True  # Pull this from the frame format variable
        return self._create_content_table(message_bits, coded_bits, array_width, coding_table_is_msb_first,
                                          coding_table)

    # Method name: _frame_coding_UART
    # Defined in: common\calculators\frame_coding.py
    def _frame_coding_UART(self):
        """_frame_coding_UART
        Function creates block coding array for UART frame coding
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        content = []
        for received in range(1024):
            if (received & 0x200) and (not (received & 0x001)):
                content.append((received >> 1) & 0xFF)
            else:
                content.append(0x8000 + ((received >> 1) & 0xFF))
        # Transmit table
        for i in range(256):
            content.append(0x200 + (i << 1))
        return content

    # Method name: _frame_coding_manchester
    # Defined in: ocelot\calculators\calc_frame_coding.py
    def _frame_coding_manchester(self):
        # List the lookup data with 1-bit sequence as keys, 2-bit sequence as values.
        # From https://jira.silabs.com/browse/MCUW_RADIO_CFG-2046
        coding_table = {
            0b0: 0b01,
            0b1: 0b10
        }
        message_bits = 1
        coded_bits = 2
        array_width = 8
        coding_table_is_msb_first = True  # Presented as msb, but coded into the RAM as lsb
        return self._create_content_table(message_bits, coded_bits, array_width,
                                          coding_table_is_msb_first, coding_table)

    # Method name: _frame_coding_none
    # Defined in: common\calculators\frame_coding.py
    def _frame_coding_none(self):
        return None

    # Method name: calc_blockwhitemode
    # Defined in: common\calculators\frame_coding.py
    def calc_blockwhitemode(self, model):
        # This method calculates the FRC_FECCTRL_BLOCKWHITEMODE field
        # The LFSR used for whitening is also used for block coding forward-error-correction.
        # This means that it is not possible to perform both whitening and block coding on the same frame.
        # Read in model variables
        ber_force_whitening = model.vars.ber_force_whitening.value
        payload_white_en = model.vars.payload_white_en.value
        header_white_en = model.vars.header_white_en.value
        frame_coding_array_width = model.vars.frame_coding_array_width.value
        white_poly = model.vars.white_poly.value
        fec_enabled = model.vars.fec_enabled.value
        prewhite_en = model.vars.prewhite_en.value
        if ber_force_whitening:
            # Force whitening when desired for BER testing
            blockwhitemode = 1
        elif prewhite_en:
            # If prewhitener is enabled, disable normal whitener
            blockwhitemode = 0
        elif frame_coding_array_width > 0:
            # Using block coding
            blockwhitemode = 7
        elif payload_white_en or header_white_en:
            # Whitening is turned on for either header or payload
            if fec_enabled:
                if payload_white_en and header_white_en:
                    # Using FEC with whitening of header and payload
                    # Should work with interleaving enabled, need to verify operation with interleaving disabled
                    blockwhitemode = 3
                elif payload_white_en:
                    # Using FEC with whitening of only payload (skip whitening of first 16*interleavewidth bits)
                    blockwhitemode = 4
            elif 'byte' in white_poly.name.lower():
                # Using whitening polynomial enum corresponding to bytewhite
                blockwhitemode = 2
            else:
                # Standard whitening
                blockwhitemode = 1
        elif white_poly != model.vars.white_poly.var_enum.NONE:
            # If a whitening polynomial is present, then enable standard whitening
            # This still allows disabling whitening via the SKIPWHITE field in each FCD
            blockwhitemode = 1
        else:
            # Disable whitening
            blockwhitemode = 0
        # Write the register
        self._ip_reg_write(model, 'FECCTRL_BLOCKWHITEMODE', blockwhitemode)

    # Method name: calc_frame_coding
    # Defined in: ocelot\calculators\calc_frame_coding.py
    def calc_frame_coding(self, model):
        # In TRECS_VITERBI demod, the encoding of the data must be performed using the hardware block coder.
        symbol_encoding = model.vars.symbol_encoding.value
        demod_select = model.vars.demod_select.value
        FRAME_CODING_LOOKUP = {
            model.vars.symbol_encoding.var_enum.Manchester.value: (1, 2, 8, self._frame_coding_manchester),
            model.vars.symbol_encoding.var_enum.Inv_Manchester.value: (1, 2, 8, self._frame_coding_manchester)
        }
        if (symbol_encoding == model.vars.symbol_encoding.var_enum.Manchester or
            symbol_encoding == model.vars.symbol_encoding.var_enum.Inv_Manchester) and \
                demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI:
            frameCodingParams = FRAME_CODING_LOOKUP[symbol_encoding]
            model.vars.frame_coding_message_bits.value = frameCodingParams[0]
            model.vars.frame_coding_coded_bits.value = frameCodingParams[1]
            model.vars.frame_coding_array_width.value = frameCodingParams[2]
            model.vars.frame_coding_array.value = frameCodingParams[3]()
        else:
            # Only perform this calculation when dealing with a frame_coding setting that produces a frame_coding_array
            # that is not None
            frame_coding = model.vars.frame_coding.value
            if frame_coding != model.vars.frame_coding.var_enum.NONE and \
                    frame_coding != model.vars.frame_coding.var_enum.UART_NO_VAL:

                coding_array = model.vars.frame_coding_array.value
                width = model.vars.frame_coding_array_width.value
                if width == 0:
                    model.vars.frame_coding_array_packed.value = None
                elif width == 8:
                    if (len(coding_array) % 4) != 0:
                        raise CalculationException("Frame coding array not word aligned!")
                    model.vars.frame_coding_array_packed.value = self.pack_list(coding_array, width)
                elif width == 16:
                    if (len(coding_array) % 2) != 0:
                        raise CalculationException("Frame coding array not word aligned!")
                    model.vars.frame_coding_array_packed.value = self.pack_list(coding_array, width)
                else:
                    raise CalculationException("Unexpected frame coding array width of %s!" % width)

    # Method name: calc_frame_coding_array_packed
    # Defined in: ocelot\calculators\calc_frame_coding.py
    def calc_frame_coding_array_packed(self, model):
        # Pack the frame coding values into 32 bits integers
        symbol_encoding = model.vars.symbol_encoding.value
        demod_select = model.vars.demod_select.value
        if (symbol_encoding == model.vars.symbol_encoding.var_enum.Manchester or
            symbol_encoding == model.vars.symbol_encoding.var_enum.Inv_Manchester) and \
                demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI:
            coding_array = model.vars.frame_coding_array.value
            width = model.vars.frame_coding_array_width.value
            model.vars.frame_coding_array_packed.value = self.pack_list(coding_array, width)
        else:
            FRAME_CODING_LOOKUP = {
                model.vars.frame_coding.var_enum.NONE.value: (0, 0, 0, self._frame_coding_none),
                model.vars.frame_coding.var_enum.UART_NO_VAL.value: (0, 0, 0, self._frame_coding_none),
                model.vars.frame_coding.var_enum.UART_VAL.value: (8, 10, 16, self._frame_coding_UART),
                model.vars.frame_coding.var_enum.MBUS_3OF6.value: (4, 6, 8, self._frame_coding_3of6)
            }

            # Need to use block coding in efr
            frameCodingParams = FRAME_CODING_LOOKUP[model.vars.frame_coding.value]
            model.vars.frame_coding_message_bits.value = frameCodingParams[0]
            model.vars.frame_coding_coded_bits.value = frameCodingParams[1]
            model.vars.frame_coding_array_width.value = frameCodingParams[2]
            model.vars.frame_coding_array.value = frameCodingParams[3]()

    # Method name: calc_frame_coding_reg_values
    # Defined in: common\calculators\frame_coding.py
    def calc_frame_coding_reg_values(self, model):
        if model.vars.frame_coding_array_width.value > 0:
            model.vars.frame_coding_fshroutputsel_val.value = model.vars.frame_coding_message_bits.value - 1
            model.vars.frame_coding_poly_val.value = 1 << (model.vars.frame_coding_coded_bits.value - 1)
        else:
            model.vars.frame_coding_fshroutputsel_val.value = 0
            model.vars.frame_coding_poly_val.value = 0

    # Method name: calc_frame_coding_var
    # Defined in: ocelot\calculators\calc_frame_coding.py
    def calc_frame_coding_var(self, model):
        # On Ocelot, we removed frame_coding as a Profile Input, so we need to calculate the variable from symbol_encoding
        symbol_encoding = model.vars.symbol_encoding.value
        if symbol_encoding == model.vars.symbol_encoding.var_enum.UART_NO_VAL:
            frame_coding = model.vars.frame_coding.var_enum.UART_NO_VAL
        elif symbol_encoding == model.vars.symbol_encoding.var_enum.UART_VAL:
            frame_coding = model.vars.frame_coding.var_enum.UART_VAL
        elif symbol_encoding == model.vars.symbol_encoding.var_enum.MBUS_3OF6:
            frame_coding = model.vars.frame_coding.var_enum.MBUS_3OF6
        else:
            frame_coding = model.vars.frame_coding.var_enum.NONE
        # Write the model variable
        model.vars.frame_coding.value = frame_coding

    # Method name: calc_uartmode
    # Defined in: common\calculators\frame_coding.py
    def calc_uartmode(self, model):
        if model.vars.frame_coding.value == model.vars.frame_coding.var_enum.UART_NO_VAL.value:
            self._ip_reg_write(model, 'CTRL_UARTMODE', 1)
        else:
            self._ip_reg_write(model, 'CTRL_UARTMODE', 0)

    # Method name: pack_list
    # Defined in: common\calculators\frame_coding.py
    @staticmethod
    def pack_list(input_list, width):
        packed_list = list()
        total_bits = 0
        word_being_built = long(0)
        for list_item in input_list:
            # word_being_built = (word_being_built << width) | list_item                # Use this line for Big Endian
            word_being_built = (word_being_built >> width) | (
                        list_item << (32 - width))  # Use this line for Little Endian
            total_bits += width
            if total_bits % 32 == 0:
                packed_list.append(word_being_built)
                word_being_built = long(0)
        return packed_list

    # Method name: flip_bits
    # Defined in: common\calculators\calc_frame_detect.py
    @staticmethod
    def flip_bits(input, numbits):
        """
        flips the order of bits in an input numbits wide
        Bits are flipped within the field defined by numbits
        Args:
            input (unknown) : input
            numbits (unknown) : numbits
        Returns:
            output (unknown) : unknown
        """
        output = long(0)
        # find index of LSB
        first_bit = numbits
        for bitnum in range(numbits):
            if (input & (1 << bitnum)):
                output = output | (1 << (numbits - 1 - bitnum))
        return output