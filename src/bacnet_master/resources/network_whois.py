import logging
from flask_restful import reqparse
from rubix_http.resource import RubixResource
from rubix_http.exceptions.exception import NotFoundException

from src import db
from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.models.device import BacnetDeviceModel
from src.bacnet_master.models.network import BacnetNetworkModel
from src.bacnet_master.resources.point import AddPoint
from src.bacnet_master.resources.rest_schema.schema_network_whois import network_whois_all_attributes
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


def poll_points_rpm(**kwargs):
    _devices = None
    _points = None
    network_uuid = kwargs.get('network_uuid')
    add_points = kwargs.get('add_points')
    device_uuid = kwargs.get('device_uuid')
    discovery = kwargs.get('discovery')
    timeout = BACnetFunctions.validate_timeout(kwargs.get('timeout'))
    if device_uuid:
        db.session.commit()  # was added for when patching points
        device = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if not device:
            raise NotFoundException(f"No device with that ID is added {device_uuid}")
        if discovery:
            logger.info(f"POLL-POINTS discovery:{discovery}  device_uuid{device_uuid} points add_points:{add_points}")
            object_list = DeviceService.get_instance().build_point_list_new(device)
            logger.info(f"POLL-POINTS returned object_list{object_list}")
            if not isinstance(object_list, list):
                logger.error(f"POLL-POINTS discovery:{device.device_name} error:{object_list}")
            else:
                points = DeviceService.get_instance().poll_points_list(device, object_list=object_list, timeout=timeout)
                logger.info(f"POLL-POINTS returned points{points}")
                points_list = points.get("discovered_points")
                points_list = points_list.get("points")
                for i in points_list:
                    _points = points_list.get(i)
                    for point in _points:
                        point_name = point.get("point_name")
                        point_object_id = point.get("point_object_id")
                        point_object_type = ObjType.from_underscore(i)
                        if add_points:
                            data = {'point_name': point_name, 'point_enable': True, 'point_object_id': point_object_id,
                                    'point_object_type': point_object_type, 'device_uuid': device_uuid}
                            AddPoint.add_point(data)
                return points
        else:
            if not device.points:
                raise NotFoundException(f"Not points are added for this device:{device_uuid}")
            _points = device
            points = DeviceService.get_instance().poll_points_list(device, timeout=timeout)
            logger.info(f"POLL-POINTS discovery:{discovery} points add_points:{add_points} points:{points}")

            return points


class DeviceAllPoints(RubixResource):
    @classmethod
    def post(cls, device_uuid):
        if not device_uuid:
            raise NotFoundException(f"device uuid is needed")
        data = Whois.parser.parse_args()
        add_points = data.get('add_points')
        discovery = data.get('discovery')
        timeout = BACnetFunctions.validate_timeout(data.get('timeout'))
        return poll_points_rpm(device_uuid=device_uuid,
                               discovery=discovery,
                               add_points=add_points,
                               timeout=timeout
                               )
