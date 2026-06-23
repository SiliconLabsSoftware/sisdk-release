from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from py_2_and_3_compatibility import *

class CalcMbus(IPCalculator):

    # Method name: calc_mbus_syncwords
    # Defined in: ocelot\calculators\calc_mbus.py
    def calc_mbus_syncwords(self, model):
        if model.profile.name.lower() == 'mbus':
            mode = model.vars.mbus_mode.value
            if mode in [model.vars.mbus_mode.var_enum.ModeTC_M2O_100k,
                        model.vars.mbus_mode.var_enum.ModeN_6p4k]:
                if mode == model.vars.mbus_mode.var_enum.ModeTC_M2O_100k:
                    len = 10
                    sync_a = long(0x3d)
                    sync_b = long(0)
                elif mode == model.vars.mbus_mode.var_enum.ModeN_6p4k:
                    # New logic for ModeN 6.4kbps
                    len = 16
                    sync_a = long(0xf68d)
                    sync_b = long(0xf672)
                # Set syncword 0/1 based on whether frame format A or B is selected
                # If only one syncword exists, don't flip them for frame B format
                if model.vars.mbus_frame_format.value != model.vars.mbus_frame_format.var_enum.FrameB or sync_b == 0:
                    syncword_0 = sync_a
                    syncword_1 = sync_b
                else:
                    syncword_0 = sync_b
                    syncword_1 = sync_a
                model.vars.syncword_0.value = syncword_0
                model.vars.syncword_1.value = syncword_1
                model.vars.syncword_length.value = len
            else:
                # Call existing logic for other Mbus modes
                if mode == model.vars.mbus_mode.var_enum.ModeC_M2O_100k or \
                        mode == model.vars.mbus_mode.var_enum.ModeC_O2M_50k:
                    len = 26
                    sync_a = long(0x03d54cd)
                    sync_b = long(0x03d543d)
                elif mode == model.vars.mbus_mode.var_enum.ModeF_2p4k:
                    len = 16
                    sync_a = long(0xf68d)
                    sync_b = long(0xf672)
                elif mode == model.vars.mbus_mode.var_enum.ModeNg or \
                        mode == model.vars.mbus_mode.var_enum.ModeN1a_4p8K or \
                        mode == model.vars.mbus_mode.var_enum.ModeN1c_2p4K:
                    len = 16
                    sync_a = long(0xf68d)
                    sync_b = long(0xf672)
                    # Note that the spec calls for a different 32-bit syncword for Ng mode,
                    # but it's really just the same 2gfsk pattern as the other modes
                    # expressed in 4gfsk notation.
                elif mode == model.vars.mbus_mode.var_enum.ModeR_4p8k:
                    len = 18
                    sync_a = long(0x7696)
                    sync_b = long(0)
                elif mode == model.vars.mbus_mode.var_enum.ModeT_M2O_100k:
                    len = 10
                    sync_a = long(0x3d)
                    sync_b = long(0)
                elif mode == model.vars.mbus_mode.var_enum.ModeT_O2M_32p768k:
                    len = 18
                    sync_a = long(0x7696)
                    sync_b = long(0)
                elif mode == model.vars.mbus_mode.var_enum.ModeS_32p768k:
                    len = 18
                    sync_a = long(0x7696)
                    sync_b = long(0)
                else:
                    raise CalculationException("Can't calculate syncwords.  Unexpected Mbus mode selected!")

                # Set syncword 0/1 based on whether frame format A or B is selected
                # If only one syncword exists, don't flip them for frame B format
                if model.vars.mbus_frame_format.value != model.vars.mbus_frame_format.var_enum.FrameB or sync_b == 0:
                    syncword_0 = sync_a
                    syncword_1 = sync_b
                else:
                    syncword_0 = sync_b
                    syncword_1 = sync_a

                model.vars.syncword_0.value = syncword_0
                model.vars.syncword_1.value = syncword_1
                model.vars.syncword_length.value = len