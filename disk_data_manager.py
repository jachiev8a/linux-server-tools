
import csv


def get_labels():
    with open('/opt/linux-server-tools/os-monitor/out/_dev-sda.csv', 'r') as file_obj:
        csv_reader = csv.reader(file_obj, delimiter=',')
        line_count = 0
        labels_list = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                label_value = row[6].replace('-', '/')
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
                int_value = float(row[2].replace('M', '').replace('G', ''))
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
                int_value = float(row[1].replace('M', '').replace('G', ''))
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
                drive_value = row[0]
                print("drive: {}".format(drive_value))
                return drive_value
