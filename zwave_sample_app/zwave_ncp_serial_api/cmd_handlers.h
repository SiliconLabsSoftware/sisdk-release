/**
 * @file
 * @copyright 2022 Silicon Laboratories Inc.
 */

#ifndef CMD_HANDLER_H_
#define CMD_HANDLER_H_

#include <stdint.h>
#include <comm_interface.h>

#ifdef ZW_CONTROLLER
#include <ZW_controller_api.h>
#endif

/**
 * @addtogroup Apps
 * @{
 * @addtogroup SerialAPI
 * @{
 */

typedef void (*cmd_handler_t)(const comm_interface_frame_ptr);

typedef struct {
  uint8_t cmd;
  cmd_handler_t pHandler;
}
cmd_handler_map_t;

#define CMD_HANDLER_SECTION "zw_cmd_handlers"

#define ZW_ADD_CMD(cmd)                                                                                                                            \
  static void cmd_handler_fcn_##cmd(__attribute__((unused)) const comm_interface_frame_ptr frame); /* Prototype */                                 \
  static const cmd_handler_map_t cmd_handler_##cmd __attribute__((__used__, __section__(CMD_HANDLER_SECTION))) = { (cmd), cmd_handler_fcn_##cmd }; \
  static void cmd_handler_fcn_##cmd(__attribute__((unused)) const comm_interface_frame_ptr frame)

/**
 * Non-payload overhead sizes for Send Data like commands.
 * Used to check that inside dataLength field is consistent with actual frame length.
 *
 * The minimum required payload length for each command is:
 *   variable_offset + OVERHEAD + dataLength
 */

/* nodeID + dataLength + txOptions + session_id */
#define SEND_DATA_FRAME_OVERHEAD              4
/* nodeID + dataLength + txOptions + txSecOptions + securityKey + txOptions2 + session_id */
#define SEND_DATA_EX_FRAME_OVERHEAD           7
/* numNodes + dataLength + txOptions + session_id (node list is variable) */
#define SEND_DATA_MULTI_FRAME_OVERHEAD        4
/* dataLength + txOptions + securityKey + groupId + session_id */
#define SEND_DATA_MULTI_EX_FRAME_OVERHEAD     5
/* srcNodeID + destNodeID + dataLength + txOptions + pRoute[4] + session_id */
#define SEND_DATA_BRIDGE_FRAME_OVERHEAD       9
/* srcNodeID + numNodes + dataLength + txOptions + session_id (node list is variable) */
#define SEND_DATA_MULTI_BRIDGE_FRAME_OVERHEAD 5

/**
 * Invoke command handler.
 *
 * @param[in] frame Frame
 * @return true if handler for given @p frame was invoked, false if no handler was found
 */
bool invoke_cmd_handler(const comm_interface_frame_ptr frame);

typedef bool (*cmd_foreach_callback_t)(cmd_handler_map_t const * const p_cmd_entry, uint8_t* supported_cmds_mask);

/**
 * Invokes callback for each registered command.
 *
 * Will stop if the callback returns true.
 *
 * @param callback Callback function to invoke.
 * @param supported_cmds_mask Bitmask of supported commands to pass to the callback function.
 */
void cmd_foreach(cmd_foreach_callback_t callback, uint8_t* supported_cmds_mask);

#ifdef ZW_CONTROLLER
void ZCB_ComplHandler_ZW_NodeManagement(LEARN_INFO_T *statusInfo);
#endif

/**
 * @}
 * @}
 */

#endif /* CMD_HANDLER_H_ */
