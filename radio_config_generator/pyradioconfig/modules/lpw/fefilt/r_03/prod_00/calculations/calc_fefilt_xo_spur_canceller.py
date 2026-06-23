import math
from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from scipy import interpolate

class CalcXOSpurCanceller(IPCalculator):
    def calc_spurcancel_mode(self, model):
        # Spur cancellers are disabled by default
        model.vars.spurcancel0_mode.value = model.vars.spurcancel0_mode.var_enum.DISABLED
        model.vars.spurcancel1_mode.value = model.vars.spurcancel0_mode.var_enum.DISABLED

    def calc_spurcancel_freq(self, model):
        # 0 by default
        model.vars.spurcancel0_freq.value = 0
        model.vars.spurcancel1_freq.value = 0

    def calc_spurcancel_en_regs(self, model):
        spurcancel0_mode = model.vars.spurcancel0_mode.value
        spurcancel1_mode = model.vars.spurcancel1_mode.value

        sc0en = (spurcancel0_mode != model.vars.spurcancel0_mode.var_enum.DISABLED)
        sc1en = (spurcancel1_mode != model.vars.spurcancel0_mode.var_enum.DISABLED)
        scen = 1 if (sc0en or sc1en) else 0

        self._ip_reg_write(model, 'SCMSTRCTRL_SCEN', scen)
        self._ip_reg_write(model, 'SCCTRL0_SCMODE', int(spurcancel0_mode))
        self._ip_reg_write(model, 'SCCTRL1_SCMODE', int(spurcancel1_mode))

    def calc_spurcancel_freq_regs(self, model):
        # This method sets the spurcancel freq regs based on a target frequency in Hz
        spurcancel0_freq = model.vars.spurcancel0_freq.value
        spurcancel1_freq = model.vars.spurcancel1_freq.value
        digmix_res_actual = model.vars.digmix_res_actual.value

        spurfreq0_reg = int(round(spurcancel0_freq / digmix_res_actual))
        spurfreq1_reg = int(round(spurcancel1_freq / digmix_res_actual))

        self._ip_reg_write(model, 'SPURFREQ0_SPURFREQ', spurfreq0_reg)
        self._ip_reg_write(model, 'SPURFREQ1_SPURFREQ', spurfreq1_reg)

    def calc_fefilt_spurcancel_misc(self, model):
        # Default configuration for spur canceller

        self._ip_reg_write(model, 'SCMSTRCTRL_SCRST', 0)
        self._ip_reg_write(model, 'SCCONFIG_LPFSEL', 1) # IIR
        self._ip_reg_write(model, 'SCCONFIG_MASEL', 3)  # 8-sample MA
        self._ip_reg_write(model, 'SCCONFIG_IIRLATCHED', 0)  # Unlatched IIR
        self._ip_reg_write(model, 'SCCONFIG_PAUSECTRL', 0)  # Pause disabled
        self._ip_reg_write(model, 'SCCONFIG_AGCRESTART', 0)  # Disable AGC restart
        self._ip_reg_write(model, 'SCCONFIG_RSSIRESTART', 0)  # Disable RSSI restart
        self._ip_reg_write(model, 'SCCONFIG_RSSILATCHMODE', 0)  # Disable RSSI latch
        self._ip_reg_write(model, 'SCCONFIG_GEARINDEXMAX', 5) # Use 5 gears
        self._ip_reg_write(model, 'SCCONFIG_GEARPERM', 32)  # Mantissa for IIR periods is 32

        self._ip_reg_write(model, 'SCPERIOD_SETPERIOD', 23)
        self._ip_reg_write(model, 'SCPERIOD_PAUSEDELAY', 79)
        self._ip_reg_write(model, 'SCPERIOD_PAUSEPERIOD', 99)

        self._ip_reg_write(model, 'SCAGCTHD_AGCINDEXTHDHI', 5)
        self._ip_reg_write(model, 'SCAGCTHD_AGCINDEXTHDLO', 3)
        self._ip_reg_write(model, 'SCAGCTHD_RSSITHDHI', 100)  # Unused
        self._ip_reg_write(model, 'SCAGCTHD_RSSITHDLO', -60, allow_neg=True)

        self._ip_reg_write(model, 'SCGEARPER_GEARPER0', 0)
        self._ip_reg_write(model, 'SCGEARPER_GEARPER1', 1)
        self._ip_reg_write(model, 'SCGEARPER_GEARPER2', 2)
        self._ip_reg_write(model, 'SCGEARPER_GEARPER3', 3)
        self._ip_reg_write(model, 'SCGEARPER_GEARPER4', 4)
        self._ip_reg_write(model, 'SCGEARPER_GEARPER5', 5)
        self._ip_reg_write(model, 'SCGEARPER_GEARPER6', 6)
        self._ip_reg_write(model, 'SCGEARPER_GEARPER7', 7)

        self._ip_reg_write(model, 'SCIIRGEAR_IIRGEAR0', 5)
        self._ip_reg_write(model, 'SCIIRGEAR_IIRGEAR1', 6)
        self._ip_reg_write(model, 'SCIIRGEAR_IIRGEAR2', 7)
        self._ip_reg_write(model, 'SCIIRGEAR_IIRGEAR3', 8)
        self._ip_reg_write(model, 'SCIIRGEAR_IIRGEAR4', 9)
        self._ip_reg_write(model, 'SCIIRGEAR_IIRGEAR5', 10)
        self._ip_reg_write(model, 'SCIIRGEAR_IIRGEAR6', 11)
        self._ip_reg_write(model, 'SCIIRGEAR_IIRGEAR7', 12)

        self._ip_reg_write(model, 'SCCLIP0_CLIPLEVEL', 0x7FF) #Disabled (max value)
        self._ip_reg_write(model, 'SCCLIP1_CLIPLEVEL', 0x7FF) #Disabled (max value)

