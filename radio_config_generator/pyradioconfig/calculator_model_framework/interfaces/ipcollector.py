"""Interface to collect all IPs and their respective calculations for a part"""

import importlib
from host_py_rm_studio_internal import RM_Factory
import inspect
from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPRegFields
from pycalcmodel.core.output import ModelOutput, ModelOutputType
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr
from pyradioconfig.calculator_model_framework.interfaces.design_status_tag import DesignStatusTag


class IPCollector_Base(object):
    perip_dict = dict()
    part_status_tag = None

    def __init__(self, part_family, part_rev):
        self.perip_dict.clear()
        if part_rev == 'ANY':
            self.reg_map = RM_Factory(part_family.upper())()
        else:
            self.reg_map = RM_Factory(part_family.upper(), part_rev.upper())()
        self.build_peripherals()

    def add_peripheral(self, peripheral_name:str, ip_name: str, ip_category: str, ip_version:int=None, prod_rev:int=None, skip_for_target_sim:bool=False):
        """
        Adds peripheral to self.perip_dict with version details with status tag - 'in production'

        Args:
            peripheral_name : this is the peripheral name as used in the register model/
            ip_name : this is the name of the ip that is defined in the pyradioconfig/modules/...
            ip_category : this tells whether the IP calculator is in pyradioconfig/modules/lpw or pyradioconfig/modules/wifi...
            ip_version : (Optional) this denotes the design revision r_X. r_01 means ip_version = 1 and matches with the value of IPREVISION.IPREVISION. If not specified, IPREVISION.IPREVISION of the peripheral is read and that ip_version is used.
            prod_rev : (Optional) this is used for a part with PROD tag to point the ip_collector to correct IP calculation snapshot revision. It should be left alone or set to 'None' for DEV parts.
        """
        if ip_version is None:
            ip_version = self.read_ip_ver_from_reg_map(peripheral_name)

        # if chip tag is prod, set default prod_rev to 0
        if self.part_status_tag == DesignStatusTag.PROD and prod_rev is None:
            prod_rev = 0

        self.perip_dict[peripheral_name] = IP_Peripheral_Base(peripheral_name, ip_name, ip_category, ip_version, prod_rev, skip_for_target_sim)

    def build_peripherals(self):
        """Placeholder function for assembling ips"""
        pass

    def build_all_peripheral_regs(self, model, profile):
        """For each ip, reg modules and build regs"""
        for peripheral_name, ip_obj in self.perip_dict.items():
            if model.target.upper() == 'SIM' and ip_obj.skip_for_target_sim:
                continue
            self.build_peripheral_regs(model, profile, peripheral_name)
        pass


    def get_ip_regfield_list(self, part_family, peripheral_name):
        peripheral = self.perip_dict[peripheral_name]
        module_path = peripheral.get_regfields_module_path(part_family)

        module = importlib.import_module(module_path)
        classes = inspect.getmembers(module, inspect.isclass)
        ip_regfields_class = None
        for (classname, classvalue) in classes:
            if issubclass(classvalue, IPRegFields) and classname != 'IPRegFields':
                ip_regfields_class = classvalue
                return ip_regfields_class().reg_field_list

        if ip_regfields_class is None:
            raise Exception(f"IPRegFields class not found in {module_path}")

    def build_peripheral_regs(self, model, profile, peripheral_name):
        reg_field_list = self.get_ip_regfield_list(model.part_family, peripheral_name)
        for reg_field in reg_field_list:
            reg_field_name = peripheral_name + "_" + reg_field.replace(".", "_")
            reg_model_var = getattr(model.vars, reg_field_name)
            profile.outputs.append(ModelOutput(reg_model_var, '', ModelOutputType.SVD_REG_FIELD,
                                               readable_name=reg_field_name.replace("_", ".")))
        pass

    def read_ip_ver_from_reg_map(self, peripheral_name:str):
        """
        Reads IP version from reg map
        Args:
            ip_name: 'agc'

        Returns:

        """
        regmap_ver = getattr(self.reg_map, peripheral_name).IPVERSION.io
        return regmap_ver

    def get_peri_regfields(self, ip_name):
        ip_obj = self.perip_dict.get(ip_name)
        regfields_module = importlib.import_module(ip_obj.get_regfields_module_path())
        return regfields_module

    def check_part_status_tag(self):
        if (self.part_status_tag is not DesignStatusTag.DEV) or (self.part_status_tag is not DesignStatusTag.PROD):
            raise SyntaxError("Chip tag is not valid. Please set a chip tag as DEV or PROD using \n"
                              "pyradioconfig.calculator_model_framework.interfaces.design_status_tag")


class IP_Peripheral_Base(object):
    peripheral_name = ''
    ip_name = ''
    category = ''
    ip_version = None
    prod_rev = None

    def __init__(self, peripheral_name:str, ip_name: str, category: str, ip_version: int, prod_rev: int, skip_for_target_sim: bool):
        self.peripheral_name = peripheral_name
        self.ip_name = ip_name.lower()
        self.category = category.lower()
        self.ip_version = f"{ip_version:02d}"
        self.prod_rev = f"{prod_rev:02d}" if isinstance(prod_rev, int) else None
        self.skip_for_target_sim = skip_for_target_sim

    def get_ip_module_path(self, part_family):
        """
        IP path is different for IP calculators tagged as dev and prod
        :return:
            calculator path
        """
        # read IP calculator tag
        try:
            ip_calc_tag = self.get_ip_calc_status_tag(self.category,self.ip_name,self.ip_version)
        except ModuleNotFoundError as error:
            message = (f"Please check if the IP version r_{self.ip_version} or a valid design status tag"
                       f" for {self.peripheral_name} exist.")
            raise ImportError(message) from error

        if ip_calc_tag == DesignStatusTag.DEV:
            # part is tagged as dev
            if self.prod_rev is not None:
                message_warning = (f"IP version r_{self.ip_version} of {self.ip_name} is tagged as dev.\n"
                                f"However, IP collector points to a certain prod revision.\n"
                                f"Set it as None to get rid of this warning.")
                LogMgr.Warning(message_warning)
            calc_path = f"pyradioconfig.modules.{self.category}.{self.ip_name}.r_{self.ip_version}.{part_family}".lower()
            # check and throw error if path does not exists
            try:
                mod = importlib.import_module(calc_path)
            except ModuleNotFoundError as error:
                message = (f"IP version r_{self.ip_version} of {self.ip_name} is tagged as dev. "
                           f"Please make sure a snapshot with folder name {part_family} exist.")
                raise ImportError(message) from error

            return calc_path
        elif ip_calc_tag == DesignStatusTag.PROD:
            # part is tagged as prod
            calc_path = f"pyradioconfig.modules.{self.category}.{self.ip_name}.r_{self.ip_version}.prod_{self.prod_rev}".lower()
            # check and throw error if path does not exists
            try:
                mod = importlib.import_module(calc_path)
            except ModuleNotFoundError as error:
                message = (f" IP version r_{self.ip_version} of {self.ip_name} is tagged as prod. "
                           f"Please make sure a snapshot with folder name prod_{self.prod_rev} exist.")
                raise ImportError(message) from error

            return calc_path
        else:
            raise SyntaxError("Invalid tag for the IP")
    def get_calc_module_path(self, part_family):
        module_path = self.get_ip_module_path(part_family)
        calc_path = module_path+".calculator"
        return calc_path

    def get_regfields_module_path(self, part_family):
        module_path = self.get_ip_module_path(part_family)
        regfields_path = module_path + ".reg_fields"
        return regfields_path

    def get_ip_calc_status_tag(self, category, ip_name, ip_version):
        tag = importlib.import_module(f"pyradioconfig.modules.{category}.{ip_name}.r_{ip_version}".lower()).ip_status_tag
        return tag