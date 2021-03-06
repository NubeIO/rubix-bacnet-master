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

device_count = 2
device_start_address = 1
reg_address = [6, 7, 8, 10, 39]
point_names = ['mode', 'fan_status', 'setpoint', 'temp', 'value_position']

is_looping = True
for i in range(device_count):
    i += device_start_address
    print("DEVICE:", i)
    for ii, r in enumerate(reg_address):
        addr = f'{i}{r}'
        addr = int(addr)
        print({"addr": addr, "i": i, "ii": ii, "r": r})

        # print(f'{i}{r}')
        name = point_names[ii]
        point_obj = {
            "object_type": "analogOutput",
            "object_name": f'{name}_{i}_{r}',
            "address": addr,
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

    if not is_looping:
        break
