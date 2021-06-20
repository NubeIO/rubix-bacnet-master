import threading
import time

import polling2
import requests
import random


from src.bacnet_master.utils.functions import BACnetFunctions
from src.utils.functions import Functions


class Polling:

    @staticmethod
    def test22():
        from src.bacnet_master.models.network import BacnetNetworkModel
        network_uuid = "21bff2d3ced4f9f2"
        host = '0.0.0.0'
        port = '1718'
        url = f"http://{host}:{port}/api/bm/network/{network_uuid}"
        network = requests.get(url).json()
        get_pv = False
        devices = {}
        discovery = True
        add_points = False
        timeout = 1
        # time.sleep(2)
        a = {}
        from src.bacnet_master.services.device import Device as DeviceService
        uuid = {'point_name': 'N-AI1111a32a1121', 'point_enable': True, 'point_object_id': 12211, 'point_object_type': 'analogInput', 'device_uuid': '22159eb053cb381e'}

        a = DeviceService.test(uuid)
        print(a)
        from src.bacnet_master.resources.network_whois import _poll_points_rpm
        for device in network.get("devices"):
            device_uuid = device["device_uuid"]
            device_name = device["device_name"]
            print(device_name)
            print(device_uuid)
            # a = _poll_points_rpm(device_uuid=device_uuid,
            #                      discovery=discovery,
            #                      add_points=add_points,
            #                      timeout=timeout
            #                      )

        print(a)
        a = random.randint(0, 9)
        return str(a)

    @staticmethod
    def test(response):
        from src.mqtt import MqttClient
        mqtt_client = MqttClient()
        mqtt_client.publish_value(('ao', "1"), response)
        print(response)
        return response == 'success'

    @staticmethod
    def test2():
        polling2.poll(lambda: Polling.test22(),
                      step=5,
                      poll_forever=True,
                      check_success=Polling.test)

    @staticmethod
    def run():
        t1 = threading.Thread(target=Polling.test2)
        t1.start()
