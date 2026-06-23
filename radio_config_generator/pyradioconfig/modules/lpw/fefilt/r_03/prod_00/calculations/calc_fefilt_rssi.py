from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from math import floor, log2, ceil, log10
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException

class CalcFefiltRSSI(IPCalculator):

    # Method name: calc_rssi_adjust_db
    # Defined in: ocelot\calculators\calc_demodulator.py
    def calc_rssi_adjust_db(self, model):
        # Read in model vars
        rssi_dig_adjust_db = model.vars.rssi_dig_adjust_db.value
        rssi_rf_adjust_db = model.vars.rssi_rf_adjust_db.value
        # Add digital and RF adjustments
        rssi_adjust_db = rssi_dig_adjust_db + rssi_rf_adjust_db
        # Write the model var
        model.vars.rssi_adjust_db.value = rssi_adjust_db


    # Method name: calc_rssi_dig_adjust_db
    # Defined in: lpwh72000\calculators\calc_demodulator.py
    def calc_rssi_dig_adjust_db(self, model):
        # These variables are passed to RAIL so that RSSI corrections can be made to more accurately measure power
        # Read in model vars
        dec0gain = model.vars.FEFILT_DIGIGAINCTRL_DEC0GAIN.value
        dec1_actual = model.vars.dec1_actual.value
        dec1gain_actual = model.vars.dec1gain_actual.value
        digigainen = model.vars.FEFILT_DIGIGAINCTRL_DIGIGAINEN.value
        digigainsel = model.vars.FEFILT_DIGIGAINCTRL_DIGIGAINSEL.value
        digigaindouble = model.vars.FEFILT_DIGIGAINCTRL_DIGIGAINDOUBLE.value
        digigainhalf = model.vars.FEFILT_DIGIGAINCTRL_DIGIGAINHALF.value
        log2x4_actual = model.vars.log2x4_actual.value
        # Calculate gains
        dec0_gain_db = 6.0 * dec0gain
        dec1_gain_linear = (dec1_actual ** 4) * (2 ** (-1 * (log2x4_actual - 4)))
        dec1_gain_db = 20 * log10(
            dec1_gain_linear / 16) + dec1gain_actual  # Normalize so that dec1=0 gives gain=16
        if digigainen:
            digigain_db = -3 + (digigainsel * 0.25)
        else:
            digigain_db = 0
        digigain_db += 6 * digigaindouble - 6 * digigainhalf
        # For consistency / simplicity, let's treat the rssi_adjust_db  output from the calculator like RAIL handles
        # EFR32_FEATURE_SW_CORRECTED_RSSI_OFFSET in that the value is thought to be added to the RSSI
        # So to compensate for the digital gain, the value should be the negative of the excess gain
        # Note that RSSISHIFT is actually subtracted from the RSSI, but EFR32_FEATURE_SW_CORRECTED_RSSI_OFFSET is
        # subtracted from the default RSSISHIFT so that the proper sign is maintained
        rssi_dig_adjust_db = -(dec0_gain_db + dec1_gain_db + digigain_db)
        # Write the vars
        model.vars.rssi_dig_adjust_db.value = rssi_dig_adjust_db


    # Method name: calc_rssi_rf_adjust_db
    # Defined in: rainier\calculators\calc_demodulator.py
    def calc_rssi_rf_adjust_db(self, model):
        model.vars.rssi_rf_adjust_db.value = -15.8