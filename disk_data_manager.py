
import csv


def get_labels():
    with open('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv', 'r') as file_obj:
        csv_reader = csv.reader(file_obj, delimiter=',')
        for row in csv_reader:
            labels_list = str(row).split(',')
            break


def get_values():
    with open('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv', 'r') as file_obj:
        csv_reader = csv.reader(file_obj, delimiter=',')
        line_count = 0
        value_list = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                int_value = float(row[2].replace('M', '').replace('G', ''))
                value_list.append(int_value)
                line_count += 1


def get_max_value():
    with open('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv', 'r') as file_obj:
        csv_reader = csv.reader(file_obj, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                int_value = float(row[1].replace('M', '').replace('G', ''))
                return int_value
