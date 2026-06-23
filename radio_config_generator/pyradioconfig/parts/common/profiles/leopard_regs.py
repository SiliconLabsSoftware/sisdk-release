from pyradioconfig.parts.common.profiles.lynx_regs import build_modem_regs_lynx
from pycalcmodel.core.output import ModelOutput, ModelOutputType

def build_modem_regs_leopard(model,profile):
    build_modem_regs_lynx(model, profile)

    # Add CLKMULT variables from bobcat
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVADC, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENDRVADC'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTDISICO, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTDISICO'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENBBDET, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENBBDET'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENBBXLDET, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENBBXLDET'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENBBXMDET, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENBBXMDET'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENCFDET, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMUTENCFDET'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENDITHER, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENDITHER'))

    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTBWCAL, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTBWCAL'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTFREQCAL, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTFREQCAL'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN1_CLKMULTLDFNIB, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN1.CLKMULTLDFNIB'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN1_CLKMULTLDMNIB, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN1.CLKMULTLDMNIB'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN1_CLKMULTRDNIBBLE, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN1.CLKMULTRDNIBBLE'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN1_CLKMULTLDCNIB, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN1.CLKMULTLDCNIB'))

    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVRX2P4G, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENDRVRX2P4G'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVRXSUBG, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENDRVRXSUBG'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENDRVTXDUALB, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENDRVTXDUALB'))

    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTREG2ADJI, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTREG2ADJI'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTREG1ADJV, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTREG1ADJV'))
    # Commenting this out as this is a protected register field according to Package/pyradioconfig/protected_fields/leopard_protected_fields.py
    # profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTREG2ADJV, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTREG2ADJV'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVN, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTCTRL.CLKMULTDIVN'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVR, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTCTRL.CLKMULTDIVR'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTCTRL_CLKMULTDIVX, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTCTRL.CLKMULTDIVX'))

    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENFBDIV, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENFBDIV'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENREFDIV, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENREFDIV'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENREG1, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENREG1'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENREG2, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENREG2'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN0_CLKMULTENROTDET, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN0.CLKMULTENROTDET'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTEN1_CLKMULTINNIBBLE, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTEN1.CLKMULTINNIBBLE'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTCTRL_CLKMULTENRESYNC, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTCTRL.CLKMULTENRESYNC'))
    profile.outputs.append(ModelOutput(model.vars.RAC_CLKMULTCTRL_CLKMULTVALID, '', ModelOutputType.SVD_REG_FIELD, readable_name='RAC.CLKMULTCTRL.CLKMULTVALID'))

    profile.outputs.append(ModelOutput(model.vars.RAC_IFADCTRIM0_IFADCCLKSEL, '', ModelOutputType.SVD_REG_FIELD,
                                       readable_name='RAC.IFADCTRIM0.IFADCCLKSEL'))