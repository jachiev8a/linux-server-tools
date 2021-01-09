#!flask/bin/python
# coding=utf-8
"""
Main script to manage swarm api with several utils
"""

# core libs
import logging
import os
import argparse

# flask libs
from flask import Flask
from flask import Markup
from flask import render_template

# custom libs
import disk_data_manager
from utils.logging_utils import setup_logger

# main logger instance
LOGGER = logging.getLogger()

# main Flask app call
app = Flask(__name__)


@app.route('/disk')
def line_disk_chart():

    error_msg = disk_data_manager.validate_source_data()
    if error_msg is not None:
        return render_template(
            'errors/error_500.html',
            error_msg=error_msg
        )

    # retrieve disk data from CSV
    date_named_values = disk_data_manager.get_date_named_values()
    disk_size_values = disk_data_manager.get_current_size_values()

    last_date_named_value = date_named_values[-1]
    last_disk_size_value = disk_size_values[-1]

    return render_template(
        'disk_chart.html',
        line_chart_title='Server Disk Usage (Daily)',
        disk_usage_title='Disk Usage (Current)',
        disk_name=disk_data_manager.get_drive_name(),
        disk_total_size=disk_data_manager.get_max_value(),
        line_chart_labels=date_named_values,
        line_chart_values=disk_size_values,
        disk_usage_labels=last_date_named_value,
        disk_usage_values=last_disk_size_value
    )


@app.route('/test/error/500')
def test_error_500():
    error_msg = "This is for testing only. No ERROR 500."
    return render_template('error_500.html', error_msg=error_msg)


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

    app.run(host='0.0.0.0')
