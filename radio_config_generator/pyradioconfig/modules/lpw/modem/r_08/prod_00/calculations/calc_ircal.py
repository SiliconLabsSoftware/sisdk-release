from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from py_2_and_3_compatibility import *

class CalcIRCal(IPCalculator):

    # for Software Averaging (used in original Dumbo release)
    sw_useSwRssiAveraging = True
    sw_numRssiToAvg = 6  # = 2^*6* = 64
    sw_throwAwayBeforeRssi = 0
    sw_delayUsBeforeRssi = 10000
    sw_delayUsBetweenSwRssi = 0
    # for Hardware Averaging
    hw_useSwRssiAveraging = False
    hw_numRssiToAvg = 2  # = 2^*2* = 4
    hw_throwAwayBeforeRssi = 2
    hw_delayUsBeforeRssi = 0
    hw_delayUsBetweenSwRssi = 0

    # Method name: calc_ircal_auxpll_dividers
    # Defined in: ocelot\calculators\calc_ircal.py
    def calc_ircal_auxpll_dividers(self, model):
        auxdividers = {2419000000: (1, 63),  # For Lodiv = 1 Not currently used by the IRCal algorithm.
                       1306000000: (2, 68),  # For Lodiv = 2 Untested
                       909000000: (3, 71),  # For Lodiv = 3
                       883000000: (3, 69),
                       # For Lodiv = 3 If the intent was to be near the 868 band, why wasn't (3,68) used to get 870?
                       643000000: (4, 67),  # For Lodiv = 4 Untested
                       486000000: (6, 76),  # For Lodiv = 5
                       435000000: (6, 68),  # For Lodiv = 6
                       365000000: (6, 58),  # For Lodiv = 7 # Added to support the 390MHz band.  Untested.
                       314000000: (6, 49),  # For Lodiv = 8
                       288000000: (8, 60),  # For Lodiv = 9 Untested
                       256000000: (9, 60),  # For Lodiv =10 Untested
                       214000000: (12, 67),  # For Lodiv =12 Untested
                       186000000: (12, 58),  # For Lodiv =14 Untested
                       170000000: (12, 53),  # For Lodiv =15
                       160000000: (12, 50),  # For Lodiv =16 Untested
                       143000000: (18, 67),  # For Lodiv =18 Untested
                       128000000: (18, 60),  # For Lodiv =20 Untested
                       124000000: (18, 58),  # For Lodiv =21 Untested
                       107000000: (18, 50),  # For Lodiv =24 Untested
                       102000000: (18, 48),  # For Lodiv =25 Untested
                       96000000: (18, 45),  # For Lodiv =27 Untested
                       92000000: (18, 43),  # For Lodiv =28 Untested
                       }
        # Per spec sheet \\silabs.com\design\project\ip_em_90nm\tsmc90f_ull\modules\aux_pll\docs\specs\aux_pll_stop.docx
        # and tests in ESVALID-1673
        rfFreq = model.vars.base_frequency_actual.value
        rfFreqMin = model.vars.tuning_limit_min.value
        rfFreqMax = model.vars.tuning_limit_max.value
        smallestDifference = sys.maxint  # large number
        closestBandFreq = None
        for bandFreq in auxdividers.keys():
            if (bandFreq < rfFreqMax) and (bandFreq > rfFreqMin):
                difference = abs(rfFreq - bandFreq)
                if difference < smallestDifference:
                    smallestDifference = difference
                    closestBandFreq = bandFreq
        # If we can't
        if closestBandFreq is not None:
            (auxLODiv, auxNDiv) = auxdividers[closestBandFreq]
            model.vars.ircal_auxndiv.value = auxNDiv
            model.vars.ircal_auxlodiv.value = auxLODiv
        else:
            if rfFreq > 100000000:
                # This is just to allow one existing 50MHz phy to not generate an error.
                # There are no valid values that would work for this frequency for the IRCal
                # alorithm.  The Aux pll cannot tune that low.
                # That phy probably should just be removed.  It's only used for TX CW testing.
                # We can accomplish the same thing using something like a 100MHz CW phy with
                # the frequency overridden.  For now we can let it go, since the gui would not
                # allow that phy to be created anyway.  The gui limits the input frequency to
                # a minimum value of 100MHz.
                raise CalculationException(
                    "Unexpected frequency band found.  Unable to calculate IR calibration values.")

    # Method name: calc_ircal_common_values
    # Defined in: common\calculators\calc_ircal.py
    def calc_ircal_common_values(self, model):
        model.vars.ircal_rampval.value = 6
        model.vars.ircal_rxamppll.value = 4
        model.vars.ircal_rxamppa.value = 16

    # Method name: calc_ircal_datarate_considerations
    # Defined in: common\calculators\calc_ircal.py
    def calc_ircal_datarate_considerations(self, model):
        # bitrate = model.vars.rx_baud_rate_actual.value
        # todo:  Check if we're supposed to be using bitrate or baudrate here.  Baudrate seems more correct
        bitrate = model.vars.bitrate.value
        # Dumbo:
        #   Initial release: (per Euisoo Yoo, 2016-5-11)
        #       for datarates below 10Kbps, use HW averaging
        #       for datarates above 10Kbps, use SW averaging
        if bitrate >= 10000:
            model.vars.ircal_useswrssiaveraging.value = self.sw_useSwRssiAveraging
            model.vars.ircal_numrssitoavg.value = self.sw_numRssiToAvg
            model.vars.ircal_throwawaybeforerssi.value = self.sw_throwAwayBeforeRssi
            model.vars.ircal_delayusbeforerssi.value = self.sw_delayUsBeforeRssi
            model.vars.ircal_delayusbetweenswrssi.value = self.sw_delayUsBetweenSwRssi
        else:
            model.vars.ircal_useswrssiaveraging.value = self.hw_useSwRssiAveraging
            model.vars.ircal_numrssitoavg.value = self.hw_numRssiToAvg
            model.vars.ircal_throwawaybeforerssi.value = self.hw_throwAwayBeforeRssi
            model.vars.ircal_delayusbeforerssi.value = self.hw_delayUsBeforeRssi
            model.vars.ircal_delayusbetweenswrssi.value = self.hw_delayUsBetweenSwRssi
        # Dumbo:
        #   After Jumbo release:
        #       for all datarates, use HW averaging (since validation will have validated HW averaging for all datarates with Jumbo)
        # Jumbo:
        #   Initial release:
        #       for all datarates, use HW averaging
        model.vars.ircal_useswrssiaveraging2.value = self.hw_useSwRssiAveraging
        model.vars.ircal_delayusbeforerssi2.value = self.hw_delayUsBeforeRssi
        model.vars.ircal_delayusbetweenswrssi2.value = self.hw_delayUsBetweenSwRssi
        if bitrate >= 1000000:  # datarates >= 1 Mbps
            model.vars.ircal_numrssitoavg2.value = 0
            model.vars.ircal_throwawaybeforerssi2.value = 0
            model.vars.ircal_agcrssiperiod.value = 12
        elif bitrate >= 500000:  # datarates >= 100 Kbps
            model.vars.ircal_numrssitoavg2.value = 0
            model.vars.ircal_throwawaybeforerssi2.value = 0
            model.vars.ircal_agcrssiperiod.value = 10
        elif bitrate >= 100000:  # datarates >= 100 Kbps
            model.vars.ircal_numrssitoavg2.value = 0
            model.vars.ircal_throwawaybeforerssi2.value = 0
            model.vars.ircal_agcrssiperiod.value = 9
        elif bitrate >= 10000:  # datarates >= 10 Kbps
            model.vars.ircal_numrssitoavg2.value = 1
            model.vars.ircal_throwawaybeforerssi2.value = 1
            model.vars.ircal_agcrssiperiod.value = 5
        elif bitrate >= 1000:  # datarates >= 1 Kbps
            model.vars.ircal_numrssitoavg2.value = 1
            model.vars.ircal_throwawaybeforerssi2.value = 1
            model.vars.ircal_agcrssiperiod.value = 5
        else:
            model.vars.ircal_numrssitoavg2.value = 1  # 2^1 = really 2
            model.vars.ircal_throwawaybeforerssi2.value = 1
            model.vars.ircal_agcrssiperiod.value = 3  # 2^3 = really 8

    # Method name: calc_ircal_determine_best_config
    # Defined in: common\calculators\calc_ircal.py
    def calc_ircal_determine_best_config(self, model):
        freq = model.vars.base_frequency_actual.value
        subgig_band = model.vars.subgig_band.value
        # default value is shared path
        model.vars.ircal_rxtx_path_common.value = model.vars.ircal_rxtx_path_common.var_enum.SHARED_RX_TX_PATH
        # unless set otherwise by advanced input
        ircal_rxtx_path_common = model.vars.ircal_rxtx_path_common.value
        # These values go to RAIL via newIrCalConfig in https://stash.silabs.com/projects/WMN_TOOLS/repos/rail_scripts/browse/rail_adapter_multi_phy.py
        # IR cal power level: default value is 0
        model.vars.ircal_power_level.value = 0
        # unless set otherwise by advanced input
        ircal_power_level = model.vars.ircal_power_level.value
        if not subgig_band:
            bestConfig = model.vars.ircal_bestconfig.var_enum.MANUFACTURING
        else:
            # In the original code, 490 band and above was PA, 434 and below was PLL.  Halfway between was where
            # it would switch.  That's where this breakpoint came from.
            if (freq > 462000000) and (
                    ircal_rxtx_path_common.value == model.vars.ircal_rxtx_path_common.var_enum.SHARED_RX_TX_PATH):
                bestConfig = model.vars.ircal_bestconfig.var_enum.PA
            else:
                # for a split RX TX path application, use PLL (internal) mode always
                bestConfig = model.vars.ircal_bestconfig.var_enum.PLL
        model.vars.ircal_bestconfig.value = bestConfig

    # Method name: calc_ircal_murshf_muishf
    # Defined in: bobcat\calculators\calc_ircal.py
    def calc_ircal_murshf_muishf(self, model):
        # if there is a 2.4Ghz PHY being built, it should use the same ircal coefficient
        # as all the 2.4GHz PHYs should get the coefficient from DEVINFO
        pass

    # Method name: calc_ircal_valid_methods
    # Defined in: common\calculators\calc_ircal.py
    def calc_ircal_valid_methods(self, model):
        lodiv = model.vars.lodiv_actual.value
        subgig_band = model.vars.subgig_band.value
        part_family = model.part_family.lower()
        if part_family in ["dumbo", "unit_test_part"]:
            # Dumbo has a sub-gig PTE value on the Device Information page.
            if lodiv <= 3:
                model.vars.ircal_manufconfigvalid.value = True
            else:
                model.vars.ircal_manufconfigvalid.value = False
        else:  # part_family == "jumbo"
            # Jumbo does NOT have a sub-gig PTE value on the Device Information page (at least not one we should access).
            # This setting is more conservative, so default to this as well.
            if not subgig_band:
                model.vars.ircal_manufconfigvalid.value = True
            else:
                model.vars.ircal_manufconfigvalid.value = False
        # pll config is valid for all subgig frequencies
        if not subgig_band:
            model.vars.ircal_pllconfigvalid.value = False
        else:
            model.vars.ircal_pllconfigvalid.value = True
        # pa config is valid for all subgig frequencies
        if not subgig_band:
            model.vars.ircal_paconfigvalid.value = False
        else:
            model.vars.ircal_paconfigvalid.value = True