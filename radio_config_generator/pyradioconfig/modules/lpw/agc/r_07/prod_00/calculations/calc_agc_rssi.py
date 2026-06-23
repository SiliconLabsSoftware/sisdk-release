from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator


class CalcAgcRssi(IPCalculator):
    def calc_rssiperiod_val(self, model):
        rssi_period_val = 3
        model.vars.rssi_period.value = rssi_period_val

    def calc_rssiperiod_reg(self, model):

        period = model.vars.rssi_period.value

        if period > 15:
            period = 15

        if period < 0:
            period = 0

        self._ip_reg_write(model, 'CTRL1_RSSIPERIOD', period)

    def calc_rssi_access_time(self, model):
        adc_freq_actual = model.vars.adc_freq_actual.value
        rssi_fast = model.vars.AGC_RSSISTEPTHR_RSSIFAST.value == 1
        xtal_freq = model.vars.xtal_frequency_hz.value
        dec0_actual = model.vars.dec0_actual.value
        dec0_rate = adc_freq_actual / 8 / dec0_actual
        demod_rate_actual = model.vars.demod_rate_actual.value
        cfloopdel_actual_us = model.vars.cfloopdel_us_actual.value
        pwrperiod_actual = model.vars.agcperiod_actual.value
        rx_baud_rate_actual = model.vars.rx_baud_rate_actual.value
        rssi_period_sym_actual = model.vars.rssi_period_sym_actual.value

        # : Demod startup delay from Michael Wu
        T1_us = 20 / xtal_freq * 1e6
        T2_us = 1 / dec0_rate
        T3_us = 2 / demod_rate_actual * 1e6
        demod_startup_time_us = T1_us + T2_us + T3_us

        # : RSSI startup delay us
        scalar = 0 if rssi_fast else 2
        rssi_startup_time_us = scalar * pwrperiod_actual / rx_baud_rate_actual * 1e6

        # : RSSI update period us
        rssi_update_period_us = rssi_period_sym_actual / rx_baud_rate_actual * 1e6

        # : Corrected RSSI access time based on Ferenc Plesznik's measurement
        # : MCUW_RADIO_CFG-1950
        correction_factor = 2 if rssi_fast else 3
        correction_us = correction_factor / rx_baud_rate_actual * 1e6

        # : RSSI access time
        rssi_access_time_us = demod_startup_time_us + cfloopdel_actual_us + rssi_startup_time_us + \
                              rssi_update_period_us + correction_factor
        model.vars.rssi_access_time_us_actual.value = rssi_access_time_us

    def calc_rssi_period_actual(self, model):

        #Read in the RSSI period register and take 2 to that power to compute the symbols in the period
        rssi_period_reg = model.vars.AGC_CTRL1_RSSIPERIOD.value
        rssi_period_sym_actual = 2**rssi_period_reg

        model.vars.rssi_period_sym_actual.value = rssi_period_sym_actual
