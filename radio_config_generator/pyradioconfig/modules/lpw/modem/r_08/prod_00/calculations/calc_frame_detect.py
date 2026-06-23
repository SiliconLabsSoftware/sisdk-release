from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from py_2_and_3_compatibility import *
from math import ceil
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr

class CalcFrameDetect(IPCalculator):
    # Method name: _build_framedet_regs
    # Defined in: lpwh72000\calculators\calc_frame_detect.py
    def _build_framedet_regs(self, model):
        pass


    # Method name: calc_addtimseq_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_addtimseq_reg(self, model):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        addtimseq = model.vars.number_of_timing_windows.value
        # one search is done by default
        if addtimseq > 0:
            addtimseq -= 1
        self._ip_reg_write(model, 'TIMING_ADDTIMSEQ', addtimseq)

    # Method name: calc_addtimseq_val
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_addtimseq_val(self, model):
        """
        calculate additional timing sequences to detect given preamble length
        the equation used to calcualte ADDTIMSEQ is derived emprically and might need
        tweaking as we have more PHY providing additional data
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        preamble_pattern_bits = model.vars.preamble_pattern_len_actual.value
        preamble_detection_length = model.vars.preamble_detection_length.value * 1.0
        timingbases = model.vars.timingbases_actual.value
        timingwindow = model.vars.timing_window_actual.value
        mod_format = model.vars.modulation_type.value
        demod_select = model.vars.demod_select.value
        symbol_enconding_type = model.vars.symbol_encoding.value
        antdivmode = model.vars.antdivmode.value
        # : if antenna diversity is enabled, set number of timing windows to 1 (addtimseq = 0)
        if antdivmode != model.vars.antdivmode.var_enum.DISABLE:
            addtimseq = 0
        elif demod_select == model.vars.demod_select.var_enum.COHERENT:
            # Process first aligned window 6 times for preamble search for coherent demod based on Ocelot measurements.
            addtimseq = 6
        elif mod_format == model.vars.modulation_type.var_enum.OQPSK \
                and symbol_enconding_type == model.vars.symbol_encoding.var_enum.DSSS:
            # : determine number of symbols in preamble
            num_sym_in_preamble = preamble_detection_length / preamble_pattern_bits
            # : Timing window for DSSS is always 1 symbol. Allow number of timing windows to detect to be up to
            # : quarter of preamble. The final ratio between preamble length and number of timing windows may need
            # : to be tweaked based on additional investigations.
            addtimseq = int(round(num_sym_in_preamble / 4.0)) - 1
        elif mod_format == model.vars.modulation_type.var_enum.OOK:
            # Always use 1 timing window for OOK
            addtimseq = 0
        else:
            if timingbases > 1:
                # Figure out how many timing windows fit in the preamble. Assume one is throwaway.
                addtimseq = math.floor(preamble_detection_length / timingwindow) - 2
            else:
                addtimseq = 0
        # saturate addtimseq to fit into 4 bits
        if addtimseq > 15:
            addtimseq = 15
        if addtimseq < 0:
            addtimseq = 0
        model.vars.number_of_timing_windows.value = int(addtimseq) + 1

    # Method name: calc_allow_received_window
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_allow_received_window(self, model):
        demod_select = model.vars.demod_select.value
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            # : Always allow received windows for coherent demod
            self._ip_reg_write(model, 'CTRL6_ARW', 1)
        else:
            # : allow received windows when window size is less than half of RAM size
            self._ip_reg_write(model, 'CTRL6_ARW', 0)

    # Method name: calc_base_reg
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_base_reg(self, model):
        """
        set BASE register using input
        The bits have to be flipped around before writing the register
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        preamble_pattern_len = model.vars.preamble_pattern_len.value
        preamble_pattern = model.vars.preamble_pattern.value
        # When manchester invert is selected, then elsewhere we flip the entire fsk mapping,
        # which also flips the preamble and sync word.  We don't want the the preamble and
        # syncword flipped, so to fix it, we invert the preamble pattern and sync word register
        # to undo the fsk mapping flip.
        encoding = model.vars.symbol_encoding.value
        manchester_map = model.vars.manchester_mapping.value
        if encoding == model.vars.symbol_encoding.var_enum.Inv_Manchester:
            preamble_pattern_mask = (1 << preamble_pattern_len) - 1
            preamble_pattern ^= preamble_pattern_mask
        modem_pre_base = self.flip_bits(preamble_pattern, preamble_pattern_len)
        modem_pre_base = int(modem_pre_base)
        self._ip_reg_write(model, 'PRE_BASE', modem_pre_base)

    # Method name: calc_basebits_actual
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_basebits_actual(self, model):
        """
        return actual base bits
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        model.vars.preamble_pattern_len_actual.value = model.vars.MODEM_PRE_BASEBITS.value + 1

    # Method name: calc_basebits_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_basebits_reg(self, model):
        """
        set BASEBITS register using input
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        basebits = model.vars.preamble_pattern_len.value

        if basebits > 0:
            reg = basebits - 1
        else:
            reg = 0

        self._ip_reg_write(model, 'PRE_BASEBITS', reg)

    # Method name: calc_baud_rewind_after_timing_detect
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_baud_rewind_after_timing_detect(self, model):
        demod_select = model.vars.demod_select.value
        dsss_sf = model.vars.dsss_spreading_factor.value
        mod_format = model.vars.modulation_type.value
        if demod_select == model.vars.demod_select.var_enum.COHERENT and \
                mod_format == model.vars.modulation_type.var_enum.OQPSK:
            # : For coherent oqpsk, rewind AFC window by 2 symbols from the initial timing window
            number_of_symbols_to_rewind = 2
            number_of_bauds_to_rewind = int(4 * dsss_sf * number_of_symbols_to_rewind)
        else:
            number_of_bauds_to_rewind = 0
        self._ip_reg_write(model, 'CTRL6_TDREW', number_of_bauds_to_rewind)

    # Method name: calc_diffencmode_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_diffencmode_modem_reg(self, model):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        DIFFENCMODE_LOOKUP = {
            model.vars.diff_encoding_mode.var_enum.DISABLED.value: 0,
            model.vars.diff_encoding_mode.var_enum.RR0.value: 1,
            model.vars.diff_encoding_mode.var_enum.RE0.value: 2,
            model.vars.diff_encoding_mode.var_enum.RR1.value: 3,
            model.vars.diff_encoding_mode.var_enum.RE1.value: 4,
        }
        self._ip_reg_write(model, 'CTRL0_DIFFENCMODE',
                        DIFFENCMODE_LOOKUP[(model.vars.diff_encoding_mode.value).value])

    # Method name: calc_dsss0_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_dsss0_reg(self, model):
        """
        write DSSS symbol 0 register
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        self._ip_reg_write(model, 'DSSS0_DSSS0', model.vars.dsss_chipping_code.value)

    # Method name: calc_dsss_bits_per_symbol
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_dsss_bits_per_symbol(self, model):
        """
        calculate bits per symbol in DSSS mode
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        length = model.vars.dsss_len.value
        spreading_factor = model.vars.dsss_spreading_factor.value * 1.0
        if spreading_factor == 0:
            bps = 0
        else:
            bps = length / spreading_factor
        model.vars.dsss_bits_per_symbol.value = int(bps)

    # Method name: calc_dsss_payload_correlation_detection_mode
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_dsss_payload_correlation_detection_mode(self, model):
        demod_select = model.vars.demod_select.value
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            # : When this bit is set, correlation threshold is only used until preamble is detected
            # : after preamble detection, only detected symbol is used to qualify a valid preamble.
            self._ip_reg_write(model, 'CTRL5_DSSSCTD', 1)
        else:
            self._ip_reg_write(model, 'CTRL5_DSSSCTD', 0)

    # Method name: calc_dsssdouble_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_dsssdouble_reg(self, model):
        """
        based on modulation used select if DSSS symbol's inverted version
        should also be a DSSS symbol
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        length = model.vars.dsss_len.value
        modulation = model.vars.modulation_type.value

        if length > 0:
            if modulation == model.vars.modulation_type.var_enum.OQPSK:
                dsssdouble = 2
            else:
                dsssdouble = 1
        else:
            dsssdouble = 0

        self._ip_reg_write(model, 'CTRL0_DSSSDOUBLE', dsssdouble)

    # Method name: calc_dssslen_actual
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_dssslen_actual(self, model):
        """
        given register setting return actual DSSS length
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        dsss0 = model.vars.MODEM_DSSS0_DSSS0.value

        if dsss0 == 0:
            len = 0
        else:
            len = model.vars.MODEM_CTRL0_DSSSLEN.value + 1

        model.vars.dsss_len_actual.value = len

    # Method name: calc_dssslen_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_dssslen_reg(self, model):
        """
        set DSSS length register
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        length = model.vars.dsss_len.value
        shifts = model.vars.dsss_shifts_actual.value

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

    # Method name: calc_dsssshifts_actual
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_dsssshifts_actual(self, model):
        """
        given register setting return actual DSSS shifts value
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        reg = model.vars.MODEM_CTRL0_DSSSSHIFTS.value

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

        model.vars.dsss_shifts_actual.value = val

    # Method name: calc_dsssshifts_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_dsssshifts_reg(self, model):
        """
        write DSSS cyclic shifts number to generate new symbols when using DSSS
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        val = model.vars.dsss_shifts.value
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

    # Method name: calc_dsssshifts_val
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_dsssshifts_val(self, model):
        """
        calculate DSSS shift value
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        length = model.vars.dsss_len.value
        bps = model.vars.dsss_bits_per_symbol.value
        if bps <= 1:
            val = 0
        else:
            val = length / (pow(2, bps) / 2)
        model.vars.dsss_shifts.value = int(val)

    # Method name: calc_dualsync
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_dualsync(selfself, model):
        sync1 = model.vars.syncword_1_actual.value
        if sync1 > 0:
            model.vars.syncword_dualsync.value = True
        else:
            model.vars.syncword_dualsync.value = False

    # Method name: calc_dualsync_reg
    # Defined in: rainier\calculators\calc_frame_detect.py
    def calc_dualsync_reg(self, model):
        demod_sel = model.vars.demod_select.value
        dualsync = model.vars.syncword_dualsync.value
        timingbases = model.vars.timingbases_actual.value
        trisync = model.vars.syncword_trisync.value
        # dualsync is disabled in FDM0 mode (MCUW_RADIO_CFG-1732)
        if dualsync == False:
            reg1_value = 0
        elif dualsync == True and timingbases == 0 and demod_sel == model.vars.demod_select.var_enum.LEGACY:
            LogMgr.Warning(
                "Second syncword is not supported if preamble is shorter than 8 bits and legacy demod is used")
            reg1_value = 0
        else:
            reg1_value = 1
        if trisync == False:
            reg2_value = 0
        else:
            reg1_value = 1
            reg2_value = 1
        self._ip_reg_write(model, 'SYNCWORDCTRL_DUALSYNC', reg1_value)
        self._ip_reg_write(model, 'SYNCWORDCTRL_SYNCDET2TH', reg2_value)

    # Method name: calc_dynamic_timing_thresholds
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_dynamic_timing_thresholds(self, model):
        demod_select = model.vars.demod_select.value
        mod_format = model.vars.modulation_type.value
        bbss_transition_threhold_1 = model.vars.MODEM_LONGRANGE2_LRCHPWRTH1.value
        bbss_transition_threhold_2 = model.vars.MODEM_LONGRANGE2_LRCHPWRTH2.value
        bbss_transition_threhold_3 = model.vars.MODEM_LONGRANGE2_LRCHPWRTH3.value
        average_transition_threhold = int(round((bbss_transition_threhold_1 + bbss_transition_threhold_2) / 2.0))
        if hasattr(model.profiles, 'Long_Range'):
            is_long_range = model.profile == model.profiles.Long_Range
        else:
            is_long_range = False
        """ Set dynamic threshold modes """
        if demod_select == model.vars.demod_select.var_enum.COHERENT and \
                mod_format == model.vars.modulation_type.var_enum.OQPSK:
            """ Set timing threshold gain """
            self._ip_reg_write(model, 'CTRL6_TIMTHRESHGAIN', 2)
            """ Enable dynamic preamble and sync thresholds """
            # : Enable dynamic preamble threshold
            self._ip_reg_write(model, 'COH0_COHDYNAMICPRETHRESH', 1)
            # : Set dynamic preamble threshold to 1x sync threshold
            self._ip_reg_write(model, 'COH0_COHDYNAMICPRETHRESHSEL', 0)
            # : Disable static sync threshold and enable dynamic sync threshold
            self._ip_reg_write(model, 'SYNCPROPERTIES_STATICSYNCTHRESHEN', 0)
            self._ip_reg_write(model, 'COH0_COHDYNAMICSYNCTHRESH', 1)
            """ Enforce qualifications for valid preamble detect """
            self._ip_reg_write(model, 'CTRL5_LINCORR', 1)
            self._ip_reg_write(model, 'CTRL6_PSTIMABORT0', 1)
            self._ip_reg_write(model, 'CTRL6_PSTIMABORT1', 1)
            self._ip_reg_write(model, 'CTRL6_PSTIMABORT2', 1)
            self._ip_reg_write(model, 'CTRL6_PSTIMABORT3', 0)
        else:
            self._ip_reg_write(model, 'CTRL6_TIMTHRESHGAIN', 0)
            self._ip_reg_write(model, 'COH0_COHDYNAMICPRETHRESH', 0)
            self._ip_reg_write(model, 'COH0_COHDYNAMICPRETHRESHSEL', 0)
            self._ip_reg_write(model, 'SYNCPROPERTIES_STATICSYNCTHRESHEN', 0)
            self._ip_reg_write(model, 'COH0_COHDYNAMICSYNCTHRESH', 0)
            self._ip_reg_write(model, 'CTRL5_LINCORR', 0)
            self._ip_reg_write(model, 'CTRL6_PSTIMABORT0', 0)
            self._ip_reg_write(model, 'CTRL6_PSTIMABORT1', 0)
            self._ip_reg_write(model, 'CTRL6_PSTIMABORT2', 0)
            self._ip_reg_write(model, 'CTRL6_PSTIMABORT3', 0)
        if demod_select == model.vars.demod_select.var_enum.COHERENT and is_long_range:
            self._ip_reg_write(model, 'CTRL6_TIMTHRESHGAIN', 2)
            """ Where to begin new region in terms of channel power """
            self._ip_reg_write(model, 'COH0_COHCHPWRTH0', average_transition_threhold)
            self._ip_reg_write(model, 'COH0_COHCHPWRTH1', bbss_transition_threhold_2)
            self._ip_reg_write(model, 'COH0_COHCHPWRTH2', bbss_transition_threhold_3)
            """ Starting sync threshold for each region """
            self._ip_reg_write(model, 'COH1_SYNCTHRESH0', 23)  # 27)
            self._ip_reg_write(model, 'COH1_SYNCTHRESH1', 26)  # 30)
            self._ip_reg_write(model, 'COH1_SYNCTHRESH2', 29)  # 33)
            self._ip_reg_write(model, 'COH1_SYNCTHRESH3', 80)
            """ Slopes of each region """
            self._ip_reg_write(model, 'COH2_SYNCTHRESHDELTA0', 0)
            self._ip_reg_write(model, 'COH2_SYNCTHRESHDELTA1', 2)
            self._ip_reg_write(model, 'COH2_SYNCTHRESHDELTA2', 4)
            self._ip_reg_write(model, 'COH2_SYNCTHRESHDELTA3', 0)
        else:
            self._ip_reg_write(model, 'COH0_COHCHPWRTH0', 0)
            self._ip_reg_write(model, 'COH0_COHCHPWRTH1', 0)
            self._ip_reg_write(model, 'COH0_COHCHPWRTH2', 0)
            self._ip_reg_write(model, 'COH1_SYNCTHRESH0', 0)
            self._ip_reg_write(model, 'COH1_SYNCTHRESH1', 0)
            self._ip_reg_write(model, 'COH1_SYNCTHRESH2', 0)
            self._ip_reg_write(model, 'COH1_SYNCTHRESH3', 0)
            self._ip_reg_write(model, 'COH2_SYNCTHRESHDELTA0', 0)
            self._ip_reg_write(model, 'COH2_SYNCTHRESHDELTA1', 0)
            self._ip_reg_write(model, 'COH2_SYNCTHRESHDELTA2', 0)
            self._ip_reg_write(model, 'COH2_SYNCTHRESHDELTA3', 0)

    # Method name: calc_fdm0diffdis_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_fdm0diffdis_reg(self, model):
        mod_type = model.vars.modulation_type.value
        timingbases = model.vars.timingbases_actual.value
        # If using OOK and FDM0, enable FDM0DIFFDIS so that sliding window detection works properly
        if (mod_type == model.vars.modulation_type.var_enum.OOK) and timingbases == 0:
            self._ip_reg_write(model, 'CTRL0_FDM0DIFFDIS', 1)
        else:
            self._ip_reg_write(model, 'CTRL0_FDM0DIFFDIS', 0)

    # Method name: calc_preamble_string
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_preamble_string(self, model):
        encoding = model.vars.symbol_encoding.value
        preamble_pattern = model.vars.preamble_pattern.value
        preamble_pattern_len = model.vars.preamble_pattern_len.value
        preamble_length = model.vars.preamble_length.value  # This is the TX preamble length
        if encoding == model.vars.symbol_encoding.var_enum.DSSS:
            # : Preamble base pattern is irrelevant if DSSS is enabled. Preamble bits are always substituted with
            # : Base chip sequence (i.e. base patttern = 0)
            preamble_pattern = 0
        repeats = int(preamble_length / preamble_pattern_len)
        preamble_pattern_string = ('{:0' + str(preamble_pattern_len) + 'b}').format(preamble_pattern)
        # The preamble string is for the full TX preamble
        preamble_string = preamble_pattern_string * repeats
        model.vars.preamble_string.value = preamble_string

    def calc_preamble_string_actual(self, model):
        if model.vars.MODEM_CTRL0_CODING.value == 2 or model.vars.MOD_PRE_DSSSPRE.value == 1:
            # : Preamble base pattern is irrelevant if DSSS is enabled. Preamble bits are always substituted with
            # : Base chip sequence (i.e. base patttern = 0)
            preamble_pattern_string = '0'
            preamble_length = model.vars.MODEM_CTRL0_DSSSLEN.value + 1  # This is the TX preamble length
            repeats = int(preamble_length)
        elif model.vars.MODEM_LONGRANGE_LRBLE.value == 1 and model.vars.MODEM_CTRL0_CODING.value == 3:
            preamble_pattern_string = '00111100'
            repeats = model.vars.MOD_PRE_TXBASES.value
        else:
            preamble_pattern_len = model.vars.MODEM_PRE_BASEBITS.value + 1
            preamble_pattern_value = self.flip_bits(model.vars.MODEM_PRE_BASE.value, preamble_pattern_len)
            preamble_pattern_string = ('{:0' + str(preamble_pattern_len) + 'b}').format(preamble_pattern_value)
            repeats = model.vars.MOD_PRE_TXBASES.value

        preamble_string = preamble_pattern_string * repeats
        model.vars.preamble_string_actual.value = preamble_string

    # Method name: calc_preerrors_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_preerrors_reg(self, model):
        """
        write value to register
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        preerrors = model.vars.errors_in_timing_window.value
        if preerrors > 15:
            preerrors = 15
        self._ip_reg_write(model, 'PRE_PREERRORS', preerrors)

    # Method name: calc_preerrors_val
    # Defined in: rainier\calculators\calc_frame_detect.py
    def calc_preerrors_val(self, model):
        # FIXME: consider adding +1 to errors when AFC is enbabled - seems to work better

        dssslen = model.vars.dsss_len_actual.value
        in_2fsk_opt_scope = model.vars.in_2fsk_opt_scope.value
        baudrate = model.vars.baudrate.value
        demod_select = model.vars.demod_select.value
        if demod_select == model.vars.demod_select.var_enum.ENHANCED_DSSS:
            model.vars.errors_in_timing_window.value = 0
        else:
            if dssslen == 0:
                if in_2fsk_opt_scope and baudrate > 1900000:
                    preerrors = 1
                else:
                    preerrors = 0
            else:
                preerrors = dssslen / 2.0

            if demod_select == model.vars.demod_select.var_enum.COHERENT:
                # : For coherent demod, set to maximum value in order to disable this feature.
                preerrors = 15

            # make sure we fit into 4 bits
            if preerrors > 15:
                preerrors = 15

            model.vars.errors_in_timing_window.value = int(round(preerrors))

    # Method name: calc_rxpinmode_reg
    # Defined in: common\calculators\calc_frame_detect.py
    # def calc_rxpinmode_reg(self, model):
    #     if model.vars.asynchronous_rx_enable.value is True:
    #         mode = 1
    #     else:
    #         mode = 0
    #     self._ip_reg_write(model, 'CTRL2_RXPINMODE', mode)

    # Method name: calc_sync_words_reg
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_sync_words_reg(self, model):
        """
        write sync words from input to registers
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        syncword_length = model.vars.syncword_length.value
        syncword0_reg = long(self.flip_bits(model.vars.syncword_0.value, syncword_length))
        syncword1_reg = long(self.flip_bits(model.vars.syncword_1.value, syncword_length))
        if model.vars.ber_force_sync.value == True:
            syncword0_reg = long(0x1dd3d4a0)  # gdc:  Fix this after we get rid of the "_left" stuff above.
            # gdc:  Fix it so we just write syncword_0 before it gets flipped
        # When manchester invert is selected, then elsewhere we flip the entire fsk mapping,
        # which also flips the preamble and sync word.  We don't want the the preamble and
        # syncword flipped, so to fix it, we invert the preamble pattern and sync word register
        # to undo the fsk mapping flip.
        encoding = model.vars.symbol_encoding.value
        # For 4FSK + BCR, syncword inversion is required due to limitations of BCR syncword detection block
        fsk_symbol_map = model.vars.fsk_symbol_map.value
        modulation_type = model.vars.modulation_type.value
        demod_select = model.vars.demod_select.value
        if encoding == model.vars.symbol_encoding.var_enum.Inv_Manchester or \
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

    # Method name: calc_syncbits_reg
    # Defined in: rainier\calculators\calc_frame_detect.py
    def calc_syncbits_modem_reg(self, model):
        """
        write sync word length from input to register
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        if model.vars.syncword_length.value < 2:
            LogMgr.Error("Syncword length must be at least 2")
        if model.vars.ber_force_sync.value == True:
            syncword_length = 32
        else:
            syncword_length = model.vars.syncword_length.value
        # FIXME: amtudave: Remove SYNCBITS once tri-sync control added to sync_det
        self._ip_reg_write(model, 'CTRL1_SYNCBITS', syncword_length - 1)
        # self._ip_reg_write(model, 'SYNCWORDCTRL_SYNC0BITS', syncword_length - 1)
        # self._ip_reg_write(model, 'SYNCWORDCTRL_SYNCBITS2TH', syncword_length - 1)

    # Method name: calc_syncerrors_reg
    # Defined in: rainier\calculators\calc_frame_detect.py
    def calc_syncerrors_reg(self, model):
        # This function calulates the SYNCERRORS field
        # Read in model variables
        demod_select = model.vars.demod_select.value
        rtschmode_actual = model.vars.MODEM_REALTIMCFE_RTSCHMODE.value
        directmode_rx = model.vars.directmode_rx.value
        mod_type = model.vars.modulation_type.value
        if directmode_rx != model.vars.directmode_rx.var_enum.DISABLED and mod_type == model.vars.modulation_type.var_enum.FSK2:
            syncerrors = 2
        # Allow 1 sync error if using TRECS and RTSCHMODE = 1 (hard slicing instead of CFE)
        elif demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or \
                demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
            if rtschmode_actual == 1:
                syncerrors = 1
            else:
                syncerrors = 0
        else:
            syncerrors = 0
        # Write the register
        self._ip_reg_write(model, 'CTRL1_SYNCERRORS', syncerrors)
        self._ip_reg_write(model, 'SYNCWORDCTRL_SYNC0ERRORS', syncerrors)
        self._ip_reg_write(model, 'SYNCWORDCTRL_SYNC1ERRORS', syncerrors)
        self._ip_reg_write(model, 'SYNCWORDCTRL_SYNC2ERRORS', 0)  ##fix me

    # Method name: calc_syncword_actual
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_syncword_actual(self, model):
        syncword_length = model.vars.syncword_length_actual.value
        syncword0_reg = model.vars.MODEM_SYNC0_SYNC0.value #TODO: implement ipread
        syncword1_reg = model.vars.MODEM_SYNC1_SYNC1.value
        encoding = model.vars.symbol_encoding.value
        manchester_map = model.vars.manchester_mapping.value
        # For 4FSK + BCR, syncword written in SYNC0/1 is inversed from actual
        fsk_symbol_map = model.vars.fsk_symbol_map.value
        modulation_type = model.vars.modulation_type.value
        demod_select = model.vars.demod_select.value
        if encoding == model.vars.symbol_encoding.var_enum.Inv_Manchester or \
                (fsk_symbol_map in [model.vars.fsk_symbol_map.var_enum.MAP1,
                                    model.vars.fsk_symbol_map.var_enum.MAP3,
                                    model.vars.fsk_symbol_map.var_enum.MAP5,
                                    model.vars.fsk_symbol_map.var_enum.MAP7] and \
                 demod_select == model.vars.demod_select.var_enum.BCR and \
                 modulation_type == model.vars.modulation_type.var_enum.FSK4):
            syncword_mask = (1 << syncword_length) - 1
            syncword0_reg ^= syncword_mask
            syncword1_reg ^= syncword_mask
        # if MSbit is set, will need to trip the leading '-' character from the binary string
        model.vars.syncword_0_actual.value = long(bin(syncword0_reg).replace('-', '')[2:].zfill(syncword_length)[::-1],
                                                  2)
        model.vars.syncword_1_actual.value = long(bin(syncword1_reg).replace('-', '')[2:].zfill(syncword_length)[::-1],
                                                  2)

    # Method name: calc_syncword_length_actual
    # Defined in: rainier\calculators\calc_frame_detect.py
    def calc_syncword_length_actual(self, model):
        """given register read back actual sync word length
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        model.vars.syncword_length_actual.value = model.vars.MODEM_CTRL1_SYNCBITS.value + 1 # todo:implement IPREAD

    # Method name: calc_syncword_string
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_syncword_string(self, model):
        syncword_length = model.vars.syncword_length_actual.value
        syncword = model.vars.syncword_0_actual.value
        model.vars.syncword_string.value = bin(syncword)[2:].zfill(syncword_length)

    # Method name: calc_syncword_tx_skip
    # Defined in: lpwh72000\calculators\calc_frame_detect.py
    def calc_syncword_tx_skip(self, model):
        pass

    # Method name: calc_timbases_actual
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_timbases_actual(self, model):
        """
        return actual TIMINGBASES value
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        model.vars.timingbases_actual.value = model.vars.MODEM_TIMING_TIMINGBASES.value

    # Method name: calc_timbases_reg
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_timbases_reg(self, model):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        timingwindow = model.vars.symbols_in_timing_window.value * 1.0
        basebits = model.vars.preamble_pattern_len_actual.value
        if model.vars.ber_force_fdm0.value == True:
            timingbases = 0
        else:
            timingbases = int(math.ceil(timingwindow / basebits))
        if timingbases > 15:
            timingbases = 15
        self._ip_reg_write(model, 'TIMING_TIMINGBASES', timingbases)

    # Method name: calc_timbases_val
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_timbases_val(self, model):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        preamble_detection_length = model.vars.preamble_detection_length.value
        modformat = model.vars.modulation_type.value
        basebits = model.vars.preamble_pattern_len_actual.value
        encoding = model.vars.symbol_encoding.value
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        demod_select = model.vars.demod_select.value
        baudrate_tol_ppm = model.vars.baudrate_tol_ppm.value
        agc_settling_delay = model.vars.agc_settling_delay.value
        grpdelay_to_demod = model.vars.grpdelay_to_demod.value
        osr = model.vars.oversampling_rate_actual.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)
        preamblebits = model.vars.preamble_length.value

        if model.vars.asynchronous_rx_enable.value is True:
            # When asynchronous direct mode is enabled set to max
            timingbases = 15
        else:
            # Not asynchronous mode
            if encoding == model.vars.symbol_encoding.var_enum.DSSS:
                # Unique timing window settings are required for PHYs that use DSSS
                # : For coherent demod, timing base of 3 seems to work regardless of preamble length
                if demod_select == model.vars.demod_select.var_enum.COHERENT:
                    # : OQPSK uses 3 symbols for timing detect if coherent demod is enabled
                    if modformat == model.vars.modulation_type.var_enum.OQPSK:
                        timingbases = 3
                    # : BPSK uses 8 symbols for timing detect
                    elif modformat == model.vars.modulation_type.var_enum.DBPSK:
                        timingbases = 8
                    else:  # modulation format is not supported by COHERENT demod. Follow DSSS default
                        timingbases = 1
                else:
                    # for DSSS set to 1
                    timingbases = 1
            else:
                # Not DSSS
                if vtdemoden:
                    if not fast_detect_enable:
                        # In this case some bits may be shifted from preamble -> syncword
                        trecs_effective_preamble_len = model.vars.trecs_effective_preamble_len.value
                        effective_preamble_len_after_delay = trecs_effective_preamble_len - int(
                            ceil(grpdelay_to_demod / osr))
                        if effective_preamble_len_after_delay > 32:
                            preamsch_len = 32  # can only use 32 preamble bits
                        elif effective_preamble_len_after_delay <= 24:
                            preamsch_len = 0  # if preamble length is less than or equal to 24 don't use preamble search in TRECS
                        else:
                            preamsch_len = effective_preamble_len_after_delay
                    else:
                        # No bits will be shifted from preamble->syncword
                        preamsch_len = 8  # Optimized for fast detection (max sleep time)
                    # When using TRECS, use the calculated preamble search length
                    timingbases = preamsch_len // basebits
                else:
                    # Default Legacy Demod calculation
                    # If cfloopdel is set correctly, then the first timing window after the cfloopdel period will be valid
                    cfloopdel_symbols = int(round(agc_settling_delay / osr))
                    remaining_pre_symbols = preamble_detection_length - cfloopdel_symbols
                    if remaining_pre_symbols >= 4:
                        if baudrate_tol_ppm >= 1000:
                            # Maximum timing window size is 8 to allow for more frequent resynchronization
                            max_timingbases = 8 // basebits
                        else:
                            # Maximum timing window size is 16
                            max_timingbases = 16 // basebits
                        # Use fixed window if we can make it 4 bits or larger
                        timingbases = min(remaining_pre_symbols // basebits, max_timingbases)
                    else:
                        # Short preamble 4FSK seems to work better with older calculation (https://jira.silabs.com/browse/MCUW_RADIO_CFG-2065)
                        if modformat == model.vars.modulation_type.var_enum.FSK4:
                            # super().calc_timbases_val(model)
                            timingbases = round(preamblebits / 8.0)
                        else:
                            # Use sliding window (FDM0)
                            timingbases = 0
        # Calculate the final timing window size and write to model variable
        timing_window_size = int(timingbases * basebits)
        model.vars.symbols_in_timing_window.value = timing_window_size

    # Method name: calc_timingwindow_actual
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_timingwindow_actual(self, model):
        """
        calculate the size of the timing window. If timingbases == 0 we are in FDM0 mode where
        the timing window is set by number of sync bits. In FDM1 (ADDTIMSEQ = 0) and FDM2 (ADDTIMSEQ > 0)
        modes the timing window size is a product of timingbases and basebits.
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        timingbases = model.vars.timingbases_actual.value
        basebits = model.vars.preamble_pattern_len_actual.value
        syncword_length = model.vars.syncword_length_actual.value
        spreading_factor = model.vars.dsss_spreading_factor.value
        if timingbases == 0:
            timing_window = syncword_length
        elif spreading_factor > 0:
            timing_window = timingbases * spreading_factor
        else:
            timing_window = timingbases * basebits
        model.vars.timing_window_actual.value = timing_window

    # Method name: calc_timthresh_actual
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_timthresh_actual(self, model):
        """
        given register value return actual threshold value
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        model.vars.timthresh_actual.value = model.vars.MODEM_TIMING_TIMTHRESH.value

    # Method name: calc_timthresh_gain_actual
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_timthresh_gain_actual(self, model):
        # This function calculates the actual timing threshold gain based on the register value
        # Load model values into local variables
        timthresh_gain_reg = model.vars.MODEM_CTRL6_TIMTHRESHGAIN.value
        timthresh_gain_actual = 2 ** (timthresh_gain_reg + 3)
        # Load local variables back into model variables
        model.vars.timing_detection_threshold_gain_actual.value = timthresh_gain_actual

    # Method name: calc_timthresh_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_timthresh_reg(self, model):
        """
        given desired threshold set register value
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        threshold = model.vars.timing_detection_threshold.value
        if threshold > 255.0:
            threshold = 255.0
            LogMgr.Warning("WARNING: threshold larger than max allowed 255!")
        self._ip_reg_write(model, 'TIMING_TIMTHRESH', int(threshold))

    # Method name: calc_timthresh_value
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_timthresh_value(self, model):
        # This function calculates the timing threshold
        # Load model values into local variables
        mod_type = model.vars.modulation_type.value
        demod_rate_actual = model.vars.demod_rate_actual.value
        deviation = model.vars.deviation.value
        freq_gain_actual = model.vars.freq_gain_actual.value
        timing_window_actual = model.vars.timing_window_actual.value
        timthresh_gain_actual = model.vars.timing_detection_threshold_gain_actual.value
        symbol_enconding_type = model.vars.symbol_encoding.value
        dsss_len = model.vars.dsss_len.value
        dsss_sf = model.vars.dsss_spreading_factor.value
        if (mod_type == model.vars.modulation_type.var_enum.OOK):
            timthresh = 0
        elif (mod_type == model.vars.modulation_type.var_enum.OQPSK):
            # : semi-empirical calculation based on Ocelot OQPSK DSSS investigation
            # : For DSSS, timing window is always 1 symbol long. Number of bits used in correlation is
            # : 1 symbol x DSSS Length = # of bits
            # : The noise in the correlation therefore depends on DSSS length. The actual noise level is
            # : based on dsss length times scale factor
            # : https://jira.silabs.com/browse/MCUW_RADIO_CFG-1212
            if (symbol_enconding_type == model.vars.symbol_encoding.var_enum.DSSS):
                # : noise scale factor. Value is based on RTL simulation and generating a histogram of max_corr.
                # : Factor is set such that threshold is at 99 percentile of max_corr
                noise_scale_factor = 110
                nominal_decision = noise_scale_factor * math.log2(dsss_len)
                timthresh = int(math.ceil(nominal_decision / timthresh_gain_actual))
            else:
                timthresh = 60
        else:
            nominal_decision = 2.0 * deviation / demod_rate_actual * 128 * freq_gain_actual
            # FIXME: arbitrary scaling of 3 here. Should this be function of the sensitivity?
            timthresh = int(round(timing_window_actual * nominal_decision / timthresh_gain_actual / 3))
        # Load local variables back into model variables
        model.vars.timing_detection_threshold.value = timthresh

    # Method name: calc_tr_td_edge
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_tr_td_edge(self, model):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        modformat = model.vars.modulation_type.value
        if modformat == model.vars.modulation_type.var_enum.BPSK or \
                modformat == model.vars.modulation_type.var_enum.DBPSK:
            self._ip_reg_write(model, 'CTRL5_TDEDGE', 1)
            self._ip_reg_write(model, 'CTRL5_TREDGE', 1)
        else:
            self._ip_reg_write(model, 'CTRL5_TDEDGE', 0)
            self._ip_reg_write(model, 'CTRL5_TREDGE', 0)

    # Method name: calc_trisync
    # Defined in: rainier\calculators\calc_frame_detect.py
    def calc_trisync(self, model):
        # FIXME: Need to make a profile input eventually
        # sync2 = model.vars.syncword_2_actual.value
        sync2 = 0
        if sync2 > 0:
            syncword_trisync = True
        else:
            syncword_trisync = False
        model.vars.syncword_trisync.value = syncword_trisync

    # Method name: calc_tsampdel_val
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_tsampdel_val(self, model):
        """
        We do not see a strong relation between performance and this delay parameter but
        using hand optimized results for about 50 PHYs we came up with a simple equation
        to calculate the delay parameter when TSAMPMODE is enabled.
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        baudrate = model.vars.baudrate.value
        osr = model.vars.oversampling_rate_actual.value
        if model.vars.MODEM_CTRL3_TSAMPMODE.value == 1:
            tsampdel = py2round(2.5e6 / baudrate / osr)
        else:
            tsampdel = 0
        if tsampdel > 3:
            tsampdel = 3
        self._ip_reg_write(model, 'CTRL3_TSAMPDEL', int(tsampdel))

    # Method name: calc_tsamplim_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_tsamplim_reg(self, model):
        """
        calculate TSAMPLIM register based on variable. Saturating to 100 based on the fact
        that we have not seen a register setting greater than 20 up to this point despite
        the the register being 16 bits
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        threshold = model.vars.timing_sample_threshold.value
        if threshold < 0:
            threshold = 0
        elif threshold > 100 and not model.vars.asynchronous_rx_enable.value is True:
            threshold = 100
        self._ip_reg_write(model, 'CTRL3_TSAMPLIM', threshold)

    # Method name: calc_tsamplim_val
    # Defined in: ocelot\calculators\calc_frame_detect.py
    def calc_tsamplim_val(self, model):
        modformat = model.vars.modulation_type.value
        preamble_detection_length = model.vars.preamble_detection_length.value
        dsa_enable = model.vars.dsa_enable.value
        if model.vars.asynchronous_rx_enable.value is True:
            # for asynchronous direct mode we don't want the demod to change states so
            # keep the thresholds at the upper limit
            th = 65535
        elif dsa_enable:
            th = 0  # If we are using the phase DSA then don't use TSAMPMODE
        else:
            if modformat == model.vars.modulation_type.var_enum.OOK or \
                    modformat == model.vars.modulation_type.var_enum.ASK:
                # for amplitude modulated signal we need to turn off TSAMPMODE as enabling it
                # switches the slicer level from FREQOFFESTLIM to TSAMPLIM which we don't want.
                th = 0
            else:
                if preamble_detection_length >= 32:
                    th = 0  # [MCUW_RADIO_CFG-1077] If we have at least 32 preamble bits then correlation is robust
                else:
                    # nominal threshold of 10 seems to work well for most PHYs
                    th = 10
        model.vars.timing_sample_threshold.value = th

    # Method name: calc_tsampmode_reg
    # Defined in: common\calculators\calc_frame_detect.py
    def calc_tsampmode_reg(self, model):
        """
        set TSAMPMODE if we need a non-zero TSAMPLIM value
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        threshold = model.vars.timing_sample_threshold.value
        modformat = model.vars.modulation_type.value
        encoding = model.vars.symbol_encoding.value
        if threshold == 0 or \
                modformat == model.vars.modulation_type.var_enum.OOK or \
                modformat == model.vars.modulation_type.var_enum.ASK or \
                encoding == model.vars.symbol_encoding.var_enum.DSSS:
            mode = 0
        else:
            mode = 1
        self._ip_reg_write(model, 'CTRL3_TSAMPMODE', mode)

    # Method name: calc_txsync_reg
    # Defined in: lpwh72000\calculators\calc_frame_detect.py
    def calc_txsync_reg(self, model):
        pass

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