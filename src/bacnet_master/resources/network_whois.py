import logging

from flask_restful import reqparse
from rubix_http.resource import RubixResource
from rubix_http.exceptions.exception import NotFoundException

from src.bacnet_master.models.device import BacnetDeviceModel
from src.bacnet_master.models.network import BacnetNetworkModel
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


def _discover_points(**kwargs):
    _devices = None
    network_uuid = kwargs.get('network_uuid')
    if network_uuid:
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        if not network.devices:
            raise NotFoundException(f"Not devices are are added to the system network uuid:{network_uuid}")
        else:
            _devices = network.devices

    device_uuid = kwargs.get('device_uuid')
    if device_uuid:
        device = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if not device:
            raise NotFoundException(f"No device with that ID is added {device_uuid}")
        else:
            _devices = [device]

    add_points = kwargs.get('add_points')
    fast_poll = kwargs.get('fast_poll')
    timeout = BACnetFunctions.validate_timeout(kwargs.get('timeout'))

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

    count = 0
    network_devices = {}
    network_devices_list = {}
    for device in _devices:
        _device_uuid = device.device_uuid
        _device_name = device.device_name
        # do bacnet read and build the points list
        points = DeviceService.get_instance().build_point_list(device,
                                                               get_point_name,
                                                               get_point_value,
                                                               get_point_priority=get_point_priority,
                                                               timeout=timeout)

        if not isinstance(points, dict):
            if not network_uuid:
                raise NotFoundException(points)
        count = count + 1
        network_devices.update({"devices_found": count})
        _device_key = f"{_device_name}_{_device_uuid}"
        network_devices.update({_device_key: points})
        if add_points:
            _points = BACnetFunctions.add_points(_device_uuid, points, _device_name)
            network_devices_list.update({_device_key: _points})
    if add_points and network_uuid:
        return network_devices_list
    elif add_points and device_uuid:
        out = {}
        for key, value in network_devices_list.items():
            out = value
        return out
    elif device_uuid:
        out = {}
        for key, value in network_devices.items():
            out = value
        return out
    elif network_uuid:
        return network_devices


class NetworkAllPoints(RubixResource):
    @classmethod
    def post(cls, network_uuid):
        if not network_uuid:
            raise NotFoundException(f"network uuid is needed")
        data = Whois.parser.parse_args()
        add_points = data.get('add_points')
        fast_poll = data.get('fast_poll')
        timeout = BACnetFunctions.validate_timeout(data.get('timeout'))
        return _discover_points(network_uuid=network_uuid,
                                fast_poll=fast_poll,
                                add_points=add_points,
                                timeout=timeout
                                )


class DeviceAllPoints(RubixResource):
    @classmethod
    def post(cls, device_uuid):
        if not device_uuid:
            raise NotFoundException(f"device uuid is needed")
        data = Whois.parser.parse_args()
        add_points = data.get('add_points')
        fast_poll = data.get('fast_poll')
        timeout = BACnetFunctions.validate_timeout(data.get('timeout'))
        return _discover_points(device_uuid=device_uuid,
                                fast_poll=fast_poll,
                                add_points=add_points,
                                timeout=timeout
                                )


def _poll_points(**kwargs):
    _devices = None
    _points = None
    network_uuid = kwargs.get('network_uuid')
    if network_uuid:
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        if not network.devices:
            raise NotFoundException(f"Not devices are are added to the system network uuid:{network_uuid}")
        else:
            _devices = network.devices

    device_uuid = kwargs.get('device_uuid')
    if device_uuid:
        device = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if not device:
            raise NotFoundException(f"No device with that ID is added {device_uuid}")
        if not device.points:
            raise NotFoundException(f"Not points are added for this device:{network_uuid}")
        else:
            _points = device
            timeout = BACnetFunctions.validate_timeout(kwargs.get('timeout'))
            return DeviceService.get_instance().poll_points(device, timeout=timeout)


def _poll_points_rpm(**kwargs):
    _devices = None
    _points = None
    network_uuid = kwargs.get('network_uuid')
    if network_uuid:
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        if not network.devices:
            raise NotFoundException(f"Not devices are are added to the system network uuid:{network_uuid}")
        else:
            _devices = network.devices

    device_uuid = kwargs.get('device_uuid')
    if device_uuid:
        device = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if not device:
            raise NotFoundException(f"No device with that ID is added {device_uuid}")
        if not device.points:
            raise NotFoundException(f"Not points are added for this device:{network_uuid}")
        else:
            _points = device
            timeout = BACnetFunctions.validate_timeout(kwargs.get('timeout'))
            return DeviceService.get_instance().poll_points_rpm(device, timeout=timeout)


class DevicePollAllPoints(RubixResource):
    @classmethod
    def post(cls, device_uuid):
        if not device_uuid:
            raise NotFoundException(f"device uuid is needed")
        data = Whois.parser.parse_args()
        add_points = data.get('add_points')
        fast_poll = data.get('fast_poll')
        timeout = BACnetFunctions.validate_timeout(data.get('timeout'))
        return _poll_points_rpm(device_uuid=device_uuid,
                                fast_poll=fast_poll,
                                add_points=add_points,
                                timeout=timeout
                                )
