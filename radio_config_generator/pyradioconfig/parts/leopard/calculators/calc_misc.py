from pyradioconfig.parts.lynx.calculators.calc_misc import CALC_Misc_lynx

class calc_misc_leopard(CALC_Misc_lynx):

    def calc_lnamixlowcur_reg(self, model):
        #This field is now programmed by PTE and so don't set it in the Radio Configurator
        pass

    def calc_misc_ifadcenhalfmode(self, model):
        #This calculation is moved to calc_synth for Leopard
        pass

    def calc_misc_sylodivrloadcclksel(self, model):
        # This calculation is moved to calc_synth for Leopard
        pass

    def calc_misc_bbssdebouncetim(self, model):
        #Now moved to calc_demodulator as this is used for log2x4 for A1
        pass

    def calc_misc_Lynx(self, model):
        # Omitting writes to CLKMULT regs in calc_misc_leopard
        pass

    def calc_misc_Leopard(self, model):
        """
        These aren't really calculating right now.  Just using defaults or forced values.
        Specifically registers that are not handled in inherited CALC_Misc_panther

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        # All of the registers here are new in Lynx (and are read-write; read-only and write-only are omitted)
        # Many IF, IEN, and RAC registers are intentionally ommitted

        #AGC default values are located in calc_agc.py and the calc_agc_misc() function

        self._reg_write(model.vars.FRC_DFLCTRL_DFLBOIOFFSET, 0)
        self._reg_write(model.vars.FRC_CTRL_WAITEOFEN, 0)
        self._reg_write(model.vars.FRC_TRAILTXDATACTRL_TRAILTXREPLEN, 0)
        self._reg_write(model.vars.FRC_TRAILTXDATACTRL_TXSUPPLENOVERIDE, 0)
        self._reg_write(model.vars.FRC_WCNTCMP3_SUPPLENFIELDLOC, 0)
        self._reg_write(model.vars.FRC_BOICTRL_BOIEN, 0)
        self._reg_write(model.vars.FRC_BOICTRL_BOIFIELDLOC, 0)
        self._reg_write(model.vars.FRC_BOICTRL_BOIBITPOS, 0)
        self._reg_write(model.vars.FRC_BOICTRL_BOIMATCHVAL, 0)
        self._reg_write(model.vars.FRC_DSLCTRL_DSLMODE, 0)
        self._reg_write(model.vars.FRC_DSLCTRL_DSLBITORDER, 0)
        self._reg_write(model.vars.FRC_DSLCTRL_DSLSHIFT, 0)
        self._reg_write(model.vars.FRC_DSLCTRL_DSLOFFSET, 0)
        self._reg_write(model.vars.FRC_DSLCTRL_DSLBITS, 0)
        self._reg_write(model.vars.FRC_DSLCTRL_DSLMINLENGTH, 0)
        self._reg_write(model.vars.FRC_DSLCTRL_RXSUPRECEPMODE, 0)
        self._reg_write(model.vars.FRC_DSLCTRL_STORESUP, 0)
        self._reg_write(model.vars.FRC_DSLCTRL_SUPSHFFACTOR, 0)
        self._reg_write(model.vars.FRC_WCNTCMP4_SUPPLENGTH, 0)
        self._reg_write(model.vars.MODEM_DIGMIXCTRL_DIGMIXFB, 0)
        self._reg_write(model.vars.MODEM_VTTRACK_SYNCTIMEOUTSEL, 1)
        self._reg_write(model.vars.MODEM_LRFRC_LRCORRMODE, 1)
        self._reg_write(model.vars.MODEM_ETSCTRL_ETSLOC, 0)
        self._reg_write(model.vars.MODEM_ETSCTRL_CAPTRIG, 0)
        self._reg_write(model.vars.MODEM_ANTSWCTRL_ANTDFLTSEL, 0)
        self._reg_write(model.vars.MODEM_ANTSWCTRL_ANTCOUNT, 0)
        self._reg_write(model.vars.MODEM_ANTSWCTRL_ANTSWTYPE, 0)
        self._reg_write(model.vars.MODEM_ANTSWCTRL_CFGANTPATTEN, 0)
        self._reg_write(model.vars.MODEM_ANTSWCTRL_ANTSWENABLE, 0)
        self._reg_write(model.vars.MODEM_ANTSWCTRL_EXTDSTOPPULSECNT, 30)
        self._reg_write(model.vars.MODEM_ANTSWSTART_ANTSWSTARTTIM, 0)
        self._reg_write(model.vars.MODEM_ANTSWEND_ANTSWENDTIM, 0)
        self._reg_write(model.vars.MODEM_CFGANTPATT_CFGANTPATTVAL, 0)
        self._reg_write(model.vars.MODEM_ETSTIM_ETSTIMVAL, 0)
        self._reg_write(model.vars.MODEM_ETSTIM_ETSCOUNTEREN, 0)
        self._reg_write(model.vars.MODEM_ANTSWCTRL1_TIMEPERIOD, 436906)
        self._reg_write(model.vars.MODEM_COCURRMODE_CONCURRENT, 0)
        self._reg_write(model.vars.MODEM_ANTDIVCTRL_ADPRETHRESH, 0)
        self._reg_write(model.vars.MODEM_ANTDIVCTRL_ENADPRETHRESH, 0)
        self._reg_write(model.vars.MODEM_BLEIQDSAEXT2_DISMAXPEAKTRACKMODE, 0)
        self._reg_write(model.vars.MODEM_BLEIQDSAEXT2_BBSSDIFFCHVAL, 0)
        self._reg_write(model.vars.RAC_LNAMIXDEBUG_LNAMIXDISMXR, 0)
        self._reg_write(model.vars.RAC_LNAMIXTRIM0_LNAMIXRFPKDBWSEL, 2)
        self._reg_write(model.vars.RAC_LNAMIXTRIM0_LNAMIXRFPKDCALDM, 16)
        self._reg_write(model.vars.RAC_LNAMIXTRIM0_LNAMIXTRIMVREG, 8)
        self._reg_write(model.vars.RAC_LNAMIXTRIM1_LNAMIXLNACAPSEL, 0)
        self._reg_write(model.vars.RAC_LNAMIXTRIM1_LNAMIXMXRBIAS, 2)
        self._reg_write(model.vars.RAC_LNAMIXTRIM1_LNAMIXNCASADJ, 2)
        self._reg_write(model.vars.RAC_LNAMIXTRIM1_LNAMIXPCASADJ, 2)
        self._reg_write(model.vars.RAC_LNAMIXTRIM1_LNAMIXVOUTADJ, 8)
        self._reg_write(model.vars.RAC_PGACTRL_PGABWMODE, 0)
        self._reg_write(model.vars.RAC_SYTRIM1_SYLODIVSGTESTDIV, 0)
        self._reg_write(model.vars.RAC_SYMMDCTRL_SYMMDMODE, 2)
        self._reg_write(model.vars.RAC_SYNTHCTRL_MMDPOWERBALANCEDISABLE, 1)
        self._reg_write(model.vars.RAC_SYNTHREGCTRL_MMDLDOVREFTRIM, 3)
        self._reg_write_default(model.vars.RAC_IFADCTRIM0_IFADCSIDETONEAMP)
        self._reg_write_default(model.vars.FRC_AUTOCG_AUTOCGEN)

        #Fairly confident that these CAL values are not actually used, but can not modify validated PHYs
        #at this point and Design can not confirm these are unused. So if the value isn't forced then these
        #are a do not care.
        if model.vars.SYNTH_LPFCTRL1CAL_OP1BWCAL.value_forced is None:
            self._reg_do_not_care(model.vars.SYNTH_LPFCTRL1CAL_OP1BWCAL)
        if model.vars.SYNTH_LPFCTRL1CAL_OP1COMPCAL.value_forced is None:
            self._reg_do_not_care(model.vars.SYNTH_LPFCTRL1CAL_OP1COMPCAL)
        if model.vars.SYNTH_LPFCTRL1CAL_RZVALCAL.value_forced is None:
            self._reg_do_not_care(model.vars.SYNTH_LPFCTRL1CAL_RZVALCAL)
        if model.vars.SYNTH_LPFCTRL1CAL_RPVALCAL.value_forced is None:
            self._reg_do_not_care(model.vars.SYNTH_LPFCTRL1CAL_RPVALCAL)
        if model.vars.SYNTH_LPFCTRL1CAL_RFBVALCAL.value_forced is None:
            self._reg_do_not_care(model.vars.SYNTH_LPFCTRL1CAL_RFBVALCAL)