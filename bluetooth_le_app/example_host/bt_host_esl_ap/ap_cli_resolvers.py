"""
ESL AP CLI placeholder resolver plugins.
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

import esl_lib_wrapper as elw
from esl_lib import Address

# Virtual placeholders resolved through tag_db at runtime (not direct event fields).
# Available for any event that carries a device identifier (address, connection_handle, or node_id).
VIRTUAL_PLACEHOLDERS = {"ble_address", "esl_id", "group_id"}
DEVICE_ID_FIELDS = {"address", "connection_handle", "node_id"}
_UNSET = object()

def split_conditional(token):
    """Split ``token`` on ``|`` while respecting ``{…}`` nesting depth.

    Unlike a plain ``str.split('|')``, pipe characters inside nested brace
    groups (e.g. ``{if|…}`` or ``{name}``) are *not* treated as separators.
    """
    parts = []
    depth = 0
    current = []
    for ch in token:
        if ch == '{':
            depth += 1
            current.append(ch)
        elif ch == '}':
            depth -= 1
            current.append(ch)
        elif ch == '|' and depth == 0:
            parts.append(''.join(current))
            current = []
        else:
            current.append(ch)
    parts.append(''.join(current))
    return parts


def normalize_hex(value):
    """Normalize a user-supplied hex string for comparison.

    Strips an optional ``0x`` / ``0X`` prefix, lowercases all digits,
    and zero-pads to an even length so the result always represents
    whole bytes (matching the output of ``bytes.hex()``).
    """
    s = value.strip()
    if s.startswith(("0x", "0X")):
        s = s[2:]
    s = s.lower()
    if len(s) % 2:
        s = "0" + s
    return s


def _match_value(actual, expected):
    """Compare an event field value against a user-supplied string.

    Comparison order:
    1. ``str(actual) == expected`` — covers int, str, and most scalar types.
    2. ``bytes.hex()`` — for ``bytes`` fields (e.g. ``data_sent``) the
       normalized hex representation is compared, accepting ``0x`` prefix,
       mixed case, and odd-length input (zero-padded to whole bytes).
    3. Reverse constant lookup — for integer values, checks whether
       ``expected`` is a known constant in esl_lib_wrapper whose value
       equals ``actual``.  Works for any prefix (SL_STATUS_*, ESL_LIB_STATUS_*,
       ESL_LIB_CONNECTION_STATE_*, etc.) without hardcoded prefix lists.
    """
    if str(actual) == expected:
        return True
    if isinstance(actual, bytes):
        return actual.hex() == normalize_hex(expected)
    if isinstance(actual, int):
        try:
            return getattr(elw, expected) == actual
        except AttributeError:
            pass
    return False


class PlaceholderResolver:
    """ Base class for an easily expandable placeholder substitution engine for the ESL AP CLI """
    def can_resolve(self, field: str) -> bool:
        raise NotImplementedError

    def resolve(self, field: str, event) -> str:
        raise NotImplementedError


class EventFieldResolver(PlaceholderResolver):
    """ Simple ESL library event field resolver """
    def can_resolve(self, field):
        return True  # fallback resolver

    def resolve(self, field, event):
        try:
            value = getattr(event, field)
        except AttributeError:
            raise AttributeError(
                f"Event '{type(event).__name__}' has no field '{field}'."
            )
        return repr(value) if isinstance(value, Address) else str(value)


class VirtualFieldResolver(PlaceholderResolver):
    """ ESL library event device identifier fields resolver / translator """
    def __init__(self, tag_lookup):
        self.tag_lookup = tag_lookup
        self._cache = _UNSET

    def can_resolve(self, field):
        return field in VIRTUAL_PLACEHOLDERS

    def resolve(self, field, event):
        if self._cache is _UNSET:
            self._cache = self.tag_lookup(event)

        tag = self._cache
        if tag is None:
            raise AttributeError(f"Cannot resolve virtual placeholder '{field}': device not found in tag database.")

        value = getattr(tag, field, None)
        if value is None:
            raise AttributeError(f"Tag has no '{field}' assigned (device may not be fully configured).")

        return repr(value) if isinstance(value, Address) else str(value)

class IfResolver(PlaceholderResolver):
    """
    Conditional resolver with pipe-separated fields.
    Then/else values may contain spaces (full command fragments) and nested
    {placeholder} tokens that are resolved in a subsequent phase.

    Syntax:
        {if|field|expected|then_value|else_value}
    Example:
        {if|status|SL_STATUS_OK|ping {esl_id}|disconnect {ble_address}}
    """
    def can_resolve(self, token: str) -> bool:
        return token.startswith("if|")

    def resolve(self, token: str, event) -> str:
        parts = split_conditional(token)
        # parts = ["if", field, expected, then_value, else_value]
        if len(parts) != 5:
            raise ValueError(f"Invalid IF placeholder syntax: {token}")

        _, field, expected, then_val, else_val = parts

        actual = getattr(event, field, None)
        return then_val if _match_value(actual, expected) else else_val


class CaseResolver(PlaceholderResolver):
    """
    Switch-case style conditional resolver with pipe-separated fields.
    Output values may contain spaces (full command fragments) and nested
    {placeholder} tokens that are resolved in a subsequent phase.

    Syntax:
        {case|field|val1|out1|val2|out2|default}
    Example:
        {case|status|SL_STATUS_OK|ping {esl_id}|SL_STATUS_TIMEOUT|list|disconnect {ble_address}}
    """

    def can_resolve(self, token: str) -> bool:
        return token.startswith("case|")

    def resolve(self, token: str, event) -> str:
        parts = split_conditional(token)
        # parts = ["case", field, val1, out1, val2, out2, ..., default]
        if len(parts) < 5 or len(parts) % 2 == 0:
            raise ValueError(f"Invalid CASE placeholder syntax: {token}")

        field = parts[1]
        cases = parts[2:-1]
        default = parts[-1]

        actual = getattr(event, field, None)

        # Iterate pairs: (val, out)
        for i in range(0, len(cases), 2):
            if _match_value(actual, cases[i]):
                return cases[i + 1]

        return default
