from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPRegFields


class BtcRegFields(IPRegFields):
    reg_field_list = []

    def __init__(self):
        super().__init__()
        self.reg_field_list = [
            'BRVITDEMOD.VITERBIKSI1',
            'BRVITDEMOD.VITERBIKSI2',
            'BRVITDEMOD.VITERBIKSI3',
            'FREQ_COMP.FBAFCGAIN',
            'CTRL3.TXPOLAREN',
            'EDR_TX_GUARD3.EDRGUARDTX',
        ]