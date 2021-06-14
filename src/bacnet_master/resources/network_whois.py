import logging

import requests
from flask_restful import reqparse
from rubix_http.resource import RubixResource
from rubix_http.exceptions.exception import NotFoundException, BadDataException, InternalServerErrorException

from src.bacnet_master.models.network import BacnetNetworkModel
from src.bacnet_master.resources.rest_schema.schema_network_whois import network_whois_all_attributes, \
    network_unknown_device_objects_attributes, point_unknown_read_point_pv_attributes
from src.bacnet_master.services.device import Device as DeviceService
from src.utils.functions import Functions

logger = logging.getLogger(__name__)


class NetworkWhois(RubixResource):
    parser = reqparse.RequestParser()
    for attr in network_whois_all_attributes:
        parser.add_argument(attr,
                            type=network_whois_all_attributes[attr]['type'],
                            required=network_whois_all_attributes[attr].get('required', None),
                            help=network_whois_all_attributes[attr].get('help', None),
                            store_missing=False)


class Whois(NetworkWhois):
    @classmethod
    def post(cls, network_uuid):
        data = Whois.parser.parse_args()
        network_number = data['network_number']
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        whois = data['whois']
        global_broadcast = data['global_broadcast']
        full_range = data['full_range']
        range_start = data['range_start']
        range_end = data['range_end']
        add_devices = data['add_devices']
        add_devices = Functions.to_bool(add_devices)
        devices = DeviceService().whois(network_uuid, whois=whois,
                                        network_number=network_number,
                                        global_broadcast=global_broadcast,
                                        full_range=full_range,
                                        range_start=range_start,
                                        range_end=range_end)
        if not add_devices:
            return {
                "discovered_devices": devices,
                "added_devices_count": 0,
                "added_devices":  {},
                "existing_or_failed_to_add": {},

            }

        elif add_devices:
            host = '0.0.0.0'
            port = '1718'
            url = f"http://{host}:{port}/api/bm/device"
            added_devices = {}
            fail_add_devices = {}
            count = 0
            for idx, device in enumerate(devices):
                _device = devices.get(device)
                device_name = _device.get("device_name")
                device_ip = _device.get("device_ip")
                device_mask = _device.get("device_mask", 24)
                device_port = _device.get("device_port", 47808)
                device_mac = _device.get("device_mac")
                device_object_id = _device.get("device_object_id")
                network_number = _device.get("network_number")
                type_mstp = _device.get("type_mstp")
                network_uuid = network_uuid
                body = {
                    "device_name": device_name,
                    "device_ip": device_ip,
                    "device_mask": device_mask,
                    "device_port": device_port,
                    "device_mac": device_mac,
                    "device_object_id": device_object_id,
                    "network_number": network_number,
                    "type_mstp": type_mstp,
                    "supports_rpm": False,
                    "supports_wpm": False,
                    "network_uuid": network_uuid
                }
                res = requests.put(url,
                                   headers={'Content-Type': 'application/json'},
                                   json=body)

                if res.status_code == 200:
                    count = count + 1
                    dev = {device_name: body}
                    added_devices.update(dev)
                else:
                    dev = {device_name: body}
                    fail_add_devices.update(dev)

            return {
                "discovered_devices": devices,
                "added_devices_count": count,
                "added_devices": added_devices,
                "existing_or_failed_to_add": fail_add_devices
            }


class NetworkUnknownDeviceObjects(RubixResource):
    parser = reqparse.RequestParser()
    for attr in network_unknown_device_objects_attributes:
        parser.add_argument(attr,
                            type=network_unknown_device_objects_attributes[attr]['type'],
                            required=network_unknown_device_objects_attributes[attr].get('required', None),
                            help=network_unknown_device_objects_attributes[attr].get('help', None),
                            store_missing=False)


class UnknownDeviceObjects(NetworkUnknownDeviceObjects):
    @classmethod
    def post(cls, net_uuid):
        data = UnknownDeviceObjects.parser.parse_args()
        device_object_id = data['device_object_id']
        device_ip = data['device_ip']
        device_mac = data['device_mac']
        device_mask = data['device_mask']
        device_port = data['device_port']
        type_mstp = data['type_mstp']
        network_number = data['network_number']
        device = {
            "device_object_id": device_object_id,
            "device_ip": device_ip,
            "device_mac": device_mac,
            "device_mask": device_mask,
            "device_port": device_port,
            "type_mstp": type_mstp,
            "network_number": network_number
        }
        return DeviceService().unknown_get_object_list(net_uuid, device)


class PointUnknownReadPointPv(RubixResource):
    parser = reqparse.RequestParser()
    for attr in point_unknown_read_point_pv_attributes:
        parser.add_argument(attr,
                            type=point_unknown_read_point_pv_attributes[attr]['type'],
                            required=point_unknown_read_point_pv_attributes[attr].get('required', None),
                            help=point_unknown_read_point_pv_attributes[attr].get('help', None),
                            store_missing=False)


class UnknownReadPointPv(PointUnknownReadPointPv):
    @classmethod
    def post(cls, net_uuid):
        data = UnknownReadPointPv.parser.parse_args()
        device_object_id = data['device_object_id']
        device_ip = data['device_ip']
        device_mac = data['device_mac']
        device_mask = data['device_mask']
        device_port = data['device_port']
        type_mstp = data['type_mstp']
        network_number = data['network_number']
        point_object_id = data['point_object_id']
        point_object_type = data['point_object_type']
        device = {
            "device_object_id": device_object_id,
            "device_ip": device_ip,
            "device_mac": device_mac,
            "device_mask": device_mask,
            "device_port": device_port,
            "type_mstp": type_mstp,
            "network_number": network_number,
            "point_object_id": point_object_id,
            "point_object_type": point_object_type
        }
        return DeviceService().unknown_get_point_pv(net_uuid, device)
