from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from py_2_and_3_compatibility import *

class CalcAgcResponse(IPCalculator):

    def calc_agc_cnt_thresholds(self, model):
        # Override method to account for IFPKD settling time
        periodhi_reg = model.vars.AGC_AGCPERIOD0_PERIODHI.value
        periodhistl_reg = model.vars.AGC_AGCPERIOD0_PERIODHISTL.value
        settletimeif_reg = model.vars.AGC_AGCPERIOD0_SETTLETIMEIF.value

        if periodhistl_reg == 0:
            # We start the period counter alongside the IFPKD settling, so we have to acccount for
            # the settling time (blanking period)
            periodhi_usable = periodhi_reg - settletimeif_reg
        else:
            periodhi_usable = periodhi_reg

        # % There are many possible ways to handle the table but the simplest would be:
        # % this is based on sine wave tripping N times at different gain settings
        self._ip_reg_write(model, 'STEPDWN_STEPDWN0', 0)
        self._ip_reg_write(model, 'STEPDWN_STEPDWN1', 1)
        self._ip_reg_write(model, 'STEPDWN_STEPDWN2', 2)
        self._ip_reg_write(model, 'STEPDWN_STEPDWN3', 3)
        self._ip_reg_write(model, 'STEPDWN_STEPDWN4', 4)
        self._ip_reg_write(model, 'STEPDWN_STEPDWN5', 5)

        hicntregion0 = int(py2round(0.55 * periodhi_usable))
        hicntregion1 = int(py2round(0.75 * periodhi_usable))
        hicntregion2 = int(py2round(0.85 * periodhi_usable))
        hicntregion3 = int(py2round(0.90 * periodhi_usable))
        hicntregion4 = int(py2round(0.93 * periodhi_usable))

        if (hicntregion0 > 255):
            print(
                "  WARNING: AGC_HICNTREGION_HICNTREGION 0 calculated beyond range: hicntregion0 {}, hicntregion1 {}, AGC_AGCPERIOD0_PERIODHI {}. Saturating value to 255 !".format(
                    hicntregion0, hicntregion1, periodhi_reg))
            hicntregion0 = 255

        if (hicntregion1 > 255):
            print(
                "  WARNING: AGC_HICNTREGION_HICNTREGION 1 calculated beyond range: hicntregion0 {}, hicntregion1 {}, AGC_AGCPERIOD0_PERIODHI {}. Saturating value to 255 !".format(
                    hicntregion0, hicntregion1, periodhi_reg))
            hicntregion1 = 255

        self._ip_reg_write(model, 'HICNTREGION0_HICNTREGION0', hicntregion0)
        self._ip_reg_write(model, 'HICNTREGION0_HICNTREGION1', hicntregion1)
        self._ip_reg_write(model, 'HICNTREGION0_HICNTREGION2', hicntregion2)
        self._ip_reg_write(model, 'HICNTREGION0_HICNTREGION3', hicntregion3)
        self._ip_reg_write(model, 'HICNTREGION1_HICNTREGION4', hicntregion4)

        # % safe way of setting this.
        self._ip_reg_write(model, 'AGCPERIOD0_MAXHICNTTHD', hicntregion4)

    def calc_antdiv_debouncecntthd(self, model):
        # This is do not care (functionality disabled)
        self._ip_reg_write(model, 'ANTDIV_DEBOUNCECNTTHD', do_not_care=True)

    def calc_periodhistl_reg(self, model):
        self._ip_reg_write(model, 'AGCPERIOD0_PERIODHISTL', 1)

    def calc_periodlostl_reg(self, model):
        self._ip_reg_write(model, 'AGCPERIOD0_PERIODLOSTL', 1)

    def calc_pnupdisthd_reg(self, model):

        # MCUW_RADIO_CFG-1856: Set PNUPDISTHD to 0 When Using RFPKD to Prevent AGC chattering at after PN exhaustion
        # only acceptable to set to 0 when dual RFPKD THD can release the disgainup
        self._ip_reg_write(model, 'CTRL5_PNUPDISTHD', 0)

    def calc_agc_periodhi_periodlow(self, model):
        mod_format = model.vars.modulation_type.value
        modem_frequency_hz = model.vars.modem_frequency_hz.value
        f_if = model.vars.if_frequency_hz_actual.value
        baudrate = model.vars.baudrate.value

        # period over which we count how many times we tripped the HI threshold - xtal PLL freq because AGC runs at this clock
        if f_if > 0:
            periodhi = int(py2round(modem_frequency_hz / (2 * f_if)))
        else:
            periodhi = 14  # for zero-IF used on FPGA tests fix periodhi to 14

        # Function of PERIODHI and attack vs decay ratio needed. We currently use 3x
        # The scaler 3 could be an input that tunes attack vs decay ratio.

        if (mod_format == model.vars.modulation_type.var_enum.OOK):
            periodlow = int(py2round((modem_frequency_hz / (baudrate * 0.9))))
        else:
            periodlow = 3 * periodhi

        self._ip_reg_write(model, 'AGCPERIOD0_PERIODHI', int(round(periodhi)))
        self._ip_reg_write(model, 'AGCPERIOD1_PERIODLOW', int(round(periodlow)))

    def calc_pngainstep_reg(self, model):
        etsi_cat1_compatability = model.vars.etsi_cat1_compatible.value

        # PN gain step size should be 1 for ETSI Cat 1 case and 2 in all other cases
        if (etsi_cat1_compatability != model.vars.etsi_cat1_compatible.var_enum.Normal):
            reg = 1
        else:
            reg = 2

        self._ip_reg_write(model, 'GAINRANGE_PNGAINSTEP', reg)

    def calc_agcperiod_actual(self, model):

        #Read in the actual AGC period register (different name for Ocelot)
        agc_period_reg = model.vars.AGC_CTRL1_PWRPERIOD.value

        #Calculate the actual period value based on the reg
        val = 2 ** (agc_period_reg * 1.0)

        model.vars.agcperiod_actual.value = val

    def calc_cfloopdel_reg(self, model):
        """calculate AGC settling delay which is basically the group delay of decimation and
        channel filters through the datapath plus processing delays

        calculations are in channel filter clock cycles to directly program into CFLOOPDEL

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        agc_delay = model.vars.agc_settling_delay.value

        cfloopdel = agc_delay

        if cfloopdel > 127:
            cfloopdel = 127

        self._ip_reg_write(model, 'GAINSTEPLIM0_CFLOOPDEL', int(math.ceil(cfloopdel)))

    def calc_agc_cfloopdel_actual(self, model):
        reg = model.vars.AGC_GAINSTEPLIM0_CFLOOPDEL.value
        adc_freq_actual = model.vars.adc_freq_actual.value
        dec0 = model.vars.dec0_actual.value
        dec1 = model.vars.dec1_actual.value
        src2_actual = model.vars.src2_ratio_actual.value

        fsrc2 = adc_freq_actual / 8.0 / dec0 / dec1 * src2_actual
        model.vars.cfloopdel_us_actual.value = reg / fsrc2 * 1e6

        return

    def calc_agc_sub_reg(self, model):
        demod_sel = model.vars.demod_select.value
        adc_freq_actual = model.vars.adc_freq_actual.value
        dec0_actual = model.vars.dec0_actual.value
        dec1_actual = model.vars.dec1_actual.value
        dec2_actual = model.vars.dec2_actual.value
        baudrate = model.vars.baudrate.value
        src2_actual = model.vars.src2_ratio_actual.value

        osr = adc_freq_actual * src2_actual / (dec0_actual * dec1_actual * 8 * dec2_actual * baudrate)
        # when BCR demod is selected we the OSR can be as high as 127
        # this does not fit into the RXBR register which is used in generating a baudrate clock
        # we switch to using SUB registers instead of RXBR for this purpose when BCR is selected
        if (demod_sel == model.vars.demod_select.var_enum.BCR):
            rawndec = model.vars.MODEM_BCRDEMODOOK_RAWNDEC.value #Checking inside of the BCR condition to allow inheritance for Bobcat
            subperiod = 1
            dec = pow(2, rawndec)
            osr_bcr = osr / dec

            # write half of sampling rate into SUB registers
            subfrac = osr_bcr / 2

            subint = math.floor(subfrac)

            frac = subfrac - subint

            best_error = 999
            for den in range(1,256):
                num = round(frac * den)
                error = abs(frac - num/den)
                if error < best_error:
                    subden = den
                    subnum = num
                    best_error = error

                if best_error < 1e-3:
                    break
        elif (demod_sel == model.vars.demod_select.var_enum.TRECS_VITERBI or
              demod_sel == model.vars.demod_select.var_enum.TRECS_SLICER) and osr >= 8:
            subint = model.vars.rxbrint.value
            subnum = model.vars.rxbrnum.value
            subden = model.vars.rxbrden.value
            subperiod = 1

        else:
            subden = 0
            subint = 0
            subnum = 0
            subperiod = 0

        self._ip_reg_write(model, 'CTRL7_SUBDEN', subden)
        self._ip_reg_write(model, 'CTRL7_SUBINT', subint)
        self._ip_reg_write(model, 'CTRL7_SUBNUM', subnum)
        self._ip_reg_write(model, 'CTRL7_SUBPERIOD', subperiod)

        return

    def calc_subfrac_actual(self, model):

        # Load model variables into local variables
        subint_actual = model.vars.AGC_CTRL7_SUBINT.value
        subnum_actual = model.vars.AGC_CTRL7_SUBNUM.value
        subden_actual = model.vars.AGC_CTRL7_SUBDEN.value
        subperiod = model.vars.AGC_CTRL7_SUBPERIOD.value

        # Calculate the sub fraction
        if subperiod and subden_actual > 0:
            subfrac_actual = float(subint_actual + float(subnum_actual) / subden_actual)
        else:
            subfrac_actual = 0.0

        # Load local variables back into model variables
        model.vars.subfrac_actual.value = subfrac_actual