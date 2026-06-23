from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from math import floor, log2, ceil
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException

class CalcFefiltMisc(IPCalculator):
    def calc_enable_rcos_reg(self, model):
        rcosen = 0
        if model.vars.protocol_id.value == model.vars.protocol_id.var_enum.BTC:
            rcosen = 1

        self._ip_reg_write(model, 'CHFCTRL_ENABLERCOS', rcosen, limit_lower=0, limit_upper=1)

    # kulee: For now, NADM uses maximum possible bandwidth, corresponding to
    # all pass filter. Only the center tap is used, 2047 in 12.11 format is
    # 2047/2^11 ~ 1.0 and 2047 in CSD format is {2049,1}. For non-HADM PHYs,
    # the second CHF is turned off it doesn't matter what we do here.
    def calc_hadm_nadm_second_chf(self, model):
        self._ip_reg_write(model, 'CHFCSDCOE00_NADM_SET0CSDCOEFF0_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE00_NADM_SET0CSDCOEFF1_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE00_NADM_SET0CSDCOEFF2_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE00_NADM_SET0CSDCOEFF3_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE01_NADM_SET0CSDCOEFF4_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE01_NADM_SET0CSDCOEFF5_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE01_NADM_SET0CSDCOEFF6_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE02_NADM_SET0CSDCOEFF7_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE02_NADM_SET0CSDCOEFF8_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE02_NADM_SET0CSDCOEFF9_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE03_NADM_SET0CSDCOEFF10_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE03_NADM_SET0CSDCOEFF11_NADM', 2049)
        self._ip_reg_write(model, 'CHFCSDCOE00S_NADM_SET0CSDCOEFF0S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE00S_NADM_SET0CSDCOEFF1S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE00S_NADM_SET0CSDCOEFF2S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE00S_NADM_SET0CSDCOEFF3S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE00S_NADM_SET0CSDCOEFF4S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE00S_NADM_SET0CSDCOEFF5S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE00S_NADM_SET0CSDCOEFF6S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE01S_NADM_SET0CSDCOEFF7S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE01S_NADM_SET0CSDCOEFF8S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE01S_NADM_SET0CSDCOEFF9S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE01S_NADM_SET0CSDCOEFF10S_NADM', 0)
        self._ip_reg_write(model, 'CHFCSDCOE01S_NADM_SET0CSDCOEFF11S_NADM', 1)

    def calc_log2x4fwsel_reg(self, model):
        # set to use LOG2X4 register value for log2 calculation in DEC1 rather than HW calculation
        self._ip_reg_write(model, 'LOG2X4_LOG2X4FWSEL', 1)

    def calc_log2x4_reg(self, model):
        # given DEC1 decimation ratio calculate log2 in 4Q2 format
        dec1 = model.vars.dec1_actual.value

        val = floor(4.0*log2(dec1))

        self._ip_reg_write(model, 'LOG2X4_LOG2X4', val)

    def calc_fefilt_misc(self, model):
        # Digital Gain Control
        self._ip_reg_write(model, 'DIGIGAINCTRL_DEC0GAIN', 0)
        self._ip_reg_write(model, 'DIGIGAINCTRL_DIGIGAINDOUBLE', 0)
        self._ip_reg_write(model, 'DIGIGAINCTRL_DIGIGAINEN', 0)
        self._ip_reg_write(model, 'DIGIGAINCTRL_DIGIGAINHALF', 0)
        self._ip_reg_write(model, 'DIGIGAINCTRL_DIGIGAINSEL', 0)
        #
        self._ip_reg_write(model, 'CHFCTRL_FWSELCOEFF', 0)
        self._ip_reg_write(model, 'CHFCTRL_FWSWCOEFFEN', 0)
        ## New registers
        # FIXME: how to calculate these?

        self._ip_reg_write(model, 'CHFCTRL_CHFGAINREDUCTION', 0)
        #self._ip_reg_write(model, 'CHFLATENCYCTRL_CHFLATENCY', 0)
        # self._ip_reg_write(model, 'DIGMIXCTRL_DIGMIXMODE', 1)
        self._ip_reg_write(model, 'DIGMIXCTRL_DIGMIXFB', 1)
        self._ip_reg_write(model, 'DCCOMPFILTINIT_DCCOMPINIT', 0)
        self._ip_reg_write(model, 'DCCOMPFILTINIT_DCCOMPINITVALI', 0)
        self._ip_reg_write(model, 'DCCOMPFILTINIT_DCCOMPINITVALQ', 0)

    # Method name: calc_synchronous_ifadc_clk
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_synchronous_ifadc_clk(self, model):
        # default to disabled, only HADM PHYs will set the profile input
        model.vars.synchronous_ifadc_clk.value = False

    # Method name: calc_synchronous_ifadc_clk_regs
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_synchronous_ifadc_clk_regs(self, model):
        if not model.vars.synchronous_ifadc_clk.value:
            # normal async front filtering
            self._ip_reg_write(model, 'CTRL0_FEFILTCLKSEL', 0)
            self._ip_reg_write(model, 'CTRL0_AFIFOBYP', 0)
        else:
            self._ip_reg_write(model, 'CTRL0_FEFILTCLKSEL', 1)
            self._ip_reg_write(model, 'CTRL0_AFIFOBYP', 1)