# coding=utf-8
"""
Module disk data manager
"""

import csv
import logging
import os
import glob
import json
from typing import *
from collections import OrderedDict

# main logger instance
LOGGER = logging.getLogger(__name__)

CSV_POSITION_FILESYSTEM_NAME = 0
CSV_POSITION_TOTAL_SIZE = 1
CSV_POSITION_CURRENT_SIZE = 2
CSV_POSITION_IN_USE_SIZE = 4
CSV_POSITION_MOUNTED_PATH = 5
CSV_POSITION_DATE = 6
CSV_POSITION_TIME = 7
CSV_POSITION_SERVER_NAME = 8
CSV_POSITION_SERVER_IP = 9

MOUNT_ID_ROOT = 'root'

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


####################################################################################################
class DataDiskManager(object):
    """"""

    def __init__(self, source_data_path, disk_config_file):
        # type: (str, str) -> None
        """"""
        self._source_data_path = source_data_path
        self._server_disk_config = ServerDiskConfig(disk_config_file)
        self._disks = OrderedDict()  # type: Dict[str, DataDisk]

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

            # validate if the server related to the disk data
            # is found in the configuration file.
            if self._is_server_found(new_disk):

                # if the server is defined. Search for all defined disks in config.
                # if the disk is found, the disk is loaded into the manager.
                if self._is_disk_found(new_disk):
                    self._disks[new_disk.uid] = new_disk

            else:
                # server is not in config. All disks are loaded.
                self._disks[new_disk.uid] = new_disk

        if not bool(self.disks):
            error_msg = "Source Data Path does not have files in it: '{}'".format(self._source_data_path)
            LOGGER.error(error_msg)
            raise Exception(error_msg)

    def _is_server_found(self, disk):
        # type: (DataDisk) -> bool
        """"""
        # check if the server name matches the server defined in the config file
        server_found = self._server_disk_config.get_server_by_name(disk.server.name)
        if server_found is not None:
            return True
        return False

    def _is_disk_found(self, disk):
        # type: (DataDisk) -> bool
        """"""
        # check if the server name matches the server defined in the config file
        if self._is_server_found(disk):
            server_obj = self._server_disk_config.get_server_by_name(disk.server.name)
            if disk.mount_id in server_obj.disk_names:
                return True
        return False

    def get_max_disk_size(self):
        # type: () -> float
        """Returns the max size value found from checking all loaded disks
        into the disk manager object.

        :return: the max sized disk value
        """
        max_values_list = []  # type: List[float]
        for disk in self._disks.values():
            max_values_list.append(disk.total_size)
        return max(max_values_list)

    def get_server_name(self):
        # type: () -> str
        """Returns the server name related to all disks
        """
        return list(self._disks.values())[0].server.name

    def get_server_ip(self):
        # type: () -> str
        """Returns the server name related to all disks
        """
        return list(self._disks.values())[0].server.ip

    @property
    def disks(self):
        # type: () -> Dict[str, DataDisk]
        return self._disks

    @property
    def source_data_path(self):
        # type: () -> str
        return self._source_data_path


####################################################################################################
class DataDisk(object):
    """"""

    class DiskDataValue(object):
        """"""

        def __init__(self, date, size_value, in_use_value):
            # type: (str, float, str) -> None
            self._date = date  # type: str
            self._size = size_value  # type: float
            self._in_use = in_use_value  # type: str

        @property
        def date(self):
            # type: () -> str
            return self._date

        @property
        def size(self):
            # type: () -> float
            return self._size

        @property
        def in_use(self):
            # type: () -> str
            return self._in_use

    def __init__(self, csv_file):
        # type: (str) -> None
        """
        :param csv_file:
        """
        self._csv_file = csv_file

        # static non-changeable values
        self._uid = None
        self._filesystem_name = None
        self._total_size = 0.0  # type: float
        self._mounted_path = None
        self._mount_id = None
        self._server = None

        # list of raw values retrieved from csv
        self._csv_raw_values = []

        # listed variable values
        self._disk_data_values = OrderedDict()

        self._csv_raw_values = self.__parse_csv_content()
        self._build_disk_from_content()

        LOGGER.debug("Data Disk Loaded! '{}'".format(self._filesystem_name))

    def _build_disk_from_content(self):

        # CSV DATA: filesystem name
        self._filesystem_name = self._csv_raw_values[0][CSV_POSITION_FILESYSTEM_NAME]
        LOGGER.debug("Drive name retrieved: '{}'".format(self._filesystem_name))

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
        self._uid = self._mount_id

    def get_last_disk_data_value(self):
        # type: () -> DataDisk.DiskDataValue
        return list(self.disk_data_values.values())[-1]

    def is_root_disk(self):
        # type: () -> bool
        if self._mount_id == MOUNT_ID_ROOT:
            return True
        return False

    def _get_mount_id(self):
        # type: () -> str
        if self._mounted_path == '/':
            mount_id = MOUNT_ID_ROOT
        else:
            mount_id = self._mounted_path.replace('/', '-')[1:]
        return mount_id

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

    def __str__(self):
        # type: () -> str
        return self._filesystem_name

    @property
    def uid(self):
        # type: () -> str
        return self._uid

    @property
    def filesystem_name(self):
        # type: () -> str
        return self._filesystem_name

    @property
    def total_size(self):
        # type: () -> float
        return self._total_size

    @property
    def mounted_path(self):
        # type: () -> str
        return self._mounted_path

    @property
    def mount_id(self):
        # type: () -> str
        """Returns the id given to a mounted path of the disk partition.
        If it is root partition, this id will return 'root' string.
        If not, it will return the same path as 'mounted_path' attribute.
        """
        return self._mount_id

    @property
    def server(self):
        # type: () -> Server
        return self._server

    @property
    def disk_data_values(self):
        # type: () -> Dict[str, DataDisk.DiskDataValue]
        return self._disk_data_values


####################################################################################################
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


####################################################################################################
class ServerDiskConfig(object):
    """"""

    class ServerDiskObject(object):
        """"""

        def __init__(self, server_name, disks):
            # type: (str, list[str]) -> None
            self._name = server_name  # type: str
            self._disk_names = disks  # type: list[str]

        @property
        def name(self):
            # type: () -> str
            return self._name

        @property
        def disk_names(self):
            # type: () -> list[str]
            return self._disk_names

    def __init__(self, config_file_path):
        """"""
        self._servers = {}  # type: Dict[str, ServerDiskConfig.ServerDiskObject]
        self._config_file_path = config_file_path
        self._configuration = self._read_config_file()
        self._parse_configuration()

    def _read_config_file(self):
        # type: () -> dict
        with open(self._config_file_path) as file_obj:
            json_config = json.load(file_obj)
        return json_config

    def server_exists(self, server_name):
        # type: (str) -> bool
        return bool([server for server in self._servers.values() if server.name == server_name])

    def get_server_by_name(self, server_name):
        # type: (str) -> ServerDiskConfig.ServerDiskObject
        if self.server_exists(server_name):
            return self._servers[server_name]

    def _parse_configuration(self):
        # type: () -> None
        for server_config in self._configuration['servers']:
            server_name = server_config['name']
            disk_list = server_config['disks']
            new_server = ServerDiskConfig.ServerDiskObject(server_name, disk_list)
            self._servers[new_server.name] = new_server

    @property
    def servers(self):
        # type: () -> Dict[str, ServerDiskConfig.ServerDiskObject]
        return self._servers
