from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from math import floor, log2, ceil
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException

class CalcFefiltRX(IPCalculator):
    SRC2DENUM = 524288.0


    # Method name: calc_dec0_actual
    # Defined in: lpwh74000\calculators\calc_demodulator.py
    def calc_dec0_actual(self,model):
        #This function calculates the actual dec0 based on the register value

        #Load model variables into local variables
        dec0_reg = model.vars.FEFILT_CF_DEC0.value

        #Define a constant list for the (register data, value pairs)
        dec0_list = [(0, 3), (1, 4), (2, 4), (3, 8), (4, 8), (5, 5)]
        #Search for the value in the list
        for dec0_pair in dec0_list:
            if (dec0_pair[0]==dec0_reg):
                dec0_value = dec0_pair[1]

        #Load local variables back into model variables
        model.vars.dec0_actual.value = dec0_value

    # Method name: calc_dec0_reg
    # Defined in: lpwh74000\calculators\calc_demodulator.py
    def calc_dec0_reg(self,model):
        #This function writes the register for dec0

        #Load model variables into local variables
        dec0_value = model.vars.dec0.value

        #Define a constant list for the (register data, value pairs)
        dec0_list = [(0, 3), (2, 4), (4, 8), (5, 5)]
        # Search for the value in the list
        for dec0_pair in dec0_list:
            if (dec0_pair[1]==dec0_value):
                dec0_reg = dec0_pair[0]

        # Write the registers
        self._ip_reg_write(model, 'CF_DEC0', dec0_reg)

    # Method name: calc_dec1_actual
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_dec1_actual(self, model):
        # This function calculates the actual dec1 based on the register value
        # Load model variables into local variables
        dec1_reg = model.vars.FEFILT_CF_DEC1.value
        # Dec1 value is simply one more than the register setting
        dec1_value = dec1_reg + 1
        # Load local variables back into model variables
        model.vars.dec1_actual.value = dec1_value

    # Method name: calc_dec1_reg
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_dec1_reg(self, model):
        # This function writes the register for dec1
        # Load model variables into local variables
        dec1_value = model.vars.dec1.value
        # Dec1 register is simply one less than the value
        dec1_reg = dec1_value - 1
        # Write the registers
        self._ip_reg_write(model, 'CF_DEC1', dec1_reg)

    # Method name: calc_dec1gain_actual
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_dec1gain_actual(self, model):
        """given register settings return actual DEC1GAIN used
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        reg = model.vars.FEFILT_CF_DEC1GAIN.value
        if reg == 0:
            val = 0
        elif reg == 1:
            val = 6
        else:
            val = 12
        model.vars.dec1gain_actual.value = val

    # Method name: calc_dec1gain_reg
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_dec1gain_reg(self, model):
        """set DEC1GAIN register based on calculated value
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        val = model.vars.dec1gain.value
        if val == 12:
            reg = 2
        elif val == 6:
            reg = 1
        else:
            reg = 0
        self._ip_reg_write(model, 'CF_DEC1GAIN', reg)

    # Method name: calc_dec1gain_value
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_dec1gain_value(self, model):
        """calculate additional gain we want in the DEC1 decimator for very low bandwidth
        PHY settings.
        see register definition of DEC1GAIN in EFR32 Reference Manual (internal.pdf)
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        bw = model.vars.bandwidth_actual.value
        if bw < 500:
            dec1gain = 12
        elif bw < 2000:
            dec1gain = 6
        else:
            dec1gain = 0
        model.vars.dec1gain.value = dec1gain

    # Method name: calc_digmixfreq_actual
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_digmixfreq_actual(self, model):
        # This function calculates the actual digital mixer frequency based on the register
        # Load model variables into local variables
        digmixfreq_reg = model.vars.FEFILT_DIGMIXCTRL_DIGMIXFREQ.value
        # Calculate the actual mixer frequency
        if model.vars.lo_injection_side.value == model.vars.lo_injection_side.var_enum.HIGH_SIDE:
            digmixfreq_actual = int(digmixfreq_reg * model.vars.digmix_res_actual.value)
        else:
            model_var = model.vars.FEFILT_DIGMIXCTRL_DIGMIXFREQ
            digmixfreq_regsize = model_var.rm.bitWidth
            digmixfreq_pos = (2 ** digmixfreq_regsize) - digmixfreq_reg
            digmixfreq_actual = -1 * int(digmixfreq_pos * model.vars.digmix_res_actual.value)
        # Load local variables back into model variables
        model.vars.digmixfreq_actual.value = digmixfreq_actual

    # Method name: calc_digmixfreq_reg
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_digmixfreq_reg(self, model):
        # This function calculates the digital mixer register
        digmixfreq_reg = model.vars.digmixfreq.value
        # Write register
        self._reg_write(model.vars.FEFILT_DIGMIXCTRL_DIGMIXFREQ, digmixfreq_reg, allow_neg=True, neg_twos_comp=True)

    # Method name: calc_digmixfreq_val
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_digmixfreq_val(self, model):
        digmix_res = model.vars.digmix_res_actual.value
        fif = model.vars.if_frequency_hz_actual.value  # IF frequency based on the actual SYNTH settings
        """From series 2 onwards, using negative DIGMIXFREQ for low-side injection (See https://jira.silabs.com/browse/MCUW_RADIO_CFG-1906)"""
        if model.vars.lo_injection_side.value == model.vars.lo_injection_side.var_enum.HIGH_SIDE:
            model.vars.digmixfreq.value = int(round(fif / digmix_res))
        else:
            model.vars.digmixfreq.value = int(round(fif / digmix_res)) * -1


    # Method name: calc_src2_actual
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_src2_actual(self, model):
        # This function calculates the actual SRC2 ratio from the register value
        # Load model variables into local variables
        src2_reg = model.vars.FEFILT_SRCCHF_SRCRATIO2.value
        src2_en_reg = model.vars.FEFILT_SRCCHF_SRCENABLE2.value
        if src2_en_reg:
            # The src2 ratio is simply 2^19 divided by the register value
            src2_ratio_actual = self.SRC2DENUM / src2_reg
        else:
            src2_ratio_actual = 1.0
        # Load local variables back into model variables
        model.vars.src2_ratio_actual.value = src2_ratio_actual

    # Method name: calc_src2_dec2
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_src2_dec2(self, model):
        # This function calculates dec2 and src2
        # FIXME: need to have an options for TRecS where DEC2 is bypassed DEC2=1
        #        unless the remod is enabled
        # Load model variables into local variables
        adc_freq = model.vars.adc_freq_actual.value
        dec0 = model.vars.dec0_actual.value
        dec1 = model.vars.dec1_actual.value
        baudrate = model.vars.baudrate.value  # We don't know the actual baudrate yet
        target_osr = model.vars.target_osr.value  # We don't know the actual OSR value yet
        demod_sel = model.vars.demod_select.value
        max_dec2 = model.vars.max_dec2.value
        min_dec2 = model.vars.min_dec2.value
        min_src2 = model.vars.min_src2.value  # min value for SRC2
        max_src2 = model.vars.max_src2.value  # max value for SRC2
        if (demod_sel == model.vars.demod_select.var_enum.BCR):
            # BCR demod, dec2 and src2 not enabled
            best_dec2 = 1
            best_src2 = 1.0
        else:
            # Legacy, Coherent, Trecs/Viterbi Demods
            # Calculate the OSR at the input to SRC2
            osr_src2_min = float(adc_freq) / (8 * dec0 * dec1 * baudrate) * min_src2
            osr_src2_max = float(adc_freq) / (8 * dec0 * dec1 * baudrate) * max_src2
            # Calculate dec2 to achieve close to the target OSR
            dec2_min = max(int(ceil(osr_src2_min / target_osr)), min_dec2)
            dec2_max = min(int(floor(osr_src2_max / target_osr)), max_dec2)
            target_src2 = 1.0
            best_error = 999
            # default values
            best_dec2 = 1
            best_src2 = (8 * dec0 * dec1 * baudrate) * target_osr / float(adc_freq)
            for dec2 in range(dec2_min, dec2_max + 1):
                src2 = dec2 * (8 * dec0 * dec1 * baudrate) * target_osr / float(adc_freq)
                error = abs(target_src2 - src2)
                if best_error > error:
                    best_error = error
                    best_src2 = src2
                    best_dec2 = dec2
        # Load local variables back into model variables
        model.vars.dec2.value = best_dec2
        model.vars.src2_ratio.value = best_src2

    # Method name: calc_src2_denominator
    # Defined in: bobcat\calculators\calc_demodulator.py
    def calc_src2_denominator(self, model):
        # Load model variables into local variables
        osr = model.vars.oversampling_rate_actual.value
        datarate = model.vars.baudrate.value
        dec0 = model.vars.dec0_actual.value
        dec1 = model.vars.dec1_actual.value
        dec2 = model.vars.dec2_actual.value
        adc_clock_mode = model.vars.adc_clock_mode.value
        if (model.vars.adc_clock_mode.var_enum.HFXOMULT == adc_clock_mode):
            src2_calcDenominator = 0
        else:
            # This does not include the 8x downsampling polyphase filter after IFADC. Handled in RAIL code
            src2_calcDenominator = int(datarate * dec0 * dec1 * dec2 * osr)
        # Load local variables back into model variables
        model.vars.src2_calcDenominator.value = src2_calcDenominator

    # Method name: calc_src2_reg
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_src2_reg(self, model):
        # This function calculates the src2 register writes
        # Load model variables into local variables
        src2_value = model.vars.src2_ratio.value
        min_src2 = model.vars.min_src2.value  # min value for SRC2
        max_src2 = model.vars.max_src2.value  # max value for SRC2
        if (src2_value >= min_src2) and (src2_value <= max_src2):
            src2_reg = int(round(self.SRC2DENUM / src2_value))
        else:
            raise CalculationException('WARNING: src2 value out of range in calc_src2_reg()')
        # : The scipy resample_poly function within the gen_frequency_signal function is not able to efficiently handle
        # : prime numbers, leading to extremely long calculation time. This code adjusts src2 reg value by small amount
        # : if large prime number is encountered.
        if self._is_prime(src2_reg):
            if src2_reg < 1048576 - 1:
                src2_reg = src2_reg + 1
            else:
                src2_reg = src2_reg - 1
        if (src2_reg != self.SRC2DENUM):
            src2_en = 1
        else:
            src2_en = 0
        # Write to registers
        self._ip_reg_write(model, 'SRCCHF_SRCRATIO2', src2_reg)
        self._ip_reg_write(model, 'SRCCHF_SRCENABLE2', src2_en)


    # Method name: calc_dccomp_misc_reg
    def calc_dccomp_misc_reg(self, model):
        # always enable both DC offset estimation and compensation blocks
        self._ip_reg_write(model, 'DCCOMP_DCESTIEN', 1)
        # don't reset at every packet
        self._ip_reg_write(model, 'DCCOMP_DCRSTEN', 0)
        # always enable gear shifting option
        self._ip_reg_write(model, 'DCCOMP_DCGAINGEAREN', 1)
        # when AGC gain change happens set the gear to fastest
        self._ip_reg_write(model, 'DCCOMP_DCGAINGEAR', 10)
        # final gear setting after settling
        self._ip_reg_write(model, 'DCCOMP_DCCOMPGEAR', 6)
        # limit max DC to 1V
        self._ip_reg_write(model, 'DCCOMP_DCLIMIT', 0)
        # don't freeze state of DC comp filters
        self._ip_reg_write(model, 'DCCOMP_DCCOMPFREEZE', 0)
        # time between gear shifts - set to fixed value for now
        self._ip_reg_write(model, 'DCCOMP_DCGAINGEARSMPS', 40)

    def calc_dc_comp_en_reg(self, model):
        if_frequency_hz = model.vars.if_frequency_hz_actual.value
        if if_frequency_hz == 0:
            dccomp_en = 0
        else:
            dccomp_en = 1
        self._ip_reg_write(model, 'DCCOMP_DCCOMPEN', dccomp_en)

    # Method name: calc_chflatency_actual
    def calc_chflatency_actual(self, model):
        # chflatency = model.vars.FEFILT_CHFLATENCYCTRL_CHFLATENCY.value
        # model.vars.chflatency_actual.value = chflatency
        model.vars.chflatency_actual.value = 0

    # Method name: _is_prime
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def _is_prime(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        max_divisor = int(n ** 0.5) + 1
        for d in range(3, max_divisor, 2):
            if n % d == 0:
                return False
        return True

    # Method name: calc_lo_side_regs
    # Defined in: lpwh72000\calculators\calc_synth.py
    def calc_lo_side_fefilt_regs(self, model):
        """Both these values should be the same for low-side and high-side. Use negative DIGMIXFREQ for low-side.
         See https://jira.silabs.com/browse/MCUW_RADIO_CFG-1906"""
        digiqswapen = 1
        mixerconj = 0
        self._ip_reg_write(model, 'MIXCTRL_DIGIQSWAPEN', digiqswapen)
        self._ip_reg_write(model, 'DIGMIXCTRL_MIXERCONJ', mixerconj)

    def calc_zif_mixer_bypass_reg(self, model):
        if model.vars.if_frequency_hz_actual.value == 0:
            zif_bypass = 1
        else:
            zif_bypass = 0
        self._ip_reg_write(model, 'DIGMIXCTRL_ZIFMODEENABLE', zif_bypass)