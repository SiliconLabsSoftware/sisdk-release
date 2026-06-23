from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcEnhanced(IPCalculator):

    def calc_ehdsssen_reg(self, model):
        demod_select = model.vars.demod_select.value

        if demod_select == model.vars.demod_select.var_enum.ENHANCED_DSSS:
            ehdsssen = 1
        else:
            ehdsssen = 0

        self._ip_reg_write(model, 'EHDSSSCTRL_EHDSSSEN', ehdsssen)

    def calc_enhanced_misc(self, model):
        do_not_care = model.vars.MODEM_EHDSSSCTRL_EHDSSSEN.value == 0

        self._ip_reg_write(model, 'EHDSSSCTRL_DSSSTIMEACQUTHD', 16)
        self._ip_reg_write(model, 'EHDSSSCTRL_FOEBIAS', 1)
        self._ip_reg_write(model, 'EHDSSSCTRL_FREQCORREN', 1)
        self._ip_reg_write(model, 'EHDSSSCTRL_DSSSFRQLIM', 16)
        self._ip_reg_write(model, 'EHDSSSCFG0_DSSSPATT', 122)
        self._ip_reg_write(model, 'EHDSSSCFG1_DSSSEXPSYNCLEN', 128)
        self._ip_reg_write(model, 'EHDSSSCFG1_DSSSCORRTHD', 400)
        self._ip_reg_write(model, 'EHDSSSCFG1_DSSSDSAQTHD', 700)
        self._ip_reg_write(model, 'EHDSSSCFG2_DSSSTIMCORRTHD', 600)
        self._ip_reg_write(model, 'EHDSSSCFG2_DSSSFRTCORRTHD', 700)
        self._ip_reg_write(model, 'EHDSSSCFG2_DSSSTRACKINGWIN', 5)
        self._ip_reg_write(model, 'EHDSSSCFG2_DSSSCORRSCHWIN', 8)
        self._ip_reg_write(model, 'EHDSSSCFG2_ONESYMBOLMBDD', 1)

        self._ip_reg_write(model, 'EHDSSSCTRL_DSSSDSATHD', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'EHDSSSCTRL_DUALDSA', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'EHDSSSCFG2_MAXSCHMODE', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'EHDSSSCFG2_DSSSDSAQUALEN', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'EHDSSSCFG3_DSSSDASMAXTHD', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'EHDSSSCFG3_DSSSFOETRACKGEAR', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'EHDSSSCFG3_OPMODE', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'EHDSSSCFG3_DSSSINITIMLEN', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'EHDSSSCFG3_LQIAVGWIN', default=True, do_not_care=do_not_care)

        self._ip_reg_write(model, 'EHDSSSCTRL_DSSSPMTIMEOUT', default=True)
        self._ip_reg_write(model, 'EHDSSSCTRL_DSSSFRMTIMEOUT', default=True)

    def calc_si_misc(self, model):
        do_not_care = model.vars.MODEM_EHDSSSCTRL_EHDSSSEN.value == 0

        # Set the following to POR values for now when Enhanced demod is selected, otherwise don't care
        self._ip_reg_write(model, 'SICTRL0_SIMODE', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL0_NOISETHRESH', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL0_PEAKNUMTHRESHLW', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL0_PEAKNUMADJ', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL0_NOISETHRESHADJ', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL0_FREQNOMINAL', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL0_SYMIDENTDIS', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_SUPERCHIPTOLERANCE', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_SMALLSAMPLETHRESH', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_PEAKNUMP2ADJ', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_FASTMODE', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_TWOSYMBEN', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_ZCEN', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_ZCSAMPLETHRESH', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_SOFTCLIPBYPASS', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_SOFTCLIPTHRESH', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_SIRSTAGCMODE', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_SIRSTPRSMODE', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_SIRSTCCAMODE', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_DISSIFRAMEDET', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_AGCRSTUPONSI', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_SHFTWIN', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_SUPERCHIPNUM', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_CORRNUM', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_NARROWPULSETHRESH', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_PEAKNUMADJEN', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICORR_CORRTHRESH', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICORR_CORRTHRESHLOW', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICORR_CORRTHRESHUP', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICORR_CORRTHRESH2SYMB', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL1_FREQOFFTOLERANCE', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_SISTARTDELAY', default=True, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SICTRL2_SISTARTDELAYMODE', default=True, do_not_care=do_not_care)