import json
import os

import requests

CWD = os.getcwd()
bacnet_file = f"{CWD}/bacnet.json"  # bacnet json export from wires-plat
modbus_file = f"{CWD}/modbus_devices.json"  # devices (not network) json export from wires-plat
host = '123.209.71.183'
port = '1515'
url = f'http://{host}:{port}/api/mappings/mp_gbp'
RUBIX_NETWORK_NAME = "IAQ"
test_run = False
count = 0
with open(bacnet_file) as f1, open(modbus_file) as f2:
    bacnet = json.load(f1)
    mb = json.load(f2)
    for devices in mb:
        points = devices.get("points")
        device_name = devices.get("name")
        for point in points:
            name = point.get("name")
            uuid = point.get("uuid")
            point_name = f"{RUBIX_NETWORK_NAME}_{device_name}_{name}"
            count = count + 1
            for i in bacnet:

                object_name = i.get("object_name")
                bacnet_uuid = i.get("uuid")
                if point_name == object_name:
                    body = {
                        "modbus_point_uuid": uuid,
                        "bacnet_point_uuid": bacnet_uuid,
                        "modbus_point_name": point_name,
                        "bacnet_point_name": object_name
                    }
                    if not test_run:
                        result = requests.post(url,
                                               headers={'Content-Type': 'application/json'},
                                               json=body)
                        print(result.status_code)
                        print(result.json)
                    print(body)
print(count)