/**
 * @file cmd_handlers_invoker.c
 * @copyright 2022 Silicon Laboratories Inc.
 */

#include "cmd_handlers.h"
#include <assert.h>

/* Linker: section CMD_HANDLER_SECTION. __start_ / __stop_ are address symbols; extern T name[] is the incomplete-type idiom. */
extern const cmd_handler_map_t __start_zw_cmd_handlers[];
extern const cmd_handler_map_t __stop_zw_cmd_handlers[];

bool invoke_cmd_handler(const comm_interface_frame_ptr frame)
{
  cmd_handler_map_t const * iter = __start_zw_cmd_handlers;
  for ( ; iter < __stop_zw_cmd_handlers; ++iter) {
    if (iter->cmd == frame->cmd) {
      iter->pHandler(frame);
      return true;
    }
  }

  return false;
}

void cmd_foreach(cmd_foreach_callback_t callback, uint8_t* supported_cmds_mask)
{
  assert(callback != NULL);
  cmd_handler_map_t const * iter = __start_zw_cmd_handlers;
  for ( ; iter < __stop_zw_cmd_handlers; ++iter) {
    if (true == callback(iter, supported_cmds_mask)) {
      break;
    }
  }
}
