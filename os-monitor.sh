#!/bin/bash

# import other libraries
source ./utils/logging_utils.sh

# ----------------------------------------------------------------------
# Script definitions
# ----------------------------------------------------------------------

TOOL_NAME="os-monitor"
TOOLS_USER="servertool"

TOOLS_ROOT_DIR=/opt/linux-server-tools
OS_MONITOR_DIR=$TOOLS_ROOT_DIR/os-monitor
OS_MONITOR_OUT_DIR=$OS_MONITOR_DIR/out

OS_MONITOR_MEM_CSV_FILE=$OS_MONITOR_OUT_DIR/_mem-info.csv

DISK_CSV_TITLES="Drive,Total,Used,Available,Use,Mount,Date,Time,Hostname,IP"

CLEAN_OUTPUT=false

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
while getopts "hc" option; do
    case "$option" in
        c) CLEAN_OUTPUT=true ;;
        h) usage ;;
        *) usage ;;
    esac
done
echo "" # new line

# user validation
# ----------------------------------------------------------------------
log " > [$TOOL_NAME]: Validating Tools User '$TOOLS_USER'..."
log "------------------------------------------------------------"

USER_EXISTS_RES=$(grep -c "^$TOOLS_USER:" /etc/passwd)

if [ $USER_EXISTS_RES -eq 0 ]; then
    handle_error "User '$TOOLS_USER' does not exist. Please create it."
else
    log_info " > [$TOOL_NAME]: User '$TOOLS_USER' exists [OK]"
    log ""
fi

# create directory structure (if not exists)
# ----------------------------------------------------------------------
log " > [$TOOL_NAME]: Validating Directory Structure..."
log "------------------------------------------------------------"
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

# check if cleaning output directory
# ----------------------------------------------------------------------
if [ "$CLEAN_OUTPUT" = true ]; then
    log_warning " --------------------------------------------"
    log_warning " > [$TOOL_NAME]: Clean Output selected!"
    log_warning " > DIR: $OS_MONITOR_OUT_DIR"
    log_warning " --------------------------------------------"
    log ""
    read -p " > Are you sure you want to continue? [Y/y]" -n 1 -r
    echo    # (optional) move to a new line
    log ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log " > Removing contents from: '$OS_MONITOR_OUT_DIR/*'"
        # this syntax is for shellcheck: SC2115
        rm -rf "${OS_MONITOR_OUT_DIR:?}/"*
        log " > Removed! [OK]"
        log ""
    else
        log "Skipping Clean Output..."
        log ""
    fi
fi

# date time data
# ----------------------------------------------------------------------
xTIME=$(date +"%H-%M-%S")
xTIME_FMT=$(date +"%H:%M:%S")
xDATE=$(date +"%m-%d-%Y")
xDATE_SUMMARY=$(date +"%b-%d-%Y__%Z")
DATE_FORMAT="$xDATE""__$xTIME""__$xDATE_SUMMARY"

# Other meta data
# ----------------------------------------------------------------------
THIS_IP=$(hostname -i | awk '{print $1}')
THIS_HOSTNAME=$(hostname)

# get os metadata
# ----------------------------------------------------------------------

log " > [$TOOL_NAME]: Getting Disk Space info..."
log "------------------------------------------------------------"

FILE_NAME_DISK="$TOOL_NAME""__disk__""$DATE_FORMAT.txt"

df -h | grep "^/dev/s" > $OS_MONITOR_OUT_DIR/$FILE_NAME_DISK

log_fine " > [$TOOL_NAME]: disk space info to file: '$FILE_NAME_DISK'..."
log ""
log " > [$TOOL_NAME]: Getting Memory info..."
log "------------------------------------------------------------"

FILE_NAME_MEM="$TOOL_NAME""__mem__""$DATE_FORMAT.txt"

free -ht > $OS_MONITOR_OUT_DIR/$FILE_NAME_MEM

log_fine " > [$TOOL_NAME]: memory info to file: '$FILE_NAME_MEM'..."
log ""
log_info " > [$TOOL_NAME]: OS Metadata successfully retrieved! [OK]"
log ""

# start CSV Generation
# ----------------------------------------------------------------------
log " > [$TOOL_NAME]: Starting CSV Generation..."
log "------------------------------------------------------------"

cat $OS_MONITOR_OUT_DIR/$FILE_NAME_DISK | while read line
do
    # go trough all drives found inside the disk file
    # ----------------------------------------------------------------------
    CURRENT_DRIVE=$(echo $line | awk -F " " '{printf("%s", $1)}')
    CURRENT_DRIVE_VALUES=$(echo $line | awk -F " " '{printf("%s,%s,%s,%s,%s,%s", $1,$2,$3,$4,$5,$6)}')
    DRIVE_ID=$(echo $CURRENT_DRIVE | awk -F "/" '{printf("%s-%s", $2, $3)}')

    DRIVE_CSV_FILE_NAME="_$DRIVE_ID.csv"
    
    if [[ ! -f "$OS_MONITOR_OUT_DIR/$DRIVE_CSV_FILE_NAME" ]]; then
        # CSV file does not exists. generate it.
        echo " > [$TOOL_NAME]: Generating '$DRIVE_CSV_FILE_NAME'..."
        echo $DISK_CSV_TITLES >> $OS_MONITOR_OUT_DIR/$DRIVE_CSV_FILE_NAME
    fi

    # ----------------------------------------------------------------------
    # Append ALL CSV values that should be in the generated file.
    # attach more values / variable in here in case of needed.
    # ----------------------------------------------------------------------
    DRIVE_CSV_VALUES="$CURRENT_DRIVE_VALUES,$xDATE,$xTIME_FMT,$THIS_HOSTNAME,$THIS_IP"

    log " > Writing values to CSV file: '$DRIVE_CSV_FILE_NAME'"
    log ""
    echo $DRIVE_CSV_VALUES >> $OS_MONITOR_OUT_DIR/$DRIVE_CSV_FILE_NAME
done
log ""

# change directory permissions
# ----------------------------------------------------------------------
log " > [$TOOL_NAME]: Changing Directory permissions to user '$TOOLS_USER'"
log "------------------------------------------------------------"

chown -R $TOOLS_USER:$TOOLS_USER $TOOLS_ROOT_DIR

log ""
log_info "==================================================================="
log_info " > [$TOOL_NAME]: Successfully Executed! [OK]"
log_info "==================================================================="
log ""