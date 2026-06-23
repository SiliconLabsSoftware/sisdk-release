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

        self._ip_reg_write(model, 'RTTCTRL1_RAMRADDRBACK', 137, do_not_care=hadm_do_not_care)
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
        self._ip_reg_write(model, 'NADMCONFIG_RECREWINDSAMPLES', 132, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'NADMCONFIG_REFMAPFSK', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'NADMCONFIG_SNRNUMFASTSAMPLES', 3, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'NADMCONFIG_SNRFASTCOEFF', 4, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'NADMCONFIG_SNRSLOWCOEFF', 6, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'DFTAMFREQ_DFTAMFREQ', 0, do_not_care=hadm_do_not_care)
        self._ip_reg_write(model, 'DFTECLDFREQ_DFTECLDFREQ', 0, do_not_care=hadm_do_not_care)

    def calc_rtt_src(self, model):
        hadm_do_not_care = model.vars.hadm_do_not_care.value
        xo_sel = model.vars.HADM_RTTCTRL1_XOSEL.value
        phy_sel = model.vars.HADM_CTRL0_PHYSEL.value
        if (phy_sel==0):
            self._ip_reg_write(model, 'RTTCTRL0_DFTSTARTOFF', 8, do_not_care=hadm_do_not_care)
            self._ip_reg_write(model, 'RTTCTRL2_SRCMUREFBACK', 1, do_not_care=hadm_do_not_care)
        else:
            self._ip_reg_write(model, 'RTTCTRL0_DFTSTARTOFF', 7, do_not_care=hadm_do_not_care)
            self._ip_reg_write(model, 'RTTCTRL2_SRCMUREFBACK', 2, do_not_care=hadm_do_not_care)

        if (xo_sel!=3 and phy_sel!=0):
            # only enable for non-40MHz XO and non-1MHz PHY
            self._ip_reg_write(model, 'RTTCTRL2_SRCCOMPSAMPSKIPEN', 1, do_not_care=hadm_do_not_care)
        else:
            self._ip_reg_write(model, 'RTTCTRL2_SRCCOMPSAMPSKIPEN', 0, do_not_care=hadm_do_not_care)

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
            'REFGENCOEFF7':  [[   -3,   11,  -26,   26], [   14,   -1,  -26,   26], [   20,    6,  -12,   62]],
            'REFGENCOEFF8':  [[   11,   39,   37,   49], [   -2,   35,   37,   49], [    4,   24,   15,   12]],
            'REFGENCOEFF9':  [[    3,   20,   52,   27], [  -34,   25,   52,   27], [   -3,   58,   64,   55]],
            'REFGENCOEFF10': [[   83,  112,  112,   67], [  109,  124,  112,   67], [   33,   34,   37, -147]],
            'REFGENCOEFF11': [[  561,  563,  648,  542], [  620,  628,  648,  542], [   21,  -47,  -87, -247]],
            'REFGENCOEFF12': [[ 1885, 1876, 2070, 1866], [ 1918, 1986, 2070, 1866], [ 1138, 1160, 1107, 1290]],
            'REFGENCOEFF13': [[ 4127, 4097, 4365, 4131], [ 4174, 4285, 4365, 4131], [ 4231, 4346, 4236, 4446]],
            'REFGENCOEFF14': [[ 6220, 6178, 6373, 6224], [ 6281, 6381, 6373, 6224], [ 7216, 7282, 7169, 7207]],
            'REFGENCOEFF15': [[ 7003, 6967, 7039, 7002], [ 7061, 7182, 7039, 7002], [ 8324, 8378, 8384, 8232]],
            'REFGENCOEFF16': [[ 6051, 5937, 5898, 6074], [ 6025, 6116, 5898, 6074], [ 6978, 6974, 7042, 6926]],
            'REFGENCOEFF17': [[ 3909, 3792, 3659, 3892], [ 3791, 3799, 3659, 3892], [ 3747, 3649, 3699, 3852]],
            'REFGENCOEFF18': [[ 1748, 1678, 1554, 1742], [ 1611, 1588, 1554, 1742], [  885,  801,  887,  883]],
            'REFGENCOEFF19': [[  501,  484,  432,  467], [  402,  407,  432,  467], [  -45,  -48,    7, -288]],
            'REFGENCOEFF20': [[  113,  137,  136,   67], [   45,   78,  136,   67], [  -38,   -8,  -71, -130]],
            'REFGENCOEFF21': [[   78,   61,   62,   30], [   33,   57,   62,   30], [    6,   36,  -30,  101]],
            'REFGENCOEFF22': [[  103,   84,   39,  -15], [   79,   93,   39,  -15], [  104,  126,  126,  113]],
            'REFGENCOEFF23': [[   96,   82,   75,   18], [   83,   95,   75,   18], [  132,  150,  167,   -2]],
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
