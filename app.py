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
from flask import send_file

# custom libs
from disk_data_manager import *
from utils.logging_utils import setup_logger

# main logger instance
LOGGER = logging.getLogger()

# main Flask app call
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/disk')
def line_disk_chart():

    error_msg = validate_source_data()
    if error_msg is not None:
        return render_template(
            'errors/error_500.html',
            error_msg=error_msg
        )

    # retrieve disk data from CSV
    disk = DataDisk('/os-monitor/output/_dev-sdc1.csv')

    last_date_named_value = disk.get_last_disk_data_value().date
    last_disk_in_use_value = disk.get_last_disk_data_value().in_use

    disk_usage_label = "{} ({})".format(last_date_named_value, last_disk_in_use_value)

    return render_template(
        'disk_chart.html',
        line_chart_title='Server Disk Usage (Daily)',
        disk_usage_title='Disk Usage (Current)',
        disk_usage_label=disk_usage_label,
        disk_usage_value=disk.get_last_disk_data_value().size,
        disk_obj=disk
    )


@app.route('/download')
def download_file():
    error_msg = validate_source_data()
    if error_msg is not None:
        return render_template(
            'errors/error_500.html',
            error_msg=error_msg
        )

    # retrieve disk data from CSV
    return send_file(
        "/os-monitor/output/_dev-sdc1.csv",
        attachment_filename='disk.csv',
        as_attachment=True
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
