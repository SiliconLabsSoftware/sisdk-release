from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcAgcMisc(IPCalculator):

    # Inherit everything but registers calculated in V1

    def calc_agc_misc(self, model):
        self._ip_reg_write(model, 'AGCPERIOD0_SETTLETIMEIF',6)
        self._ip_reg_write(model, 'AGCPERIOD0_SETTLETIMERF',14)
        self._ip_reg_write(model, 'AGCPERIOD0_PERIODLOLDFRZ',0)
        self._ip_reg_write(model, 'CTRL0_AGCRST',0)
        self._ip_reg_write(model, 'CTRL0_DISCFLOOPADJ',1)
        self._ip_reg_write(model, 'CTRL0_DISRESETCHPWR',0)
        self._ip_reg_write(model, 'CTRL0_DSADISCFLOOP',0)
        self._ip_reg_write(model, 'CTRL0_DISPNDWNCOMP',0)
        self._ip_reg_write(model, 'CTRL0_DISPNGAINUP',0)
        self._ip_reg_write(model, 'CTRL0_ENRSSIRESET',0)
        self._ip_reg_write(model, 'CTRL1_PWRPERIOD', 1)
        self._ip_reg_write(model, 'CTRL2_DMASEL',0)
        self._ip_reg_write(model, 'CTRL2_PRSDEBUGEN',0)
        self._ip_reg_write(model, 'CTRL2_REHICNTTHD',7)
        self._ip_reg_write(model, 'CTRL2_RELBYCHPWR',3)
        self._ip_reg_write(model, 'CTRL2_RELOTHD',4)
        self._ip_reg_write(model, 'CTRL2_RELTARGETPWR',236)
        self._ip_reg_write(model, 'CTRL2_SAFEMODE',0)
        self._ip_reg_write(model, 'CTRL2_SAFEMODETHD',3)
        self._ip_reg_write(model, 'CTRL3_IFPKDDEB',1)
        self._ip_reg_write(model, 'CTRL3_IFPKDDEBPRD',40)
        self._ip_reg_write(model, 'CTRL3_IFPKDDEBRST',10)
        self._ip_reg_write(model, 'CTRL3_IFPKDDEBTHD',1)
        self._ip_reg_write(model, 'CTRL3_RFPKDDEB',1)
        self._ip_reg_write(model, 'CTRL3_RFPKDDEBPRD',40)
        self._ip_reg_write(model, 'CTRL3_RFPKDDEBRST',10)
        self._ip_reg_write(model, 'CTRL3_RFPKDDEBTHD',1)
        self._ip_reg_write(model, 'CTRL4_PERIODRFPKD',4000)
        self._ip_reg_write(model, 'CTRL4_RFPKDPRDGEAR',4)
        self._ip_reg_write(model, 'CTRL5_PNUPRELTHD',4)
        self._ip_reg_write(model, 'CTRL5_SEQPNUPALLOW',0)
        self._ip_reg_write(model, 'CTRL5_SEQRFPKDEN',0)
        self._ip_reg_write(model, 'GAINRANGE_GAININCSTEP',1)
        self._ip_reg_write(model, 'GAINRANGE_HIPWRTHD',3)
        self._ip_reg_write(model, 'GAINRANGE_LATCHEDHISTEP',0)
        self._ip_reg_write(model, 'GAINSTEPLIM0_MAXPWRVAR',0)
        self._ip_reg_write(model, 'GAINSTEPLIM0_TRANRSTAGC',0)
        self._ip_reg_write(model, 'LBT_CCARSSIPERIOD',0)
        self._ip_reg_write(model, 'LBT_ENCCAGAINREDUCED',0)
        self._ip_reg_write(model, 'LBT_ENCCARSSIMAX',0)
        self._ip_reg_write(model, 'LBT_ENCCARSSIPERIOD',0)
        self._ip_reg_write(model, 'MANGAIN_MANGAINEN',0)
        self._ip_reg_write(model, 'MANGAIN_MANGAINIFPGA',0)
        self._ip_reg_write(model, 'MANGAIN_MANGAINLNA',0)
        self._ip_reg_write(model, 'MANGAIN_MANGAINPN',0)
        self._ip_reg_write(model, 'MANGAIN_MANIFHILATRST',0)
        self._ip_reg_write(model, 'MANGAIN_MANIFLOLATRST',0)
        self._ip_reg_write(model, 'MANGAIN_MANRFLATRST',0)
        # self._ip_reg_write(model, 'PGACODE0_PGAGAIN1',0)
        # self._ip_reg_write(model, 'PGACODE0_PGAGAIN2',1)
        # self._ip_reg_write(model, 'PGACODE0_PGAGAIN3',2)
        # self._ip_reg_write(model, 'PGACODE0_PGAGAIN4',3)
        # self._ip_reg_write(model, 'PGACODE0_PGAGAIN5',4)
        # self._ip_reg_write(model, 'PGACODE0_PGAGAIN6',5)
        # self._ip_reg_write(model, 'PGACODE0_PGAGAIN7',6)
        # self._ip_reg_write(model, 'PGACODE0_PGAGAIN8',7)
        # self._ip_reg_write(model, 'PGACODE1_PGAGAIN9',8)
        # self._ip_reg_write(model, 'PGACODE1_PGAGAIN10',9)
        # self._ip_reg_write(model, 'PGACODE1_PGAGAIN11',10)
        self._ip_reg_write(model, 'RSSISTEPTHR_RSSIFAST',0)
        self._ip_reg_write(model, 'GAINSTEPLIM0_CFLOOPSTEPMAX', 0)
        self._ip_reg_write(model, 'GAINSTEPLIM0_HYST', 0)

        # coming from misc
        # FIXME: figure out how these AGC registers need to be calculated
        self._ip_reg_write(model, 'RSSISTEPTHR_DEMODRESTARTPER', 0)
        self._ip_reg_write(model, 'RSSISTEPTHR_DEMODRESTARTTHR', 0)
        self._ip_reg_write(model, 'RSSISTEPTHR_NEGSTEPTHR', 0)
        self._ip_reg_write(model, 'RSSISTEPTHR_POSSTEPTHR', 0)
        self._ip_reg_write(model, 'RSSISTEPTHR_STEPPER', 0)

    # Method name: calc_ook_rssi_offset
    # Defined in: nixi\calculators\calc_misc.py
    def calc_ook_rssi_offset(self, model):
        # OOK RSSI offset measured experimentally for Nixi
        model.vars.ook_rssi_offset.value = 16

    pass