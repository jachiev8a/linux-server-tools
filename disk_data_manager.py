# coding=utf-8
"""
Module disk data manager
"""

import csv
import logging

# main logger instance
LOGGER = logging.getLogger(__name__)

CSV_POSITION_DRIVE_NAME = 0
CSV_POSITION_TOTAL_SIZE = 1
CSV_POSITION_CURRENT_SIZE = 2
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

CSV_FILES_PATH = "/opt/linux-server-tools/os-monitor/out/"


def get_date_labels():
    labels = get_y_values()
    date_labels = []
    for label in labels:
        date_without_month = label[2:]
        month_name = MONTHS[label[:2]]
        named_date = "{}{}".format(month_name, date_without_month)
        date_labels.append(named_date)
    return date_labels
    

def get_x_values():
    csv_rows = __parse_csv_content('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv')
    labels_list = []
    for row in csv_rows:
        label_value = row[CSV_POSITION_DATE].replace('-', '/')
        LOGGER.debug("Current Date Value: '{}'".format(label_value))
        labels_list.append(label_value)
    return labels_list


def get_y_values():
    csv_rows = __parse_csv_content('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv')
    value_list = []
    for row in csv_rows:
        int_value = float(row[CSV_POSITION_CURRENT_SIZE].replace('M', '').replace('G', ''))
        LOGGER.debug("Current Size value retrieved: '{}'".format(int_value))
        value_list.append(int_value)
    return value_list


def get_max_value():
    csv_rows = __parse_csv_content('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv')
    for row in csv_rows:
        max_size_value = float(row[CSV_POSITION_TOTAL_SIZE].replace('M', '').replace('G', ''))
        LOGGER.debug("Max Drive size retrieved: '{}'".format(max_size_value))
        return max_size_value


def get_drive_name():
    csv_rows = __parse_csv_content('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv')
    for row in csv_rows:
        drive_name = row[CSV_POSITION_DRIVE_NAME]
        LOGGER.debug("Drive name retrieved: '{}'".format(drive_name))
        return drive_name


def __parse_csv_content(csv_file):
    LOGGER.info("Parsing CSV file: '{}'".format(csv_file))
    with open(csv_file, 'r') as file_obj:
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
