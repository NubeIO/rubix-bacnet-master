import logging
from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.bacnet_master.resources.rest_schema.schema_network_whois import network_whois_all_attributes, \
    network_unknown_device_objects_attributes, point_unknown_read_point_pv_attributes
from src.bacnet_master.services.device import Device as DeviceService

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
    def post(cls, net_uuid):
        data = Whois.parser.parse_args()
        network_number = data['network_number']
        whois = data['whois']
        global_broadcast = data['global_broadcast']
        full_range = data['full_range']
        range_start = data['range_start']
        range_end = data['range_end']
        return DeviceService().whois(net_uuid, whois=whois,
                                     network_number=network_number,
                                     global_broadcast=global_broadcast,
                                     full_range=full_range,
                                     range_start=range_start,
                                     range_end=range_end)


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
        device_id = data['device_id']
        device_ip = data['device_ip']
        device_mac = data['device_mac']
        device_mask = data['device_mask']
        device_port = data['device_port']
        type_mstp = data['type_mstp']
        network_number = data['network_number']
        device = {
            "device_id": device_id,
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
        device_id = data['device_id']
        device_ip = data['device_ip']
        device_mac = data['device_mac']
        device_mask = data['device_mask']
        device_port = data['device_port']
        type_mstp = data['type_mstp']
        network_number = data['network_number']
        point_obj_id = data['point_obj_id']
        point_obj_type = data['point_obj_type']
        device = {
            "device_id": device_id,
            "device_ip": device_ip,
            "device_mac": device_mac,
            "device_mask": device_mask,
            "device_port": device_port,
            "type_mstp": type_mstp,
            "network_number": network_number,
            "point_obj_id": point_obj_id,
            "point_obj_type": point_obj_type
        }
        return DeviceService().unknown_get_point_pv(net_uuid, device)
