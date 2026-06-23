from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException

class CalcHadmMisc(IPCalculator):

    def calc_hadm_enable_default(self, model):
        # define hadm_enable as false by default
       model.vars.hadm_enable.value = model.vars.hadm_enable.var_enum.DISABLED

    def calc_hadm_do_not_care(self, model):
        hadm_enable = model.vars.hadm_enable.value
        if hadm_enable == model.vars.hadm_enable.var_enum.DISABLED:
            model.vars.hadm_do_not_care.value = True
        else:
            model.vars.hadm_do_not_care.value = False

    def calc_hadm_trecsosr(self, model):

        osr = model.vars.oversampling_rate_actual.value
        hadm_do_not_care =  model.vars.hadm_do_not_care.value

        if osr == 4:
            reg = 0
        else:
            reg = 1

        self._ip_reg_write(model, 'RTTCTRL1_TRECSOSR', reg, do_not_care=hadm_do_not_care)

    def calc_hadm_xosel(self, model):

        xtal = model.vars.xtal_frequency_hz.value
        hadm_do_not_care = model.vars.hadm_do_not_care.value

        if xtal == 38e6:
            xosel = 0
        elif xtal == 38.4e6:
            xosel = 1
        elif xtal == 39e6:
            xosel = 2
        elif xtal == 40e6:
            xosel = 3
        else:
            raise CalculationException('ERROR: unknown value for xtal frequency in calc_hadm_xosel')

        self._ip_reg_write(model, 'RTTCTRL1_XOSEL', xosel, do_not_care=hadm_do_not_care)

    def calc_hadm_misc(self, model):
        hadm_do_not_care = model.vars.hadm_do_not_care.value

        self._ip_reg_write(model, 'CTRL0_ROLE',0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'CTRL0_PHYSEL',0, do_not_care=hadm_do_not_care)  # set correctly in PHY definition of 1M, 2M and 2M2BT HADM PHY
        self._ip_reg_write(model, 'CTRL0_SSAFCGEAR',0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'CTRL0_TXUPSAMPOSR4',0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'CTRL0_TGUARDPERIOD',4, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'CTRL0_AVGSTARTOFF',10 , do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'CTRL0_OWRRSTDLO',0 , do_not_care=hadm_do_not_care)

        self._ip_reg_write(model, 'RTTCTRL0_RTTMODE',3, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL0_RTTLEN',8, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL0_PESEN',1, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL0_SNDSEQEN',1, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL0_PKTSENTSEL',1, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL0_DFTSCALE',3, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL0_RBSTRACKNUM',3, do_not_care=hadm_do_not_care)        
        self._ip_reg_write(model, 'RTTCTRL0_RTTTIMEOUT',3, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL0_MAXSCHWIN',4, do_not_care=hadm_do_not_care)

        self._ip_reg_write(model, 'RTTCTRL1_FRAMEDETSEL', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL1_FRAMEDETTIMEOUT', 8, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL1_SBFLIPEN', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL1_EPLBWREN', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL1_SSPMSWAPEN', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL1_ELSWAPEN', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL1_CORRACCDLY', 4, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL1_SSDFTEN', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL1_TIMEROWEN', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL1_FBROCEN', 0, do_not_care=hadm_do_not_care)

        self._ip_reg_write(model, 'RTTCTRL2_FBROCMUL2EN', 1, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL2_TIMERDETSEL', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL2_FLIPEPL1EN', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL2_FLIPEPL2EN', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL2_SINGLEPKTMODEEN', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTCTRL2_SSFFOLEN', 0, do_not_care=hadm_do_not_care)

        self._ip_reg_write(model, 'RTTTUNE_RTTINITTUNE',0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTTUNE_RTTREFLTUNE',0, do_not_care=hadm_do_not_care)

        self._ip_reg_write(model, 'RTTRPTTIME0_REFBACKSYMB',8, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTRPTTIME0_REFBACKCYCLE',0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTRPTTIME0_GROUPDLY',0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTRPTTIME0_RTTTIP1IDX',7, do_not_care=hadm_do_not_care)

        self._ip_reg_write(model, 'RTTRPTTIME1_FFO',0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTRPTTIME1_COARSETIMEOW',12900, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTRPTTIME1_SSFFONEG', 0, do_not_care=hadm_do_not_care)

        self._ip_reg_write(model, 'RTTPKT0_RTTPAYLOAD0',32, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTPKT1_RTTPAYLOAD1',32, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTPKT2_RTTPAYLOAD2',32, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'RTTPKT3_RTTPAYLOAD3',32, do_not_care=hadm_do_not_care)

        # kulee: hard coding the following NADM values
        self._ip_reg_write(model, 'NADMCONFIG_NADMDIFFD', 1, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'NADMCONFIG_REFMAPFSK', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'NADMCONFIG_SNRNUMFASTSAMPLES', 3, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'NADMCONFIG_SNRFASTCOEFF', 4, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'NADMCONFIG_SNRSLOWCOEFF', 6, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'DFTAMFREQ_DFTAMFREQ', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'DFTECLDFREQ_DFTECLDFREQ', 0, do_not_care=hadm_do_not_care)

    def calc_nadm_recrewindsamples(self, model):
        # This is chip-specific and must be overridden for every IC (based on FEFILT)
        hadm_do_not_care = model.vars.hadm_do_not_care.value
        self._ip_reg_write(model, 'NADMCONFIG_RECREWINDSAMPLES', 135, do_not_care=hadm_do_not_care)

    def calc_rtt_ramaddrback(self, model):
        hadm_do_not_care = model.vars.hadm_do_not_care.value
        self._ip_reg_write(model, 'RTTCTRL1_RAMRADDRBACK', 129, do_not_care=hadm_do_not_care)

    def calc_rtt_src(self, model):
        hadm_do_not_care = model.vars.hadm_do_not_care.value
        xo_sel = model.vars.HADM_RTTCTRL1_XOSEL.value
        phy_sel = model.vars.HADM_CTRL0_PHYSEL.value

        if (phy_sel==0):
            self._ip_reg_write(model, 'RTTCTRL0_DFTSTARTOFF', 3, do_not_care=hadm_do_not_care)
            self._ip_reg_write(model, 'RTTCTRL2_SRCCOMPSAMPSKIPEN', 0, do_not_care=hadm_do_not_care)
            self._ip_reg_write(model, 'RTTCTRL2_SRCMUREFBACK', 0, do_not_care=hadm_do_not_care)
        else:
            self._ip_reg_write(model, 'RTTCTRL0_DFTSTARTOFF', 5, do_not_care=hadm_do_not_care)
            self._ip_reg_write(model, 'RTTCTRL2_SRCCOMPSAMPSKIPEN', 1, do_not_care=hadm_do_not_care)
            self._ip_reg_write(model, 'RTTCTRL2_SRCMUREFBACK', 1, do_not_care=hadm_do_not_care)

    def calc_refgencoeff(self, model):
        hadm_do_not_care = model.vars.hadm_do_not_care.value
        # TODO: implement with ip_read
        xo_sel = model.vars.HADM_RTTCTRL1_XOSEL.value
        # | XOSEL   | xtal_freq
        # | 0       | 38MHz
        # | 1       | 38.4MHz
        # | 2       | 39MHz
        # | 3       | 40MHz
        phy_sel = model.vars.HADM_CTRL0_PHYSEL.value
        # | PHYSEL  | HADM PHY
        # | 0       | 1M
        # | 1       | 2M
        # | 2       | 2M, BT = 2

        refgencoeff_settings_LUT = {
            # Format: REFGENCOEFFx[PHYSEL][XOSEL]
            # for PHYSEL :   [     0                   ,      1                   ,      2                  ]
            # for XOSEL :    [     0,    1,    2,    3], [    0,    1,    2,    3], [    0,    1,    2,    3]
            'REFGENCOEFF0':  [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF1':  [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF2':  [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF3':  [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF4':  [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF5':  [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF6':  [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF7':  [[   18,   24,  -17,   78], [   -6,    4,   -5,   37], [   -4,  -10,   21,   47]],
            'REFGENCOEFF8':  [[   31,   39,   33,   61], [   24,   25,   22,   90], [   20,   19,   38,  110]],
            'REFGENCOEFF9':  [[   17,   27,   39,   -1], [   52,   62,   36,   74], [   42,   49,   28,   58]],
            'REFGENCOEFF10': [[   91,   94,  103,   55], [   89,   85,   83,   37], [   20,   15,   87,  -69]],
            'REFGENCOEFF11': [[  570,  558,  593,  532], [  576,  678,  493,  527], [    3,   34,  -86,  -74]],
            'REFGENCOEFF12': [[ 1868, 1901, 1985, 1933], [ 1959, 1980, 1807, 1956], [ 1018, 1027, 1036, 1036]],
            'REFGENCOEFF13': [[ 4111, 4170, 4290, 4210], [ 4270, 4324, 4159, 4307], [ 4325, 4485, 4578, 4546]],
            'REFGENCOEFF14': [[ 6230, 6285, 6354, 6253], [ 6367, 6378, 6262, 6350], [ 7258, 7281, 7285, 7329]],
            'REFGENCOEFF15': [[ 7028, 7056, 7023, 6977], [ 7118, 7118, 7071, 7105], [ 8062, 8112, 8263, 8032]],
            'REFGENCOEFF16': [[ 6060, 5972, 5907, 5968], [ 6092, 6027, 6043, 6052], [ 7128, 7057, 7183, 7069]],
            'REFGENCOEFF17': [[ 3919, 3820, 3712, 3792], [ 3785, 3716, 3827, 3701], [ 3762, 3593, 3699, 3524]],
            'REFGENCOEFF18': [[ 1761, 1698, 1602, 1668], [ 1575, 1587, 1589, 1503], [  761,  770,  764,  589]],
            'REFGENCOEFF19': [[  512,  466,  453,  449], [  397,  341,  396,  377], [   11,  -24,    7,   -3]],
            'REFGENCOEFF20': [[  115,  102,  132,   92], [   91,  107,   81,  115], [  -12,    9,    1,   29]],
            'REFGENCOEFF21': [[   64,   58,   77,   -1], [   90,   82,   87,   38], [   53,   60,   60,   33]],
            'REFGENCOEFF22': [[   86,   77,   81,  -14], [   84,   62,   64,  -35], [   94,   70,   86,  -38]],
            'REFGENCOEFF23': [[   81,   76,   82,  -20], [   87,  104,  120,  -21], [  133,  132,  152,   -6]],
            'REFGENCOEFF24': [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF25': [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF26': [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF27': [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF28': [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF29': [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF30': [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
            'REFGENCOEFF31': [[    0,    0,    0,    0], [    0,    0,    0,    0], [    0,    0,    0,    0]],
        }



        self._ip_reg_write(model, 'REFGENCOEFFG0_REFGENCOEFF0', refgencoeff_settings_LUT['REFGENCOEFF0'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG0_REFGENCOEFF1', refgencoeff_settings_LUT['REFGENCOEFF1'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG1_REFGENCOEFF2', refgencoeff_settings_LUT['REFGENCOEFF2'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG1_REFGENCOEFF3', refgencoeff_settings_LUT['REFGENCOEFF3'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG2_REFGENCOEFF4', refgencoeff_settings_LUT['REFGENCOEFF4'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG2_REFGENCOEFF5', refgencoeff_settings_LUT['REFGENCOEFF5'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG3_REFGENCOEFF6', refgencoeff_settings_LUT['REFGENCOEFF6'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG3_REFGENCOEFF7', refgencoeff_settings_LUT['REFGENCOEFF7'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG4_REFGENCOEFF8', refgencoeff_settings_LUT['REFGENCOEFF8'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG4_REFGENCOEFF9', refgencoeff_settings_LUT['REFGENCOEFF9'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG5_REFGENCOEFF10', refgencoeff_settings_LUT['REFGENCOEFF10'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG5_REFGENCOEFF11', refgencoeff_settings_LUT['REFGENCOEFF11'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG6_REFGENCOEFF12', refgencoeff_settings_LUT['REFGENCOEFF12'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG6_REFGENCOEFF13', refgencoeff_settings_LUT['REFGENCOEFF13'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG7_REFGENCOEFF14', refgencoeff_settings_LUT['REFGENCOEFF14'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG7_REFGENCOEFF15', refgencoeff_settings_LUT['REFGENCOEFF15'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG8_REFGENCOEFF16', refgencoeff_settings_LUT['REFGENCOEFF16'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG8_REFGENCOEFF17', refgencoeff_settings_LUT['REFGENCOEFF17'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG9_REFGENCOEFF18', refgencoeff_settings_LUT['REFGENCOEFF18'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG9_REFGENCOEFF19', refgencoeff_settings_LUT['REFGENCOEFF19'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG10_REFGENCOEFF20', refgencoeff_settings_LUT['REFGENCOEFF20'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG10_REFGENCOEFF21', refgencoeff_settings_LUT['REFGENCOEFF21'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG11_REFGENCOEFF22', refgencoeff_settings_LUT['REFGENCOEFF22'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG11_REFGENCOEFF23', refgencoeff_settings_LUT['REFGENCOEFF23'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG12_REFGENCOEFF24', refgencoeff_settings_LUT['REFGENCOEFF24'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG12_REFGENCOEFF25', refgencoeff_settings_LUT['REFGENCOEFF25'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG13_REFGENCOEFF26', refgencoeff_settings_LUT['REFGENCOEFF26'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG13_REFGENCOEFF27', refgencoeff_settings_LUT['REFGENCOEFF27'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG14_REFGENCOEFF28', refgencoeff_settings_LUT['REFGENCOEFF28'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG14_REFGENCOEFF29', refgencoeff_settings_LUT['REFGENCOEFF29'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG15_REFGENCOEFF30', refgencoeff_settings_LUT['REFGENCOEFF30'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'REFGENCOEFFG15_REFGENCOEFF31', refgencoeff_settings_LUT['REFGENCOEFF31'][phy_sel][xo_sel], allow_neg=True, do_not_care=hadm_do_not_care)
