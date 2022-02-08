import json

import requests

"""
Makes an api call to get all the bacnet devices and updates the device bacnet_mac_address
(Note there was a bug in bacnet-master and in the config file you need to set all the clean_names to false)

run in bacnet-stack ./bin/bacwi
make a text file to and copy paste from the console as per example below
"""

"""
  1760305 0A:11:45:29:BA:C0    0     00                   1476
  1760399 0A:11:45:99:BA:C0    0     00                   1476
  1760436 0A:11:45:BA:BA:C0    0     00                   1476
  1760193 0A:11:44:C5:BA:C0    0     00                   1476
"""


host = '4s.dyndns.ws'
port = '1616'
payload = {"username": "admin", "password": "N00BWires"}
get_token = requests.post(f"http://{host}:{port}/api/users/login", json=payload)
res = get_token.json()
access_token = res.get('access_token')
print(access_token)

# rbm
devices_url = f"http://{host}:{port}/rbm/api/bm/devices/true"
bacnet = requests.get(devices_url,
                      headers={'Content-Type': 'application/json',
                               'Authorization': '{}'.format(access_token)},
                      json="")

bac = bacnet.json()
count = 0

for net in bacnet.json():
    devices = bac.get("devices")
    for d in devices:
        bac_device = d.get("device_object_id")
        uuid = d.get("device_uuid")
        device_name = d.get("device_name")
        bac_device = str(bac_device)
        count += 1
        for line in open("bacnet_stack_whois_text.txt"):
            if line[0].isspace():
                s = line.split()
                le = len(s)
                if le >= 1:
                    device_id = s[0]
                    mac = s[1]
                    snet = s[2]
                    sadr = s[3]
                    if sadr != "00":
                        mac = sadr.replace(":", "")
                        mac = mac.lower()
                        mac = "0x" + mac
                        if bac_device == device_id:
                            if count <= 1000000:
                                print(device_name, bac_device, device_id, mac)
                                device_url = f"http://{host}:{port}/rbm/api/bm/device/{uuid}"
                                payload = {
                                    "device_name": device_name,
                                    "device_enable": True,
                                    "ethernet_mac_address": mac
                                }
                                print(payload)
                                bacnet = requests.patch(device_url, json.dumps(payload),
                                                        headers={'Content-Type': 'application/json',
                                                                 'Authorization': '{}'.format(access_token)})
                                print(bacnet.status_code)
                                # print(bacnet.json())

