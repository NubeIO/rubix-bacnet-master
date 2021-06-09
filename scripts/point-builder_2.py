import json
import requests

host = '123.209.253.77'
port = '1616'
payload = {"username": "admin", "password": "N00BWires"}
get_token = requests.post(f"http://{host}:{port}/api/users/login", json=payload)
res = get_token.json()
access_token = res.get('access_token')
print(access_token)

url = f'http://{host}:{port}/bacnet/api/bacnet/points'


device_start_address = 1
sensors_sound = [
    "1004",
    "1006",
    "1010",
    "1022",
    "1Q03",
    "2001",
    "2014",
    "2026",
    "2032",
    "2034",
    "2035",
    "2041",
    "2046",
    "2Q03",
    "3006",
    "3021",
    "3030",
    "3034",
    "3035",
    "3037",
    "3040",
    "3047",
    "3Q04",
    "3Q05",
    "3Q07",
    "4008",
    "4030",
    "4035",
    "4036",
    "4041",
    "4042",
    "4Q03",
    "5003",
    "5007",
    "5010",
    "5016",
    "5021",
    "6002",
    "6003",
    "6005",
    "6007",
    "B030",
    "CW00",
    "G001",
    "G003",
    "M004",
    "M010"
    "B07",
    "BO2",
    "BO3",
]

sensors_voc = [
    "1003-VOC",
    "1018-VOC",
    "B03-VOC",
    "G002-VOC",
]


point_names_sound = ['rssi', 'temperature', 'humidity', 'sound-avg', 'sound-peak', "voltage"]
point_names_voc = ['rssi', 'temperature', 'humidity', 'voc', 'voltage']
device_count = len(sensors_sound)
is_looping = True
for i in range(device_count):
    for ii, r in enumerate(point_names_sound):
        name = f"H13_{sensors_sound[i]}_IOT_{r}".replace('-', '_')
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
                               headers={'Content-Type': 'application/json', 'Authorization': '{}'.format(access_token)},
                               json=point_obj)
        print(result.text)

    # print(f"iot_{reg_address[i]}")


