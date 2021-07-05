import json
import os

import requests

CWD = os.getcwd()
bacnet_file = f"{CWD}/bacnet.json"
host = '123.209.71.183'
port = '1717'
url = f'http://{host}:{port}/api/bacnet/points'


def clean_string(val: str) -> str:
    val = val.replace(' ', '_')
    val = val.replace('__', '_')
    return val


test_run = False
clean_name = False
count = 0
with open(bacnet_file) as json_file:
    data = json.load(json_file)
    for point in data:
        count = count + 1
        point_name = point.get("object_name")
        if clean_name:
            point_name = point_name.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"})
            point_name = clean_string(point_name)
        new_point_name = f"{point_name}"
        new_point_name = clean_string(new_point_name)
        point_obj = {
            "object_type": "analogOutput",
            "object_name": new_point_name,
            "use_next_available_address": True,
            "relinquish_default": 1,
            "priority_array_write": {
                "_1": None,
                "_2": None,
                "_3": None,
                "_4": None,
                "_5": None,
                "_6": None,
                "_7": None,
                "_8": None,
                "_9": None,
                "_10": None,
                "_11": None,
                "_12": None,
                "_13": None,
                "_14": None,
                "_15": None,
                "_16": None
            },
            "event_state": "lowLimit",
            "units": "noUnits",
            "description": "description",
            "enable": True,
            "fault": False,
            "data_round": 0,
            "data_offset": 0

        }
        if not test_run:
            # if count > 5:
            #     break
            result = requests.post(url,
                                   headers={'Content-Type': 'application/json'},
                                   json=point_obj)
            print(result.status_code)
        print(new_point_name)
print(count)
