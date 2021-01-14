# coding=utf-8
"""
Module disk data manager
"""

import csv
import logging
import os
from collections import OrderedDict

# main logger instance
LOGGER = logging.getLogger(__name__)

CSV_POSITION_DRIVE_NAME = 0
CSV_POSITION_TOTAL_SIZE = 1
CSV_POSITION_CURRENT_SIZE = 2
CSV_POSITION_IN_USE_SIZE = 4
CSV_POSITION_MOUNTED_PATH = 5
CSV_POSITION_DATE = 6

MONTHS = {
    '01': 'JAN',
    '02': 'FEB',
    '03': 'MAR',
    '04': 'APR',
    '05': 'MAY',
    '06': 'JUN',
    '07': 'JUL',
    '08': 'AUG',
    '09': 'SEP',
    '10': 'OCT',
    '11': 'NOV',
    '12': 'DEC'
}

CSV_FILES_PATH = "/os-monitor/output"
CSV_DISK_FILE = os.path.join(CSV_FILES_PATH, '_dev-sdc1.csv')


def validate_source_data():
    # type: () -> str
    error_msg = None
    if not os.path.exists(CSV_FILES_PATH):
        error_msg = "Source Data Path does not exists! ('{}')".format(CSV_FILES_PATH)
    elif not os.path.exists(CSV_DISK_FILE):
        error_msg = "CSV Source Data file does not exists! ('{}')".format(CSV_DISK_FILE)
    return error_msg


class DataDisk(object):
    """"""

    class DiskDataValue(object):
        """"""

        def __init__(self, date, size_value, in_use_value):
            self.date = date,
            self.size = size_value,
            self.in_use = in_use_value

    def __init__(self, csv_file):
        """
        :param csv_file:
        """
        self._csv_file = csv_file

        # static non-changeable values
        self._name = None
        self._total_size = None
        self._mounted_path = None

        # list of raw values retrieved from csv
        self._csv_raw_values = []

        # listed variable values
        self._disk_data_values = OrderedDict()

        self._csv_raw_values = self.__parse_csv_content()
        self._build_disk_from_content()

        LOGGER.debug("Data Disk Loaded! '{}'".format(self._name))

    def _build_disk_from_content(self):

        # CSV DATA: drive name
        self._name = self._csv_raw_values[0][CSV_POSITION_DRIVE_NAME]
        LOGGER.debug("Drive name retrieved: '{}'".format(self._name))

        # CSV DATA: total size
        csv_value = self._csv_raw_values[0][CSV_POSITION_TOTAL_SIZE]
        self._total_size = self._get_valid_size_number_value(csv_value)
        LOGGER.debug("Max Drive size retrieved: '{}'".format(self._total_size))

        # CSV DATA: mounted path
        self._mounted_path = self._csv_raw_values[0][CSV_POSITION_MOUNTED_PATH]
        LOGGER.debug("Mounted Path retrieved: '{}'".format(self._mounted_path))

        # drive name
        for csv_value in self._csv_raw_values:

            date_raw_value = csv_value[CSV_POSITION_DATE]
            date_named_value = self._get_named_date_value(date_raw_value)

            size_value = csv_value[CSV_POSITION_CURRENT_SIZE]
            in_use_value = csv_value[CSV_POSITION_IN_USE_SIZE]

            # new disk data value instanced
            new_disk_data_value = DataDisk.DiskDataValue(
                date_named_value,
                size_value,
                in_use_value
            )
            self._disk_data_values[date_raw_value] = new_disk_data_value

    def get_last_disk_data_value(self):
        # type: () -> DataDisk.DiskDataValue
        return list(self.disk_data_values.values())[-1]

    @staticmethod
    def _get_named_date_value(date_raw_value):
        # type: (str) -> str
        date_without_month = date_raw_value[2:]
        month_name = MONTHS[date_raw_value[:2]]
        named_date = "{}{}".format(month_name, date_without_month)
        return named_date

    @staticmethod
    def _get_valid_size_number_value(value):
        # type: (str) -> float
        formatted_value = float(1)
        if 'G' in value:
            formatted_value = float(value.replace('M', '').replace('G', ''))
        return formatted_value

    def __parse_csv_content(self):
        # type: () -> list[list[str]]
        if not os.path.exists(self._csv_file):
            LOGGER.error("CSV file does not exists! : '{}'".format(self._csv_file))
        LOGGER.info("Parsing CSV file: '{}'".format(self._csv_file))
        with open(self._csv_file, 'r') as file_obj:
            csv_reader = csv.reader(file_obj, delimiter=',')
            line_count = 0
            value_rows = []
            for row in csv_reader:
                # avoid the first line with all the csv headers
                if line_count == 0:
                    line_count += 1
                else:
                    LOGGER.debug("CSV row parsed: '{}'".format(row))
                    value_rows.append(row)
        return value_rows

    @property
    def name(self):
        return self._name

    @property
    def total_size(self):
        return self._total_size

    @property
    def mounted_path(self):
        return self._mounted_path

    @property
    def disk_data_values(self):
        # type: () -> dict[str, DataDisk.DiskDataValue]
        return self._disk_data_values
