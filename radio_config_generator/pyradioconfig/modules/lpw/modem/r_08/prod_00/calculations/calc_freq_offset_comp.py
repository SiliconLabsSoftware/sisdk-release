from pyradioconfig.calculator_model_framework.interfaces.ipcalculator import IPCalculator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException
from py_2_and_3_compatibility import *

class CalcFreqOffsetComp(IPCalculator):

# Method name: afc_adj_limit
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def afc_adj_limit(self, model):
        freq_limit = model.vars.freq_offset_hz.value
        synth_res = model.vars.synth_res_actual.value
        afclimreset = model.vars.afc_lim_reset_actual.value
        digmix_res = model.vars.digmix_res_actual.value
        digmixfb = model.vars.MODEM_DIGMIXCTRL_DIGMIXFB.value
        if digmixfb:
            res = digmix_res
        else:
            res = synth_res
        # calculate limit
        afcadjlim = freq_limit / res
        # if AFC_LIM_RESET is enabled we reset to the center frequency
        # once the accumulated offset reaches the limit. In this mode we
        # like to set the limit to about 20% higher than where we like the
        # limit to be
        if afclimreset:
            afcadjlim *= 1.2
        return int(round(afcadjlim))

# Method name: calc_afc_adjlim_actual
# Defined in: lpwh74000\calculators\calc_freq_offset_comp.py
    def calc_afc_adjlim_actual(self, model):

        afcadjlim = model.vars.MODEM_AFCADJLIM_AFCADJLIM.value
        synth_res = model.vars.synth_res_actual.value
        digmix_res = model.vars.digmix_res_actual.value
        digmixfb = model.vars.FEFILT_DIGMIXCTRL_DIGMIXFB.value

        if digmixfb:
            res = digmix_res
        else:
            res = synth_res

        model.vars.afc_limit_hz_actual.value = afcadjlim * res

# Method name: calc_afc_period
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_afc_period(self, model):
        """
        calculate AFC period based on osr
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        mode = model.vars.frequency_comp_mode.value
        osr = model.vars.oversampling_rate_actual.value
        offsub = model.vars.offsub_ratio_actual.value
        mode_index = self.freq_comp_mode_index(model, mode)
        if mode_index >= 4:
            if offsub == 0:
                afcavgper = int(math.log(4.0 * osr, 2))
            else:
                afcavgper = int(math.log((round(4.0 * osr / offsub)), 2))
        else:
            afcavgper = 0
        model.vars.afc_period.value = afcavgper
# Method name: calc_afc_scale_actual
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_afc_scale_actual(self, model):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        e = float(model.vars.MODEM_AFCADJRX_AFCSCALEE.value)
        m = float(model.vars.MODEM_AFCADJRX_AFCSCALEM.value)
        if e > 7:
            e -= 16
        model.vars.afc_scale_actual.value = m * 2**e
# Method name: calc_afc_scale_reg
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_afc_scale_reg(self, model):
        """
        convert AFC scale value to mantissa and exponent register values
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        afc_scale = model.vars.afc_scale.value
        if afc_scale == 0:
            best_m = 0
            best_e = 0
        else:
            best_diff = 99e9
            best_e = 0
            best_m = 0
            # start with the highest allowed mantissa and find best m, e pair
            for m in xrange(1, 31, 1):
                e = math.floor(math.log(afc_scale / m, 2))
                diff = abs(afc_scale - m * 2**e)
                # solution is valid only if e is within the limits
                if (diff < best_diff) and e >= -8 and e <= 7:
                    best_diff = diff
                    best_e = e
                    best_m = m
            if best_e < 0:
                best_e += 16
            if best_m > 31:
                best_m = 31
        self._ip_reg_write(model, 'AFCADJRX_AFCSCALEE', int(best_e))
        self._ip_reg_write(model, 'AFCADJRX_AFCSCALEM', int(best_m))
# Method name: calc_afc_scale_tx_actual
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_afc_scale_tx_actual(self, model):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        e = float(model.vars.MODEM_AFCADJTX_AFCSCALEE.value)
        m = float(model.vars.MODEM_AFCADJTX_AFCSCALEM.value)
        if e > 7:
            e -= 16
        model.vars.afc_scale_tx_actual.value = m * 2**e

# Method name: calc_afc_scale_tx_reg
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_afc_scale_tx_reg(self, model):
        """
        convert AFC scale TX value to mantissa and exponent register values
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        afc_scale = model.vars.afc_scale_tx.value
        if afc_scale == 0:
            best_m = 0
            best_e = 0
        else:
            best_diff = 99e9
            # find best m, e pair that gives a scale less than or equal to the target scale
            for m in range(1,32):
                for e in range(-8,8):
                    diff = afc_scale - m * 2**e
                    if diff > 0 and diff <= best_diff:
                        best_diff = diff
                        best_e = e
                        best_m = m
            if best_e < 0:
                best_e += 16
        self._ip_reg_write(model, 'AFCADJTX_AFCSCALEE', int(best_e))
        self._ip_reg_write(model, 'AFCADJTX_AFCSCALEM', int(best_m))

# Method name: calc_afc_scale_value
# Defined in: lpwh74000\calculators\calc_freq_offset_comp.py
    def calc_afc_scale_value(self, model):
        # Overriding this function due to variable name change

        # Load model values into local variables
        freqgain = model.vars.freq_gain_actual.value
        mod_format = model.vars.modulation_type.value
        mode = model.vars.frequency_comp_mode.value
        scale = model.vars.afc_step_scale.value
        remoden = model.vars.MODEM_PHDMODCTRL_REMODEN.value
        remodoutsel = model.vars.MODEM_PHDMODCTRL_REMODOUTSEL.value
        digmix_res = model.vars.digmix_res_actual.value
        synth_res = model.vars.synth_res_actual.value
        phscale = 2 ** model.vars.MODEM_TRECPMDET_PHSCALE.value
        mode_index = self.freq_comp_mode_index(model, mode)
        demod_sel = model.vars.demod_select.value
        digmixfb = model.vars.FEFILT_DIGMIXCTRL_DIGMIXFB.value
        baudrate = model.vars.rx_baud_rate_actual.value
        osr = model.vars.oversampling_rate_actual.value
        vtafcframe = model.vars.MODEM_REALTIMCFE_VTAFCFRAME.value
        afc_tx_adjust_enable = model.vars.afc_tx_adjust_enable.value
        afc_oneshot = model.vars.MODEM_AFC_AFCONESHOT.value
        bcr_det_en = model.vars.MODEM_PHDMODCTRL_BCRDETECTOR.value

        if digmixfb:
            res = digmix_res
        else:
            res = synth_res

        # AFC to synth for Legacy
        if(demod_sel==model.vars.demod_select.var_enum.LEGACY):
            if mode_index >= 4 and freqgain > 0:
                if mod_format == model.vars.modulation_type.var_enum.FSK2 or \
                    mod_format == model.vars.modulation_type.var_enum.MSK or \
                    mod_format == model.vars.modulation_type.var_enum.FSK4:
                    afcscale = baudrate * osr / ( 256 * freqgain * res)
                    afcscale_tx = baudrate * osr / ( 256 * freqgain * synth_res)
                else:
                    afcscale = baudrate * osr / ( 256 * res)
                    afcscale_tx = baudrate * osr / ( 256 * synth_res)
            else:
                afcscale = 0.0
                afcscale_tx = 0.0

        elif((demod_sel==model.vars.demod_select.var_enum.TRECS_VITERBI or
              demod_sel==model.vars.demod_select.var_enum.TRECS_SLICER) and
             model.vars.MODEM_VITERBIDEMOD_VITERBIKSI1.value != 0) or \
                demod_sel==model.vars.demod_select.var_enum.LONGRANGE:
            if remoden and remodoutsel == 1:
                afcscale = baudrate * osr * phscale / (256 * freqgain * res)
                afcscale_tx = baudrate * osr * phscale / (256 * freqgain * synth_res)
            else:
                if vtafcframe == 0:
                    #Digmix only updated one time, so use 100% scale to ensure we are in the channel bw
                    afcscale = 1.0 * baudrate * phscale / (256 * res)
                else:
                    #Digmix updated constantly, so use smaller scale to reduce jitter
                    afcscale = 0.8 * baudrate * phscale / (256 * res) #Less correction jitter if we use gain < 1
                afcscale_tx = baudrate * phscale / (256 * synth_res)

                # Reduce afc scale by eighth if oneshot is disabled. Following BLE case
                if afc_oneshot == 0 and bcr_det_en == 1:
                    afcscale = afcscale / 8.0
        elif (demod_sel == model.vars.demod_select.var_enum.BCR):
            # digital mixer frequency comp
            afcscale =  model.vars.pro2_afc_gain.value /  res
            afcscale_tx = model.vars.pro2_afc_gain.value / synth_res
        elif (demod_sel == model.vars.demod_select.var_enum.ENHANCED_DSSS):
            # feedback 80% of estimated offset to digital mixer
            afcscale = baudrate / (256 * res) * 0.8
            afcscale_tx = baudrate / (256 * synth_res) * 0.8
        else:
            afcscale = 0.0
            afcscale_tx = 0.0

        afcscale = afcscale * scale

        #Special case to set afc_scale_tx to 0 to disable TX AFC adjust when using oneshot
        #See https://jira.silabs.com/browse/MCUW_RADIO_CFG-1510
        if (afc_tx_adjust_enable == False) and afc_oneshot:
            afcscale_tx = 0.0

        model.vars.afc_scale.value = afcscale
        model.vars.afc_scale_tx.value = afcscale_tx
# Method name: calc_afc_step_scale_val
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_afc_step_scale_val(self, model):
        """by default use scale of 1.0
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # by default use scale of 1.0
        model.vars.afc_step_scale.value = 1.0
# Method name: calc_afc_tx_adjust_enable
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_afc_tx_adjust_enable(self, model):
        #This method calculates when to enable TX freq adjustments based on RX AFC
        #For now, always disable
        afc_tx_adjust_enable = False
        #Write to the model var
        model.vars.afc_tx_adjust_enable.value = afc_tx_adjust_enable
# Method name: calc_afcadjlim
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_afcadjlim(self, model):
        """
        set AFCADJLIM register if AFC is enabled
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        mode = model.vars.frequency_comp_mode.value
        freq_limit = model.vars.freq_offset_hz.value
        mode_index = self.freq_comp_mode_index(model, mode)
        # check if freq_offset_hz advanced input is forced
        if model.vars.freq_offset_hz.value_forced is None:
            forced = 0
        else:
            forced = 1
        # we only care about this register when AFC is enabled
        # if not set register to 0
        if mode_index >= 4:
            if freq_limit == 0:
                if forced:
                    # if offset limit is intentionally set to zero by forcing
                    # freq_offset_hz that means we want not limit in AFC range
                    # and we should set register to 0
                    afcadjlim = 0
                else:
                    # if offset limit is zero but not because we forced
                    # freq_offset_hz but because ppm values were set to zero
                    # we assume the user wants AFC on with no effect so we set
                    # the limit to minimum value of 1 - not sure why one would do this
                    # but we have PHYs setup this way
                    afcadjlim = 1
            else:
                # if offset limit is non-zero calculate the correct value
                afcadjlim = self.afc_adj_limit(model)
        else:
            afcadjlim = 0
        # make sure we are within register limits
        if afcadjlim > 2**18 - 1:
            afcadjlim = 2**18 - 1
        self._ip_reg_write(model, 'AFCADJLIM_AFCADJLIM', afcadjlim)
# Method name: calc_afcavgper_reg
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_afcavgper_reg(self, model):
        """
        calculate AFC period based on osr
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        self._ip_reg_write(model, 'AFC_AFCAVGPER', model.vars.afc_period.value)
# Method name: calc_afcdel_reg
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_afcdel_reg(self, model):
        """
        calculate AFC Delay based on over sampling rate (osr) if AFC is enabled
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        mode = model.vars.frequency_comp_mode.value
        osr = model.vars.oversampling_rate_actual.value
        demod_select = model.vars.demod_select.value
        afconeshot = model.vars.MODEM_AFC_AFCONESHOT.value
        del_digmix_to_demod = model.vars.grpdelay_to_demod.value
        remoddwn = model.vars.MODEM_PHDMODCTRL_REMODDWN.value + 1
        if demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
            if afconeshot:
                # AFCDEL is in symbols when used for Viterbi Demod so divide by OSR
                # if REMODDWN is not 1 that will also need to be taken into account
                afcdel = math.ceil(del_digmix_to_demod / osr * remoddwn)
            else:
                afcdel = 0
        else:
            mode_index = self.freq_comp_mode_index(model, mode)
            # AFC mode
            if mode_index >= 4:
                afcdel = model.vars.grpdelay_to_demod.value
            else:
                afcdel = 0
        if afcdel > 31:
            afcdel = 31
        self._ip_reg_write(model, 'AFC_AFCDEL', int(afcdel))
# Method name: calc_afclimreset_actual
# Defined in: jumbo\calculators\calc_freq_offset_comp.py
    def calc_afclimreset_actual(self, model):
        model.vars.afc_lim_reset_actual.value = model.vars.MODEM_AFC_AFCLIMRESET.value
# Method name: calc_afconeshoft_reg
# Defined in: rainier\calculators\calc_freq_offset_comp.py
    def calc_afconeshoft_reg(self, model):
        modtype = model.vars.modulation_type.value
        run_mode = model.vars.afc_run_mode.value
        comp_mode = model.vars.frequency_comp_mode.value
        demod_select = model.vars.demod_select.value
        comp_mode_index = self.freq_comp_mode_index(model, comp_mode)
        if (run_mode == model.vars.afc_run_mode.var_enum.ONE_SHOT) and (modtype != model.vars.modulation_type.var_enum.OOK and modtype != model.vars.modulation_type.var_enum.ASK):
            oneshot = 1
        else:
            oneshot = 0
        if ((comp_mode_index > 3) or
                (demod_select == model.vars.demod_select.var_enum.BCR) or
                (demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI)):
            limreset = 1
        else:
            limreset = 0
        self._ip_reg_write(model, 'AFC_AFCONESHOT', oneshot)
        self._ip_reg_write(model, 'AFC_AFCDELDET', 0)
        self._ip_reg_write(model, 'AFC_AFCDSAFREQOFFEST', 0)
        self._ip_reg_write(model, 'AFC_AFCENINTCOMP', 0)
        self._ip_reg_write(model, 'AFC_AFCLIMRESET', limreset)
        self._ip_reg_write(model, 'AFC_AFCGEAR', 3)
# Method name: calc_afcrxmode_reg
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_afcrxmode_reg(self, model):
        """
        set the AFC RX mode based on input
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        mode = model.vars.frequency_comp_mode.value
        mode_index = self.freq_comp_mode_index(model, mode)
        if model.vars.ber_force_freq_comp_off.value==True:
            rxmode = 0
        elif mode_index <= 3:
            rxmode = 0
        else:
            rxmode = mode_index - 3
        self._ip_reg_write(model, 'AFC_AFCRXMODE', rxmode)
# Method name: calc_afctxmode_reg
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_afctxmode_reg(self, model):
        #This method calculates the AFC_AFCTXMODE field
        #Read in model vars
        afc_tx_adjust_enable = model.vars.afc_tx_adjust_enable.value
        #Calculate the register
        if afc_tx_adjust_enable:
            afctxmode = 1
        else:
            afctxmode = 0
        #Write register
        self._ip_reg_write(model, 'AFC_AFCTXMODE', afctxmode)
# Method name: calc_afcxclr_reg
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_afcxclr_reg(self, model):
        """
        clear AFC register at the beginning of each frame if enabled
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        mode = model.vars.frequency_comp_mode.value
        mode_index = self.freq_comp_mode_index(model, mode)
        if mode_index >= 4:
            afcrxclr = 1
        else:
            afcrxclr = 0
        self._ip_reg_write(model, 'AFC_AFCRXCLR', afcrxclr)
# Method name: calc_compmode_reg
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_compmode_reg(self, model):
        """
        determine best internal frequency compensation mode and set COMPMODE register
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        mode = model.vars.frequency_comp_mode.value
        mode_index = self.freq_comp_mode_index(model, mode)
        # Turn off frequency compensation when running BER tests
        if model.vars.ber_force_freq_comp_off.value==True:
            self._ip_reg_write(model, 'CTRL1_COMPMODE', 0)
        elif mode_index == 1:
            # enable internal compensation at preamble
            self._ip_reg_write(model, 'CTRL1_COMPMODE', 1)
        elif mode_index == 2:
            # enable internal compensation at frame detect
            self._ip_reg_write(model, 'CTRL1_COMPMODE', 2)
        elif mode_index == 3:
            # enable continues compensation
            self._ip_reg_write(model, 'CTRL1_COMPMODE', 3)
        elif mode_index == 0 or mode_index >= 4:
            # disable internal compensation
            self._ip_reg_write(model, 'CTRL1_COMPMODE', 0)
        else:
            raise CalculationException("ERROR: frequency_comp_mode not recognized!")
# Method name: calc_fdm0thresh_reg
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_fdm0thresh_reg(self, model):
        """
        set FMD0 register given calculated value
        Equation from definition of FDM0THRESH in registers list of EFR32 Reference Manual (internal.pdf)
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        fdm0_thresh = model.vars.fdm0_thresh.value
        # The threshold can be up to 71 max, and still have the register not overflow a 3 bit field
        if fdm0_thresh == 0:
            reg = 0
        else:
            reg = int(fdm0_thresh / 8.0) - 1
            # Using the equation above, the threshold can be up to 71 max
            # and still have the register not overflow a 3 bit field.  A value of 72
            # will cause an overflow
            # I'm limiting fdm0_thresh and not the register because I'm trying to figure out
            # how to push the limiting upstream to inherently prevent the overflow, in case
            # this overflow is not the correct way to limit things.
        # The register is limited to a value of 7 (3 bits)
        self._ip_reg_write(model, 'TIMING_FDM0THRESH', reg)
# Method name: calc_fdm0thresh_val
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_fdm0thresh_val(self, model):
        """
        in FDM0 mode set FDM0THRESH register
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        timingbases = model.vars.timingbases_actual.value
        #scale = model.vars.freq_gain_scale.value
        # only used in FDM0 mode which is active if timingbases = 0
        if timingbases > 0:
            model.vars.fdm0_thresh.value = 0
            return
        # nominal frequency deviation is +/- 64 we like to set this threshold
        # to half of that so 32 but if the FREQGAIN setting is scaled to avoid
        # saturation we need to scale this value accordingly
        fdm0_thresh = 32 #* scale
        if fdm0_thresh < 8:
            fdm0_thresh = 8
        elif fdm0_thresh > 71:      # Limiting so the register won't overflow
            fdm0_thresh = 71        # See calc_fdm0thresh_reg for details
        model.vars.fdm0_thresh.value = int(fdm0_thresh)
# Method name: calc_freq_comp_mode
# Defined in: rainier\calculators\calc_freq_offset_comp.py
    def calc_freq_comp_mode(self, model):
        preamble_detection_length = model.vars.preamble_detection_length.value
        demod_select = model.vars.demod_select.value
        preamsch = model.vars.MODEM_TRECPMDET_PREAMSCH.value
        modtype = model.vars.modulation_type.value
        tol = model.vars.baudrate_tol_ppm.value
        freq_offset_hz = model.vars.freq_offset_hz.value
        baudrate = model.vars.baudrate.value
        rtschmode = model.vars.MODEM_REALTIMCFE_RTSCHMODE.value
        antdivmode = model.vars.antdivmode.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)
        demod_sel = model.vars.demod_select.value
        if demod_sel == model.vars.demod_select.var_enum.ENHANCED_DSSS:
            model.vars.afc_run_mode.value = model.vars.afc_run_mode.var_enum.INTERNAL
        else:
            # default modes
            freq_mode = model.vars.frequency_comp_mode.var_enum.INTERNAL_ALWAYS_ON
            afc_mode = model.vars.afc_run_mode.var_enum.INTERNAL

            if modtype == model.vars.modulation_type.var_enum.OOK or modtype == model.vars.modulation_type.var_enum.ASK:
                afc_mode = model.vars.afc_run_mode.var_enum.INTERNAL
            # enable 1-shot for Viterbi demod only if preamble search mode is enabled
            elif demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
                # Owner: Rossano Pantaleoni
                # Jira Link: https://jira.silabs.com/browse/MCUW_RADIO_CFG-2231
                # AFC for TRECS according to https://confluence.silabs.com/download/attachments/232054930/TRECS_Demodulator_Instruction.pdf?version=1&modificationDate=1660157520047&api=v2
                # Register are not updated in this function, but in calc_afconeshoft_reg() and calc_realtimcfe_vtafcframe_reg() functions
                # afc_run_mode     | AFCONESHOT | VTAFCFRAME
                # _________________|____________|____________
                # INTERNAL_ONLY    |      0     |      0
                # CONTINUOUS       |      0     |      1
                # ONE_SHOT         |      1     |      0
                # ONESHOT_FRAME    |      1     |      1
                if preamsch and not fast_detect_enable and ((rtschmode == 0) or (freq_offset_hz / baudrate <= 2)):
                    if antdivmode == model.vars.antdivmode.var_enum.DISABLE or rtschmode == 0:
                        # If we turn off the CFE for the syncword, frequency comp is harder
                        # Only use oneshot if the CFE is enabled or the offset is not too large compared to the baudrate
                        afc_mode = model.vars.afc_run_mode.var_enum.ONE_SHOT
            # enable 1-shot for BCR only if preamble length is larger than 15 and modulation is not OOK and baudrate offset is less than 1%
            elif demod_select == model.vars.demod_select.var_enum.BCR:
                if preamble_detection_length >= 16 and tol < 50000:
                    afc_mode = model.vars.afc_run_mode.var_enum.ONE_SHOT
            # Disable frequency compensation for coherent demod
            elif demod_select == model.vars.demod_select.var_enum.COHERENT:
                freq_mode = model.vars.frequency_comp_mode.var_enum.DISABLED

            model.vars.frequency_comp_mode.value = freq_mode
            model.vars.afc_run_mode.value = afc_mode
# Method name: calc_freq_offset
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_freq_offset(self, model):
        #Overriding this function due to variable name change
        #Load model values into local variables
        rx_ppm = model.vars.rx_xtal_error_ppm.value
        tx_ppm = model.vars.tx_xtal_error_ppm.value
        rf_freq_hz = model.vars.base_frequency_hz.value * 1.0
        freq_offset = (rx_ppm + tx_ppm) * rf_freq_hz / 1e6
        #Load local variables back into model variables
        model.vars.freq_offset_hz.value = int(round(freq_offset,0))
# Method name: calc_freq_offset_scale_value
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_freq_offset_scale_value(self, model):
        #Overriding function due to variable name change
        # From the MODEM_FREQOFFEST documentation:
        # When AFC is enabled, this field is the residual frequency offset after
        # AFC correction. Frequency offset between transmitter and receiver is
        # given by AFCADJRX. Encoding of this signed value depends on modulation
        # format and if coherent detection is enabled.
        # For 2/4-FSK, and MSK the offset in Hz equals:
        # FREQOFFEST * fHFXO / (FREQGAIN * (Decimation Factor 0) * (Decimation Factor 1) *
        # (Decimation Factor 2) * 256).
        # For OQPSK and (D)BPSK, the offset in Hz equals:
        # FREQOFFEST * fHFXO / (2 * RXBRFRAC * (Decimation Factor 0) * (Decimation Factor 1) *
        # (Decimation Factor 2) * 256).
        # When coherent detection is enabled, the offset in Hz equals:
        # FREQOFFEST * chiprate / 2^13.
        # Frequency offset estimate is not available for OOK/ASK.
        #Load model values into local variables
        modem_frequency_hz = model.vars.modem_frequency_hz.value
        dec0 = model.vars.dec0_actual.value
        dec1 = model.vars.dec1_actual.value
        dec2 = model.vars.dec2_actual.value
        freq_gain = model.vars.freq_gain_actual.value
        osr = model.vars.oversampling_rate_actual.value # This is (2*RXBRFRAC)
        mod_format = model.vars.modulation_type.value
        chip_rate = model.vars.baudrate.value # In the calculator chiprate = baudrate
        try:
            # Check for coherent detection first
            if model.vars.MODEM_CTRL1_PHASEDEMOD.value == 3: # (COH)
                freq_offset_scale = (chip_rate//(2**13))*1.0 # force a float #
            else:
                if mod_format == model.vars.modulation_type.var_enum.FSK2 or \
                    mod_format == model.vars.modulation_type.var_enum.MSK or \
                    mod_format == model.vars.modulation_type.var_enum.FSK4:
                    freq_offset_scale = modem_frequency_hz / (freq_gain * dec0 * dec1 * dec2 * 256.0)
                elif mod_format == model.vars.modulation_type.var_enum.OQPSK or \
                    mod_format == model.vars.modulation_type.var_enum.BPSK or \
                    mod_format == model.vars.modulation_type.var_enum.DBPSK:
                    freq_offset_scale = modem_frequency_hz / (osr * dec0 * dec1 * dec2 * 256.0)
                else:
                    freq_offset_scale = 0.0
        except ZeroDivisionError:
            # In case the divisor ends up being 0 (freq_gain or osr or dec0/1/2)
            freq_offset_scale = 0.0
        #Load local variables back into model variables
        model.vars.freq_offset_scale.value = freq_offset_scale
# Method name: calc_freqoffestlim_reg
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_freqoffestlim_reg(self, model):
        """
        calculate internal frequency offset limit
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        modulation = model.vars.modulation_type.value
        deviation = model.vars.deviation.value
        freq_limit = model.vars.freq_offset_hz.value
        mode = model.vars.frequency_comp_mode.value
        slicer_level = model.vars.ook_slicer_level.value
        mode_index = self.freq_comp_mode_index(model, mode)
        # check if freq_offset_hz advanced input is forced
        if model.vars.freq_offset_hz.value_forced is None:
            forced = 0
        else:
            forced = 1
        # for OOK and ASK FREQOFFESTLIM is used as the slicer level
        # nothing to do with frequency offset compensation
        if modulation == model.vars.modulation_type.var_enum.OOK or \
           modulation == model.vars.modulation_type.var_enum.ASK:
            reg = slicer_level
        # only enable limit with internal compensation if user explicitly
        # set the freq_offset_hz advanced limit and deviation is non-zero
        elif forced and deviation > 0 and mode_index < 4:
            reg = int(round(freq_limit * 64.0 / deviation))
        else:
            reg = 0
        # if limit is larger than we can program in the register disable
        # the limit by setting the register to 0
        if reg > 127:
            reg = 0
        self._ip_reg_write(model, 'CTRL1_FREQOFFESTLIM', reg)
# Method name: calc_freqoffestper_reg
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_freqoffestper_reg(self, model):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        freqoffestper = model.vars.frequency_offset_period.value
        self._ip_reg_write(model, 'CTRL1_FREQOFFESTPER', freqoffestper)
# Method name: calc_freqoffestper_val
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_freqoffestper_val(self, model):
        #This function calculates the frequency offset estimate period
        #Load model values into local variables
        mod_type = model.vars.modulation_type.value
        if (mod_type == model.vars.modulation_type.var_enum.BPSK):
            freqoffestper = 2
        elif (mod_type == model.vars.modulation_type.var_enum.OQPSK):
            freqoffestper = 1
        elif (mod_type == model.vars.modulation_type.var_enum.FSK2) or \
                (mod_type == model.vars.modulation_type.var_enum.FSK4) or \
                (mod_type == model.vars.modulation_type.var_enum.MSK):
            freqoffestper = 2
        else:
            freqoffestper = 0
        #Load local variables back into model variables
        model.vars.frequency_offset_period.value = freqoffestper
# Method name: calc_frequency_offset_factor_value
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_frequency_offset_factor_value(self, model):
        """
        calculate Frequency Offset factor used by the RAIL Adapter
        RAIL_LIB-878
        MCUW_RADIO_CFG-606
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        # Frequency Offset Scale is somewhat complicated to calculate, but
        # I was able to determine that the largest and smallest numbers should
        # come from:
        #   freq_offset_scale = fxo / (freq_gain * dec0 * dec1 * dec2 * 256.0)
        # where:
        #   fxo is fixed at 38400000
        #   freq_gain = 0.21875 = m * 2**(2-e), m = 7, e = 7
        #   dec0 = dec1 = dec2 = 1
        # So, freq_offset_scale max theoretical value is 685714.2857142857
        # Looking at all the current PHY cfg file in the Calculator, I found
        # that the highest number freq_offset_scale can be is 16666.6666667,
        # (PHY_Bluetooth_LE_2M_Viterbi.cfg and others), so, I'm going to round
        # this up (arbitrarily) to 25000.
        freqOffsetScale = model.vars.freq_offset_scale.value
        # Synth Resolution is calculated as:
        # synth_res = fxo / lodiv / pow(2, 19)
        # We know:
        #   fxo is fixed at 38400000
        #   lodiv in theory, can only have only certain values, restricted by
        #   the three subdividers A, B and C in LODIVFREQCTRL, but technically
        #   it can range between 0 (error) and 175 (divA=5, divB=5, divC=7);
        #   see calc_lodiv_value for more details.
        # Therefore, synthResolution can vary from:
        #   0.4185267 (lodiv = 1) to 73.2421875 (lodiv = 175)
        synthResolution = model.vars.synth_res_actual.value
        # In firmware, we need both the freqOffsetScale and the synthResolution
        # to convert the value in FREQOFFEST to synthesizer resolution units
        # (synthTicks). freqOffsetScale only scales the value in FREQOFFEST to
        # actual Hz. synthResolution has units (Hz/synthTicks), so in order to
        # get pure synthTicks, and get rid of the Hz, we need to multiply by the
        # reciprocal of the synthResolution (synthTicks/Hz).
        freqOffsetFactor = freqOffsetScale * (1.0/synthResolution)
        # Assuming the worst case scenario (max possible value for freqOffsetScale,
        # and min possible value for synthResolution; and vice versa):
        #   25000*(1/0.4185267) = 59733.345566722506
        #   0.0018166333859430362*(1/73.2421875) = 0.000024803101162742255
        # It makes sense to scale the freqOffsetFactor to increase the precision
        # of the result in the FW once we multiply by FREQOFFEST, which is 8 bits
        # on Dumbo and 13 bits on Jumbo and above.
        # IMPORTANT: Since we are using FXP<16.16>, we need to make sure the
        # integer part fits in 16 bits, otherwise we can't recover it.
        assert int(freqOffsetFactor) <= 2**16, \
            "Resulting freqOffsetFactor ({}) value does not fit in 16 bits".format(freqOffsetFactor)
        # Convert the floating point value to FXP<16.16>
        # NOTE: Bitwise AND (&) yields a long int
        freqOffsetFactor_fxp = (long(freqOffsetFactor*(2**16)) & 0XFFFFFFFF)
        # Finally, set model output variables
        model.vars.frequency_offset_factor.value = freqOffsetFactor
        model.vars.frequency_offset_factor_fxp.value = freqOffsetFactor_fxp
# Method name: calc_intafc_preaverage
# Defined in: ocelot\calculators\calc_freq_offset_comp.py
    def calc_intafc_preaverage(self, model):
        dsss_sf = model.vars.dsss_spreading_factor.value
        demod_select = model.vars.demod_select.value
        if demod_select == model.vars.demod_select.var_enum.COHERENT:
            # : Frequency offset estimate pre averaging
            FOEPREAVG_mode = 7 # : enable dynamic pre averaging
            # : increase number of averaging linearly starting from 1
            stage_0_avg = 1
            stage_1_avg = int(math.log2(dsss_sf))
            stage_2_avg = stage_1_avg + 2
            stage_3_avg = stage_2_avg # : TODO silicon bug prevents continuous increase
            # : Controls POE period in number of DSSS symbols
            model.vars.MODEM_CTRL5_POEPER.value_forced = 1
            self._ip_reg_write(model, 'CTRL5_FOEPREAVG', FOEPREAVG_mode)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG0', stage_0_avg)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG1', stage_1_avg)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG2', stage_2_avg)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG3', stage_3_avg)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG4', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG5', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG6', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG7', 0)
        else:
            self._ip_reg_write(model, 'CTRL5_FOEPREAVG', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG0', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG1', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG2', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG3', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG4', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG5', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG6', 0)
            self._ip_reg_write(model, 'INTAFC_FOEPREAVG7', 0)
# Method name: calc_offsub_actual
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_offsub_actual(self, model):
        """
        calculate actual ratio
        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        den = model.vars.MODEM_TIMING_OFFSUBDEN.value
        num = model.vars.MODEM_TIMING_OFFSUBNUM.value * 1.0
        if den != 0:
            model.vars.offsub_ratio_actual.value = num / den
        else:
            model.vars.offsub_ratio_actual.value = 0.0
# Method name: calc_offsub_reg
# Defined in: bobcat\calculators\calc_freq_offset_comp.py
    def calc_offsub_reg(self, model):
        #calculate OFFSUBDEN and OFFSUBNUM register for more accurate frequency offset estimation
        #described in Section 5.7.7.1 of EFR32 Reference Manual (internal.pdf)
        # TODO: implement case when AFC is enabled
        rxbrfrac = 2*model.vars.rxbrfrac_actual.value
        timing_window = model.vars.timing_window_actual.value
        demod_sel = model.vars.demod_select.value
        # : Variables used in case of antenna diversity enabled
        enable_parallel_correlation = model.vars.antdiv_enable_parallel_correlation.value
        oversampling_rate_actual = model.vars.oversampling_rate_actual.value
        # : Calculate based on parallel window size if antenna diversity parallel correlator is enabled
        if enable_parallel_correlation and demod_sel != model.vars.demod_select.var_enum.COHERENT:
            adpcwndsizechip = model.vars.antdiv_adpcwndsize.value
            exp = adpcwndsizechip * oversampling_rate_actual / 128.0
            diff_min = 9999.0
            num = 1
            num_max = 15
            best_num = 1
            best_den = 1
            while num <= num_max:
                den = 1
                while den < num:
                    res = 1.0 * num / den
                    if res <= exp:
                        diff = exp - res
                        if diff < diff_min:
                            diff_min = diff
                            best_num = num
                            best_den = den
                    den += 1
                num += 1
        elif(demod_sel==model.vars.demod_select.var_enum.LEGACY):
            timing_samples = timing_window * rxbrfrac
            closest_power_of_two = 2.0 ** (math.floor(math.log(timing_samples, 2)))
            if timing_samples == closest_power_of_two:
                best_den = 0
                best_num = 0
            else:
                error_min = 1e9
                # find best den, num pair that gets us closest to 2**N
                for den in xrange(1, 16):
                    for num in xrange(1, 16):
                        error = abs(closest_power_of_two * num / den - timing_samples)
                        if error < error_min:
                            error_min = error
                            best_den = den
                            best_num = num
        else:
            best_den = 0
            best_num = 0
        self._ip_reg_write(model, 'TIMING_OFFSUBDEN', best_den)
        self._ip_reg_write(model, 'TIMING_OFFSUBNUM', best_num)
# Method name: calc_ook_slicer
# Defined in: common\calculators\calc_freq_offset_comp.py
    def calc_ook_slicer(self, model):
        # empirically determined to work well used as default value
        model.vars.ook_slicer_level.value = 3
# Method name: freq_comp_mode_index
# Defined in: common\calculators\calc_freq_offset_comp.py
    def freq_comp_mode_index(self, model, mode):
        """
        Args:
            model (ModelRoot) : Data model to read and write variables from
            mode (Enum FREQ_COMP_MODE) : FREQ_COMP_MODE
        """
        FREQ_COMP_MODE_LOOKUP = {
            model.vars.frequency_comp_mode.var_enum.DISABLED.value                                  : 0,
            model.vars.frequency_comp_mode.var_enum.INTERNAL_LOCK_AT_PREAMBLE_DETECT.value          : 1,
            model.vars.frequency_comp_mode.var_enum.INTERNAL_LOCK_AT_FRAME_DETECT.value             : 2,
            model.vars.frequency_comp_mode.var_enum.INTERNAL_ALWAYS_ON.value                        : 3,
            model.vars.frequency_comp_mode.var_enum.AFC_FREE_RUNNING.value                          : 4,
            model.vars.frequency_comp_mode.var_enum.AFC_START_AT_PREAMBLE_FREE_RUNNING.value        : 5,
            model.vars.frequency_comp_mode.var_enum.AFC_LOCK_AT_TIMING_DETECT.value                 : 6,
            model.vars.frequency_comp_mode.var_enum.AFC_LOCK_AT_PREAMBLE_DETECT.value               : 7,
            model.vars.frequency_comp_mode.var_enum.AFC_LOCK_AT_FRAME_DETECT.value                  : 8,
            model.vars.frequency_comp_mode.var_enum.AFC_START_AT_PREAMBLE_LOCK_AT_FRAME_DETECT.value: 9,
        }
        return FREQ_COMP_MODE_LOOKUP[mode.value]