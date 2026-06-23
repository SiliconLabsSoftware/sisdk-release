from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
import math

class CalcFec(IPCalculator):
    # Method name: calc_convdecodemode_reg
    # Defined in: ocelot\calculators\calc_fec.py
    def calc_convdecodemode_reg(self, model):
        # This function calculates the CONVDECODEMODE (hard vs soft decision symbols)
        # Assign inputs to variables
        fec_en = model.vars.fec_en.value
        fec_enabled = model.vars.fec_enabled.value
        if fec_enabled or (fec_en not in [model.vars.fec_en.var_enum.NONE, model.vars.fec_en.var_enum.FEC_BLE_HDT]):
            convdecodemode = 1  # hard decision (default in most cases)
        else:
            convdecodemode = 0
        # Write the register
        self._ip_reg_write(model, 'FECCTRL_CONVDECODEMODE', convdecodemode)

    # Method name: calc_convgenerator_recursive_reg
    # Defined in: common\calculators\calc_fec.py
    def calc_convgenerator_recursive_reg(self, model):
        # This function calculates the FRC_CONVGENERATOR_RECURSIVE reg field
        # Read in model variables
        fec_en = model.vars.fec_en.value
        if (fec_en == model.vars.fec_en.var_enum.FEC_154G_RSC_INTERLEAVING) or (
                fec_en == model.vars.fec_en.var_enum.FEC_154G_RSC_NO_INTERLEAVING):
            recursive = 1
        else:
            recursive = 0
        # Load value into register
        self._ip_reg_write(model, 'CONVGENERATOR_RECURSIVE', recursive)

    # Method name: calc_convolutional_decoder_buffer_size
    # Defined in: common\calculators\calc_fec.py
    def calc_convolutional_decoder_buffer_size(self, model):
        """
        calc_convolutional_decoder_buffer_size
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # This whole calculation only applies if convolutional Encoder/Decoder is enabled
        if model.vars.FRC_FECCTRL_CONVMODE != 0:
            # From Reference Manual, section 5.8.16.4 Convolutional decoder,
            # 'Convolutional decoding RAM buffer size' table
            # Constraint length : RAM size (bytes)
            convDecodRamBufSize = {0: 0,
                                   1: 0,
                                   2: 16,
                                   3: 32,
                                   4: 64,
                                   5: 128,
                                   6: 384,
                                   7: 768}
            # Get the value set in FRC_CONVGENERATOR_GENERATOR0/1
            generator0 = model.vars.FRC_CONVGENERATOR_GENERATOR0.value
            generator1 = model.vars.FRC_CONVGENERATOR_GENERATOR1.value
            # Make sure the values are >= 1
            generator0 = 1 if generator0 < 1 else generator0
            generator1 = 1 if generator1 < 1 else generator1
            # Get the MSB set in the generator0/generator1 variables
            # We use ceil to round up any fractional value
            generator0_constraintLength = int(math.ceil(math.log(generator0, 2)))
            generator1_constraintLength = int(math.ceil(math.log(generator1, 2)))
            # Get the larger of the two MSBs obtained in the previous step and use that
            # as the key to lookup the required buffer size in convDecodRamBufSize dict
            constraintLength = max(generator0_constraintLength, generator1_constraintLength)
            model.vars.frc_conv_decoder_buffer_size.value = convDecodRamBufSize[constraintLength]

    # Method name: calc_fec
    # Defined in: ocelot\calculators\calc_fec.py
    def calc_fec(self, model):
        # Need override method here due to added FEC_K7_INTERLEAVING case
        model.vars.fec_en.value = model.vars.fec_en.var_enum.NONE  # Calculate a default value for Profiles where this is an advanced input
        # Always initialize FEC regs to these values
        self._calc_init(model)
        # IF FEC is enabled then write the 802.15.4g base values
        if model.vars.fec_en.value != model.vars.fec_en.var_enum.NONE:
            if model.vars.fec_en.value == model.vars.fec_en.var_enum.FEC_BLE_HDT:
                self._ip_reg_write(model, 'FECCTRL_CONVBUSLOCK', 0)
                self._ip_reg_write(model, 'FECCTRL_CONVHARDERROR', 0)
                self._ip_reg_write(model, 'FECCTRL_CONVSUBFRAMETERMINATE', 0)
                self._ip_reg_write(model, 'FECCTRL_CONVTRACEBACKDISABLE', 0)
                self._ip_reg_write(model, 'FECCTRL_FORCE2FSK', 0)
                self._ip_reg_write(model, 'FECCTRL_INTERLEAVEFIRSTINDEX', 0)
                self._ip_reg_write(model, 'FECCTRL_SINGLEBLOCK', 0)
                self._ip_reg_write(model, 'FECCTRL_BITORDERMAP', 1)

                self._ip_reg_write(model, 'CONVGENERATOR_GENERATOR0', 0x2f)
                self._ip_reg_write(model, 'CONVGENERATOR_GENERATOR1', 0x35)

                self._ip_reg_write(model, 'PUNCTCTRL_PUNCT0', 1)
                self._ip_reg_write(model, 'PUNCTCTRL_PUNCT1', 1)

            if model.vars.fec_en.value in [model.vars.fec_en.var_enum.FEC_154G_NRNSC_INTERLEAVING,
                                           model.vars.fec_en.var_enum.FEC_154G_RSC_INTERLEAVING,
                                           model.vars.fec_en.var_enum.FEC_154G_RSC_NO_INTERLEAVING,
                                           model.vars.fec_en.var_enum.FEC_K7_INTERLEAVING]:
                self._ip_reg_write(model, 'FECCTRL_CONVTRACEBACKDISABLE', 0)
                self._ip_reg_write(model, 'FECCTRL_INTERLEAVEFIRSTINDEX', 0)
                self._ip_reg_write(model, 'FECCTRL_CONVBUSLOCK', 0)
                self._ip_reg_write(model, 'FECCTRL_CONVSUBFRAMETERMINATE', 0)
                self._ip_reg_write(model, 'FECCTRL_SINGLEBLOCK', 0)
                self._ip_reg_write(model, 'FECCTRL_FORCE2FSK', 0)
                self._ip_reg_write(model, 'FECCTRL_CONVHARDERROR', 0)

                self._ip_reg_write(model, 'CONVGENERATOR_GENERATOR0', 0x0F)
                self._ip_reg_write(model, 'CONVGENERATOR_GENERATOR1', 0x0D)
                self._ip_reg_write(model, 'CONVGENERATOR_NONSYSTEMATIC', 0)

                self._ip_reg_write(model, 'PUNCTCTRL_PUNCT0', 1)
                self._ip_reg_write(model, 'PUNCTCTRL_PUNCT1', 1)
                # : FEC_154G_Base uses K=4 by default. Override code to K=7 case.
                if model.vars.fec_en.value == model.vars.fec_en.var_enum.FEC_K7_INTERLEAVING:
                    self._ip_reg_write(model, 'CONVGENERATOR_GENERATOR0', 0x6D)
                    self._ip_reg_write(model, 'CONVGENERATOR_GENERATOR1', 0x4F)

    # Method name: calc_fec_enabled
    # Defined in: ocelot\calculators\calc_fec.py
    def calc_fec_enabled(self, model):
        model.vars.fec_enabled.value = int(model.vars.FRC_FECCTRL_CONVMODE.value != 0)

    # Method name: calc_fec_tx_enable
    # Defined in: common\calculators\calc_fec.py
    def calc_fec_tx_enable(self, model):
        # This function enables or disables FEC in TX
        # It is used so that we can configure FEC type with fec_en but still disable on TX if desired
        # Read in model variables
        fec_en = model.vars.fec_en.value
        # By default enable FEC TX whenever a customer selects a fec_en setting that is not NONE
        if fec_en != model.vars.fec_en.var_enum.NONE:
            fec_tx_enable = model.vars.fec_tx_enable.var_enum.ENABLED
        else:
            fec_tx_enable = model.vars.fec_tx_enable.var_enum.DISABLED
        # Write the variable
        model.vars.fec_tx_enable.value = fec_tx_enable

    # Method name: calc_feccrl_interleavemode_reg
    # Defined in: ocelot\calculators\calc_fec.py
    def calc_feccrl_interleavemode_reg(self, model):
        # This function calculates the FRC_FECCTRL_INTERLEAVEMODE reg field
        # A unique version is needed here due to the added FEC_K7_INTERLEAVING mode
        # Read in model variables
        fec_en = model.vars.fec_en.value
        fec_enabled = model.vars.fec_enabled.value
        # For dynamic FEC case, RAIL will handle reading in this interleavemode and enabling RX buffering
        # (changing to interleavemode=2) as needed
        if fec_enabled:
            if (fec_en == model.vars.fec_en.var_enum.FEC_154G_NRNSC_INTERLEAVING) or \
                    (fec_en == model.vars.fec_en.var_enum.FEC_154G_RSC_INTERLEAVING) or \
                    (fec_en == model.vars.fec_en.var_enum.FEC_K7_INTERLEAVING):
                # We need to turn on interleaving to TX properly
                interleavemode = 1
            else:
                interleavemode = 0
        else:
            interleavemode = 0
        # Load value into register
        self._ip_reg_write(model, 'FECCTRL_INTERLEAVEMODE', interleavemode)

    # Method name: calc_fecctrl_convinv_reg
    # Defined in: common\calculators\calc_fec.py
    def calc_fecctrl_convinv_reg(self, model):
        # This function calculates the FRC_FECCTRL_CONVINV reg field
        # Read in model variables
        fec_en = model.vars.fec_en.value
        # Calculate the output bits to invert based on the fec_en mode
        if fec_en == model.vars.fec_en.var_enum.FEC_154G_NRNSC_INTERLEAVING:
            convinv = 3  # Invert both bits
        else:
            convinv = 0
        # Write the register
        self._ip_reg_write(model, 'FECCTRL_CONVINV', convinv)

    # Method name: calc_fecctrl_convmode_reg
    # Defined in: common\calculators\calc_fec.py
    def calc_fecctrl_convmode_reg(self, model):
        # This function calculates the CONVMODE field
        # Read in model variables
        fec_tx_enable = (model.vars.fec_tx_enable.value == model.vars.fec_tx_enable.var_enum.ENABLED)
        # Calculate the register
        if fec_tx_enable:
            convmode = 1
        else:
            convmode = 0
        # Set the register
        self._ip_reg_write(model, 'FECCTRL_CONVMODE', convmode)

    # Method name: calc_fecctrl_interleavewidth_reg
    # Defined in: common\calculators\calc_fec.py
    def calc_fecctrl_interleavewidth_reg(self, model):
        # This function calculates the FRC_FECCTRL_INTERLEAVEWIDTH reg field
        # Read in model variables
        modulation_type = model.vars.modulation_type.value
        fec_en = model.vars.fec_en.value
        if fec_en not in [model.vars.fec_en.var_enum.NONE, model.vars.fec_en.var_enum.FEC_BLE_HDT]:
            if modulation_type == model.vars.modulation_type.var_enum.FSK2:
                interleavewidth = 1
            elif modulation_type == model.vars.modulation_type.var_enum.FSK4:
                interleavewidth = 0
            else:
                interleavewidth = 0
        else:
            interleavewidth = 0
        # Load value into register
        self._ip_reg_write(model, 'FECCTRL_INTERLEAVEWIDTH', interleavewidth)

    # Method name: calc_postamble_regs
    # Defined in: ocelot\calculators\calc_fec.py
    def calc_postamble_regs(self, model):
        # This function calculate  registers to configure the postamble of PHYs with FEC enabled and
        # Mbus Mode T/Mode S/Mode R PHYs. All other PHYs are not affected
        # Write the Mbus postamble length as 0 by default (overridden by Mbus Profile Input)
        model.vars.mbus_postamble_length.value = 0
        mbus_symbol_encoding = model.vars.mbus_symbol_encoding.value
        profile = model.profile.name.lower()
        fec_enable = model.vars.fec_en.value
        postamble_length = model.vars.mbus_postamble_length.value
        if profile == 'mbus':
            if mbus_symbol_encoding == model.vars.mbus_symbol_encoding.var_enum.Manchester:
                trailtxdataforce = 1
                trailtxdata = 0xff
                postambleen = 0
                trailtxreplen = 0
                # model.vars.FRC_TRAILTXDATACTRL_TRAILTXDATACNT.value_forced = 0  # shortest allowed postamble is 2 chip
                # Setting total number of chips, Due to Manchester encoding
                # the actual number of chips used is (FRC_TRAILTXDATACTRL_TRAILTXDATACNT + 1)*2
                if postamble_length == 1:
                    trailtxdatacnt = 0
                elif postamble_length == 2:
                    trailtxdatacnt = 1
                elif postamble_length == 3:
                    trailtxdatacnt = 2
                elif postamble_length == 4:
                    trailtxdatacnt = 3
                else:
                    trailtxdatacnt = 0
            elif mbus_symbol_encoding == model.vars.mbus_symbol_encoding.var_enum.MBUS_3OF6:
                trailtxdataforce = 1
                trailtxdata = 0
                postambleen = 1
                trailtxreplen = 0
                # Setting total number of chips, the actual number of chips used is FRC_TRAILTXDATACTRL_TRAILTXDATACNT + 1
                if postamble_length == 1:
                    trailtxdatacnt = 1
                elif postamble_length == 2:
                    trailtxdatacnt = 3
                elif postamble_length == 3:
                    trailtxdatacnt = 5
                elif postamble_length == 4:
                    trailtxdatacnt = 7
                else:
                    trailtxdatacnt = 1
            else:
                trailtxdataforce = 0
                trailtxdata = 0
                trailtxdatacnt = 0
                postambleen = 0
                trailtxreplen = 0
        elif fec_enable != model.vars.fec_en.var_enum.NONE:
            trailtxdata = 0x0B
            trailtxdatacnt = 0
            postambleen = 0
            trailtxdataforce = 0
            trailtxreplen = 0
        else:
            trailtxdataforce = 0
            trailtxdata = 0
            trailtxdatacnt = 0
            postambleen = 0
            trailtxreplen = 0
        self._ip_reg_write(model, 'TRAILTXDATACTRL_TRAILTXDATA', trailtxdata)
        self._ip_reg_write(model, 'TRAILTXDATACTRL_TRAILTXDATAFORCE', trailtxdataforce)
        self._ip_reg_write(model, 'TRAILTXDATACTRL_POSTAMBLEEN', postambleen)
        self._ip_reg_write(model, 'TRAILTXDATACTRL_TRAILTXDATACNT', trailtxdatacnt)
        self._ip_reg_write(model, 'TRAILTXDATACTRL_TRAILTXREPLEN', trailtxreplen)

    # Method name: _build_frc_reg_var
    # Defined in: lpwh72000\calculators\calc_fec.py
    def _build_frc_reg_var(self, model):
        pass

    # Method name: _calc_init
    # Defined in: common\calculators\calc_fec.py
    def _calc_init(self, model):
        # Need to override this method in order to instead set CONVMODE elsewhere
        self._ip_reg_write(model, 'FECCTRL_CONVTRACEBACKDISABLE', 0)
        self._ip_reg_write(model, 'FECCTRL_INTERLEAVEFIRSTINDEX', 0)
        self._ip_reg_write(model, 'FECCTRL_CONVBUSLOCK', 0)
        self._ip_reg_write(model, 'FECCTRL_CONVSUBFRAMETERMINATE', 0)
        self._ip_reg_write(model, 'FECCTRL_SINGLEBLOCK', 0)
        self._ip_reg_write(model, 'FECCTRL_FORCE2FSK', 0)
        self._ip_reg_write(model, 'FECCTRL_CONVHARDERROR', 0)
        self._ip_reg_write(model, 'CONVGENERATOR_GENERATOR0', 0)
        self._ip_reg_write(model, 'CONVGENERATOR_GENERATOR1', 0)
        self._ip_reg_write(model, 'CONVGENERATOR_NONSYSTEMATIC', 0)
        self._ip_reg_write(model, 'PUNCTCTRL_PUNCT0', 0)
        self._ip_reg_write(model, 'PUNCTCTRL_PUNCT1', 0)
        self._ip_reg_write_default(model, 'FECCTRL_BITORDERMAP')