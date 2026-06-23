import importlib
import inspect
import os.path
import os
import glob
from pyradioconfig.calculator_model_framework.interfaces.ipcollector import IPCollector_Base
from pyradioconfig.calculator_model_framework.interfaces.icalculator import ICalculator
from pyradioconfig.calculator_model_framework.Utils.LogMgr import LogMgr

__all__ = ['ClassManager']


class ClassManager(object):
    """
    Common utitly class
    """
    @staticmethod
    def getClassListFromImportPath(import_path, class_type):
        class_list = []

        mod = importlib.import_module(import_path)
        for att_name in mod.__all__:
            fooModule = importlib.import_module(import_path + ".{}".format(att_name))
            classes = inspect.getmembers(fooModule, inspect.isclass)
            for (classname, classvalue) in classes:
                if issubclass(classvalue, class_type) and inspect.getmodule(classvalue) == fooModule:
                    # Make sure it is a class
                    # and
                    # Make sure it was defined in module, not just imported
                    class_list.append(classvalue)

        return class_list

    @staticmethod
    def verify_ip_based_part(import_path):
        try:
            mod = importlib.import_module(import_path)
            return True
        except ImportError as e:
            return False

    @staticmethod
    def get_calc_ips(import_path, part_family, part_rev, return_ip_obj=True):
        """
        Searches for IPCalcFactory class type in import_path.
        Instantiates the first one found and collect calculations
        return_perip_name is used to select the return type.
        If True, it returns a list of tuples(peripheral name, calc class), else returns a list of clac class.
        True is used when building model variables
        """

        calc_class_type = ICalculator
        peripheral_calcs_list = []

        mod = importlib.import_module(import_path)
        for att_name in mod.__all__:
            fooModule = importlib.import_module(import_path + ".{}".format(att_name))
            classes = inspect.getmembers(fooModule, inspect.isclass)
            for (classname, classvalue) in classes:
                if issubclass(classvalue, IPCollector_Base) and classname != 'IPCollector_Base':
                    ip_collector = classvalue(part_family, part_rev)
                    for ip_obj in ip_collector.perip_dict.values():
                        peripheral_name = ip_obj.peripheral_name
                        calc_path = ip_obj.get_calc_module_path(part_family)
                        calc_mod = importlib.import_module(calc_path)
                        calcclasses = inspect.getmembers(calc_mod, inspect.isclass)
                        for (calcclassname, calcclassvalue) in calcclasses:
                            if issubclass(calcclassvalue, calc_class_type) and inspect.getmodule(calcclassvalue) == calc_mod:
                                if return_ip_obj:
                                    peripheral_calcs_list.append((ip_obj, calcclassvalue))
                                else:
                                    peripheral_calcs_list.append(calcclassvalue)
        return peripheral_calcs_list

    @staticmethod
    def load_module_from_import_path(import_path):
        mod = importlib.import_module(import_path)
        return mod

    @staticmethod
    def merge_lists_classes(common_classes, part_specific_classes):
        # Loop through common calculators and remove and parent classes from part rev specific instance
        for common_class in common_classes[:]:
            common_calculator_name = str(common_class().__class__.__name__)
            for part_specific_class in part_specific_classes:
                if ClassManager.class_is_parent_whole_hierarchy(common_calculator_name, part_specific_class):
                    common_classes.remove(common_class)
                    break

        class_list = []
        class_list.extend(part_specific_classes)
        class_list.extend(common_classes)
        return class_list

    @staticmethod
    def class_is_parent_whole_hierarchy(class_name_to_search_for, class_object):
        try:
            parent_classes = class_object().__class__.__bases__
        except TypeError:
            parent_classes = class_object.__class__.__bases__

        for parent_class in parent_classes:
            parent_class_name = str(parent_class.__name__)
            if parent_class_name == class_name_to_search_for:
                return True

            return ClassManager.class_is_parent_whole_hierarchy(class_name_to_search_for, parent_class)
        return False

    @staticmethod
    def getModuleNamesFromPath(file_Path):
        modules = glob.glob(os.path.dirname(file_Path)+"/*.py")
        if len(modules) == 0:
            modules = glob.glob(os.path.dirname(file_Path)+"/*.pyc")
        if len(modules) == 0:
            modules = glob.glob(os.path.dirname(file_Path)+"/*$py.class")
        module_names = sorted([os.path.basename(f)[:-3] for f in modules])
        return module_names
