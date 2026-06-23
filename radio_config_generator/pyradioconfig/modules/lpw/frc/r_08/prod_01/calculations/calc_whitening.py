from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcWhitening(IPCalculator):

    # Method name: calc_white_settings
    # Defined in: common\calculators\calc_white.py
    def calc_white_settings(self, model):
        """
        This is a dictionary lookup of each of the supported CRC Polynomials\n
        Each dictionary entry is a tuple which maps to the following entries:\n
          (POLY, XORFEEDBACK, FEEDBACKSEL)\n
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        WHITE_POLY_LOOKUP = {
            model.vars.white_poly.var_enum.PN9.value: (0x00000108, 0, 0),
            model.vars.white_poly.var_enum.PN9_BYTE.value: (0x00000100, 1, 5),
            model.vars.white_poly.var_enum.PN16.value: (0x00008016, 0, 0),
            model.vars.white_poly.var_enum.BLE.value: (0x00000044, 0, 0),
            model.vars.white_poly.var_enum.Bytewise_XOR_seed_LSB.value: (0x00000080, 0, 0),
            model.vars.white_poly.var_enum.PN9_802154.value: (0x100, 1, 5),
            model.vars.white_poly.var_enum.ANT_TYPE1_XORINTERNAL: (0x108, 0, 0),
            model.vars.white_poly.var_enum.ANT_TYPE1_XOREXTERNAL: (0x21, 0, 8),
            model.vars.white_poly.var_enum.BLE_HDT: (0x00006000, 0, 0)
        }
        if model.vars.ber_force_whitening.value == True:
            self._ip_reg_write(model, 'WHITEPOLY_POLY', 0x0100)
            self._ip_reg_write(model, 'WHITECTRL_XORFEEDBACK', 1)
            self._ip_reg_write(model, 'WHITECTRL_FEEDBACKSEL', 4)
            self._ip_reg_write(model, 'WHITEINIT_WHITEINIT', 0x0138)
            self._ip_reg_write(model, 'WHITECTRL_SHROUTPUTSEL', 0)
        elif model.vars.white_poly.value.value != model.vars.white_poly.var_enum.NONE.value:
            white_params = WHITE_POLY_LOOKUP[model.vars.white_poly.value.value]
            # Handle POLY configuration
            self._ip_reg_write(model, 'WHITEPOLY_POLY', white_params[0])
            # Subtract 1 from the CRC size to get the proper value
            self._ip_reg_write(model, 'WHITECTRL_XORFEEDBACK', white_params[1])
            self._ip_reg_write(model, 'WHITECTRL_FEEDBACKSEL', white_params[2])
            self._ip_reg_write(model, 'WHITEINIT_WHITEINIT', model.vars.white_seed.value)
            self._ip_reg_write(model, 'WHITECTRL_SHROUTPUTSEL', model.vars.white_output_bit.value)

        else:
            # Defaults if whitening is disabled
            self._ip_reg_write(model, 'WHITECTRL_XORFEEDBACK', 0)
            self._ip_reg_write(model, 'WHITECTRL_FEEDBACKSEL', 0)
            self._ip_reg_write(model, 'WHITEINIT_WHITEINIT', 0)

            # If whitening is disabled, set the following values to whatever they were set to in
            # the block coding code in case it is enabled.
            self._ip_reg_write(model, 'WHITECTRL_SHROUTPUTSEL', model.vars.frame_coding_fshroutputsel_val.value)
            self._ip_reg_write(model, 'WHITEPOLY_POLY', model.vars.frame_coding_poly_val.value)

    def calc_prewhite_reg(self, model):
        # Default value for prewhite_en is False
        model.vars.prewhite_en.value = False

        self._ip_reg_write(model, 'WHITECTRL_PREWHITE', int(model.vars.prewhite_en.value))