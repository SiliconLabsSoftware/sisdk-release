#from pyradioconfig.parts.bobcat.phys.Phys_Studio_Base import PHYS_Studio_Base_Bobcat
from pyradioconfig.calculator_model_framework.decorators.phy_decorators import do_not_inherit_phys
from pyradioconfig.calculator_model_framework.interfaces.iphy import IPhy
from pyradioconfig.parts.ocelot.phys.Phys_Studio_Base import PHYS_Studio_Base_Ocelot, PHY_COMMON_FRAME_INTERNAL

@do_not_inherit_phys
class Phy_Studio_Base_Curl(IPhy): #PHYS_Studio_Base_Bobcat):

    """
        https://jira.silabs.com/browse/MCUW_RADIO_CFG-3358
        Define the Datasheet PHYs for curl based on bobcat.
        Those PHY are based on Studio Profile Base profile.
    """    
    ##########2FSK PHYS##########
    def _part_specific_phy_overrides(self, phy, model):
        pass


    def _set_xtal_frequency(self, phy, xtal_freq=None):
        if xtal_freq is None:
            phy.profile_inputs.xtal_frequency_hz.value = 40000000
        else:
            phy.profile_inputs.xtal_frequency_hz.value = xtal_freq


    def Studio_2GFSK_base(self, phy, model):
        # Inherit the base configuratons from Ocelot (minor changes wrt Panther)
        PHYS_Studio_Base_Ocelot().Studio_2GFSK_base(phy, model)
        # Specific settings from Panther\Phys\Phys_Internal_Base.py
        phy.profile_inputs.agc_power_target.value = -8
        phy.profile_inputs.symbols_in_timing_window.value = 14
        phy.profile_inputs.timing_detection_threshold.value = 20
        phy.profile_inputs.agc_period.value = 0
        phy.profile_inputs.agc_speed.value = model.vars.agc_speed.var_enum.FAST


    def PHY_Studio_2450M_2GFSK_1Mbps_500K(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='915M 2GFSK 2Mbps 500K', phy_name=phy_name)

        # Start with the base function
        self.Studio_2GFSK_base(phy, model)

        # Add data-rate specific parameters
        phy.profile_inputs.bitrate.value = 1000000
        phy.profile_inputs.deviation.value = 500000

        # Add band-specific parameters
        phy.profile_inputs.base_frequency_hz.value = 2450000000

        phy.profile_inputs.rx_xtal_error_ppm.value = 20
        phy.profile_inputs.tx_xtal_error_ppm.value = 20

        self._set_xtal_frequency(phy, 40000000)

        return phy


    def PHY_Studio_2450M_2GFSK_250Kbps_125K(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='2450M 2GFSK 250Kbps 125K', phy_name=phy_name)

        # Start with the base function
        self.Studio_2GFSK_base(phy, model)

        # Add data-rate specific parameters
        phy.profile_inputs.bitrate.value = 250000
        phy.profile_inputs.deviation.value = 125000

        # Add band-specific parameters
        phy.profile_inputs.base_frequency_hz.value = 2450000000

        phy.profile_inputs.rx_xtal_error_ppm.value = 20
        phy.profile_inputs.tx_xtal_error_ppm.value = 20

        self._set_xtal_frequency(phy, 40000000)

        return phy


    def PHY_Studio_2450M_2GFSK_2Mbps_1M(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='2450M 2GFSK 2Mbps 1M', phy_name=phy_name)

        # Start with the base function
        self.Studio_2GFSK_base(phy=phy, model=model)

        # Add data-rate specific parameters
        phy.profile_inputs.bitrate.value = 2000000
        phy.profile_inputs.deviation.value = 1000000

        # Add band-specific parameters
        phy.profile_inputs.base_frequency_hz.value = 2450000000

        phy.profile_inputs.rx_xtal_error_ppm.value = 20
        phy.profile_inputs.tx_xtal_error_ppm.value = 20

        self._set_xtal_frequency(phy, 40000000)

        return phy

