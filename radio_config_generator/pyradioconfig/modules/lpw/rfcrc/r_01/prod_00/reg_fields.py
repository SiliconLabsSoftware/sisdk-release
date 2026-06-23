from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPRegFields


class RfcrcRegFields(IPRegFields):
    reg_field_list = []

    def __init__(self):
        super().__init__()
        self.reg_field_list = [
        'CTRL.BITREVERSE',
        'CTRL.BITSPERWORD',
        'CTRL.BYTEREVERSE',
        'CTRL.CRCWIDTH',
        'CTRL.INPUTBITORDER',
        'CTRL.OUTPUTINV',
        'CTRL.PADCRCINPUT',
        'INIT.INIT',
        'POLY.POLY',
        'CTRL1.BITREVERSE1',
        'CTRL1.BYTEREVERSE1',
        'CTRL1.CRCWIDTH1',
        'CTRL1.INPUTBITORDER1',
        'CTRL1.OUTPUTINV1',
        'CTRL1.PADCRCINPUT1',
        'INIT1.INIT1',
        'POLY1.POLY1',
    ]