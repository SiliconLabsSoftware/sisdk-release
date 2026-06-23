from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from enum import Enum
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_aox import CalcAoX
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_diversity import CalcDiversity
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_coherent import CalcCoherent
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_enhanced import CalcEnhanced
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_frame_detect import CalcFrameDetect
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_freq_offset_comp import CalcFreqOffsetComp
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_ircal import CalcIRCal
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_mbus import CalcMbus
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_sq import CalcSQ
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_demodulator import CalcDemodulator
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_viterbi import CalcViterbi
from pyradioconfig.modules.lpw.modem.r_08.prod_00.calculations.calc_modem_misc import CalcModemMisc

from py_2_and_3_compatibility import *

from pyradioconfig.modules.lpw.modem.r_08.prod_00.reg_fields import ModemRegFields

class CalcModem_r08(CalcAoX, CalcDiversity, CalcCoherent, CalcEnhanced, CalcFrameDetect, CalcFreqOffsetComp, CalcIRCal,
                  CalcMbus, CalcSQ, CalcDemodulator, CalcViterbi, CalcModemMisc):

    def __init__(self, peripheral_name='MODEM'):
        self._reg_field_list = ModemRegFields().reg_field_list
        super().__init__(peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)

        """
        # AOX
        """

        var = self._addModelVariable(model, 'aox_enable', Enum, ModelVariableFormat.DECIMAL, units='',
                                     desc='Enables AoX settings')
        member_data = [
            ['DISABLED', 0, 'AoX Disabled'],
            ['ENABLED', 1, 'AoX Enabled'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'AoxEnableEnum',
            'AoX Enable/Disable Selection',
            member_data)

        """
        Antenna Diversity
        """

        # Internal variables
        # Must exposing the forced selection of a antenna 0 only as DISABLE enum
        var = self._addModelVariable(model, 'antdivmode', Enum, ModelVariableFormat.DECIMAL, 'Antenna diversity mode')
        member_data = [
            ['DISABLE', 0, 'Antenna 0 used'],
            ['ANTENNA1', 1, 'Antenna 1 is used'],
            ['ANTSELFIRST', 2, 'Select-First algorithm'],
            ['ANTSELCORR', 3, 'Select-Best algorithm based on correlation'],
            ['ANTSELRSSI', 4, 'Select-Best algorithm based on RSSI value'],
            ['PHDEMODANTDIV', 5, 'Select PHASE Demod ANT-DIV algorithm'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'AntDivModeEnum',
            'List of supported antenna diversity mode',
            member_data)

        # Bools not allowed as advanced inputs due to GUI constraint. Using enum instead
        var = self._addModelVariable(model, 'antdivrepeatdis', Enum, ModelVariableFormat.DECIMAL,
                                     'Repeated measurement of first antenna when Select-Best algorithm is used')
        member_data = [
            ['REPEATFIRST', 0, 'Enable repeated measurement of first antenna'],
            ['NOREPEATFIRST', 1, 'Disable repeated measurement of first antenna'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'AntDivRepeatDisModeEnum',
            'Enable or disable repeated measurement of first antenna',
            member_data)

        var = self._addModelVariable(model, 'skip2ant', Enum, ModelVariableFormat.DECIMAL,
                                     'Skip 2nd antenna check with phase demod antenna diversity')
        member_data = [
            ['SKIP2ANT', 0, 'Enable repeated measurement of first antenna'],
            ['NOSKIP2ANT', 1, 'Disable repeated measurement of first antenna'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'Skip2AntModeEnum',
            'Enable or disable Skip 2nd antenna check with phase demod antenna diversity',
            member_data)

        # Output software variables for RAIL to consume
        self._addModelVariable(model, 'div_antdivmode', int, ModelVariableFormat.DECIMAL, 'Antenna diversity mode')
        self._addModelVariable(model, 'div_antdivrepeatdis', int, ModelVariableFormat.DECIMAL,
                               'Repeated measurement of first antenna when Select-Best algorithm is used')

        # Calculation variable for reset period
        if model.part_family.lower() in ["jumbo", "nerio", "nixi"]:
            self._addModelVariable(model, 'div_demod_reset_period_hemi_usec', int, ModelVariableFormat.DECIMAL,
                                   'Sequencer FW issues a reset to demod at this interval. Used in antenna diversity.')

        self._addModelVariable(model, 'antdiv_adprethresh_scale', float, ModelVariableFormat.DECIMAL,
                                     'Set adpretrehsh as a scaled value of timthresh ')

        self._addModelVariable(model, 'antdiv_switch_delay_us', float, ModelVariableFormat.DECIMAL,
                               desc='Delay correlation samples after antenna switch.')
        self._addModelVariable(model, 'antdiv_switch_skip_us', float, ModelVariableFormat.DECIMAL,
                               desc='Skip correlation samples after antenna switch.')
        self._addModelVariable(model, 'antdiv_freq_offset_bias', int, ModelVariableFormat.DECIMAL,
                               desc='Antenna diversity frequency offset bias.')
        self._addModelVariable(model, 'antdiv_enable_parallel_correlation', bool, ModelVariableFormat.ASCII,
                               desc='Antenna diversity enable parallel correlation')
        self._addModelVariable(model, 'antdiv_enable_dual_window', bool, ModelVariableFormat.ASCII,
                               desc='Enable dual correlation window')
        self._addModelVariable(model, 'antdiv_adpcsigampthr', int, ModelVariableFormat.DECIMAL,
                               desc='Signal Amplitude Threshold')
        self._addModelVariable(model, 'antdiv_adpcwndsize', int, ModelVariableFormat.DECIMAL,
                               desc='Antenna Diversity Correlation window size in chips')
        self._addModelVariable(model, 'antdiv_adbbss_refamp', int, ModelVariableFormat.DECIMAL,
                               desc='Antenna Diversity ADBBSS LUT reference amplitude (coherent only)')

        """
        Frame Detect
        """
        # Method name: buildVariables
        # Defined in: rainier\calculators\calc_frame_detect.py

        self._addModelVariable(model, 'preamble_string', str, ModelVariableFormat.ASCII,
                               desc='Output string representing the preamble pattern in binary')
        self._addModelActual(model, 'preamble_string', str, ModelVariableFormat.ASCII,
                             desc='Output string representing the actual preamble pattern in binary')
        self._addModelVariable(model, 'syncword_string', str, ModelVariableFormat.ASCII,
                               desc='Output string representing the sync word in binary')
        self._addModelVariable(model, 'syncword_dualsync', bool, ModelVariableFormat.ASCII,
                               desc='Enable dual syncword detection')

        # Actual values
        self._addModelActual(model, 'syncword_0', long,
                             ModelVariableFormat.HEX, )  # desc='Syncword 0 extracted from the register )
        self._addModelActual(model, 'syncword_1', long,
                             ModelVariableFormat.HEX, )  # desc='Syncword 1 extracted from the register )

        self._addModelVariable(model, 'syncword_trisync', bool, ModelVariableFormat.ASCII,
                               desc='Enable tri syncword detection')

        self._addModelVariable(model, 'in_2fsk_opt_scope', bool, ModelVariableFormat.DECIMAL)

        """
        Frequency offset compensation
        """

        # Method name: buildVariables
        # Defined in: ocelot\calculators\calc_freq_offset_comp.py
        self._addModelVariable(model, 'afc_step_scale', float, ModelVariableFormat.DECIMAL,
                               desc='Scale applied to the default frequency adjustment step size')
        self._addModelVariable(model, 'afc_tx_adjust_enable', bool, ModelVariableFormat.DECIMAL,
                                   desc='Enable TX frequency adjustment based on AFC during RX')

        """
        Coherent detection
        """
        # : Noise floor of channel power accumulator used for coherent demod.
        self._addModelVariable(model, 'chpwraccu_noise', float, ModelVariableFormat.DECIMAL)

        """
        IRCAL
        """
        # Method name: buildVariables
        # Defined in: ocelot\calculators\calc_ircal.py
        self._addModelVariable(model, 'ircal_murshf', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'ircal_muishf', int, ModelVariableFormat.DECIMAL)
        # -------- Register Settings Used During Calibration --------
        # auxNDiv (to be put into synth.auxfreq.mmddenom during ir cal only)
        self._addModelVariable(model, 'ircal_auxndiv', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='This value is predetermined.')
        # auxLoDiv (to be put into  synth.divctrl.auxlodivfreqctrl during ir cal only)
        self._addModelVariable(model, 'ircal_auxlodiv', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='This value is predetermined.')
        # rampVal (to be put into modem.rampctrl.rampval during ir cal only)
        self._addModelVariable(model, 'ircal_rampval', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='This value is predetermined.')
        # rxAmp_PLL (to be put into rac.auxctrl.rxamp during PLL loopback, ir cal only)
        self._addModelVariable(model, 'ircal_rxamppll', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='This value is predetermined.')
        # rxAmp_PA (to be put into rac.auxctrl.rxamp during PA loopback, ir cal only)
        self._addModelVariable(model, 'ircal_rxamppa', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='This value is predetermined.')

        # -------- Decide Between Calibration Procedures --------
        # diConfigIsValid (true = DI value / PTE value is an option)
        self._addModelVariable(model, 'ircal_manufconfigvalid', bool, ModelVariableFormat.ASCII,
                               'True = the manufacturing calibration value is saved on the chip')
        # pllLoopbackConfigIsValid (true = PLL loopback is an option)
        self._addModelVariable(model, 'ircal_pllconfigvalid', bool, ModelVariableFormat.ASCII,
                               'True = PLL loopback is permitted to generate a calibration value')
        # paLoopbackConfigIsValid (true = PA loopback is an option)
        self._addModelVariable(model, 'ircal_paconfigvalid', bool, ModelVariableFormat.ASCII,
                               'True = PA loopback is permitted to generate a calibration value')
        # recommendedConfig (DI/PTE vs PLL loopback vs PA loopback)
        var = self._addModelVariable(model, 'ircal_bestconfig', Enum, ModelVariableFormat.DECIMAL,
                                     'Specify the best calibration method for this radio configuration.')
        member_data = [
            ['MANUFACTURING', 1, 'Use the calibration value saved during manufacturing, if applicable.'],
            ['PLL', 2, 'Put the part into a PLL loopback to generate a calibration value.'],
            ['PA', 3, 'Put the part into a PA loopback to generate a calibration value.'],
            ['UNSUPPORTED', 4, 'Image rejection calibration not supported.'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'configType',
            'Specify how image rejection calibration is to run.',
            member_data)

        # -------- Decide Between Software/Hardware RSSI Averaging --------
        self._addModelVariable(model, 'ircal_useswrssiaveraging', bool, ModelVariableFormat.ASCII,
                               'True = use software RSSI averaging; False = use hardware RSSI averaging')
        self._addModelVariable(model, 'ircal_numrssitoavg', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Number of RSSI values (2^value) to average in software. If value = 3, 8 values will be averaged.')
        self._addModelVariable(model, 'ircal_throwawaybeforerssi', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Number of RSSI values to discard before starting to average RSSI values.')
        self._addModelVariable(model, 'ircal_delayusbeforerssi', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Microsecond delay between applying a calibration value and then reading RSSI values.')
        self._addModelVariable(model, 'ircal_delayusbetweenswrssi', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Microsecond delay between gathering RSSI values. Software RSSI averaging mode only.')

        # ------ Determine number of raw RSSI values averaged by hardware ------
        # agcRssiPeriod
        self._addModelVariable(model, 'ircal_agcrssiperiod', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Number of raw RSSI values averaged by hardware.')

        # ------ Registers specific to Jumbo (and new Dumbo) support ------
        self._addModelVariable(model, 'ircal_useswrssiaveraging2', bool, ModelVariableFormat.ASCII,
                               'True = use software RSSI averaging; False = use hardware RSSI averaging; Jumbo support')
        self._addModelVariable(model, 'ircal_numrssitoavg2', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Number of RSSI values (2^value) to average in software. If value = 3, 8 values will be averaged. Jumbo support')
        self._addModelVariable(model, 'ircal_throwawaybeforerssi2', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Number of RSSI values to discard before starting to average RSSI values. Jumbo support')
        self._addModelVariable(model, 'ircal_delayusbeforerssi2', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Microsecond delay between applying a calibration value and then reading RSSI values. Jumbo support')
        self._addModelVariable(model, 'ircal_delayusbetweenswrssi2', int, ModelVariableFormat.DECIMAL, units='bytes',
                               desc='Microsecond delay between gathering RSSI values. Software RSSI averaging mode only. Jumbo support')

        #
        # Bools not allowed as advanced inputs due to GUI constraint. Using enum instead
        var = self._addModelVariable(model, 'ircal_rxtx_path_common', Enum, ModelVariableFormat.DECIMAL,
                                     'RX and TX are on a common/shared circuit, or split. Refer to document AN971.')
        member_data = [
            ['SHARED_RX_TX_PATH', 0, 'RX and TX circuit paths are common/shared/connected'],
            ['SPLIT_RX_TX_PATH', 1, 'RX and TX circuit paths are separated/not connected'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'IRCalRXTXPathCommonEnum',
            'RX and TX are on a common/shared circuit, or split. Refer to document AN971.',
            member_data)

        self._addModelVariable(model, 'ircal_power_level', int, ModelVariableFormat.DECIMAL, units='codes',
                               desc='Specify IR cal power level (amplitude) instead of auto (0). Refer to document AN971.')

        """
        MBUS
        """
        # Method name: buildVariables
        # Defined in: common\calculators\calc_mbus.py
        var = self._addModelVariable(model, 'mbus_frame_format', Enum, ModelVariableFormat.DECIMAL,
                                     'List of supported Mbus Frame Format Configurations')
        member_data = [
            ['NoFormat', 0, 'No frame formatting'],
            ['FrameA', 1, 'Mbus Format A '],
            ['FrameB', 2, 'Mbus Format B'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'MbusFrameFormatEnum',
            'List of supported Mbus frame formats',
            member_data)
        # Mbus Frame Format
        var = self._addModelVariable(model, 'mbus_symbol_encoding', Enum, ModelVariableFormat.DECIMAL,
                                     'List of supported Mbus Symbol Encoding Configurations')
        member_data = [
            ['NRZ', 0, 'NRZ'],
            ['Manchester', 1, 'Manchester'],
            ['MBUS_3OF6', 2, '3 of 6'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'MbusFrameFormatEnum',
            'List of supported Mbus frame formats',
            member_data)
        var = self._addModelVariable(model, 'mbus_mode', Enum, ModelVariableFormat.DECIMAL,
                                     'List of supported Mbus Modes')
        member_data = [
            ['ModeC_M2O_100k', 0, 'Mode C Meter to Other, 100kbps'],
            ['ModeC_O2M_50k', 1, 'Mode C Other to Meter, 50kbps'],
            ['ModeF_2p4k', 2, 'Mode F, 2.4kbps'],
            ['ModeNg', 3, 'Mode Ng'],
            ['ModeN1a_4p8K', 4, 'Mode N1a, 4.8kbps'],
            ['ModeN1c_2p4K', 5, 'Mode N1c, 2.4kbps'],
            ['ModeR_4p8k', 6, 'Mode R, 2.8kbps'],
            ['ModeT_M2O_100k', 7, 'Mode T, Meter to Other, 100kbps'],
            ['ModeT_O2M_32p768k', 8, 'Mode T, Other to Meter, 100kbps'],
            ['ModeS_32p768k', 9, 'Mode S, 32.768kbps'],
            ['ModeN_6p4k', 10, 'Mode N, 6.4kbps'],
            ['ModeTC_M2O_100k', 11, 'Mode T + C, Meter to Other, 100kbps'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'MbusModeEnum',
            'List of supported Mbus modoes',
            member_data)

        """
        SQ
        """
        self._addModelVariable(model, 'psm_max_sleep_us', int, ModelVariableFormat.DECIMAL, units='',
                               desc='Maximum time we can sleep in PSM mode including disable/enable times')
        var = self._addModelVariable(model, 'fast_detect_enable', Enum, ModelVariableFormat.DECIMAL,
                                     'Enable fast timing detection')
        member_data = [
            ['DISABLED', 0, 'Fast Detect Disabled'],
            ['ENABLED', 1, 'Fast Detect Enabled'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'FastDetectEnum',
            'Fast Detect Enable/Disable Selection',
            member_data)


        """Build Rx Duty Cycle variables:

        rxdc_power_save_mode --> controls which blocks (Demod, RF, Synth) are duty cycled (default: DISABLED).
        rxdc_power_save_time_us --> controls the duration of power saving time.
        rxdc_on_time_us --> Calculated RxDC ON time. During this period, the duty cycled blocks are ON.
        rxdc_off_time_us --> Calculated RxDC OFF time. During this period, the duty cycled blocks are OFF."""

        self._addModelVariable(model, 'rxdc_power_save_mode', Enum, ModelVariableFormat.DECIMAL, 'Rx Duty Cycle mode')
        member_data = [
            ['DISABLED', 0, 'Rx Duty Cycle is disabled (default)'],
            ['DEMOD', 1, 'Demod block is duty-cycled'],
            ['RF', 2, 'Demod and RF blocks are duty-cycled'],
            ['SYNTH', 3, 'Demod, RF and Synth blocks are duty-cycled'],
        ]
        model.vars.rxdc_power_save_mode.var_enum = CreateModelVariableEnum(
            'RxDutyCycleEnum',
            'List of supported duty cycle modes',
            member_data)
        self._addModelVariable(model, 'rxdc_power_save_time_us', int, ModelVariableFormat.DECIMAL, 'RxDC power save time in us')
        self._addModelVariable(model, 'rxdc_on_time_us_actual', int, ModelVariableFormat.DECIMAL, 'Calculated RxDC ON time in us')
        self._addModelVariable(model, 'rxdc_off_time_us_actual', int, ModelVariableFormat.DECIMAL, 'Calculated RxDC OFF time in us')


        # ocelot
        #New variables
        self._addModelVariable(model, 'adc_xo_mult', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'enable_high_mod_trecs', int, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'adc_xo_mult', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'lo_target_freq', long, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'a_divider', int, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'b_divider', int, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'c_divider', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'adc_freq_error', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'src2_ratio', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'max_dec2', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'min_dec2', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'bitrate_gross', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'digmixfreq', int, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'log2x4', int, ModelVariableFormat.DECIMAL, desc='Actual log2x4 for FEFILT in use')

        self._addModelVariable(model, 'min_bwsel', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'max_bwsel', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'target_bwsel', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'min_src2', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'max_src2', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'bandwidth_tol', float, ModelVariableFormat.DECIMAL)

        var = self._addModelVariable(model, 'directmode_rx', Enum,      ModelVariableFormat.DECIMAL, desc='Direct RX modes')
        member_data = [
            ['DISABLED', 0, 'Direct Mode Disabled'],
            ['SYNC', 1, 'Configure modem to output demod data directly to GPIO or RAM buffer (2FSK or OOK). Data is synchronized to a recovered bit clock.'],
            ['ASYNC', 2, 'Configure modem to output raw demod data directly to GPIO or RAM buffer (2FSK or OOK) at the rate of the demodulator clock.'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'DirectModeEnum',
            'List of supported direct modes',
            member_data)

        self._addModelActual(model, 'iq_rate', float, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'maximize_bwsel_range', bool, ModelVariableFormat.DECIMAL)

        var = self._addModelVariable(model, 'bpsk_feature', Enum, ModelVariableFormat.DECIMAL,
                                     'IEEE802154 BPSK Feature')
        member_data = [
            ['STANDARD_20KBPS', 0, 'IEEE802154 Standard 20kbps'],
            ['STANDARD_40KBPS', 1, 'IEEE802154 Standard 40kbps'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'BPSKFeatureEnum',
            'List of supported IEEE802154 PHY features',
            member_data
        )
        self._addModelVariable(model, 'modem_frequency_hz', float, ModelVariableFormat.DECIMAL, units='Hz',
                               desc='MODEM clock frequency (may differ from xtal rate if FPLL is configured')

        # lynx
        self._addModelVariable(model, 'preamble_detection_length', int, ModelVariableFormat.DECIMAL,
                               desc='Number of preamble bits to use for timing detection')
        self._addModelVariable(model, 'phscale_derate_factor', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'trecs_enabled', bool, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'rx_deviation_scaled', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'freq_dev_max', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'freq_dev_min', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'modulation_index_for_ksi', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'datafilter_taps', int, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'rx_grp_delay_us', float, ModelVariableFormat.DECIMAL,
                               desc='RX group delay in us from adc to demod')

        self._addModelVariable(model, 'adc_rate_mode', Enum, ModelVariableFormat.DECIMAL)
        model.vars.adc_rate_mode.var_enum = CreateModelVariableEnum(
            enum_name='AdcRateModeEnum',
            enum_desc='ADC Clock Rate Mode',
            member_data=[
                ['FULLRATE', 0, 'Full rate mode'],
                ['HALFRATE', 1, 'Half rate mode'],
                ['EIGHTHRATE', 2, 'Eighth rate mode']
            ])

        self._addModelActual(model, 'adc_rate_mode', Enum, ModelVariableFormat.DECIMAL)
        model.vars.adc_rate_mode_actual.var_enum = model.vars.adc_rate_mode.var_enum

        self._addModelActual(model, 'timing_detection_threshold_gain', int, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'digmix_res', float, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'digmixfreq', int, ModelVariableFormat.DECIMAL)

        var = self._addModelVariable(model, 'zigbee_feature', Enum, ModelVariableFormat.DECIMAL, 'Zigbee Feature')
        member_data = [
            ['NONE', 0xFF, 'None'],
            ['STANDARD', 0, 'Standard'],
            ['ANTDIV', 1, 'Antenna Diversity'],
            ['COEX', 2, 'Antenna Diversity'],
            ['ANTDIV_COEX', 3, 'Antenna Diversity'],
            # [Reserved space, 4..7, reserved]
            ['FEM', 8, 'External LNA'],
            ['ANTDIV_FEM', 9, 'Antenna Diversity with External LNA'],
            ['COEX_FEM', 10, 'External LNA'],
            ['ANTDIV_COEX_FEM', 11, 'External LNA'],
            # [Reserved space, 12, reserved]
            ['HDR_2M', 13, 'Mode Switch to 2M'],
            ['FCS', 14, 'Fast Channel Switching'],
            ['HDR_1M_FEC', 15, 'Mode Switch to 1M with FEC'],
            ['FCS_HDR_2M', 16, 'Fast Channel Switching and 2M'],
            ['FCS_HDR_1M_FEC', 17, 'Fast Channel Switching and 1M with FEC'],
            ['RXDC', 18, 'Rx Duty Cycling'],
            ['GB868_863', 133, 'UK Metering 863 MHz Band'],
            ['GB868_915', 134, 'UK Metering 915 MHz Band'],
            ['NA915_R23', 135, 'NA R23 915 MHz Band'],
            # We use the thousands place (decimal) to indicate different PHY (different demod) for same feature
            # See https://jira.silabs.com/browse/MCUW_RADIO_CFG-2862
            ['LEGACY', 1000, 'Legacy Demod'],
            ['COHERENT', 2000, 'Coherent Demod'],
            ['ENHANCED', 3000, 'Enhanced Demod'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'ZigbeeFeatureEnum',
            'List of supported zigbee PHY features',
            member_data)

        var = self._addModelVariable(model, 'ble_feature', Enum, ModelVariableFormat.DECIMAL, 'Bluetooth LE Feature')
        member_data = [
            # Keep this in sync with RAIL's sl_rail_ble.h
            ['NONE', 0xFF, 'None'],
            ['LE_1M', 0, 'Bluetooth LE 1Mbps'],
            ['LE_2M', 1, 'Bluetooth LE 2Mbps'],
            ['CODED_125K', 2, 'Bluetooth LE Coded 125Kbps'],
            ['CODED_500K', 3, 'Bluetooth LE Coded 500Kbps'],
            ['CONCURRENT', 4, 'Bluetooth LE Simulscan'],
            ['AOX_2M', 5, 'Bluetooth LE AoX 2Mbps'],
            ['CUSTOM_1M', 6, 'Bluetooth LE Custom 1Mbps'],
            ['HADM_1M', 7, 'Bluetooth LE HADM (Channel Sounding) 1Mbps'],
            ['HADM_2M', 8, 'Bluetooth LE HADM (Channel Sounding) 2Mbps'],
            ['AOX_1M', 9, 'Bluetooth LE AoX 1Mbps'],
            ['HADM_2M_2BT', 10, 'Bluetooth LE HADM (Channel Sounding) 2Mbps 2BT'],
            ['FASTSW', 12, 'Fast switching'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'BleFeatureEnum',
            'List of supported Bluetooth LE PHY features',
            member_data)

        # common

        self._addModelVariable(model,'cost_bandwidth', float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model,'cost_osr',       float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model,'cost_range',     float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model,'cost_rate',      float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model,'cost_src',       float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model,'cost_fc',        float, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model,'cost_total',     float, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'sample_freq_actual', float, ModelVariableFormat.DECIMAL)
        self._addModelActual(model, 'adc_freq', int, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'src1_calcDenominator', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'src2_calcDenominator', int, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'fxo_or_fdec8', float, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'src1_bit_width', int, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'src2_bit_width', int, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'ch_filt_bw_available', int, ModelVariableFormat.DECIMAL, desc='Values of BWSEL available to use in SRC calculation.', is_array=True, units='unitless')

        self._addModelVariable(model, 'src1_range_available', int, ModelVariableFormat.DECIMAL, desc='Values of SRCRATIO1 available to use in SRC calculation.', is_array=True, units='unitless')

        self._addModelVariable(model, 'input_decimation_filter_allow_dec3', int, ModelVariableFormat.DECIMAL, desc='1=Allow input decimation filter decimate by 3', is_array=False, units='unitless')
        self._addModelVariable(model, 'input_decimation_filter_allow_dec8', int, ModelVariableFormat.DECIMAL, desc='1=Allow input decimation filter decimate by 8', is_array=False, units='unitless')

        self._addModelVariable(model, 'rx_ch_hopping_order_num', int, ModelVariableFormat.DECIMAL)

        # These values pass through to be consumed by RAIL API calls to enable RX scanning/hopping. Implemented as overrides to enable development. Long-term should be calculate-able.
        var = self._addModelVariable(model, 'rx_ch_hopping_mode', Enum, ModelVariableFormat.DECIMAL, 'For receive scanning PHYs: event to trigger a hop to next PHY')
        # Enum values are defined by RAIL.
        # TODO: find a better, programmatic way to ensure this enum definition always matches what is in RAIL
        # One place to find them is pyrailib:
        # \libraries\py_system_common\app\pyraillib\platform\efr32xg21\RpcWrapper.py
        member_data = [
            ['RAIL_RX_CHANNEL_HOPPING_MODE_MANUAL', 0, 'Manual mode'],
            ['RAIL_RX_CHANNEL_HOPPING_MODE_TIMEOUT'  , 1, 'Fixed time out'],
            ['RAIL_RX_CHANNEL_HOPPING_MODE_TIMING_SENSE'   , 2, 'Timing sense'],
            ['RAIL_RX_CHANNEL_HOPPING_MODE_PREAMBLE_SENSE'   , 3, 'Preamble sense'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'RAILRxChHoppingEnum',
            'List of supported RAIL RX channel hopping modes',
            member_data)
        self._addModelVariable(model, 'rx_ch_hopping_delay_usec', int, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'viterbi_demod_expect_patt', long, ModelVariableFormat.DECIMAL)
        self._addModelVariable(model, 'viterbi_demod_expect_patt_head_tail', int, ModelVariableFormat.DECIMAL)

        self._addModelVariable(model, 'src1_range_available_minimum', int, ModelVariableFormat.DECIMAL, 'SRC range minimum')
        self._addModelVariable(model, 'viterbidemod_disdemodof_viterbi_demod_disable_overflow_detect', int, ModelVariableFormat.DECIMAL)

        """
        Viterbi
        """
        self._addModelVariable(model, 'trecs_weak_syncword_optimization', bool, ModelVariableFormat.BINARY,
                               desc='Optimize threshold for packet reception using weak syncword')

        # lynx
        self._addModelVariable(model,'trecs_pre_bits_to_syncword',int,ModelVariableFormat.DECIMAL,desc='Number of preamble bits to move to syncword with TRECS'	)
        self._addModelVariable(model, 'trecs_effective_preamble_len', int, ModelVariableFormat.DECIMAL,desc='TRECS preamble length minus bits shifted to syncword')
        self._addModelVariable(model, 'trecs_effective_syncword_len', int, ModelVariableFormat.DECIMAL,desc='TRECS syncword length plus bits shifted from preamble')
        self._addModelVariable(model, 'trecs_syncword_timeout_us', float, ModelVariableFormat.DECIMAL, desc='TRECS syncword timeout in us')
        self._addModelVariable(model, 'trecs_optimize_cost_thd', bool, ModelVariableFormat.BINARY, desc='Enable conservative threshold calculation')

        """
        Error Calc
        """
        self._addModelVariable(model, 'max_timing_window',  float, ModelVariableFormat.DECIMAL )
        self._addModelVariable(model, 'timing_window',      float, ModelVariableFormat.DECIMAL )
        self._addModelVariable(model, 'rx_bitrate_error',   float, ModelVariableFormat.DECIMAL )
        self._addModelVariable(model, 'rx_deviation_error', float, ModelVariableFormat.DECIMAL )
        self._addModelVariable(model, 'bw_error',           float, ModelVariableFormat.DECIMAL )


