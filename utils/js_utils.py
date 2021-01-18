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

# main logger instance
LOGGER = logging.getLogger(__name__)


class JsValue(object):
    """"""

    def __init__(self, value, quoted_value=False):
        """"""
        self._value = value
        self._is_quoted = quoted_value

    def __str__(self):
        return self._value

    @property
    def value(self):
        # type: () -> str
        return self._value

    @property
    def is_quoted(self):
        # type: () -> bool
        return self._is_quoted
