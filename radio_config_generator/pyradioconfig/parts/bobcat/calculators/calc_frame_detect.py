from pyradioconfig.parts.ocelot.calculators.calc_frame_detect import CALC_Frame_Detect_Ocelot
from pycalcmodel.core.variable import ModelVariableFormat
import math
from math import ceil


class Calc_Frame_Detect_Bobcat(CALC_Frame_Detect_Ocelot):
   def buildVariables(self, model):
      super().buildVariables(model)
      """Populates a list of needed variables for this calculator

      Args:
          model (ModelRoot) : Builds the variables specific to this calculator
      """

      self._addModelActual(model, 'preamble_string', str, ModelVariableFormat.ASCII,
                           desc='Output string representing the actual preamble pattern in binary')

   def calc_preamble_string_actual(self, model):
      if model.vars.MODEM_CTRL0_CODING.value == 2 or model.vars.MODEM_PRE_DSSSPRE.value == 1:
         # : Preamble base pattern is irrelevant if DSSS is enabled. Preamble bits are always substituted with
         # : Base chip sequence (i.e. base patttern = 0)
         preamble_pattern_string = '0'
         preamble_length = model.vars.MODEM_CTRL0_DSSSLEN.value + 1  # This is the TX preamble length
         repeats = int(preamble_length)
      elif model.vars.MODEM_LONGRANGE_LRBLE.value == 1 and model.vars.MODEM_CTRL0_CODING.value == 3:
         preamble_pattern_string = '00111100'
         repeats = model.vars.MODEM_PRE_TXBASES.value
      else:
         preamble_pattern_len = model.vars.MODEM_PRE_BASEBITS.value + 1
         preamble_pattern_value = self.flip_bits(model.vars.MODEM_PRE_BASE.value, preamble_pattern_len)
         preamble_pattern_string = ('{:0' + str(preamble_pattern_len) + 'b}').format(preamble_pattern_value)
         repeats = model.vars.MODEM_PRE_TXBASES.value

      preamble_string = preamble_pattern_string * repeats
      model.vars.preamble_string_actual.value = preamble_string

   def calc_timbases_val(self, model):
      # Run existing Ocelot logic
      super().calc_timbases_val(model)
      # JIRA MCUW_RADIO_CFG-3184: When ADPC (antenna-diversity parallel correlation) is enabled
      # on a LEGACY or COHERENT demodulator, set TIMINGBASE = ADPCWNDCNT.
      # This change cannot be applied on Ocelot, since ADPCEN is not available
      # Bobcat-only additions (locals that Ocelot doesn't have)
      demod_select = model.vars.demod_select.value
      basebits = model.vars.preamble_pattern_len_actual.value
      antdiv_parallel_corr_en = model.vars.antdiv_enable_parallel_correlation.value
      adpc_wndcnt = model.vars.MODEM_ADPC1_ADPCWNDCNT.value

      if (demod_select in (model.vars.demod_select.var_enum.LEGACY,model.vars.demod_select.var_enum.COHERENT) and antdiv_parallel_corr_en):
         model.vars.symbols_in_timing_window.value = int(adpc_wndcnt) * int(basebits)
