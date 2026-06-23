from pyradioconfig.modules.lpw.btcphy.r_01.prod_00.calculations.calc_btcphy_brvitdemod import CalcBtcphyBrvitdemod
from pyradioconfig.modules.lpw.btcphy.r_01.prod_00.reg_fields import BtcRegFields


class CalcBtcphy_r01(CalcBtcphyBrvitdemod):

    def __init__(self, peripheral_name='BTCPHY'):
        self._reg_field_list = BtcRegFields().reg_field_list
        super().__init__(peripheral_name=peripheral_name)

    def buildVariables(self, model):
        super().buildVariables(model)