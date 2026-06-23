#!/usr/bin/env python3
# SPDX-License-Identifier: Zlib
"""Teardown multiprotocol host state on a Raspberry Pi (Debian packages, no Docker)."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys


def _sudo() -> list[str]:
    return [os.environ.get("SUDO", "sudo")]


def _run_ignore(cmd: list[str]) -> None:
    subprocess.run(cmd, capture_output=True, text=True)


def stop_docker_multiprotocol() -> None:
    if shutil.which("docker") is None:
        return
    _run_ignore([*_sudo(), "docker", "stop", "-t", "0", "multiprotocol"])


def stop_systemd_services() -> None:
    """Stop known multiprotocol-related units (ignore failures)."""
    sudo = _sudo()
    # Application / stack layers first, then cpcd.
    names = [
        "zigbeed",
        "zigbeed-socat",
        "hciattach",
        "cpc-hci-bridge",
    ]
    for n in names:
        _run_ignore([*sudo, "systemctl", "stop", n])

    # Template otbr@N — stop common interface IDs (matches validate_interface_id 0–3 in run.sh).
    for i in range(4):
        _run_ignore([*sudo, "systemctl", "stop", f"otbr@{i}"])

    _run_ignore([*sudo, "systemctl", "stop", "otbr-agent"])
    _run_ignore([*sudo, "systemctl", "stop", "otbr-web"])

    _run_ignore([*sudo, "systemctl", "stop", "cpcd"])


def restore_bluetooth() -> None:
    """Undo host bluetooth stop/mask from run.sh -L path (best effort)."""
    sudo = _sudo()
    _run_ignore([*sudo, "systemctl", "unmask", "bluetooth.service"])
    _run_ignore([*sudo, "systemctl", "start", "bluetooth.service"])


def main() -> int:
    p = argparse.ArgumentParser(
        description=(
            "Stop multiprotocol systemd services on the Pi (Debian packages, no Docker). "
            "Optional: stop the legacy Docker container or restore Bluetooth."
        )
    )
    p.add_argument(
        "--docker",
        action="store_true",
        help='Stop legacy container "multiprotocol" if docker is available.',
    )
    p.add_argument(
        "--restore-bluetooth",
        action="store_true",
        help="Unmask and start bluetooth.service (use after tests that masked Bluetooth).",
    )
    args = p.parse_args()

    stop_systemd_services()
    if args.docker:
        stop_docker_multiprotocol()
    if args.restore_bluetooth:
        restore_bluetooth()

    return 0


if __name__ == "__main__":
    sys.exit(main())
