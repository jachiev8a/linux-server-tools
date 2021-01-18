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
    "rgba(151, 187, 205, 0.2)",     # Light Blue
    "#EE8585"                      # Light Red
]

BORDER_COLORS = [
    "rgba(151, 187, 205, 1)",       # Light Blue
    "#EE8585"                      # Light Red
]

POINT_BG_COLORS = [
    "rgba(151, 187, 205, 1)",       # Light Blue
    "#EE8585"                      # Light Red
]

POINT_BORDER_COLORS = [
    "#fff",                         # Black
    "#fff"                         # Black
]

POINT_HOVER_BG_COLORS = [
    "rgba(151, 187, 205, 1)",       # Light Blue
    "#EE8585"                      # Light Red
]

POINT_HOVER_BORDER_COLORS = [
    "#fff",                         # Black
    "#fff"                         # Black
]

BORDER_WIDTH = 4


class DiskChartJsManager(object):
    """"""

    def __init__(self):
        """"""
        self._disks = OrderedDict()
        self._disk_charts = OrderedDict()

    def load_disk(self, disk):
        # type: (DataDisk) -> None
        self._disks[disk.name] = disk
        self._disk_charts[disk.uid] = DiskChartJs(disk)

    @property
    def disks(self):
        return self._disks

    @property
    def disk_charts(self):
        # type: () -> dict
        return self._disk_charts


class DiskChartJs(object):
    """"""

    def __init__(self, disk):
        """"""
        self._disk = disk

        self._labels = []
        self._dataset_data = []
        self._dataset = None

        self._abstract_disk_data(disk)

    def _abstract_disk_data(self, disk):
        # type: (DataDisk) -> None
        for disk_value in disk.disk_data_values.values():
            self._labels.append(disk_value.date)
            self._dataset_data.append(disk_value.size)

        self._dataset = ChartJsDataset(disk.name, disk.uid)

    @property
    def labels(self):
        return self._labels

    @property
    def dataset(self):
        # type: () -> ChartJsDataset
        return self._dataset

    @property
    def dataset_data(self):
        return self._dataset_data


class ChartJsDataset(object):
    """"""

    def __init__(self, label_name, uid_data):
        """"""
        self._label = label_name
        self._uid_data = uid_data
        self._data_placeholder = "data_placeholder{}".format(self._uid_data)
        self._definition = self._build_dataset()

    def _build_dataset(self):

        definition = {
            'label': JsValue(self._label, True),
            'backgroundColor': JsValue(BG_COLORS[0], True),
            'borderColor': JsValue(BORDER_COLORS[0], True),
            'pointBackgroundColor': JsValue(POINT_BG_COLORS[0], True),
            'pointBorderColor': JsValue(POINT_BORDER_COLORS[0], True),
            'pointHoverBackgroundColor': JsValue(POINT_HOVER_BG_COLORS[0], True),
            'pointHoverBorderColor': JsValue(POINT_HOVER_BORDER_COLORS[0], True),
            'borderWidth': JsValue(BORDER_WIDTH, False),
            'data': JsValue(self._data_placeholder, False),
        }
        return definition

    @property
    def label(self):
        return self._label

    @property
    def data_placeholder(self):
        return self._data_placeholder

    @property
    def definition(self):
        return self._definition
