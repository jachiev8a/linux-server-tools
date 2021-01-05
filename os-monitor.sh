#!/bin/bash

# import other libraries
source logging_utils.sh

# ----------------------------------------------------------------------
# Script definitions
# ----------------------------------------------------------------------

TOOL_NAME="os-monitor"
TOOLS_USER="servertool"

TOOLS_ROOT_DIR=/opt/linux-server-tools
OS_MONITOR_DIR=$TOOLS_ROOT_DIR/os-monitor
OS_MONITOR_OUT_DIR=$OS_MONITOR_DIR/out

# usage help use
# ----------------------------------------------------------------------
usage() {
    log_info "\n--- [$TOOL_NAME]: docker-start-app.sh ---\n"
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
    log_error " > [$TOOL_NAME]: ERROR:"
    log_error " > $error_msg"
    log_error "==================================================================="
    log_warning "\n > Exiting...\n"
    exit 1
}

# run script as root
# ----------------------------------------------------------------------
if [ "$EUID" -ne 0 ] ; then
    handle_error "Please run this script as 'root'"
    exit 1
fi

# validate arguments parsing
# ----------------------------------------------------------------------
while getopts "hdi" option; do
    case "$option" in
        d) USE_DEFAULT_REPO_PATH=true ;;
        i) USE_DEFAULT_SSH_FILE=true ;;
        h) usage ;;
        *) usage ;;
    esac
done
echo "" # new line

# create directory structure (if not exists)
# ----------------------------------------------------------------------
log " > [$TOOL_NAME]: Validating Directory Structure..."
log ""

# root dir
if [ ! -d $TOOLS_ROOT_DIR ] ; then
    log_debug " > [$TOOL_NAME]: Creating main tools directory: $TOOLS_ROOT_DIR"
    mkdir $TOOLS_ROOT_DIR
fi

# tool dir
if [ ! -d $OS_MONITOR_DIR ] ; then
    log_debug " > [$TOOL_NAME]: Creating tool directory: $OS_MONITOR_DIR"
    mkdir $OS_MONITOR_DIR
fi

# tool output dir
if [ ! -d $OS_MONITOR_OUT_DIR ] ; then
    log_debug " > [$TOOL_NAME]: Creating tool output directory: $OS_MONITOR_OUT_DIR"
    mkdir $OS_MONITOR_OUT_DIR
fi

log_info " > [$TOOL_NAME]: Directory Structure Successfully created [OK]"
log ""

# user and directory permissions (if not exists)
# ----------------------------------------------------------------------
log " > [$TOOL_NAME]: Validating Tools User '$TOOLS_USER'..."
log ""

USER_EXISTS_RES=$(grep -c "^$TOOLS_USER:" /etc/passwd)

if [ $USER_EXISTS_RES -eq 0 ]; then
    handle_error "User '$TOOLS_USER' does not exist. Please create it."
else
    log_info " > [$TOOL_NAME]: User '$TOOLS_USER' exists [OK]"
    log ""
fi

log " > [$TOOL_NAME]: Changing permissions to user '$TOOLS_USER' in '$TOOLS_ROOT_DIR'"
log ""

chown -R $TOOLS_USER:$TOOLS_USER $TOOLS_ROOT_DIR

# get os metadata
# ----------------------------------------------------------------------
log " > [$TOOL_NAME]: Getting disk space..."
log ""

DATE_FORMAT=$(date +"%m-%d-%Y__%H-%M-%S__%b-%d-%Y__%Z")
FILE_NAME="$TOOL_NAME__disk__$DATE_FORMAT.txt"

df -h | grep /dev/s > $OS_MONITOR_OUT_DIR/$FILE_NAME

exit 0












echo " > [DOCKER]: Running Docker App as user: '$(whoami)'"

# create logs folder (if not exists)
# ----------------------------------------------------------------------
if [ ! -d "./logs" ] ; then
    echo " > [DOCKER]: Creating logs folder..."
    mkdir logs
fi

# Validate repo path argument
# ----------------------------------------------------------------------
if [ "$USE_DEFAULT_REPO_PATH" = true ] ; then
    echo -e " > [DOCKER]: Using Default repo path: '$DEFAULT_REPO_PATH'\n"
    REPO_PATH_TO_DEPLOY=$DEFAULT_REPO_PATH
else
    echo -e " > [DOCKER]: Setting up Repo Path...\n"
    read -r -p " > Enter the Repo Path Value: " input_repo_path

    # validate that repo path exists
    if [ ! -d "$input_repo_path" ] ; then
        handle_error "Given Repo Path does not exists! -> '$input_repo_path'"
    else
        echo -e ""
        echo -e " > [DOCKER]: Valid Repo Path Value -> '$input_repo_path'"
        log_info " > [DOCKER]: [OK]\n"
    fi
    REPO_PATH_TO_DEPLOY="$input_repo_path"
fi

# Validate ssh argument
# ----------------------------------------------------------------------
if [ "$USE_DEFAULT_SSH_FILE" = true ] ; then
    echo -e " > [DOCKER]: Using Default SSH id_rsa: '$DEFAULT_SSH_FILE'\n"
    GIT_SSH_FILE=$DEFAULT_SSH_FILE
else
    echo -e " > [DOCKER]: Setting up SSH id_rsa...\n"
    read -r -p " > Enter the SSH id_rsa Path Value: " input_ssh_path

    # validate that ssh path exists
    if [ ! -f "$input_ssh_path" ] ; then
        handle_error "Given SSH id_rsa Path does not exists! -> '$input_ssh_path'"
    else
        echo -e ""
        echo -e " > [DOCKER]: Valid SSH id_rsa Value -> '$input_ssh_path'"
        log_info " > [DOCKER]: [OK]\n"
    fi
    GIT_SSH_FILE="$input_ssh_path"
fi

# Validate ssh argument
# ----------------------------------------------------------------------
current_working_dir=$(pwd)
this_root_ssh_file="$current_working_dir/$DEFAULT_SSH_FILE_ID"

# validate that ssh path exists
# ----------------------------------------------------------------------
log_debug " > [DOCKER]: Validate SSH $DEFAULT_SSH_FILE_ID is located in root..."
echo -e " > SSH File -> '$this_root_ssh_file'"
if [ ! -f "$this_root_ssh_file" ] ; then

    echo -e " > [DOCKER]: SSH $DEFAULT_SSH_FILE_ID not located in root."
    echo -e " > [DOCKER]: start copying file from source..."
    echo -e " > Source File: '$GIT_SSH_FILE'"
    echo -e " > Destination: '$current_working_dir'"
    echo -e ""

    # copy ssh key to root in order to be used by docker
    cp "$GIT_SSH_FILE" "$current_working_dir"
    log_info " > [DOCKER]: Successfully Copied [OK]"
else
    echo -e " > [DOCKER]: SSH $DEFAULT_SSH_FILE_ID already located in root."
    log_info " > [DOCKER]: Nothing to do! [OK]\n"
fi
echo -e " ------------------------------------------------------------"

# set the repo path variable use at docker-compose file.
export REPO_TO_DEPLOY="$REPO_PATH_TO_DEPLOY"

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