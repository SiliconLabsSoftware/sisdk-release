from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator

class CalcAoX(IPCalculator):

    # Method name: calc_aox_enable
    # Defined in: bobcat\calculators\calc_aox.py
    def calc_aox_enable(self, model):
        # Disable by default
        model.vars.aox_enable.value = model.vars.aox_enable.var_enum.DISABLED

    # Method name: calc_aox_misc
    # Defined in: lpwh72000\calculators\calc_aox.py
    def calc_aox_misc(self, model):
        aox_enable = True if model.vars.aox_enable.value == model.vars.aox_enable.var_enum.ENABLED else False
        if aox_enable:
            disafcsupp = 1  # disable AFC during the CTE
            chfswtrig = 1  # clk cycles to trigger after ets_set_mux, must be non-zero
        else:
            disafcsupp = 0
            chfswtrig = 0
        self._ip_reg_write(model, 'CHFSWCTRL_CHFSWTIME', chfswtrig)
        self._ip_reg_write(model, 'AFC_DISAFCCTE', disafcsupp)

        # TODO: check this, my guess is this is being used for AOX
        self._ip_reg_write(model, 'CHFCTRL_ADJGAINWIN', 85)

    # Method name: calc_timeperiod_reg
    # Defined in: bobcat\calculators\calc_aox.py
    def calc_timeperiod_reg(self, model):
        TIMEPERIOD_FRACTIONAL_BITS = 24
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        timeperiod = int(2 ** TIMEPERIOD_FRACTIONAL_BITS / (xtal_frequency_hz / 1e6))
        self._ip_reg_write(model, 'ANTSWCTRL1_TIMEPERIOD', timeperiod)

    # Method name: calc_aox_misc
    # Defined in: bobcat\calculators\calc_misc.py
    def calc_aox_misc_2(self, model):
        # Always force these to zero so all AoX features are disabled.
        # RAIL will dynamically set these when an AoX  packet is detected.
        # Still write them in the RC so other PHYs are guarenteed to have AoX features disabled and we can
        # exclude ETSLOC, ANTSWTIMSTART, ANTSWTIMSTOP
        self._ip_reg_write(model, 'ANTSWCTRL_ANTSWENABLE', 0)
        self._ip_reg_write(model, 'ANTSWCTRL_CFGANTPATTEN', 0)
