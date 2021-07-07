import logging
import time

import BAC0

from src.bacnet_master.models.network import BacnetNetworkModel

logger = logging.getLogger(__name__)


class Network:
    __instance = None


    @staticmethod
    def get_instance():
        if not Network.__instance:
            Network()
        return Network.__instance

    def __init__(self):
        if Network.__instance:
            raise Exception("Network class is a singleton!")
        else:
            Network.__instance = self
            self.networks = {}

    def start(self):
        logger.info("BACNET MASTER Network Start...")
        network_service = Network.get_instance()
        for network in BacnetNetworkModel.query.all():
            network_service.add_network(network)

    def add_network(self, network):
        net_url = f"{network.network_ip}/{network.network_mask}:{network.network_port}"
        network_device_object_id = network.network_device_object_id
        network_device_name = network.network_device_name
        if not self.networks.get(net_url):
            self.networks[net_url] = {}
        if not self.networks.get(net_url).get(network_device_object_id):
            self.networks[net_url][network_device_object_id] = {}
        logger.info('=====================================================')
        logger.info('...........Creating BACnet MASTER network with..............')
        net = self.get_network(network)
        if net:
            net.disconnect()
        else:
            try:
                network = BAC0.lite(ip=net_url, deviceId=network_device_object_id, localObjName=network_device_name)
                self.networks[net_url][network_device_object_id][network_device_name] = network
            except ValueError as e:
                logger.error(f"BACnet MASTER  Initialization error! msg:{e}")
            except Exception as e:
                logger.error(f"BACnet MASTER  Initialization error! msg:{e}")

    def delete_network(self, network):
        net_url = f"{network.network_ip}/{network.network_mask}:{network.network_port}"
        network_device_object_id = network.network_device_object_id
        network_device_name = network.network_device_name
        network = self.networks.get(net_url, {}).get(network_device_object_id, {}).get(network_device_name)
        if network:
            pass
            # TODO: uncomment, disconnect is not working fine
            # network.disconnect()
            # del self.networks[net_url][network_device_object_id][network_device_name]

    def get_network(self, network):
        net_url = f'{network.network_ip}/{network.network_mask}:{network.network_port}'
        network_device_object_id = network.network_device_object_id
        network_device_name = network.network_device_name
        out = self.networks.get(net_url, {}).get(network_device_object_id, {}).get(network_device_name)
        return out
