from pycalcmodel.core.variable import ModelVariableFormat
from pyradioconfig.parts.lion.calculators.calc_demodulator import CalcDemodulatorLion
import math
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException

class CalcDemodulatorCurl(CalcDemodulatorLion):
    # This table is generated with srw_model/models/channel_filters/gen_channel_filter_coeffs.m
    # Key: bwsel (actual) - Value: Corresponding channel filter coeff
    # if bwsel < 0.155:
    #     coeffs = coeff_list_1
    # elif bwsel < 0.165:
    #     coeffs = coeff_list_2
    # is equivalent to
    # bwsel_actual = round(bwsel, 2)
    # channel_filter_lut = { 0.15: coeff_list_1, 0.16: coeff_list_2}
    # coeffs = channel_filter_lut[bwsel_actual]
    channel_filter_lut = {
        0.15: [-16, -51, -86, -101, -82, -17, 97, 248, 414, 565, 671, 709],
        0.16: [-6, -38, -84, -115, -111, -54, 60, 223, 409, 582, 704, 749],
        0.17: [1, -22, -74, -121, -134, -89, 23, 196, 402, 599, 740, 792],
        0.18: [22, 5, -53, -110, -139, -113, -12, 164, 388, 609, 772, 831],
        0.19: [25, 21, -32, -98, -145, -138, -48, 131, 372, 619, 804, 872],
        0.20: [24, 32, -10, -82, -147, -162, -86, 95, 354, 627, 836, 914],
        0.21: [19, 37, 8, -65, -147, -183, -123, 56, 332, 634, 868, 956],
        0.22: [21, 47, 31, -38, -130, -189, -153, 18, 305, 632, 893, 992],
        0.23: [23, 56, 54, -7, -107, -190, -180, -23, 273, 627, 915, 1026],
        0.24: [24, 67, 83, 36, -67, -171, -190, -51, 251, 632, 951, 1075],
        0.25: [14, 61, 97, 66, -36, -159, -205, -84, 223, 631, 981, 1118],
        0.26: [6, 48, 100, 91, -5, -143, -218, -119, 190, 625, 1007, 1159],
        0.27: [-2, 34, 99, 113, 29, -121, -226, -154, 154, 616, 1033, 1201],
        0.28: [-9, 17, 88, 126, 62, -93, -226, -185, 117, 604, 1058, 1243],
        0.29: [-15, -1, 72, 132, 92, -61, -221, -212, 79, 589, 1081, 1284],
        0.30: [-21, -19, 50, 130, 118, -26, -208, -235, 42, 573, 1102, 1324],
        0.31: [-26, -38, 23, 117, 137, 11, -188, -252, 4, 555, 1125, 1367],
        0.32: [-30, -57, -10, 95, 148, 47, -162, -262, -28, 540, 1150, 1413],
        0.33: [-33, -76, -50, 55, 135, 61, -151, -283, -73, 509, 1160, 1444],
        0.34: [-23, -78, -75, 30, 137, 92, -125, -293, -111, 485, 1178, 1485],
        0.35: [-13, -70, -94, -1, 130, 120, -93, -297, -150, 457, 1195, 1528],
        0.36: [-4, -59, -107, -32, 116, 143, -59, -296, -186, 429, 1211, 1570],
        0.37: [6, -43, -110, -61, 95, 160, -24, -290, -220, 398, 1225, 1611],
        0.38: [15, -24, -108, -88, 68, 170, 11, -279, -251, 366, 1238, 1652],
        0.39: [23, -2, -96, -109, 37, 171, 44, -264, -281, 333, 1249, 1692],
        0.40: [31, 22, -76, -124, 4, 165, 73, -247, -308, 298, 1258, 1731],
        0.41: [39, 51, -42, -124, -28, 153, 98, -231, -339, 255, 1260, 1765],
        0.42: [40, 78, 1, -106, -42, 152, 138, -195, -352, 225, 1275, 1814],
        0.43: [30, 86, 29, -101, -70, 135, 164, -166, -371, 188, 1283, 1854],
        0.44: [20, 86, 58, -87, -97, 112, 188, -133, -387, 148, 1289, 1897],
        0.45: [9, 80, 82, -66, -117, 84, 205, -99, -399, 108, 1293, 1939],
        0.46: [-2, 68, 101, -39, -131, 54, 217, -63, -407, 69, 1296, 1980],
        0.47: [-14, 49, 111, -9, -135, 22, 223, -27, -411, 29, 1297, 2020],
        0.48: [-26, 25, 114, 23, -131, -8, 224, 10, -411, -10, 1297, 2060]
    }

    def calc_dec0_reg(self,model):
        val = model.vars.dec0.value
        fxo = model.vars.xtal_frequency.value
        bw = model.vars.bandwidth_hz.value * 1.0

        if val == 3:
            reg = 0
        elif val == 4:
            reg = 1
        elif val == 8:
            if bw > fxo * 0.005:
                reg = 3
            else:
                reg = 4
        elif val == 5:
            reg = 5
        else:
            raise CalculationException("Unsupported DEC0 value")

        self._reg_write(model.vars.MODEM_CF_DEC0, reg)

    def calc_dec0_actual(self, model):
        """Read register value and return decimation rate for DEC0."""
        reg = model.vars.MODEM_CF_DEC0.value

        try:
            dec_list = [3, 4, 4, 8, 8, 5]
            dec0 = dec_list[reg]
        except IndexError:
            raise CalculationException(f"Unsupported register value for DEC0 ({reg})")

        model.vars.dec0_actual.value = dec0

    def calc_chfilt_reg(self,model):
        # This function calculates the channel filter registers
        csdcoeffs = [0 for i in range(12)]
        csdcoeffs_sign = [0 for i in range(12)]
        bit_widths = [7, 8, 8, 9, 9, 9, 9, 10, 10, 11, 12, 12]

        #chfgainreduction_reg = model.vars.FEFILT_CHFCTRL_CHFGAINREDUCTION.value

        #if (chfgainreduction_reg == 1):
        #    coeffs = [13, 31, 29, -1, -52, -94, -89, -12, 136, 313, 458, 514]
        #else:
        coeffs = self.return_coeffs(model)

        #csdcoeffs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #csdcoeffs_sign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # csdcoeffs_bit_widths = [6,8,8,8,8,9,9,9,10,10,11,12] CSD coefficients bit width is smaller due to it's unsigned
        #bit_widths = [7, 8, 8, 9, 9, 9, 9, 10, 10, 11, 12, 12]

        # replace negative numbers with 2s complement
        for i in range(12):
            csdcoeffs[i], csdcoeffs_sign[i] = self.return_csd(coeffs[i], bit_widths[i])

        # Write registers
        self._reg_write(model.vars.MODEM_CHFCSDCOE00_SET0CSDCOEFF0,  csdcoeffs[0])
        self._reg_write(model.vars.MODEM_CHFCSDCOE00_SET0CSDCOEFF1,  csdcoeffs[1])
        self._reg_write(model.vars.MODEM_CHFCSDCOE00_SET0CSDCOEFF2,  csdcoeffs[2])
        self._reg_write(model.vars.MODEM_CHFCSDCOE00_SET0CSDCOEFF3,  csdcoeffs[3])
        self._reg_write(model.vars.MODEM_CHFCSDCOE01_SET0CSDCOEFF4,  csdcoeffs[4])
        self._reg_write(model.vars.MODEM_CHFCSDCOE01_SET0CSDCOEFF5,  csdcoeffs[5])
        self._reg_write(model.vars.MODEM_CHFCSDCOE01_SET0CSDCOEFF6,  csdcoeffs[6])
        self._reg_write(model.vars.MODEM_CHFCSDCOE02_SET0CSDCOEFF7,  csdcoeffs[7])
        self._reg_write(model.vars.MODEM_CHFCSDCOE02_SET0CSDCOEFF8,  csdcoeffs[8])
        self._reg_write(model.vars.MODEM_CHFCSDCOE02_SET0CSDCOEFF9,  csdcoeffs[9])
        self._reg_write(model.vars.MODEM_CHFCSDCOE03_SET0CSDCOEFF10, csdcoeffs[10])
        self._reg_write(model.vars.MODEM_CHFCSDCOE03_SET0CSDCOEFF11, csdcoeffs[11])

        self._reg_write(model.vars.MODEM_CHFCSDCOE00S_SET0CSDCOEFF0S,  csdcoeffs_sign[0])
        self._reg_write(model.vars.MODEM_CHFCSDCOE00S_SET0CSDCOEFF1S,  csdcoeffs_sign[1])
        self._reg_write(model.vars.MODEM_CHFCSDCOE00S_SET0CSDCOEFF2S,  csdcoeffs_sign[2])
        self._reg_write(model.vars.MODEM_CHFCSDCOE00S_SET0CSDCOEFF3S,  csdcoeffs_sign[3])
        self._reg_write(model.vars.MODEM_CHFCSDCOE00S_SET0CSDCOEFF4S,  csdcoeffs_sign[4])
        self._reg_write(model.vars.MODEM_CHFCSDCOE00S_SET0CSDCOEFF5S,  csdcoeffs_sign[5])
        self._reg_write(model.vars.MODEM_CHFCSDCOE00S_SET0CSDCOEFF6S,  csdcoeffs_sign[6])
        self._reg_write(model.vars.MODEM_CHFCSDCOE01S_SET0CSDCOEFF7S,  csdcoeffs_sign[7])
        self._reg_write(model.vars.MODEM_CHFCSDCOE01S_SET0CSDCOEFF8S,  csdcoeffs_sign[8])
        self._reg_write(model.vars.MODEM_CHFCSDCOE01S_SET0CSDCOEFF9S,  csdcoeffs_sign[9])
        self._reg_write(model.vars.MODEM_CHFCSDCOE01S_SET0CSDCOEFF10S, csdcoeffs_sign[10])
        self._reg_write(model.vars.MODEM_CHFCSDCOE01S_SET0CSDCOEFF11S, csdcoeffs_sign[11])


        coeffs = self.return_coeffs(model)

        # print(f"CHF Set 1 coefficient values for BW, BWSEL = : {model.vars.bandwidth_hz.value, bwsel}")

        # replace negative numbers with 2s complement
        for i in range(12):
            csdcoeffs[i], csdcoeffs_sign[i] = self.return_csd(coeffs[i], bit_widths[i])

        # TODO: calculate the second set separately
        self._reg_write(model.vars.MODEM_CHFCSDCOE10_SET1CSDCOEFF0,  csdcoeffs[0])
        self._reg_write(model.vars.MODEM_CHFCSDCOE10_SET1CSDCOEFF1,  csdcoeffs[1])
        self._reg_write(model.vars.MODEM_CHFCSDCOE10_SET1CSDCOEFF2,  csdcoeffs[2])
        self._reg_write(model.vars.MODEM_CHFCSDCOE10_SET1CSDCOEFF3,  csdcoeffs[3])
        self._reg_write(model.vars.MODEM_CHFCSDCOE11_SET1CSDCOEFF4,  csdcoeffs[4])
        self._reg_write(model.vars.MODEM_CHFCSDCOE11_SET1CSDCOEFF5,  csdcoeffs[5])
        self._reg_write(model.vars.MODEM_CHFCSDCOE11_SET1CSDCOEFF6,  csdcoeffs[6])
        self._reg_write(model.vars.MODEM_CHFCSDCOE12_SET1CSDCOEFF7,  csdcoeffs[7])
        self._reg_write(model.vars.MODEM_CHFCSDCOE12_SET1CSDCOEFF8,  csdcoeffs[8])
        self._reg_write(model.vars.MODEM_CHFCSDCOE12_SET1CSDCOEFF9,  csdcoeffs[9])
        self._reg_write(model.vars.MODEM_CHFCSDCOE13_SET1CSDCOEFF10, csdcoeffs[10])
        self._reg_write(model.vars.MODEM_CHFCSDCOE13_SET1CSDCOEFF11, csdcoeffs[11])

        self._reg_write(model.vars.MODEM_CHFCSDCOE10S_SET1CSDCOEFF0S,  csdcoeffs_sign[0])
        self._reg_write(model.vars.MODEM_CHFCSDCOE10S_SET1CSDCOEFF1S,  csdcoeffs_sign[1])
        self._reg_write(model.vars.MODEM_CHFCSDCOE10S_SET1CSDCOEFF2S,  csdcoeffs_sign[2])
        self._reg_write(model.vars.MODEM_CHFCSDCOE10S_SET1CSDCOEFF3S,  csdcoeffs_sign[3])
        self._reg_write(model.vars.MODEM_CHFCSDCOE10S_SET1CSDCOEFF4S,  csdcoeffs_sign[4])
        self._reg_write(model.vars.MODEM_CHFCSDCOE10S_SET1CSDCOEFF5S,  csdcoeffs_sign[5])
        self._reg_write(model.vars.MODEM_CHFCSDCOE10S_SET1CSDCOEFF6S,  csdcoeffs_sign[6])
        self._reg_write(model.vars.MODEM_CHFCSDCOE11S_SET1CSDCOEFF7S,  csdcoeffs_sign[7])
        self._reg_write(model.vars.MODEM_CHFCSDCOE11S_SET1CSDCOEFF8S,  csdcoeffs_sign[8])
        self._reg_write(model.vars.MODEM_CHFCSDCOE11S_SET1CSDCOEFF9S,  csdcoeffs_sign[9])
        self._reg_write(model.vars.MODEM_CHFCSDCOE11S_SET1CSDCOEFF10S, csdcoeffs_sign[10])
        self._reg_write(model.vars.MODEM_CHFCSDCOE11S_SET1CSDCOEFF11S, csdcoeffs_sign[11])

    def return_coeffs(self, model):
        bwsel_actual = model.vars.bwsel_actual.value

        coeffs = self.channel_filter_lut[bwsel_actual]
        # Confirm Sum of the Magnitudes is in spec to not overflow the filter accumulator
        try:
            assert sum([abs(i) for i in coeffs]) < 2**16
        except AssertionError:
            raise CalculationException('ERROR: Channel Filter Coefficients Sum of Magnitudes >= 2^16')

        return coeffs

    def return_csd(self, coeff, bitwidth):
        coeff1 = coeff
        sign_bitwidth = math.ceil(bitwidth / 2)
        csdcoeffsign = 0
        pointer = 0
        signinv = 0
        if coeff < 0:
            coeff = -coeff
            signinv = 1
        csdcoeff = coeff
        if coeff > 2:
            while coeff > 2:
                if coeff % 4 == 3 and (pointer + 2) < bitwidth:
                    csdcoeff = csdcoeff + 2 ** (pointer + 1)
                    csdcoeffsign = csdcoeffsign + 2 ** (pointer // 2)
                coeff = csdcoeff // 2 ** (pointer + 1)
                pointer += 1
        # mask values per csdcoeff and csdcoeffsign bitwidths
        csdcoeff = csdcoeff & (2 ** bitwidth - 1)
        csdcoeffsign = csdcoeffsign & (2 ** sign_bitwidth - 1)

        if signinv:
            csdcoeffsign = csdcoeffsign ^ (2 ** sign_bitwidth - 1)
        # print(f"coeff, bitwidth, csdcoeff ,csdcoeffsign : {coeff1,bitwidth,csdcoeff,csdcoeffsign}")
        # print(f"{coeff1}")
        return csdcoeff, csdcoeffsign

    # kulee: For now, NADM uses maximum possible bandwidth, corresponding to
    # all pass filter. Only the center tap is used, 2047 in 12.11 format is
    # 2047/2^11 ~ 1.0 and 2047 in CSD format is {2049,1}. For non-HADM PHYs,
    # the second CHF is turned off it doesn't matter what we do here.
    def calc_hadm_nadm_second_csd_chf(self, model):
        self._reg_write(model.vars.MODEM_CHFCSDCOE00NADM_NADMCSDCOEFF0, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00NADM_NADMCSDCOEFF1, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00NADM_NADMCSDCOEFF2, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00NADM_NADMCSDCOEFF3, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE01NADM_NADMCSDCOEFF4, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE01NADM_NADMCSDCOEFF5, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE01NADM_NADMCSDCOEFF6, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE02NADM_NADMCSDCOEFF7, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE02NADM_NADMCSDCOEFF8, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE02NADM_NADMCSDCOEFF9, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE03NADM_NADMCSDCOEFF10, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE03NADM_NADMCSDCOEFF11, 2049)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00SNADM_NADMCSDCOEFF0S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00SNADM_NADMCSDCOEFF1S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00SNADM_NADMCSDCOEFF2S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00SNADM_NADMCSDCOEFF3S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00SNADM_NADMCSDCOEFF4S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00SNADM_NADMCSDCOEFF5S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE00SNADM_NADMCSDCOEFF6S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE01SNADM_NADMCSDCOEFF7S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE01SNADM_NADMCSDCOEFF8S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE01SNADM_NADMCSDCOEFF9S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE01SNADM_NADMCSDCOEFF10S, 0)
        self._reg_write(model.vars.MODEM_CHFCSDCOE01SNADM_NADMCSDCOEFF11S, 1)

    def calc_dec0_values_available(self, model):
        hadm_enable = model.vars.hadm_enable.value == model.vars.hadm_enable.var_enum.ENABLED

        flag_allow_dec0_dec_by_5 = 1 if hadm_enable else 0

        model.vars.input_decimation_filter_allow_dec3.value = 1
        model.vars.input_decimation_filter_allow_dec8.value = 1
        model.vars.input_decimation_filter_allow_dec5.value = flag_allow_dec0_dec_by_5

    def calc_ch_filt_bw_available(self, model):
        """
        List of available channel filter bandwidth (bwsel). Channel filter bandwidth is configured by the programmable
        channel filter. Calculator will choose a bwsel in the list, and a set of decimator value to be the closest
        to target bandwidth.
        """
        hadm_enable = model.vars.hadm_enable.value == model.vars.hadm_enable.var_enum.ENABLED

        if hadm_enable:
            # For HADM, belows bwsel values has been tested and validated, so the calculator must select one among them.
            # bwsel is such that bandwidth_hz = bwsel * xtal_frequency_hz / (dec0 * dec1)
            # ------------------------------------
            # XTAL = 40MHz:          bwsel = 0.275
            # XTAL = 39MHz:          bwsel = 0.226
            # XTAL = 38.4MHz:        bwsel = 0.229
            # XTAL = 38MHz:          bwsel = 0.232
            model.vars.ch_filt_bw_available.value = [0.275, 0.226, 0.229, 0.232]
        else:
            # For non HADM PHYs, use same bwsel list as for the fixed coeff channel filter, like older part.
            super().calc_ch_filt_bw_available(model)

    def calc_bwsel_actual(self, model):
        bwsel = model.vars.bwsel.value

        bwsel_list = self.channel_filter_lut.keys()  # Get the list of all possible programmable bwsel
        bwsel_actual = min(bwsel_list, key=lambda x: abs(x - round(bwsel, 2)))  # Get the closest actual from calculated

        model.vars.bwsel_actual.value = bwsel_actual

    def calc_bwsel_reg(self, model):
        # The field has no effect: fixed channel bandwidth channel filter replaced by a programmable one
        self._reg_do_not_care(model.vars.MODEM_SRCCHF_BWSEL)

    def calc_init_advanced(self, model):
        hadm_enable = model.vars.hadm_enable.value == model.vars.hadm_enable.var_enum.ENABLED

        if hadm_enable:
            model.vars.src_disable.value = model.vars.src_disable.var_enum.SRC2_ONLY  # Disable SRC1
            model.vars.viterbi_enable.value = True
            model.vars.dsa_enable.value = False
            model.vars.target_osr.value = 4
        else:
            super().calc_init_advanced(model)

    def calc_adc_clock_config(self, model):
        # These are explicitly set for parts>=Curl
        pass