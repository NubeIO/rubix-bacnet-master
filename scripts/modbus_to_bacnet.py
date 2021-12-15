import json
import os

import requests

CWD = os.getcwd()
print(CWD)
bacnet_file = f"{CWD}/bacnet.json"  # bacnet json export from wires-plat
modbus_file = f"{CWD}/modbus_devices.json"  # devices (not network) json export from wires-plat
host = '192.168.15.10'
port = '1516'
url = f'http://{host}:{port}/api/mappings/mp_gbp/uuid'
RUBIX_NETWORK_NAME = "net-1"
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
            point_name = f"{name}"
            count = count + 1
            for i in bacnet:
                object_name = i.get("object_name")
                bacnet_uuid = i.get("uuid")
                if point_name == object_name:
                    body = {
                        "point_uuid": uuid,
                        "mapped_point_uuid": bacnet_uuid,
                        "type": "BACNET"
                        # "modbus_point_name": point_name,
                        # "bacnet_point_name": object_name
                    }
                    print(body)
                    if not test_run:
                        print(1)
                        result = requests.post(url,
                                               headers={'Content-Type': 'application/json'},
                                               json=body)
                        print(result.status_code)
                        print(result.json)
                    # print(body)
print(count)