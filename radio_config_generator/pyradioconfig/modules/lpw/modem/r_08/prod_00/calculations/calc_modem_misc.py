from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
import math
class CalcModemMisc(IPCalculator):
    #FIXME: Please find right place for me
    def calc_modem_misc(self, model):
        self._ip_reg_write_default(model, 'EXPECTPATTDUAL_EXPECTPATTDUAL')
        self._ip_reg_write_default(model, 'DUALTIM_DUALTIMEN')
        self._ip_reg_write_default(model, 'DUALTIM_MINCOSTTHD2')
        self._ip_reg_write_default(model, 'DUALTIM_SYNCACQWIN2')
        self._ip_reg_write_default(model, 'PHDMODCTRL_CHPWRQUAL')
        self._ip_reg_write_default(model, 'CTRL3_ANTDIVMODE')
        self._ip_reg_write_default(model, 'DIGMIXCTRL_BLEORZB')
        self._ip_reg_write_default(model, 'DIGMIXCTRL_MULTIPHYHOP')
        self._ip_reg_write_default(model, 'DIGMIXCTRL_RXBRINTSHIFT')
        self._ip_reg_write_default(model, 'DIGMIXCTRL_DSSSCFECOMBO')
        self._ip_reg_write(model, 'SYNC2_SYNC2', 0)
        self._ip_reg_write_default(model, 'SYNC3_SYNC3')
        self._ip_reg_write_default(model, 'COCURRMODE_DSSSDSACHK')
        self._ip_reg_write_default(model, 'COCURRMODE_TRECSDSACHK')
        self._ip_reg_write_default(model, 'COCURRMODE_CORRCHKMUTE')
        self._ip_reg_write_default(model, 'SYNCWORDCTRL_SYNCBITS2TH')
        self._ip_reg_write_default(model, 'SYNCWORDCTRL_SYNC3ERRORS')
        self._ip_reg_write_default(model, 'SYNCWORDCTRL_DUALSYNC2TH')
        self._ip_reg_write_default(model, 'SYNCWORDCTRL_SYNCSWFEC')

        # Added new reg-fields related to 15.4 subG OQPSK phys
        self._ip_reg_write(model, 'COH3_COHDSACMPLX', 0)
        self._ip_reg_write(model, 'SYNCPROPERTIES_STATICSYNCTHRESH', 0)

        # Modem Registers with fixed value
        self._ip_reg_write(model, 'CTRL0_DEMODRAWDATASEL', 0)
        self._ip_reg_write(model, 'CTRL2_DMASEL', 0)
        # self._ip_reg_write(model, 'CTRL3_PRSDINEN', 0)
        self._ip_reg_write(model, 'CTRL4_CLKUNDIVREQ', 0)
        self._ip_reg_write(model, 'CTRL3_RAMTESTEN', 0)
        # self._ip_reg_write(model, 'DIRECTMODE_CLKWIDTH', 1)
        # self._ip_reg_write(model, 'DIRECTMODE_DMENABLE', 0)
        # self._ip_reg_write(model, 'DIRECTMODE_SYNCASYNC', 0)
        # self._ip_reg_write(model, 'DIRECTMODE_SYNCPREAM', 3)
        # self._ip_reg_write(model, 'PADEBUG_ENMANPACLKAMPCTRL', 0)
        # self._ip_reg_write(model, 'PADEBUG_ENMANPAPOWER', 0)
        # self._ip_reg_write(model, 'PADEBUG_ENMANPASELSLICE', 0)
        # self._ip_reg_write(model, 'PADEBUG_MANPACLKAMPCTRL', 0)
        # self._ip_reg_write(model, 'CTRL0_OOKASYNCPIN', 0)
        self._ip_reg_write(model, 'CTRL0_DUALCORROPTDIS', 0)
        self._ip_reg_write(model, 'CTRL0_FRAMEDETDEL', 0)
        self._ip_reg_write(model, 'CTRL1_SYNC1INV', 0)

        # Clock-gating register
        self._ip_reg_write(model, 'AUTOCG_AUTOCGEN', 0) #We calculate MODEM_CGCLKSTOP_FORCEOFF in calculator instead

        # Coherent Demod Registers
        #FIXME: Check with Yan/Per on how to calculate these
        self._ip_reg_write(model, 'COH2_DSAPEAKCHPWRTH', 0)
        self._ip_reg_write(model, 'COH3_COHDSADETDIS', 0)
        self._ip_reg_write(model, 'COH3_DSAPEAKCHPWREN', 0)
        self._ip_reg_write(model, 'COH3_LOGICBASEDCOHDEMODGATE', 0)
        self._ip_reg_write(model, 'COH3_ONEPEAKQUALEN', 0)
        self._ip_reg_write(model, 'COH3_PEAKCHKTIMOUT', 0)

        # Long Range registers
        # FIXME: calculate these
        self._ip_reg_write(model, 'LONGRANGE1_LOGICBASEDLRDEMODGATE', 0)
        self._ip_reg_write(model, 'LONGRANGE1_LOGICBASEDPUGATE', 0)
        self._ip_reg_write(model, 'LONGRANGE1_LRSPIKETHADD', 0)
        self._ip_reg_write(model, 'LONGRANGE1_LRSS', 0)
        self._ip_reg_write(model, 'LRFRC_CI500', 1)
        self._ip_reg_write(model, 'LRFRC_FRCACKTIMETHD', 0)
        self._ip_reg_write(model, 'LRFRC_LRCORRMODE', 1)

        # Legacy Demod Registers
        # FIXME: calculate these

        self._ip_reg_write(model, 'CTRL2_BRDIVA', 0)
        self._ip_reg_write(model, 'CTRL2_BRDIVB', 0)
        # self._ip_reg_write(model, 'CTRL2_DEVMULA', 0)
        # self._ip_reg_write(model, 'CTRL2_DEVMULB', 0)
        self._ip_reg_write(model, 'CTRL2_RATESELMODE', 0)
        self._ip_reg_write(model, 'CTRL2_SQITHRESH', 0)
        # self._ip_reg_write(model, 'CTRL2_TXPINMODE', 0)
        self._ip_reg_write(model, 'CTRL4_ADCSATDENS', 0)
        self._ip_reg_write(model, 'CTRL4_ADCSATLEVEL', 6)
        self._ip_reg_write(model, 'CTRL4_OFFSETPHASESCALING', 0)
        self._ip_reg_write(model, 'CTRL4_PHASECLICKFILT', 0)
        self._ip_reg_write(model, 'CTRL4_SOFTDSSSMODE', 0)
        self._ip_reg_write(model, 'CTRL5_DEMODRAWDATASEL2', 0)
        self._ip_reg_write(model, 'CTRL5_DETDEL', 0)
        self._ip_reg_write(model, 'CTRL5_POEPER', 0)
        self._ip_reg_write(model, 'CTRL5_RESYNCLIMIT', 0)
        # self._ip_reg_write(model, 'CTRL6_CODINGB', 0)
        self._ip_reg_write(model, 'CTRL6_CPLXCORREN', 0)
        self._ip_reg_write(model, 'CTRL6_DEMODRESTARTALL', 0)
        self._ip_reg_write(model, 'CTRL6_DSSS3SYMBOLSYNCEN', 0)
        self._ip_reg_write(model, 'CTRL6_PREBASES', 0)
        self._ip_reg_write(model, 'CTRL6_RXRESTARTUPONRSSI', 0)
        self._ip_reg_write(model, 'CTRL6_RXRESTARTUPONSHORTRSSI', 0)
        # self._ip_reg_write(model, 'CTRL6_TXDBPSKINV', 0)
        # self._ip_reg_write(model, 'CTRL6_TXDBPSKRAMPEN', 0)
        # self._ip_reg_write(model, 'ANARAMPCTRL_VMIDCTRL', 1)
        # self._ip_reg_write(model, 'ANARAMPCTRL_MUTEDLY', 0)
        self._ip_reg_write(model, 'ETSTIM_ETSCOUNTEREN', 0)
        self._ip_reg_write(model, 'ETSTIM_ETSTIMVAL', 0)

        # self._ip_reg_write(model, 'PRE_DSSSPRE', 0)
        # self._ip_reg_write(model, 'PRE_PRESYMB4FSK', 0)
        self._ip_reg_write(model, 'PRE_SYNCSYMB4FSK', 0)
        self._ip_reg_write(model, 'TIMING_FASTRESYNC', 0)
        self._ip_reg_write(model, 'TIMING_TIMSEQINVEN', 0)
        self._ip_reg_write(model, 'TIMING_TIMSEQSYNC', 0)
        self._ip_reg_write(model, 'TIMING_TSAGCDEL', 0)

        # Added new reg-fields related to Internal Long Range
        self._ip_reg_write(model, 'PRE_PREWNDERRORS', 0)
        self._ip_reg_write(model, 'CTRL3_TIMINGBASESGAIN', 0)


        # reg-fields to modify sync detection reset behavior PGOCELOT-5282
        self._ip_reg_write(model, 'FRMSCHTIME_PMRSTSYCNEN', 0)
        self._ip_reg_write(model, 'FRMSCHTIME_DSARSTSYCNEN', 0)

        self._ip_reg_write(model, 'LRFRC_LRDSACORRTHD', 1000)

        # Add LongRange reg writes
        self._ip_reg_write(model, 'LONGRANGE_LRBLE', 0)
        self._ip_reg_write(model, 'LONGRANGE_LRBLEDSA', 0)
        self._ip_reg_write(model, 'LONGRANGE_LRCORRSCHWIN', 0xA)
        self._ip_reg_write(model, 'LONGRANGE_LRCORRTHD', 0x3E8)
        self._ip_reg_write(model, 'LONGRANGE_LRDEC', 0)
        self._ip_reg_write(model, 'LONGRANGE_LRTIMCORRTHD', 0x0FA)

        self._ip_reg_write(model, 'COCURRMODE_CONCURRENT', 0)

        self._ip_reg_write(model, 'CTRL5_BBSS', 0)

    # Method name: calc_in_2fsk_opt_scope
    # Defined in: jumbo\calculators\calc_misc.py
    def calc_in_2fsk_opt_scope(self, model):
        # This function determines if a PHY is in 2FSK optimization scope

        modulation_type = model.vars.modulation_type.value
        viterbi_en_reg = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value
        antdivmode = model.vars.antdivmode.value
        part_family = model.part_family
        profile = model.profile.name
        dsss_len = model.vars.dsss_len.value
        etsi_cat1_compatible = model.vars.etsi_cat1_compatible.value

        is_2fsk = modulation_type == model.vars.modulation_type.var_enum.FSK2
        viterbi_en = viterbi_en_reg == 1
        antdiv_off = antdivmode == model.vars.antdivmode.var_enum.DISABLE
        in_supported_profile = profile.lower() in ['base', 'sidewalk']
        not_spread = dsss_len == 0
        is_etsi = (etsi_cat1_compatible == model.vars.etsi_cat1_compatible.var_enum.Band_169) or \
                  (etsi_cat1_compatible == model.vars.etsi_cat1_compatible.var_enum.Band_868)

        part_list = ['dumbo', 'jumbo', 'nerio', 'nixi']
        in_part_list = part_family.lower() in part_list

        in_scope = is_2fsk and in_part_list and in_supported_profile and not viterbi_en and antdiv_off and not_spread and not is_etsi

        model.vars.in_2fsk_opt_scope.value = in_scope

    def calc_dynamic_slicer_sw_en(self, model):
        #TODO: remove this as output variable for series 3
        # We will not use dynamic slicing with series 2
        model.vars.dynamic_slicer_enabled.value = False

# Method name: calc_error_check
# Defined in: ocelot\calculators\calc_utilities.py
    def calc_error_check_demod(self, model):
        #Overriding function due to removal of freq_gain_scale variable
        #Load model variables into local variables
        baudrate = model.vars.baudrate.value
        rx_baud_rate = model.vars.rx_baud_rate_actual.value
        carson_bw = model.vars.bandwidth_carson_hz.value
        bw_dig = model.vars.bandwidth_actual.value
        osr = model.vars.oversampling_rate_actual.value
        brcalen = model.vars.brcalen.value
        rxbr = model.vars.rxbrfrac_actual.value
        basebits = model.vars.preamble_pattern_len_actual.value
        timingbases = model.vars.MODEM_TIMING_TIMINGBASES.value
        num_timing_windows = model.vars.number_of_timing_windows.value
        preamble_detection_length = model.vars.preamble_detection_length.value
        dsss_length = model.vars.dsss_len.value
        max_timing_window = 256.0 / osr
        timing_window = timingbases * basebits * 1.0
        if num_timing_windows * timing_window > preamble_detection_length + 2 and dsss_length == 0:
            print(" WARNING: timing window chosen too large for given preamble length")
        if timing_window > max_timing_window:
            print("  WARNING: timing window larger than max allowed %d!" % math.floor(128.0 / (2 * rxbr * basebits)))
        rx_bitrate_error = abs(baudrate - rx_baud_rate) * 1.0 / baudrate
        if rx_bitrate_error > 0.004 and brcalen == 0:
            print("  WARNING: RX bitrate is off by more than 0.4%!")
        if baudrate >= 1e6:
            carson_scale = 0.82
        else:
            carson_scale = 0.95
        bw_error = abs(carson_bw * carson_scale - bw_dig) * 1.0 / carson_bw
        model.vars.max_timing_window.value  = max_timing_window
        model.vars.timing_window.value      = timing_window
        model.vars.rx_bitrate_error.value   = rx_bitrate_error
        model.vars.bw_error.value           = bw_error