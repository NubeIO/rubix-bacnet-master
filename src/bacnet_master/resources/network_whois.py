import logging

import requests
from flask_restful import reqparse
from rubix_http.resource import RubixResource
from rubix_http.exceptions.exception import NotFoundException, BadDataException

from src.bacnet_master.models.network import BacnetNetworkModel
from src.bacnet_master.resources.rest_schema.schema_network_whois import network_whois_all_attributes, \
    network_unknown_device_objects_attributes, point_unknown_read_point_pv_attributes
from src.bacnet_master.services.device import Device as DeviceService
from src.bacnet_master.utils.functions import BACnetFunctions
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
        is_mstp = data['is_mstp']
        show_supported_services = data['show_supported_services']
        add_devices = Functions.to_bool(add_devices)
        show_supported_services = Functions.to_bool(show_supported_services)
        devices = DeviceService().whois(network_uuid, whois=whois,
                                        network_number=network_number,
                                        global_broadcast=global_broadcast,
                                        full_range=full_range,
                                        range_start=range_start,
                                        range_end=range_end,
                                        is_mstp=is_mstp,
                                        show_supported_services=show_supported_services)
        if not add_devices:
            return {
                "discovered_devices": devices,
                "added_devices_count": 0,
                "added_devices": {},
                "existing_or_failed_to_add": {},

            }

        elif add_devices:
            if not devices:
                raise NotFoundException("no devices found and or an error")
            return BACnetFunctions.who_add_devices(devices, network_uuid)


class NetworkAllPoints(RubixResource):
    @classmethod
    def post(cls, network_uuid):
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        data = Whois.parser.parse_args()
        add_points = data.get('add_points')
        fast_poll = data.get('fast_poll')
        timeout = data.get('timeout')
        get_point_name = None
        get_point_priority = None
        get_point_value = None
        if add_points:
            get_point_name = True
        else:
            if fast_poll:
                get_point_value = True
            else:
                get_point_name = True
                get_point_value = True
                get_point_priority = True

        if not network:
            raise NotFoundException("Network not found")
        count = 0
        devices = {}
        devices_list = {}
        print("add_points", add_points)
        print("fast_poll", fast_poll)
        print(get_point_name, get_point_priority, get_point_value)
        for device in network.devices:
            device_uuid = device.device_uuid
            device_name = device.device_name
            points = DeviceService.get_instance().build_point_list(device, get_point_name, get_point_value,
                                                                   get_point_priority)
            count = count + 1
            devices.update({"devices_found": count})
            name = f"{device_name}_{device_uuid}"
            name2 = f"points_{device_name}_{device_uuid}"
            devices.update({name: points})
            if add_points:
                _points = BACnetFunctions.add_points2(device_uuid, points, device_name)
                devices_list.update({name2: _points})
        if add_points:
            return devices_list
        else:
            return devices


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
    def post(cls, network_uuid):
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
        return DeviceService().unknown_get_object_list(network_uuid, device)


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
    def post(cls, network_uuid):
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
        return DeviceService().unknown_get_point_pv(network_uuid, device)
