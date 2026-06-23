/**
 * @file sl_jamming_cmd_handlers.h
 * @brief Jamming detection command handler constants and subcommand IDs.
 * @copyright 2026 Silicon Laboratories Inc.
 */

#ifndef SL_JAMMING_CMD_HANDLERS_H
#define SL_JAMMING_CMD_HANDLERS_H

#include "SerialAPI.h"

#define FUNC_ID_PROP_JAMMING_DETECTION_COMMAND FUNC_ID_PROPRIETARY_1

typedef enum func_id_propieraty_jamming_subcommands {
  FUNC_ID_PROP_JAMMING_SUBCOMMAND_REPORT,
  FUNC_ID_PROP_JAMMING_SUBCOMMAND_COLLECTION,
  FUNC_ID_PROP_JAMMING_SUBCOMMAND_CHANNEL_CONFIGURATION,
  FUNC_ID_PROP_JAMMING_SUBCOMMAND_REPORT_CONFIGURATION
} func_id_propieraty_jamming_subcommands_t;

#endif /* SL_JAMMING_CMD_HANDLERS_H */
