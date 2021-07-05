import json
import requests


# payload = {"username": "admin", "password": "N00BWires"}
# get_token = requests.post(f"http://{host}:{port}/api/users/login", json=payload)
# res = get_token.json()
# access_token = res.get('access_token')
# print(access_token)
host = '0.0.0.0'
port = '1717'
url = f'http://{host}:{port}/api/bacnet/points'


device_start_address = 1
sensors = [
    "9EAB96B4",
    "8AAB95D2",
]

sensors_voc = [
    "1003-VOC",
    "1018-VOC",
    "B03-VOC",
    "G002-VOC",
]


point_names = ['temp', 'humidity']

device_count = len(sensors)
is_looping = True
for i in range(device_count):
    for ii, r in enumerate(point_names):
        name = f"{sensors[i]}_{r}".replace('-', '_')
        point_obj = {
            "object_type": "analogOutput",
            "object_name": name,
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
        result = requests.post(url,
                               headers={'Content-Type': 'application/json'},
                               json=point_obj)
        print(result.status_code)

    # print(f"iot_{reg_address[i]}")


