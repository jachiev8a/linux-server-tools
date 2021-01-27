#!/bin/bash

ANSI_LOG_OFF="\033[0m"
ANSI_LOG_RED="\e[91m"
ANSI_LOG_GREEN="\e[92m"
ANSI_LOG_YELLOW="\e[93m"
ANSI_LOG_BLUE="\e[94m"
ANSI_LOG_CYAN="\e[96m"
ANSI_LOG_WHITE="\e[97m"

# log_fine
# ----------------------------------------------------------------------
function log_fine() {
    local log_msg="$1"
    echo -e "$ANSI_LOG_CYAN$log_msg$ANSI_LOG_OFF"
}

# log_debug
# ----------------------------------------------------------------------
function log_debug() {
    local log_msg="$1"
    echo -e "$ANSI_LOG_BLUE$log_msg$ANSI_LOG_OFF"
}

# log_info
# ----------------------------------------------------------------------
function log_info() {
    local log_msg="$1"
    echo -e "$ANSI_LOG_GREEN$log_msg$ANSI_LOG_OFF"
}

# log_warning
# ----------------------------------------------------------------------
function log_warning() {
    local log_msg="$1"
    echo -e "$ANSI_LOG_YELLOW$log_msg$ANSI_LOG_OFF"
}

# log_error
# ----------------------------------------------------------------------
function log_error() {
    local log_msg="$1"
    echo -e "$ANSI_LOG_RED$log_msg$ANSI_LOG_OFF"
}

# log (normal)
# ----------------------------------------------------------------------
function log_white() {
    local log_msg="$1"
    echo -e "$ANSI_LOG_WHITE$log_msg$ANSI_LOG_WHITE"
}

# log (normal)
# ----------------------------------------------------------------------
function log() {
    local log_msg="$1"
    echo -e "$log_msg"
}

# banner / header
# ----------------------------------------------------------------------
function print_header() {
    local tool_name="$1"
    log_white " ==================================================================="
    log_white " |  [$tool_name]"
    log_white " ==================================================================="
    log ""
}
