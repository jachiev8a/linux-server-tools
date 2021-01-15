#!/bin/bash

# import other libraries
source ./utils/logging_utils.sh
source ./bin/setenv.sh

# ----------------------------------------------------------------------
# Script definitions
# ----------------------------------------------------------------------

SCRIPT_NAME="Setup"
RUNNING_RHEL_OS=true

# interface variables [setenv.sh]:
# --------------------------------------------------
# server tools root dir
TOOLS_ROOT_DIR="$SERVER_TOOLS_ROOT_DIR"
# destination directory for the repository
TOOL_REPO_DIR="$SERVER_TOOLS_REPO_DIR"
# tools user used
TOOLS_USER="$SERVER_TOOLS_USER"
# --------------------------------------------------

CRONTAB_COMMENT="# linux-server-tools (os-monitor) - [daily 23:00] | contact: javier.ochoa"
CRONTAB_CMD="0 23 * * *   $TOOLS_ROOT_DIR/os-monitor.sh"
CRONTAB_STRING="$CRONTAB_COMMENT\n$CRONTAB_CMD"

CRONTAB_SEARCH_KEY="os-monitor.sh"

# usage help use
# ----------------------------------------------------------------------
usage() {
    log_info "\n--- [$SCRIPT_NAME]: setup.sh ---\n"
    log "Usage:\n"
    log ""
    exit 0
}

# script error handler
# ----------------------------------------------------------------------
handle_error() {
    error_msg=$1
    log_error ""
    log_error "==================================================================="
    log_error " > [$SCRIPT_NAME]: ERROR:"
    log_error " > $error_msg"
    log_error "==================================================================="
    log_warning "\n > Exiting...\n"
    exit 1
}

# run script as root
# ----------------------------------------------------------------------
if [ "$EUID" -ne 0 ] ; then
    handle_error "Please run this script as 'root' / 'sudo'"
    exit 1
fi

# validate arguments parsing
# ----------------------------------------------------------------------
while getopts "h" option; do
    case "$option" in
        h) usage ;;
        *) usage ;;
    esac
done
log "" # new line

# user validation
# ----------------------------------------------------------------------
log " > [$SCRIPT_NAME]: Validating Tools User '$TOOLS_USER'..."
log "------------------------------------------------------------"
log ""

USER_EXISTS_RES=$(grep -c "^$TOOLS_USER:" /etc/passwd)

# if 0 records are found. no user exists.
if [[ "$USER_EXISTS_RES" -eq 0 ]]; then
    log_warning "------------------------------------------------------------"
    log_warning " > [$SCRIPT_NAME]: User '$TOOLS_USER' does not exist!..."
    log_warning "------------------------------------------------------------"
    log " > Trying to create user: '$TOOLS_USER'"
    log ""

    # os validation
    # ----------------------------------------------------------------------
    log " > [$SCRIPT_NAME]: Validating Running OS..."
    log "------------------------------------------------------------"

    RUNNING_RHEL_CMD=$(grep -c -i 'red hat\|rhel' /etc/os-release)

    if [ "$RUNNING_RHEL_CMD" -eq 0 ]; then
        log_debug " > NOT running in RHEL OS environment..."
        log ""
        RUNNING_RHEL_OS=false
    fi

    # check how to add user depending on the OS
    # ----------------------------------------------------------------------
    if [ "$RUNNING_RHEL_OS" = true ]; then
        # RHEL: adduser
        log_debug " > Adding user for RHEL OS environment..."
        adduser "$TOOLS_USER"
        log ""
    else
        # UBUNTU: adduser
        log_debug " > Adding user for UBUNTU OS environment..."
        adduser --disabled-password --gecos "" "$TOOLS_USER"
        log ""
    fi
else
    log_info " > [$SCRIPT_NAME]: User '$TOOLS_USER' exists [OK]"
    log ""
fi

# create base directory structure (if not exists)
# ----------------------------------------------------------------------
log " > [$SCRIPT_NAME]: Creating Base Directory Structure..."
log "------------------------------------------------------------"
log ""

# root dir
if [ ! -d "$SERVER_TOOLS_ROOT_DIR" ] ; then
    log_debug " > [$SCRIPT_NAME]: Creating server-tools directory: $SERVER_TOOLS_ROOT_DIR"
    mkdir "$SERVER_TOOLS_ROOT_DIR"
fi

# repo dir
if [ ! -d "$TOOL_REPO_DIR" ] ; then
    log_debug " > [$SCRIPT_NAME]: Creating server-tools repository directory: $TOOL_REPO_DIR"
    mkdir "$TOOL_REPO_DIR"
fi

log_info " > [$SCRIPT_NAME]: Base Directory Structure Successfully created [OK]"
log ""

# jenkins user validation
# ----------------------------------------------------------------------
log " > [$SCRIPT_NAME]: Validating Jenkins user: '$JENKINS_USER'..."
log "------------------------------------------------------------"

JENKINS_USER_EXISTS_RES=$(grep -c "^$JENKINS_USER:" /etc/passwd)

if [ "$JENKINS_USER_EXISTS_RES" -ne 0 ]; then
    # jenkins user exists
    log_debug " > Adding jenkins user '$JENKINS_USER' to tools user-group '$TOOLS_USER'"
    usermod -a -G "$TOOLS_USER" "$JENKINS_USER"
else
    log " > jenkins user does not exist. Nothing to do!"
fi

# copy repository to directory destination
# ----------------------------------------------------------------------
log " > [$SCRIPT_NAME]: rsync this repository to: $TOOL_REPO_DIR"
log "------------------------------------------------------------"

log_debug " > running rsync: '$(pwd -P)' -> '$TOOL_REPO_DIR'"
log ""
rsync -avr --progress "$(pwd -P)" "$TOOL_REPO_DIR"

# Change Directory permissions
# ----------------------------------------------------------------------
log " > [$SCRIPT_NAME]: Changing Directory permissions to user '$TOOLS_USER'"
log "------------------------------------------------------------"

chown -R "$TOOLS_USER":"$TOOLS_USER" "$TOOLS_ROOT_DIR"

# Crontab setup
# ----------------------------------------------------------------------
log " > [$SCRIPT_NAME]: Setup Crontab for user '$TOOLS_USER'..."
log "------------------------------------------------------------"

CRONTAB_EXISTS_ALREADY=$( crontab -u "$TOOLS_USER" -l | grep -c "$CRONTAB_SEARCH_KEY")

if [ "$CRONTAB_EXISTS_ALREADY" -ne 0 ]; then
    log_debug " > Adding crontab CMD for user: '$TOOLS_USER'"
    (crontab -u "$TOOLS_USER" -l 2>/dev/null; echo "$CRONTAB_STRING") | crontab -
fi

log ""
log_info "==================================================================="
log_info " > [$SCRIPT_NAME]: Successfully Executed! [OK]"
log_info "==================================================================="
log ""