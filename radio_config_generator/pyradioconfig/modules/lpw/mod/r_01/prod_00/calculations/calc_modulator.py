from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
from math import ceil, floor, log
from py_2_and_3_compatibility import *
import numpy as np
from pyradioconfig.parts.common.utils.tinynumpy import tinynumpy


class CalcModulator(IPCalculator):
    # Method name: _get_modindex
    # Defined in: ocelot\calculators\calc_modulator.py
    def _get_modindex(self, model, modem_frequency_hz, modformat, freq_dev_hz, synth_res, shaping_filter_gain,
                      interpolation_gain):
        if modformat == model.vars.modulation_type.var_enum.FSK2 or \
                modformat == model.vars.modulation_type.var_enum.MSK or \
                modformat == model.vars.modulation_type.var_enum.FSK4:
            modindex = freq_dev_hz * 16.0 / (synth_res * shaping_filter_gain * interpolation_gain)
        elif modformat == model.vars.modulation_type.var_enum.OQPSK:
            modindex = modem_frequency_hz / (synth_res * 2 * shaping_filter_gain * interpolation_gain)
        elif modformat == model.vars.modulation_type.var_enum.OOK or \
                modformat == model.vars.modulation_type.var_enum.ASK or \
                modformat == model.vars.modulation_type.var_enum.BPSK or \
                modformat == model.vars.modulation_type.var_enum.DBPSK:
            modindex = self.max_pa_value * 16.0 / (shaping_filter_gain * interpolation_gain) #todo: find where is self.max_pa_value
        else:
            modindex = 0.0  # don't care in OFDM
        return modindex

    # Method name: _get_modindex_field
    # Defined in: common\calculators\calc_modulator.py
    def _get_modindex_field(self, modindex):
        # convert fractional modindex into m * 2^e format
        m, e = self.frac2exp(31, modindex)
        # MODEINDEXE is a signed value
        if e < 0:
            e += 32
        # verify number fits into register
        if m > 31:
            m = 31
        if e > 31:
            e = 31
        if m < 0:
            m = 0
        return m, e

    # Method name: _get_txbr_reg
    # Defined in: ocelot\calculators\calc_modulator.py
    def _get_txbr_reg(self, ratio, txbr_num_err_tol, txbr_max_den):
        # : local variable for finding baudrate ratio that minimizes error between desired and actual baudrate
        txbr_num_err_map = {}
        # find best integer ratio to match desired ratio
        found_best_ratio = False
        for den in xrange(txbr_max_den, 0, -1):
            num = ratio * den
            txbr_num_err = abs(round(num) - num)
            if num < 32768:
                txbr_num_err_map[den] = abs(txbr_num_err - txbr_num_err_tol)
                if txbr_num_err < txbr_num_err_tol:
                    found_best_ratio = True
                    break
        # if best integer ratio is not found, re-calculate and find the ratio that is closest to the tolerance
        if not found_best_ratio:
            if len(txbr_num_err_map) > 0:
                den = min(txbr_num_err_map, key=txbr_num_err_map.get)
            else:
                den = 1
            num = ratio * den
        return num, den

    # Method name: calc_am_low_ramplev
    # Defined in: ocelot\calculators\calc_modulator.py
    def calc_am_low_ramplev(self, model):
        # For now, always set to 0 (detailed calculation to be added when we add ASK support to calculator)
        model.vars.am_low_ramplev.value = 0


    # Method name: calc_manchester_mapping
    # Defined in: ocelot\calculators\calc_modulator.py
    def calc_manchester_mapping(self, model):
        # Since manchester_mapping was removed as an input on Ocelot, we need to calculate it from symbol_encoding
        # Read in model vars
        symbol_encoding = model.vars.symbol_encoding.value
        if symbol_encoding == model.vars.symbol_encoding.var_enum.Inv_Manchester:
            manchester_mapping = model.vars.manchester_mapping.var_enum.Inverted
        else:
            manchester_mapping = model.vars.manchester_mapping.var_enum.Default
        # Write the model var
        model.vars.manchester_mapping.value = manchester_mapping

    # Method name: calc_mapfsk_reg
    # Defined in: ocelot\calculators\calc_modulator.py
    def calc_mapfsk_reg(self, model):
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
        self._reg_write(model.vars.MODEM_CTRL0_MAPFSK, mapfsk)

    # Method name: calc_modindex_actual
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_modindex_actual(self, model):
        """
        given register settings return actual MODINDEX as fraction

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        m = model.vars.MOD_MODINDEX_MODINDEXM.value
        e = model.vars.MOD_MODINDEX_MODINDEXE.value

        # MODEINDEXE is a signed value
        if e > 15:
            e -= 32

        # removing the adjustment from exp(e) done for bit fixed point implementation adjustment
        e = e - 8
        model.vars.modindex_actual.value = 1.0 * m * 2**e

    # Method name: calc_modindex_field
    # Defined in: rainier\calculators\calc_modulator.py
    def calc_modindex_field(self, model):
        """
        convert desired modindex fractional value to MODINDEXM * 2^MODINDEXE

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        modindex = model.vars.modindex.value
        max_m = (2 ** model.vars.MOD_MODINDEX_MODINDEXM.get_bit_width()) - 1
        max_e = (2 ** model.vars.MOD_MODINDEX_MODINDEXE.get_bit_width()) - 1

        # convert fractional modindex into m * 2^e format
        m, e = self.frac2exp(max_m, modindex, up=True)

        # ############
        # In series 3, RTL implementation of the modindex multiplier is as follows
        # input -> 16bit fractional value (fixed point implementation, signed 5.11, sign bit included)
        # output -> 20bit fractional value (fixed point implementation, signed 1.19, sign bit included)
        # mod_index -> mantissa * 2^exp
        # for any fractional value 'a' with fixed point binary implementation of lets say 5.11
        # a = (value of 16 bit assuming no implied binary point) * 2^-11
        # therefore,
        # output = input * 2^-11 * (mantissa * 2^exp) = input * (mantissa * 2^exp) * 2^-11
        # since required output is needed with 19 fractional bits, output can be re-written as
        # output = input * (mantissa * 2^exp * 2^8) * 2^-19 = input * (mantissa * 2^exp+8) * 2^-19
        # therefore we need to make this adjustment in exp(e)
        # ############
        e = e + 8

        # MODEINDEXE is a signed value, therefore wrap if value is negative
        if e < 0:
            e += (2 ** model.vars.MOD_MODINDEX_MODINDEXE.get_bit_width())

        # verify number fits into register
        if m > max_m:
            m = max_m
        if e > max_e:
            e = max_e
        if m < 0:
            m = 0

        self._ip_reg_write(model, 'MODINDEX_MODINDEXM', int(m))
        self._ip_reg_write(model, 'MODINDEX_MODINDEXE', int(e))

    # Method name: calc_modindex_value
    # Defined in: rainier\calculators\calc_modulator.py
    def calc_modindex_value(self, model):
        """
        calculate MODINDEX value
        Modulation scaling for PHMOD happens after src and interpolator
        Modulation scaling for IQMOD happens after src but before interpolator, therefore modulation scaling needs to be
        adjusted as per br2m bit
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        fxo = model.vars.xtal_frequency_hz.value * 1.0
        modformat = model.vars.modulation_type.value
        freq_dev_hz = model.vars.deviation.value * 1.0
        shaping_filter_gain = model.vars.shaping_filter_gain_actual.value
        br2m = model.vars.br2m.value
        baudrate = model.vars.baudrate.value
        # setup inputs for modindex calculations
        mod_samp_rate_factor = self.get_mod_sample_rate_factor(model)
        # calculate modindex
        if modformat == model.vars.modulation_type.var_enum.OQPSK:
            src_output_rate = fxo / 2 if br2m else fxo / 4
            # conv_gain = shaping_filter_output_rate/ src_output_rate
            # conv_gain = (T_fxo * 2 / T_shape), freq --> phase --> freq
            conv_gain = 8 * baudrate / src_output_rate
            modindex = 0.5 * mod_samp_rate_factor * baudrate / (2 * shaping_filter_gain * conv_gain * fxo)
        elif (modformat == model.vars.modulation_type.var_enum.FSK2 or
              modformat == model.vars.modulation_type.var_enum.FSK4 or
              modformat == model.vars.modulation_type.var_enum.MSK):
            modindex = freq_dev_hz / (shaping_filter_gain * (fxo / mod_samp_rate_factor))
        else:
            raise CalculationException("ERROR: %s modulation not yet supported!" % modformat)
        model.vars.modindex.value = modindex

    # Method name: calc_modindex_virtual_reg_field
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_modindex_virtual_reg_field(self, model):
        pass

    # Method name: calc_modulation_index_actual
    # Defined in: common\calculators\calc_modulator.py
    def calc_modulation_index_actual(self, model):
        """
        calculate the actual modulation index for given PHY
        This is the traditional modulation index as 2 * deviation / baudrate
        the one above we call modindex and is specific value used by EFR32
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        baudrate_hz = model.vars.tx_baud_rate_actual.value
        tx_deviation = model.vars.tx_deviation_actual.value
        model.vars.modulation_index_actual.value = tx_deviation * 2.0 / baudrate_hz

    # Method name: calc_symbol_encoding
    # Defined in: ocelot\calculators\calc_modulator.py
    def calc_symbol_encoding(self, model):
        encoding = model.vars.symbol_encoding.value
        demod_select = model.vars.demod_select.value
        if encoding == model.vars.symbol_encoding.var_enum.DSSS:
            coding = 2
        elif (encoding == model.vars.symbol_encoding.var_enum.Manchester or
              encoding == model.vars.symbol_encoding.var_enum.Inv_Manchester) and \
                demod_select != model.vars.demod_select.var_enum.TRECS_VITERBI:
            # Decoder not implemented with Viterbi demod
            # See https://jira.silabs.com/browse/MCUW_RADIO_CFG-2046
            coding = 1
        else:
            coding = 0
        self._reg_write(model.vars.MODEM_CTRL0_CODING, coding)

    # Method name: calc_symbol_rates_actual
    # Defined in: ocelot\calculators\calc_modulator.py
    def calc_symbol_rates_actual(self, model):
        encoding = model.vars.symbol_encoding.value
        encodingEnum = model.vars.symbol_encoding.var_enum
        demod_select = model.vars.demod_select.value
        baud_per_symbol = 1
        if demod_select == model.vars.demod_select.var_enum.LONGRANGE:
            # In case of BLE LR 125 kps, baud_per_symbol is 8
            if model.vars.FRC_CTRL_RATESELECT.value == 0:
                baud_per_symbol = 8
            # In case of BLE LR 500 kps, baud_per_symbol is 2
            elif model.vars.FRC_CTRL_RATESELECT.value == 2:
                baud_per_symbol = 2
            else:
                raise ValueError("Invalid FRC_CTRL_RATESELECT value used in LONGRANGE configuration")
        if model.vars.FRC_CTRL_RATESELECT.value == 1:
            encoding = model.vars.MODEM_CTRL6_CODINGB
        if encoding == encodingEnum.LINECODE:
            baud_per_symbol *= 4
        if encoding == encodingEnum.DSSS:
            baud_per_symbol *= model.vars.dsss_len.value
        elif encoding == encodingEnum.Manchester or encoding == encodingEnum.Inv_Manchester:
            baud_per_symbol *= 2
        model.vars.baud_per_symbol_actual.value = baud_per_symbol
        if encoding == encodingEnum.DSSS:
            bits_per_symbol = model.vars.dsss_bits_per_symbol.value
        else:
            modFormat = model.vars.modulation_type.value
            modFormatEnum = model.vars.modulation_type.var_enum
            if modFormat in [modFormatEnum.FSK4, modFormatEnum.OQPSK]:
                bits_per_symbol = 2
            else:
                bits_per_symbol = 1
        model.vars.bits_per_symbol_actual.value = bits_per_symbol

    # Method name: calc_synchronous_mixdac_clk
    # Defined in: rainier\calculators\calc_modulator.py
    def calc_synchronous_mixdac_clk(self, model):
        # default to disabled, only HADM PHYs will set the profile input
        model.vars.synchronous_mixdac_clk.value = False

    # Method name: calc_tx_baud_rate_actual
    # Defined in: rainier\calculators\calc_modulator.py
    def calc_tx_baud_rate_actual(self, model):
        """
        calculate actual TX baud rate from register settings
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        fxo = model.vars.xtal_frequency_hz.value
        txbr_ratio = model.vars.txbr_ratio_actual.value
        interp_factor = 2.0 if model.vars.br2m.value else 4.0
        tx_baud_rate = fxo / interp_factor / 8.0 * txbr_ratio
        model.vars.tx_baud_rate_actual.value = tx_baud_rate

    # Method name: calc_tx_br2m
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_tx_br2m(self, model):
        """
        controls the interpolator ratio and SRC outout_rate
        interpolator ratio is 2X when br2m = 1, 4X when br2m = 0
        SRC outout_rate is f_xo/2 when br2m = 1, f_xo/4 when br2m = 0

        SRC_ratio = input_rate / output_rate
        input_rate = baudrate * 8
        output_rate = f_xo/2 if br2m else f_xo/4
        given baud_rate and fxo we should choose BR2M so that SRC is as close to 1.0 as possible to get best performance

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        baudrate = model.vars.baudrate.value
        fxo = model.vars.xtal_frequency_hz.value * 1.0

        # given baud_rate and fxo we should choose BR2M so that SRC is as close to 1.0
        # as possible to get best performance
        src_distance_to_1 = float("inf")  # set
        br2m = 0  # set default value
        for br2m_value in range(2 ** model.vars.MOD_TXCTRL_BR2M.get_bit_width()):
            src = (fxo / (2 + 2*(1 - br2m_value))) / (8*baudrate)
            if abs(1 - src) < src_distance_to_1:
                src_distance_to_1 = abs(1 - src)
                br2m = br2m_value

        model.vars.br2m.value = br2m
        self._ip_reg_write(model, 'TXCTRL_BR2M', int(br2m))

    # Method name: calc_tx_delay
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_tx_delay(self, model):
        """ calculate tx delay in ns """
        # : Get Model Variables
        shaping = model.vars.MOD_CTRL0_SHAPING.value
        shaping_filter_taps = model.vars.shaping_filter_taps.value
        tx_baud_rate_actual = model.vars.tx_baud_rate_actual.value

        # : FIR filter is operating at 8x baud rate
        if shaping == 1: # : odd symmetric
            shaping_filter_delay = (shaping_filter_taps + 1) / 2
        else: # : assume even
            shaping_filter_delay = shaping_filter_taps/2
        tx_grp_delay_us = shaping_filter_delay / (8 * tx_baud_rate_actual) * 1e6

        model.vars.tx_grp_delay_us.value = tx_grp_delay_us
    # Method name: calc_tx_freq_dev_actual
    # Defined in: rainier\calculators\calc_modulator.py
    def calc_tx_freq_dev_actual(self, model):
        """
        given register setting return actual frequency deviation used in the modulator
        Using Equations in Table 5.25 of EFR32 Reference Manual (internal.pdf)
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        modformat = model.vars.modulation_type.value
        modindex = model.vars.modindex_actual.value
        shaping_filter_gain = model.vars.shaping_filter_gain_actual.value
        mod_samp_rate = self.get_modulator_sample_rate(model)
        if modformat == model.vars.modulation_type.var_enum.FSK2 or \
                modformat == model.vars.modulation_type.var_enum.FSK4:
            freq_dev_hz = modindex * (mod_samp_rate * shaping_filter_gain)
        else:
            freq_dev_hz = 0.0
        model.vars.tx_deviation_actual.value = freq_dev_hz

    # Method name: calc_tx_mode
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_modulator_select_default(self, model):
        demod_select = model.vars.demod_select.value
        if demod_select == model.vars.demod_select.var_enum.BTC:
            model.vars.modulator_select.value = model.vars.modulator_select.var_enum.IQ_MOD_DIRECT
        else:
            # default should be PHMOD
            model.vars.modulator_select.value = model.vars.modulator_select.var_enum.PH_MOD

    # Method name: calc_txbr_actual
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_txbr_actual(self, model):
        """
        given register values calculate actual TXBR ratio implemented

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        num = model.vars.MOD_TXBR_TXBRNUM.value * 1.0
        # TXBRNUM is a 16bits fractional number
        ratio = num / (2 ** 16)
        model.vars.txbr_ratio_actual.value = ratio

    # Method name: calc_txbr_reg
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def calc_txbr_reg(self, model):
        ratio = model.vars.txbr_ratio.value
        # TXBRNUM is a 16bits fractional number
        self._ip_reg_write(model, 'TXBR_TXBRNUM', int(round(ratio * (2 ** 16))))

    # Method name: calc_txbr_value
    # Defined in: rainier\calculators\calc_modulator.py
    def calc_txbr_value(self, model):
        """
        TXBRNUM is the register used to set SRC ratio. Unlike series 2 where interpolator controlled the datarate,
        an SRC (after shaping) in the modulator datapath indirectly controls the baudrate.
        SRC_ratio = TXBRNUM = input_rate / output_rate
        input_rate = baudrate * 8
        output_rate = f_xo/2 if br2m else f_xo/4
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # Load model values into local variables
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        baudrate = model.vars.baudrate.value
        # calculate baudrate to fxo ratio
        interp_factor = 2.0 if model.vars.br2m.value else 4.0
        ratio = (8.0 * baudrate) / (xtal_frequency_hz / interp_factor)
        # Load local variables back into model variables
        model.vars.txbr_ratio.value = ratio

    # Method name: get_mod_sample_rate_factor
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def get_mod_sample_rate_factor(self, model):
        """
        Return modulator sample multiplier factor based on modulator data path selection
        :param modulator_select:
        :return:
        """
        modulator_select = model.vars.modulator_select.value
        br2m = model.vars.br2m.value
        protocol_id = model.vars.protocol_id.value
        if (modulator_select == model.vars.modulator_select.var_enum.IQ_MOD_DIRECT and
                protocol_id != model.vars.protocol_id.var_enum.BTC):
            if br2m:
                # modulation multiplier is running at (f_xo/2)
                mod_samp_rate_factor = 2
            else:
                # modulation multiplier is running at (f_xo/4)
                mod_samp_rate_factor = 4
        else:  # : PHMOD and IQMOD, inherit calculation from Rainier
            # mod_samp_rate_factor = super().get_mod_sample_rate_factor(model)
            # Sampling rate before cordic is now fxo in all modes"
            mod_samp_rate_factor = 1
        return mod_samp_rate_factor

    # Method name: get_modulator_sample_rate
    # Defined in: lpwh72000\calculators\calc_modulator.py
    def get_modulator_sample_rate(self, model):
        fxo = model.vars.xtal_frequency_hz.value * 1.0
        br2m = model.vars.br2m.value
        modulator_select = model.vars.modulator_select.value
        if False: #modulator_select == model.vars.modulator_select.var_enum.IQ_MOD_DIRECT:
            mod_samp_rate = fxo / 2 if br2m else fxo / 4  # IQMOD
        else:
            # mod_samp_rate = super().get_modulator_sample_rate(model)
            # Sampling rate before cordic is now fxo in all modes"
            mod_samp_rate = fxo
        return mod_samp_rate

# Method name: frac2exp
# Defined in: common\calculators\calc_utilities.py
    def frac2exp(self, max_m, frac, up=False):
        """
        convert fraction into mantissa and exponent format
        Args:
            max_m (unknown) : unknown\n
            frac (unknown) : unknown\n
        """
        if frac == 0:
            return 0, 0
        best_diff = 99e9
        if up:
            m_values = xrange(1, max_m, 1)
        else:
            m_values = xrange(max_m, 0, -1)
        # start with the highest allowed mantissa and find best m, e pair
        for m in m_values:
            e = py2round(math.log(frac / m, 2))
            diff = abs(frac - m * 2**e)
            if diff < best_diff:
                best_diff = diff
                best_e = e
                best_m = m
        return best_m, best_e

# Method name: calc_modulation_index
# Defined in: common\calculators\calc_utilities.py
    def calc_modulation_index(self, model):
        """
        calculate informational modulation index based on baudrate and deviation
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        baudrate_hz = model.vars.baudrate.value
        freq_dev_hz = model.vars.deviation.value * 1.0
        model.vars.modulation_index.value = freq_dev_hz * 2.0 / baudrate_hz