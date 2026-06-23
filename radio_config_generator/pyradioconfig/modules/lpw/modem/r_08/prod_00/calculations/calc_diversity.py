from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
import math


#TODO: is there a way to figure out don't care for diversity? maybe some model variable?
class CalcDiversity(IPCalculator):
    # Method name: adbbss_lut
    # Defined in: bobcat\calculators\calc_diversity.py
    def adbbss_lut(self, refamp, nbitgain, index):
        sat_val = round(math.pow(2, nbitgain) - 1)
        if index == 0:
            int_val = sat_val
        else:
            int_val = round(1.0 * refamp / index * math.pow(2, nbitgain - 1))
            if int_val > sat_val:
                int_val = sat_val
        return int_val


    # Method name: calc_adpc_adbbss
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_adpc_adbbss(self, model):
        demod_sel = model.vars.demod_select.value
        refamp = model.vars.antdiv_adbbss_refamp.value
        antdivmode = model.vars.antdivmode.value
        if demod_sel == model.vars.demod_select.var_enum.COHERENT and antdivmode != model.vars.antdivmode.var_enum.DISABLE:
            nbitgain = 5
            adbbss_lut = []
            for lut_idx in range(16):
                adbbss_lut.append(self.adbbss_lut(refamp, nbitgain, lut_idx))
        else:
            adbbss_lut = [31, 31, 31, 31, 31, 31, 31, 27, 24, 21, 19, 17, 16, 14, 13, 12]

        self._ip_reg_write(model, 'ADPC4_ADBBSSAMPLUT0', adbbss_lut[0])
        self._ip_reg_write(model, 'ADPC4_ADBBSSAMPLUT1', adbbss_lut[1])
        self._ip_reg_write(model, 'ADPC4_ADBBSSAMPLUT2', adbbss_lut[2])
        self._ip_reg_write(model, 'ADPC4_ADBBSSAMPLUT3', adbbss_lut[3])
        self._ip_reg_write(model, 'ADPC5_ADBBSSAMPLUT4', adbbss_lut[4])
        self._ip_reg_write(model, 'ADPC5_ADBBSSAMPLUT5', adbbss_lut[5])
        self._ip_reg_write(model, 'ADPC5_ADBBSSAMPLUT6', adbbss_lut[6])
        self._ip_reg_write(model, 'ADPC5_ADBBSSAMPLUT7', adbbss_lut[7])
        self._ip_reg_write(model, 'ADPC6_ADBBSSAMPLUT8', adbbss_lut[8])
        self._ip_reg_write(model, 'ADPC6_ADBBSSAMPLUT9', adbbss_lut[9])
        self._ip_reg_write(model, 'ADPC6_ADBBSSAMPLUT10', adbbss_lut[10])
        self._ip_reg_write(model, 'ADPC6_ADBBSSAMPLUT11', adbbss_lut[11])
        self._ip_reg_write(model, 'ADPC7_ADBBSSAMPLUT12', adbbss_lut[12])
        self._ip_reg_write(model, 'ADPC7_ADBBSSAMPLUT13', adbbss_lut[13])
        self._ip_reg_write(model, 'ADPC7_ADBBSSAMPLUT14', adbbss_lut[14])
        self._ip_reg_write(model, 'ADPC7_ADBBSSAMPLUT15', adbbss_lut[15])

    # Method name: calc_adpcsigampthr_reg
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_adpcsigampthr_reg(self, model):
        sigampthr_dec = model.vars.antdiv_adpcsigampthr.value
        # compress ampthr to adpcsigampthr (ampthr = [7:4] << [3:0])
        i = 0
        while i < 16:
            div = round(sigampthr_dec / float(pow(2, i)))
            if div < 16:
                break
            i += 1
        adpcsigampthr = div * 16 + i
        self._ip_reg_write(model, 'ADPC2_ADPCSIGAMPTHR', adpcsigampthr)

    # Method name: calc_adprethresh_scale
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_adprethresh_scale(self, model):
        adpcen = model.vars.MODEM_ADPC1_ADPCEN.value
        if adpcen:
            antdiv_adprethresh_scale = 0.2
        else:
            antdiv_adprethresh_scale = 0.0
        model.vars.antdiv_adprethresh_scale.value = antdiv_adprethresh_scale

    # Method name: calc_diveristy_adpc_windowsize
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diveristy_adpc_windowsize(self, model):
        adpcwndsizechip = model.vars.antdiv_adpcwndsize.value
        self._ip_reg_write(model, 'ADPC1_ADPCWNDSIZECHIP', adpcwndsizechip)

    # Method name: calc_diversity_adctrl1
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diversity_adctrl1(self, model):
        demod_sel = model.vars.demod_select.value
        adpcen = model.vars.MODEM_ADPC1_ADPCEN.value
        frequency_offset_bias = model.vars.antdiv_freq_offset_bias.value
        adbacorrthr = model.vars.MODEM_ADQUAL6_ADBACORRTHR.value
        adbacorrdiff = model.vars.MODEM_ADQUAL6_ADBACORRDIFF.value
        # : Enable or disable correlation threshold decision
        adbacorrthr_dis_val = 1 if adbacorrthr == 0 else 0
        # : Enable or disable correlation difference decision
        adbacorrdiff_dis_val = 1 if adbacorrdiff == 0 else 0
        # : Calculate frequency offset bias by converting to two's complement
        frequency_offset_bias_val = frequency_offset_bias + 32 if frequency_offset_bias < 0 else frequency_offset_bias
        # : calculate
        if demod_sel == model.vars.demod_select.var_enum.COHERENT:
            adbarssithr_dis_val = 1
        else:
            adbarssithr_dis_val = 0
        # : Register field definitions for adctrl1 does not exists in cmsis.
        # : Manually define offsets for each field within adctrl1 register
        field_offsets_vals = {
            'QUAL_UPDATE_TDS': [0, 1],
            'FSM_RESET': [1, 0],
            'DEMODRXREQ_RST': [2, 0],
            'DEMODRXREQ_SET': [3, 0],
            'DEMODRXREQ_CLR': [4, 0],
            'DEMODRXREQ_FORCE': [5, 0],
            'DEMODRXREQ_VAL': [6, 0],
            'RSSIVALID_SW': [7, 0],
            'IT_ENTER': [8, 0],
            'IT_LEAVE': [9, 0],
            'RSVD': [10, 0],
            'PWR_SWFSM': [11, 0],
            'PWR_SWO': [12, 0],
            'QUAL_UPD_NOTIMDET': [13, 0],
            'QUAL_CLR_NOTIMDET': [14, 0],
            'BA_OPT': [15, 0],
            'BA_CORR_HI_DIS': [16, adbacorrthr_dis_val],
            'BA_CORR_EQ_DIS': [17, adbacorrdiff_dis_val],
            'BA_RSSI_HI_DIS': [18, adbarssithr_dis_val],
            'BA_RSSI_EQ_DIS': [19, 1],
            'BA_GAIN_LO_DIS': [20, 0],
            'FGR_HI_CORR_DIS': [21, 0],
            'FGR_GR_RSSI_DIS': [22, 0],
            'FGR_GR_AGC_DIS': [23, 0],
            'FGR_GR_GAIN_DIS': [24, 0],
            'FGR_GR_DIS': [25, 0],
            'FREQ_BIAS': [26, frequency_offset_bias_val],
        }
        # : calculate ctrl1 register by applying offsets to each field
        adctrl1 = 0
        if adpcen == 1:
            adctrl1 = 0
            for field_name in field_offsets_vals:
                adctrl1 += field_offsets_vals[field_name][1] * pow(2, field_offsets_vals[field_name][0])
        self._ip_reg_write(model, 'ADCTRL1_ADCTRL1', adctrl1)

    # Method name: calc_diversity_adctrl2
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diversity_adctrl2(self, model):
        demod_sel = model.vars.demod_select.value
        adpcen = model.vars.MODEM_ADPC1_ADPCEN.value
        if demod_sel == model.vars.demod_select.var_enum.COHERENT:
            wnd_amp_rst = 0
            wnd_rst_amp = 1
        else:
            wnd_amp_rst = 1
            wnd_rst_amp = 0
        # : Register field definitions for adctrl2 does not exists in cmsis.
        # : Manually define offsets for each field within adctrl2 register
        field_offsets_vals = {
            'PCORR_EN_BC': [0, 1],
            'ANTSEL_DELAY': [11, 1],
            'BA_AMP_DIS': [19, 0],
            'WND_AMP_RST': [20, wnd_amp_rst],
            'TIM_AMP_THR': [21, 0],
            'FOC_MODE0': [23, 0],
            'FOC_MODE1': [24, 0],
            'WND_RST_AMP': [25, wnd_rst_amp],
            'WND_RST_BBSS': [27, 0],
        }
        # : calculate ctrl2 register by applying offsets to each field
        if adpcen == 1:
            adctrl2 = 0
            for field_name in field_offsets_vals:
                adctrl2 += field_offsets_vals[field_name][1] * pow(2, field_offsets_vals[field_name][0])
        else:
            adctrl2 = 129
        self._ip_reg_write(model, 'ADCTRL2_ADCTRL2', adctrl2)

    # Method name: calc_diversity_adpc_buffersize
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diversity_adpc_buffersize(self, model):
        adpcen = model.vars.MODEM_ADPC1_ADPCEN.value
        delay_us = model.vars.antdiv_switch_delay_us.value
        skip_us = model.vars.antdiv_switch_skip_us.value
        oversampling_rate_actual = model.vars.oversampling_rate_actual.value
        baudrate_actual = model.vars.rx_baud_rate_actual.value
        adpcwndsizechip = model.vars.MODEM_ADPC1_ADPCWNDSIZECHIP.value
        # : calculate chip period in us
        chip_period_us = 1.0 / baudrate_actual * 1e6  # chip_us
        # : Convert delay/skip in us to number of chips
        delay_chips = delay_us / chip_period_us
        skip_chips = skip_us / chip_period_us
        # : calculate buffer size and write size
        adpcantsampbuf = delay_chips * oversampling_rate_actual
        adpcantsampwrite = adpcantsampbuf + skip_chips * oversampling_rate_actual
        # : calculate how long to stay on one antenna in number of adc samples
        adpcantsampswitch = (adpcwndsizechip + skip_chips) * oversampling_rate_actual
        # : convert to int
        adpcantsampbuf_int = int(round(adpcantsampbuf))
        adpcantsampwrite_int = int(round(adpcantsampwrite))
        adpcantsampswitch_int = int(round(adpcantsampswitch))
        if adpcen == 1:
            self._ip_reg_write(model, 'ADPC8_ADPCANTSAMPBUF', adpcantsampbuf_int)
            self._ip_reg_write(model, 'ADPC8_ADPCANTSAMPWRITE', adpcantsampwrite_int)
            self._ip_reg_write(model, 'ADPC8_ADPCANTSAMPSWITCH', adpcantsampswitch_int)
        else:
            self._ip_reg_write(model, 'ADPC8_ADPCANTSAMPBUF', 1)
            self._ip_reg_write(model, 'ADPC8_ADPCANTSAMPWRITE', 0x1F)
            self._ip_reg_write(model, 'ADPC8_ADPCANTSAMPSWITCH', 0xBE)

    # Method name: calc_diversity_adpc_corroffsetchip
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diversity_adpc_corroffsetchip(self, model):
        adpcwndsizechip = model.vars.MODEM_ADPC1_ADPCWNDSIZECHIP.value
        adpcwndcnt = model.vars.MODEM_ADPC1_ADPCWNDCNT.value
        adpctimingbauds = model.vars.MODEM_ADPC1_ADPCTIMINGBAUDS.value
        adpccorroffsetchip = adpcwndsizechip * adpcwndcnt - adpctimingbauds
        self._ip_reg_write(model, 'ADPC1_ADPCCORROFFSETCHIP', adpccorroffsetchip)

    # Method name: calc_diversity_adpc_corrsamples
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diversity_adpc_corrsamples(self, model):
        adpcen = model.vars.MODEM_ADPC1_ADPCEN.value
        oversampling_rate_actual = model.vars.oversampling_rate_actual.value
        adpctimingbauds = model.vars.MODEM_ADPC1_ADPCTIMINGBAUDS.value
        if adpcen == 1:
            adpccorrsamples = adpctimingbauds * oversampling_rate_actual
        else:
            adpccorrsamples = 160
        adpccorrsamples_int = int(round(adpccorrsamples))
        self._ip_reg_write(model, 'ADPC2_ADPCCORRSAMPLES', adpccorrsamples_int)

    # Method name: calc_diversity_adpc_timingbauds
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diversity_adpc_timingbauds(self, model):
        adpcwndsizechip = model.vars.MODEM_ADPC1_ADPCWNDSIZECHIP.value
        adpcwndcnt = model.vars.MODEM_ADPC1_ADPCWNDCNT.value
        # : Calculate number of bauds (window size in chips times total number of windows)
        adpctimingbauds = adpcwndsizechip * adpcwndcnt
        self._ip_reg_write(model, 'ADPC1_ADPCTIMINGBAUDS', adpctimingbauds)

    # Method name: calc_diversity_adpc_windowcnt
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diversity_adpc_windowcnt(self, model):
        adpcen = model.vars.MODEM_ADPC1_ADPCEN.value
        if adpcen:  # : enable dual window if paralle correlation is enabled
            adpcwndcnt = 2
        else:
            adpcwndcnt = 1
        self._ip_reg_write(model, 'ADPC1_ADPCWNDCNT', adpcwndcnt)

    # Method name: calc_diversity_adpcen
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diversity_adpcen(self, model):
        enable_parallel_correlation = model.vars.antdiv_enable_parallel_correlation.value
        if enable_parallel_correlation:
            adpcen = 1
        else:
            adpcen = 0
        self._ip_reg_write(model, 'ADPC1_ADPCEN', adpcen)

    # Method name: calc_diversity_adprethresh
    # Defined in: ocelot\calculators\calc_diversity.py
    def calc_diversity_adprethresh(self, model):
        timthresh = model.vars.MODEM_TIMING_TIMTHRESH.value
        adprethresh_scale = model.vars.antdiv_adprethresh_scale.value
        # : Per David Rault - Scale adprethresh by a factor of timing threshold
        adprethresh = adprethresh_scale * timthresh
        adprethresh_int = int(round(adprethresh))
        # : if adprethresh register is non-zero, enable preamble threshold for antenna diversity
        self._ip_reg_write(model, 'ANTDIVCTRL_ENADPRETHRESH', int(adprethresh_int > 0))
        self._ip_reg_write(model, 'ANTDIVCTRL_ADPRETHRESH', adprethresh_int)

    # Method name: calc_diversity_default_configs
    # Defined in: bobcat\calculators\calc_diversity.py
    def calc_diversity_default_configs(self, model):
        demod_sel = model.vars.demod_select.value
        # : Assign default values to antenna diversity profile inputs on non-diversity phys
        model.vars.antdiv_enable_parallel_correlation.value = False
        model.vars.antdiv_switch_delay_us.value = 0.0
        model.vars.antdiv_switch_skip_us.value = 0.0
        model.vars.antdiv_adpcwndsize.value = 32
        model.vars.antdiv_adpcsigampthr.value = 0
        model.vars.antdiv_adbbss_refamp.value = 0
        # : Disable freq offset bias for coherent mode
        if demod_sel == model.vars.demod_select.var_enum.COHERENT:
            freq_offset_bias = 0
        else:
            freq_offset_bias = -16
        model.vars.antdiv_freq_offset_bias.value = freq_offset_bias


    # Method name: calc_diversity_div_demod_reset_period_hemi_usec_value
    # Defined in: common\calculators\calc_diversity.py
    def calc_diversity_div_demod_reset_period_hemi_usec_value(self, model):
        """
        Calculate period/interval for sequencer FW to issue a reset to demod.
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        antdivmode = model.vars.antdivmode.value
        preamblebits = model.vars.preamble_length.value * 1.0
        baudrate = model.vars.baudrate.value * 1.0
        if model.part_family.lower() in ["jumbo", "nerio", "nixi"]:
            if antdivmode == model.vars.antdivmode.var_enum.DISABLE:
                # disable if not in diversity mode
                model.vars.div_demod_reset_period_hemi_usec.value = 0
            elif (antdivmode == model.vars.antdivmode.var_enum.ANTSELFIRST) or (
                    antdivmode == model.vars.antdivmode.var_enum.ANTSELRSSI):
                # Units are half uSec. Use 1000x preamble time as the period
                model.vars.div_demod_reset_period_hemi_usec.value = int(preamblebits / baudrate * 1000 * 1e6 * 2)

    # Method name: calc_diversity_values
    # Defined in: ocelot\calculators\calc_diversity.py
    def calc_diversity_values(self, model):
        """apply inputs to antenna diversity output software variables for RAIL to consume
        TODO: consider preamble length--should be long enough to allow the diversity search algorithm to make a proper antenna selection
        Not handled here: MODEM_ROUTEPEN: ANT0PEN, ANT1PEN to enable these pins, and MODEM_ROUTELOC1 to route to GPIO
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # default value 0 ANTENNA0 Antenna 0 (ANT0=1, ANT1=0) is used. This is not exposed as one of the enums, so use 0 here.
        # default ANTDIVREPEATDIS 0
        model.vars.antdivmode.value = model.vars.antdivmode.var_enum.DISABLE
        model.vars.antdivrepeatdis.value = model.vars.antdivrepeatdis.var_enum.REPEATFIRST
        # # unless set otherwise by advanced inputs
        antdivmode = model.vars.antdivmode.value
        antdivrepeatdis = model.vars.antdivrepeatdis.value
        model.vars.div_antdivmode.value = int(antdivmode)
        model.vars.div_antdivrepeatdis.value = int(antdivrepeatdis)

    # Method name: calc_phdemodantdiv_antenna_wait
    # Defined in: ocelot\calculators\calc_diversity.py
    def calc_phdemodantdiv_antenna_wait(self, model):
        # Number of clock cycles to wait before switching to another antenna. Base clock is symbol rate.
        # This field does matter even when antdiv is disabled
        antwait = 20  # : Recommended value by He Gou
        self._ip_reg_write(model, 'PHDMODANTDIV_ANTWAIT', antwait)

    # Method name: calc_phdemodantdiv_decision_regions
    # Defined in: ocelot\calculators\calc_diversity.py
    def calc_phdemodantdiv_decision_regions(self, model):
        """
        Phase demod antenna diversity determines the best antenna using both correlation and RSSI measurements.
        Decision to prioritize RSSI vs. Correlation is dependent on the absolute value of RSSI or correlation, which
        is known as the decision regions.
        Args:
            model:
        Returns:
        """
        antdivmode = model.vars.antdivmode.value
        demod_select = model.vars.demod_select.value
        do_not_care = antdivmode != model.vars.antdivmode.var_enum.PHDEMODANTDIV
        if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV:
            # : if rssicorr{x} = 1, then for x region, use RSSI based decision to select best antenna
            rssicorr0 = 1
            rssicorr1 = 1
            rssicorr2 = 1
            rssicorr3 = 1
            # : decision thresholds
            rssianddivthd = 20
            corranddivthd = 100
        if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV:
            self._ip_reg_write(model, 'PHANTDECSION_RSSICORR0', rssicorr0)
            self._ip_reg_write(model, 'PHANTDECSION_RSSICORR1', rssicorr1)
            self._ip_reg_write(model, 'PHANTDECSION_RSSICORR2', rssicorr2)
            self._ip_reg_write(model, 'PHANTDECSION_RSSICORR3', rssicorr3)
            self._ip_reg_write(model, 'PHANTDECSION_RSSIANDDIVTHD', rssianddivthd)
            self._ip_reg_write(model, 'PHANTDECSION_CORRANDDIVTHD', corranddivthd)
        else:
            self._reg_do_not_care(model.vars.MODEM_PHANTDECSION_RSSICORR0)
            self._reg_do_not_care(model.vars.MODEM_PHANTDECSION_RSSICORR1)
            self._reg_do_not_care(model.vars.MODEM_PHANTDECSION_RSSICORR2)
            self._reg_do_not_care(model.vars.MODEM_PHANTDECSION_RSSICORR3)
            self._reg_do_not_care(model.vars.MODEM_PHANTDECSION_RSSIANDDIVTHD)
            self._reg_do_not_care(model.vars.MODEM_PHANTDECSION_CORRANDDIVTHD)

    # Method name: calc_phdemodantdiv_skipcorrthd_reg
    # Defined in: ocelot\calculators\calc_diversity.py
    def calc_phdemodantdiv_skipcorrthd_reg(self, model):
        """
        If the first antenna correlation value is higher than the SKIPCORRTHD, then skip the second antenna check.
        Args:
            model:
        Returns:
        """
        antdivmode = model.vars.antdivmode.value
        if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV:
            self._ip_reg_write(model, 'PHDMODANTDIV_SKIPCORRTHD', 100)
        else:
            self._reg_do_not_care(model.vars.MODEM_PHDMODANTDIV_SKIPCORRTHD)

    # Method name: calc_phdemodantdiv_skiprssithd_reg
    # Defined in: ocelot\calculators\calc_diversity.py
    def calc_phdemodantdiv_skiprssithd_reg(self, model):
        """
        If the first antenna RSSI value is higher than the SKIPRSSITHD, then skip the second antenna check.
        Args:
            model:
        Returns: None
        """
        demod_select = model.vars.demod_select.value
        antdivmode = model.vars.antdivmode.value
        # : TODO update calculation since this value depends on the sensitivity
        if demod_select == model.vars.demod_select.var_enum.BCR:
            reg_val = 240
        elif demod_select == model.vars.demod_select.var_enum.TRECS_SLICER \
                or demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI:
            reg_val = 251
        if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV:
            self._ip_reg_write(model, 'PHDMODANTDIV_SKIPRSSITHD', reg_val)
        else:
            self._reg_do_not_care(model.vars.MODEM_PHDMODANTDIV_SKIPRSSITHD)

    # Method name: calc_phdmodantdiv_antdivrepeatdis
    # Defined in: ocelot\calculators\calc_diversity.py
    def calc_phdmodantdiv_antdivrepeatdis(self, model):
        model.vars.skip2ant.value = model.vars.skip2ant.var_enum.NOSKIP2ANT

    # Method name: calc_phdmodantdiv_antdivrepeatdis_reg
    # Defined in: ocelot\calculators\calc_diversity.py
    def calc_phdmodantdiv_antdivrepeatdis_reg(self, model):
        antdivmode = model.vars.antdivmode.value
        skip2ant = model.vars.skip2ant.value
        reg = 1  # : skip 2nd antenna check by default
        # : For phase demod antdiv mode, set skip2ant register
        if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV:
            if skip2ant == model.vars.skip2ant.var_enum.NOSKIP2ANT:
                reg = 0
        if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV:
            self._ip_reg_write(model, 'PHDMODANTDIV_SKIP2ANT', reg)
        else:
            self._reg_do_not_care(model.vars.MODEM_PHDMODANTDIV_SKIP2ANT)

    # Method name: calc_phdmodctrl_rssifltbyp
    # Defined in: ocelot\calculators\calc_diversity.py
    def calc_phdmodctrl_rssifltbyp(self, model):
        # do not bypass rssi filter. otherwise, sensitivity degradation if signal power difference is small.
        # This field does matter even when antdiv is disabled
        rssifltbyp = 0
        self._ip_reg_write(model, 'PHDMODCTRL_RSSIFLTBYP', rssifltbyp)

    # Method name: calc_adqual_regs
    # Defined in: bobcat\calculators\calc_misc.py
    def calc_adqual_regs(self, model):
        self._ip_reg_write(model, 'ADQUAL8_ADBAAGCTHR', 0)
        self._ip_reg_write(model, 'ADQUAL8_ADBAMODE', 0)
        self._ip_reg_write(model, 'ADQUAL7_ADBARSSITHR', 1023)
        self._ip_reg_write(model, 'ADQUAL7_ADBARSSIDIFF', 0)
        self._ip_reg_write(model, 'ADQUAL6_ADBACORRTHR', 65535)
        self._ip_reg_write(model, 'ADQUAL6_ADBACORRDIFF', 0)
        self._ip_reg_write(model, 'ADQUAL5_ADDIRECTCORR', 65535)
        self._ip_reg_write(model, 'ADQUAL4_ADAGCGRTHR', 63)
        self._ip_reg_write(model, 'ADQUAL4_ADRSSIGRTHR', 512)
        self._ip_reg_write(model, 'ADQUAL4_ADGRMODE', 0)
        self._ip_reg_write(model, 'ADQUAL8_ADBACORRTHR2', 0xFFFF)

    # Method name: calc_adpc_regs
    # Defined in: bobcat\calculators\calc_misc.py
    def calc_adpc_regs(self, model):
        self._ip_reg_write(model, 'ADPC10_ADBBSSAMPJUMP', 0)
        self._ip_reg_write(model, 'ADPC10_ADBBSSCHANGEEN', 0)
        self._ip_reg_write(model, 'ADPC10_ADBBSSCHGDNTHR', 0)
        self._ip_reg_write(model, 'ADPC10_ADBBSSCHGUPTHR', 0)
        self._ip_reg_write(model, 'ADPC2_ADPCPRETIMINGBAUDS', 0)
        self._ip_reg_write(model, 'ADPC2_ADPCWNDCNTRST', 0)
        self._ip_reg_write(model, 'ADPC3_ADBBSSAVGEN', 0)
        self._ip_reg_write(model, 'ADPC3_ADBBSSAVGFREEZE', 1)
        self._ip_reg_write(model, 'ADPC3_ADBBSSAVGPER', 0)
        self._ip_reg_write(model, 'ADPC3_ADBBSSAVGWAIT', 0)
        self._ip_reg_write(model, 'ADPC3_ADBBSSSELWRDATA', 0)
        self._ip_reg_write(model, 'ADPC8_ADPCANTSAMPOFFSET', 0)
        self._ip_reg_write(model, 'ADPC8_ADPCANTSAMPSWITCHWAIT', 1)
        self._ip_reg_write(model, 'ADPC8_ADPCOSR', 5)
        self._ip_reg_write(model, 'ADPC9_ADBBSSAMPAVGLIM', 0)
        self._ip_reg_write(model, 'ADPC9_ADBBSSAMPTHR', 0)
        self._ip_reg_write(model, 'ADPC9_ADBBSSDNTHR', 0)
        self._ip_reg_write(model, 'ADPC9_ADBBSSSYNCEN', 0)
        self._ip_reg_write(model, 'ADPC9_ADBBSSUPTHR', 0)
        self._ip_reg_write(model, 'ADPC2_ADENCORR32', 0)
        self._ip_reg_write(model, 'ADPC3_ADBBSSEN', 0)
        self._ip_reg_write(model, 'ADPC3_ADBBSSFILTLENGTH', 4)
        self._ip_reg_write(model, 'ADPC3_ADBBSSAMPMANT', 0)
        self._ip_reg_write(model, 'ADPC3_ADBBSSAMPEXP', 5)

    # Method name: calc_adfsm_regs
    # Defined in: bobcat\calculators\calc_misc.py
    def calc_adfsm_regs(self, model):
        self._ip_reg_write(model, 'ADFSM0_ADSTATREAD', 0)
        self._ip_reg_write(model, 'ADFSM0_ADSTAT1SEL', 0)
        self._ip_reg_write(model, 'ADFSM0_ADSTAT2SEL', 0)