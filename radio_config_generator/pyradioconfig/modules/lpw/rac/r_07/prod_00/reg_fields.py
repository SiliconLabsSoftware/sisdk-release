from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPRegFields


class RacRegFields(IPRegFields):
    reg_field_list = []

    def __init__(self):
        super().__init__()
        self.reg_field_list = [
            'RFMUX.WIFIRFSELECT',
#            'CTRL.BTCENABLE',
            'DEMODCLKDIS.STATEOFFDEMODCLKDIS',
            'DEMODCLKDIS.STATERXWARMDEMODCLKDIS',
            'DEMODCLKDIS.STATERXSEARCHDEMODCLKDIS',
            'DEMODCLKDIS.STATERXFRAMEDEMODCLKDIS',
            'DEMODCLKDIS.STATERXWRAPUPDEMODCLKDIS',
            'DEMODCLKDIS.STATETXWARMDEMODCLKDIS',
            'DEMODCLKDIS.STATETXDEMODCLKDIS',
            'DEMODCLKDIS.STATETXWRAPUPDEMODCLKDIS',
            'DEMODCLKDIS.STATESHUTDOWNDEMODCLKDIS',
            'MODEMSEL.LPWMODEMSEL',
        ]