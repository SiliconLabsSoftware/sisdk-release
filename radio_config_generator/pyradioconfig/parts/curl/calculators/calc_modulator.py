from pyradioconfig.parts.lion.calculators.calc_modulator import CalcModulatorLion


class CalcModulatorCurl(CalcModulatorLion):
    def calc_txbr_reg(self, model):
        """
        Calculation copied from ocelot. TXBR must vary with xtal_frequency_hz.
        """

        ratio = model.vars.txbr_ratio.value
        txbr_num_err_tol = 0.003
        txbr_max_den = 255
        num = 1275
        den = 255

        # Stocks baudrate ratio
        txbr_num_err_map = {}

        # Find best integer ratio that is below the tolerance
        found_best_ratio = False
        for den in range(txbr_max_den, 0, -1):
            num = ratio * den
            txbr_num_err = abs(round(num) - num)

            if num < 32768:
                txbr_num_err_map[den] = abs(txbr_num_err - txbr_num_err_tol)
                if txbr_num_err < txbr_num_err_tol:
                    found_best_ratio = True
                    break

        # If best integer ratio is not found, re-calculate and find the ratio that is closest to the tolerance
        if not found_best_ratio:
            if len(txbr_num_err_map) > 0:
                den = min(txbr_num_err_map, key=txbr_num_err_map.get)
            else:
                den = 1
            num = ratio * den

        self._reg_write(model.vars.MODEM_TXBR_TXBRNUM, round(num))
        self._reg_write(model.vars.MODEM_TXBR_TXBRDEN, int(den))
