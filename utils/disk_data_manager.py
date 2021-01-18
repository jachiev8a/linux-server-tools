# coding=utf-8
"""
Module disk data manager
"""

import csv
import logging
import os
import glob
from collections import OrderedDict

# main logger instance
LOGGER = logging.getLogger(__name__)

CSV_POSITION_DRIVE_NAME = 0
CSV_POSITION_TOTAL_SIZE = 1
CSV_POSITION_CURRENT_SIZE = 2
CSV_POSITION_IN_USE_SIZE = 4
CSV_POSITION_MOUNTED_PATH = 5
CSV_POSITION_DATE = 6
CSV_POSITION_TIME = 7
CSV_POSITION_SERVER_NAME = 8
CSV_POSITION_SERVER_IP = 9

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


class DataDiskManager(object):
    """"""

    def __init__(self, source_data_path):
        """"""
        self._source_data_path = source_data_path
        self._disks = OrderedDict()
        self._find_disks()

    def _find_disks(self):
        # type: () -> None
        if not os.path.exists(self._source_data_path):
            error_msg = "Source Data Path does not exist! : '{}'".format(self._source_data_path)
            LOGGER.error(error_msg)
            raise Exception(error_msg)
        LOGGER.info("Looking for source data files: '{}'".format(self._source_data_path))

        glob_source_path = os.path.join(self._source_data_path, '*.csv')
        for source_file in glob.glob(glob_source_path):
            LOGGER.debug("Source Data File Found: '{}'".format(source_file))
            new_disk = DataDisk(source_file)
            self._disks[new_disk.name] = new_disk

        if not bool(self.disks):
            error_msg = "Source Data Path does not have files in it: '{}'".format(self._source_data_path)
            LOGGER.error(error_msg)
            raise Exception(error_msg)

    @property
    def disks(self):
        # type: () -> OrderedDict
        return self._disks

    @property
    def source_data_path(self):
        # type: () -> str
        return self._source_data_path


class DataDisk(object):
    """"""

    class DiskDataValue(object):
        """"""

        def __init__(self, date, size_value, in_use_value):
            # type: (str, float, str) -> None
            self._date = date
            self._size = size_value
            self._in_use = in_use_value

        @property
        def date(self):
            return self._date

        @property
        def size(self):
            return self._size

        @property
        def in_use(self):
            return self._in_use

    def __init__(self, csv_file):
        """
        :param csv_file:
        """
        self._csv_file = csv_file

        # static non-changeable values
        self._uid = None
        self._name = None
        self._total_size = None
        self._mounted_path = None
        self._mount_id = None
        self._server = None

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
        self._mount_id = self._get_mount_id()
        LOGGER.debug("Mounted Path retrieved: '{}'".format(self._mounted_path))

        # CSV DATA: server data
        server_name = self._csv_raw_values[0][CSV_POSITION_SERVER_NAME]
        server_ip = self._csv_raw_values[0][CSV_POSITION_SERVER_IP]
        self._server = Server(server_name, server_ip)
        LOGGER.debug("Server data retrieved: '{}' ({})".format(self._server.name, self._server.ip))

        # CSV DATA: data disk values
        for csv_value in self._csv_raw_values:

            raw_date_value = csv_value[CSV_POSITION_DATE]
            date_named_value = self._get_named_date_value(raw_date_value)

            raw_size_value = csv_value[CSV_POSITION_CURRENT_SIZE]
            size_value = self._get_valid_size_number_value(raw_size_value)

            in_use_value = csv_value[CSV_POSITION_IN_USE_SIZE]

            # new disk data value instanced
            new_disk_data_value = DataDisk.DiskDataValue(
                date_named_value,
                size_value,
                in_use_value
            )
            self._disk_data_values[raw_date_value] = new_disk_data_value

        # Unique ID setup
        # it is the same as name, but with underscores: '_'
        self._uid = self._name.replace('/', '_')

    def _get_mount_id(self):
        # type: () -> str
        if self._mounted_path == '/':
            return 'root'
        return self._mounted_path

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
        """"""
        # this is set to (1) as default, because if the value is in MB
        # it is ignored how many MB are there. just rounded to 1GB
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
    def uid(self):
        return self._uid

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
    def mount_id(self):
        return self._mount_id

    @property
    def server(self):
        # type: () -> Server
        return self._server

    @property
    def disk_data_values(self):
        # type: () -> dict[str, DataDisk.DiskDataValue]
        return self._disk_data_values


class Server(object):
    """"""

    def __init__(self, name, ip_address):
        """"""
        self._name = name
        self._ip_address = ip_address

    @property
    def name(self):
        return self._name

    @property
    def ip(self):
        return self._ip_address
