from pyradioconfig.calculator_model_framework.interfaces.iprofile import IProfile
from pyradioconfig.parts.common.profiles.curl_regs import build_modem_regs_curl
from pyradioconfig.parts.lion.profiles.Profile_BLE import ProfileBLELion
from pyradioconfig.parts.curl.ip_collector.ip_collector_curl import IPCollector_Curl


class ProfileBLECurl(ProfileBLELion):

    def __init__(self):
        super().__init__()
        self._profileName = "BLE"
        self._readable_name = "Bluetooth Low Energy Profile"
        self._category = ""
        self._description = "Profile used for BLE phys"
        self._default = False
        self._activation_logic = ""
        self._family = "curl"
        self._skip_target_calculation = True

    def build_register_profile_outputs(self, model, profile):
        build_modem_regs_curl(model, profile)
        IPCollector_Curl(model.part_family, model.part_revision).build_all_peripheral_regs(model, profile)

    def _build_feature_settings(self, model):
        ble_feature = model.profile.inputs.ble_feature.var_value

        if ble_feature == model.vars.ble_feature.var_enum.LE_1M:
            self._copy_model_variables_from_phy(model, 'PHY_Bluetooth_LE_Viterbi_noDSA')
        elif ble_feature == model.vars.ble_feature.var_enum.LE_2M:
            self._copy_model_variables_from_phy(model, 'PHY_Bluetooth_LE_2M_Viterbi_noDSA_fullrate')
        elif ble_feature == model.vars.ble_feature.var_enum.CODED_125K:
            self._copy_model_variables_from_phy(model, 'PHY_Bluetooth_LongRange_nodsa_125kbps')
        elif ble_feature == model.vars.ble_feature.var_enum.CODED_500K:
            self._copy_model_variables_from_phy(model, 'PHY_Bluetooth_LongRange_nodsa_500kbps')
        elif ble_feature == model.vars.ble_feature.var_enum.AOX_1M:
            self._copy_model_variables_from_phy(model, 'PHY_Bluetooth_LE_Viterbi_noDSA_fullrate')
        elif ble_feature == model.vars.ble_feature.var_enum.AOX_2M:
            self._copy_model_variables_from_phy(model, 'PHY_Bluetooth_LE_2M_Viterbi_noDSA_fullrate')
        elif ble_feature == model.vars.ble_feature.var_enum.CONCURRENT:
            self._copy_model_variables_from_phy(model, 'PHY_Bluetooth_1M_Concurrent')
