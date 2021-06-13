import logging

import requests
from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.bacnet_master.interfaces.device import ObjType
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
    def post(cls, net_uuid, add_devices):
        data = Whois.parser.parse_args()
        add_devices = Functions.to_bool(add_devices)
        network_number = data['network_number']
        whois = data['whois']
        global_broadcast = data['global_broadcast']
        full_range = data['full_range']
        range_start = data['range_start']
        range_end = data['range_end']

        devices = DeviceService().whois(net_uuid, whois=whois,
                                        network_number=network_number,
                                        global_broadcast=global_broadcast,
                                        full_range=full_range,
                                        range_start=range_start,
                                        range_end=range_end)

        print(99999)
        print(devices)
        print(99999)
        if add_devices:
            host = '0.0.0.0'
            port = '1718'
            url = f"http://{host}:{port}/api/bm/device"
            for device in devices:
                print(device)
        return devices
                # _point_group = devices.get("points")
                # _point_group = _point_group.get(point_group)
                # if _point_group:
                #     for point in _point_group:
                #         device_uuid = device_uuid
                #         point_object_type = ObjType.has_value_by_name(point_group)
                #         point_name = point.get("point_name")
                #         point_object_id = point.get("point_object_id")
                #         body = {
                #             "point_name": point_name,
                #             "point_enable": True,
                #             "point_object_id": point_object_id,
                #             "point_object_type": point_object_type.name,
                #             "device_uuid": device_uuid
                #         }
                #
                #         requests.put(url,
                #                      headers={'Content-Type': 'application/json'},
                #                      json=body)

        # return DeviceService().whois(net_uuid, whois=whois,
        #                              network_number=network_number,
        #                              global_broadcast=global_broadcast,
        #                              full_range=full_range,
        #                              range_start=range_start,
        #                              range_end=range_end)


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
