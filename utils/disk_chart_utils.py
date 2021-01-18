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
    "rgba(238, 133, 133, 0.2)",     # Light Red
    "rgba(187, 143, 206, 0.2)",     # dark purple
]

BORDER_COLORS = [
    "rgba(151, 187, 205, 1)",       # Light Blue
    "rgba(238, 133, 133, 1)",       # Light Red
    "rgba(187, 143, 206, 1)",       # dark purple
]

POINT_BG_COLORS = [
    "rgba(151, 187, 205, 1)",       # Light Blue
    "rgba(238, 133, 133, 1)",       # Light Red
    "rgba(187, 143, 206, 1)",       # dark purple
]

POINT_BORDER_COLORS = [
    "#fff",                         # Black
    "#fff",                         # Black
    "#fff"  # Black
]

POINT_HOVER_BG_COLORS = [
    "rgba(151, 187, 205, 1)",       # Light Blue
    "rgba(238, 133, 133, 1)",       # Light Red
    "rgba(187, 143, 206, 1)",       # dark purple
]

POINT_HOVER_BORDER_COLORS = [
    "#fff",                         # Black
    "#fff",                         # Black
    "#fff"  # Black
]

BORDER_WIDTH = 4
MAIN_INDEX = 0
MAX_INDEX = len(BG_COLORS)-1


def increment_index():
    global MAIN_INDEX
    global MAX_INDEX
    if MAIN_INDEX < MAX_INDEX:
        MAIN_INDEX = MAIN_INDEX + 1
    else:
        MAIN_INDEX = 0


def get_index():
    global MAIN_INDEX
    return MAIN_INDEX


class DiskChartJsManager(object):
    """"""

    def __init__(self):
        """"""
        self._disks = OrderedDict()
        self._disk_charts = OrderedDict()
        self._chart_labels = set()

    def load_disk(self, disk):
        # type: (DataDisk) -> None
        self._disks[disk.name] = disk

        disk_chart_obj = DiskChartJs(disk)
        self._disk_charts[disk.uid] = disk_chart_obj

        self._chart_labels = disk_chart_obj.labels

    @property
    def chart_labels(self):
        return self._chart_labels

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
        # type: (DataDisk) -> None
        """"""
        self._disk = disk

        self._labels = set()
        self._dataset_data = []
        self._dataset = None
        self._data_placeholder = "data_placeholder{}".format(self._disk.uid)

        self._abstract_disk_data(disk)

    def _abstract_disk_data(self, disk):
        # type: (DataDisk) -> None
        for disk_value in disk.disk_data_values.values():
            self._labels.add(disk_value.date)
            self._dataset_data.append(disk_value.size)

        self._dataset = ChartJsDataset(disk.name, self._data_placeholder)

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

    @property
    def data_placeholder(self):
        return self._data_placeholder


class ChartJsDataset(object):
    """"""

    def __init__(self, label_name, data_placeholder_name):
        """"""
        self._label = label_name
        self._data_placeholder = data_placeholder_name
        self._definition = self._build_dataset()

    def _build_dataset(self):

        index = get_index()

        definition = {
            'label': JsValue(self._label, True),
            'backgroundColor': JsValue(BG_COLORS[index], True),
            'borderColor': JsValue(BORDER_COLORS[index], True),
            'pointBackgroundColor': JsValue(POINT_BG_COLORS[index], True),
            'pointBorderColor': JsValue(POINT_BORDER_COLORS[index], True),
            'pointHoverBackgroundColor': JsValue(POINT_HOVER_BG_COLORS[index], True),
            'pointHoverBorderColor': JsValue(POINT_HOVER_BORDER_COLORS[index], True),
            'borderWidth': JsValue(BORDER_WIDTH, False),
            'data': JsValue(self._data_placeholder, False),
        }

        increment_index()
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
