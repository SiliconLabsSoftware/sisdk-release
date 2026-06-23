from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from pyradioconfig.parts.common.calculators.calc_diversity import CALC_Diversity


class CalcDiversityCurl(CALC_Diversity):

    def calc_diversity_values(self, model):
        # default value 0 ANTENNA0 Antenna 0 (ANT0=1, ANT1=0) is used. This is not exposed as one of the enums, so use 0 here.
        # default ANTDIVREPEATDIS 0
        model.vars.antdivmode.value = model.vars.antdivmode.var_enum.DISABLE
        model.vars.antdivrepeatdis.value = model.vars.antdivrepeatdis.var_enum.REPEATFIRST

        # unless set otherwise by advanced inputs
        antdivmode = model.vars.antdivmode.value
        antdivrepeatdis = model.vars.antdivrepeatdis.value

        flag_using_viterbi_demod = model.vars.MODEM_VITERBIDEMOD_VTDEMODEN.value == 1

        if not flag_using_viterbi_demod:
            # not using coherent demod, OK to enable diversity
            model.vars.div_antdivmode.value = int(antdivmode)
            model.vars.div_antdivrepeatdis.value = int(antdivrepeatdis)
        else:
            # Viterbi demod, may not enable diversity

            model.vars.div_antdivmode.value = int(model.vars.antdivmode.var_enum.DISABLE)
            model.vars.div_antdivrepeatdis.value = int(model.vars.antdivrepeatdis.var_enum.REPEATFIRST)

            if antdivmode != int(model.vars.antdivmode.var_enum.DISABLE) and flag_using_Viterbi_demod:
                raise CalculationException("Cannot enable antenna diversity when using Viterbi demodulation.")
