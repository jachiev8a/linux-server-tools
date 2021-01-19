# coding=utf-8
"""
Module disk data manager
"""

import csv
import logging
import os
import glob
from collections import OrderedDict

# custom libs
from utils.disk_data_manager import *
from utils.js_utils import JsValue

# main logger instance
LOGGER = logging.getLogger(__name__)


BG_COLORS = [
    "rgba(151, 187, 205, 0.3)",     # Light Blue
    "rgba(238, 133, 133, 0.3)",     # Light Red
    "rgba(187, 143, 206, 0.3)",     # dark purple
    "rgba(255, 255, 128, 0.3)",     # yellow
]

BORDER_COLORS = [
    "rgba(151, 187, 205, 1)",       # Light Blue
    "rgba(238, 133, 133, 1)",       # Light Red
    "rgba(187, 143, 206, 1)",       # dark purple
    "rgba(255, 255, 128, 1)",       # yellow
]

POINT_BG_COLORS = [
    "rgba(151, 187, 205, 1)",       # Light Blue
    "rgba(238, 133, 133, 1)",       # Light Red
    "rgba(187, 143, 206, 1)",       # dark purple
    "rgba(255, 255, 128, 1)",       # yellow
]

POINT_BORDER_COLORS = [
    "#fff",                         # Black
    "#fff",                         # Black
    "#fff"                          # Black
    "#fff",                         # Black
]

POINT_HOVER_BG_COLORS = [
    "rgba(151, 187, 205, 1)",       # Light Blue
    "rgba(238, 133, 133, 1)",       # Light Red
    "rgba(187, 143, 206, 1)",       # dark purple
    "rgba(255, 255, 128, 1)",       # yellow
]

POINT_HOVER_BORDER_COLORS = [
    "#fff",                         # Black
    "#fff",                         # Black
    "#fff",                         # Black
    "#fff",                         # Black
]

BORDER_WIDTH = 4

# definition for bar chart for disk usage
BAR_CHART_COLORS = [
    "rgba(38, 194, 129, 1)",        # Light Green (current)
    "rgba(151, 187, 205, 1)",       # Light Blue (total)
]

BAR_CHART_LABELS = [
    "Current",
    "Total",
]


class DiskChartJsManager(object):
    """"""

    def __init__(self):
        """"""
        # DataDisk container
        self._disks = OrderedDict()

        # Chart JS Line charts for disk objects
        self._disk_line_charts = OrderedDict()
        self._disk_line_chart_labels = set()

        # Chart JS Bar charts for disk objects
        self._disk_bar_charts = OrderedDict()

        self._load_index = 0

    def load_disk(self, disk):
        # type: (DataDisk) -> None
        """"""
        # load raw disk object in container
        self._disks[disk.name] = disk

        # create an abstraction object for the disk data.
        # into a ChartJs Line object.
        disk_line_chart_obj = DiskLineChartJs(disk, self._load_index)
        self._disk_line_charts[disk.uid] = disk_line_chart_obj

        # create an abstraction object for the disk data.
        # into a ChartJs Bar object.
        # (There should only be 1 main chart created for this)
        if not bool(self._disk_bar_charts):
            disk_bar_chart_current = DiskBarChartJs(disk, 0)
            disk_bar_chart_total = DiskBarChartJs(disk, 1)
            self._disk_bar_charts['current'] = disk_bar_chart_current
            self._disk_bar_charts['total'] = disk_bar_chart_total

        self._disk_line_chart_labels = disk_line_chart_obj.labels

    @property
    def line_chart_labels(self):
        # type: () -> set
        return self._disk_line_chart_labels

    @property
    def disks(self):
        return self._disks

    @property
    def disk_line_charts(self):
        # type: () -> dict
        return self._disk_line_charts


class DiskLineChartJs(object):
    """"""

    def __init__(self, disk, index):
        # type: (DataDisk, int) -> None
        """"""
        self._disk = disk

        self._labels = []
        self._dataset_data = []
        self._dataset = None
        self._chart_index = index
        self._data_placeholder = "line_chart_data_placeholder{}".format(self._disk.uid)

        self._abstract_disk_data(disk)

    def _abstract_disk_data(self, disk):
        # type: (DataDisk) -> None
        """Retrieve metadata from disk object (DataDisk) in order to build
        the metadata for a Disk ChartJs Object (datasets... etc)

        :param disk: (DataDisk) disk object to get the data from.
        :return:
        """
        for disk_value in disk.disk_data_values.values():
            self._labels.append(disk_value.date)
            self._dataset_data.append(disk_value.size)

        # build custom dataset label id for each disk
        # format: "{disk_name} [{path}]"
        disk_chart_label = "{name} [{mount}]".format(
            name=disk.name,
            mount=disk.mount_id
        )
        self._dataset = ChartJsLineDataset(
            disk_chart_label,
            self._data_placeholder,
            self._chart_index
        )

    @property
    def labels(self):
        return self._labels

    @property
    def dataset(self):
        # type: () -> ChartJsLineDataset
        return self._dataset

    @property
    def dataset_data(self):
        return self._dataset_data

    @property
    def data_placeholder(self):
        return self._data_placeholder


class ChartJsLineDataset(object):
    """"""

    def __init__(self, label_name, data_placeholder_name, index):
        # type: (str, str, int) -> None
        """"""
        self._label = label_name
        self._index = index  # type: int
        self._data_placeholder = data_placeholder_name
        self._definition = self._build_dataset()

    def _build_dataset(self):
        # type: () -> Dict[str, Any]
        """"""
        definition = {
            'label': JsValue(self._label, True),
            'backgroundColor': JsValue(BG_COLORS[self._index], True),
            'borderColor': JsValue(BORDER_COLORS[self._index], True),
            'pointBackgroundColor': JsValue(POINT_BG_COLORS[self._index], True),
            'pointBorderColor': JsValue(POINT_BORDER_COLORS[self._index], True),
            'pointHoverBackgroundColor': JsValue(POINT_HOVER_BG_COLORS[self._index], True),
            'pointHoverBorderColor': JsValue(POINT_HOVER_BORDER_COLORS[self._index], True),
            'borderWidth': JsValue(BORDER_WIDTH, False),
            'data': JsValue(self._data_placeholder, False),
        }
        return definition

    @property
    def label(self):
        # type: () -> str
        return self._label

    @property
    def data_placeholder(self):
        # type: () -> str
        return self._data_placeholder

    @property
    def definition(self):
        # type: () -> Dict[str, Any]
        return self._definition


class DiskBarChartJs(object):
    """"""

    def __init__(self, disk, index):
        # type: (DataDisk, int) -> None
        """"""
        self._disk = disk

        self._labels = []
        self._dataset_data = []
        self._dataset = None
        self._chart_index = index
        self._data_placeholder = "bar_chart_data_placeholder{}".format(self._disk.uid)

        self._abstract_disk_data(disk)

    def _abstract_disk_data(self, disk):
        # type: (DataDisk) -> None
        """Retrieve metadata from disk object (DataDisk) in order to build
        the metadata for a Disk ChartJs Object (datasets... etc)

        :param disk: (DataDisk) disk object to get the data from.
        :return:
        """

        # get the metadata only from the last values from the disk object.
        # 1. last date of the values retrieved
        # 2. last in use value (% value)
        # 3. last disk size measured. (in GB)
        last_date_named_value = disk.get_last_disk_data_value().date
        last_disk_in_use_value = disk.get_last_disk_data_value().in_use
        last_disk_size_value = disk.get_last_disk_data_value().size

        # build the format of the label:
        # {date} (%{in_use_value})
        disk_usage_label = "{} ({})".format(
            last_date_named_value, last_disk_in_use_value)

        self._labels.append(disk_usage_label)
        self._dataset_data.append(last_disk_size_value)

        self._dataset = ChartJsBarDataset(
            BAR_CHART_LABELS[self._chart_index],
            self._data_placeholder,
            self._chart_index
        )

    @property
    def labels(self):
        return self._labels

    @property
    def dataset(self):
        # type: () -> ChartJsLineDataset
        return self._dataset

    @property
    def dataset_data(self):
        return self._dataset_data

    @property
    def data_placeholder(self):
        return self._data_placeholder


class ChartJsBarDataset(object):
    """"""

    def __init__(self, label_name, data_placeholder_name, index):
        # type: (str, str, int) -> None
        """"""
        self._label = label_name
        self._index = index  # type: int
        self._data_placeholder = data_placeholder_name
        self._definition = self._build_dataset()

    def _build_dataset(self):
        # type: () -> Dict[str, Any]
        """"""
        definition = {
            'label': JsValue(self._label, True),
            'backgroundColor': JsValue(BAR_CHART_COLORS[self._index], True),
            'borderColor': JsValue(BAR_CHART_COLORS[self._index], True),
            'data': JsValue(self._data_placeholder, False),
        }
        return definition

    @property
    def label(self):
        # type: () -> str
        return self._label

    @property
    def data_placeholder(self):
        # type: () -> str
        return self._data_placeholder

    @property
    def definition(self):
        # type: () -> Dict[str, Any]
        return self._definition
