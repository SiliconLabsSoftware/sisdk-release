from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
from pyradioconfig.parts.common.calculators.calc_frame_detect import CALC_Frame_Detect as CALC_Frame_Detect_Common
from math import ceil, floor, log
from py_2_and_3_compatibility import *


class CalcModMisc(IPCalculator):

    def calc_mod_misc(self, model):
        self._ip_reg_write_default(model, "TXCTRL_TXENDTIMER")

    def calc_mod_default(self, model):
        #TODO: why are these needed?
        model.vars.tx_modulation_type.value = model.vars.modulation_type.value
        model.vars.tx_manchester_mapping.value = model.vars.manchester_mapping.value
        model.vars.tx_fsk_symbol_map.value = model.vars.fsk_symbol_map.value
        model.vars.tx_symbol_encoding.value = model.vars.symbol_encoding.value
        model.vars.tx_diff_encoding_mode.value = model.vars.diff_encoding_mode.value

        model.vars.tx_dsss_shifts.value = model.vars.dsss_shifts.value
        model.vars.tx_dsss_len.value = model.vars.dsss_len.value
        model.vars.tx_dsss_chipping_code.value = model.vars.dsss_chipping_code.value

        model.vars.tx_preamble_length.value = model.vars.preamble_length.value
        model.vars.tx_preamble_pattern_len.value = model.vars.preamble_pattern_len.value
        model.vars.tx_preamble_pattern.value = model.vars.preamble_pattern.value

        model.vars.tx_syncword_length.value = model.vars.syncword_length.value
        model.vars.tx_syncword_0.value = model.vars.syncword_0.value
        model.vars.tx_syncword_1.value = model.vars.syncword_1.value

    def calc_tx_mapfsk_mod_reg(self, model):

        mod_format = model.vars.modulation_type.value
        manchester_map = model.vars.manchester_mapping.value
        fsk_map = model.vars.fsk_symbol_map.value
        encoding = model.vars.symbol_encoding.value

        FSKMAP_LOOKUP = {
            model.vars.fsk_symbol_map.var_enum.MAP0.value: 0,
            model.vars.fsk_symbol_map.var_enum.MAP1.value: 1,
            model.vars.fsk_symbol_map.var_enum.MAP2.value: 2,
            model.vars.fsk_symbol_map.var_enum.MAP3.value: 3,
            model.vars.fsk_symbol_map.var_enum.MAP4.value: 4,
            model.vars.fsk_symbol_map.var_enum.MAP5.value: 5,
            model.vars.fsk_symbol_map.var_enum.MAP6.value: 6,
            model.vars.fsk_symbol_map.var_enum.MAP7.value: 7,
        }

        mapfsk = FSKMAP_LOOKUP[fsk_map.value]

        if mod_format != model.vars.modulation_type.var_enum.FSK4:
            # if we're using Manchester encoding (or any FSK modulation actually),
            # then only MAP0 and MAP1 are valid
            if mapfsk > 1:
                raise CalculationException("Invalid fsk symbol map value for modulation type selected.")

        if encoding == model.vars.symbol_encoding.var_enum.Manchester or \
                encoding == model.vars.symbol_encoding.var_enum.Inv_Manchester:
            # if we're using Manchester encoding,
            # then only MAP0 and MAP1 are valid
            if mapfsk > 1:
                raise CalculationException("Invalid fsk_symbol_map value for Manchester encoding")

            # if we're using inverted Manchester encoding, then flip the polarity of the fsk
            # map.  This flips the polarity of the entire transmission, including the preamble
            # and syncword.  We don't want the preamble and syncword flipped, so we'll invert those
            # registers elsewhere
            if manchester_map != model.vars.manchester_mapping.var_enum.Default:
                mapfsk ^= 1

        self._ip_reg_write(model, 'CTRL0_MAPFSK', mapfsk)

    def calc_tx_symbol_encoding_mod(self, model):

        encoding = model.vars.tx_symbol_encoding.value
        demod_select = model.vars.demod_select.value

        if encoding == model.vars.tx_symbol_encoding.var_enum.DSSS:
            coding = 2
        elif (encoding == model.vars.tx_symbol_encoding.var_enum.Manchester or
                encoding == model.vars.tx_symbol_encoding.var_enum.Inv_Manchester) and\
                demod_select != model.vars.demod_select.var_enum.TRECS_VITERBI:
            # Decoder not implemented with Viterbi demod
            # See https://jira.silabs.com/browse/MCUW_RADIO_CFG-2046
            coding = 1
        else:
            coding = 0

        self._ip_reg_write(model, 'CTRL0_CODING',  coding)

    def calc_tx_mod_type_mod_reg(self, model):
        #This function writes the modulation type register

        #Load model variables into local variables
        modformat = model.vars.tx_modulation_type.value

        if modformat == model.vars.tx_modulation_type.var_enum.FSK2 or \
                modformat == model.vars.tx_modulation_type.var_enum.MSK:
            mod = 0
        elif modformat == model.vars.tx_modulation_type.var_enum.FSK4:
            mod = 1
        elif modformat == model.vars.tx_modulation_type.var_enum.BPSK:
            mod = 2
        elif modformat == model.vars.tx_modulation_type.var_enum.DBPSK:
            mod = 3
        elif modformat == model.vars.tx_modulation_type.var_enum.OQPSK:
            mod = 4
        elif modformat == model.vars.tx_modulation_type.var_enum.OOK or \
                modformat == model.vars.tx_modulation_type.var_enum.ASK:
            mod = 6
        else:
            raise CalculationException('ERROR: modulation method in input file not recognized')

        #Write register
        self._ip_reg_write(model, 'CTRL0_MODFORMAT', mod)

    def calc_ctrl0_ook_asyncpin_mod(self, model):
        self._ip_reg_write(model, 'CTRL0_OOKASYNCPIN', 0)

    def calc_tx_dsssshifts_mod_reg(self, model):
        """
        write DSSS cyclic shifts number to generate new symbols when using DSSS

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        val = model.vars.tx_dsss_shifts.value

        if val == 0:
            reg = 0
        elif val == 1:
            reg = 1
        elif val == 2:
            reg = 2
        elif val == 4:
            reg = 3
        elif val == 8:
            reg = 4
        elif val == 16:
            reg = 5
        else:
            raise CalculationException("Invalid dsss_shift value!")
            return

        self._ip_reg_write(model, 'CTRL0_DSSSSHIFTS', reg)

    def calc_tx_dsssshifts_mod_actual(self, model):
        """
        given register setting return actual DSSS shifts value

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        reg = model.vars.MOD_CTRL0_DSSSSHIFTS.value

        if reg == 0:
            val = 0
        elif reg == 1:
            val = 1
        elif reg == 2:
            val = 2
        elif reg == 3:
            val = 4
        elif reg == 4:
            val = 8
        elif reg == 5:
            val = 16

        model.vars.tx_dsss_shifts_actual.value = val

    def calc_tx_dssslen_mod_reg(self, model):
        """
        set DSSS length register

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        length = model.vars.tx_dsss_len.value
        shifts = model.vars.tx_dsss_shifts_actual.value

        if length == 0:
            reg = 0
        else:
            if shifts == 0:
                if length < 4 or length > 32:
                    raise CalculationException("dsss_shift value must be between 4 and 32")
                    return
            else:
                if not length % shifts == 0:
                    raise CalculationException("dsss_len must be an integer multiple of dsss_shifts")
                    return
            reg = length - 1

        self._ip_reg_write(model, 'CTRL0_DSSSLEN', reg)

    def calc_tx_dssslen_mod_actual(self, model):
        """
        given register setting return actual DSSS length

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        dsss0 = model.vars.MOD_DSSS0_DSSS0.value
        dssslen = model.vars.MOD_CTRL0_DSSSLEN.value

        if dsss0 == 0:
            len = 0
        else:
            len = dssslen + 1

        model.vars.tx_dsss_len_actual.value = len

    def calc_tx_dsssdouble_mod_reg(self, model):
        """
        based on modulation used select if DSSS symbol's inverted version
        should also be a DSSS symbol

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        length = model.vars.tx_dsss_len.value
        modulation = model.vars.tx_modulation_type.value

        if length > 0:
            if modulation == model.vars.tx_modulation_type.var_enum.OQPSK:
                dsssdouble = 2
            else:
                dsssdouble = 1
        else:
            dsssdouble = 0

        self._ip_reg_write(model, 'CTRL0_DSSSDOUBLE', dsssdouble)

    def calc_diffencmode_mod_reg(self, model):
        """

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        DIFFENCMODE_LOOKUP = {
            model.vars.tx_diff_encoding_mode.var_enum.DISABLED.value:  0,
            model.vars.tx_diff_encoding_mode.var_enum.RR0.value:  1,
            model.vars.tx_diff_encoding_mode.var_enum.RE0.value:  2,
            model.vars.tx_diff_encoding_mode.var_enum.RR1.value:  3,
            model.vars.tx_diff_encoding_mode.var_enum.RE1.value:  4,
        }

        self._ip_reg_write(model, 'CTRL0_DIFFENCMODE',
                       DIFFENCMODE_LOOKUP[(model.vars.tx_diff_encoding_mode.value).value])

    def calc_syncbits_mod_reg(self, model):
        """
        write sync word length from input to register

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        syncword_length = model.vars.tx_syncword_length.value

        if syncword_length < 2:
            LogMgr.Error("Syncword length must be at least 2")

        # FIXME: amtudave: Remove SYNCBITS once tri-sync control added to sync_det
        self._ip_reg_write(model, 'CTRL1_SYNCBITS', syncword_length - 1)

    def calc_txsync_mod_reg(self, model):
        #This function calculates what syncword to transmit when using dualsync

        #Always use syncword0 to transmit by default
        self._ip_reg_write(model, 'CTRL1_TXSYNC', 0)

    def calc_syncword_tx_mod_skip(self, model):
        if model.vars.syncword_tx_skip.value:
            self._ip_reg_write(model, 'CTRL1_SYNCDATA', 1)
        else:
            self._ip_reg_write(model, 'CTRL1_SYNCDATA', 0)

    def calc_txpinmode_mod_reg(self, model):
        self._ip_reg_write(model, 'CTRL2_TXPINMODE', 0)

    def calc_brdiv_devmult_mod_reg(self, model):
        self._ip_reg_write(model, 'CTRL2_BRDIVA', 0)
        self._ip_reg_write(model, 'CTRL2_BRDIVB', 0)
        self._ip_reg_write(model, 'CTRL2_DEVMULA', 0)
        self._ip_reg_write(model, 'CTRL2_DEVMULB', 0)

    def calc_rateselmode_mod_reg(self, model):
        self._ip_reg_write(model, 'CTRL2_RATESELMODE', 0)

    def calc_prsdinen_mod_reg(self, model):
        self._ip_reg_write(model, 'CTRL3_PRSDINEN', 0)

    def calc_predistavg_mod_reg(self, model):
        self._ip_reg_write(model, 'CTRL4_PREDISTAVG', 0)

    def calc_codingb_mod_reg(self, model):
        self._ip_reg_write(model, 'CTRL6_CODINGB', 0)

    def calc_txdbpsk_mod_reg(self, model):
        self._ip_reg_write(model, 'CTRL6_TXDBPSKINV', 0)
        self._ip_reg_write(model, 'CTRL6_TXDBPSKRAMPEN', 0)

    def calc_tx_base_mod_reg(self, model):
        """
        set BASE register using input
        The bits have to be flipped around before writing the register

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        preamble_pattern_len = model.vars.tx_preamble_pattern_len.value
        preamble_pattern = model.vars.tx_preamble_pattern.value

        # When manchester invert is selected, then elsewhere we flip the entire fsk mapping,
        # which also flips the preamble and sync word.  We don't want the the preamble and
        # syncword flipped, so to fix it, we invert the preamble pattern and sync word register
        # to undo the fsk mapping flip.
        encoding = model.vars.tx_symbol_encoding.value
        manchester_map = model.vars.tx_manchester_mapping.value
        if encoding == model.vars.tx_symbol_encoding.var_enum.Inv_Manchester:
            preamble_pattern_mask = (1 << preamble_pattern_len) - 1
            preamble_pattern ^= preamble_pattern_mask

        mod_pre_base = CALC_Frame_Detect_Common.flip_bits(preamble_pattern, preamble_pattern_len)
        mod_pre_base = int(mod_pre_base)

        self._ip_reg_write(model, 'PRE_BASE', mod_pre_base)

    def calc_tx_basebits_mod_reg(self, model):
        """
        set BASEBITS register using input

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        basebits = model.vars.tx_preamble_pattern_len.value

        if basebits > 0:
            reg = basebits - 1
        else:
            reg = 0

        self._ip_reg_write(model, 'PRE_BASEBITS', reg)

    def calc_tx_pre_mod_misc(self, model):
        self._ip_reg_write(model, 'PRE_DSSSPRE', 0)
        self._ip_reg_write(model, 'PRE_PRESYMB4FSK', 0)
        self._ip_reg_write(model, 'PRE_SYNCSYMB4FSK', 0)

    def calc_tx_basebits_mod_actual(self, model):
        """
        return actual base bits

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        model.vars.tx_preamble_pattern_len_actual.value = model.vars.MOD_PRE_BASEBITS.value + 1

    def calc_txbases_mod_reg(self, model):

        #Read in model variables
        preamble_length = model.vars.tx_preamble_length.value #This is the TX preamble length
        preamble_pattern_len_actual = model.vars.tx_preamble_pattern_len_actual.value

        #Calculate txbases
        txbases = preamble_length / preamble_pattern_len_actual

        #Limit checking
        if (txbases) > 0xffff:
            raise CalculationException("Calculated TX preamble sequences (TXBASE) value of %s exceeds limit of 65535! Adjust preamble inputs." % txbases )

        #Write the register
        self._ip_reg_write(model, 'PRE_TXBASES', int(txbases))

    def calc_tx_dsss0_mod_reg(self, model):
        """
        write DSSS symbol 0 register

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        self._ip_reg_write(model, 'DSSS0_DSSS0', model.vars.tx_dsss_chipping_code.value)

    def calc_OOKSHPING_mod_misc(self, model):
        # self._ip_reg_write(model, 'OOKSHAPING_OOKSHAPINGEN', 0)
        # self._ip_reg_write(model, 'OOKSHAPING_OOKSHAPINGLUTSIZE', 0)
        # self._ip_reg_write(model, 'OOKSHAPING_OOKSHAPINGSTEP', 0)
        pass

    def calc_tx_aox_mod_misc(self, model):
        # Always force these to zero so all AoX features are disabled.
        # RAIL will dynamically set these when an AoX  packet is detected.
        # Still write them in the RC so other PHYs are guarenteed to have AoX features disabled and we can
        # exclude ETSLOC, ANTSWTIMSTART, ANTSWTIMSTOP
        self._ip_reg_write(model, 'ANTSWCTRL_ANTSWENABLE', 0)
        self._ip_reg_write(model, 'ANTSWCTRL_CFGANTPATTEN', 0)
        # self._ip_reg_write(model, 'ETSCTRL_CAPTRIG', 0)
        # self._ip_reg_write(model, 'ETSCTRL_ETSLOC', 0)
        # self._ip_reg_write(model, 'ANTSWCTRL1_TIMEPERIOD', 436906)
        self._ip_reg_write(model, 'ANTSWCTRL_ANTCOUNT', 0)
        self._ip_reg_write(model, 'ANTSWCTRL_ANTDFLTSEL', 0)
        self._ip_reg_write(model, 'ANTSWCTRL_ANTSWTYPE', 0)
        self._ip_reg_write(model, 'ANTSWCTRL_EXTDSTOPPULSECNT', 30)
        self._ip_reg_write(model, 'ANTSWEND_ANTSWENDTIM', 0)
        self._ip_reg_write(model, 'ANTSWSTART_ANTSWSTARTTIM', 0)
        self._ip_reg_write(model, 'CFGANTPATT_CFGANTPATTVAL', 0)

    def calc_sync_words_mod_reg(self, model):
        """
        write sync words from input to registers

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        syncword_length = model.vars.tx_syncword_length.value
        syncword0_reg = long(CALC_Frame_Detect_Common.flip_bits(model.vars.tx_syncword_0.value, syncword_length))
        syncword1_reg = long(CALC_Frame_Detect_Common.flip_bits(model.vars.tx_syncword_1.value, syncword_length))

        if model.vars.ber_force_sync.value == True:
            syncword0_reg = long(0x1dd3d4a0)  # gdc:  Fix this after we get rid of the "_left" stuff above.
            # gdc:  Fix it so we just write syncword_0 before it gets flipped

        # When manchester invert is selected, then elsewhere we flip the entire fsk mapping,
        # which also flips the preamble and sync word.  We don't want the the preamble and
        # syncword flipped, so to fix it, we invert the preamble pattern and sync word register
        # to undo the fsk mapping flip.
        encoding = model.vars.tx_symbol_encoding.value

        # For 4FSK + BCR, syncword inversion is required due to limitations of BCR syncword detection block
        fsk_symbol_map = model.vars.tx_fsk_symbol_map.value
        modulation_type = model.vars.modulation_type.value
        demod_select = model.vars.demod_select.value

        if encoding == model.vars.tx_symbol_encoding.var_enum.Inv_Manchester or \
                (fsk_symbol_map in [model.vars.fsk_symbol_map.var_enum.MAP1,
                                   model.vars.fsk_symbol_map.var_enum.MAP3,
                                   model.vars.fsk_symbol_map.var_enum.MAP5,
                                   model.vars.fsk_symbol_map.var_enum.MAP7] and \
                        demod_select == model.vars.demod_select.var_enum.BCR and \
                        modulation_type == model.vars.modulation_type.var_enum.FSK4):
            syncword_mask = (1 << syncword_length) - 1
            syncword0_reg ^= syncword_mask
            syncword1_reg ^= syncword_mask

        self._ip_reg_write(model, 'SYNC0_SYNC0', syncword0_reg)
        self._ip_reg_write(model, 'SYNC1_SYNC1', syncword1_reg)


    def calc_synchronous_mixdac_clk_mod_regs(self, model):
        if not model.vars.synchronous_mixdac_clk.value:
            # normal async front filtering
            self._ip_reg_write(model, 'TXCTRL_TXAFIFOBYP', 0)
        else:
            self._ip_reg_write(model, 'TXCTRL_TXAFIFOBYP', 1)


    def calc_interpolation_gain_mod_actual(self, model):
        #This function calculates the actual interpolation gain

        #Load model variables into local variables
        txbrnum = model.vars.MOD_TXBR_TXBRNUM.value
        modformat = model.vars.tx_modulation_type.value

        if txbrnum < 256:
            interpolation_gain = txbrnum / 1.0
        elif modformat == model.vars.tx_modulation_type.var_enum.BPSK or \
             modformat == model.vars.tx_modulation_type.var_enum.DBPSK:
            interpolation_gain = 16 * txbrnum * 2 ** (3-floor(log(txbrnum, 2)))
        elif txbrnum < 512:
            interpolation_gain = txbrnum / 2.0
        elif txbrnum < 1024:
            interpolation_gain = txbrnum / 4.0
        elif txbrnum < 2048:
            interpolation_gain = txbrnum / 8.0
        elif txbrnum < 4096:
            interpolation_gain = txbrnum / 16.0
        elif txbrnum < 8192:
            interpolation_gain = txbrnum / 32.0
        elif txbrnum < 16384:
            interpolation_gain = txbrnum / 64.0
        else:
            interpolation_gain = txbrnum / 128.0

        # following the rtl
        interpolation_gain = floor(interpolation_gain)

        # calculate phase interpolation gain for OQPSK cases
        if modformat == model.vars.tx_modulation_type.var_enum.OQPSK:
            interpolation_gain = 2 ** (ceil(log(interpolation_gain, 2)))

        #Load local variables back into model variables
        model.vars.interpolation_gain_actual.value = float(interpolation_gain)

    def calc_timeperiod_mod_reg(self, model):
        TIMEPERIOD_FRACTIONAL_BITS = 24
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        timeperiod = int(2**TIMEPERIOD_FRACTIONAL_BITS / (xtal_frequency_hz / 1e6))

        self._ip_reg_write(model, 'ANTSWCTRL1_TIMEPERIOD', timeperiod)


    ### https://jira.silabs.com/browse/MCUW_RADIO_CFG-3103
    def calc_srcratio_mod_reg(self, model):
        xtal = model.vars.xtal_frequency_hz.value

        src_in = 32e6  # Fixed 32sps IQ sample rate
        src_out = xtal
        srcratio_bitwidth = model.vars.MOD_SRCIQ_SRCRATIO.get_bit_width()
        srcratio = int(pow(2, srcratio_bitwidth - 1) * (src_in/src_out))

        if (src_in/src_out) > 1:
            raise CalculationException('IQ SRCRATIO overflow ({0} bits!)'.format(srcratio_bitwidth))
        else:
            self._ip_reg_write(model, 'SRCIQ_SRCRATIO', srcratio, check_saturation=True)


    def calc_rf_path_default(self, model):
        # Set RF path to the default value here
        model.vars.rf_path.value = model.vars.rf_path.var_enum.LPW

    def get_required_filter_taps_mod(self, bt):
        """
        Calculate required filter taps for gaussian shaping filter with BT
        Pulse shaping will spread over (1/bt) symbols. Since shaping filter is implemented at 8*baudrate, the required
        taps for a bt will be 8/bt
        :param bt:Bandwidth time product
        :return: req_filter_taps
        """
        req_filter_taps = math.ceil(8/bt)
        return req_filter_taps

    # Method name: calc_error_check
    # Defined in: ocelot\calculators\calc_utilities.py
    def calc_error_check_mod(self, model):
        #Overriding function due to removal of freq_gain_scale variable
        #Load model variables into local variables
        modulation_type = model.vars.modulation_type.value
        bitrate = model.vars.bitrate.value
        baudrate = model.vars.baudrate.value
        tx_baud_rate = model.vars.tx_baud_rate_actual.value
        target_deviation = model.vars.deviation.value
        tx_deviation = model.vars.tx_deviation_actual.value

        tx_bitrate_error = abs(baudrate - tx_baud_rate) * 1.0 / baudrate
        if tx_bitrate_error > 0.001:
            print("  WARNING: TX bitrate is off by more than 0.1%!")
        if tx_deviation > 0:
            tx_deviation_error = abs(target_deviation - tx_deviation) * 1.0 / target_deviation
        else:
            tx_deviation_error = 0.0
        if modulation_type == model.vars.modulation_type.var_enum.MSK:
            deviation_within_MSK_bound = math.floor(0.25 * bitrate) <= target_deviation <= math.ceil(0.25 * bitrate)
            if not deviation_within_MSK_bound:
                LogMgr.Warning("WARNING: Deviation is not 1/4 of data rate for MSK!")
        if tx_deviation_error > 0.1:
            print("  WARNING: TX frequency deviation is more than 10% away from target!")
        model.vars.tx_bitrate_error.value   = tx_bitrate_error
        model.vars.tx_deviation_error.value = tx_deviation_error