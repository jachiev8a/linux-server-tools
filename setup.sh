#!/bin/bash

# import other libraries
source ./utils/logging_utils.sh
source ./bin/setenv.sh

# ----------------------------------------------------------------------
# Script definitions
# ----------------------------------------------------------------------

RUNNING_RHEL_OS=true

filename=$( basename -- "$0" )
SCRIPT_NAME="${filename%.*}"

# interface variables [setenv.sh]:
# --------------------------------------------------
# server tools root dir
TOOLS_ROOT_DIR="$SERVER_TOOLS_ROOT_DIR"
# destination directory for the repository
TOOL_REPO_DIR="$SERVER_TOOLS_REPO_DIR"
# tools user used
TOOLS_USER="$SERVER_TOOLS_USER"
# logs dir
TOOLS_LOGS_DIR="$SERVER_TOOLS_LOGS_DIR"
# --------------------------------------------------

DELIMITER="# ------------------------------------------------------------"

CRONTAB_COMMENT="# linux-server-tools (os-monitor) - [daily 23:00] | contact: javier.ochoa"
CRONTAB_CMD="0 23 * * *  $TOOLS_USER /bin/bash $TOOLS_ROOT_DIR/os-monitor.sh >> $TOOLS_LOGS_DIR/os-monitor.log"
CRONTAB_STRING="$CRONTAB_COMMENT\n$DELIMITER\n$CRONTAB_CMD\n"

CRONTAB_USER_FILE="/etc/cron.d/$TOOLS_USER"
CRONTAB_HEADER_FILE="# crontab file generated by server-tools (user: $TOOLS_USER)\n$DELIMITER"

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
        log ""
        adduser "$TOOLS_USER"
        log ""
    else
        # UBUNTU: adduser
        log_debug " > Adding user for UBUNTU OS environment..."
        log ""
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

# logs dir
if [ ! -d "$TOOLS_LOGS_DIR" ] ; then
    log_debug " > [$SCRIPT_NAME]: Creating logs directory: $TOOLS_LOGS_DIR"
    mkdir "$TOOLS_LOGS_DIR"
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
    log ""
fi

# copy repository to directory destination
# ----------------------------------------------------------------------
log " > [$SCRIPT_NAME]: rsync this repository to: $TOOL_REPO_DIR"
log "------------------------------------------------------------"

DIR_TO_RSYNC="$(pwd -P)/"
log_debug " > running rsync: '$DIR_TO_RSYNC' -> '$TOOL_REPO_DIR'"

log ""
rsync -avr --info=progress2 --info=name0 --stats "$DIR_TO_RSYNC" "$TOOL_REPO_DIR"
log ""

# Change Directory permissions
# ----------------------------------------------------------------------
log " > [$SCRIPT_NAME]: Changing Directory permissions to user '$TOOLS_USER'"
log "------------------------------------------------------------"

chown -R "$TOOLS_USER":"$TOOLS_USER" "$TOOLS_ROOT_DIR"

# Crontab setup
# ----------------------------------------------------------------------
log " > [$SCRIPT_NAME]: Setup crontab for user '$TOOLS_USER'..."
log "------------------------------------------------------------"

# Crontab file exists
if [ ! -f "$CRONTAB_USER_FILE" ] ; then
    log_debug " > [$SCRIPT_NAME]: crontab file does not exist. Generating one..."
    log_debug " > [$SCRIPT_NAME]: Generating crontab file: '$CRONTAB_USER_FILE'"
    echo -e "$CRONTAB_HEADER_FILE" > "$CRONTAB_USER_FILE"
    log_info " > [$SCRIPT_NAME]: crontab file successfully generated! [OK]"
fi

# returns 0 if nothing was found already
CRONTAB_EXISTS_ALREADY=$( grep -c "$CRONTAB_SEARCH_KEY" "$CRONTAB_USER_FILE" )

if [ "$CRONTAB_EXISTS_ALREADY" -eq 0 ]; then
    log_debug " > Adding crontab CMD for user: '$TOOLS_USER'"
    echo -e "$CRONTAB_STRING" >> "$CRONTAB_USER_FILE"
    log_info " > [$SCRIPT_NAME]: crontab CMD successfully generated! [OK]"
    log "------------------------------------------------------------"
    log_debug "$( cat "$CRONTAB_USER_FILE")"
    log "------------------------------------------------------------"
else
    log " > crontab already set. Nothing to do!"
fi

log ""
log_info "==================================================================="
log_info " > [$SCRIPT_NAME]: Successfully Executed! [OK]"
log_info "==================================================================="
log ""