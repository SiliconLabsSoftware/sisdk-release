--[[
    This script validates that apps which configure platform defined logging
    include the necessary logging component (ot_sl_log, ot_rtt_log, or ot_backchannel_log) to include the platform
    logging API definitions and associated utility interfaces.
--]]
local log_output_cfg = slc.config("OPENTHREAD_CONFIG_LOG_OUTPUT")
local platform_logging_enabled = log_output_cfg and log_output_cfg.value == "OPENTHREAD_CONFIG_LOG_OUTPUT_PLATFORM_DEFINED"
local has_platform_logger = slc.is_provided("ot_sl_log") or slc.is_provided("ot_rtt_log") or slc.is_provided("ot_backchannel_log")

if platform_logging_enabled and not has_platform_logger then
    validation.error("ot_sl_log, ot_rtt_log, or ot_backchannel_log must be included when OPENTHREAD_CONFIG_LOG_OUTPUT is configured to PLATFORM_DEFINED.",
                      validation.target_for_project(),
                      "Include the ot_sl_log, ot_rtt_log, or ot_backchannel_log component, or select a different log output configuration value.",
                      nil
    )
end
