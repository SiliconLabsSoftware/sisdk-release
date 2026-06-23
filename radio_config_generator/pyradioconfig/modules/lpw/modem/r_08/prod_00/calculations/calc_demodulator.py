from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from py_2_and_3_compatibility import *
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from enum import Enum
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from math import *
from py_2_and_3_compatibility import *
from pyradioconfig.parts.ocelot.calculators.calc_shaping import CALC_Shaping_ocelot
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
import numpy as np
import numpy.matlib
from scipy import signal as sp
from pyradioconfig.parts.common.calculators.ksi_cache_utils import KsiCacheMixin
from pyradioconfig.parts.common.calculators.scipy_cache_utils import resample_poly_cached

class CalcDemodulator(KsiCacheMixin, IPCalculator):
    SRC2DENUM = 524288.0

    # Method name: _channel_filter_clocks_valid
    # Defined in: ocelot\calculators\calc_demodulator.py
    def _channel_filter_clocks_valid(self, model, dec0, dec1):
        # returns if the requested configuration is safe to not trigger ipmcusrw-876
        # to avoid the channel filter sampling issue, clks_per_sample >= 4
        # helper function for return_osr_dec0_dec1
        # no margin on the first check. hfxomult clocking at exactly 4 clks/sample will not trigger this issue
        safe_clks_per_sample = self.chf_required_clks_per_sample
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        adc_freq = model.vars.adc_freq_actual.value
        adc_clock_mode_actual = model.vars.adc_clock_mode_actual.value
        base_frequency_hz = model.vars.base_frequency_hz.value
        f_dec1 = adc_freq / (8 * dec0 * dec1)
        clks_per_sample = xtal_frequency_hz / f_dec1
        base_config_valid = clks_per_sample >= safe_clks_per_sample
        # for lodiv based clocking, sample rate varies with RF. VCODIV PHYs are only used in the 2.4G band
        # maximum ppm change can be determined by the min, max of the FCC band of 2400-2483.5 MHz
        # for current 2.4G LODIV products, if its LODIV and subG the channel plan doesn't span
        # wide enough where this is a problem
        in_2p4G_band = base_frequency_hz >= 2400e6 and base_frequency_hz <= 2500e6
        if adc_clock_mode_actual == model.vars.adc_clock_mode.var_enum.VCODIV and in_2p4G_band:
            max_rf_frequency = 2480e6
            max_ppm = (max_rf_frequency - base_frequency_hz) / base_frequency_hz
            # (1-max_ppm because adc_freq is in the denominator
            clks_per_sample_highest_channel = clks_per_sample * (1 - max_ppm)
            highest_channel_valid = clks_per_sample_highest_channel >= self.chf_required_clks_per_sample
            valid = base_config_valid and highest_channel_valid
        else:
            valid = base_config_valid
        return valid

    # Method name: _check_trecs_required_clk_cycles
    # Defined in: ocelot\calculators\calc_demodulator.py
    def _check_trecs_required_clk_cycles(self, adc_freq, baudrate, osr, dec0, dec1, xtal_frequency_hz, relaxsrc2,
                                         model):
        # Returns True if the filter chain configuration meets the requirement for trecs
        # minimum clock cycles between samples. Returns False if the configuration is invalid
        #
        # IPMCUSRW-668 - TRECS requires minimum of 4 clk between samples. SRC interpolation on ocelot
        # has a fixed 3 clk separation and cannot be used with TRECS. Limiting max_src2_ratio is sufficient
        # for ocelot, but this function is used by inherited classes which are able to adjust the
        # interpolated sample clk delay
        # calculate the src_ratio as this function is called in the process of evaluating
        # osr, dec0, dec1, so the src_ratio_actual cannot be calculated
        dec1_freq = adc_freq / (8 * dec0 * dec1)
        src_freq = baudrate * osr
        src_ratio = src_freq / dec1_freq
        TRECS_REQUIRED_CLKS_PER_SAMPLE = 4
        bandwidth_hz = model.vars.bandwidth_hz.value
        is_vcodiv = model.vars.adc_clock_mode.value == model.vars.adc_clock_mode.var_enum.VCODIV
        if src_ratio > 1:
            # ocelot has fixed clk delay of 3
            # IPMCUSRW-668 when it occurs causes slightly slower waterfall curves, and minor < 1% PER bumps
            # if a PHY suffers from IPMCUSRW-876 (channel filter clocks), it is preferable to solve the channel
            # filter issue by allowing the PHY workaround of a lower f_dec1 and interpolation on SRC2
            bandwidth_threshold = 38e6 / 4 * 0.2  # minimum hfxo / chf_clks_per_sample * min_bwsel
            return relaxsrc2 and is_vcodiv and bandwidth_hz > bandwidth_threshold
        else:
            cycles_per_sample = floor(xtal_frequency_hz / src_freq)
            meets_clk_cycle_requirement = cycles_per_sample >= TRECS_REQUIRED_CLKS_PER_SAMPLE
            return meets_clk_cycle_requirement

    # Method name: calc_bandwdith_tol
    # Defined in: bobcat\calculators\calc_demodulator.py
    def calc_bandwdith_tol(self, model):
        # For 2.4GHz PHYs that use divided down LO for ADC, we inherently will have some bandwidth tolerance
        # based on the amount the clock is allowed to change
        protocol_id = model.vars.protocol_id.value
        base_frequency_hz = model.vars.base_frequency_hz.value
        if protocol_id == model.vars.protocol_id.var_enum.Zigbee:
            # Assume our target bandwidth_hz applies to center of band
            # Therefore we are allowed tolerance based on how far away we currently are
            bandwidth_tol = abs((base_frequency_hz - 2450e6) / base_frequency_hz)
        else:
            bandwidth_tol = 0.0
        model.vars.bandwidth_tol.value = float(bandwidth_tol)

    # Method name: calc_bandwidth_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_bandwidth_actual(self, model):
        # This function calculates the actual channel bandwidth based on adc rate, decimator, and bwsel settings
        # Load model variables into local variables
        adc_freq_actual = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        dec1_actual = model.vars.dec1_actual.value
        bwsel = model.vars.bwsel.value
        # Calculate the actual channel bandwidth
        bandwidth_actual = int(adc_freq_actual * bwsel / dec0_actual / dec1_actual / 8)
        # Load local variables back into model variables
        model.vars.bandwidth_actual.value = bandwidth_actual

    # Method name: calc_baudrate
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_baudrate(self, model):
        # This function calculates baudrate based on the input bitrate and modulation/encoding settings
        # Load model variables into local variables
        mod_type = model.vars.modulation_type.value
        bitrate_gross = model.vars.bitrate_gross.value
        encoding = model.vars.symbol_encoding.value
        spreading_factor = model.vars.dsss_spreading_factor.value
        # Based on modulation type calculate baudrate from bitrate
        if (mod_type == model.vars.modulation_type.var_enum.OQPSK) or \
                (mod_type == model.vars.modulation_type.var_enum.OOK) or \
                (mod_type == model.vars.modulation_type.var_enum.ASK) or \
                (mod_type == model.vars.modulation_type.var_enum.FSK2) or \
                (mod_type == model.vars.modulation_type.var_enum.MSK) or \
                (mod_type == model.vars.modulation_type.var_enum.BPSK) or \
                (mod_type == model.vars.modulation_type.var_enum.DBPSK):
            baudrate = bitrate_gross
        elif (mod_type == model.vars.modulation_type.var_enum.FSK4):
            baudrate = bitrate_gross / 2
        else:
            raise CalculationException('ERROR: modulation type not supported in calc_baudrate()')
        # Account for the DSSS spreading factor
        if (encoding == model.vars.symbol_encoding.var_enum.DSSS):
            baudrate *= spreading_factor
        # Load local variables back into model variables
        model.vars.baudrate.value = int(round(baudrate))

    # Method name: calc_baudrate_actual
    # Defined in: bobcat\calculators\calc_demodulator.py
    def calc_baudrate_actual(self, model):
        # This function calculates the actual baudrate based on register settings
        # Load model variables into local variables
        adc_freq = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        dec1_actual = model.vars.dec1_actual.value
        dec2_actual = model.vars.dec2_actual.value
        src2ratio_actual = model.vars.src2_ratio_actual.value
        rxbrfrac_actual = model.vars.rxbrfrac_actual.value
        # Calculate actual baudrate once the ADC, decimator, SRC, and rxbr settings are kown
        baudrate_actual = (adc_freq * src2ratio_actual) / (
                    dec0_actual * dec1_actual * dec2_actual * 8 * 2 * rxbrfrac_actual)
        # Load local variables back into model variables
        model.vars.rx_baud_rate_actual.value = baudrate_actual


    def calc_bitrate_gross(self, model):
        #This function calculates the gross bitrate (bitrate including redundant coding bits)
        #Note that this gross bitrate excludes DSSS, because in RX the DSSS chips never make it
        #through the demod path (they are only used for correlation)

        #Read from model variables
        bitrate = model.vars.bitrate.value
        encoding = model.vars.symbol_encoding.value
        mbus_encoding = model.vars.mbus_symbol_encoding.value
        fec_enabled = model.vars.fec_enabled.value
        fec_en = model.vars.fec_en.value # FEC configuration
        ble_concurrent = (model.vars.MODEM_LONGRANGE_LRBLE.value == 1) and (model.vars.MODEM_COCURRMODE_CONCURRENT.value == 1)

        #Start by assuming the gross bitrate is equal to the net bitrate
        bitrate_gross = bitrate

        #Calculate the encoded bitrate based on the encoding parameters
        if (encoding == model.vars.symbol_encoding.var_enum.Manchester or encoding == model.vars.symbol_encoding.var_enum.Inv_Manchester):
            bitrate_gross *= 2
        if (mbus_encoding == model.vars.mbus_symbol_encoding.var_enum.MBUS_3OF6):
            bitrate_gross *= 1.5
        if ble_concurrent:
            # In BLE LR mode, FEC is always 1/2 rate
            bitrate_gross *= 2
        if fec_enabled:
                if fec_en not in [model.vars.fec_en.var_enum.FEC_BLE_HDT]:
                    # BLE HDT FEC shall not affect the non-HDT demods
                    bitrate_gross *= 2

        #Write the model variable
        model.vars.bitrate_gross.value =  int(round(bitrate_gross))

    # Method name: calc_brcal_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_brcal_reg(self, model):
        # This function writes the brcal average and enable registers
        # Load model variables into local variables
        brcalavg = model.vars.brcalavg.value
        brcalen = model.vars.brcalen.value
        # Write registers
        self._ip_reg_write(model, 'CTRL5_BRCALAVG', brcalavg)
        self._ip_reg_write(model, 'CTRL5_BRCALEN', brcalen)

    # Method name: calc_brcalmode_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_brcalmode_reg(self, model):
        # This function writes the brcal model register
        # Write register
        self._ip_reg_write(model, 'CTRL5_BRCALMODE', 0)

    # Method name: calc_bw_carson
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_bw_carson(self, model):
        # This function calculates the Carson bandwidth (minimum bandwidth)
        # Load model variables into local variables
        baudrate = model.vars.baudrate.value
        deviation = model.vars.deviation.value
        mod_type = model.vars.modulation_type.value
        # Calculate the Carson bandwidth
        if (mod_type == model.vars.modulation_type.var_enum.FSK4):
            # Assumes deviation = inner symbol deviation
            bw_carson = baudrate + 6 * deviation
        else:
            bw_carson = baudrate + 2 * deviation
        # Load local variables back into model variables
        model.vars.bandwidth_carson_hz.value = int(bw_carson)

    # Method name: calc_bwsel
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_bwsel(self, model, softmodem_narrowing=False):
        # This function calculates the bwsel ratio that sets the channel bandwidth
        # Load model variables into local variables
        adc_freq = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        dec1_actual = model.vars.dec1_actual.value
        afc_run_mode = model.vars.afc_run_mode.value
        bandwidth = model.vars.bandwidth_hz.value  # We don't know the actual channel bandwidth yet
        lock_bandwidth = model.vars.lock_bandwidth_hz.value  # maybe this cab be reduced further based on residual freq offset
        min_bwsel = model.vars.min_bwsel.value
        # Calculate the required BWSEL from the adc rate, decimators, and required bandwidth
        bwsel = float(bandwidth * 8 * dec0_actual * dec1_actual) / adc_freq
        lock_bwsel = float(lock_bandwidth * 8 * dec0_actual * dec1_actual) / adc_freq
        # print(f"BWSEL = {bwsel}, LOCK_BWSEL = {lock_bwsel}")
        if (lock_bwsel < min_bwsel) and (
                (afc_run_mode == model.vars.afc_run_mode.var_enum.ONE_SHOT) or softmodem_narrowing):
            lock_bwsel = min_bwsel
        # Load local variables back into model variables
        model.vars.bwsel.value = bwsel
        model.vars.lock_bwsel.value = lock_bwsel

    # Method name: calc_chmutetimer_reg
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_chmutetimer_reg(self, model):
        hop_enable = model.vars.hop_enable.value == model.vars.hop_enable.var_enum.ENABLED
        duty_cycled = model.vars.rxdc_power_save_mode.value != model.vars.rxdc_power_save_mode.var_enum.DISABLED
        if duty_cycled:
            # This directly controls period of NOISE detector duration (and hence duty cycle ON period)
            chmutetimer = 280  # For BLE: 280 - For ZB: 170
        elif hop_enable:
            chmutetimer = 195  # Default value for 2ZB hopping
        else:
            chmutetimer = 0
        self._ip_reg_write(model, 'SRCCHF_CHMUTETIMER', chmutetimer)

    # Method name: calc_datafilter
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_datafilter(self, model):
        demod_select = model.vars.demod_select.value
        osr = model.vars.oversampling_rate_actual.value
        demod_sel = model.vars.demod_select.value
        modformat = model.vars.modulation_type.value
        remoden = model.vars.MODEM_PHDMODCTRL_REMODEN.value
        remoddwn = model.vars.MODEM_PHDMODCTRL_REMODDWN.value + 1
        trecs_enabled = model.vars.trecs_enabled.value
        cplx_corr_enabled = model.vars.MODEM_CTRL6_CPLXCORREN.value == 1

        if demod_select == model.vars.demod_select.var_enum.BTC:
            model.vars.datafilter_taps.value = 2
        else:
            if demod_sel == model.vars.demod_select.var_enum.COHERENT and \
                    modformat == model.vars.modulation_type.var_enum.OQPSK:
                # : For Cohererent demod, set data filter taps to 9
                # : TODO for complex correlation enabled, set datafilter taps to 6
                if cplx_corr_enabled:
                    datafilter_taps = 6
                else:
                    datafilter_taps = 9
            # no data filter in path when TRecS is enabled
            elif demod_sel == model.vars.demod_select.var_enum.BCR or \
                    modformat == model.vars.modulation_type.var_enum.OQPSK or \
                    (trecs_enabled and not remoden) or remoddwn > 1:
                datafilter_taps = 2  # 2 here translates to datafilter_reg = 0 meaning disabled datafilter
            # Calculate datafitler based on OSR
            elif (osr > 1) and (osr < 10):
                datafilter_taps = int(round(osr))
            else:
                raise CalculationException('ERROR: OSR out of range in calc_datafilter()')

            # Load local variables back into model variables
            model.vars.datafilter_taps.value = datafilter_taps

    # Method name: calc_datafilter_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_datafilter_actual(self, model):
        # This function calculates the actual datafilter taps from the register value
        # Load model variables into local variables
        datafilter_reg = model.vars.MODEM_CTRL2_DATAFILTER.value
        # The number of taps is the register value plus 2
        datafilter_taps_actual = datafilter_reg
        # Load local variables back into model variables
        model.vars.datafilter_taps_actual = datafilter_taps_actual

    # Method name: calc_datafilter_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_datafilter_reg(self, model):
        # This function writes the datafilter register
        # Load model variables into local variables
        datafilter_taps = model.vars.datafilter_taps.value
        # The datafilter register setting is 2 less than the number of taps
        datafilter_reg = datafilter_taps - 2
        if datafilter_reg < 0:
            datafilter_reg = 0
        # Write register
        self._ip_reg_write(model, 'CTRL2_DATAFILTER', datafilter_reg)

    # Method name: calc_datapath_delays
    # Defined in: lpwh74000\calculators\calc_demodulator.py
    def calc_datapath_delays(self, model):

        dec0 = model.vars.dec0_actual.value
        dec1 = model.vars.dec1_actual.value
        dec2 = model.vars.dec2_actual.value
        datafilter_taps = model.vars.datafilter_taps.value
        chflatency = model.vars.chflatency_actual.value
        src2_actual = model.vars.src2_ratio_actual.value
        adc_freq_actual = model.vars.adc_freq_actual.value
        trecs_enabled = model.vars.trecs_enabled.value
        harddecision_enabled = model.vars.MODEM_VITERBIDEMOD_HARDDECISION.value == 1
        remoden = model.vars.MODEM_PHDMODCTRL_REMODEN.value
        remoddwn = model.vars.MODEM_PHDMODCTRL_REMODDWN.value
        oversampling_rate = model.vars.oversampling_rate_actual.value
        baudrate_actual = model.vars.rx_baud_rate_actual.value

        # : DEC8
        dec8_filter_taps = del_dec8 = 22
        dec8_filter_rate = adc_freq_actual / 8
        dec8_grp_delay = dec8_filter_taps / 2
        dec8_grp_delay_us = dec8_grp_delay / adc_freq_actual * 1e6

        # : DEC0
        del_dec0_filter_taps_dict = {3:27, 4:27, 5:30, 8:40}
        del_dec0 = del_dec0_filter_taps_dict[dec0]
        dec0_filter_taps = del_dec0
        dec0_filter_rate = dec8_filter_rate / dec0
        dec0_grp_delay = dec0_filter_taps / 2
        dec0_grp_delay_us = dec0_grp_delay / dec8_filter_rate * 1e6

        # : IRCAL
        dc_ircal_digmix_grp_delay = del_dc_ircal_digmix = 2
        dc_ircal_digmix_rate = dec0_filter_rate
        dc_ircal_digmix_grp_delay_us = dc_ircal_digmix_grp_delay / dc_ircal_digmix_rate * 1e6

        # : DEC1
        dec1_filter_taps = del_dec1 = (dec1 - 1) * 4.0 + 1
        dec1_filter_rate = dc_ircal_digmix_rate / dec1
        dec1_delay = dec1_filter_taps / 2
        dec1_grp_delay_us = dec1_delay / dc_ircal_digmix_rate * 1e6

        # : channel filter
        chf_filter_taps = del_chflt = 29.0 - chflatency * 6.0
        # print(f"Channel Filter number of taps = {chf_filter_taps}")
        chf_filter_rate = dec1_filter_rate
        # : channel filter is odd (taps+1)/2.
        # : -1 term comes from CHF input goes directly into the combinational logic and does not pass into the delay line before multiplier.
        chf_grp_delay = (chf_filter_taps + 1) / 2 - 1 # : channel filter is odd (taps+1)/2.
        chf_grp_delay_us = chf_grp_delay / chf_filter_rate * 1e6

        # : src delay
        src2_grp_delay = del_src2 = 2
        src2_rate = chf_filter_rate * src2_actual
        src2_delay_us = src2_grp_delay / chf_filter_rate * 1e6

        # Digital gain and CORDIC do not introduce any delays
        del_digigain = 0
        del_cordic = 0

        # Differentiation delay of 1, frequency gain has no delay
        diff_grp_delay = del_diff = 1
        diff_rate = src2_rate
        diff_delay_us = diff_grp_delay / diff_rate * 1e6

        # : DEC2
        dec2_grp_delay = del_dec2 = dec2
        dec2_rate = src2_rate / dec2
        dec2_delay_us = dec2_grp_delay / src2_rate * 1e6

        # : data filter delay
        del_data = datafilter_taps
        datafilter_grp_delay = datafilter_taps / 2
        datafilter_rate = dec2_rate
        datafilter_delay_us = datafilter_grp_delay / datafilter_rate * 1e6

        # : Phase Remod Down sampling delay
        if remoddwn > 1:
            del_remod = remoddwn
            remod_rate = dec2_rate / remoddwn
            remod_delay_us = del_remod / remod_rate * 1e6
        else:
            del_remod = 0
            remod_delay_us = 0

        # : calculate delay in samples from adc to src
        del_adc_to_src = (((del_dec8 / 8 + del_dec0) / dec0 + del_dc_ircal_digmix + del_dec1) / dec1 + \
                           del_chflt + del_src2) / src2_actual

        # : calculate delay in samples from adc to diff
        del_adc_to_diff = del_adc_to_src + del_digigain + del_cordic + del_diff

        grpdel_mixer_to_diff = ((del_dec1 + 1) / 2 / dec1 + (del_chflt + 1) / 2 + del_src2) / src2_actual + del_digigain + del_cordic + del_diff

        # : Calculate group delay to src in us
        grp_delay_to_src_us = dec8_grp_delay_us + dec0_grp_delay_us + dc_ircal_digmix_grp_delay_us + \
                              dec1_grp_delay_us + chf_grp_delay_us + src2_delay_us

        # : delay within demod
        if trecs_enabled and not harddecision_enabled:
            # : MCUW_RADIO_CFG-2395: depth of viterbi decoder in demod is 4 symbols
            demod_delay_symbols = 4
        else:
            demod_delay_symbols = 0
        demod_delay_us = demod_delay_symbols / baudrate_actual * 1e6

        # : Calculate group delay for each demod
        if trecs_enabled:
            if remoden == 1 and remoddwn == 0:  # demod at DEC2 output
                grp_delay_us = grp_delay_to_src_us + diff_delay_us + dec2_delay_us + demod_delay_us
                delay_adc_to_demod = (del_adc_to_diff + del_dec2) / dec2  # delay at dec2 output in samples at that point
                delay_adc_to_demod_symbols = (delay_adc_to_demod + del_data) / oversampling_rate / dec2
                grpdelay_to_demod = (grpdel_mixer_to_diff + (del_dec2 + 1) / 2) / dec2  # delay at dec2 output in samples at that point
                delay_agc = delay_adc_to_demod * dec2 * src2_actual
            elif remoden == 1 and remoddwn > 1: # demod at down sampler
                grp_delay_us = grp_delay_to_src_us + diff_delay_us + dec2_delay_us + datafilter_delay_us + remod_delay_us + demod_delay_us
                delay_adc_to_demod = ((del_adc_to_diff + del_dec2) / dec2 + del_data + del_remod) / remoddwn
                delay_adc_to_demod_symbols = delay_adc_to_demod / oversampling_rate / dec2
                grpdelay_to_demod = ((grpdel_mixer_to_diff + (del_dec2 + 1) / 2) / dec2 + (del_data + 1) / 2 + (del_remod + 1) / 2) / remoddwn
                delay_agc = delay_adc_to_demod * dec2 * src2_actual * remoddwn
            else: # : demod at differentiator
                grp_delay_us = grp_delay_to_src_us + diff_delay_us + demod_delay_us
                delay_adc_to_demod = del_adc_to_diff
                delay_adc_to_demod_symbols = delay_adc_to_demod / oversampling_rate
                grpdelay_to_demod = grpdel_mixer_to_diff
                delay_agc = del_adc_to_diff * src2_actual
        else:
            grp_delay_us = grp_delay_to_src_us + diff_delay_us + dec2_delay_us + datafilter_delay_us
            delay_adc_to_demod = (del_adc_to_diff + del_dec2) / dec2 + del_data
            delay_adc_to_demod_symbols = delay_adc_to_demod / oversampling_rate / dec2
            grpdelay_to_demod = (grpdel_mixer_to_diff + (del_dec2 + 1) / 2) / dec2 + (del_data + 1) / 2
            delay_agc = delay_adc_to_demod * dec2 * src2_actual

        model.vars.rx_grp_delay_us.value = grp_delay_us
        model.vars.grpdelay_to_demod.value = int(ceil(grpdelay_to_demod))
        model.vars.agc_settling_delay.value = int(ceil(delay_agc))
        model.vars.delay_adc_to_demod_symbols.value = int(ceil(delay_adc_to_demod_symbols))


    # Method name: calc_default_feature_mode
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_default_feature_mode(self, model):
        model.vars.zigbee_feature.value = model.vars.zigbee_feature.var_enum.NONE
        model.vars.ble_feature.value = model.vars.ble_feature.var_enum.NONE

    # Method name: calc_demod_misc
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_demod_misc(self, model):
        # Now that we always use the digital mixer, the CFOSR reg field is never used
        pass

    # Method name: calc_demod_rate_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_demod_rate_actual(self, model):
        # This function calculates the actual sample rate at the demod
        # Load model variables into local variables
        adc_freq_actual = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        dec1_actual = model.vars.dec1_actual.value
        dec2_actual = model.vars.dec2_actual.value
        src2_actual = model.vars.src2_ratio_actual.value
        demod_rate_actual = adc_freq_actual * src2_actual / (8 * dec0_actual * dec1_actual * dec2_actual)
        # Load local variables back into model variables
        model.vars.demod_rate_actual.value = demod_rate_actual

    # Method name: calc_demod_sel
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_demod_sel(self, model):
        protocol_id = model.vars.protocol_id.value
        modtype = model.vars.modulation_type.value
        tol = model.vars.baudrate_tol_ppm.value
        mi = model.vars.modulation_index.value
        antdivmode = model.vars.antdivmode.value
        directmode_rx = model.vars.directmode_rx.value

        if protocol_id == model.vars.protocol_id.var_enum.BTC:
            demod_select = model.vars.demod_select.var_enum.BTC
            [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select)
            model.vars.demod_select.value = demod_select
            model.vars.target_osr.value = target_osr
            model.vars.targetmin_osr.value = min_osr
            model.vars.targetmax_osr.value = max_osr
            model.vars.dec0.value = dec0
            model.vars.dec1.value = dec1
        else:
            if hasattr(model.profiles, 'Long_Range'):
                is_long_range = model.profile == model.profiles.Long_Range
            else:
                is_long_range = False

            if model.vars.demod_select._value_forced != None:
                demod_select = model.vars.demod_select._value_forced
                [target_osr, dec0, dec1, min_osr, max_osr] = self.return_solution(model, demod_select)

            elif directmode_rx != model.vars.directmode_rx.var_enum.DISABLED:  # Have to use BCR if using direct mode. See https://jira.silabs.com/browse/MCUW_RADIO_CFG-1515
                if modtype not in [model.vars.modulation_type.var_enum.OOK,
                                   model.vars.modulation_type.var_enum.FSK2]:
                    raise CalculationException("Direct Mode RX is only supported for OOK and 2FSK")

                demod_select = model.vars.demod_select.var_enum.BCR
                [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select)

            else:
                # choose demod_select based on modulation and demod priority
                if (modtype == model.vars.modulation_type.var_enum.OOK) or \
                        (modtype == model.vars.modulation_type.var_enum.ASK):
                    demod_select = model.vars.demod_select.var_enum.BCR
                    [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select)
                    # TODO: Is there a case where osr < 7

                elif (modtype == model.vars.modulation_type.var_enum.OQPSK):
                    if is_long_range:
                        demod_select = model.vars.demod_select.var_enum.COHERENT
                        [target_osr, dec0, dec1, min_osr, max_osr] = self.return_solution(model, demod_select)
                    else:
                        demod_select = model.vars.demod_select.var_enum.LEGACY
                        [target_osr, dec0, dec1, min_osr, max_osr] = self.return_solution(model, demod_select)

                elif (modtype == model.vars.modulation_type.var_enum.BPSK) or \
                        (modtype == model.vars.modulation_type.var_enum.DBPSK):
                    demod_select = model.vars.demod_select.var_enum.LEGACY
                    [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select)

                elif (modtype == model.vars.modulation_type.var_enum.FSK4):

                    demod_select = model.vars.demod_select.var_enum.LEGACY
                    [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select)

                elif (modtype == model.vars.modulation_type.var_enum.FSK2 or \
                      modtype == model.vars.modulation_type.var_enum.MSK):

                    # : for these antdivmode, can only use legacy or coherent demod
                    if antdivmode == model.vars.antdivmode.var_enum.ANTSELFIRST or \
                            antdivmode == model.vars.antdivmode.var_enum.ANTSELCORR or \
                            antdivmode == model.vars.antdivmode.var_enum.ANTSELRSSI:
                        demod_select = model.vars.demod_select.var_enum.LEGACY
                        [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select)
                    else:
                        if tol > 10000:
                            demod_select = model.vars.demod_select.var_enum.BCR
                            [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select)
                        else:
                            if mi < 1.0:
                                if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV:
                                    # : don't use legacy demod for this anntena diversity mode
                                    demod_select_list = [model.vars.demod_select.var_enum.TRECS_VITERBI,
                                                         model.vars.demod_select.var_enum.BCR]
                                else:
                                    demod_select_list = [model.vars.demod_select.var_enum.TRECS_VITERBI,
                                                         model.vars.demod_select.var_enum.BCR,
                                                         model.vars.demod_select.var_enum.LEGACY]
                            else:
                                if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV:
                                    # : don't use legacy demod for this anntena diversity mode
                                    demod_select_list = [model.vars.demod_select.var_enum.TRECS_SLICER,
                                                         model.vars.demod_select.var_enum.BCR]
                                else:
                                    demod_select_list = [model.vars.demod_select.var_enum.TRECS_SLICER,
                                                         model.vars.demod_select.var_enum.BCR,
                                                         model.vars.demod_select.var_enum.LEGACY]

                            # loop over demod list and see if we can find a solution
                            for demod_select in demod_select_list:
                                [target_osr, dec0, dec1, min_osr, max_osr] = self.return_solution(model, demod_select)

                                # stop at first solution
                                if target_osr != 0:
                                    break

            if target_osr == 0:
                raise CalculationException('WARNING: target_osr=0 in calc_choose_demod()')

            # from https://jira.silabs.com/browse/MCUW_RADIO_CFG-1994
            # do not support modulation index less than 0.4 for TRECS
            if (demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI \
                or demod_select == model.vars.demod_select.var_enum.TRECS_SLICER) \
                    and 0.0 < mi < 0.4:
                # Adding 0.0 < mi for CW PHYs
                LogMgr.Error("ERROR: Modulation indices less than 0.4 not supported for 2FSK on this part")

            model.vars.demod_select.value = demod_select
            model.vars.target_osr.value = int(target_osr)
            model.vars.targetmin_osr.value = int(min_osr)
            model.vars.targetmax_osr.value = int(max_osr)
            model.vars.dec0.value = int(dec0)
            model.vars.dec1.value = int(dec1)

    # Method name: calc_detdis_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_detdis_reg(self, model):
        # This method calculates the MODEM_CTRL0_DETDIS field
        # For Ocelot always set to 0
        self._ip_reg_write(model, 'CTRL0_DETDIS', 0)

    # Method name: calc_devoffcomp_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_devoffcomp_reg(self, model):
        # This function calculates the register value of devoffcomp
        # Load model variables into local variables
        mod_type = model.vars.modulation_type.value
        if (mod_type == model.vars.modulation_type.var_enum.FSK4):
            devoffcomp = 1
        else:
            devoffcomp = 0
        # Write register
        self._ip_reg_write(model, 'CTRL4_DEVOFFCOMP', devoffcomp)

    # Method name: calc_devweightdis_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_devweightdis_reg(self, model):
        # This function calculates the register value of devweightdis
        # Load model variables into local variables
        mod_type = model.vars.modulation_type.value
        rx_deviation_scaled = model.vars.rx_deviation_scaled.value
        if (mod_type == model.vars.modulation_type.var_enum.FSK2) or \
                (mod_type == model.vars.modulation_type.var_enum.MSK):
            if (abs(rx_deviation_scaled - 64) > 6):
                devweightdis = 1
            else:
                devweightdis = 0
        else:
            devweightdis = 0
        # Write register
        self._ip_reg_write(model, 'CTRL2_DEVWEIGHTDIS', devweightdis)

    # Method name: calc_digmix_res_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_digmix_res_actual(self, model):
        # This function calculates the digital mixer register
        # Load model variables into local variables
        adc_freq_actual = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        # digital mixer frequency resolution, Hz/mixer ticks
        digmix_res = adc_freq_actual / ((2 ** 20) * 8.0 * dec0_actual)
        model.vars.digmix_res_actual.value = digmix_res

    # Method name: calc_directmode_regs
    # Defined in: bobcat\calculators\calc_demodulator.py
    def calc_directmode_regs(self, model):
        # Set defaults to disabled for Bobcat (or 2.4GHz parts)
        model.vars.directmode_rx.value = model.vars.directmode_rx.var_enum.DISABLED
        model.vars.asynchronous_rx_enable.value = False

    # Method name: calc_dsa_enable
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_dsa_enable(self, model):
        # This function sets a value for dsa_enable
        dsa_enable = False
        # Write the model variable
        model.vars.dsa_enable.value = dsa_enable

    # Method name: calc_dsss_concurrent_reg
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_dsss_concurrent_reg(self, model):
        trecs_used = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        enhdsss_used = model.vars.MODEM_EHDSSSCTRL_EHDSSSEN.value
        # https://jira.silabs.com/browse/MCUW_RADIO_CFG-2587
        # making this calculation makes sure concurrent detection is disabled for standalone PHYs
        if trecs_used and enhdsss_used:
            self._ip_reg_write(model, 'COCURRMODE_DSSSCONCURRENT', 1)
        else:
            self._ip_reg_write(model, 'COCURRMODE_DSSSCONCURRENT', 0)

    # Method name: calc_fast_switching_regs
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_fast_switching_regs(self, model):
        hop_enable = True if model.vars.hop_enable.value == model.vars.hop_enable.var_enum.ENABLED else False
        protocol_id = model.vars.protocol_id.value
        ble2zb_hop = model.vars.MODEM_COCURRMODE_DSSSCONCURRENT.value
        # Enable DTIMLOSS feature for BLE2ZB fast switching PHYs
        # See https://jira.silabs.com/browse/MCUW_RADIO_CFG-2525
        if hop_enable and ble2zb_hop and protocol_id == model.vars.protocol_id.var_enum.Zigbee:
            self._ip_reg_write(model, 'TRECSCFG_DTIMLOSSEN', 1)
            self._ip_reg_write(model, 'TRECSCFG_DTIMLOSSTHD', 200)
        elif hop_enable and ble2zb_hop and protocol_id == model.vars.protocol_id.var_enum.BLE:
            self._ip_reg_write(model, 'TRECSCFG_DTIMLOSSEN', 1)
            self._ip_reg_write(model, 'TRECSCFG_DTIMLOSSTHD', 1000)
        else:
            self._ip_reg_write(model, 'TRECSCFG_DTIMLOSSEN', 0)
            self._ip_reg_write(model, 'TRECSCFG_DTIMLOSSTHD', 0)

    # Method name: calc_fasthopping_regs
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_fasthopping_regs(self, model):
        duty_cycled = model.vars.rxdc_power_save_mode.value is not model.vars.rxdc_power_save_mode.var_enum.DISABLED
        if duty_cycled:
            fasthoppingen = 0
            # Required for NOISEDET IF to trigger ISR for duty-cycle + noise detector
            hoppingsrc = 0
            fwhopping = 1
        else:
            # Default values
            fasthoppingen = 0
            hoppingsrc = 0
            fwhopping = 0
        self._ip_reg_write(model, 'PHDMODCTRL_FASTHOPPINGEN', fasthoppingen)  # Default value
        self._ip_reg_write(model, 'DIGMIXCTRL_HOPPINGSRC', hoppingsrc)
        self._ip_reg_write(model, 'DIGMIXCTRL_FWHOPPING', fwhopping)

    # Method name: calc_forceoff_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_forceoff_reg(self, model):
        demod_sel = model.vars.demod_select.value
        trecs_enabled = model.vars.trecs_enabled.value
        if demod_sel == model.vars.demod_select.var_enum.BCR or trecs_enabled:
            clock_gate_off_reg = 0xfdff
        else:
            clock_gate_off_reg = 0x00
        self._ip_reg_write(model, 'CGCLKSTOP_FORCEOFF', clock_gate_off_reg)

    # Method name: calc_freq_dev_max
    # Defined in: bobcat\calculators\calc_demodulator.py
    def calc_freq_dev_max(self, model):
        # Reading variables from model variables
        fdeverror = model.vars.deviation_tol_ppm.value
        deviation = model.vars.deviation.value
        freq_dev_max = int(deviation + (fdeverror * deviation) / 1000000)
        model.vars.freq_dev_max.value = freq_dev_max

    # Method name: calc_freq_dev_min
    # Defined in: bobcat\calculators\calc_demodulator.py
    def calc_freq_dev_min(self, model):
        # Reading variables from model variables
        fdeverror = model.vars.deviation_tol_ppm.value
        deviation = model.vars.deviation.value
        freq_dev_min = int(deviation - (fdeverror * deviation) / 1000000)
        model.vars.freq_dev_min.value = freq_dev_min

    # Method name: calc_freq_gain_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_freq_gain_actual(self, model):
        # This function calculates the actual frequency gain from the register values
        # Load model variables into local variables
        M_actual = model.vars.MODEM_MODINDEX_FREQGAINM.value
        E_actual = model.vars.MODEM_MODINDEX_FREQGAINE.value
        freq_gain_actual = M_actual * float(2 ** (2 - E_actual))
        # Load local variables back into model variables
        model.vars.freq_gain_actual.value = freq_gain_actual

    # Method name: calc_freq_gain_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_freq_gain_reg(self, model):
        # This function calculates the frequency gain registers
        # Load model variables into local variables
        freq_gain_target = model.vars.freq_gain.value
        best_error = 1e9
        bestM = 0
        bestE = 0
        for M in range(1, 8):
            for E in range(0, 8):
                calculated_gain = M * 2 ** (2 - E)
                error = abs(freq_gain_target - calculated_gain)
                if error < best_error:
                    best_error = error
                    bestM = M
                    bestE = E
        # Write registers
        self._ip_reg_write(model, 'MODINDEX_FREQGAINM', bestM)
        self._ip_reg_write(model, 'MODINDEX_FREQGAINE', bestE)

    # Method name: calc_freq_gain_target
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_freq_gain_target(self, model):
        # This function calculates the target frequency gain value
        # Load model variables into local variables
        mod_type = model.vars.modulation_type.value
        demod_rate_actual = model.vars.demod_rate_actual.value
        deviation = model.vars.deviation.value
        freq_offset_hz = model.vars.freq_offset_hz.value
        large_tol = (freq_offset_hz > deviation)
        afconeshot = model.vars.MODEM_AFC_AFCONESHOT.value
        trecs_remoden = model.vars.MODEM_PHDMODCTRL_REMODEN.value
        if (mod_type == model.vars.modulation_type.var_enum.FSK2 or \
            mod_type == model.vars.modulation_type.var_enum.MSK) and deviation > 0:
            if large_tol and (not afconeshot) and trecs_remoden:
                freq_gain_target = demod_rate_actual / (4.0 * (deviation + freq_offset_hz * 0.75) / 2.0)
            else:
                freq_gain_target = demod_rate_actual / (4.0 * (deviation + freq_offset_hz) / 2.0)
        elif (mod_type == model.vars.modulation_type.var_enum.FSK4) and deviation > 0:
            freq_gain_target = demod_rate_actual / (4.0 * (3.0 * deviation + freq_offset_hz) / 2.0)
        else:
            freq_gain_target = 0.0
        # Load local variables back into model variables
        model.vars.freq_gain.value = freq_gain_target

    # Method name: calc_freq_gain_virtual_reg
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_freq_gain_virtual_reg(self, model):
        pass

    # Method name: calc_interpolation_gain_actual
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_interpolation_gain_actual(self, model):
        pass

    # Method name: calc_intosr_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_intosr_reg(self, model):
        pass

    # Method name: calc_iq_rate_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_iq_rate_actual(self, model):
        demod_rate_actual = model.vars.demod_rate_actual.value
        dec2_actual = model.vars.dec2_actual.value
        model.vars.iq_rate_actual.value = demod_rate_actual * dec2_actual

    # Method name: calc_isicomp_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_isicomp_reg(self, model):
        # This function calculates the ISICOMP register field
        # Read in global variables
        modulation = model.vars.modulation_type.value
        shaping_filter = model.vars.shaping_filter.value
        # Calculate the ISICOMP value based on filter type and BT
        if modulation == model.vars.modulation_type.var_enum.FSK4:
            if shaping_filter == model.vars.shaping_filter.var_enum.Gaussian:
                # Currently we only consider Gaussian shaping, support for other filter types with 4FSK and ISICOMP is TBD
                # Read in shaping filter param here as some PHYs do not have shaping filter defined if filter is NONE
                shaping_filter_param = model.vars.shaping_filter_param.value
                if shaping_filter_param >= 0.75:
                    isicomp = 5
                elif shaping_filter_param >= 0.6:
                    isicomp = 8
                else:
                    # This is the default BT=0.5 case
                    isicomp = 10
            else:
                # Not gaussian filtering
                isicomp = 8
        else:
            # Do not use ISI compensation for other modulation types
            isicomp = 0
        # Write the register
        self._ip_reg_write(model, 'CTRL4_ISICOMP', isicomp)

    # Method name: calc_ksi1
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_ksi1(self, model):
        # This function writes the ksi1 model variable that is used to program both
        # hardmodem and softmodem ksi1 regs
        # Read in model vars
        phscale_actual = model.vars.phscale_actual.value
        # Call the calculation routine for ksi1 based on actual selected phscale
        model.vars.ksi1.value = self.return_ksi1_calc(model, phscale_actual)

    # Method name: calc_ksi1_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_ksi1_reg(self, model):
        # Read in model vars
        ksi1 = model.vars.ksi1.value
        # Write the reg
        self._reg_sat_write(model.vars.MODEM_VITERBIDEMOD_VITERBIKSI1, ksi1)

    # Method name: calc_ksi2_ksi3
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_ksi2_ksi3(self, model):
        # This function writes the ksi2,3 model variables that are used to program both
        # hardmodem and softmodem ksi regs
        # Read in model vars
        ksi1 = model.vars.ksi1.value
        # Call the calculation routine for ksi2 and ksi3
        ksi2, ksi3, ksi3wb = self.return_ksi2_ksi3_calc(model, ksi1)
        # Write the model vars
        model.vars.ksi2.value = int(ksi2)
        model.vars.ksi3.value = int(ksi3)
        model.vars.ksi3wb.value = int(ksi3wb)

    # Method name: calc_ksi2_ksi3_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_ksi2_ksi3_reg(self, model):
        # Read in model vars
        ksi2 = model.vars.ksi2.value
        ksi3 = model.vars.ksi3.value
        ksi3wb = model.vars.ksi3wb.value
        # Write the reg fields
        self._reg_sat_write(model.vars.MODEM_VITERBIDEMOD_VITERBIKSI2, int(ksi2))
        self._reg_sat_write(model.vars.MODEM_VITERBIDEMOD_VITERBIKSI3, int(ksi3))
        self._reg_sat_write(model.vars.MODEM_VTCORRCFG1_VITERBIKSI3WB, int(ksi3wb))

    # Method name: calc_lock_bandwidth
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_lock_bandwidth(self, model, softmodem_narrowing=False):
        demod_select = model.vars.demod_select.value
        bw_demod = model.vars.demod_bandwidth_hz.value
        afc_run_mode = model.vars.afc_run_mode.value
        rtschmode = model.vars.MODEM_REALTIMCFE_RTSCHMODE.value
        antdivmode = model.vars.antdivmode.value
        bw_acq = model.vars.bandwidth_hz.value
        aox_enable = model.vars.aox_enable.value == model.vars.aox_enable.var_enum.ENABLED
        if demod_select == model.vars.demod_select.var_enum.ENHANCED_DSSS:
            model.vars.lock_bandwidth_hz.value = int(bw_demod)
        else:
            if not aox_enable:
                if (model.vars.demod_bandwidth_hz._value_forced != None):
                    # Prioritize forced value
                    lock_bandwidth_hz = bw_demod
                elif (afc_run_mode == model.vars.afc_run_mode.var_enum.ONE_SHOT) or softmodem_narrowing:
                    # for calculated bw_demod, upper limit: lock_bandwidth_hz <= bandwidth_hz
                    lock_bandwidth_hz = min(bw_demod, bw_acq)
                elif (afc_run_mode == model.vars.afc_run_mode.var_enum.INTERNAL) and rtschmode == 1:
                    if antdivmode != model.vars.antdivmode.var_enum.DISABLE:
                        lock_bandwidth_hz = min(bw_demod, bw_acq)
                    else:
                        lock_bandwidth_hz = bw_acq
                else:
                    # for calculated bw_demod, if AFC is disabled, set lock_bandwidth_hz = bandwidth_hz
                    lock_bandwidth_hz = bw_acq

                model.vars.lock_bandwidth_hz.value = int(lock_bandwidth_hz)
            else:
                # Widen channel filter bandwidth for faster settling time during CTE, controlled by CHFSWSEL
                # See PGBOBCATVALTEST-807. 2xBW came from system study as default. Silicon may need further tweaks
                # to limit step response overshoot, depending on the channel filter
                lock_bandwidth_hz = 2 * bw_acq
                model.vars.lock_bandwidth_hz.value = int(lock_bandwidth_hz)

    # Method name: calc_lock_bandwidth_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_lock_bandwidth_actual(self, model):
        # This function calculates the actual channel bandwidth based on adc rate, decimator, and bwsel settings
        # Load model variables into local variables
        adc_freq_actual = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        dec1_actual = model.vars.dec1_actual.value
        lock_bwsel = model.vars.lock_bwsel.value
        min_bwsel = model.vars.min_bwsel.value
        # Lower limit - calc filter coeffs limits lock_bwsel to min_bwsel
        lock_bwsel_actual = max(lock_bwsel, min_bwsel)
        # Calculate the actual channel bandwidth
        lock_bandwidth_actual = int(adc_freq_actual * lock_bwsel_actual / dec0_actual / dec1_actual / 8)
        # Load local variables back into model variables
        model.vars.lock_bandwidth_actual.value = lock_bandwidth_actual

    # Method name: calc_log2x4_actual
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_log2x4_actual(self, model):
        # Read in model vars
        dec1_actual = model.vars.dec1_actual.value
        log2x4_actual = floor(4 * log2(dec1_actual))
        # Write the model var
        model.vars.log2x4_actual.value = log2x4_actual

    # Method name: calc_maximize_bwsel_range_value
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_maximize_bwsel_range_value(self, model):
        # Set default as false
        model.vars.maximize_bwsel_range.value = False

    # Method name: calc_mbus_symbol_encoding
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_mbus_symbol_encoding(self, model):
        # This function calculates the default value for mbus_symbol_encoding
        # Set defaults
        mbus_symbol_encoding = model.vars.mbus_symbol_encoding.var_enum.NRZ
        # Load local variables back into model variables
        model.vars.mbus_symbol_encoding.value = mbus_symbol_encoding
        model.vars.symbol_encoding.value = model.vars.symbol_encoding.var_enum.NRZ  # mbus_symbol_encoding

    # Method name: calc_mod_type_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_mod_type_actual(self, model):
        # This function calculates the actual modulation type based on the register value
        # Load model variables into local variables
        mod = model.vars.MODEM_CTRL0_MODFORMAT.value
        if mod == 0:
            modformat = '2-FSK'
        elif mod == 1:
            modformat = '4-FSK'
        elif mod == 2:
            modformat = 'BPSK'
        elif mod == 3:
            modformat = 'DBPSK'
        elif mod == 4:
            modformat = 'OQPSK'
        elif mod == 5:
            modformat = 'MSK'
        elif mod == 6:
            modformat = 'OOKASK'
        # Load local variables back into model variables
        model.vars.mod_format_actual.value = modformat

    # Method name: calc_mod_type_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_mod_type_reg(self, model):
        # This function writes the modulation type register
        # Load model variables into local variables
        modformat = model.vars.modulation_type.value
        if modformat == model.vars.modulation_type.var_enum.FSK2 or \
                modformat == model.vars.modulation_type.var_enum.MSK:
            mod = 0
        elif modformat == model.vars.modulation_type.var_enum.FSK4:
            mod = 1
        elif modformat == model.vars.modulation_type.var_enum.BPSK:
            mod = 2
        elif modformat == model.vars.modulation_type.var_enum.DBPSK:
            mod = 3
        elif modformat == model.vars.modulation_type.var_enum.OQPSK:
            mod = 4
        elif modformat == model.vars.modulation_type.var_enum.OOK or \
                modformat == model.vars.modulation_type.var_enum.ASK:
            mod = 6
        else:
            raise CalculationException('ERROR: modulation method in input file not recognized')
        # Write register
        self._ip_reg_write(model, 'CTRL0_MODFORMAT', mod)

    # Method name: calc_modulation_index_for_ksi
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_modulation_index_for_ksi(self, model):
        demod_sel = model.vars.demod_select.value
        modtype = model.vars.modulation_type.value
        freq_dev_max = model.vars.freq_dev_max.value
        freq_dev_min = model.vars.freq_dev_min.value
        baudrate = model.vars.baudrate.value
        # Calculate minimum and maximum possible modulation indices
        mi_min = 2.0 * freq_dev_min / baudrate
        mi_max = 2.0 * freq_dev_max / baudrate
        # Determine which modulation index to use for the purposes of KSI calculation
        mi_to_use = mi_min + (mi_max - mi_min) * 0.5
        if (modtype == model.vars.modulation_type.var_enum.FSK4 and \
                demod_sel == model.vars.demod_select.var_enum.BCR):
            mi_to_use *= 3  # KSI values used for 4FSK + BCR are primarily for CFE-DSA (2FSK-like)
        model.vars.modulation_index_for_ksi.value = mi_to_use

    # Method name: calc_offsetphasemasking_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_offsetphasemasking_reg(self, model):
        # This function calculates OFFSETPHASEMASKING
        modulation = model.vars.modulation_type.value
        if modulation == model.vars.modulation_type.var_enum.BPSK or \
                modulation == model.vars.modulation_type.var_enum.DBPSK:
            self._ip_reg_write(model, 'CTRL4_OFFSETPHASEMASKING', 1)
        else:
            self._ip_reg_write(model, 'CTRL4_OFFSETPHASEMASKING', 0)

    # Method name: calc_osr_actual
    # Defined in: bobcat\calculators\calc_demodulator.py
    def calc_osr_actual(self, model):
        # This function calculates the actual OSR based on the ADC rate and decimator/SRC values
        # Load model variables into local variables
        adc_freq_actual = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        dec1_actual = model.vars.dec1_actual.value
        dec2_actual = model.vars.dec2_actual.value
        baudrate_actual = model.vars.rx_baud_rate_actual.value
        src2_actual = model.vars.src2_ratio_actual.value
        osr_actual = adc_freq_actual * src2_actual / (dec0_actual * dec1_actual * 8 * dec2_actual * baudrate_actual)
        # Load local variables back into model variables
        model.vars.oversampling_rate_actual.value = osr_actual

    # Method name: calc_phasedemod_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_phasedemod_reg(self, model):
        # This function writes the phase demod register
        # Load model variables into local variables
        length = model.vars.dsss_len.value
        modulation = model.vars.modulation_type.value
        demod_sel = model.vars.demod_select.value
        if modulation == model.vars.modulation_type.var_enum.OQPSK:
            if demod_sel == model.vars.demod_select.var_enum.COHERENT:
                phasedemod = 2
            else:
                phasedemod = 1
        elif modulation == model.vars.modulation_type.var_enum.BPSK or \
                modulation == model.vars.modulation_type.var_enum.DBPSK:
            if length > 0:
                phasedemod = 2
            else:
                phasedemod = 1
        else:
            phasedemod = 0
        # Load local variables back into model variables
        self._ip_reg_write(model, 'CTRL1_PHASEDEMOD', phasedemod)

    # Method name: calc_phscale_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_phscale_actual(self, model):
        phscale_reg = model.vars.MODEM_TRECPMDET_PHSCALE.value
        model.vars.phscale_actual.value = float(2 ** (phscale_reg))

    # Method name: calc_phscale_derate_factor
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_phscale_derate_factor(self, model):
        # This function calculates the derating factor for PHSCALE for TRECS PHYs with large freq offset tol
        # Always set to 1 on Ocelot for now
        phscale_derate_factor = 1
        # Write the model var
        model.vars.phscale_derate_factor.value = phscale_derate_factor

    # Method name: calc_phscale_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_phscale_reg(self, model):
        # Load model variables into local variables
        mi = model.vars.modulation_index.value
        remoden = model.vars.MODEM_PHDMODCTRL_REMODEN.value
        demod_sel = model.vars.demod_select.value
        osr = model.vars.oversampling_rate_actual.value
        phscale_derate_factor = model.vars.phscale_derate_factor.value
        if remoden:
            # if remodulation path is enabled freqgain block is handling the scaling
            phscale_reg = 0
        elif mi > 0.0:
            if demod_sel == model.vars.demod_select.var_enum.BCR:
                # phscale_reg = int(floor(log(8 * 4 * mi / osr, 2)))
                bcr_phscale_list = [0, 1, 2, 3]
                bcrksi3_list = []
                diff_from_opt_bcrksi3_list = []
                for bcr_phscale_val in bcr_phscale_list:
                    bcr_phscale_val_actual = float(2 ** (bcr_phscale_val))
                    ksi1_val = self.return_ksi1_calc(model, bcr_phscale_val_actual)
                    ksi2_val, ksi3_val, ksi3wb_val = self.return_ksi2_ksi3_calc(model, ksi1_val)
                    bcrksi3_list.append(ksi3wb_val)
                    diff_from_opt_bcrksi3_list.append(40 - ksi3wb_val)
                # : Determine lowest phscale value with bcrksi3 < 64
                phscale_reg = -1
                for diff_index in range(len(diff_from_opt_bcrksi3_list)):
                    if diff_from_opt_bcrksi3_list[diff_index] >= 0:
                        phscale_reg = bcr_phscale_list[diff_index]
                        break
                # : If fail, calculate following est osr disable case
                if phscale_reg == -1:
                    phscale_reg = int(floor(log(8 * 4 * mi / osr, 2)))
            else:
                # this scaling will bring the nominal soft decision as close to 64 as possible with a power of 2 scaling
                phscale_reg = int(round(log(2 * mi, 2)))
        else:
            phscale_reg = 0
        # Derate phscale per phscale_derate_factor (used to accomodate large freq offset tol)
        phscale_reg += int(round(log2(phscale_derate_factor)))
        # limit phscale_reg from 0 to 3
        phscale_reg = max(min(phscale_reg, 3), 0)
        self._ip_reg_write(model, 'TRECPMDET_PHSCALE', phscale_reg)

    # Method name: calc_preamble_detection_length
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_preamble_detection_length(self, model):
        # This method calculates a defualt value for preamble_detection_length
        preamble_length = model.vars.preamble_length.value
        directmode_rx = model.vars.directmode_rx.value
        if directmode_rx != model.vars.directmode_rx.var_enum.DISABLED:
            # No preamble is expected in direct mode, so any DSA configuration should bypass preamble search
            model.vars.preamble_detection_length.value = 0
        else:
            # Set the preamble detection length to the preamble length (TX) by default
            model.vars.preamble_detection_length.value = preamble_length

    # Method name: calc_prefiltcoeff_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_prefiltcoeff_reg(self, model):
        dsss0 = model.vars.MODEM_DSSS0_DSSS0.value
        modtype = model.vars.modulation_type.value
        demod_select = model.vars.demod_select.value
        if modtype == model.vars.modulation_type.var_enum.OQPSK and dsss0 != 0:
            dsss0_rotated = ((dsss0 << 1) | (dsss0 >> 31)) & 0xFFFFFFFF
            dsss0_rotated_conj = dsss0_rotated ^ 0x55555555
            prefilt = 2 ** 32 + (dsss0 ^ ~dsss0_rotated_conj)
        elif demod_select == model.vars.demod_select.var_enum.LONGRANGE:
            prefilt = 0x3C3C3C3C
        else:
            prefilt = 0
        self._ip_reg_write(model, 'PREFILTCOEFF_PREFILTCOEFF', prefilt)

    # Method name: calc_prefiltercoff_len
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_prefiltercoff_len(self, model):
        demod_select = model.vars.demod_select.value
        cplxcorr_enabled = model.vars.MODEM_CTRL6_CPLXCORREN.value
        dsss_len = model.vars.dsss_len_actual.value
        # : For coherent demod, set prefilter length to 4 symbols
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            prefilter_len_actual = dsss_len * 4
            # If complex correlation is enabled, max length is 64 (prefilter_len_reg = 1)
            if cplxcorr_enabled == 1:
                if prefilter_len_actual > 64:
                    prefilter_len_actual = 64
        else:  # : default value for all other demods
            prefilter_len_actual = 64
        # : convert actual length to register values
        prefilter_len_reg = int(round(prefilter_len_actual / 32.0 - 1.0))
        self._ip_reg_write(model, 'LONGRANGE1_PREFILTLEN', prefilter_len_reg)

    # Method name: calc_remoddwn_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_remoddwn_reg(self, model):
        osr = model.vars.oversampling_rate_actual.value
        # trecs_enabled = model.vars.trecs_enabled.value
        # if trecs_enabled and osr > 7:
        #     remoddwn = int(osr/4) - 1   # we know osr is a multiple of 4 if we're here
        # else:
        # We prefer to not use the slice and remod path so this shoudl always be 0
        remoddwn = 0
        self._ip_reg_write(model, 'PHDMODCTRL_REMODDWN', remoddwn)

    # Method name: calc_remoden_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_remoden_reg(self, model):
        osr = model.vars.oversampling_rate_actual.value
        dec2_actual = model.vars.dec2_actual.value
        trecs_enabled = model.vars.trecs_enabled.value
        # Current assumption is that we are going to use the REMOD path only for Viterbi/TRecS
        if trecs_enabled and (osr > 7 or dec2_actual > 1):
            reg = 1
        else:
            reg = 0
        self._ip_reg_write(model, 'PHDMODCTRL_REMODEN', reg)

    # Method name: calc_remodosr_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_remodosr_reg(self, model):
        osr = model.vars.oversampling_rate_actual.value
        trecs_enabled = model.vars.trecs_enabled.value
        if trecs_enabled:
            remodosr = int(round(osr)) - 1
        else:
            remodosr = 0
        self._ip_reg_write(model, 'PHDMODCTRL_REMODOSR', remodosr)

    # Method name: calc_resyncbaudtrans_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_resyncbaudtrans_reg(self, model):
        # This function writes the resyncbaudtrans register
        demod_select = model.vars.demod_select.value
        # : for coherent demod, disable otherwise the measured baudrate tolerance is effectively 0
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            self._ip_reg_write(model, 'CTRL5_RESYNCBAUDTRANS', 0)
        else:
            # Based on Series 1 findings, always set RESYNCBAUDTRANS for all other demods
            self._ip_reg_write(model, 'CTRL5_RESYNCBAUDTRANS', 1)

    # Method name: calc_resyncper_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_resyncper_actual(self, model):
        # This function calculates the actual resynchonization period based on the register value
        # Load model variables into local variables
        resyncper_actual = float(model.vars.MODEM_CTRL1_RESYNCPER.value)
        # Load local variables back into model variables
        model.vars.resyncper_actual.value = resyncper_actual

    # Method name: calc_resyncper_brcal_val
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_resyncper_brcal_val(self, model):
        # This function calculates the resynchronization and baud rate calibration values
        # Load model variables into local variables
        mod_type = model.vars.modulation_type.value
        osr = model.vars.oversampling_rate_actual.value
        symbols_in_timing_window = model.vars.symbols_in_timing_window.value
        baudrate_tol_ppm = model.vars.baudrate_tol_ppm.value
        syncword_length = model.vars.syncword_length.value
        if symbols_in_timing_window > 0:
            timing_wind_size = symbols_in_timing_window
        else:
            timing_wind_size = syncword_length
        # Estimate the baudrate tol with resyncper=2
        estimated_baudrate_tol_ppm = int(
            1.0 / (2 * timing_wind_size * osr) * 1e6 / 2)  # Divide by 2 is to be conservative
        # Use a resynchronization period of 2 if we don't need much baudrate tolerance, otherwise use 1
        if estimated_baudrate_tol_ppm >= baudrate_tol_ppm:
            resyncper = 2
        else:
            resyncper = 1
        # Baudrate calibration does not work well with the Legacy demod, so disable
        brcalavg = 0
        brcalen = 0
        # Load local variables back into model variables
        model.vars.brcalavg.value = brcalavg
        model.vars.brcalen.value = brcalen
        model.vars.timing_resync_period.value = resyncper

    # Method name: calc_rsyncper_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_rsyncper_reg(self, model):
        # This function writes the resyncper register
        # Load model variables into local variables
        timing_resync_period = model.vars.timing_resync_period.value
        # Write register
        self._ip_reg_write(model, 'CTRL1_RESYNCPER', timing_resync_period)

    # Method name: calc_rx_deviation_scaled
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_rx_deviation_scaled(self, model):
        # This function calculates the scaled RX deviation
        # Load model variables into local variables
        deviation = model.vars.deviation.value
        freq_gain_actual = model.vars.freq_gain_actual.value
        demod_rate_actual = model.vars.demod_rate_actual.value
        rx_deviation_scaled = float(256 * deviation * freq_gain_actual / demod_rate_actual)
        # Load local variables back into model variables
        model.vars.rx_deviation_scaled.value = rx_deviation_scaled

    # Method name: calc_rx_duty_cycle_vars
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_rx_duty_cycle_vars(self, model):
        model.vars.rxdc_power_save_time_us.value = 0
        model.vars.rxdc_power_save_mode.value = model.vars.rxdc_power_save_mode.var_enum.DISABLED
        model.vars.rxdc_on_time_us_actual.value = 0
        model.vars.rxdc_off_time_us_actual.value = 0

    # Method name: calc_rx_restart_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_rx_restart_reg(self, model):
        """
        Calculate collision restart control registers.
        Args:
            model:
        Returns:
        """
        antdivmode = model.vars.antdivmode.value
        fltrsten = 0
        antswrstfltdis = 1
        rxrestartb4predet = 0
        rxrestartmatap = 1
        rxrestartmalatchsel = 0
        rxrestartmacompensel = 2
        rxrestartmathreshold = 6
        rxrestartuponmarssi = 0
        # The following need to be set the same regardless of antdiv enable
        self._ip_reg_write(model, 'RXRESTART_FLTRSTEN', fltrsten)
        self._ip_reg_write(model, 'RXRESTART_ANTSWRSTFLTTDIS', antswrstfltdis)
        if antdivmode == model.vars.antdivmode.var_enum.DISABLE or \
                antdivmode == model.vars.antdivmode.var_enum.ANTENNA1:
            self._reg_do_not_care(model.vars.MODEM_RXRESTART_RXRESTARTB4PREDET)
            self._reg_do_not_care(model.vars.MODEM_RXRESTART_RXRESTARTMATAP)
            self._reg_do_not_care(model.vars.MODEM_RXRESTART_RXRESTARTMALATCHSEL)
            self._reg_do_not_care(model.vars.MODEM_RXRESTART_RXRESTARTMACOMPENSEL)
            self._reg_do_not_care(model.vars.MODEM_RXRESTART_RXRESTARTMATHRESHOLD)
            self._reg_do_not_care(model.vars.MODEM_RXRESTART_RXRESTARTUPONMARSSI)
        else:
            self._ip_reg_write(model, 'RXRESTART_RXRESTARTB4PREDET', rxrestartb4predet)
            self._ip_reg_write(model, 'RXRESTART_RXRESTARTMATAP', rxrestartmatap)
            self._ip_reg_write(model, 'RXRESTART_RXRESTARTMALATCHSEL', rxrestartmalatchsel)
            self._ip_reg_write(model, 'RXRESTART_RXRESTARTMACOMPENSEL', rxrestartmacompensel)
            self._ip_reg_write(model, 'RXRESTART_RXRESTARTMATHRESHOLD', rxrestartmathreshold)
            self._ip_reg_write(model, 'RXRESTART_RXRESTARTUPONMARSSI', rxrestartuponmarssi)

    # Method name: calc_rx_tx_ppm
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_rx_tx_ppm(self, model):
        # This function calculates the default RX and TX HFXO tolerance in PPM
        # Set defaults
        rx_ppm = 0
        tx_ppm = 0
        # Load local variables back into model variables
        model.vars.rx_xtal_error_ppm.value = rx_ppm
        model.vars.tx_xtal_error_ppm.value = tx_ppm

    # Method name: calc_rxbr
    # Defined in: bobcat\calculators\calc_demodulator.py
    def calc_rxbr(self, model):
        # This function calculates the receive baudrate settings
        # based on actual dec0,dec1,dec2,src2, and desired baudrate
        # then baudrate_actual will be calculated from rxbrfrac_actual
        # Load model variables into local variables
        target_osr = model.vars.target_osr.value  # We don't know the actual OSR yet, because that has to be based on the final baudrate
        targetmax_osr = model.vars.targetmax_osr.value
        targetmin_osr = model.vars.targetmin_osr.value
        adc_freq_actual = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        dec1_actual = model.vars.dec1_actual.value
        dec2_actual = model.vars.dec2_actual.value
        src2_actual = model.vars.src2_ratio_actual.value
        baudrate = model.vars.baudrate.value
        denlist = range(2, 31)
        error_limit = 0.5
        # not using target_osr, because in some cases (e.g. BCR with fractional OSR)
        # the OSR w.r.t desired baudrate and acutal decimators varies from the target
        # allowing 0.01% variation from targetmin_osr and targetmax_osr for range check
        # because this osr calculation uses src2_actual, which has some small quantization noise
        osr = float(adc_freq_actual * src2_actual) / float(dec0_actual * dec1_actual * 8 * dec2_actual * baudrate)
        osr_limit_min = targetmin_osr * (1 - 0.0001)
        osr_limit_max = targetmax_osr * (1 + 0.0001)
        if (osr >= osr_limit_min) and (osr <= osr_limit_max):
            # search for best fraction
            rxbrint = int(floor(osr / 2))
            frac = (osr / 2) - float(rxbrint)
            numlist = range(0, 31)
            min_error = 100
            for den in denlist:
                for num in numlist:
                    frac_error = abs(float(num) / float(den) - frac)
                    if (frac_error < min_error):
                        min_error = frac_error
                        best_den = den
                        best_num = num
            # calculate error in percent of baudrate, and require < 0.5% error
            # matlab simulation sweeping osr with 0.01% step size, showed the max osr relative error = 0.4%
            # using num=0:31, den=2:31
            error_percent = 100 * abs(2 * (rxbrint + float(best_num) / float(best_den)) - osr) / osr
            if error_percent < error_limit:
                rxbrnum = best_num
                rxbrden = best_den
                if (rxbrnum == rxbrden):
                    rxbrden = 2
                    rxbrnum = 0
                    rxbrint = rxbrint + 1
                elif rxbrnum > rxbrden:
                    raise CalculationException('ERROR: num > den in calc_rxbr()')
            else:
                # print("adc_freq = %f" % adc_freq_actual)
                # print("baudrate = %f" % baudrate)
                # print("target_osr = %f" % target_osr)
                # print("adjust_osr = %f" % osr)
                # print("rxbrint = %d" % rxbrint)
                # print("best_num = %d" % best_num)
                # print("best_den = %d" % best_den)
                # print(model.vars.demod_select.value)
                raise CalculationException('ERROR: baudrate error > 0.5% in calc_rxbr()')
        else:
            # print("adc_freq = %f" % adc_freq_actual)
            # print("baudrate = %f" % baudrate)
            # print("target_osr = %f" % target_osr)
            # print("adjust_osr = %f" % osr)
            # print("targetmin_osr = %f" % targetmin_osr)
            # print("targetmax_osr = %f" % targetmax_osr)
            # print(str(model.vars.demod_select.value).split(".")[-1])
            raise CalculationException('ERROR: OSR out of range in calc_rxbr()')
        # Load local variables back into model variables
        model.vars.rxbrint.value = rxbrint
        model.vars.rxbrnum.value = rxbrnum
        model.vars.rxbrden.value = rxbrden

    # Method name: calc_rxbr_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_rxbr_actual(self, model):
        # This function shows the actual rxbr values contained in the registers
        # Load model variables into local variables
        rxbrint_actual = model.vars.MODEM_RXBR_RXBRINT.value
        rxbrnum_actual = model.vars.MODEM_RXBR_RXBRNUM.value
        rxbrden_actual = model.vars.MODEM_RXBR_RXBRDEN.value
        # Calculate the rxbr fraction
        rxbrfrac_actual = float(rxbrint_actual + float(rxbrnum_actual) / rxbrden_actual)
        # Load local variables back into model variables
        model.vars.rxbrint_actual.value = rxbrint_actual
        model.vars.rxbrnum_actual.value = rxbrnum_actual
        model.vars.rxbrden_actual.value = rxbrden_actual
        model.vars.rxbrfrac_actual.value = rxbrfrac_actual

    # Method name: calc_rxbr_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_rxbr_reg(self, model):
        # This function writes the rxbr registers
        # Load model variables into local variables
        rxbrint = model.vars.rxbrint.value
        rxbrnum = model.vars.rxbrnum.value
        rxbrden = model.vars.rxbrden.value
        adc_freq_actual = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        dec1_actual = model.vars.dec1_actual.value
        dec2_actual = model.vars.dec2_actual.value
        baudrate = model.vars.baudrate.value
        src2_actual = model.vars.src2_ratio_actual.value
        trecs_enabled = model.vars.trecs_enabled.value
        osr = adc_freq_actual * src2_actual / (dec0_actual * dec1_actual * 8 * dec2_actual * baudrate)
        if trecs_enabled and osr >= 8:
            rxbrint = 0
            rxbrden = 2
            rxbrnum = 1
        # Write registers
        self._reg_sat_write(model.vars.MODEM_RXBR_RXBRINT, rxbrint)
        self._reg_sat_write(model.vars.MODEM_RXBR_RXBRNUM, rxbrnum)
        self._reg_sat_write(model.vars.MODEM_RXBR_RXBRDEN, rxbrden)

    # Method name: calc_softd_reg
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_softd_reg(self, model):
        trecs_used = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        fec_enabled = model.vars.fec_enabled.value
        fec_en = model.vars.fec_en.value  # FEC configuration
        is_ble_longrange = model.vars.MODEM_LONGRANGE_LRBLE.value
        # https://jira.silabs.com/browse/MCUW_RADIO_CFG-2587
        # For the most PHYs, FEC is not selected in PHY's definition. So, TRECSCFG_SOFTD = 0 is as the default.
        # and hardcode to Viterbi decoder in FRC. So, we set TRECSCFG_SOFTD = 1 to get better performance.
        if not (is_ble_longrange) and (trecs_used and (fec_enabled and fec_en ==model.vars.fec_en.var_enum.FEC_154G_NRNSC_INTERLEAVING)):
            self._ip_reg_write(model, 'TRECSCFG_SOFTD', 1)
        else:
            self._ip_reg_write(model, 'TRECSCFG_SOFTD', 0)

    # Method name: calc_spare_regs
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_spare_regs(self, model):
        pass

    # Method name: calc_syncacqwin_actual
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_syncacqwin_actual(self, model):
        """ set syc word acquisition window for TRECS basd on register value
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        model.vars.syncacqwin_actual.value = (model.vars.MODEM_REALTIMCFE_SYNCACQWIN.value + 1)

    # Method name: calc_syncbits_actual
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_syncbits_actual(self, model):
        syncword_bits = model.vars.syncword_length.value  ##fix me
        model.vars.syncbits_actual.value = syncword_bits

    # Method name: calc_target_bandwidth
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_target_bandwidth(self, model):
        # This function calculates the target bandwidth in case the user didn't enter one
        # This is the acquisition bandwidth
        # Load model variables into local variables
        mod_type = model.vars.modulation_type.value
        bw_carson = model.vars.bandwidth_carson_hz.value
        baudrate = model.vars.baudrate.value
        freq_offset_hz = model.vars.freq_offset_hz.value
        # Calculate bw_demod and bw_acq
        # bw_demod is the target demod bandwidth before adding frequency shift
        # bw_acq combines bw_demod and frequency shift
        if (mod_type == model.vars.modulation_type.var_enum.FSK2) or \
                (mod_type == model.vars.modulation_type.var_enum.MSK):
            modulation_index = model.vars.modulation_index.value
            shaping_filter = model.vars.shaping_filter.value
            shaping_filter_param = model.vars.shaping_filter_param.value
            alpha = self.get_alpha(model, modulation_index, shaping_filter, shaping_filter_param)
            bw_acq = self.get_target_2fsk_bandwidth(bw_carson, freq_offset_hz, alpha)
        elif (mod_type == model.vars.modulation_type.var_enum.FSK4):
            bw_acq = bw_carson + 2.0 * freq_offset_hz
        else:
            # Default values for other modulation types
            if (mod_type == model.vars.modulation_type.var_enum.OOK) or \
                    (mod_type == model.vars.modulation_type.var_enum.ASK):
                bw_modulation = baudrate * 5.0
                if (model.vars.bandwidth_hz._value_forced == None):
                    print("  WARNING:  OOKASK bandwidth_hz has not been optimized")
            elif (mod_type == model.vars.modulation_type.var_enum.OQPSK):
                bw_modulation = baudrate * 1.25
            else:
                bw_modulation = baudrate * 1.0
            bw_acq = bw_modulation + 2.0 * freq_offset_hz
        # Set max limit on bandwidth_hz
        bw_acq = min(bw_acq, 2.5e6)
        if model.vars.bandwidth_hz.value_forced:
            if model.vars.bandwidth_hz.value > 1.2 * bw_acq:
                LogMgr.Warning("WARNING: Programmed acquisition channel bandwidth is much higher than calculated")
        # Load local variables back into model variables
        model.vars.bandwidth_hz.value = int(bw_acq)

    # Method name: calc_target_demod_bandwidth
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_target_demod_bandwidth(self, model):
        demod_select = model.vars.demod_select.value
        baudrate = model.vars.baudrate.value
        mod_type = model.vars.modulation_type.value
        bw_carson = model.vars.bandwidth_carson_hz.value
        harddecision = model.vars.MODEM_VITERBIDEMOD_HARDDECISION.value
        baudrate = model.vars.baudrate.value
        trecs_enabled = model.vars.trecs_enabled.value
        if demod_select == model.vars.demod_select.var_enum.ENHANCED_DSSS:
            model.vars.demod_bandwidth_hz.value = int(baudrate * 0.9)
        else:
            if (mod_type == model.vars.modulation_type.var_enum.FSK2) or \
                    (mod_type == model.vars.modulation_type.var_enum.MSK):
                if trecs_enabled and (harddecision == 0):
                    bw_demod = baudrate * 1.1
                else:
                    bw_demod = bw_carson

            elif (mod_type == model.vars.modulation_type.var_enum.FSK4):
                bw_demod = bw_carson

            else:
                # Default values for other modulation types
                if (mod_type == model.vars.modulation_type.var_enum.OOK) or \
                        (mod_type == model.vars.modulation_type.var_enum.ASK):
                    bw_demod = baudrate * 5.0
                    if (model.vars.bandwidth_hz._value_forced == None):
                        print("  WARNING:  OOKASK bandwidth_hz has not been optimized")
                elif (mod_type == model.vars.modulation_type.var_enum.OQPSK):
                    bw_demod = baudrate * 1.25
                else:
                    bw_demod = baudrate * 1.0

            # Load local variables back into model variables
            model.vars.demod_bandwidth_hz.value = int(bw_demod)

    # Method name: calc_trecs_enabled
    # Defined in: bobcat\calculators\calc_demodulator.py
    def calc_trecs_enabled(self, model):
        demod_select = model.vars.demod_select.value
        concurrent_ble = model.vars.MODEM_COCURRMODE_CONCURRENT.value
        if demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
            trecs_enabled = True
        elif concurrent_ble:
            trecs_enabled = True
        else:
            trecs_enabled = False
        model.vars.trecs_enabled.value = trecs_enabled

    # Method name: calc_trecsosr_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_trecsosr_reg(self, model):
        # This function writes the TRECSOSR register
        # Load model variables into local variables
        demod_select = model.vars.demod_select.value
        osr_actual = model.vars.oversampling_rate_actual.value
        remoddwn = model.vars.MODEM_PHDMODCTRL_REMODDWN.value + 1
        trecs_enabled = model.vars.trecs_enabled.value
        if trecs_enabled:
            trecsosr_reg = osr_actual / remoddwn
        else:
            trecsosr_reg = 0
        # Write the register
        self._ip_reg_write(model, 'TRECSCFG_TRECSOSR', int(round(trecsosr_reg)))

    # Method name: gen_frequency_signal
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def gen_frequency_signal(self, x, sf, cf, sfosr, model):
        # get parameters
        deviation = model.vars.deviation.value
        baudrate = model.vars.baudrate.value
        demodosr = round(model.vars.oversampling_rate_actual.value)
        src2 = model.vars.FEFILT_SRCCHF_SRCRATIO2.value #todo: create a model variable to share this
        datafilter = model.vars.MODEM_CTRL2_DATAFILTER.value
        remoden = model.vars.MODEM_PHDMODCTRL_REMODEN.value
        remodoutsel = model.vars.MODEM_PHDMODCTRL_REMODOUTSEL.value
        demod_select = model.vars.demod_select.value
        dec2 = model.vars.dec2_actual.value
        remodpath = True if remoden or demod_select == model.vars.demod_select.var_enum.BCR else False
        if demod_select == model.vars.demod_select.var_enum.BCR:
            rawndec = model.vars.MODEM_BCRDEMODOOK_RAWNDEC.value  # Moved inside BCR statement to allow inheritance
            dec2 = 2 ** rawndec
        # scale shaping filter to desired amplitude OSR = 8
        sf = sf / np.sum(sf) * sfosr
        # pulse shape OSR = 8
        y = sp.lfilter(sf, 1, x)
        # apply deviation OSR = 8
        z = y * deviation
        # integrate to get phase after scaling by sampling rate at TX OSR = 8
        t = np.cumsum(z / (baudrate * sfosr))
        # modulate at baseband OSR = 8
        u = np.exp(1j * 2 * pi * t)
        # resample at channel filter rate (e.g. sfosr -> osr) OSR = chflt_osr * src2
        # FIXME: handle other remod paths here if we end up using them
        if remodpath:
            osr = demodosr * dec2
        else:
            osr = demodosr
        u2 = resample_poly_cached(u, round(osr * src2 / 32), round(sfosr * self.SRC2DENUM / 32))
        # channel filter OSR = chflt_osr * src2
        v = sp.lfilter(cf, 1, u2)
        # src2 - resample to target OSR rate OSR = target_osr * dec2
        v2 = resample_poly_cached(v, round(self.SRC2DENUM / 32), round(src2 / 32))  # updated to speed up the calculation
        # CORDIC OSR = target_osr * dec2
        a = np.unwrap(np.angle(v2))
        # downsample by dec2 to get to target_osr if remod enabled
        if remodpath:  # and remodoutsel == 1:
            # differentiate phase to frequency OSR = target_osr * dec2
            f1 = a[1:] - a[0:-1]
            # f = sp.resample_poly(f1, 1, dec2)
            # when downsampling pick the best phase that results in max eye opening as we are going to feed the samples
            # from here to the datafilter. Low value samples will bring the average soft decision to a lower value.
            best_min = 0
            for phase in range(dec2):
                f2 = resample_poly_cached(f1[round(len(f1) / 4) + phase:], 1, dec2)
                min_val = min(abs(f2[3:-3]))
                if min_val >= best_min:
                    best_min = min_val
                    f = f2
        else:
            # differentiate phase to frequency OSR = target_osr * dec2
            f = a[osr:] - a[0:-osr]
        # optional decimation and filtering for remod paths
        if demod_select == model.vars.demod_select.var_enum.BCR:
            rawgain = model.vars.MODEM_BCRDEMODOOK_RAWGAIN.value  # Moved inside BCR statement to allow inheritance
            rawfltsel = model.vars.MODEM_BCRDEMODCTRL_RAWFLTSEL.value #todo: implement ip_read
            ma1 = self.get_ma1_filter(rawgain)
            g1 = sp.lfilter(ma1, 1, f)
            ma2 = self.get_ma2_filter(rawfltsel)
            g = sp.lfilter(ma2, 1, g1)
        elif remoden and (remodoutsel == 0 or remodoutsel == 1):
            df = self.get_data_filter(datafilter)
            g = sp.lfilter(df, 1, f)
        else:
            g = f
        # return frequency signal
        return g

    # Method name: get_alpha
    # Defined in: ocelot\calculators\calc_demodulator.py
    def get_alpha(self, model, modulation_index, shaping_filter, shaping_filter_param):
        # Bandwidth adjustment based on mi and bt
        # the thresholds were derived based simulating bandwidth of modulated signal with 98% of the energy
        mi = modulation_index
        sf = shaping_filter
        if sf == model.vars.shaping_filter.var_enum.NONE.value:
            if mi < 0.75:
                alpha = 0.1
            elif mi < 0.85:
                alpha = 0
            elif mi < 1.5:
                alpha = -0.1
            else:
                alpha = -0.2
        elif sf == model.vars.shaping_filter.var_enum.Gaussian.value:
            bt = shaping_filter_param  # BT might not be defined if not Gaussian shaping so read it here
            if bt < 0.75:
                if mi < 0.95:
                    alpha = 0.2
                elif mi < 1.5:
                    alpha = 0.1
                elif mi < 6.5:
                    alpha = 0
                else:
                    alpha = -0.1
            elif bt < 1.5:
                if mi < 0.85:
                    alpha = 0.1
                elif mi < 1.5:
                    alpha = 0
                else:
                    alpha = -0.1
            elif bt < 2.5:
                if mi < 0.75:
                    alpha = 0.1
                elif mi < 0.85:
                    alpha = 0
                else:
                    alpha = -0.1
        else:
            # for non Gaussian shaping keeping the original alpha calculation
            if (mi < 1.0):
                alpha = 0.2
            elif (mi == 1.0):
                alpha = 0.1
            else:
                alpha = 0
        return alpha

    # Method name: get_data_filter
    # Defined in: ocelot\calculators\calc_demodulator.py
    def get_data_filter(self, datafilter):
        if datafilter == 0:
            coef = [1]
        elif datafilter == 1:
            coef = [1 / 4, 2 / 4, 1 / 4]
        elif datafilter == 2:
            coef = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
        elif datafilter == 3:
            coef = [1 / 8, 2 / 8, 2 / 8, 2 / 8, 1 / 8]
        elif datafilter == 4:
            coef = [1 / 8, 1 / 8, 2 / 8, 2 / 8, 1 / 8, 1 / 8]
        elif datafilter == 5:
            coef = [1 / 8, 1 / 8, 1 / 8, 2 / 8, 1 / 8, 1 / 8, 1 / 8]
        elif datafilter == 6:
            coef = [1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8]
        elif datafilter == 7:
            coef = [1 / 16, 2 / 16, 2 / 16, 2 / 16, 2 / 16, 2 / 16, 2 / 16, 2 / 16, 1 / 16]
        else:
            raise CalculationException('ERROR: Invalid setting for datafilter in get_datafilter in calc_demodulator.py')
        return coef

    # Method name: get_limits
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def get_limits(self, demod_select, withremod, relaxsrc2, model):
        bandwidth = model.vars.bandwidth_hz.value #from calc_target_bandwidth

        baudrate = model.vars.baudrate.value #We don't know the actual bandrate yet
        modtype = model.vars.modulation_type.value
        mi = model.vars.modulation_index.value
        hadm_enable = (model.vars.hadm_enable.value == model.vars.hadm_enable.var_enum.ENABLED)
        min_chfilt_osr = None
        max_chfilt_osr = None
        osr_list = None
        if demod_select == model.vars.demod_select.var_enum.BTC:
            # : TODO Using same settings as Legacy demod for now.
            osr_list = [8]
            min_osr = 8
            max_osr = 8
            min_src2 = 0.8
            max_src2 = 1.65 if relaxsrc2 else 1.2
            min_dec2 = 1
            max_dec2 = 1
            min_bwsel = 0.1
            target_bwsel = 0.4
            max_bwsel = 0.4
            min_chfilt_osr = None
            max_chfilt_osr = None
        elif demod_select == model.vars.demod_select.var_enum.ENHANCED_DSSS or \
                demod_select == model.vars.demod_select.var_enum.HDT:
            osr_list = [4]
            min_osr = 4
            max_osr = 4
            min_src2 = 0.8
            max_src2 = 1.2
            min_dec2 = 1
            max_dec2 = 1
            min_bwsel = 0.15
            target_bwsel = 0.4
            max_bwsel = 0.4
            min_chfilt_osr = None
            max_chfilt_osr = None
        # Define constraints for osr, src2, dec2
        elif demod_select == model.vars.demod_select.var_enum.BCR:
            # FIXME:  osr_list and resulting target osr are really chfilt_osr, pro2 calculator defines target_osr
            #       This doesn't cause an error but is confusing.
            osr_est = int(ceil(2 * float(bandwidth) / baudrate))

            min_osr = 8
            max_osr = 127
            min_chfilt_osr = 8
            if (modtype == model.vars.modulation_type.var_enum.OOK) or \
                    (modtype == model.vars.modulation_type.var_enum.ASK):
                max_chfilt_osr = 16256  #127*max_bcr_dec = 127*128
                osr_list = range(12, max_chfilt_osr)
            else:
                max_chfilt_osr = 127
                osr_list = [osr_est]

            min_src2 = 1.0
            max_src2 = 1.0
            min_dec2 = 1
            max_dec2 = 1
            min_bwsel = 0.2
            target_bwsel = 0.4
            max_bwsel = 0.4
        elif demod_select == model.vars.demod_select.var_enum.LEGACY:
            if (modtype == model.vars.modulation_type.var_enum.FSK2 or \
                  modtype == model.vars.modulation_type.var_enum.FSK4 or \
                  modtype == model.vars.modulation_type.var_enum.MSK) and (mi<1):
                # >=7 is better for sensitivity and frequency offset
                # cost (sens degrade) increases with decreasing osr 6,5,4
                osr_list = [7, 8, 9, 6, 5, 4]
                min_osr = 4
            else:
                osr_list = [5, 7, 6, 4, 8, 9]
                min_osr = 4
            max_osr = 9
            min_src2 = 0.8
            max_src2 = 1.65 if relaxsrc2 else 1.2
            min_dec2 = 1
            max_dec2 = 64
            min_bwsel = 0.2
            target_bwsel = 0.4
            max_bwsel = 0.4
        elif demod_select == model.vars.demod_select.var_enum.COHERENT:
            osr_list = [5]
            min_osr = 5
            max_osr = 5
            min_src2 = 0.8
            min_dec2 = 1
            max_dec2 = 1
            min_bwsel = 0.2
            target_bwsel = 0.4
            max_bwsel = 0.4
            max_src2 = 1.65 if relaxsrc2 else 1.2
        elif demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:

            min_bwsel = 0.2
            target_bwsel = 0.4
            max_bwsel = 0.4

            if hadm_enable == False:
                if relaxsrc2 == True:
                    min_src2 = 0.55
                    max_src2 = 1.3
                    min_bwsel = 0.15
                else:
                    min_src2 = 0.8
                    max_src2 = 1.0
            else: #HADM
                if relaxsrc2 == True:
                    min_src2 = 0.8
                    max_src2 = 1.0
                else: #Try to disable SRC2 (best performance)
                    min_src2 = 0.99
                    max_src2 = 1.0

            if withremod == True:
                min_dec2 = 1
                max_dec2 = 64
                min_osr = 4
                max_osr = 32
                osr_list = [4, 5, 6, 7]
            elif mi > 2.5: #FIXME: arbitrary threshold here - for zwave 9.6kbps with mi=2.1 we prefer not to use int/diff path but at some point we will have to
                min_dec2 = 1
                max_dec2 = 64
                min_osr = 4
                max_osr = 7
                osr_list = [4, 5, 6, 7]
            else:
                # Standard TRECs, no DEC2 or remod path
                min_dec2 = 1
                max_dec2 = 1
                min_osr = 4
                max_osr = 7
                osr_list = [4, 5, 6, 7]
        elif demod_select == model.vars.demod_select.var_enum.LONGRANGE:
            min_dec2 = 1
            max_dec2 = 1
            min_osr = 4
            max_osr = 4
            osr_list = [4]
            min_src2 = 0.8
            max_src2 = 1.2
            min_bwsel = 0.2
            target_bwsel = 0.3
            max_bwsel = 0.3
        else:
            raise CalculationException('ERROR: invalid demod_select in return_osr_dec0_dec1()')

        # save to use in other functions
        model.vars.min_bwsel.value = min_bwsel  # min value for normalized channel filter bandwidth
        model.vars.max_bwsel.value = max_bwsel  # max value for normalized channel filter bandwidth
        model.vars.min_src2.value = min_src2  # min value for SRC2
        model.vars.max_src2.value = max_src2  # max value for SRC2
        model.vars.max_dec2.value = max_dec2
        model.vars.min_dec2.value = min_dec2
        return min_bwsel, max_bwsel, min_chfilt_osr, max_chfilt_osr, min_src2, max_src2, min_dec2, max_dec2, min_osr, max_osr, target_bwsel, osr_list

    # Method name: get_ma1_filter
    # Defined in: ocelot\calculators\calc_demodulator.py
    def get_ma1_filter(self, rawgain):
        if rawgain == 0:
            df = [4]
        elif rawgain == 1:
            df = [2, 2]
        elif rawgain == 2:
            df = [1, 2, 1]
        else:
            df = [1 / 2, 3 / 2, 3 / 2, 1 / 2]
        return df

    # Method name: get_ma2_filter
    # Defined in: ocelot\calculators\calc_demodulator.py
    def get_ma2_filter(self, rawfltsel):
        if rawfltsel == 0:
            df = [1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4]
        elif rawfltsel == 1:
            df = [1 / 2, 1 / 2, 1 / 2, 1 / 2]
        else:
            df = [1]
        return df

    # Method name: get_target_2fsk_bandwidth
    # Defined in: ocelot\calculators\calc_demodulator.py
    def get_target_2fsk_bandwidth(self, bw_carson, freq_offset_hz, alpha):
        bw_acq = bw_carson + 2 * max(0.0, freq_offset_hz - alpha * bw_carson)
        return bw_acq

    def return_dec0_from_reg(self, reg):
        """convert register value to decimation value
        Args:
            reg (int) : register value to decimation value
        """
        if reg == 0:
            dec0 = 3
        elif reg == 1 or reg == 2:
            dec0 = 4
        elif reg == 3 or reg == 4:
            dec0 = 8
        elif reg == 5:
            dec0 = 5
        return dec0

    # Method name: return_dec0_list
    # Defined in: ocelot\calculators\calc_demodulator.py
    def return_dec0_list(self,if_frequency_hz,adc_freq):
        # The purpose of this function is determine the prioritized dec0 list from decimation options 3,4,8,5
        # Rules:
        # 1) DEC0=8 was only designed for adc_freq <= 40MHz
        # 2) DEC0 anti-aliasing rejection >60dB for DEC0=8 and 4

        first_null_d8 = float(adc_freq) / (8 * 8)
        ratio_d8 = float(if_frequency_hz) / first_null_d8

        first_null_d4 = float(adc_freq) / (8 * 4)
        ratio_d4 = float(if_frequency_hz) / first_null_d4

        # fixme: Need to review algorithm for selecting D0
        # 15.4 Enhanced, HDT are picking D0=5 for better bwsel > 0.2
        # but D0=5 will pull in image, potentially degrading ACI

        if (ratio_d8 < 0.248) and (adc_freq <= 40e6):
            # 0.248 = (.125-.094)/.125 corresponds to >60dB attenuation on d0=8 response
            dec0_priority_list = [8,4,3,5]
        elif ratio_d4 < 0.27:
            # 0.27 = (.25-0.1825)/.25 corresponds to >60dB attenuation on d0=4 response
            dec0_priority_list = [4,3,5]
        else:
            dec0_priority_list = [3,4,5]

        return dec0_priority_list

    # Method name: return_ksi1_calc
    # Defined in: ocelot\calculators\calc_demodulator.py
    def return_ksi1_calc(self, model, phscale):
        # Load model variables into local variables
        demod_sel = model.vars.demod_select.value
        modtype = model.vars.modulation_type.value
        trecs_enabled = model.vars.trecs_enabled.value
        remoden = model.vars.MODEM_PHDMODCTRL_REMODEN.value
        freq_gain_actual = model.vars.freq_gain_actual.value
        osr = model.vars.oversampling_rate_actual.value
        mi_to_use = model.vars.modulation_index_for_ksi.value
        # when remod is enabled scaling is controlled by freqgain and phscale is currently set to 1
        if remoden:
            gain = freq_gain_actual / phscale / osr
        elif demod_sel == model.vars.demod_select.var_enum.BCR:
            gain = 8 / (phscale * osr)
        else:
            gain = 1 / phscale
        # calculate ksi values for Viterbi demod only
        # if the gain is set correctly this should give us nominal soft decisions of 64 for regular case
        # in case of remod we actually use the legacy demod's gain which sets the deviation + freq offset to 128
        if ((trecs_enabled or demod_sel == model.vars.demod_select.var_enum.BCR) and
                (modtype == model.vars.modulation_type.var_enum.FSK2 or
                 modtype == model.vars.modulation_type.var_enum.FSK4 or
                 modtype == model.vars.modulation_type.var_enum.MSK)):
            if demod_sel == model.vars.demod_select.var_enum.BCR:
                saturation_value = 63
            else:
                saturation_value = 127
            ksi1 = int(round(saturation_value * mi_to_use * gain))
        else:
            ksi1 = 0
        return ksi1

    # Method name: return_osr_dec0_dec1
    # Defined in: rainier\calculators\calc_demodulator.py
    def return_osr_dec0_dec1(self, model, demod_select, withremod=False, relaxsrc2=False, quitatfirstvalid=True):
        # Load model variables into local variables
        bandwidth = model.vars.bandwidth_hz.value  # from calc_target_bandwidth
        adc_freq = model.vars.adc_freq_actual.value
        baudrate = model.vars.baudrate.value  # We don't know the actual bandrate yet
        modtype = model.vars.modulation_type.value
        mi = model.vars.modulation_index.value
        if_frequency_hz = model.vars.if_frequency_hz.value
        etsi_cat1_compatability = model.vars.etsi_cat1_compatible.value
        bw_var = model.vars.bandwidth_tol.value
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        # set limits based on selected demod
        [min_bwsel, max_bwsel, min_chfilt_osr, max_chfilt_osr, min_src2, max_src2, min_dec2, \
         max_dec2, min_osr, max_osr, target_bwsel, osr_list] = self.get_limits(demod_select, withremod, relaxsrc2,
                                                                               model)
        # read from advanced variable
        if (model.vars.target_bwsel._value_forced != None):
            target_bwsel = model.vars.target_bwsel._value_forced
        # initialize output
        best_bwsel_error = 1e9
        best_osr = 0
        best_dec0 = 0
        best_dec1 = 0
        # Setup for osr loop
        # osr_list is a prioritized list, where first value with valid config will be returned
        if (model.vars.target_osr._value_forced != None):
            osr_forced = model.vars.target_osr._value_forced
            osr_list = [osr_forced]
        # Setup for dec0 loop
        # dec0_list is a prioritized list, where ties in best bwsel go to earlier value in list
        dec0_list = self.return_dec0_list(if_frequency_hz, adc_freq)
        # Search values of osr, dec0, dec1 to find solution
        # Exit on first osr with valid dec0 and dec1
        for osr in osr_list:
            for dec0 in dec0_list:
                # define integer range for dec1
                min_dec1 = int(max(1, ceil(float(adc_freq) * min_bwsel / (8 * dec0 * bandwidth * (1 + bw_var)))))
                max_dec1 = int(min(11500, floor(float(adc_freq) * max_bwsel / (8 * dec0 * bandwidth * (1 - bw_var)))))
                if min_dec1 <= max_dec1:
                    # Order list from highest to lowest, bwsel from highest to lowest
                    dec1_list = range(max_dec1, min_dec1 - 1, -1)
                else:
                    # No solution
                    continue
                for dec1 in dec1_list:
                    # check configuration does trigger IPMCUSRW-876 channel filter issue when input sample rate
                    # is too fast relative to the processing clock cycles needed
                    # if not self._channel_filter_clocks_valid(model, dec0, dec1):
                    #     continue
                    # calculated dec2 range
                    if demod_select == model.vars.demod_select.var_enum.BCR:
                        calc_min_dec2 = 1
                        calc_max_dec2 = 1
                        chfilt_osr_actual = float(adc_freq) / (8 * dec0 * dec1 * baudrate)
                        if (modtype == model.vars.modulation_type.var_enum.OOK) or \
                                (modtype == model.vars.modulation_type.var_enum.ASK):
                            if chfilt_osr_actual < osr or chfilt_osr_actual > osr + 1.0:
                                continue
                        else:
                            if (chfilt_osr_actual < min_chfilt_osr) or (chfilt_osr_actual > max_chfilt_osr):
                                # not a solution, next value of dec1 loop
                                continue
                    elif demod_select == model.vars.demod_select.var_enum.TRECS_SLICER or \
                            demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI:
                        # forcing integer osr condition, which applies to TRECS
                        # check for TRECS minimum clk cycle requirements
                        calc_min_dec2 = ceil(min_src2 * float(adc_freq) / (osr * dec0 * dec1 * 8 * baudrate))
                        calc_max_dec2 = floor(max_src2 * float(adc_freq) / (osr * dec0 * dec1 * 8 * baudrate))
                        # trecs_src_interp_okay = self._check_trecs_required_clk_cycles(adc_freq, baudrate, osr, dec0,
                        #                                                              dec1, xtal_frequency_hz, relaxsrc2, model)
                        # if not trecs_src_interp_okay:
                        #     # not a solution due to trecs clocking constraints, continue
                        #     continue
                    else:
                        # forcing integer osr condition, which applies to LEGACY, COHERENT
                        calc_min_dec2 = ceil(min_src2 * float(adc_freq) / (osr * dec0 * dec1 * 8 * baudrate))
                        calc_max_dec2 = floor(max_src2 * float(adc_freq) / (osr * dec0 * dec1 * 8 * baudrate))
                    if (calc_min_dec2 <= calc_max_dec2) and (calc_min_dec2 <= max_dec2) and \
                            (calc_max_dec2 >= min_dec2):
                        # calculation of dec1 has constrained bwsel to range bwsel_min to bwsel_max
                        bwsel = bandwidth * (8 * dec0 * dec1) / float(adc_freq)
                        bwsel_error = abs(bwsel - target_bwsel)
                        # Select largest bwsel as best result
                        if (bwsel_error < best_bwsel_error):
                            best_bwsel_error = bwsel_error
                            best_osr = osr
                            best_dec0 = dec0
                            best_dec1 = dec1
                            best_bwsel = bwsel
            if best_osr > 0 and quitatfirstvalid:
                # break out of the osr loop on first successful configuration
                break
        return best_osr, best_dec0, best_dec1, min_osr, max_osr

    # Method name: return_solution
    # Defined in: ocelot\calculators\calc_demodulator.py
    def return_solution(self, model, demod_select):
        # Check if we have a solution for OSR, DEC0, and DEC1
        [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select)
        # If we have selected TRECS but did not find a solution with the above line try to find a solution
        # with relaxed SRC2 limits (SRC2 > 0.55 instead of SRC2 > 0.8)
        # FIXME: once we are comfortable with the limit at 0.55 we might want to make this the general limit and remove this call
        is_trecs = demod_select == model.vars.demod_select.var_enum.TRECS_SLICER or demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI
        # is_vcodiv_high_bw widens the src2 limits for PHYs that would be affected by IPMCUSRW_876
        # The issue occurs when the filter chain is in a VCODIV + dec=4,1 configuration. We'll want to constrain
        # the filter to go to the next decimation factor (likely 3,2) and use fractional interpolation on the SRC2.
        # We can't use dec0_actual, dec1_actual because those are the variables we are solving for
        # instead, base the decision on if the bandwidth is in the range of what would use dec=4,1.
        # the final check is handled by _channel_filter_clocks_valid
        bandwidth_hz_threshold = model.vars.adc_freq_actual.value / (8 * 4 * 1) * 0.2
        is_vcodiv_high_bw = model.vars.adc_clock_mode.value == model.vars.adc_clock_mode.var_enum.VCODIV and \
                            model.vars.bandwidth_hz.value > bandwidth_hz_threshold
        no_solution = target_osr == 0 or target_osr > max_osr
        if (is_trecs or is_vcodiv_high_bw) and no_solution:
            [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select, relaxsrc2=True)
        # If in TRECS SLICER mode we have one more chance to find a working solution this time with the remodulation
        # path enabled.
        if demod_select == model.vars.demod_select.var_enum.TRECS_SLICER and (
                target_osr == 0 or target_osr > max_osr):
            [target_osr, dec0, dec1, min_osr, max_osr] = self.return_osr_dec0_dec1(model, demod_select, withremod=True)
        # return solution if we have found one
        return target_osr, dec0, dec1, min_osr, max_osr

# Method name: calc_target_sensitivity
# Defined in: ocelot\calculators\calc_utilities.py
    def calc_target_sensitivity(self, model):
        #Overriding function due to variable name change
        #Load model variables into local variables
        bitrate = model.vars.bitrate.value #This is the net bitrate (data only), because that is how Eb/No is defined
        freq = model.vars.base_frequency_hz.value
        modformat = model.vars.modulation_type.value
        demod = model.vars.demod_select.value
        # approximate EbNo number to use for our PHY
        if modformat == model.vars.modulation_type.var_enum.FSK4:
            ebno = 14.0
        elif modformat == model.vars.modulation_type.var_enum.OOK:
            ebno = 19.0
        elif modformat == model.vars.modulation_type.var_enum.OQPSK:
            # : For coherent demod, ebno = 8.5 based on measurement and Per's sim
            if demod == model.vars.demod_select.var_enum.COHERENT:
                ebno = 8.5
            else: # : Legacy demod
                ebno = 13.0
        else:
            ebno = 13.0
        # approximate noise figure to use for each band
        if freq < 500e6:
            nf = 3.5
        else:
            nf = 4.0
        target_sensitivity = -173.9 + 10 * math.log(bitrate, 10) + ebno + nf
        #Load local variables back into model variables
        model.vars.sensitivity.value = target_sensitivity

# Method name: calc_ook_ebno
# Defined in: common\calculators\calc_utilities.py
    def calc_ook_ebno(self,model):
        #Set the EbN0 for OOK on Dumbo, Jumbo, Nerio as 21.5
        model.vars.ook_ebno.value = 21.5

    # Method name: calc_dec2_actual
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_dec2_actual(self, model):
        # This function calculates the actual dec2 ratio from the register value
        # Load model variables into local variables
        dec2_reg = model.vars.MODEM_CF_DEC2.value
        # The actual dec2 value is the dec2 register plus one
        dec2_actual = dec2_reg + 1
        # Load local variables back into model variables
        model.vars.dec2_actual.value = dec2_actual

    # Method name: calc_dec2_reg
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_dec2_reg(self, model):
        # This function calculates the dec2 register value
        # Load model variables into local variables
        dec2_value = model.vars.dec2.value
        # The dec2 register is one less than the decimation value
        dec2_reg = dec2_value - 1
        # Write to register
        self._ip_reg_write(model, 'CF_DEC2', dec2_reg)

    # Method name: calc_ctrl2_rxfrcdis
    # Defined in: ocelot\calculators\calc_frame.py
    def calc_ctrl2_rxfrcdis(self, model):
        # TODO: move this to modem IP module
        # This method calculates the RXFRCDIS field
        # Disable writing to FRC in direct mode
        directmode_rx = model.vars.directmode_rx.value
        if directmode_rx != model.vars.directmode_rx.var_enum.DISABLED:
            rxfrcdis = 1
        else:
            rxfrcdis = 0
        self._ip_reg_write(model, 'CTRL2_RXFRCDIS', rxfrcdis)

    # Method name: calc_modem_frequency
    # Defined in: ocelot\calculators\calc_fpll.py
    def calc_modem_frequency(self, model):
        #Read in model variables
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        #For Ocelot, the hard demod rate is simply the xtal frequency
        modem_frequency_hz = float(xtal_frequency_hz)
        #Write the model variable
        model.vars.modem_frequency_hz.value = modem_frequency_hz
