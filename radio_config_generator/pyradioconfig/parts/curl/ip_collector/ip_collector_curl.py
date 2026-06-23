from pyradioconfig.calculator_model_framework.interfaces.ipcollector import IPCollector_Base
from pyradioconfig.calculator_model_framework.interfaces.design_status_tag import DesignStatusTag

class IPCollector_Curl(IPCollector_Base):
    part_status_tag = DesignStatusTag.PROD

    def build_peripherals(self):
        self.add_peripheral(peripheral_name='HADM', ip_name='hadm', ip_category='lpw', ip_version=1, prod_rev=1)
