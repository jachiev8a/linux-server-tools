#!/bin/bash

export SERVER_TOOLS_ROOT_DIR="/var/lib/server-tools"
export SERVER_TOOLS_REPO_DIR="$SERVER_TOOLS_ROOT_DIR/repository"
export SERVER_TOOLS_OS_MONITOR_ROOT="$SERVER_TOOLS_ROOT_DIR/os-monitor"
export SERVER_TOOLS_OS_MONITOR_OUTPUT="$SERVER_TOOLS_OS_MONITOR_ROOT/out"
export SERVER_TOOLS_LOGS_DIR="$SERVER_TOOLS_ROOT_DIR/logs"

export SERVER_TOOLS_USER="servertool"

# configuration in case of running at jenkins deployment
export JENKINS_USER="jenkins"