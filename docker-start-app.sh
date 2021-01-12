#!/bin/bash

# import other libraries
source ./utils/logging_utils.sh

# ----------------------------------------------------------------------
# Script definitions
# ----------------------------------------------------------------------

# default one used as repo path to deploy
OS_MONITOR_OUTPUT=/opt/linux-server-tools/os-monitor/out

# usage help use
# ----------------------------------------------------------------------
usage() {
    log_info "\n--- [DOCKER]: docker-start-app.sh ---\n"
    echo -e "Usage:\n"
    exit 0
}

# script error handler
# ----------------------------------------------------------------------
handle_error() {
    error_msg=$1
    log_error ""
    log_error "==================================================================="
    log_error " > [DOCKER]: ERROR:"
    log_error " > $error_msg"
    log_error "==================================================================="
    log_warning "\n > Exiting...\n"
    exit 1
}

# run script as root
# ----------------------------------------------------------------------
if [ "$EUID" -ne 0 ] ; then
    handle_error "docker-compose is required and it is not installed!"
fi

# check docker-compose command exists
# ----------------------------------------------------------------------
if ! command -v COMMAND &> /dev/null
then
    handle_error "COMMAND could not be found"
    exit
fi

# validate arguments parsing
# ----------------------------------------------------------------------
while getopts "h" option; do
    case "$option" in
        h) usage ;;
        *) usage ;;
    esac
done
echo "" # new line

echo " > [DOCKER]: Running Docker App as user: '$(whoami)'"

# create logs folder (if not exists)
# ----------------------------------------------------------------------
if [ ! -d "./logs" ] ; then
    echo " > [DOCKER]: Creating logs folder..."
    mkdir logs
fi

# validate output monitor directory exists
# ----------------------------------------------------------------------
if [ ! -d "$OS_MONITOR_OUTPUT" ] ; then
    handle_error "'$OS_MONITOR_OUTPUT' is not created yet!"
fi

# set the repo path variable use at docker-compose file.
export OS_MONITOR_OUTPUT="$OS_MONITOR_OUTPUT"

log_debug " > [DOCKER]: Executing docker-compose Process...\n"

echo -e " > [DOCKER]: Stop all running containers..."
docker-compose -f docker-compose.yml down
log_info " > [DOCKER]: Containers Stopped [OK]\n"
echo -e " ------------------------------------------------------------"

echo -e " > [DOCKER]: Starting containers..."
docker-compose -f docker-compose.yml up --build -d
docker_exit_status=$?

if [ $docker_exit_status -ne 0 ]; then
    handle_error "docker-compose command failed! Check the logs..."
fi

echo -e "\n"
log_info "==================================================================="
log_info " > [DOCKER]: Docker App Executed! [OK]"
log_info ""
log_info " > [Executed in Background...]"
log_info "==================================================================="
echo -e "\n"