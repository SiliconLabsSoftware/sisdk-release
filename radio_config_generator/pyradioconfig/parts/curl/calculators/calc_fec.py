from pyradioconfig.parts.lion.calculators.calc_fec import CalcFecLion


class CalcFecCurl(CalcFecLion):

    def calc_convramaddr_reg(self, model):

        #Value is static per part
        conv_ram_addr = 0x8000 >> 2

        self._reg_write(model.vars.FRC_CONVRAMADDR_CONVRAMADDR, conv_ram_addr)
