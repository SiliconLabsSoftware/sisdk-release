from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from math import floor, log2, ceil
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr

class CalcFefiltCHF(IPCalculator):
    # Method name: calc_chfilt_reg
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_chfilt_reg(self, model):
        # This function calculates the channel filter registers
        protocol = model.vars.protocol_id.value
        csdcoeffs = [0 for i in range(12)]
        csdcoeffs_sign = [0 for i in range(12)]
        bit_widths = [7, 8, 8, 9, 9, 9, 9, 10, 10, 11, 12, 12]
        bwsel = model.vars.bwsel.value
        chfgainreduction_reg = model.vars.FEFILT_CHFCTRL_CHFGAINREDUCTION.value #todo: implement ip_read
        if protocol == model.vars.protocol_id.var_enum.BTC:
            # BTC PHY, it uses a specific channel filter
            csdcoeffs = [1, 73, 80, 2, 85, 162, 170, 2, 293, 650, 1172, 1026]
            csdcoeffs_sign = [0, 1, 4, 0, 30, 30, 28, 31, 3, 3, 8, 0]
            # Write registers
            self._ip_reg_write(model, 'CHFCSDCOE00_SET0CSDCOEFF0', csdcoeffs[0])
            self._ip_reg_write(model, 'CHFCSDCOE00_SET0CSDCOEFF1', csdcoeffs[1])
            self._ip_reg_write(model, 'CHFCSDCOE00_SET0CSDCOEFF2', csdcoeffs[2])
            self._ip_reg_write(model, 'CHFCSDCOE00_SET0CSDCOEFF3', csdcoeffs[3])
            self._ip_reg_write(model, 'CHFCSDCOE01_SET0CSDCOEFF4', csdcoeffs[4])
            self._ip_reg_write(model, 'CHFCSDCOE01_SET0CSDCOEFF5', csdcoeffs[5])
            self._ip_reg_write(model, 'CHFCSDCOE01_SET0CSDCOEFF6', csdcoeffs[6])
            self._ip_reg_write(model, 'CHFCSDCOE02_SET0CSDCOEFF7', csdcoeffs[7])
            self._ip_reg_write(model, 'CHFCSDCOE02_SET0CSDCOEFF8', csdcoeffs[8])
            self._ip_reg_write(model, 'CHFCSDCOE02_SET0CSDCOEFF9', csdcoeffs[9])
            self._ip_reg_write(model, 'CHFCSDCOE03_SET0CSDCOEFF10', csdcoeffs[10])
            self._ip_reg_write(model, 'CHFCSDCOE03_SET0CSDCOEFF11', csdcoeffs[11])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF0S', csdcoeffs_sign[0])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF1S', csdcoeffs_sign[1])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF2S', csdcoeffs_sign[2])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF3S', csdcoeffs_sign[3])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF4S', csdcoeffs_sign[4])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF5S', csdcoeffs_sign[5])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF6S', csdcoeffs_sign[6])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF7S', csdcoeffs_sign[7])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF8S', csdcoeffs_sign[8])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF9S', csdcoeffs_sign[9])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF10S', csdcoeffs_sign[10])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF11S', csdcoeffs_sign[11])
            # replace negative numbers with 2s complement
            csdcoeffs1 = [0 for i in range(12)]
            # for i in range(12):
            #    csdcoeffs1[i], csdcoeffs_sign[i] = self.return_csd(csdcoeffs[i], bit_widths[i])
            csdcoeffs1 = csdcoeffs
            # TODO: calculate the second set separately
            self._ip_reg_write(model, 'CHFCSDCOE10_SET1CSDCOEFF0', csdcoeffs1[0])
            self._ip_reg_write(model, 'CHFCSDCOE10_SET1CSDCOEFF1', csdcoeffs1[1])
            self._ip_reg_write(model, 'CHFCSDCOE10_SET1CSDCOEFF2', csdcoeffs1[2])
            self._ip_reg_write(model, 'CHFCSDCOE10_SET1CSDCOEFF3', csdcoeffs1[3])
            self._ip_reg_write(model, 'CHFCSDCOE11_SET1CSDCOEFF4', csdcoeffs1[4])
            self._ip_reg_write(model, 'CHFCSDCOE11_SET1CSDCOEFF5', csdcoeffs1[5])
            self._ip_reg_write(model, 'CHFCSDCOE11_SET1CSDCOEFF6', csdcoeffs1[6])
            self._ip_reg_write(model, 'CHFCSDCOE12_SET1CSDCOEFF7', csdcoeffs1[7])
            self._ip_reg_write(model, 'CHFCSDCOE12_SET1CSDCOEFF8', csdcoeffs1[8])
            self._ip_reg_write(model, 'CHFCSDCOE12_SET1CSDCOEFF9', csdcoeffs1[9])
            self._ip_reg_write(model, 'CHFCSDCOE13_SET1CSDCOEFF10', csdcoeffs1[10])
            self._ip_reg_write(model, 'CHFCSDCOE13_SET1CSDCOEFF11', csdcoeffs1[11])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF0S', csdcoeffs_sign[0])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF1S', csdcoeffs_sign[1])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF2S', csdcoeffs_sign[2])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF3S', csdcoeffs_sign[3])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF4S', csdcoeffs_sign[4])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF5S', csdcoeffs_sign[5])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF6S', csdcoeffs_sign[6])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF7S', csdcoeffs_sign[7])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF8S', csdcoeffs_sign[8])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF9S', csdcoeffs_sign[9])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF10S', csdcoeffs_sign[10])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF11S', csdcoeffs_sign[11])
        else:
            # print(f"CHF Set 0 coefficient values for BW, BWSEL = : {model.vars.bandwidth_hz.value, bwsel}")
            if (chfgainreduction_reg == 1):
                coeffs = [13, 31, 29, -1, -52, -94, -89, -12, 136, 313, 458, 514]
            else:
                coeffs = model.vars.channel_filter_coeffs_acq_bwsel.value
                # csdcoeffs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            # csdcoeffs_sign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            # csdcoeffs_bit_widths = [6,8,8,8,8,9,9,9,10,10,11,12] CSD coefficients bit width is smaller due to it's unsigned
            # bit_widths = [7, 8, 8, 9, 9, 9, 9, 10, 10, 11, 12, 12]
            # replace negative numbers with 2s complement
            for i in range(12):
                csdcoeffs[i], csdcoeffs_sign[i] = self.return_csd(coeffs[i], bit_widths[i])
            # Write registers
            self._ip_reg_write(model, 'CHFCSDCOE00_SET0CSDCOEFF0', csdcoeffs[0])
            self._ip_reg_write(model, 'CHFCSDCOE00_SET0CSDCOEFF1', csdcoeffs[1])
            self._ip_reg_write(model, 'CHFCSDCOE00_SET0CSDCOEFF2', csdcoeffs[2])
            self._ip_reg_write(model, 'CHFCSDCOE00_SET0CSDCOEFF3', csdcoeffs[3])
            self._ip_reg_write(model, 'CHFCSDCOE01_SET0CSDCOEFF4', csdcoeffs[4])
            self._ip_reg_write(model, 'CHFCSDCOE01_SET0CSDCOEFF5', csdcoeffs[5])
            self._ip_reg_write(model, 'CHFCSDCOE01_SET0CSDCOEFF6', csdcoeffs[6])
            self._ip_reg_write(model, 'CHFCSDCOE02_SET0CSDCOEFF7', csdcoeffs[7])
            self._ip_reg_write(model, 'CHFCSDCOE02_SET0CSDCOEFF8', csdcoeffs[8])
            self._ip_reg_write(model, 'CHFCSDCOE02_SET0CSDCOEFF9', csdcoeffs[9])
            self._ip_reg_write(model, 'CHFCSDCOE03_SET0CSDCOEFF10', csdcoeffs[10])
            self._ip_reg_write(model, 'CHFCSDCOE03_SET0CSDCOEFF11', csdcoeffs[11])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF0S', csdcoeffs_sign[0])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF1S', csdcoeffs_sign[1])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF2S', csdcoeffs_sign[2])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF3S', csdcoeffs_sign[3])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF4S', csdcoeffs_sign[4])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF5S', csdcoeffs_sign[5])
            self._ip_reg_write(model, 'CHFCSDCOE00S_SET0CSDCOEFF6S', csdcoeffs_sign[6])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF7S', csdcoeffs_sign[7])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF8S', csdcoeffs_sign[8])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF9S', csdcoeffs_sign[9])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF10S', csdcoeffs_sign[10])
            self._ip_reg_write(model, 'CHFCSDCOE01S_SET0CSDCOEFF11S', csdcoeffs_sign[11])
            # Load model variables into local variables
            coeffs = model.vars.channel_filter_coeffs_lock_bwsel.value
            # print(f"CHF Set 1 coefficient values for BW, BWSEL = : {model.vars.bandwidth_hz.value, bwsel}")
            # replace negative numbers with 2s complement
            for i in range(12):
                csdcoeffs[i], csdcoeffs_sign[i] = self.return_csd(coeffs[i], bit_widths[i])
            # TODO: calculate the second set separately
            self._ip_reg_write(model, 'CHFCSDCOE10_SET1CSDCOEFF0', csdcoeffs[0])
            self._ip_reg_write(model, 'CHFCSDCOE10_SET1CSDCOEFF1', csdcoeffs[1])
            self._ip_reg_write(model, 'CHFCSDCOE10_SET1CSDCOEFF2', csdcoeffs[2])
            self._ip_reg_write(model, 'CHFCSDCOE10_SET1CSDCOEFF3', csdcoeffs[3])
            self._ip_reg_write(model, 'CHFCSDCOE11_SET1CSDCOEFF4', csdcoeffs[4])
            self._ip_reg_write(model, 'CHFCSDCOE11_SET1CSDCOEFF5', csdcoeffs[5])
            self._ip_reg_write(model, 'CHFCSDCOE11_SET1CSDCOEFF6', csdcoeffs[6])
            self._ip_reg_write(model, 'CHFCSDCOE12_SET1CSDCOEFF7', csdcoeffs[7])
            self._ip_reg_write(model, 'CHFCSDCOE12_SET1CSDCOEFF8', csdcoeffs[8])
            self._ip_reg_write(model, 'CHFCSDCOE12_SET1CSDCOEFF9', csdcoeffs[9])
            self._ip_reg_write(model, 'CHFCSDCOE13_SET1CSDCOEFF10', csdcoeffs[10])
            self._ip_reg_write(model, 'CHFCSDCOE13_SET1CSDCOEFF11', csdcoeffs[11])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF0S', csdcoeffs_sign[0])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF1S', csdcoeffs_sign[1])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF2S', csdcoeffs_sign[2])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF3S', csdcoeffs_sign[3])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF4S', csdcoeffs_sign[4])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF5S', csdcoeffs_sign[5])
            self._ip_reg_write(model, 'CHFCSDCOE10S_SET1CSDCOEFF6S', csdcoeffs_sign[6])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF7S', csdcoeffs_sign[7])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF8S', csdcoeffs_sign[8])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF9S', csdcoeffs_sign[9])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF10S', csdcoeffs_sign[10])
            self._ip_reg_write(model, 'CHFCSDCOE11S_SET1CSDCOEFF11S', csdcoeffs_sign[11])

    # Method name: return_coeffs
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    #TODO: make this a calc_method and share the channel filter coeff variable with calc_demod
    def return_coeffs(self, bwsel):
        # this table is generated with srw_model/models/channel_filters/gen_channel_filter_coeffs.m
        if bwsel < 0.155:
            coeffs = [-16, -51, -86, -101, -82, -17, 97, 248, 414, 565, 671, 709]
        elif bwsel < 0.165:
            coeffs = [-6, -38, -84, -115, -111, -54, 60, 223, 409, 582, 704, 749]
        elif bwsel < 0.175:
            coeffs = [1, -22, -74, -121, -134, -89, 23, 196, 402, 599, 740, 792]
        elif bwsel < 0.185:
            coeffs = [22, 5, -53, -110, -139, -113, -12, 164, 388, 609, 772, 831]
        elif bwsel < 0.195:
            coeffs = [25, 21, -32, -98, -145, -138, -48, 131, 372, 619, 804, 872]
        elif bwsel < 0.205:
            coeffs = [24, 32, -10, -82, -147, -162, -86, 95, 354, 627, 836, 914]
        elif bwsel < 0.215:
            coeffs = [19, 37, 8, -65, -147, -183, -123, 56, 332, 634, 868, 956]
        elif bwsel < 0.225:
            coeffs = [21, 47, 31, -38, -130, -189, -153, 18, 305, 632, 893, 992]
        elif bwsel < 0.235:
            coeffs = [23, 56, 54, -7, -107, -190, -180, -23, 273, 627, 915, 1026]
        elif bwsel < 0.245:
            coeffs = [24, 67, 83, 36, -67, -171, -190, -51, 251, 632, 951, 1075]
        elif bwsel < 0.255:
            coeffs = [14, 61, 97, 66, -36, -159, -205, -84, 223, 631, 981, 1118]
        elif bwsel < 0.265:
            coeffs = [6, 48, 100, 91, -5, -143, -218, -119, 190, 625, 1007, 1159]
        elif bwsel < 0.275:
            coeffs = [-2, 34, 99, 113, 29, -121, -226, -154, 154, 616, 1033, 1201]
        elif bwsel < 0.285:
            coeffs = [-9, 17, 88, 126, 62, -93, -226, -185, 117, 604, 1058, 1243]
        elif bwsel < 0.295:
            coeffs = [-15, -1, 72, 132, 92, -61, -221, -212, 79, 589, 1081, 1284]
        elif bwsel < 0.305:
            coeffs = [-21, -19, 50, 130, 118, -26, -208, -235, 42, 573, 1102, 1324]
        elif bwsel < 0.315:
            coeffs = [-26, -38, 23, 117, 137, 11, -188, -252, 4, 555, 1125, 1367]
        elif bwsel < 0.325:
            coeffs = [-30, -57, -10, 95, 148, 47, -162, -262, -28, 540, 1150, 1413]
        elif bwsel < 0.335:
            coeffs = [-33, -76, -50, 55, 135, 61, -151, -283, -73, 509, 1160, 1444]
        elif bwsel < 0.345:
            coeffs = [-23, -78, -75, 30, 137, 92, -125, -293, -111, 485, 1178, 1485]
        elif bwsel < 0.355:
            coeffs = [-13, -70, -94, -1, 130, 120, -93, -297, -150, 457, 1195, 1528]
        elif bwsel < 0.365:
            coeffs = [-4, -59, -107, -32, 116, 143, -59, -296, -186, 429, 1211, 1570]
        elif bwsel < 0.375:
            coeffs = [6, -43, -110, -61, 95, 160, -24, -290, -220, 398, 1225, 1611]
        elif bwsel < 0.385:
            coeffs = [15, -24, -108, -88, 68, 170, 11, -279, -251, 366, 1238, 1652]
        elif bwsel < 0.395:
            coeffs = [23, -2, -96, -109, 37, 171, 44, -264, -281, 333, 1249, 1692]
        elif bwsel < 0.405:
            coeffs = [31, 22, -76, -124, 4, 165, 73, -247, -308, 298, 1258, 1731]
        elif bwsel < 0.415:
            coeffs = [39, 51, -42, -124, -28, 153, 98, -231, -339, 255, 1260, 1765]
        elif bwsel < 0.425:
            coeffs = [40, 78, 1, -106, -42, 152, 138, -195, -352, 225, 1275, 1814]
        elif bwsel < 0.435:
            coeffs = [30, 86, 29, -101, -70, 135, 164, -166, -371, 188, 1283, 1854]
        elif bwsel < 0.445:
            coeffs = [20, 86, 58, -87, -97, 112, 188, -133, -387, 148, 1289, 1897]
        elif bwsel < 0.455:
            coeffs = [9, 80, 82, -66, -117, 84, 205, -99, -399, 108, 1293, 1939]
        elif bwsel < 0.465:
            coeffs = [-2, 68, 101, -39, -131, 54, 217, -63, -407, 69, 1296, 1980]
        elif bwsel < 0.475:
            coeffs = [-14, 49, 111, -9, -135, 22, 223, -27, -411, 29, 1297, 2020]
        else:
            coeffs = [-26, 25, 114, 23, -131, -8, 224, 10, -411, -10, 1297, 2060]
        # Confirm Sum of the Magnitudes is in spec to not overflow the
        # filter accumulator
        try:
            assert sum([abs(i) for i in coeffs]) < 2 ** 16
        except AssertionError:
            raise CalculationException('ERROR: Channel Filter Coefficients Sum of Magnitudes >= 2^16')
        return coeffs

    def calc_channel_filer_coeff(self, model):
        bwsel_acq = model.vars.bwsel.value
        bwsel_lock = model.vars.lock_bwsel.value
        model.vars.channel_filter_coeffs_lock_bwsel.value = self.return_coeffs(bwsel_lock)
        model.vars.channel_filter_coeffs_acq_bwsel.value = self.return_coeffs(bwsel_acq)


    # Method name: return_csd
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def return_csd(self, coeff, bitwidth):
        coeff1 = coeff
        sign_bitwidth = ceil(bitwidth / 2)
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

    # Method name: calc_swcoeffen_reg
    # Defined in: lpwh72000\calculators\calc_viterbi.py
    def calc_swcoeffen_reg(self, model):
        afc1shot_en = model.vars.MODEM_AFC_AFCONESHOT.value
        aox_en = model.vars.aox_enable.value == model.vars.aox_enable.var_enum.ENABLED
        if afc1shot_en and aox_en:
            # both AFC oneshot and AoX cannot be simultaneously enabled as they both use the second CHF coefficient set
            LogMgr.Error('both AFC oneshot and AoX cannot be simultaneously enabled')
        swcoeffen = 1 if afc1shot_en or aox_en else 0  # affects the channel filter switching only
        # don't switch for aox, as KSI3 switch mechanism is based on dsa/preamble, but the aox channel switch is based on the CTE
        # Don't care about the demodulated data during CTE, so just leave it on the KSI3
        self._ip_reg_write(model, 'CHFCTRL_SWCOEFFEN', swcoeffen)

    # Method name: calc_aox_misc
    # Defined in: lpwh72000\calculators\calc_aox.py
    def calc_aox_chfsel(self, model):
        aox_enable = True if model.vars.aox_enable.value == model.vars.aox_enable.var_enum.ENABLED else False
        if aox_enable:
            chfswsel = 2  # CHFSWTRIG
        else:
            chfswsel = 0
        self._ip_reg_write(model, 'CHFCTRL_CHFSWSEL', chfswsel)