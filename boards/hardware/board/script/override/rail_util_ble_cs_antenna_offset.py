from siliconlabs.slc.board_gen.project_config import ProjectConfig
from siliconlabs.slc.board_gen.hardware import Hardware
from siliconlabs.slc.board_gen.util.clock_util import get_board_id as _hardware_board_slug

import yaml
from pathlib import Path
from typing import Set


def _rail_util_cs_antenna_offset_yaml() -> Path:
    """
    Resolve generation data whether the override script lives under legacy
    platform/hardware/... or under package/boards/hardware/... (Jenkins board-gen).
    """
    rels = (
        Path('platform/scripts/board_generation/generation_files/rail_util_cs_antenna_offset.yaml'),
        Path('platform/platform/scripts/board_generation/generation_files/rail_util_cs_antenna_offset.yaml'),
    )
    here = Path(__file__).resolve().parent
    for anc in [here, *here.parents]:
        for rel in rels:
            cand = anc / rel
            if cand.is_file():
                return cand
    raise Exception(
        'rail_util_cs_antenna_offset.yaml not found. Make sure that the file exists! '
        '(searched under ancestors of {!r})'.format(here)
    )


antenna_offset_info_file = _rail_util_cs_antenna_offset_yaml()

with open(antenna_offset_info_file) as file_handle:
    antenna_offset_info = yaml.safe_load(file_handle)


def get_board_id(board: Hardware) -> str:
    return _hardware_board_slug(board)


def compatible(provides: Set[str], board: Hardware) -> bool:
    if get_board_id(board) in antenna_offset_info['cs_antenna_offset']:
        return True
    return False

def configure(project: ProjectConfig, board: Hardware, _):
    board_id = get_board_id(board)
    antenna_offset_info_board = antenna_offset_info['cs_antenna_offset'][board_id]

    project.config('SL_RAIL_UTIL_CS_ANTENNA_COUNT').value = antenna_offset_info_board['count']
    project.config('SL_RAIL_UTIL_CS_ANTENNA_OFFSET_WIRELESS_CM').set_array_values(antenna_offset_info_board['offset_wireless'])
    project.config('SL_RAIL_UTIL_CS_ANTENNA_OFFSET_WIRED_CM').set_array_values(antenna_offset_info_board['offset_wired'])

    project.config('SL_RAIL_UTIL_CS_ANTENNA_COUNT').set_user_default_value(antenna_offset_info_board['count'])
    project.config('SL_RAIL_UTIL_CS_ANTENNA_OFFSET_WIRELESS_CM').set_user_default_value("{ " + ", ".join(map(str, antenna_offset_info_board['offset_wireless'])) + " }")
    project.config('SL_RAIL_UTIL_CS_ANTENNA_OFFSET_WIRED_CM').set_user_default_value("{ " + ", ".join(map(str, antenna_offset_info_board['offset_wired'])) + " }")

