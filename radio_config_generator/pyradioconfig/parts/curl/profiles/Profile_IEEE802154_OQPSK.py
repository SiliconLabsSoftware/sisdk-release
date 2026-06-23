from pyradioconfig.parts.common.profiles.curl_regs import build_modem_regs_curl
from pyradioconfig.parts.lion.profiles.Profile_IEEE802154_OQPSK import ProfileIEEE802154OQPSKLion
from pyradioconfig.parts.curl.ip_collector.ip_collector_curl import IPCollector_Curl


class ProfileIEEE802154OQPSKCurl(ProfileIEEE802154OQPSKLion):

    def __init__(self):
        super().__init__()
        self._profileName = "IEEE802154OQPSK"
        self._readable_name = "IEEE802154 OQPSK Profile"
        self._category = ""
        self._description = "Profile used for IEEE802154 OQPSK phys"
        self._default = False
        self._activation_logic = ""
        self._family = "curl"
        self._skip_target_calculation = True

    def build_register_profile_outputs(self, model, profile):
        build_modem_regs_curl(model, profile)
        IPCollector_Curl(model.part_family, model.part_revision).build_all_peripheral_regs(model, profile)