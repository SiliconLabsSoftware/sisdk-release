#!/bin/bash
# SPDX-License-Identifier: Zlib
# Native Raspberry Pi setup for Multiprotocol (Debian packages, no Docker).
# Replaces the container bootstrap path in run.sh: install host packages, install systemd
# units from artifacts/systemd, enable cpcd, optional CPCd binding key generation.
#
# Usage: see --help.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PACKAGES_SH="${SCRIPT_DIR}/artifacts/tmp/install_silabs_packages.sh"
SYSTEMD_SRC="${SCRIPT_DIR}/artifacts/systemd"

CPCD_DEFAULT_BINDING_KEY_PATH="${HOME}/.cpcd"
CPCD_DEFAULT_BINDING_KEY_FILE="${CPCD_DEFAULT_BINDING_KEY_PATH}/binding.key"

CPCD_SECURITY_ENABLED=true
CPCD_CONFIG_FILE=""
CPCD_BINDING_KEY_FILE="${CPCD_DEFAULT_BINDING_KEY_FILE}"
GENERATE_CPCD_BINDING_KEY=false
START_CPCD=true
INSTALL_HOST_PACKAGES=true
INSTALL_SYSTEMD=true

# Log directory used by legacy Docker run.sh for binding key staging (parity with run.sh).
LEGACY_LOG_DIR="/tmp/multiprotocol-container/log"

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

Prepare a Raspberry Pi (or Debian host) for multiprotocol host tests using .deb/.tgz
packages and systemd units (same as the host container image, without Docker).

Options:
  -p DIR       Host package directory (contains *.deb and/or *.tgz). Passed to
               install_silabs_packages.sh. If omitted, skip package install.
  -c FILE      Path to cpcd.conf to install on the system (optional).
  -k FILE      CPCd binding key file to use (default: ${CPCD_DEFAULT_BINDING_KEY_FILE}).
  -K           Generate CPCd ECDH binding key (requires cpcd on PATH; RCP must be reachable).
  -X           Disable CPCd security (no binding key mount).
  --no-start   Do not start cpcd.service after setup.
  --no-packages Skip installing .deb/.tgz from -p (still install systemd units if enabled).
  --no-systemd Skip copying systemd units (for bring-up only).
  -h|--help    Show this help.

Environment:
  SUDO        If set, use this instead of "sudo" for privileged steps (e.g. SUDO=echo).

Examples:
  $(basename "$0") -p /artifacts/host-packages
  $(basename "$0") -p /artifacts/host-packages -c /etc/cpcd.conf -K
EOF
}

SUDO="${SUDO:-sudo}"

run_as_root() {
  "$SUDO" "$@"
}

require_file() {
  if [[ ! -f "$1" ]]; then
    echo "Error: missing file: $1" >&2
    exit 1
  fi
}

install_cpcd_conf() {
  if [[ -z "${CPCD_CONFIG_FILE}" ]]; then
    return 0
  fi
  require_file "${CPCD_CONFIG_FILE}"
  echo "Installing cpcd.conf from ${CPCD_CONFIG_FILE}"
  run_as_root install -m 0644 "${CPCD_CONFIG_FILE}" /etc/cpcd.conf
}

install_host_packages() {
  if [[ "${INSTALL_HOST_PACKAGES}" != "true" ]]; then
    echo "Skipping host package install (--no-packages or no -p)."
    return 0
  fi
  if [[ -z "${PACKAGE_ROOT:-}" ]]; then
    echo "No -p DIR: skipping host package install."
    return 0
  fi
  require_file "${INSTALL_PACKAGES_SH}"
  echo "Installing host packages from ${PACKAGE_ROOT}"
  run_as_root bash "${INSTALL_PACKAGES_SH}" -p "${PACKAGE_ROOT}"
}

install_systemd_units() {
  if [[ "${INSTALL_SYSTEMD}" != "true" ]]; then
    echo "Skipping systemd unit install (--no-systemd)."
    return 0
  fi
  if [[ ! -d "${SYSTEMD_SRC}" ]]; then
    echo "Error: systemd source dir not found: ${SYSTEMD_SRC}" >&2
    exit 1
  fi
  echo "Installing systemd units from ${SYSTEMD_SRC}"
  run_as_root install -m 0644 "${SYSTEMD_SRC}"/*.service /etc/systemd/system/
  run_as_root systemctl daemon-reload

  # Match Dockerfile: disable bluetooth autostart; enable cpcd; disable OTBR agent/web if present.
  run_as_root systemctl disable bluetooth.service 2>/dev/null || true
  run_as_root systemctl enable cpcd.service
  run_as_root systemctl disable otbr-agent 2>/dev/null || true
  run_as_root systemctl disable otbr-web 2>/dev/null || true
}

generate_binding_key() {
  echo "Generating CPCd ECDH binding key at ${CPCD_DEFAULT_BINDING_KEY_FILE}"
  mkdir -p "${LEGACY_LOG_DIR}"
  run_as_root rm -f "${LEGACY_LOG_DIR}/binding.key"
  run_as_root systemctl stop cpcd 2>/dev/null || true
  run_as_root systemctl start cpcd || true
  sleep 3
  run_as_root systemctl stop cpcd 2>/dev/null || true
  echo "Running cpcd --bind ecdh (requires RCP; may fail if RCP is bound elsewhere)"
  if run_as_root cpcd --bind ecdh --key "${LEGACY_LOG_DIR}/binding.key"; then
    if run_as_root test -s "${LEGACY_LOG_DIR}/binding.key"; then
      run_as_root mkdir -p "${CPCD_DEFAULT_BINDING_KEY_PATH}"
      run_as_root mv "${LEGACY_LOG_DIR}/binding.key" "${CPCD_DEFAULT_BINDING_KEY_FILE}"
      run_as_root chown "${SUDO_USER:-$USER}:${SUDO_USER:-$USER}" "${CPCD_DEFAULT_BINDING_KEY_FILE}"
      echo "Generated binding key at ${CPCD_DEFAULT_BINDING_KEY_FILE}"
    else
      echo "Error: binding key was not written to ${LEGACY_LOG_DIR}/binding.key" >&2
      exit 1
    fi
  else
    echo "Error: cpcd --bind failed. See CPCd security documentation." >&2
    exit 1
  fi
}

require_binding_key_file() {
  if [[ "${CPCD_SECURITY_ENABLED}" != "true" ]]; then
    return 0
  fi
  if [[ ! -e "${CPCD_BINDING_KEY_FILE}" ]]; then
    echo ""
    echo "No CPCd binding key file found at ${CPCD_BINDING_KEY_FILE}."
    echo "Use -K to generate one, or -X to run without security."
    echo ""
    exit 1
  fi
  echo "Using binding key file ${CPCD_BINDING_KEY_FILE} (ensure cpcd.conf points to it)."
}

start_cpcd() {
  if [[ "${START_CPCD}" != "true" ]]; then
    echo "Skipping cpcd start (--no-start)."
    return 0
  fi
  echo "Starting cpcd.service"
  run_as_root systemctl start cpcd.service
}

# --- main --------------------------------------------------------------------

PACKAGE_ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    -p)
      shift
      PACKAGE_ROOT="${1:-}"
      shift
      ;;
    -c|--cpcd-conf)
      shift
      CPCD_CONFIG_FILE="${1:-}"
      shift
      ;;
    -k|--cpcd-binding-key-file)
      shift
      CPCD_BINDING_KEY_FILE="$(realpath "${1:-}")"
      shift
      ;;
    -K|--generate-cpcd-binding-key)
      GENERATE_CPCD_BINDING_KEY=true
      shift
      ;;
    -X|--disable-cpcd-security)
      CPCD_SECURITY_ENABLED=false
      shift
      ;;
    --no-start)
      START_CPCD=false
      shift
      ;;
    --no-packages)
      INSTALL_HOST_PACKAGES=false
      shift
      ;;
    --no-systemd)
      INSTALL_SYSTEMD=false
      shift
      ;;
    *)
      echo "Unrecognized option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -n "${PACKAGE_ROOT:-}" ]]; then
  PACKAGE_ROOT="$(realpath "${PACKAGE_ROOT}")"
fi

install_host_packages
install_systemd_units
install_cpcd_conf

if [[ "${GENERATE_CPCD_BINDING_KEY}" == "true" ]]; then
  generate_binding_key
fi

if [[ "${CPCD_SECURITY_ENABLED}" == "true" ]]; then
  require_binding_key_file
fi

start_cpcd

echo "setup_pi.sh completed."
