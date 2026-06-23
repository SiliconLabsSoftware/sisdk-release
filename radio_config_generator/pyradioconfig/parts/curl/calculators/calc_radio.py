from pycalcmodel.core.variable import ModelVariableFormat
from pyradioconfig.parts.lion.calculators.calc_radio import CalcRadioLion


class CalcRadioCurl(CalcRadioLion):

    def _build_radio_regs(self, model):
        self._addModelRegister(model, 'RAC.IFPGACTRL.BANDSEL', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFPGACTRL.VLDO', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFPGACTRL.CASCBIAS', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFPGACTRL.TRIMVCASLDO', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFPGACTRL.TRIMVCM', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFPGACTRL.TRIMVREFLDO', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFPGACTRL.TRIMVREGMIN', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFPGACTRL.ENHYST', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFPGACTRL.ENOFFD', int, ModelVariableFormat.HEX)

        self._addModelRegister(model, 'RAC.IFADCCTRL.REALMODE', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.VLDOCLKGEN', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.REGENCLKDELAY', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.INPUTSCALE', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.OTA1CURRENT', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.OTA2CURRENT', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.OTA3CURRENT', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.VCM', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.VLDOSERIES', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.VLDOSERIESCURR', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.VLDOSHUNT', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFADCCTRL.INVERTCLK', int, ModelVariableFormat.HEX)

        self._addModelRegister(model, 'RAC.IFFILTCTRL.BANDWIDTH', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFFILTCTRL.CENTFREQ', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFFILTCTRL.VCM', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.IFFILTCTRL.VREG', int, ModelVariableFormat.HEX)

        self._addModelRegister(model, 'RAC.RFENCTRL.DEMEN', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.RFENCTRL.IFADCCAPRESET', int, ModelVariableFormat.HEX)

        # Don't write this register directly any more.  Write the version in sequencer code instead.
        # self._addModelRegister(model, 'RAC.LPFCTRL.LPFBW'              , int, ModelVariableFormat.HEX )
        self._addModelRegister(model, 'SEQ.SYNTHLPFCTRLRX.SYNTHLPFCTRLRX', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'SEQ.SYNTHLPFCTRLTX.SYNTHLPFCTRLTX', int, ModelVariableFormat.HEX)

        # Misc fields that were being written by the firmware to non-default values
        self._addModelRegister(model, 'RAC.LNAMIXCTRL1.TRIMAUXPLLCLK', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.LNAMIXCTRL1.TRIMTRSWGATEV', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.LNAMIXCTRL1.TRIMVCASLDO', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.LNAMIXCTRL1.TRIMVREFLDO', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.LNAMIXCTRL1.TRIMVREGMIN', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.LNAMIXCTRL1.TRIMAUXBIAS', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.LNAMIXCTRL1.ENBIASCAL', int, ModelVariableFormat.HEX)

        self._addModelRegister(model, 'RAC.VCOCTRL.VCOAMPLITUDE', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.VCOCTRL.VCODETAMPLITUDE', int, ModelVariableFormat.HEX)

        self._addModelRegister(model, 'RAC.VCOCTRL.VCODETEN', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.VCOCTRL.VCODETMODE', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.VCOCTRL.VCOAREGCURR', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.VCOCTRL.VCOCREGCURR', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'RAC.VCOCTRL.VCODIVCURR', int, ModelVariableFormat.HEX)

        self._addModelRegister(model, 'SYNTH.CTRL.DITHERDSMOUTPUT', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'SYNTH.CTRL.DITHERDAC', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'SYNTH.CTRL.DITHERDSMINPUT', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'SYNTH.CTRL.DSMMODE', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'SYNTH.CTRL.LSBFORCE', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'SYNTH.CTRL.LOCKTHRESHOLD', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'SYNTH.CTRL.AUXLOCKTHRESHOLD', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'SYNTH.CTRL.PRSMUX0', int, ModelVariableFormat.HEX)
        self._addModelRegister(model, 'SYNTH.CTRL.PRSMUX1', int, ModelVariableFormat.HEX)
