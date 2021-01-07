
import csv

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
    labels = get_labels()
    date_labels = []
    for label in labels:
        date_without_month = label[2:]
        month_name = MONTHS[label[:2]]
        named_date = "{}{}".format(month_name, date_without_month)
        date_labels.append(named_date)
    return date_labels
    

def get_labels():
    with open('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv', 'r') as file_obj:
        csv_reader = csv.reader(file_obj, delimiter=',')
        line_count = 0
        labels_list = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                label_value = row[CSV_POSITION_DATE].replace('-', '/')
                print("val: {}".format(label_value))
                labels_list.append(label_value)
                line_count += 1
        return labels_list


def get_values():
    with open('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv', 'r') as file_obj:
        csv_reader = csv.reader(file_obj, delimiter=',')
        line_count = 0
        value_list = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                int_value = float(row[CSV_POSITION_CURRENT_SIZE].replace('M', '').replace('G', ''))
                print("val: {}".format(int_value))
                value_list.append(int_value)
                line_count += 1
        return value_list


def get_max_value():
    with open('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv', 'r') as file_obj:
        csv_reader = csv.reader(file_obj, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                int_value = float(row[CSV_POSITION_TOTAL_SIZE].replace('M', '').replace('G', ''))
                print("MAX: {}".format(int_value))
                return int_value


def get_drive_value():
    with open('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv', 'r') as file_obj:
        csv_reader = csv.reader(file_obj, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                drive_value = row[CSV_POSITION_DRIVE_NAME]
                print("drive: {}".format(drive_value))
                return drive_value
