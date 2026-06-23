from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
from math import ceil
from py_2_and_3_compatibility import *

#TODO; can dontcare be set here with demod select?
class CalcViterbi(IPCalculator):
    MIN_COST_THD_FULL = 600
    acqwin_unit = 1

    # Method name: calc_bcr_detector_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_bcr_detector_reg(self, model):
        rtschmode = model.vars.MODEM_REALTIMCFE_RTSCHMODE.value
        antdivmode = model.vars.antdivmode.value
        # : Disable by default
        bcrdetector_en = 0
        # : Enable Pro2 DSA detection path if antenna diversity is enabled and dual sync detection is enabled
        if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV \
                or antdivmode == model.vars.antdivmode.var_enum.ANTENNA1:
            if rtschmode == 1:
                bcrdetector_en = 1
        self._ip_reg_write(model, 'PHDMODCTRL_BCRDETECTOR', bcrdetector_en)

    # Method name: calc_demod_expect_patt_head_tail_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_demod_expect_patt_head_tail_reg(self, model):
        viterbi_demod_expect_patt_head_tail = model.vars.viterbi_demod_expect_patt_head_tail.value
        self._ip_reg_write(model, 'VTCORRCFG1_EXPECTHT', viterbi_demod_expect_patt_head_tail)

    # Method name: calc_demod_expect_patt_head_tail_value
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_demod_expect_patt_head_tail_value(self, model):
        demod_select = model.vars.demod_select.value
        preamble_pattern = model.vars.preamble_pattern.value
        mapfsk = model.vars.MODEM_CTRL0_MAPFSK.value
        if demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or \
                demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
            # Head (end of preamble) and tail bits after syncword (0)
            # Need to ensure this is only 4 bits max
            viterbi_demod_expect_patt_head_tail = int((preamble_pattern << 2) & 0xF)
            # if MAPFSK is 1 mapping is inverted so invert the expected pattern to match
            if mapfsk:
                viterbi_demod_expect_patt_head_tail ^= 0xF
            model.vars.viterbi_demod_expect_patt_head_tail.value = viterbi_demod_expect_patt_head_tail
        else:
            # set to default reset value
            model.vars.viterbi_demod_expect_patt_head_tail.value = 5

    # Method name: calc_demod_expect_patt_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_demod_expect_patt_reg(self, model):
        viterbi_demod_expect_patt = model.vars.viterbi_demod_expect_patt.value
        self._ip_reg_write(model, 'VTCORRCFG0_EXPECTPATT', viterbi_demod_expect_patt)

    # Method name: calc_demod_expect_patt_value
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_demod_expect_patt_value(self, model):
        demod_select = model.vars.demod_select.value
        syncword0 = model.vars.MODEM_SYNC0_SYNC0.value
        mapfsk = model.vars.MODEM_CTRL0_MAPFSK.value
        trecs_pre_bits_to_syncword = model.vars.trecs_pre_bits_to_syncword.value
        preamble_string = model.vars.preamble_string.value
        syncword_len = model.vars.syncword_length.value
        ber_force_sync = model.vars.ber_force_sync.value
        if demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or \
                demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
            if ber_force_sync:
                # If BER test mode is enabled then set the expected pattern to the first 32-bits of PN9 sequence
                patt = 0x052bcbb8
            else:
                syncword_str_part = '{:032b}'.format(syncword0)[-syncword_len:]  # Read the rightmost characters
                # Need to check for zero because python treats -0 the same as 0 in terms of list slicing
                if trecs_pre_bits_to_syncword > 0:
                    # We can use the full TX preamble string for this because we are reading only the rightmost characters anyway
                    preamble_str_part = preamble_string[-trecs_pre_bits_to_syncword:]  # Read the rightmost characters
                else:
                    preamble_str_part = ""
                effective_syncword_str = preamble_str_part + syncword_str_part[
                                                             ::-1] + '0' * 32  # reverse syncword part only
                # HW will add head and tail for correlation computation
                viterbi_demod_expect_patt = int(effective_syncword_str[0:32], 2)
                patt = viterbi_demod_expect_patt
            # if MAPFSK is 1 mapping is inverted so invert the expected pattern to match
            if mapfsk:
                patt ^= 0xFFFFFFFF
        else:
            # set to default reset value
            patt = long(0x123556B7)
        model.vars.viterbi_demod_expect_patt.value = patt

    # Method name: calc_expsynclen_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_expsynclen_reg(self, model):
        """ set register EXPSYNCLEN that determines RAM pointer rollback from the last write
        after TRECS recovers timing from sync word. This needs to include 2 preamble bits. It may need
        additional bits depending on delay between last write and timing acquisition
        This worked for FSK2 for wmbus.
        """
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        syncacqwinsize = model.vars.syncacqwin_actual.value
        osr = model.vars.MODEM_TRECSCFG_TRECSOSR.value
        if vtdemoden:
            expsynclen = osr * (syncacqwinsize + 4) + 2
            if expsynclen > 511:
                expsynclen = 511
        else:
            expsynclen = 0
        self._ip_reg_write(model, 'VTCORRCFG1_EXPSYNCLEN', int(expsynclen))

    # Method name: calc_freqtrackmode_reg
    # Defined in: bobcat\calculators\calc_viterbi.py
    def calc_freqtrackmode_reg(self, model):
        # Copied old Ocelot method to avoid regression impact on later parts
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        if vtdemoden:
            freqtrackmode = 1
        else:
            freqtrackmode = 0
        self._ip_reg_write(model, 'VTTRACK_FREQTRACKMODE', freqtrackmode)

    # Method name: calc_harddecision_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_harddecision_reg(self, model):
        demod_select = model.vars.demod_select.value
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        mi = model.vars.modulation_index.value
        if demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI:
            reg = 0
        elif demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
            reg = 1
        elif vtdemoden and mi >= 1.0:
            # This addresses concurrent cases where another demod may also be selected
            reg = 1
        else:
            reg = 0
        self._ip_reg_write(model, 'VITERBIDEMOD_HARDDECISION', reg)

    # Method name: calc_mincostthd_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_mincostthd_reg(self, model):
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        syncacqwin_reg = model.vars.MODEM_REALTIMCFE_SYNCACQWIN.value
        phscale_derate_factor = model.vars.phscale_derate_factor.value
        trecs_weak_syncword_optimization = model.vars.trecs_weak_syncword_optimization.value
        # If the syncword is considered weak (trecs_weak_syncword_optimization = True), the MINCOSTTHD must be optimized to avoid
        # frequency and timing error. A threshold limit is calculated, MINCOSTTHD would be below this limit.
        if vtdemoden:
            if trecs_weak_syncword_optimization:
                thd_limit = int(self.return_trecs_min_cost_limit(model))
            else:
                # No limit
                thd_limit = 1023
            reg = self.MIN_COST_THD_FULL - (32 // self.acqwin_unit - 1 - syncacqwin_reg) * (15 * self.acqwin_unit)
            reg = int(reg / phscale_derate_factor)  # Derate for PHSCALE if not set to nominal 64
            reg = min(thd_limit, reg)
        else:
            reg = 0
        self._ip_reg_write(model, 'REALTIMCFE_MINCOSTTHD', reg)

    # Method name: calc_pmacquingwin_actual
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmacquingwin_actual(self, model):
        pmacquingwin = model.vars.MODEM_TRECPMDET_PMACQUINGWIN.value
        model.vars.pmacquingwin_actual.value = self.acqwin_unit * (pmacquingwin + 1)

    # Method name: calc_pmacqwin_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmacqwin_reg(self, model):
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        preamsch_len = model.vars.preamsch_len.value
        antdivmode = int(model.vars.antdivmode.value)
        if preamsch_len >= 4 and vtdemoden:
            if antdivmode == 5 or antdivmode == 1:
                pmacqwin = 12 // self.acqwin_unit - 1  # 12 bits
            else:
                pmacqwin = preamsch_len // self.acqwin_unit - 1
        else:
            pmacqwin = 0
        self._ip_reg_write(model, 'TRECPMDET_PMACQUINGWIN', pmacqwin)

    # Method name: calc_pmcostthd_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmcostthd_reg(self, model):
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        preamsch_len = model.vars.preamsch_len.value
        pmacquingwin = model.vars.MODEM_TRECPMDET_PMACQUINGWIN.value
        freq_dev_min = model.vars.freq_dev_min.value
        freq_dev_max = model.vars.freq_dev_max.value
        deviation = model.vars.deviation.value
        antdivmode = model.vars.antdivmode.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)
        modulation_index = model.vars.modulation_index.value
        phscale_derate_factor = model.vars.phscale_derate_factor.value
        large_freq_dev = (freq_dev_min < 0.8 * deviation) or (freq_dev_max > 1.2 * deviation)
        ksi3wb = model.vars.MODEM_VTCORRCFG1_VITERBIKSI3WB.value
        trecs_optimize_cost_thd = model.vars.trecs_optimize_cost_thd.value
        # Calculate the cost threshold based on preamble detect window and deviation tolerance requirement
        if preamsch_len > 0 and vtdemoden:
            if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV or antdivmode == model.vars.antdivmode.var_enum.ANTENNA1:
                # Special values for antenna diversity
                reg = 200 if large_freq_dev else 150
            elif large_freq_dev and pmacquingwin >= (28 // self.acqwin_unit - 1):
                # Experimental results show that with PMACQUINGWIN less than  28 bits, increasing cost threshold will introduce floor
                reg = 750 - (32 // self.acqwin_unit - 1 - pmacquingwin) * (15 * self.acqwin_unit)
            else:
                if fast_detect_enable:
                    # Optimized value because our calculation isn't yet good for small windows (window size is 8)
                    if modulation_index <= 0.7:
                        reg = 100
                    else:
                        reg = 80
                else:
                    reg = 500 - (32 // self.acqwin_unit - 1 - pmacquingwin) * (15 * self.acqwin_unit)
            # Derate for PHSCALE if not set to nominal 64
            reg = int(reg / phscale_derate_factor)
            # See Jira: https://jira.silabs.com/browse/MCUW_RADIO_CFG-2380
            # Optimization of pmmin to avoid false detection
            if ksi3wb and trecs_optimize_cost_thd:  # Never set PMMINCOSTTHD = 0
                # maximum frequency error: KSI3WB * 0.4
                pmmincostthd_ksi3wb_optimization = self.acqwin_unit * (pmacquingwin + 1) * ceil(0.4 * ksi3wb)
                # Sometimes, the calculated pmmin is greater than the one chosen in the if/then statement. This is the case
                # for mode 1a (no shaping), and for antenna diversity (among others). In this case, use the fixed one, if
                # the performances are satisfying.
                reg = min(reg, pmmincostthd_ksi3wb_optimization)
        else:
            reg = 0
        self._ip_reg_write(model, 'TRECPMDET_PMMINCOSTTHD', reg)

    # Method name: calc_pmcostvalthd_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmcostvalthd_reg(self, model):
        preamsch_len = model.vars.preamsch_len.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)
        modulation_index = model.vars.modulation_index.value
        if fast_detect_enable:
            # updated as per https://jira.silabs.com/browse/MCUW_RADIO_CFG-1994
            reg = 2
        elif preamsch_len <= 16:
            reg = 2
        elif preamsch_len <= 24:
            reg = 3
        else:
            reg = 4
        self._ip_reg_write(model, 'TRECPMDET_PMCOSTVALTHD', reg)

    # Method name: calc_pmdeten_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmdeten_reg(self, model):
        # Update: We found these bugs caused by PMDETEN, so disabling PMDET
        # https://jira.silabs.com/browse/IPMCUSRW-997
        # https://jira.silabs.com/browse/IPMCUSRW-999
        pmdeten = 0
        # Write the register
        self._ip_reg_write(model, 'PHDMODCTRL_PMDETEN', pmdeten)

    # Method name: calc_pmdetthd_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmdetthd_reg(self, model):
        # Always set to 8 for now
        self._ip_reg_write(model, 'PHDMODCTRL_PMDETTHD', 8)

    # Method name: calc_pmendschen
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmendschen(self, model):
        # This function enables a timeout for frame detect based on the end of preamble
        # Read in model vars
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        rtschmode = model.vars.MODEM_REALTIMCFE_RTSCHMODE.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)
        # Calculate the register
        if vtdemoden:
            if rtschmode == 1 and fast_detect_enable:
                # If we are using hard slicing, then we can enable PMENDSCH
                # Only do this if we are in a PSM case
                pmendschen = 1
            else:
                pmendschen = 0
        else:
            pmendschen = 0
        # Write the register
        self._ip_reg_write(model, 'FRMSCHTIME_PMENDSCHEN', pmendschen)

    # Method name: calc_pmexpectpatt_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmexpectpatt_reg(self, model):
        pre_str = model.vars.preamble_string.value
        mapfsk = model.vars.MODEM_CTRL0_MAPFSK.value
        demod_sel = model.vars.demod_select.value
        trecs_effective_preamble_len = model.vars.trecs_effective_preamble_len.value
        # Only calculate pmexpectpatt for TRECS or BCR (BCR reuses this reg)
        if demod_sel == model.vars.demod_select.var_enum.TRECS_VITERBI or demod_sel == model.vars.demod_select.var_enum.TRECS_SLICER or demod_sel == model.vars.demod_select.var_enum.BCR:
            # We can use the TX preamble string for this, becuase we only use a small number of bits corresponding to the eff preamble len
            effective_pre_str = pre_str[
                                :trecs_effective_preamble_len]  # This is the preamble once some bits are shifted to the syncword
            zero_filler_str = '0' * 32  # Add 32 zeroes to the end to make sure we have a long enough string
            combined_str = effective_pre_str + zero_filler_str
            # if PM search is enabled set pattern to preamble string
            # then convert binary string to integer to write into register field
            reg = int(combined_str[0:32], 2)
            # if MAPFSK is 1 mapping is inverted so invert the expected pattern to match
            if mapfsk:
                reg ^= 0xFFFFFFFF
        else:
            reg = 0
        self._ip_reg_write(model, 'TRECPMPATT_PMEXPECTPATT', reg)

    # Method name: calc_pmoffset_reg
    # Defined in: rainier\calculators\calc_viterbi.py
    def calc_pmoffset_reg(self, model):
        afc_oneshot_enabled = (model.vars.MODEM_AFC_AFCONESHOT.value == 1)
        rtschmode = model.vars.MODEM_REALTIMCFE_RTSCHMODE.value
        osr = model.vars.MODEM_TRECSCFG_TRECSOSR.value
        if (rtschmode == 1) and afc_oneshot_enabled:
            # Special case for dual syncword detection case where hard slicing on syncword is required
            # In this case we choose a minimal PMOFFSET to avoid a bad estimate due to AFC transient
            pmoffset = 2
        else:
            # + 2 for processing delay. Always a function of OSR as per Wentao
            pmoffset = osr * 2 + 2
        self._ip_reg_write(model, 'TRECSCFG_PMOFFSET', pmoffset)

    # Method name: calc_pmtimeoutsel_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmtimeoutsel_reg(self, model):
        preamble_length = model.vars.preamble_length.value  # This is the TX preamble length
        sync_len = model.vars.syncbits_actual.value
        # first approximation time out should be total length of TX preamble and sync word
        # we add a margin of half the sync_len for extreme test cases
        total_len = int(preamble_length + sync_len * 1.5)
        # set closest setting possible based on total_len
        if total_len <= 16 or total_len == 0:
            reg = 0
        elif total_len <= 24:
            reg = 1
        elif total_len <= 32:
            reg = 2
        else:
            reg = 3
        if total_len > 65535:
            total_len = 65535
        self._ip_reg_write(model, 'TRECPMDET_PMTIMEOUTSEL', reg)
        self._ip_reg_write(model, 'FRMSCHTIME_FRMSCHTIME', total_len)

    # Method name: calc_pmtimlosen_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmtimlosen_reg(self, model):
        # Read in model variables
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        pmdeten = model.vars.MODEM_PHDMODCTRL_PMDETEN.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)
        if vtdemoden and fast_detect_enable:
            pmtimlosen = 1
        else:
            pmtimlosen = 0
        # Write the register
        self._ip_reg_write(model, 'PHDMODCTRL_PMTIMLOSEN', pmtimlosen)

    # Method name: calc_pmtimlosthd_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_pmtimlosthd_reg(self, model):
        # Read in model variables
        pmtimlosen = model.vars.MODEM_PHDMODCTRL_PMTIMLOSEN.value
        pmmincostthd = model.vars.MODEM_TRECPMDET_PMMINCOSTTHD.value
        if pmtimlosen:
            pmtimlosthd = int(1.5 * pmmincostthd)
        else:
            pmtimlosthd = 0
        # Write the register (with saturation since if pmmincostthd is large we might overflow)
        self._ip_reg_write(model, 'PHDMODCTRL_PMTIMLOSTHD', pmtimlosthd, check_saturation=True)

    # Method name: calc_preamsch_len
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_preamsch_len(self, model):
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        ber_force_fdm0 = model.vars.ber_force_fdm0.value
        symbols_in_timing_window = model.vars.symbols_in_timing_window.value
        if vtdemoden and not ber_force_fdm0:
            preamsch_len = symbols_in_timing_window
        else:
            # Not using TRECS, or in BER test mode
            preamsch_len = 0
        model.vars.preamsch_len.value = preamsch_len

    # Method name: calc_preamsch_reg
    # Defined in: lynx\calculators\calc_viterbi.py
    def calc_preamsch_reg(self, model):
        # The preamsch len is the effective preamble length minus delay bits
        preamsch_len = model.vars.preamsch_len.value
        # If the preamble search length is set to 0 just do syncword detection
        if preamsch_len == 0:
            reg = 0
        else:
            reg = 1
        self._ip_reg_write(model, 'TRECPMDET_PREAMSCH', reg)

    # Method name: calc_realtimcfe_extenschbyp_reg
    # Defined in: rainier\calculators\calc_viterbi.py
    def calc_realtimcfe_extenschbyp_reg(self, model):
        pass

    # Method name: calc_realtimcfe_rtschmode_reg
    # Defined in: rainier\calculators\calc_viterbi.py
    def calc_realtimcfe_rtschmode_reg(self, model):
        # This function calculates the RTSCHMODE register field for TRECS
        # Read in model variables
        dualsync = model.vars.syncword_dualsync.value
        demod_select = model.vars.demod_select.value
        ber_force_fdm0 = model.vars.ber_force_fdm0.value
        pmdeten = model.vars.MODEM_PHDMODCTRL_PMDETEN.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)
        # Calculate the register value based on whether we are using TRECS and whether dual syncword detect is enabled
        if demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or \
                demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
            # If dual syncword detection is enabled, then stop using CFE and hard slice syncword w TRECS
            if fast_detect_enable:
                rtschmode = 1
            else:
                rtschmode = 0  # 0 means detect timing again using syncword
        else:
            rtschmode = 0
        # Write the register
        self._ip_reg_write(model, 'REALTIMCFE_RTSCHMODE', rtschmode)

    # Method name: calc_realtimcfe_trackingwin
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_realtimcfe_trackingwin(self, model):
        # This function calculates the REALTIMCFE_TRACKINGWIN reg field
        # Read in model variables
        baudrate_tol_ppm = model.vars.baudrate_tol_ppm.value
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        freq_offset_hz = model.vars.freq_offset_hz.value
        modulation_index = model.vars.modulation_index.value
        baudrate = model.vars.baudrate.value
        if vtdemoden:
            # If the tol request is at least 5000ppm, then reduce the tracking win size
            if baudrate_tol_ppm >= 5000:
                trackingwin = 5
            elif (freq_offset_hz / baudrate) > 0.57 and modulation_index <= 0.5:
                trackingwin = 2
            else:
                trackingwin = 7
        else:
            trackingwin = 0
        # Write the reg
        self._ip_reg_write(model, 'REALTIMCFE_TRACKINGWIN', trackingwin)

    # Method name: calc_realtimcfe_vtafcframe_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_realtimcfe_vtafcframe_reg(self, model):
        # This function calculates the REALTIMCFE_VTAFCFRAME reg field
        # Read in model vars
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        # Calculate the reg
        if vtdemoden:
            # Constantly update digmix based on freq offset estimates each trackingwin
            vtafcframe = 1
        else:
            vtafcframe = 0
        # Write the register
        self._ip_reg_write(model, 'REALTIMCFE_VTAFCFRAME', vtafcframe)

    # Method name: calc_remodoutsel_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_remodoutsel_reg(self, model):
        # always set to 1 for now. This feeds datafilter output into TRECS if remoden is 1.
        # note that phscale is still in the path even though the datafilter output is a frequency signal
        # if remodoutsel == 0 and (remoden == 1 and remoddwn == 0) -> input is datafilter output before TRECS DSA and DEC2 output after
        # if remodoutsel == 1 and (remoden == 1 and remoddwn == 0) -> input is taken from datafilter output
        # if remodoutsel == 2 and (remoden == 1 and remoddwn == 0) -> input is taken from DEC2 output
        # if remodoutsel == 3 -> input is from remodulated sliced signal before TRECS DSA and DEC2 output after
        # if remodoutsel < 3 and (remoden == 0 or remoddwn != 0) -> input is taken from remodulated sliced signal
        self._ip_reg_write(model, 'PHDMODCTRL_REMODOUTSEL', 1)

    # Method name: calc_rtcfeen_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_rtcfeen_reg(self, model):
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        reg = 1 if vtdemoden else 0
        self._ip_reg_write(model, 'REALTIMCFE_RTCFEEN', reg)

    # Method name: calc_rtschwin_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_rtschwin_reg(self, model):
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        preamsch_len = model.vars.preamsch_len.value
        preamble_pattern_len = model.vars.preamble_pattern_len.value
        if vtdemoden:
            if (preamsch_len <= 24) and (preamble_pattern_len == 2):
                reg = 4
            else:
                reg = 5
        else:
            reg = 0
        self._ip_reg_write(model, 'REALTIMCFE_RTSCHWIN', reg)

    # Method name: calc_shift_trecs_pre_bits_to_syncword
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_shift_trecs_pre_bits_to_syncword(self, model):
        # This method calculates how many bits to shift from premable to syncword when using TRECS
        # The goal is to strengthen correlation
        demod_select = model.vars.demod_select.value
        preamble_detection_length = model.vars.preamble_detection_length.value
        delay_samp = model.vars.grpdelay_to_demod.value
        osr = model.vars.oversampling_rate_actual.value
        rtschmode_actual = model.vars.MODEM_REALTIMCFE_RTSCHMODE.value
        ber_force_sync = model.vars.ber_force_sync.value
        antdivmode = model.vars.antdivmode.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)
        is_trecs = demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or \
                   demod_select == model.vars.demod_select.var_enum.TRECS_SLICER
        if ber_force_sync:
            syncword_len = 32
        else:
            syncword_len = model.vars.syncword_length.value
        if demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or \
                demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
            if antdivmode == model.vars.antdivmode.var_enum.PHDEMODANTDIV or antdivmode == model.vars.antdivmode.var_enum.ANTENNA1:
                target_cfe_len = 16  # 20 # If antenna diversity enabled, reduce window so smaller preamble can be used
            else:
                target_cfe_len = 32  # The goal is to end up with a 32 bit window, length must end up as a mult of 4
            delay_symbols = int(ceil(delay_samp / osr))  # Calculate the group delay in symbols
            min_pre_len = 26 + delay_symbols  # Need to leave at least 26 preamble bits after delay so that we can enable preamsch and AFC
            min_pre_no_preamsch_len = 8  # Need to leave 8 bits of preamble if preamsch is disabled
            if (syncword_len < target_cfe_len) and (
                    rtschmode_actual == 0) and not fast_detect_enable and not ber_force_sync:
                # We want to shift some preamble bits to the syncword
                # Skip this if using RTSCHMODE=1 (hard slicing)
                cfe_len_shortage = target_cfe_len - syncword_len
                # Check if we have a long enough preamble to accommodate moving bits to the syncword while leaving
                # at least the minimum number of preamble bits
                if preamble_detection_length >= cfe_len_shortage + min_pre_len:
                    trecs_pre_bits_to_syncword = cfe_len_shortage  # Resulting CFE len is equal to target
                elif preamble_detection_length >= min_pre_len:
                    # If the preamble is not long enough, then only move enough bits to leave the min preamble bits
                    # If the preamble is exactly the minimum length then this won't move any bits
                    trecs_pre_bits_to_syncword = preamble_detection_length - min_pre_len
                elif preamble_detection_length > min_pre_no_preamsch_len:
                    # If we are going to turn off preamble search and AFC anyway, then just leave a minimal number of bits
                    # But make sure to not move more bits than the CFE length shortage
                    trecs_pre_bits_to_syncword = min(preamble_detection_length - min_pre_no_preamsch_len,
                                                     cfe_len_shortage)
                else:
                    # The preamble is too short to be able to move any bits
                    trecs_pre_bits_to_syncword = 0
            else:
                # The syncword is already long enough to meet our target CFE length, or we are using RTSCHMODE=1, or BER test
                trecs_pre_bits_to_syncword = 0
        else:
            # Not using TRECS
            trecs_pre_bits_to_syncword = 0
        # The resulting CFE length needs to be a multiple of 4, so if it's not then move less preamble bits
        if trecs_pre_bits_to_syncword > 0:
            cfe_len_expected = syncword_len + trecs_pre_bits_to_syncword
            correction_factor = cfe_len_expected % 4
            trecs_pre_bits_to_syncword = trecs_pre_bits_to_syncword - correction_factor
        model.vars.trecs_pre_bits_to_syncword.value = trecs_pre_bits_to_syncword
        model.vars.trecs_effective_preamble_len.value = preamble_detection_length - trecs_pre_bits_to_syncword
        model.vars.trecs_effective_syncword_len.value = syncword_len + trecs_pre_bits_to_syncword
        # : display log output if trecs
        model.vars.trecs_pre_bits_to_syncword.in_public_log = is_trecs
        model.vars.trecs_effective_preamble_len.in_public_log = is_trecs
        model.vars.trecs_effective_syncword_len.in_public_log = is_trecs

    # Method name: calc_swcoeffen_reg
    # Defined in: lpwh72000\calculators\calc_viterbi.py
    def calc_ksi3swen_reg(self, model):
        afc1shot_en = model.vars.MODEM_AFC_AFCONESHOT.value
        aox_en = model.vars.aox_enable.value == model.vars.aox_enable.var_enum.ENABLED
        # ksi3swen is do not care if afc1shot_en is False - MCUW_RADIO_CFG-1901
        ksi3swen_donotccare = not afc1shot_en
        if afc1shot_en and aox_en:
            # both AFC oneshot and AoX cannot be simultaneously enabled as they both use the second CHF coefficient set
            LogMgr.Error('both AFC oneshot and AoX cannot be simultaneously enabled')
        ksi3swenable = afc1shot_en
        # don't switch for aox, as KSI3 switch mechanism is based on dsa/preamble, but the aox channel switch is based on the CTE
        # Don't care about the demodulated data during CTE, so just leave it on the KSI3
        self._ip_reg_write(model, 'VTCORRCFG1_KSI3SWENABLE', ksi3swenable, do_not_care=ksi3swen_donotccare)

    # Method name: calc_syncacqwin_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_syncacqwin_reg(self, model):
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        trecs_effective_syncword_len = model.vars.trecs_effective_syncword_len.value
        if vtdemoden:
            syncacqwin = trecs_effective_syncword_len // self.acqwin_unit - 1
        else:
            syncacqwin = 0
        self._ip_reg_write(model, 'REALTIMCFE_SYNCACQWIN', syncacqwin)

    # Method name: calc_synthafc_reg
    # Defined in: bobcat\calculators\calc_viterbi.py
    def calc_synthafc_reg(self, model):
        demod_select = model.vars.demod_select.value
        afc1shot_en = model.vars.MODEM_AFC_AFCONESHOT.value
        ber_force_freq_comp_off = model.vars.ber_force_freq_comp_off.value
        do_not_care = False
        if ber_force_freq_comp_off:
            reg = 1
        # : If Legacy, set if oneshot afc is enabled
        elif demod_select == model.vars.demod_select.var_enum.LEGACY:
            if afc1shot_en:
                reg = 1
            else:
                reg = 0
        # : If TRECS, always set SYNTHAFC = 1
        elif demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or \
                demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
            reg = 1
        # : Not used by BCR, Coherent, or Longrange
        else:
            do_not_care = True
            reg = 0
        self._ip_reg_write(model, 'VITERBIDEMOD_SYNTHAFC', reg, do_not_care=do_not_care)

    # Method name: calc_trecs_demod_enable
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_trecs_demod_enable(self, model):
        pass

    # Method name: calc_trecs_optimize_cost_thd
    # Defined in: rainier\calculators\calc_viterbi.py
    def calc_trecs_optimize_cost_thd(self, model):
        trecs_enabled = model.vars.trecs_enabled.value
        protocol_id = model.vars.protocol_id.value
        is_ble = protocol_id == model.vars.protocol_id.var_enum.BLE
        enable_opt = trecs_enabled and not is_ble
        model.vars.trecs_optimize_cost_thd.value = enable_opt

    # Method name: calc_trecs_syncword_timeout_us
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_trecs_syncword_timeout_us(self, model):
        frmschtime = model.vars.MODEM_FRMSCHTIME_FRMSCHTIME.value
        baudrate = model.vars.baudrate.value
        demod_select = model.vars.demod_select.value
        is_trecs = demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or \
                   demod_select == model.vars.demod_select.var_enum.TRECS_SLICER
        model.vars.trecs_syncword_timeout_us.value = frmschtime / baudrate * 1e6
        # : display log output if trecs demod
        model.vars.trecs_syncword_timeout_us.in_public_log = is_trecs

    # Method name: calc_trecs_weak_syncword_optimization
    # Defined in: rainier\calculators\calc_viterbi.py
    def calc_trecs_weak_syncword_optimization(self, model):
        trecs_enabled = model.vars.trecs_enabled.value
        protocol_id = model.vars.protocol_id.value
        is_ble = protocol_id == model.vars.protocol_id.var_enum.BLE
        enable_opt = trecs_enabled and not is_ble
        model.vars.trecs_weak_syncword_optimization.value = enable_opt

    # Method name: calc_viterbi_misc_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_viterbi_misc_reg(self, model):
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        ber_force_freq_comp_off = model.vars.ber_force_freq_comp_off.value
        self._ip_reg_write(model, 'REALTIMCFE_SINEWEN', 0)
        self._ip_reg_write(model, 'TRECPMDET_COSTHYST', 0)
        self._ip_reg_write(model, 'VITERBIDEMOD_CORRCYCLE', 0)
        self._ip_reg_write(model, 'VTBLETIMING_FLENOFF', 0)
        self._ip_reg_write(model, 'VTTRACK_FREQBIAS', 0)
        self._ip_reg_write(model, 'VTTRACK_TIMGEAR', 0)
        self._ip_reg_write(model, 'PHDMODCTRL_BCRTRECSCONC', 0)
        self._ip_reg_write(model, 'PHDMODCTRL_BCRLEGACYCONC', 0)
        # self._ip_reg_write(model, 'VTCORRCFG1_VITERBIKSI3WB', 0)
        self._ip_reg_write(model, 'TRECSCFG_SDSCALE', 3)
        if vtdemoden:
            # these register fields have a fixed value for now
            self._ip_reg_write(model, 'VITERBIDEMOD_CORRSTPSIZE', 4)
            self._ip_reg_write(model, 'VTBLETIMING_DISDEMODOF', 1)
            self._ip_reg_write(model, 'VTBLETIMING_TIMINGDELAY', 60)
            self._ip_reg_write(model, 'VTTRACK_HIPWRTHD', 1)
            self._ip_reg_write(model, 'VTTRACK_TIMTRACKTHD', 2)
            self._ip_reg_write_default(model, 'VTTRACK_TIMEACQUTHD')
        else:
            self._ip_reg_write(model, 'VITERBIDEMOD_CORRSTPSIZE', 0)
            self._ip_reg_write(model, 'VTBLETIMING_DISDEMODOF', 0)
            self._ip_reg_write(model, 'VTBLETIMING_TIMINGDELAY', 0)
            self._ip_reg_write(model, 'VTTRACK_HIPWRTHD', 0)
            self._ip_reg_write(model, 'VTTRACK_TIMTRACKTHD', 0)
            self._ip_reg_write(model, 'VTTRACK_TIMEACQUTHD', default=True, do_not_care=True)

    # Method name: calc_vtbletimingsel_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_vtbletimingsel_reg(self, model):
        # This function calculates the MODEM_VTBLETIMING_VTBLETIMINGSEL field
        # Always set to 0 now, this field only needs to be set when the old "viterbi demodulator" is used, which
        # is replaced as of Lynx with TRECS
        self._ip_reg_write(model, 'VTBLETIMING_VTBLETIMINGSEL', 0)

    # Method name: calc_vtdemoden_reg
    # Defined in: rainier\calculators\calc_viterbi.py
    def calc_vtdemoden_reg(self, model):
        demod_sel = model.vars.demod_select.value
        dssscfe_combo = model.vars.MODEM_DIGMIXCTRL_DSSSCFECOMBO.value
        # VTDEMODEN is set if: the selected demod uses the TRECS
        # Or if the CFE of the TRECS is used along the DSSS correlator for timing and detection (dssscfecombo)
        if (demod_sel == model.vars.demod_select.var_enum.TRECS_VITERBI
                or demod_sel == model.vars.demod_select.var_enum.TRECS_SLICER
                or dssscfe_combo):
            reg = 1
        else:
            reg = 0
        self._ip_reg_write(model, 'VITERBIDEMOD_VTDEMODEN', reg)

    # Method name: calc_vtfreqlim_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_vtfreqlim_reg(self, model):
        vtdemoden = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        freq_offset_hz = model.vars.freq_offset_hz.value
        rf_freq_hz = model.vars.base_frequency_hz.value * 1.0
        baudrate = model.vars.baudrate.value
        # Frequency offset is never exactly zero. To be conservative we act like xtal tol is at least 1ppm for rx/tx.
        freq_offset_hz_min = (2) * rf_freq_hz / 1e6
        freq_offset_hz = max(freq_offset_hz_min, freq_offset_hz)
        # limit is actually offset/baudrate but we don't want this to have an effect on frequency offset
        # performance so we multiply result by 2 to have margin
        val = (20 + (1.2 * 2 * 256 * freq_offset_hz / baudrate)) if vtdemoden else 0
        # make sure we can fit result into register
        reg = int(511 if val > 511 else val)
        self._ip_reg_write(model, 'VTCORRCFG1_VTFRQLIM', reg)

    # Method name: calc_vtpmdetsel_reg
    # Defined in: ocelot\calculators\calc_viterbi.py
    def calc_vtpmdetsel_reg(self, model):
        pass

    # Method name: return_trecs_min_cost_limit
    # Defined in: ocelot\calculators\calc_viterbi.py
    def return_trecs_min_cost_limit(self, model):
        """After the preamble detection and before the syncword detection, if the expected pattern
        (viterbi_demod_expect_patt) is similar to a preamble, there is a chance the CFE uses the preamble
        instead of the expected pattern to adjust timing and frequency. If the Tx frequency is offset, there
        is a risk the adjustment is impaired and the packet wrong, resulting in a CRC error. This method
        returns the minimum cost that can be measured when the CFE slide in a preamble pattern,
        shifted in frequency and timing. The returned value is used to calculate MINCOSTTHD."""
        ksi1 = model.vars.ksi1.value
        ksi2 = model.vars.ksi2.value
        ksi3 = model.vars.ksi3.value
        cost_thd_min_offset = -20
        # 20 is substracted to make sure we are below the calculated limit.
        # Experimentally found in https://jira.silabs.com/browse/MCUW_RADIO_CFG-2429
        # For the specific customer, the experimental threshold value is 140. The calculated value is 158.
        if not ksi1:  # Viterbi is not used
            return 0
        expectpatt = model.vars.viterbi_demod_expect_patt.value
        syncacqwin_reg = model.vars.MODEM_REALTIMCFE_SYNCACQWIN.value
        head_and_tail = model.vars.viterbi_demod_expect_patt_head_tail.value
        # Expected pattern
        pre_tail = "{:04b}".format(
            head_and_tail)  # The bit before and after the expected pattern, necessary to calculate first and last ksis values
        expectpatt_len = self.acqwin_unit * (1 + syncacqwin_reg)
        expected_pattern = pre_tail[1] + "{:032b}".format(expectpatt)[:expectpatt_len] + pre_tail[-1]
        # Expected signal
        ksis = [-ksi1, -ksi2, ksi3, ksi2, -ksi2, -ksi3, ksi2, ksi1]
        expected_signal = [ksis[int(expected_pattern[i - 1:i + 2], 2)] for i in range(1, len(expected_pattern) - 1)]
        cost_frequency = []
        cost_timing = []
        # Calculate the cost between the cost of a preamble signal shifted in frequency.
        # i = -ksi1 means means offset = - freq dev
        # i = +ksi1 means offset = + freq dev
        # Frequency range from -2*dev to +2*dev (usually the problem occurs at +- freq dev)
        for i in range(-2 * ksi1, 2 * ksi1):
            # Unwanted signal: preamble signal shifted in frequency
            unwanted_signal_frequency = [-ksi3 + i, ksi3 + i] * int(expectpatt_len / 2)
            # Cost = abs( sum( ksi[i] - phase_diff[i] ) )
            cost_frequency.append(
                sum([min(abs(unwanted_signal_frequency[j] - expected_signal[j]), 32)
                     for j in range(len(unwanted_signal_frequency))]))
        # Calculate the cost between the cost of a preamble signal shifted in timing.
        # i = -ksi3 means the cost is calculated with a signal = 10101010...
        # i = ksi3 means 01010101
        # i = 0 means phase_diff = 0 (the CFE reads the signal at the zero crossing)
        for i in range(-ksi3, ksi3):
            unwanted_signal_timing = [i, -i] * int(expectpatt_len / 2)
            cost_timing.append(
                sum([min(abs(unwanted_signal_timing[j] - expected_signal[j]), 32)
                     for j in range(len(unwanted_signal_timing))]))
        # Return the minimum of the 2 calculated values (positive)
        return max(0, min(cost_frequency + cost_timing) + cost_thd_min_offset)
