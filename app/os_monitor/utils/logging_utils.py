#!/usr/bin/env python
# coding=utf-8
"""
Module for main logging properties for all scripts
and also main setup configuration
"""
import logging
import os

LOGGING_FORMAT_CONSOLE = '%(asctime)s | %(module)-24s |: [%(levelname)s] -> %(message)s'
# LOGGING_FORMAT_FILE_1 = '%(asctime)s | %(filename)s-%(funcName)s() [ln:%(lineno)s] | : [%(levelname)s] -> %(message)s'
LOGGING_FORMAT_FILE = '%(asctime)s | [%(levelname)s]: %(module)s.%(funcName)s() [ln:%(lineno)s] | > %(message)s'

# this module file path references
THIS_MODULE_ROOT_DIR = os.path.dirname(__file__)
SCRIPTS_ROOT_DIR = os.path.dirname(THIS_MODULE_ROOT_DIR)
LOGS_OUTPUT_DIR = os.path.normpath(os.path.join(SCRIPTS_ROOT_DIR, 'logs'))

# main logging levels used
LOGGING_LEVELS = {
    'off': logging.NOTSET,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


def setup_logger(
        logger_object,
        log_level_console='warning',
        log_level_file='debug',
        log_file_name=None):
    # type: (logging.Logger, str, str, str) -> None
    """Setup the logger object previously instanced at the scripts.
    Configures the logger level for console output and file handler.

    usage:
        my_logger = logging.getLogger(os.path.basename(__file__))
        setup_logger(my_logger)

    :param logger_object: logger object previously instanced.

    :param log_level_console: logging level for the console output
        options: [ error > warning > info > debug > off ]

    :param log_level_file: logging level for the file output
        options: [ error > warning > info > debug > off ]

    :param log_file_name: name to be given to the generated log file.
    """

    # main attributes for the class
    # -------------------------------------------------
    logger_object.setLevel(logging.DEBUG)
    logger_level_console = None
    logger_level_file = None

    # default name given (logger_name.log)
    logger_file_name = logger_object.name + '.log'  # default value

    # log file custom configuration (if given)
    if log_file_name is not None:
        logger_file_name = log_file_name + '.log'

    logger_file_path = os.path.normpath(os.path.join(LOGS_OUTPUT_DIR, logger_file_name))

    # validate both logging levels (Console & File)
    # -------------------------------------------------

    # Console
    # ------------
    if log_level_console not in LOGGING_LEVELS.keys():
        raise ValueError("Console Logging level not valid: '{}'".format(log_level_console))
    else:
        logger_level_console = LOGGING_LEVELS[log_level_console]

    # File
    # ------------
    if log_level_file not in LOGGING_LEVELS.keys():
        raise ValueError("Console Logging level not valid: '{}'".format(log_level_file))
    else:
        logger_level_file = LOGGING_LEVELS[log_level_file]

    # generate logs directory (if it does not exist)
    if not os.path.exists(LOGS_OUTPUT_DIR):
        os.mkdir(LOGS_OUTPUT_DIR)

    # create formatter
    # -------------------------------------------------
    log_format_console = logging.Formatter(LOGGING_FORMAT_CONSOLE)
    log_format_file = logging.Formatter(LOGGING_FORMAT_FILE)

    # create handler for console output
    # -------------------------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format_console)
    console_handler.setLevel(logger_level_console)
    logger_object.addHandler(console_handler)

    # create handler for file output
    # -------------------------------------------------
    file_handler = logging.FileHandler(logger_file_path)
    file_handler.setFormatter(log_format_file)
    file_handler.setLevel(logger_level_file)
    logger_object.addHandler(file_handler)

    logger_object.debug("['{}'] Logger Started [OK]".format(logger_object.name))


# -------------------------------------------------------------
# LOGGER CLASS OPTION (Not used, but remains as reference)
# -------------------------------------------------------------
class LoggerClass(logging.getLoggerClass()):
    """Class for general python logging purposes
    """

    def __init__(self, name, log_level_console='warning', log_level_file='debug'):

        # main attributes for the class
        # -------------------------------------------------
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        self._logger_name = name

        self._log_level_CONSOLE = None
        self._log_level_FILE = None

        self._log_format = None
        self._console_handler = None
        self._file_handler = None

        # validate both logging levels (Console & File)
        # -------------------------------------------------

        # Console
        if log_level_console not in LOGGING_LEVELS.keys():
            raise ValueError("Console Logging level not valid: '{}'".format(log_level_console))
        else:
            self._log_level_CONSOLE = LOGGING_LEVELS[log_level_console]

        # File
        if log_level_file not in LOGGING_LEVELS.keys():
            raise ValueError("Console Logging level not valid: '{}'".format(log_level_file))
        else:
            self._log_level_FILE = LOGGING_LEVELS[log_level_file]

        # create formatter
        # -------------------------------------------------
        self._log_format_CONSOLE = logging.Formatter(LOGGING_FORMAT_CONSOLE)
        self._log_format_FILE = logging.Formatter(LOGGING_FORMAT_FILE)

        # create handler for console output
        # -------------------------------------------------
        self._console_handler = logging.StreamHandler()
        self._console_handler.setFormatter(self._log_format_CONSOLE)
        self._console_handler.setLevel(self._log_level_CONSOLE)
        self._logger.addHandler(self._console_handler)

        # create handler for file output
        # -------------------------------------------------
        self._file_handler = logging.FileHandler('javier-logs.log')
        self._file_handler.setFormatter(self._log_format_FILE)
        self._file_handler.setLevel(self._log_level_FILE)
        self._logger.addHandler(self._file_handler)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)
