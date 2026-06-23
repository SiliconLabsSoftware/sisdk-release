from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator

class CalcBlehdtMisc(IPCalculator):

    def calc_set_hdt_enable(self, model):
        demod_select = model.vars.demod_select.value

        # HDT disabled by default
        self._ip_reg_write(model, 'HDTCFG_HDTENABLE', 0)
        if demod_select == model.vars.demod_select.var_enum.HDT:
            # HDT enabled for BLE HDT mode
            self._ip_reg_write(model, 'HDTCFG_HDTENABLE', 1)

    def calc_hdt_do_not_care(self, model):
        """
        MCUW_RADIO_CFG-3367: The HDT PHY settings shall be baked in BLE PHYs. This is so that we quickly enable the HDT
        from BLE PHYs.
        """

        protocol_id = model.vars.protocol_id.value
        model.vars.hdt_do_not_care.value = protocol_id not in [model.vars.protocol_id.var_enum.BLE,
                                                               model.vars.protocol_id.var_enum.HDT]

    def calc_hdt_general_settings(self, model):
        hdt_do_not_care = model.vars.hdt_do_not_care.value
        self._ip_reg_write(model, 'EQUCTRL_MUSLOT', 53, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'EQUCTRL_MU0', 6, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'EQUCTRL_MU1', 8, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'EQUCTRL_MU2', 8, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'HDTCFG_STSDETSEL', 0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'HDTCFG_NXTSYMBREQSEL', 1, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'HDTCFG_CTRLHDBYPFRC', 1, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'HDTCFG_FRCWDOG', 8, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'HDTCFG_MMTEDAVGLEN1', 1, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'HDTCFG_MMTEDAVGLEN2', 1, do_not_care=hdt_do_not_care)

    def calc_sts_lst_det_hdt_settings(self, model):
        hdt_do_not_care = model.vars.hdt_do_not_care.value

        self._ip_reg_write(model, 'DETTHD0_STSGAMMA', 85, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'DETTHD0_STSACMAXTHD', 4, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'DETTHD0_STSMAXSCHPRD', 36, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'DETTHD1_STSCORRTHD0', 40, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'DETTHD1_STSCORRTHD1', 25, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'DETTHD1_STSCORRTHD2', 20, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'DETTHD1_STSCORRTHD3', 10, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'DETTHD2_LTSCORRTHD', 5, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'DETTHD3_GAININXTHD2',20, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'DETTHD3_GAININXTHD1',10, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'DETTHD3_GAININXTHD0',5, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'DETTHD3_STSVALIDTHD', 85, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'LTSDETCTRL_LTSDETPKSPACE', 13, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSDETCTRL_LTSDETTHRES', 171, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSDETCTRL_LTSDETFILLPIPE', 18, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'HDTFSMCFG0_STSACXTHRESNUM', 8, do_not_care=hdt_do_not_care)

    def calc_hdt_blocker_detection(self, model):
        hdt_do_not_care = model.vars.hdt_do_not_care.value

        self._ip_reg_write(model, 'BLOCKERDET_FASTDETWIN', 0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'BLOCKERDET_BKDETLOCKSEL', 0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'BLOCKERDET_LEADINGTHD', 0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'BLOCKERDET_LEADINGHYS', 0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'BLOCKERDET_CHPWREN', 0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'BLOCKERDET_CHPWR2LOTHD', 0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'BLOCKERDET_CHPWRHYS', 0, do_not_care=hdt_do_not_care)

    def calc_blehdt_misc(self, model):

        hdt_do_not_care = model.vars.hdt_do_not_care.value

        # other HDT settings
        self._ip_reg_write(model, 'HDTCFG_LPMODEDIS', 1, do_not_care= hdt_do_not_care)

        self._ip_reg_write(model, 'CORRCFG_CORRENABLE', 1, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'CORRCFG_FOEOUTRNG', 110, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'HDTTIMSTAMP_STAMPDUMMY', 20, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'LTSCOEI0_CSDLTSCOEI0', 81, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEI0_CSDLTSCOEI1', 69, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEI0_CSDLTSCOEI2', 69, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEI0_CSDLTSCOEI3', 10, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEI1_CSDLTSCOEI4', 66, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEI1_CSDLTSCOEI5', 10, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEI1_CSDLTSCOEI6', 81, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEI1_CSDLTSCOEI7', 66, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEI2_CSDLTSCOEI8', 65, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEISNG0_CSDLTSCOESI0', 5, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEISNG0_CSDLTSCOESI1', 3, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEISNG0_CSDLTSCOESI2', 3, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEISNG0_CSDLTSCOESI3', 1, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEISNG0_CSDLTSCOESI4', 14, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEISNG0_CSDLTSCOESI5', 1, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEISNG0_CSDLTSCOESI6', 5, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEISNG0_CSDLTSCOESI7', 14, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEISNG1_CSDLTSCOESI8', 1, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQ0_CSDLTSCOEQ0', 42, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQ0_CSDLTSCOEQ1', 41, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQ0_CSDLTSCOEQ2', 41, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQ0_CSDLTSCOEQ3', 65, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQ1_CSDLTSCOEQ4', 20, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQ1_CSDLTSCOEQ5', 65, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQ1_CSDLTSCOEQ6', 42, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQ1_CSDLTSCOEQ7', 20, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQ2_CSDLTSCOEQ8', 0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQSNG0_CSDLTSCOESQ0', 15, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQSNG0_CSDLTSCOESQ1', 12, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQSNG0_CSDLTSCOESQ2', 3, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQSNG0_CSDLTSCOESQ3', 1, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQSNG0_CSDLTSCOESQ4', 2, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQSNG0_CSDLTSCOESQ5', 14, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQSNG0_CSDLTSCOESQ6', 0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQSNG0_CSDLTSCOESQ7', 13, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'LTSCOEQSNG1_CSDLTSCOESQ8', 0, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'HDTFSMCFG0_READPNTOFF', 4, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'HDTFSMCFG0_FSMMUTEPRD', 8, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'HDTFSMCFG0_STSSCHPRD',12, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'HDTFSMCFG0_LTSSCHPRD',71, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'HDTFSMCFG0_STSVALPER', 8, do_not_care=hdt_do_not_care)

        # self._ip_reg_write(model, 'ACCESSADDR_ACCESSADDR', 3726815874, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHA_ALPHA0', 10, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHA_ALPHA1', 9, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHA_ALPHA2', 11, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHA_ALPHA3', 13, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHA_ALPHA4', 14, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHABETA_ALPHA5', 10, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHABETA_ALPHA6', 7, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHABETA_ALPHA7', 5, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHABETA_ALPHA8', 4, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANALPHABETA_BETA0', 4, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANBETA0_BETA1', 32, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANBETA0_BETA2', 49, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANBETA0_BETA3', 55, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANBETA0_BETA4', 50, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANBETA1_BETA5', 21, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANBETA1_BETA6', 10, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANBETA1_BETA7', 6, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANBETA1_BETA8', 4, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANCTRL_KALMANEN', 1, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANCTRL_KGEARSLOT0', 8, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'KALMANCTRL_KGEARSLOT1', 41, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'TXCTRL0_TXNESN',4, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXCTRL0_TXPCAA',40725, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXCTRL0_TXPFI',0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXCTRL0_TXPHYINT',0, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXCTRL0_TXRI',5, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXCTRL1_TXF0PDULEN',447, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXCTRL1_TXF1PDUHDLEN',12, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'TXLTSGP0_TXLTS0I',24215, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP1_TXLTS1I',30554, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP2_TXLTS2I',30554, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP3_TXLTS3I',3023, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP4_TXLTS4I',33327, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP5_TXLTS5I',3023, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP6_TXLTS6I',24215, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP7_TXLTS7I',33327, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP8_TXLTS8I',32767, do_not_care=hdt_do_not_care)

        self._ip_reg_write(model, 'TXLTSGP0_TXLTS0Q',22075, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP1_TXLTS1Q',11837, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP2_TXLTS2Q',53699, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP3_TXLTS3Q',32909, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP4_TXLTS4Q',59515, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP5_TXLTS5Q',32627, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP6_TXLTS6Q',43461, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP7_TXLTS7Q',6021, do_not_care=hdt_do_not_care)
        self._ip_reg_write(model, 'TXLTSGP8_TXLTS8Q',0, do_not_care=hdt_do_not_care)