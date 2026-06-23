from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcAgcGain(IPCalculator):

    def calc_agc_settling_indicator(self, model):
        do_not_care = model.vars.demod_select.value != model.vars.demod_select.var_enum.HDT
        self._ip_reg_write(model, 'SETTLINGINDCTRL_SETLINDEN', 1, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SETTLINGINDCTRL_SETLINDNEGTHD', 2, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SETTLINGINDCTRL_SETLINDPOSTHD', 2, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SETTLINGINDPER_SETLINDDELAYPERIOD', 80, do_not_care=do_not_care)
        self._ip_reg_write(model, 'SETTLINGINDPER_SETLINDSETTLEDPERIOD', 40, do_not_care=do_not_care)

    def calc_gain_schedule_regs(self, model):
        rf_path_select = model.vars.rf_path.value

        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            lnaindexborder = 1
            pgaindexborder = 11
            pnindexborder = 0
        else:
            lnaindexborder = 5  # Pre-silicon from Chris 10/23/23
            pgaindexborder = 5  # From Chris 1/16/25
            pnindexborder = 0  # New for Series3
        # 0: RFPAD at end of RFPKD schedule
        # 1: RFPAD at end of IFPKD schedule
        self._ip_reg_write(model, 'GAINRANGE_LNAINDEXBORDER', lnaindexborder)
        self._ip_reg_write(model, 'GAINRANGE_PGAINDEXBORDER', pgaindexborder)
        self._ip_reg_write(model, 'GAINRANGE_PNINDEXBORDER', pnindexborder)

    def calc_lnamixslice_reg(self, model):
        rf_path_select = model.vars.rf_path.value

        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            lnaindexmax = 1
            pgaindexmax = 24

            lnamixslice1 = 46
            lnamixslice2 = 34
            lnamixslice3 = 25
            lnamixslice4 = 12
            lnamixslice5 = 8
            lnamixslice6 = 6
            lnamixslice7 = 3
            lnamixslice8 = 2
            lnamixslice9 = 1
        else:
            # From Mohamed - https://jira.silabs.com/browse/MCUW_RADIO_CFG-2574
            # From Jira : https://jira.silabs.com/browse/MCUW_RADIO_CFG-2624
            agc_power_mode = model.vars.agc_power_mode.value

            if agc_power_mode == model.vars.agc_power_mode.var_enum.LP:
                lnaindexmax = 8
                lnamixslice1 = 34
                lnamixslice2 = 25
                lnamixslice3 = 12
                lnamixslice4 = 8
                lnamixslice5 = 6
                lnamixslice6 = 3
                lnamixslice7 = 2
                lnamixslice8 = 1
                lnamixslice9 = 0
            else:  # default to HP mode
                lnaindexmax = 9
                lnamixslice1 = 46
                lnamixslice2 = 34
                lnamixslice3 = 25
                lnamixslice4 = 12
                lnamixslice5 = 8
                lnamixslice6 = 6
                lnamixslice7 = 3
                lnamixslice8 = 2
                lnamixslice9 = 1

        self._ip_reg_write(model, 'LNAMIXCODE0_LNAMIXSLICE1', lnamixslice1)
        self._ip_reg_write(model, 'LNAMIXCODE0_LNAMIXSLICE2', lnamixslice2)
        self._ip_reg_write(model, 'LNAMIXCODE0_LNAMIXSLICE3', lnamixslice3)
        self._ip_reg_write(model, 'LNAMIXCODE0_LNAMIXSLICE4', lnamixslice4)
        self._ip_reg_write(model, 'LNAMIXCODE0_LNAMIXSLICE5', lnamixslice5)
        self._ip_reg_write(model, 'LNAMIXCODE1_LNAMIXSLICE6', lnamixslice6)
        self._ip_reg_write(model, 'LNAMIXCODE1_LNAMIXSLICE7', lnamixslice7)
        self._ip_reg_write(model, 'LNAMIXCODE1_LNAMIXSLICE8', lnamixslice8)
        self._ip_reg_write(model, 'LNAMIXCODE1_LNAMIXSLICE9', lnamixslice9)
        self._ip_reg_write(model, 'LNAMIXCODE1_LNAMIXSLICE10', default=True)
        self._ip_reg_write(model, 'GAINSTEPLIM1_LNAINDEXMAX', lnaindexmax)

        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            self._ip_reg_write(model, 'GAINSTEPLIM1_PGAINDEXMAX', pgaindexmax)
        else:
            self._ip_reg_write(model, 'GAINSTEPLIM1_PGAINDEXMAX', default=True)

    def calc_lnamixrfatt_reg(self, model):

        rf_path_select = model.vars.rf_path.value

        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            # Jira: https://jira.silabs.com/browse/MCUW_RADIO_CFG-2880
            # shift lnamixfatt of 4 bits following RTL3
            lnamixrfatt_foo = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1023, 2047, 2047]
            lnamixrfatt = lnamixrfatt_foo
            for i in range(13):
                lnamixrfatt[i] = 16 * lnamixrfatt_foo[i]
            pnindexmax = 13
        else:
            # Values from Chris Calvo 10/5/23
            lnamixrfatt = [0, 3, 6, 10, 16, 21, 29, 33, 47, 63, 113, 159, 255, 1023, 2047, 2047]
            pnindexmax = 15  # Set to 15 to include RF PAD

        # Write registers
        self._ip_reg_write(model, 'PNRFATT0_LNAMIXRFATT1', lnamixrfatt[0])
        self._ip_reg_write(model, 'PNRFATT0_LNAMIXRFATT2', lnamixrfatt[1])
        self._ip_reg_write(model, 'PNRFATT1_LNAMIXRFATT3', lnamixrfatt[2])
        self._ip_reg_write(model, 'PNRFATT1_LNAMIXRFATT4', lnamixrfatt[3])
        self._ip_reg_write(model, 'PNRFATT2_LNAMIXRFATT5', lnamixrfatt[4])
        self._ip_reg_write(model, 'PNRFATT2_LNAMIXRFATT6', lnamixrfatt[5])
        self._ip_reg_write(model, 'PNRFATT3_LNAMIXRFATT7', lnamixrfatt[6])
        self._ip_reg_write(model, 'PNRFATT3_LNAMIXRFATT8', lnamixrfatt[7])
        self._ip_reg_write(model, 'PNRFATT4_LNAMIXRFATT9', lnamixrfatt[8])
        self._ip_reg_write(model, 'PNRFATT4_LNAMIXRFATT10', lnamixrfatt[9])
        self._ip_reg_write(model, 'PNRFATT5_LNAMIXRFATT11', lnamixrfatt[10])
        self._ip_reg_write(model, 'PNRFATT5_LNAMIXRFATT12', lnamixrfatt[11])
        self._ip_reg_write(model, 'PNRFATT6_LNAMIXRFATT13', lnamixrfatt[12])
        self._ip_reg_write(model, 'PNRFATT6_LNAMIXRFATT14', lnamixrfatt[13])
        self._ip_reg_write(model, 'PNRFATT7_LNAMIXRFATT15', lnamixrfatt[14])
        self._ip_reg_write(model, 'PNRFATT7_LNAMIXRFATT16', lnamixrfatt[15])
        self._ip_reg_write(model, 'GAINSTEPLIM1_PNINDEXMAX', pnindexmax)

    def calc_pngaindb_reg(self, model):
        rf_path_select = model.vars.rf_path.value

        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            pngaindb = [41, 31, 31, 31, 30, 30, 29, 29, 29, 29, 28, 27, 27, 31, 31, 31]
        else:
            pngaindb = [38, 0, 1, 2, 30, 1, 2, 2, 2, 2, 1, 0, 31, 31, 31, 31]

        # First index is full gain (8-bit signed with 2-bit fraction)
        # Next are delta from 2dB steps (5bits: -4.0 to 3.75dB)
        self._ip_reg_write(model, 'PNGAIN1_PNGAINDB1', pngaindb[0])  # 9.50dB * 4
        self._ip_reg_write(model, 'PNGAIN1_PNGAINDB2', pngaindb[1])  # 9.5 - 2 + 0.00 = 7.50dB
        self._ip_reg_write(model, 'PNGAIN1_PNGAINDB3', pngaindb[2])  # 9.5 - 4 + 0.25 = 5.75dB
        self._ip_reg_write(model, 'PNGAIN1_PNGAINDB4', pngaindb[3])  # 9.5 - 6 + 0.50 = 4.00dB
        self._ip_reg_write(model, 'PNGAIN2_PNGAINDB5', pngaindb[4])  # 9.5 - 8 - 0.50 = 1.00dB
        self._ip_reg_write(model, 'PNGAIN2_PNGAINDB6', pngaindb[5])
        self._ip_reg_write(model, 'PNGAIN2_PNGAINDB7', pngaindb[6])
        self._ip_reg_write(model, 'PNGAIN2_PNGAINDB8', pngaindb[7])
        self._ip_reg_write(model, 'PNGAIN3_PNGAINDB9', pngaindb[8])
        self._ip_reg_write(model, 'PNGAIN3_PNGAINDB10', pngaindb[9])
        self._ip_reg_write(model, 'PNGAIN3_PNGAINDB11', pngaindb[10])
        self._ip_reg_write(model, 'PNGAIN3_PNGAINDB12', pngaindb[11])
        self._ip_reg_write(model, 'PNGAIN4_PNGAINDB13', pngaindb[12])
        self._ip_reg_write(model, 'PNGAIN4_PNGAINDB14', pngaindb[13])
        self._ip_reg_write(model, 'PNGAIN4_PNGAINDB15', pngaindb[14])
        self._ip_reg_write(model, 'PNGAIN4_PNGAINDB16', pngaindb[15])

    def calc_lnagaindb_reg(self, model):
        rf_path_select = model.vars.rf_path.value
        agc_power_mode = model.vars.agc_power_mode.value
        # New in Rainier - initializing to reset values
        # First index is full gain (8-bit signed with 2-bit fraction)
        # Next are delta from 2dB steps (5bits: -4.0 to 3.75dB)
        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            lnagaindb = [0, 0, 0, 0, 0, 0, 0, 31, 31, 31]
        else:
            if agc_power_mode == model.vars.agc_power_mode.var_enum.LP:
                lnagaindb = [28, 0, 0, 0, 31, 31, 30, 31, 31, 31]
            else:  # Default to HP mode
                lnagaindb = [36, 0, 0, 0, 0, 31, 31, 30, 31, 31]

        self._ip_reg_write(model, 'LNAGAIN1_LNAGAINDB1', lnagaindb[0])  # 9.0dB * 4 (full gain)
        self._ip_reg_write(model, 'LNAGAIN1_LNAGAINDB2', lnagaindb[1])  # 9.0 - 2 + 0.00 = 7.00dB
        self._ip_reg_write(model, 'LNAGAIN1_LNAGAINDB3', lnagaindb[2])  # 9.0 - 4 + 0.00 = 5.00dB
        self._ip_reg_write(model, 'LNAGAIN1_LNAGAINDB4', lnagaindb[3])
        self._ip_reg_write(model, 'LNAGAIN2_LNAGAINDB5', lnagaindb[4])
        self._ip_reg_write(model, 'LNAGAIN2_LNAGAINDB6', lnagaindb[5])
        self._ip_reg_write(model, 'LNAGAIN2_LNAGAINDB7', lnagaindb[6])
        self._ip_reg_write(model, 'LNAGAIN2_LNAGAINDB8', lnagaindb[7])
        self._ip_reg_write(model, 'LNAGAIN3_LNAGAINDB9', lnagaindb[8])
        self._ip_reg_write(model, 'LNAGAIN3_LNAGAINDB10', lnagaindb[9])  # 9.0 - 18 - 0.25 = -9.25dB

    def calc_tiacomp_reg(self, model):

        rf_path_select = model.vars.rf_path.value

        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            tiacomp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        else:
            tiacomp = [0, 0, 0, 0, 0, 2, 2, 2, 2, 4, 4, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]

        # New in Rainier
        self._ip_reg_write(model, 'TIACODE0_TIACOMP1', tiacomp[0])
        self._ip_reg_write(model, 'TIACODE0_TIACOMP2', tiacomp[1])
        self._ip_reg_write(model, 'TIACODE0_TIACOMP3', tiacomp[2])
        self._ip_reg_write(model, 'TIACODE0_TIACOMP4', tiacomp[3])
        self._ip_reg_write(model, 'TIACODE0_TIACOMP5', tiacomp[4])
        self._ip_reg_write(model, 'TIACODE0_TIACOMP6', tiacomp[5])
        self._ip_reg_write(model, 'TIACODE1_TIACOMP7', tiacomp[6])
        self._ip_reg_write(model, 'TIACODE1_TIACOMP8', tiacomp[7])
        self._ip_reg_write(model, 'TIACODE1_TIACOMP9', tiacomp[8])
        self._ip_reg_write(model, 'TIACODE1_TIACOMP10', tiacomp[9])
        self._ip_reg_write(model, 'TIACODE1_TIACOMP11', tiacomp[10])
        self._ip_reg_write(model, 'TIACODE1_TIACOMP12', tiacomp[11])
        self._ip_reg_write(model, 'TIACODE1_TIACOMP13', tiacomp[12])
        self._ip_reg_write(model, 'TIACODE1_TIACOMP14', tiacomp[13])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP15', tiacomp[14])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP16', tiacomp[15])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP17', tiacomp[16])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP18', tiacomp[17])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP19', tiacomp[18])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP20', tiacomp[19])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP21', tiacomp[20])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP22', tiacomp[21])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP23', tiacomp[22])
        self._ip_reg_write(model, 'TIACODE8_TIACOMP24', tiacomp[23])

    def calc_tia_capfb_reg(self, model):

        rf_path_select = model.vars.rf_path.value

        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            # Jira: https://jira.silabs.com/browse/MCUW_RADIO_CFG-2880
            # Add new register lnaslice
            # shift tiacapfb of 6 bits and add lnaslice following RTL3
            tiacapfb = [0 for i in range (24)]
            tiacapfb_foo = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            lnaslice = [16, 13, 10, 8, 7, 6, 5, 4, 3, 2, 1, 3, 2, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1]
            for i in range(24):
                tiacapfb[i] = 64 * tiacapfb_foo[i] + lnaslice[i]
        else:
            tiacapfb = [16, 20, 26, 33, 41, 52, 64, 81, 103, 126, 155, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # New in Rainier
        self._ip_reg_write(model, 'TIACODE2_TIACAPFB1', tiacapfb[0])
        self._ip_reg_write(model, 'TIACODE2_TIACAPFB2', tiacapfb[1])
        self._ip_reg_write(model, 'TIACODE2_TIACAPFB3', tiacapfb[2])
        self._ip_reg_write(model, 'TIACODE2_TIACAPFB4', tiacapfb[3])
        self._ip_reg_write(model, 'TIACODE3_TIACAPFB5', tiacapfb[4])
        self._ip_reg_write(model, 'TIACODE3_TIACAPFB6', tiacapfb[5])
        self._ip_reg_write(model, 'TIACODE3_TIACAPFB7', tiacapfb[6])
        self._ip_reg_write(model, 'TIACODE3_TIACAPFB8', tiacapfb[7])
        self._ip_reg_write(model, 'TIACODE4_TIACAPFB9', tiacapfb[8])
        self._ip_reg_write(model, 'TIACODE4_TIACAPFB10', tiacapfb[9])
        self._ip_reg_write(model, 'TIACODE4_TIACAPFB11', tiacapfb[10])
        self._ip_reg_write(model, 'TIACODE4_TIACAPFB12', tiacapfb[11])
        self._ip_reg_write(model, 'TIACODE5_TIACAPFB13', tiacapfb[12])
        self._ip_reg_write(model, 'TIACODE5_TIACAPFB14', tiacapfb[13])
        self._ip_reg_write(model, 'TIACODE5_TIACAPFB15', tiacapfb[14])
        self._ip_reg_write(model, 'TIACODE5_TIACAPFB16', tiacapfb[15])
        self._ip_reg_write(model, 'TIACODE6_TIACAPFB17', tiacapfb[16])
        self._ip_reg_write(model, 'TIACODE6_TIACAPFB18', tiacapfb[17])
        self._ip_reg_write(model, 'TIACODE6_TIACAPFB19', tiacapfb[18])
        self._ip_reg_write(model, 'TIACODE6_TIACAPFB20', tiacapfb[19])
        self._ip_reg_write(model, 'TIACODE7_TIACAPFB21', tiacapfb[20])
        self._ip_reg_write(model, 'TIACODE7_TIACAPFB22', tiacapfb[21])
        self._ip_reg_write(model, 'TIACODE7_TIACAPFB23', tiacapfb[22])
        self._ip_reg_write(model, 'TIACODE7_TIACAPFB24', tiacapfb[23])

    def calc_pgagaindb_reg(self, model):
        rf_path_select = model.vars.rf_path.value

        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            pgagaindb = [167, 1, 0, 1, 3, 7, 7, 8, 4, 31, 2, 4, 31, 2, 4, 31, 2, 3, 0, 0, 1, 1, 1, 5]
        else:
            pgagaindb = [136, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # First index is full gain (9-bit signed with 2-bit fraction)
        # Next are delta from 2dB steps (5bits: -4.0 to 3.75dB)
        self._ip_reg_write(model, 'PGAGAIN1_PGAGAINDB1', pgagaindb[0])  # 34.0dB
        self._ip_reg_write(model, 'PGAGAIN1_PGAGAINDB2', pgagaindb[1])  # 34.0 -2 + 0.00 = 32.00dB
        self._ip_reg_write(model, 'PGAGAIN1_PGAGAINDB3', pgagaindb[2])  # 34.0 -4 + 0.00 = 30.00dB
        self._ip_reg_write(model, 'PGAGAIN2_PGAGAINDB4', pgagaindb[3])
        self._ip_reg_write(model, 'PGAGAIN2_PGAGAINDB5', pgagaindb[4])
        self._ip_reg_write(model, 'PGAGAIN2_PGAGAINDB6', pgagaindb[5])
        self._ip_reg_write(model, 'PGAGAIN3_PGAGAINDB7', pgagaindb[6])
        self._ip_reg_write(model, 'PGAGAIN3_PGAGAINDB8', pgagaindb[7])
        self._ip_reg_write(model, 'PGAGAIN3_PGAGAINDB9', pgagaindb[8])
        self._ip_reg_write(model, 'PGAGAIN4_PGAGAINDB10', pgagaindb[9])
        self._ip_reg_write(model, 'PGAGAIN4_PGAGAINDB11', pgagaindb[10])  # 34.0 -20 + 0.00 = 14.00dB
        self._ip_reg_write(model, 'PGAGAIN4_PGAGAINDB12', pgagaindb[11])
        self._ip_reg_write(model, 'PGAGAIN5_PGAGAINDB13', pgagaindb[12])
        self._ip_reg_write(model, 'PGAGAIN5_PGAGAINDB14', pgagaindb[13])
        self._ip_reg_write(model, 'PGAGAIN5_PGAGAINDB15', pgagaindb[14])
        self._ip_reg_write(model, 'PGAGAIN6_PGAGAINDB16', pgagaindb[15])
        self._ip_reg_write(model, 'PGAGAIN6_PGAGAINDB17', pgagaindb[16])
        self._ip_reg_write(model, 'PGAGAIN6_PGAGAINDB18', pgagaindb[17])
        self._ip_reg_write(model, 'PGAGAIN7_PGAGAINDB19', pgagaindb[18])
        self._ip_reg_write(model, 'PGAGAIN7_PGAGAINDB20', pgagaindb[19])
        self._ip_reg_write(model, 'PGAGAIN7_PGAGAINDB21', pgagaindb[20])
        self._ip_reg_write(model, 'PGAGAIN7_PGAGAINDB22', pgagaindb[21])
        self._ip_reg_write(model, 'PGAGAIN7_PGAGAINDB23', pgagaindb[22])
        self._ip_reg_write(model, 'PGAGAIN7_PGAGAINDB24', pgagaindb[23])

    def calc_pgacode_pgagain(self, model):

        """

        :param model:
        :return:
        """

        rf_path_select = model.vars.rf_path.value

        if rf_path_select == model.vars.rf_path.var_enum.WIFI:
            pgagain = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 5, 7, 10, 13, 15]
        else:
            pgagain = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 0, 0, 0, 0, 0, 1, 3, 5, 7, 10, 13, 15]

        self._ip_reg_write(model, 'PGACODE0_PGAGAIN1', pgagain[0])
        self._ip_reg_write(model, 'PGACODE0_PGAGAIN2', pgagain[1])
        self._ip_reg_write(model, 'PGACODE0_PGAGAIN3', pgagain[2])
        self._ip_reg_write(model, 'PGACODE0_PGAGAIN4', pgagain[3])
        self._ip_reg_write(model, 'PGACODE0_PGAGAIN5', pgagain[4])
        self._ip_reg_write(model, 'PGACODE0_PGAGAIN6', pgagain[5])
        self._ip_reg_write(model, 'PGACODE0_PGAGAIN7', pgagain[6])
        self._ip_reg_write(model, 'PGACODE0_PGAGAIN8', pgagain[7])
        self._ip_reg_write(model, 'PGACODE1_PGAGAIN9', pgagain[8])
        self._ip_reg_write(model, 'PGACODE1_PGAGAIN10', pgagain[9])
        self._ip_reg_write(model, 'PGACODE1_PGAGAIN11', pgagain[10])
        self._ip_reg_write(model, 'PGACODE1_PGAGAIN12', pgagain[11])
        self._ip_reg_write(model, 'PGACODE1_PGAGAIN13', pgagain[12])
        self._ip_reg_write(model, 'PGACODE1_PGAGAIN14', pgagain[13])
        self._ip_reg_write(model, 'PGACODE1_PGAGAIN15', pgagain[14])
        self._ip_reg_write(model, 'PGACODE1_PGAGAIN16', pgagain[15])
        self._ip_reg_write(model, 'PGACODE2_PGAGAIN17', pgagain[16])
        self._ip_reg_write(model, 'PGACODE2_PGAGAIN18', pgagain[17])
        self._ip_reg_write(model, 'PGACODE2_PGAGAIN19', pgagain[18])
        self._ip_reg_write(model, 'PGACODE2_PGAGAIN20', pgagain[19])
        self._ip_reg_write(model, 'PGACODE2_PGAGAIN21', pgagain[20])
        self._ip_reg_write(model, 'PGACODE2_PGAGAIN22', pgagain[21])
        self._ip_reg_write(model, 'PGACODE2_PGAGAIN23', pgagain[22])
        self._ip_reg_write(model, 'PGACODE2_PGAGAIN24', pgagain[23])

    def calc_antdiv_gainmode_reg(self, model):
        self._ip_reg_write(model, 'ANTDIV_GAINMODE', 0)

    def calc_lnamixcuren_reg(self, model):
        # New in Rainier - initializing to reset value
        # LSB->agcindex1, MSB->agcindex10
        agc_power_mode = model.vars.agc_power_mode.value

        if agc_power_mode == model.vars.agc_power_mode.var_enum.LP:
            lnamixcurr = 0x1F8 >> 1
        else: # Default to HP mode
            lnamixcurr = 0x1F8

        self._ip_reg_write(model, 'LNAMIXCODE2_LNAMIXCUREN', lnamixcurr)
        self._ip_reg_write(model, 'LNAMIXCODE2_LNAMIXCUREN', lnamixcurr)

    def calc_agc_adcattenmode_code(self, model):

        etsi = model.vars.etsi_cat1_compatible.value

        if etsi != model.vars.etsi_cat1_compatible.var_enum.Normal:
            self._ip_reg_write(model, 'CTRL0_ADCATTENCODE', 1)
            self._ip_reg_write(model, 'CTRL0_ADCATTENMODE', 1)
        else:
            self._ip_reg_write(model, 'CTRL0_ADCATTENCODE', 0)
            self._ip_reg_write(model, 'CTRL0_ADCATTENMODE', 0)

    def calc_adcgaindb_reg(self, model):
        # New in Rainier - initializing to reset values
        # First index is full gain (6-bit signed with 2-bit fraction)
        # Next are delta from 2dB steps (3bits: -1.0 to 0.75dB)
        #self._ip_reg_write(model, 'ADC0_ADCGAINDB0', 0) # 0.0dB * 4 (full gain)
        #self._ip_reg_write(model, 'ADC0_ADCGAINDB1', 0) # 0.0 - 2 + 0.00 = -2.00dB
        #self._ip_reg_write(model, 'ADC0_ADCGAINDB2', 0) # 0.0 - 4 + 0.00 = -4.00dB
        #self._ip_reg_write(model, 'ADC0_ADCGAINDB3', 0) # 0.0 - 6 + 0.00 = -6.00dB
        pass
        # !!! DO NOT EXPOSE ADC0 registers because it conflicts with renaming
        # !!! from ADM flow of SAR12 into ADC0. Need be fixed

    def calc_pwrtarget_val(self, model):
        """set agc_power_target based on modulation method

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        mod_format = model.vars.modulation_type.value

        if mod_format == model.vars.modulation_type.var_enum.OOK:
            model.vars.agc_power_target.value = 0
        else:
            model.vars.agc_power_target.value = -2

    def calc_pwrtarget_reg(self, model):
        """set PWTARGET register

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        # level in dBm (can be negative)
        level = model.vars.agc_power_target.value

        self._ip_reg_write(model, 'CTRL0_PWRTARGET', level, allow_neg=True)

    def calc_agc_pwr_mode(self, model):
        #High performance by default, allow override
        model.vars.agc_power_mode.value = model.vars.agc_power_mode.var_enum.HP

    def calc_agc_rfpkdthd_reg(self, model):
        # disable slow loop of agc
        self._ip_reg_write(model, 'CTRL0_CFLOOPNFADJ', 0) # disable slow loop of agc
        self._ip_reg_write(model, 'DUALRFPKDTHD1_RFPKDHITHD0', 1)
        self._ip_reg_write(model, 'DUALRFPKDTHD1_RFPKDHITHD1', 40)
        self._ip_reg_write(model, 'DUALRFPKDTHD0_RFPKDLOWTHD0', 1)
        self._ip_reg_write(model, 'DUALRFPKDTHD0_RFPKDLOWTHD1', 10)