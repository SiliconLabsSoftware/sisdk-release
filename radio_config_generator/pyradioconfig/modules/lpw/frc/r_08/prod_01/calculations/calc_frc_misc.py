from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator

class CalcFrcMisc(IPCalculator):
    def calc_frc_new_bf(self, model):
        self._ip_reg_write_default(model, 'FCD0_SKIPLASTBITS')
        self._ip_reg_write_default(model, 'FCD0_CFGSEL')
        self._ip_reg_write_default(model, 'FCD1_SKIPLASTBITS')
        self._ip_reg_write_default(model, 'FCD1_CFGSEL')
        self._ip_reg_write_default(model, 'FCD2_SKIPLASTBITS')
        self._ip_reg_write_default(model, 'FCD2_CFGSEL')
        self._ip_reg_write_default(model, 'FCD3_SKIPLASTBITS')
        self._ip_reg_write_default(model, 'FCD3_CFGSEL')
        self._ip_reg_write_default(model, 'CTRL_RXABORTHWBEH')
        
        # HWCTRL RXABORT* registers intentionally omitted for prod_01
        self._ip_reg_write_default(model, 'RXCTRL_QUICKRXCONVBYP')
        self._ip_reg_write_default(model, 'RXCTRL_QUICKRXACK')
        self._ip_reg_write_default(model, 'RXCTRL_QUICKRXCRC')
        self._ip_reg_write_default(model, 'RXCTRL_ACCEPTCRCERRORS')
        pass
    def calc_frc_misc_static(self, model):
        self._ip_reg_write(model, 'AUTOCG_AUTOCGEN', 7)
        self._ip_reg_write(model, 'BOICTRL_BOIBITPOS', 0)
        self._ip_reg_write(model, 'BOICTRL_BOIEN', 0)
        self._ip_reg_write(model, 'BOICTRL_BOIFIELDLOC', 0)
        self._ip_reg_write(model, 'BOICTRL_BOIMATCHVAL', 0)
        self._ip_reg_write(model, 'CTRL_RATESELECT', 0)
        self._ip_reg_write(model, 'CTRL_WAITEOFEN', 0)
        self._ip_reg_write(model, 'DFLCTRL_DFLBOIOFFSET', 0)
        self._ip_reg_write(model, 'DSLCTRL_DSLBITORDER', 0)
        self._ip_reg_write(model, 'DSLCTRL_DSLBITS', 0)
        self._ip_reg_write(model, 'DSLCTRL_DSLMINLENGTH', 0)
        self._ip_reg_write(model, 'DSLCTRL_DSLMODE', 0)
        self._ip_reg_write(model, 'DSLCTRL_DSLOFFSET', 0)
        self._ip_reg_write(model, 'DSLCTRL_DSLSHIFT', 0)
        self._ip_reg_write(model, 'DSLCTRL_RXSUPRECEPMODE', 0)
        self._ip_reg_write(model, 'DSLCTRL_STORESUP', 0)
        self._ip_reg_write(model, 'DSLCTRL_SUPSHFFACTOR', 0)
        self._ip_reg_write(model, 'TRAILTXDATACTRL_TXSUPPLENOVERIDE', 0)
        self._ip_reg_write(model, 'WCNTCMP3_SUPPLENFIELDLOC', 0)
        self._ip_reg_write(model, 'WCNTCMP4_SUPPLENGTH', 0)
        self._ip_reg_write(model, 'SPARE_SPARE', 0)
