from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
from pyradioconfig.parts.common.calculators.calc_utilities import CALC_Utilities
from math import ceil, floor, log
from py_2_and_3_compatibility import *
import numpy as np
from pyradioconfig.parts.common.utils.tinynumpy import tinynumpy


class CalcShaping(IPCalculator):

    # Method name: calc_filter_tap_length
    # Defined in: ocelot\calculators\calc_shaping.py
    def calc_filter_tap_length(self, model):
        """ Calculate shaping filter delay in samples """
        shaping = model.vars.MOD_CTRL0_SHAPING.value

        taps = 0
        if shaping == 0: # : DISABLED
            taps = 8
        elif shaping == 1: # : ODDLENGTH
            taps = 17
        elif shaping == 2: # : EVENLENGTH
            taps = 16
        elif shaping == 3: # : Asymmetric
            taps = 64
        else: # : Unsupported selection
            LogMgr.Error(f"Error: Unsupported shaping value of {shaping}!")
        model.vars.shaping_filter_taps.value = taps

    # Method name: calc_max_available_filter_taps
    # Defined in: ocelot\calculators\calc_shaping.py
    def calc_max_available_filter_taps(self, model):
        # this is fixed for a family of parts
        model.vars.max_filter_taps.value = 64

    # Method name: calc_shaping_filter_gain_actual
    # Defined in: rainier\calculators\calc_shaping.py
    def calc_shaping_filter_gain_actual(self, model):
        # The Ocelot shaping filter registers have changed in the register map, so need to override this function

        shaping_filter_mode = model.vars.MOD_CTRL0_SHAPING.value
        shaping_filter_coeffs = model.vars.shaping_filter_coeffs.value

        sf = shaping_filter_coeffs

        if shaping_filter_mode == 0:
            shaping_filter_gain = 127.0 / 128.0

        elif shaping_filter_mode == 1:
            shaping_filter_gain = ((sf[0] + sf[8] + sf[0]) +
                                   (sf[1] + sf[7]) +
                                   (sf[2] + sf[6]) +
                                   (sf[3] + sf[5]) +
                                   (sf[4] + sf[4])) / 5.0 / 128.0

        elif shaping_filter_mode == 2:
            shaping_filter_gain = ((sf[0] + sf[7]) +
                                   (sf[1] + sf[6]) +
                                   (sf[2] + sf[5]) +
                                   (sf[3] + sf[4])) / 4.0 / 128.0

        else:
            # use mean or max ?
            shaping_filter_gain = (sf[0] + sf[8] + sf[16] + sf[24] + sf[32] + sf[40] + sf[48] + sf[56] +
                                   sf[1] + sf[9] + sf[17] + sf[25] + sf[33] + sf[41] + sf[49] + sf[57] +
                                   sf[2] + sf[10] + sf[18] + sf[26] + sf[34] + sf[42] + sf[50] + sf[58] +
                                   sf[3] + sf[11] + sf[19] + sf[27] + sf[35] + sf[43] + sf[51] + sf[59] +
                                   sf[4] + sf[12] + sf[20] + sf[28] + sf[36] + sf[44] + sf[52] + sf[60] +
                                   sf[5] + sf[13] + sf[21] + sf[29] + sf[37] + sf[45] + sf[53] + sf[61] +
                                   sf[6] + sf[14] + sf[22] + sf[30] + sf[38] + sf[46] + sf[54] + sf[62] +
                                   sf[7] + sf[15] + sf[23] + sf[31] + sf[39] + sf[47] + sf[55] + sf[63]) / 8.0 / 128.0

        model.vars.shaping_filter_gain_actual.value = float(shaping_filter_gain)

    # Method name: calc_shaping_reg
    # Defined in: rainier\calculators\calc_shaping.py
    def calc_shaping_reg(self, model):
        """
        given shaping filter input parameter set shaping filter coeffs and type

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        coeff, shaping = self.run_shaping_filter_calc(model)

        self.write_coeff_registers(model, coeff, shaping)

    # Method name: check_coeff_write_error
    # Defined in: lpwh72000\calculators\calc_shaping.py
    def check_coeff_write_error(self, model, temp_coeffs):
        """
        COEFF 0-15        8 bits
        COEFF 16-18       6 bits
        COEFF 19-20       5 bits
        COEFF 21-31       4 bits
        COEFF 32-39       3 bits
        For Nerio, Nixi and Panther, we don't have all filter taps coefficients using 8 bit width registers. This method
        basically checks and makes sure calculator run doesn't fails if we try to write a value greater than
        the supported bit width for a register.
        Args:
            model: rc model
            temp_coeffs: temporary calculated coefficients to be checked

        Returns:
            error: True if we are writing a value greater than  the supported bit width for a register
        """
        coeff_ceil = self.get_coeff_ceil(model)
        if len(coeff_ceil) != len(temp_coeffs):
            return True
        else:
            coeff_ceil = np.array(coeff_ceil)
            temp_coeffs = np.array(temp_coeffs)
            # check if any temp_coeffs is greater than coeff_ceil
            error = np.any((coeff_ceil - temp_coeffs) < 0)

            return error

    # Method name: floor_filter_coefficients
    # Defined in: ocelot\calculators\calc_shaping.py
    def floor_filter_coefficients(self, h):
        # allow non negative h
        return h

    # Method name: gaussian
    # Defined in: common\calculators\calc_shaping.py
    @staticmethod
    def gaussian(M, std, sym=True):
        r"""Return a Gaussian window.
        Parameters
        ----------
        M : int
            Number of points in the output window. If zero or less, an empty
            array is returned.
        std : float
            The standard deviation, sigma.
        sym : bool, optional
            When True (default), generates a symmetric window, for use in filter
            design.
            When False, generates a periodic window, for use in spectral analysis.
        Returns
        -------
        w : ndarray
            The window, with the maximum value normalized to 1 (though the value 1
            does not appear if `M` is even and `sym` is True).
        Notes
        -----
        The Gaussian window is defined as
        .. math::  w(n) = e^{ -\frac{1}{2}\left(\frac{n}{\sigma}\right)^2 }
        """
        if M < 1:
            return tinynumpy.array([])
        if M == 1:
            return tinynumpy.ones(1, 'd')
        odd = M % 2
        if not sym and not odd:
            M = M + 1
        n = tinynumpy.arange(0, M) - (M - 1.0) / 2.0
        sig2 = 2 * std * std
        w = tinynumpy.exp(-n ** int(2) * (1 / sig2))
        if not sym and not odd:
            w = w[:-1]
        return w

    # Method name: gaussian_shaping_filter
    # Defined in: rainier\calculators\calc_shaping.py
    def gaussian_shaping_filter(self, model, scaling_fac):
        """

          Args:
              model (ModelRoot) : Data model to read and write variables from
          """

        # for gaussian pulse shapes pulse_shape_parameter holds BT value
        bt = model.vars.shaping_filter_param.value
        max_filter_taps = model.vars.max_filter_taps.value
        req_filter_taps = self.get_required_filter_taps(bt)
        modulator_select = model.vars.modulator_select.value
        implement_even_mode = False

        if req_filter_taps > max_filter_taps:
            minumum_bt_supported = 8 / max_filter_taps
            bt = minumum_bt_supported
            LogMgr.Error(
                "ERROR: BT < {} not supported on this part, overriding the current BT to {}".format(minumum_bt_supported,
                                                                                                    minumum_bt_supported))

        # MCUW_RADIO_CFG-2372 - IQMOD or IQ_MOD_DIRECT can only use EVEN Mode
        if modulator_select in [model.vars.modulator_select.var_enum.IQ_MOD, model.vars.modulator_select.var_enum.IQ_MOD_DIRECT]:
            implement_even_mode = True
            if req_filter_taps > 16:
                bt = 8 / 16
                LogMgr.Error("ERROR: BT < 0.5 not supported, overriding the current BT to {}".format(bt))

        # Even mode uses 16 taps (c0, c1...c7, c7, c6... c1, c0). Therefore anything that needs less than 16 taps can be
        # implemented using Even mode
        if implement_even_mode:
            shaping = 2  # sets shaping filter in Even mode
            # map BT value to standard deviation
            std = 1.05 / bt

            # generate gaussian pulse shape
            w = self.gaussian(17, std)
            # scale for unit DC gain
            w = tinynumpy.divide(w, w.sum())
            # convolve with square wave of oversampling rate width which is 8 for the shaping filter
            f_hack = tinynumpy.convolve(w, tinynumpy.ones((1, 8)).flatten())
            # scale and quantize coefficients, using 127 scaling factor to match Qiang's matlab sims
            c_hack = tinynumpy.round_((scaling_fac * f_hack))
            # keep only 8 coeffs from the peak filter tap
            coeff = c_hack[4:12]

            return coeff, shaping

        else:
            shaping = 3  # sets shaping filter in Asymmetric mode
            # map BT value to standard deviation
            std = 1.05 / bt

            # generate gaussian pulse shape
            w = self.gaussian(int(max_filter_taps + 1 - 8), std)  # To get max_filter_taps points after convolution
            # scale for unit DC gain
            w = tinynumpy.divide(w, w.sum())
            # convolve with square wave of oversampling rate width which is 8 for the shaping filter
            f_hack = tinynumpy.convolve(w, tinynumpy.ones((1, 8)).flatten())
            # scale and quantize coefficients
            c_hack = tinynumpy.round_((scaling_fac * f_hack))
            # keep only non 0 coeffs as 0 coeffs in the beginning add unnecessary delay to the TX chain
            c_hack = np.array(c_hack)
            coeff = c_hack[c_hack != 0]
            # return coeffs
            return coeff, shaping


    # Method name: get_coeff_ceil
    # Defined in: ocelot\calculators\calc_shaping.py
    def get_coeff_ceil(self, model):
        # all filter taps are 8 bit signed registers
        max_filter_taps = model.vars.max_filter_taps.value
        coeff_ceil = np.empty(max_filter_taps)
        # all filter taps are 8 bit signed registers
        coeff_ceil.fill((2 ** (8 - 1)) - 1)
        return coeff_ceil

    # Method name: get_required_filter_taps
    # Defined in: common\calculators\calc_shaping.py
    def get_required_filter_taps(self, bt):
        """
        Calculate required filter taps for gaussian shaping filter with BT
        Pulse shaping will spread over (1/bt) symbols. Since shaping filter is implemented at 8*baudrate, the required
        taps for a bt will be 8/bt
        :param bt:Bandwidth time product
        :return: req_filter_taps
        """
        req_filter_taps = math.ceil(8 / bt)
        return req_filter_taps

    # Method name: get_shaping_filter
    # Defined in: ocelot\calculators\calc_shaping.py
    def calc_shaping_filter(self, model):
        # Construct shaping filter from register settings

        # TODO: implement IP read
        shaping_filter_mode = model.vars.MOD_CTRL0_SHAPING.value
        c0 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING0_COEFF0.value, model.vars.MOD_SHAPING0_COEFF1.get_bit_width())
        c1 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING0_COEFF1.value, model.vars.MOD_SHAPING0_COEFF1.get_bit_width())
        c2 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING0_COEFF2.value, model.vars.MOD_SHAPING0_COEFF2.get_bit_width())
        c3 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING0_COEFF3.value, model.vars.MOD_SHAPING0_COEFF3.get_bit_width())
        c4 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING1_COEFF4.value, model.vars.MOD_SHAPING1_COEFF4.get_bit_width())
        c5 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING1_COEFF5.value, model.vars.MOD_SHAPING1_COEFF5.get_bit_width())
        c6 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING1_COEFF6.value, model.vars.MOD_SHAPING1_COEFF6.get_bit_width())
        c7 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING1_COEFF7.value, model.vars.MOD_SHAPING1_COEFF7.get_bit_width())
        c8 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING2_COEFF8.value, model.vars.MOD_SHAPING2_COEFF8.get_bit_width())
        c9 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING2_COEFF9.value, model.vars.MOD_SHAPING2_COEFF9.get_bit_width())
        c10 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING2_COEFF10.value, model.vars.MOD_SHAPING2_COEFF10.get_bit_width())
        c11 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING2_COEFF11.value, model.vars.MOD_SHAPING2_COEFF11.get_bit_width())
        c12 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING3_COEFF12.value, model.vars.MOD_SHAPING3_COEFF12.get_bit_width())
        c13 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING3_COEFF13.value, model.vars.MOD_SHAPING3_COEFF13.get_bit_width())
        c14 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING3_COEFF14.value, model.vars.MOD_SHAPING3_COEFF14.get_bit_width())
        c15 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING3_COEFF15.value, model.vars.MOD_SHAPING3_COEFF15.get_bit_width())
        c16 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING4_COEFF16.value, model.vars.MOD_SHAPING4_COEFF16.get_bit_width())
        c17 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING4_COEFF17.value, model.vars.MOD_SHAPING4_COEFF17.get_bit_width())
        c18 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING4_COEFF18.value, model.vars.MOD_SHAPING4_COEFF18.get_bit_width())
        c19 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING4_COEFF19.value, model.vars.MOD_SHAPING4_COEFF19.get_bit_width())
        c20 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING5_COEFF20.value, model.vars.MOD_SHAPING5_COEFF20.get_bit_width())
        c21 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING5_COEFF21.value, model.vars.MOD_SHAPING5_COEFF21.get_bit_width())
        c22 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING5_COEFF22.value, model.vars.MOD_SHAPING5_COEFF22.get_bit_width())
        c23 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING5_COEFF23.value, model.vars.MOD_SHAPING5_COEFF23.get_bit_width())
        c24 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING6_COEFF24.value, model.vars.MOD_SHAPING6_COEFF24.get_bit_width())
        c25 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING6_COEFF25.value, model.vars.MOD_SHAPING6_COEFF25.get_bit_width())
        c26 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING6_COEFF26.value, model.vars.MOD_SHAPING6_COEFF26.get_bit_width())
        c27 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING6_COEFF27.value, model.vars.MOD_SHAPING6_COEFF27.get_bit_width())
        c28 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING7_COEFF28.value, model.vars.MOD_SHAPING7_COEFF28.get_bit_width())
        c29 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING7_COEFF29.value, model.vars.MOD_SHAPING7_COEFF29.get_bit_width())
        c30 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING7_COEFF30.value, model.vars.MOD_SHAPING7_COEFF30.get_bit_width())
        c31 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING7_COEFF31.value, model.vars.MOD_SHAPING7_COEFF31.get_bit_width())
        c32 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING8_COEFF32.value, model.vars.MOD_SHAPING8_COEFF32.get_bit_width())
        c33 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING8_COEFF33.value, model.vars.MOD_SHAPING8_COEFF33.get_bit_width())
        c34 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING8_COEFF34.value, model.vars.MOD_SHAPING8_COEFF34.get_bit_width())
        c35 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING8_COEFF35.value, model.vars.MOD_SHAPING8_COEFF35.get_bit_width())
        c36 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING9_COEFF36.value, model.vars.MOD_SHAPING9_COEFF36.get_bit_width())
        c37 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING9_COEFF37.value, model.vars.MOD_SHAPING9_COEFF37.get_bit_width())
        c38 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING9_COEFF38.value, model.vars.MOD_SHAPING9_COEFF38.get_bit_width())
        c39 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING9_COEFF39.value, model.vars.MOD_SHAPING9_COEFF39.get_bit_width())
        c40 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING10_COEFF40.value, model.vars.MOD_SHAPING10_COEFF40.get_bit_width())
        c41 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING10_COEFF41.value, model.vars.MOD_SHAPING10_COEFF41.get_bit_width())
        c42 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING10_COEFF42.value, model.vars.MOD_SHAPING10_COEFF42.get_bit_width())
        c43 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING10_COEFF43.value, model.vars.MOD_SHAPING10_COEFF43.get_bit_width())
        c44 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING11_COEFF44.value, model.vars.MOD_SHAPING11_COEFF44.get_bit_width())
        c45 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING11_COEFF45.value, model.vars.MOD_SHAPING11_COEFF45.get_bit_width())
        c46 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING11_COEFF46.value, model.vars.MOD_SHAPING11_COEFF46.get_bit_width())
        c47 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING11_COEFF47.value, model.vars.MOD_SHAPING11_COEFF47.get_bit_width())
        c48 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING12_COEFF48.value, model.vars.MOD_SHAPING12_COEFF48.get_bit_width())
        c49 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING12_COEFF49.value, model.vars.MOD_SHAPING12_COEFF49.get_bit_width())
        c50 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING12_COEFF50.value, model.vars.MOD_SHAPING12_COEFF50.get_bit_width())
        c51 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING12_COEFF51.value, model.vars.MOD_SHAPING12_COEFF51.get_bit_width())
        c52 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING13_COEFF52.value, model.vars.MOD_SHAPING13_COEFF52.get_bit_width())
        c53 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING13_COEFF53.value, model.vars.MOD_SHAPING13_COEFF53.get_bit_width())
        c54 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING13_COEFF54.value, model.vars.MOD_SHAPING13_COEFF54.get_bit_width())
        c55 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING13_COEFF55.value, model.vars.MOD_SHAPING13_COEFF55.get_bit_width())
        c56 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING14_COEFF56.value, model.vars.MOD_SHAPING14_COEFF56.get_bit_width())
        c57 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING14_COEFF57.value, model.vars.MOD_SHAPING14_COEFF57.get_bit_width())
        c58 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING14_COEFF58.value, model.vars.MOD_SHAPING14_COEFF58.get_bit_width())
        c59 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING14_COEFF59.value, model.vars.MOD_SHAPING14_COEFF59.get_bit_width())
        c60 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING15_COEFF60.value, model.vars.MOD_SHAPING15_COEFF60.get_bit_width())
        c61 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING15_COEFF61.value, model.vars.MOD_SHAPING15_COEFF61.get_bit_width())
        c62 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING15_COEFF62.value, model.vars.MOD_SHAPING15_COEFF62.get_bit_width())
        c63 = self._covert_twos_complement_to_signed(model.vars.MOD_SHAPING15_COEFF63.value, model.vars.MOD_SHAPING15_COEFF63.get_bit_width())

        if shaping_filter_mode == 0:
            shaping_filter = [127, 127, 127, 127, 127, 127, 127, 127]

        elif shaping_filter_mode == 1:
            shaping_filter = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c7, c6, c5, c4, c3, c2, c1, c0]

        elif shaping_filter_mode == 2:
            shaping_filter = [c0, c1, c2, c3, c4, c5, c6, c7, c7, c6, c5, c4, c3, c2, c1, c0]

        else:
            shaping_filter = [c0,  c1,  c2,  c3,  c4,  c5,  c6,  c7,  c8,  c9, c10, c11, c12, c13, c14, c15,
                            c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31,
                            c32, c33, c34, c35, c36, c37, c38, c39, c40, c41, c42, c43, c44, c45, c46, c47,
                            c48, c49, c50, c51, c52, c53, c54, c55, c56, c57, c58, c59, c60, c61, c62, c63]

        model.vars.shaping_filter_coeffs.value = shaping_filter

    # Method name: root_raised_cosine_filter
    # Defined in: ocelot\calculators\calc_shaping.py
    def root_raised_cosine_filter(self, model):
        """

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        # for raised cosine pulse shapes pulse_shape_parameter holds roll off factor value
        bt = model.vars.shaping_filter_param.value
        max_filter_taps = model.vars.max_filter_taps.value

        if bt > 1.0 or bt < 0.0:
            LogMgr.Error("shaping_filter_param for Root Raised Cosine filter is treated as Roll-off factor. "
                         "Please ensure that 0 <= shaping_filter_param <= 1. "
                         "Overriding the current shaping_filter_param value to 0.")
            bt = 0.0

        pi = math.pi
        # create empty coefficient array
        h = [0.0] * max_filter_taps
        # for each coeff to be calculated
        for x in tinynumpy.arange(0, max_filter_taps):
            # get time index
            x = int(x)
            t = (x - int(max_filter_taps/2)) / 8.0
            # handle special cases and calculate the coeffs
            if t == 0.0:
                h[x] = (1-bt)+4*bt/pi
            elif bt != 0 and t == 1/(4*bt):
                h[x] = bt/math.sqrt(2) * ((1+2/pi)*math.sin(pi/(4*bt))+(1-2/pi)*math.cos(pi/(4*bt)))
            elif bt != 0 and t == -1/(4*bt):
                h[x] = bt/math.sqrt(2) * ((1+2/pi)*math.sin(pi/(4*bt))+(1-2/pi)*math.cos(pi/(4*bt)))
            else:
                h[x] = (math.sin(pi*t*(1-bt)) + 4*bt*t*math.cos(pi*t*(1+bt)))/( pi*t*(1-(4*bt*t)*(4*bt*t)) )

        # scale so that the peak tap is 127
        peak = max(h)
        for x in tinynumpy.arange(0, max_filter_taps):
            x = int(x)
            h[x] = py2round(h[x] / peak * 127 - 0.5)
            if h[x] < 0:
                h[x] = self.floor_filter_coefficients(h[x])

        return h

    # Method name: raised_cosine_filter
    # Defined in: common\calculators\calc_shaping.py
    def raised_cosine_filter(self, model):
        """

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        # for raised cosine pulse shapes pulse_shape_parameter holds roll off factor value
        bt = model.vars.shaping_filter_param.value

        if bt > 1.0 or bt < 0.0:
            LogMgr.Error("shaping_filter_param for Raised Cosine filter is treated as Roll-off factor. "
                         "Please ensure that 0 <= shaping_filter_param <= 1. "
                         "Overriding the current shaping_filter_param value to 1.")
            bt = 1.0
        # create empty coefficient array
        #h = tinynumpy.zeros((17,), dtype=float)
        h = [0.0] * 17
        # for each coeff to be calculated
        for x in tinynumpy.arange(0, 17):
            # get time index
            x = int(x)
            t = (x - 8) / 8.0
            # handle special cases and calculate the coeffs
            if t == 0.0:
                h[x] = 127
            elif bt != 0 and t == 1/(2*bt):
                h[x] = py2round(127*(math.pi/4)*(math.sin(math.pi*t)/(math.pi*t)))
            elif bt != 0 and t == -1/(2*bt):
                h[x] = py2round(127*(math.pi/4)*(math.sin(math.pi*t)/(math.pi*t)))
            else:
                h[x] = py2round(127*(math.sin(math.pi*t)/(math.pi*t))*(math.cos(math.pi*bt*t)/(1-(((2*bt*t))*((2*bt*t))))))
        # keep only first half of coeffs
        coeff = h[0:9]

        return coeff

    # Method name: run_shaping_filter_calc
    # Defined in: rainier\calculators\calc_shaping.py
    def run_shaping_filter_calc(self, model):
        shaping_filter_option = model.vars.shaping_filter.value
        max_filter_taps = model.vars.max_filter_taps.value
        coeff = np.zeros(max_filter_taps)
        shaping = 0
        if shaping_filter_option.value == model.vars.shaping_filter.var_enum.NONE.value:
            shaping = 0
        elif shaping_filter_option.value == model.vars.shaping_filter.var_enum.Gaussian.value:
            scaling_fac = 127
            c, shaping = self.gaussian_shaping_filter(model, scaling_fac)
            coeff = self.update_coeffs(model, c, coeff)
        elif shaping_filter_option.value == model.vars.shaping_filter.var_enum.Custom_OQPSK.value:
            # Not sure what filter this is
            coeff[0] = coeff[1] = 1
            coeff[2] = 16
            coeff[3] = 48
            coeff[4] = 80
            coeff[5] = 112
            coeff[6] = coeff[7] = 127
            coeff[8] = 0
            shaping = 2
        elif shaping_filter_option.value == model.vars.shaping_filter.var_enum.Raised_Cosine.value:
            c = self.raised_cosine_filter(model)
            shaping = 1
            coeff = self.update_coeffs(model, c, coeff)
        elif shaping_filter_option.value == model.vars.shaping_filter.var_enum.Root_Raised_Cosine.value:
            c = self.root_raised_cosine_filter(model)
            shaping = 3
            coeff = self.update_coeffs(model, c, coeff)
        elif shaping_filter_option.value == model.vars.shaping_filter.var_enum.Custom_PSK.value:
            coeff[0] = 51
            coeff[1] = 117
            coeff[2] = 96
            coeff[3] = 53
            coeff[4] = 20
            coeff[5] = 2
            coeff[6] = 0
            coeff[7] = 0
            coeff[8] = 0  # not used
            shaping = 3
        else:
            raise CalculationException("ERROR: Unrecognized shaping filter option")
        return coeff, shaping

    # Method name: update_coeffs
    # Defined in: jumbo\calculators\calc_shaping.py
    def update_coeffs(self, model, calc_c, coeff):
        """
        Coefficients calculated are mostly not the same length as the available filter taps. This method basically copys
        the calculated coefficients (from COEFF0 onwards) to corresponding taps and keep other non-calculated tap's
        coeffs to 0

        Args:
            model: rc model
            calc_c: calculated coefficients
            coeff: coefficients that will be copied into registers

        Returns:
            coeff: coefficents with calculated coeffs
        """
        max_filter_taps = model.vars.max_filter_taps.value
        # replace calculated coefficients and keep others as 0
        for idx in range(len(calc_c)):
            if idx > max_filter_taps:
                coeff[idx] = 0
            else:
                coeff[idx] = calc_c[idx]
        return coeff

    # Method name: write_coeff_registers
    # Defined in: ocelot\calculators\calc_shaping.py
    def write_coeff_registers(self, model, coeff, shaping):

        self._ip_reg_write(model, 'SHAPING0_COEFF0', int(coeff[0]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING0_COEFF1', int(coeff[1]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING0_COEFF2', int(coeff[2]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING0_COEFF3', int(coeff[3]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING1_COEFF4', int(coeff[4]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING1_COEFF5', int(coeff[5]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING1_COEFF6', int(coeff[6]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING1_COEFF7', int(coeff[7]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING2_COEFF8', int(coeff[8]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING2_COEFF9', int(coeff[9]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING2_COEFF10', int(coeff[10]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING2_COEFF11', int(coeff[11]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING3_COEFF12', int(coeff[12]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING3_COEFF13', int(coeff[13]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING3_COEFF14', int(coeff[14]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING3_COEFF15', int(coeff[15]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING4_COEFF16', int(coeff[16]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING4_COEFF17', int(coeff[17]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING4_COEFF18', int(coeff[18]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING4_COEFF19', int(coeff[19]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING5_COEFF20', int(coeff[20]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING5_COEFF21', int(coeff[21]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING5_COEFF22', int(coeff[22]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING5_COEFF23', int(coeff[23]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING6_COEFF24', int(coeff[24]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING6_COEFF25', int(coeff[25]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING6_COEFF26', int(coeff[26]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING6_COEFF27', int(coeff[27]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING7_COEFF28', int(coeff[28]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING7_COEFF29', int(coeff[29]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING7_COEFF30', int(coeff[30]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING7_COEFF31', int(coeff[31]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING8_COEFF32', int(coeff[32]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING8_COEFF33', int(coeff[33]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING8_COEFF34', int(coeff[34]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING8_COEFF35', int(coeff[35]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING9_COEFF36', int(coeff[36]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING9_COEFF37', int(coeff[37]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING9_COEFF38', int(coeff[38]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING9_COEFF39', int(coeff[39]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING10_COEFF40', int(coeff[40]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING10_COEFF41', int(coeff[41]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING10_COEFF42', int(coeff[42]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING10_COEFF43', int(coeff[43]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING11_COEFF44', int(coeff[44]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING11_COEFF45', int(coeff[45]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING11_COEFF46', int(coeff[46]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING11_COEFF47', int(coeff[47]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING12_COEFF48', int(coeff[48]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING12_COEFF49', int(coeff[49]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING12_COEFF50', int(coeff[50]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING12_COEFF51', int(coeff[51]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING13_COEFF52', int(coeff[52]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING13_COEFF53', int(coeff[53]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING13_COEFF54', int(coeff[54]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING13_COEFF55', int(coeff[55]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING14_COEFF56', int(coeff[56]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING14_COEFF57', int(coeff[57]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING14_COEFF58', int(coeff[58]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING14_COEFF59', int(coeff[59]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING15_COEFF60', int(coeff[60]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING15_COEFF61', int(coeff[61]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING15_COEFF62', int(coeff[62]), allow_neg=True)
        self._ip_reg_write(model, 'SHAPING15_COEFF63', int(coeff[63]), allow_neg=True)

        self._ip_reg_write(model, 'CTRL0_SHAPING', shaping)