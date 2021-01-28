#!flask/bin/python
# coding=utf-8
"""
Main script to manage swarm api with several utils
"""

# core libs
import argparse
import traceback

# flask libs
from flask import Flask
from flask import render_template
from flask import send_file

# custom libs
from utils.disk_data_manager import *
from utils.disk_chart_utils import *
from utils.logging_utils import setup_logger

# main logger instance
LOGGER = logging.getLogger()

# main Flask app call
app = Flask(__name__)

# main application instances (singletons)
DATA_DISK_MANAGER = None
DATA_CHART_MANAGER = None


def get_disk_manager():
    # type: () -> DataDiskManager
    global DATA_DISK_MANAGER
    DATA_DISK_MANAGER = DataDiskManager('/os-monitor/output/', './disk-config.json')
    return DATA_DISK_MANAGER


def get_disk_chart_manager():
    # type: () -> DiskChartJsManager
    global DATA_CHART_MANAGER
    DATA_CHART_MANAGER = DiskChartJsManager()
    return DATA_CHART_MANAGER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/disk')
def line_disk_chart():

    # get disk manager singleton
    disk_manager = get_disk_manager()
    # get disk chart manager singleton
    disk_chart_manager = get_disk_chart_manager()

    for disk in disk_manager.disks.values():
        disk_chart_manager.load_disk(disk)

    return render_template(
        'disk_chart.html',
        chart_manager=disk_chart_manager,
        disk_manager=disk_manager
    )


@app.route('/test')
def test():
    pass


@app.route('/download')
def download_file():
    disk_manager = get_disk_manager()
    # retrieve disk data from CSV
    return send_file(
        "/os-monitor/output/_dev-sdc1.csv",
        attachment_filename='disk.csv',
        as_attachment=True
    )


@app.errorhandler(Exception)
def server_error(err):
    error_list = "{}".format(traceback.format_exc()).split('\n')
    return render_template(
        'errors/error_500.html',
        error_msg=err,
        trace_list=error_list
    )


@app.route('/test/error/500')
def test_error_500():
    error_msg = "This is for testing only. No ERROR 500."
    return render_template('errors/error_500.html', error_msg=error_msg)


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

    # flask app run
    app.run()
