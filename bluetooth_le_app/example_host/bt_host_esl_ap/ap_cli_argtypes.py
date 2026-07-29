"""
ESL AP CLI argument type validators for argparse.
"""

# Copyright 2026 Silicon Laboratories Inc. www.silabs.com
#
# SPDX-License-Identifier: Zlib
#
# The licensor of this software is Silicon Laboratories Inc.
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import re
import argparse
from datetime import datetime as dt
from ap_config import IOP_TEST
from ap_constants import (
    VALID_ESL_ID_NUMBER_REGEX,
    VALID_GROUP_ID_NUMBER_REGEX,
    VALID_BD_ADDRESS_REGEX,
)
from esl_lib import EventType, EVENT_PREFIX
import esl_lib_wrapper as elw

# Known event names for script wait (lowercase, no prefix; matches EventDispatcher.notify)
KNOWN_EVENT_NAMES = {et.name for et in EventType.all()}

# Adv dedup CLI bounds from esl_lib_adv_dedup_config.h (via esl_lib_wrapper).
ADV_DEDUP_REFRESH_S_MIN = elw.ESL_LIB_ADV_DEDUP_REFRESH_MS_MIN // 1000
ADV_DEDUP_REFRESH_S_MAX = elw.ESL_LIB_ADV_DEDUP_REFRESH_MS_MAX // 1000
ADV_DEDUP_PERIOD_MULT_MIN = elw.ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_MIN / 10.0
ADV_DEDUP_PERIOD_MULT_MAX = elw.ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_MAX / 10.0
ADV_DEDUP_CACHE_SIZE_MIN = elw.ESL_LIB_ADV_DEDUP_CACHE_SIZE_MIN
ADV_DEDUP_CACHE_SIZE_MAX = elw.ESL_LIB_ADV_DEDUP_CACHE_SIZE_MAX
ADV_DEDUP_REFRESH_SECONDS_RANGE = "[%d-%d]" % (
    ADV_DEDUP_REFRESH_S_MIN,
    ADV_DEDUP_REFRESH_S_MAX,
)
ADV_DEDUP_CACHE_SIZE_RANGE = "[%d-%d]" % (
    ADV_DEDUP_CACHE_SIZE_MIN,
    ADV_DEDUP_CACHE_SIZE_MAX,
)
ADV_DEDUP_PERIOD_MULT_MIN_STR = "%g" % ADV_DEDUP_PERIOD_MULT_MIN
ADV_DEDUP_PERIOD_MULT_MAX_STR = "%g" % ADV_DEDUP_PERIOD_MULT_MAX
ADV_DEDUP_PERIOD_MULT_RANGE = "%s to %s" % (
    ADV_DEDUP_PERIOD_MULT_MIN_STR,
    ADV_DEDUP_PERIOD_MULT_MAX_STR,
)


def ble_address_type(arg_value):
    pat = re.compile(r"(" + VALID_BD_ADDRESS_REGEX + ")")
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Invalid Bluetooth address type.")
    return arg_value


def ble_address_type_all(arg_value):
    pat = re.compile(r"(" + VALID_BD_ADDRESS_REGEX + "|all)")
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Not a valid Bluetooth address.")
    return arg_value


def address_type(arg_value):
    pat = re.compile(
        r"^("
            + VALID_ESL_ID_NUMBER_REGEX
            + r"|"
            + VALID_BD_ADDRESS_REGEX
            + r"|all"
            + r"|\s*"
        + r")$"
    )
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Invalid address type.")
    return arg_value


def esl_id_type(arg_value):
    pat = re.compile(r"(" + VALID_ESL_ID_NUMBER_REGEX + "|all)")
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Invalid ESL ID value. Please select from the allowed range of 0 to 254, or you may use 'all' as a substitute for 255 in some contexts.")
    return arg_value


def esl_group_id_type(arg_value):
    re_str = VALID_GROUP_ID_NUMBER_REGEX if not IOP_TEST else VALID_ESL_ID_NUMBER_REGEX # IOP_TEST mode allows full <u8> range for RFU bit tests
    pat = re.compile(r"(" + re_str + ")")
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Invalid ESL Group ID. Please select from the allowed range of 0 to 127!")
    return int(arg_value)


def event_type(arg_value):
    """Validate and normalize event name for script wait (e.g. connection_opened, tag_found).
    Accepts any case and optional EVENT_PREFIX (e.g. ESL_LIB_EVT_ or esl_lib_evt_).
    """
    if not arg_value or not str(arg_value).strip():
        raise argparse.ArgumentTypeError("Event name must not be empty.")
    normalized = str(arg_value).strip().lower()
    prefix_lower = EVENT_PREFIX.lower()
    if normalized.startswith(prefix_lower):
        normalized = normalized[len(prefix_lower):]
    if normalized not in KNOWN_EVENT_NAMES:
        raise argparse.ArgumentTypeError(
            "Invalid event name: '%s'. Known events: %s."
            % (arg_value, ", ".join(sorted(KNOWN_EVENT_NAMES)))
        )
    return normalized


def time_type(arg_value):
    try:
        if "." in arg_value:
            arg_value = dt.strptime(arg_value, "%H:%M:%S.%f")
        else:
            arg_value = dt.strptime(arg_value, "%H:%M:%S")
        return arg_value
    except (
        TypeError,
        ValueError,
    ) as exc:  # strptime can cause type or value error - exception chaining
        raise argparse.ArgumentTypeError(
            "Invalid argument [time=<hh:mm:ss[.f]>]: the execution time of the command must be in hour:min:sec[.fraction] format."
        ) from exc


def date_type(arg_value):
    try:
        arg_value = dt.strptime(arg_value, "%Y-%m-%d")
        return arg_value
    except (
        ValueError,
        TypeError,
    ) as exc:  # strptime can cause type or value error - exception chaining
        raise argparse.ArgumentTypeError(
            "Invalid argument [date=<YYYY-MM-DD>]: the execution date of the command in ISO-8601 format."
        ) from exc


def data_type(arg_value):
    pat = re.compile(r"((0(?i)[x])?(?i)[0-9a-f]{1,32})")
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Invalid data type for vendor opcode command.")
    return arg_value


def _adv_dedup_seconds_in_range(seconds, name):
    if ADV_DEDUP_REFRESH_S_MIN <= seconds <= ADV_DEDUP_REFRESH_S_MAX:
        return
    raise argparse.ArgumentTypeError(
        "%s must be an integer from %d to %d seconds"
        % (name, ADV_DEDUP_REFRESH_S_MIN, ADV_DEDUP_REFRESH_S_MAX)
    )


def adv_dedup_refresh_seconds_type(arg_value):
    try:
        seconds = int(arg_value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "refresh must be an integer from %d to %d seconds"
            % (ADV_DEDUP_REFRESH_S_MIN, ADV_DEDUP_REFRESH_S_MAX)
        ) from exc
    _adv_dedup_seconds_in_range(seconds, "refresh")
    return seconds * 1000


def adv_dedup_watchdog_seconds_type(arg_value):
    try:
        seconds = int(arg_value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "watchdog must be an integer from %d to %d seconds"
            % (ADV_DEDUP_REFRESH_S_MIN, ADV_DEDUP_REFRESH_S_MAX)
        ) from exc
    _adv_dedup_seconds_in_range(seconds, "watchdog")
    return seconds * 1000


def adv_dedup_cache_size_type(arg_value):
    try:
        size = int(arg_value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "cache size must be an integer from %d to %d"
            % (ADV_DEDUP_CACHE_SIZE_MIN, ADV_DEDUP_CACHE_SIZE_MAX)
        ) from exc
    if not (ADV_DEDUP_CACHE_SIZE_MIN <= size <= ADV_DEDUP_CACHE_SIZE_MAX):
        raise argparse.ArgumentTypeError(
            "cache size must be an integer from %d to %d"
            % (ADV_DEDUP_CACHE_SIZE_MIN, ADV_DEDUP_CACHE_SIZE_MAX)
        )
    return size


def adv_dedup_multiplier_type(arg_value):
    try:
        multiplier = float(arg_value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "multiplier must be a number from %s to %s"
            % (ADV_DEDUP_PERIOD_MULT_MIN_STR, ADV_DEDUP_PERIOD_MULT_MAX_STR)
        ) from exc
    if not (ADV_DEDUP_PERIOD_MULT_MIN <= multiplier <= ADV_DEDUP_PERIOD_MULT_MAX):
        raise argparse.ArgumentTypeError(
            "multiplier must be a number from %s"
            % ADV_DEDUP_PERIOD_MULT_RANGE
        )
    return multiplier
