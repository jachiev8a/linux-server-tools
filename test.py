import json


def read_config_file(path):
    # type: () -> dict
    with open(path) as file_obj:
        json_config = json.load(file_obj)
    return json_config

config = read_config_file('./disk-config.json')

a = config['servers']
for b in a:
    l = b
print(a)
x = 0
