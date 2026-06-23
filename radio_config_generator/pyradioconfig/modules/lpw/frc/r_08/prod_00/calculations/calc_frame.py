from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
class CalcFrame(IPCalculator):

    # Method name: calc_check_crc_poly
    # Defined in: common\calculators\calc_frame.py
    def calc_check_crc_poly(self, model):
        header_include_crc = model.vars.header_include_crc.value
        payload_crc_en = model.vars.payload_crc_en.value
        crc_poly = model.vars.crc_poly.value.value
        if header_include_crc == True or payload_crc_en == True:
            if crc_poly == model.vars.crc_poly.var_enum.NONE.value:
                raise CalculationException("ERROR: CRC enabled with crc polynomial set to NONE")

    # Method name: calc_excludesubframewcnt_en
    # Defined in: ocelot\calculators\calc_frame.py
    def calc_excludesubframewcnt_en(self, model):
        # This function calculates the excludesubframewcnt_en variables for header and payload
        # based on whether we are in BER test mode or not
        # Read in model variables
        ber_force_infinite_length = model.vars.ber_force_infinite_length.value
        # Calculate based on BER test mode
        if ber_force_infinite_length:
            header_excludesubframewcnt_en = True
            payload_excludesubframewcnt_en = True
        else:
            header_excludesubframewcnt_en = False
            payload_excludesubframewcnt_en = False
        # Write to model variables
        model.vars.header_excludesubframewcnt_en.value = header_excludesubframewcnt_en
        model.vars.payload_excludesubframewcnt_en.value = payload_excludesubframewcnt_en

    # Method name: calc_frame
    # Defined in: common\calculators\calc_frame.py
    def calc_frame(self, model):
        """
        Configure general frame configurations
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # Nominal calculation
        # Account for +1 in register
        model.vars.firstframe_bitsperword.value = 8
        # Unless specied via advanced input
        bitsperword_reg = model.vars.firstframe_bitsperword.value - 1
        self._ip_reg_write(model, 'CTRL_BITSPERWORD',  bitsperword_reg)
        if model.vars.ber_force_bitorder.value == True:
            self._ip_reg_write(model, 'CTRL_BITORDER',  1)
        else:
            self._ip_reg_write(model, 'CTRL_BITORDER',
                            int(model.vars.frame_bitendian.value == model.vars.frame_bitendian.var_enum.MSB_FIRST))
        return

    # Method name: calc_frame_length
    # Defined in: panther\calculators\calc_frame.py
    def calc_frame_length(self, model):
        """calc_frame_length
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        if (model.vars.frame_length_type.value == model.vars.frame_length_type.var_enum.FIXED_LENGTH):
            if (model.vars.header_en.value == True):
                self._calc_frame_length_defaults(model)
                self._fixed_length_with_header(model)
            else:
                self._calc_frame_length_defaults(model)
                self._fixed_length_no_header(model)
        elif (
                model.vars.frame_length_type.value == model.vars.frame_length_type.var_enum.VARIABLE_LENGTH and model.vars.header_en.value == True):
            # Variable Length requires headers
            self._configure_header(model)
            # Configure rest of payload options
            self._configure_payload_with_header(model)
            # Variable Length
            self._configure_variable_length(model)
            # Use FCD0/2 for first subframe then FCD1/3 is used for all following subframes
            self._ip_reg_write(model, 'CTRL_TXFCDMODE',  2)
            self._ip_reg_write(model, 'CTRL_RXFCDMODE',  2)
        elif (model.vars.frame_length_type.value == model.vars.frame_length_type.var_enum.FRAME_TYPE):
            self._calc_frame_length_defaults(model)
            self._configure_fcd_for_frame_type(model)
            # Frame Type
            self._configure_frame_type(model)
            pass
        return

    # Method name: calc_header_bytes
    # Defined in: common\calculators\calc_frame.py
    def calc_header_bytes(self, model):
        if model.vars.header_en.value == True:
            model.vars.header_size_internal.value = model.vars.header_size.value
        else:
            model.vars.header_size_internal.value = 0

    # Method name: calc_possible_future_inputs
    # Defined in: ocelot\calculators\calc_frame.py
    def calc_possible_future_inputs(self, model):
        # Copied from Commmon but removed excludesubframewcnt_en variables as those will be calculated in another method
        model.vars.header_include_crc.value = False
        model.vars.header_addtrailtxdata_en.value = False
        model.vars.payload_addtrailtxdata_en.value = False
        return

    # Method name: calc_var_length_loc
    # Defined in: common\calculators\calc_frame.py
    def calc_var_length_loc(self, model):
        """
        The variable length location must be the last 1 or 2 bytes of the header
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # MCUW_RADIO_CFG-642
        # Calculate length location as normal
        model.vars.var_length_loc.value = model.vars.header_size_internal.value - model.vars.var_length_numbytes.value
        # We should never have the var_length_numbytes larger than the total header size.  If it is, var_length_loc
        # will go negative.  If it does, fix it.
        if model.vars.var_length_loc.value < 0:
            model.vars.var_length_loc.value = 0

    # Method name: calc_var_length_numbytes
    # Defined in: common\calculators\calc_frame.py
    def calc_var_length_numbytes(self, model):
        """calc_var_length_numbytes
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # If the number of variable length bit plus the amount needed to shift exceeds 8
        # then the number of bytes needed to contain the variable length field is two.
        quotient, remainder = divmod((model.vars.var_length_numbits.value + model.vars.var_length_shift.value), 8)
        if (remainder > 0):
            model.vars.var_length_numbytes.value = quotient + 1
        else:
            model.vars.var_length_numbytes.value = quotient

        # Method name: _fixed_length_no_header
        # Defined in: common\calculators\calc_frame.py
    def _fixed_length_no_header(self, model):
        """_fixed_length_no_header
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # FCDX_WORDS is being set to max value. To figure out the max value, reading the bitwidth.
        # assuming FCD0/1/2/3 will always have same bitwidth in future as well.
        # checking the value for None in case the register does not exist (for e.g. unit_test_part)
        fcdx_words_bitwidth = model.vars.fcdx_words_bitwidth.value

        self._ip_reg_write(model, 'WCNTCMP0_FRAMELENGTH',  model.vars.fixed_length_size.value - 1)
        fcdDict = {
            "excludesubframewcnt": int(model.vars.payload_excludesubframewcnt_en.value == True),
            "addtrailtxdata": int(model.vars.payload_addtrailtxdata_en.value == True),
            "skipwhite": int(model.vars.payload_white_en.value == False),
            "skipcrc": 0,
            "calccrc": int(model.vars.payload_crc_en.value == True),
            "includecrc": int(model.vars.payload_crc_en.value == True),
            "words": 2 ** fcdx_words_bitwidth - 1,
        }
        # Configure TX FCD
        self._configure_fcd(model, fcdindex="0", buf=0, **fcdDict)
        # Configure RX FCD
        self._configure_fcd(model, fcdindex="2", buf=1, **fcdDict)
        self._configure_fcd(model, 1)  # Turn off this fcd
        self._configure_fcd(model, 3)  # Turn off this fcd
        self._ip_reg_write(model, 'CTRL_TXFCDMODE',  0)
        self._ip_reg_write(model, 'CTRL_RXFCDMODE',  0)
        return

    # Method name: _fixed_length_with_header
    # Defined in: common\calculators\calc_frame.py
    def _fixed_length_with_header(self, model):
        """_fixed_length_with_header
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        self._ip_reg_write(model, 'WCNTCMP0_FRAMELENGTH',
                        model.vars.fixed_length_size.value + model.vars.header_size_internal.value - 1)
        # Header Configuration
        self._configure_header(model)
        # Payload Configuration
        self._configure_payload_with_header(model)
        # Use FCD0/2 for first subframe then FCD1/3 is used for all following subframes
        self._ip_reg_write(model, 'CTRL_TXFCDMODE',  2)
        self._ip_reg_write(model, 'CTRL_RXFCDMODE',  2)
        return

# Method name: _calc_frame_length_defaults
# Defined in: panther\calculators\calc_frame.py
    def _calc_frame_length_defaults(self, model):
        """_calc_frame_length_defaults
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        self._ip_reg_write(model, 'WCNTCMP0_FRAMELENGTH',  0)
        self._ip_reg_write(model, 'WCNTCMP1_LENGTHFIELDLOC',  0)
        self._ip_reg_write(model, 'DFLCTRL_DFLINCLUDECRC',  0)
        self._ip_reg_write(model, 'DFLCTRL_MINLENGTH',  0)
        self._ip_reg_write(model, 'DFLCTRL_DFLBITS',  0)
        self._ip_reg_write(model, 'DFLCTRL_DFLOFFSET',  0)
        self._ip_reg_write(model, 'DFLCTRL_DFLSHIFT',  0)
        self._ip_reg_write(model, 'DFLCTRL_DFLBITORDER',  0)
        if (model.vars.ber_force_infinite_length.value == True):
            # Infinite length
            self._ip_reg_write(model, 'DFLCTRL_DFLMODE',  5)
        else:
            self._ip_reg_write(model, 'DFLCTRL_DFLMODE',  0)
        # for Panther, do not write this to 0 -- PHYs override it
        self._ip_reg_write(model, 'MAXLENGTH_MAXLENGTH',  0)
# Method name: _configure_fcd
# Defined in: panther\calculators\calc_frame.py
    def _configure_fcd(self, model, fcdindex, excludesubframewcnt = 0, addtrailtxdata = 0, skipwhite = 0,
                                              skipcrc = 0, calccrc = 0, includecrc = 0, buf = 0, words = 0):
        """_configure_fcd
        Args:
            model (ModelRoot) : Data model to read and write variables from
            fcdindex (unknown) : unknown
            excludesubframewcnt (unknown) : unknown
            addtrailtxdata (unknown) : unknown
            skipwhite (unknown) : unknown
            skipcrc (unknown) : unknown
            calccrc (unknown) : unknown
            includecrc (unknown) : unknown
            buf (unknown) : unknown
            words (unknown) : unknown
        """
        # Moved in Panther to FRC_FCDn_* to FRC_FCDn_FCD_*
        crcprecalcsync_rx_mode = model.vars.crcprecalcsync_rx_mode.value

        self._reg_write(eval("model.vars.FRC_FCD{}_EXCLUDESUBFRAMEWCNT".format(fcdindex)), excludesubframewcnt)
        self._reg_write(eval("model.vars.FRC_FCD{}_ADDTRAILTXDATA".format(fcdindex)), addtrailtxdata)
        if model.vars.ber_force_whitening.value == True:
            self._reg_write(eval("model.vars.FRC_FCD{}_SKIPWHITE".format(fcdindex)), 0)
        elif crcprecalcsync_rx_mode != model.vars.crcprecalcsync_rx_mode.var_enum.DISABLED and int(fcdindex) in [0, 2]:
            # FCD0 and 2 (syncword) should not be involved in pre/post whitening if CRCPRECALCSYNC is enabled
            self._reg_write(eval("model.vars.FRC_FCD{}_SKIPWHITE".format(fcdindex)), 1)
        else:
            self._reg_write(eval("model.vars.FRC_FCD{}_SKIPWHITE".format(fcdindex)), skipwhite)
        self._reg_write(eval("model.vars.FRC_FCD{}_SKIPCRC".format(fcdindex)), skipcrc)
        self._reg_write(eval("model.vars.FRC_FCD{}_CALCCRC".format(fcdindex)), calccrc)
        self._reg_write(eval("model.vars.FRC_FCD{}_INCLUDECRC".format(fcdindex)), includecrc)
        self._reg_write(eval("model.vars.FRC_FCD{}_BUFFER".format(fcdindex)), buf)
        self._reg_write(eval("model.vars.FRC_FCD{}_WORDS".format(fcdindex)), words)
        return
# Method name: _configure_fcd_for_frame_type
# Defined in: common\calculators\calc_frame.py
    def _configure_fcd_for_frame_type(self, model):
        # FCDX_WORDS is being set to max value. To figure out the max value, reading the bitwidth.
        # assuming FCD0/1/2/3 will always have same bitwidth in future as well.
        # checking the value for None in case the register does not exist (for e.g. unit_test_part)
        fcdx_words_bitwidth = model.vars.fcdx_words_bitwidth.value

        # Only use one frame descriptor
        fcdDict = {
            "excludesubframewcnt": int(model.vars.payload_excludesubframewcnt_en.value == True),
            "addtrailtxdata": int(model.vars.payload_addtrailtxdata_en.value == True),
            "skipwhite": int(model.vars.payload_white_en.value == False),
            "skipcrc": 0,
            "calccrc": int(model.vars.payload_crc_en.value == True),
            "includecrc": int(model.vars.payload_crc_en.value == True),
            "words": 2 ** fcdx_words_bitwidth - 1,
        }
        #Configure TX FCD
        self._configure_fcd(model, fcdindex="0", buf=0, **fcdDict)
        self._ip_reg_write(model, 'CTRL_TXFCDMODE',  0)
        #Configure RX FCD
        self._configure_fcd(model, fcdindex="2", buf=1, **fcdDict)
        self._ip_reg_write(model, 'CTRL_RXFCDMODE',  0)
        self._configure_fcd(model, 1)   # Turn off this fcd
        self._configure_fcd(model, 3)   # Turn off this fcd
# Method name: _configure_frame_type
# Defined in: common\calculators\calc_frame.py
    def _configure_frame_type(self, model):
        """_configure_frame_type
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        BIT_MASK = {0: 0x00, 1: 0x01, 2: 0x03, 3: 0x07}
        # Handle Code Generation in RAIL Adapter to create C structures
        #Move from discrete inputs to a list
        num_entries = (2**model.vars.frame_type_bits.value)
        model.vars.frame_type_lengths.value = []
        model.vars.frame_type_valid.value = []
        model.vars.frame_type_filter.value = []
        for i in range(num_entries):
          model.vars.frame_type_lengths.value.append(eval("model.vars.frame_type_{}_length.value".format(i)))
          model.vars.frame_type_valid.value.append(eval("model.vars.frame_type_{}_valid.value".format(i)))
          model.vars.frame_type_filter.value.append(eval("model.vars.frame_type_{}_filter.value".format(i)))
        #Set FRC_WCNTCMP0 to the size of the header
        # The seqeuncer will write this register after it decodes the frame type
        # We just want to provide enough room in advance so that we don't complete the frame too early
        # Init to the smallest valid length
        min_size = 0xFF
        for i in range(len(model.vars.frame_type_lengths.value)):
          if (model.vars.frame_type_valid.value[i] == True):
            if (model.vars.frame_type_lengths.value[i] < min_size):
              min_size = model.vars.frame_type_lengths.value[i]
        self._ip_reg_write(model, 'WCNTCMP0_FRAMELENGTH',  min_size - 1)
        model.vars.frame_type_mask.value = BIT_MASK[model.vars.frame_type_bits.value] << model.vars.frame_type_lsbit.value
        return
# Method name: _configure_header
# Defined in: common\calculators\calc_frame.py
    def _configure_header(self, model):
        """_configure_header
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        #Header Configuration
        fcdDict = {
            "excludesubframewcnt": int(model.vars.header_excludesubframewcnt_en.value == True),
            "addtrailtxdata": int(model.vars.header_addtrailtxdata_en.value == True),
            "skipwhite": int(model.vars.header_white_en.value == False),
            "skipcrc": 0,
            "calccrc": int(model.vars.header_calc_crc.value == True),
            "includecrc": int(model.vars.header_include_crc.value == True),
            "words": model.vars.header_size_internal.value - 1,
        }
        #Configure TX FCD
        self._configure_fcd(model, fcdindex="0", buf=0, **fcdDict)
        #Configure RX FCD
        self._configure_fcd(model, fcdindex="2", buf=1, **fcdDict)
        return
# Method name: _configure_payload_with_header
# Defined in: common\calculators\calc_frame.py
    def _configure_payload_with_header(self, model):
        """_configure_payload_with_header
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # FCDX_WORDS is being set to max value. To figure out the max value, reading the bitwidth.
        # assuming FCD0/1/2/3 will always have same bitwidth in future as well.
        # checking the value for None in case the register does not exist (for e.g. unit_test_part)
        fcdx_words_bitwidth = model.vars.fcdx_words_bitwidth.value

        #Payload Configuration
        fcdDict = {
            "excludesubframewcnt": int(model.vars.payload_excludesubframewcnt_en.value == True),
            "addtrailtxdata": int(model.vars.payload_addtrailtxdata_en.value == True),
            "skipwhite": int(model.vars.payload_white_en.value == False),
            "skipcrc": 0,
            "calccrc": int(model.vars.payload_crc_en.value == True),
            "includecrc": int(model.vars.payload_crc_en.value == True),
            "words": 2 ** fcdx_words_bitwidth - 1,
        }
        #Configure TX FCD
        self._configure_fcd(model, fcdindex="1", buf=0, **fcdDict)
        #Configure RX FCD
        self._configure_fcd(model, fcdindex="3", buf=1, **fcdDict)
        return
# Method name: _configure_variable_length
# Defined in: common\calculators\calc_frame.py
    def _configure_variable_length(self, model):
        """_configure_variable_length
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        self._ip_reg_write(model, 'WCNTCMP0_FRAMELENGTH',  0)
        self._ip_reg_write(model, 'WCNTCMP1_LENGTHFIELDLOC',  model.vars.var_length_loc.value)
        self._ip_reg_write(model, 'MAXLENGTH_MAXLENGTH',  model.vars.var_length_maxlength.value + model.vars.header_size_internal.value + model.vars.var_length_adjust.value-1)
        self._ip_reg_write(model, 'DFLCTRL_DFLINCLUDECRC',  int(model.vars.var_length_includecrc.value == True))
        self._ip_reg_write(model, 'DFLCTRL_MINLENGTH',  model.vars.var_length_minlength.value+model.vars.header_size_internal.value + model.vars.var_length_adjust.value-1)
        self._ip_reg_write(model, 'DFLCTRL_DFLBITS',  model.vars.var_length_numbits.value)

        self._ip_reg_write(model, 'DFLCTRL_DFLOFFSET',  model.vars.header_size_internal.value + model.vars.var_length_adjust.value-1, allow_neg=True)
        self._ip_reg_write(model, 'DFLCTRL_DFLSHIFT',  model.vars.var_length_shift.value)
        if (model.vars.var_length_bitendian.value.value != model.vars.frame_bitendian.value.value):
            self._ip_reg_write(model, 'DFLCTRL_DFLBITORDER',  1)
        else:
            self._ip_reg_write(model, 'DFLCTRL_DFLBITORDER',  0)
        #DFLMODE
        if (model.vars.ber_force_infinite_length.value == True):
            # Infinite length
            self._ip_reg_write(model, 'DFLCTRL_DFLMODE',  5)
        elif (model.vars.var_length_numbytes.value == 1):
            #SINGLEBYTE
            self._ip_reg_write(model, 'DFLCTRL_DFLMODE',  1)
        else: #Two bytes
            if (model.vars.var_length_byteendian.value == model.vars.var_length_byteendian.var_enum.LSB_FIRST):
                #DUALBYTELSBFIRST
                self._ip_reg_write(model, 'DFLCTRL_DFLMODE',  3)
            else:
                #DUALBYTEMSBFIRST
                self._ip_reg_write(model, 'DFLCTRL_DFLMODE',  4)
        return

    def calc_fcdx_words_bitwidth(self, model):
        # This is the bitwidth for FCDX_WORDS
        # check if the register is part of the register model, e.g. unit_test_part does not
        if model.vars.FRC_FCD0_WORDS.rm is None:
            val = 13
        else:
            val = model.vars.FRC_FCD0_WORDS.get_bit_width()
        model.vars.fcdx_words_bitwidth.value = val

    def calc_crcprecalcsync_reg(self, model):
        # Set default value to disabled if not defined
        model.vars.crcprecalcsync_rx_mode.value = model.vars.crcprecalcsync_rx_mode.var_enum.DISABLED
        crcprecalcsync = model.vars.crcprecalcsync_rx_mode.value    # Read back for final defined value

        if crcprecalcsync == model.vars.crcprecalcsync_rx_mode.var_enum.DISABLED:
            crcprecalcsync = 0
        elif crcprecalcsync == model.vars.crcprecalcsync_rx_mode.var_enum.ENABLED:
            crcprecalcsync = 1
            self._verify_crcprecalcsync_header_vars(model)
        elif model.vars.crcprecalcsync_rx_mode.var_enum.ENABLEDSTORE:
            crcprecalcsync = 2
            self._verify_crcprecalcsync_header_vars(model)

        self._ip_reg_write(model, 'RXCTRL_CRCPRECALCSYNC',  crcprecalcsync)

    def _verify_crcprecalcsync_header_vars(self, model):
        """CRCPRECALCSYNC > 0 pushes syncword into FCD2, hence header must be enabled"""
        header_en = model.vars.header_en.value
        header_size_internal = model.vars.header_size_internal.value
        firstframe_bitsperword = model.vars.firstframe_bitsperword.value
        syncword_length = model.vars.syncword_length.value

        if not header_en:
            raise CalculationException("ERROR: CRCPRECALCSYNC is enabled but header_en is set to 0")

        if syncword_length != (header_size_internal * firstframe_bitsperword):
            raise CalculationException("Error: CRCPRECALCSYNC is enabled but syncword_length does not equal header_size * bitsperword")


