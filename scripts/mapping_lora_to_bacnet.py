import json
import os

import requests

CWD = os.getcwd()
bacnet_file = f"{CWD}/bacnet.json"
lora_file = f"{CWD}/lora.json"
host = '123.209.71.183'
port = '1919'
url = f'http://{host}:{port}/api/mappings/lp_gbp'
count = 0
test_run = False
with open(bacnet_file) as f1, open(lora_file) as f2:
    bacnet = json.load(f1)
    lora = json.load(f2)
    for devices in lora:
        points = devices.get("points")
        device_name = devices.get("name")
        for point in points:
            count = count + 1
            name = point.get("name")
            uuid = point.get("uuid")
            point_name = f"{device_name}_{name}"
            # print(f"{uuid}_{name}")
            for i in bacnet:
                object_name = i.get("object_name")
                bacnet_uuid = i.get("uuid")
                if point_name == object_name:
                    body = {
                        "lora_point_uuid": uuid,
                        "bacnet_point_uuid": bacnet_uuid,
                        "lora_point_name": point_name,
                        "bacnet_point_name": object_name
                    }
                    if not test_run:
                        result = requests.post(url,
                                               headers={'Content-Type': 'application/json'},
                                               json=body)
                        print(result.status_code)
                        # print(result.json())
                    print(point_name)

print(count)