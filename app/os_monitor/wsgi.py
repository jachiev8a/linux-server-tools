#!flask/bin/python
# coding=utf-8
"""
Main script to manage swarm api with several utils
"""

# core libs
import argparse
import logging
import os

# custom libs
from os_monitor.app import server as application
from os_monitor.utils.logging_utils import setup_logger

# main logger instance
LOGGER = logging.getLogger()

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
if __name__ == '__main__':

    # Script Argument Parser
    parser = argparse.ArgumentParser(description='[Flask] app.py')
    parser.add_argument(
        '-l', '--log-level',
        default="info",
        required=False,
        help='debugging script log level '
             '[ critical > error > warning > info > debug > off ]')
    args = parser.parse_args()

    # configure logging properties with configuration given
    setup_logger(
        logger_object=LOGGER,
        log_level_console=args.log_level,
        log_file_name=os.path.basename(__file__)
    )

    application.run(host='0.0.0.0')
