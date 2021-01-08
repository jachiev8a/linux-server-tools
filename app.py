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

app = Flask(__name__)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/disk')
def line_disk_chart():
    line_labels = disk_data_manager.get_date_labels()
    line_values = disk_data_manager.get_current_size_values()
    return render_template(
        'disk_chart.html',
        title='Server Disk Usage (Daily)',
        dataset_name=disk_data_manager.get_drive_name(),
        max=disk_data_manager.get_max_value(),
        labels=line_labels,
        values=line_values
    )


@app.route('/test/500')
def test_error_500():
    return render_template('error_500.html')


@app.route('/bar')
def bar():
    bar_labels=labels
    bar_values=values
    return render_template(
        'bar_chart.html',
        title='Server Disk Usage',
        max=17000,
        labels=bar_labels,
        values=bar_values
    )

@app.route('/pie')
def pie():
    pie_labels = labels
    pie_values = values
    return render_template('pie_chart.html', title='Bitcoin Monthly Price in USD', max=17000, set=zip(values, labels, colors))


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
