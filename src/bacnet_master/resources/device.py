import logging
import requests
from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import NotFoundException, BadDataException, InternalServerErrorException
from rubix_http.resource import RubixResource

from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.models.device import BacnetDeviceModel
from src.bacnet_master.resources.rest_schema.schema_device import device_all_attributes, device_all_fields, \
    device_extra_attributes
from src.bacnet_master.services.device import Device as DeviceService
from src.utils.functions import Functions

logger = logging.getLogger(__name__)


class DeviceBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in device_all_attributes:
        parser.add_argument(attr,
                            type=device_all_attributes[attr]['type'],
                            required=device_all_attributes[attr].get('required', None),
                            help=device_all_attributes[attr].get('help', None),
                            store_missing=False)

    post_parser = reqparse.RequestParser()
    all_attributes = {**device_extra_attributes, **device_all_attributes}
    for attr in all_attributes:
        post_parser.add_argument(attr,
                                 type=all_attributes[attr]['type'],
                                 required=all_attributes[attr].get('required', None),
                                 help=all_attributes[attr].get('help', None),
                                 store_missing=False)


class AddDevice(DeviceBase):
    parser_patch = reqparse.RequestParser()
    for attr in device_all_attributes:
        parser_patch.add_argument(attr,
                                  type=device_all_attributes[attr]['type'],
                                  required=False,
                                  help=device_all_attributes[attr].get('help', None),
                                  store_missing=False)

    @classmethod
    @marshal_with(device_all_fields)
    def put(cls):
        device_uuid = Functions.make_uuid()
        data = Device.parser.parse_args()
        device: BacnetDeviceModel = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if device is None:
            device = Device.create_device_model_obj(device_uuid, data)
            device.save_to_db()
        else:
            device.update(**data)
        return device


class Device(DeviceBase):
    parser_patch = reqparse.RequestParser()
    for attr in device_all_attributes:
        parser_patch.add_argument(attr,
                                  type=device_all_attributes[attr]['type'],
                                  required=False,
                                  help=device_all_attributes[attr].get('help', None),
                                  store_missing=False)

    @classmethod
    @marshal_with(device_all_fields)
    def get(cls, device_uuid):
        device = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if not device:
            raise NotFoundException("Device not found")
        return device

    @classmethod
    @marshal_with(device_all_fields)
    def put(cls, device_uuid):
        data = Device.parser.parse_args()
        device: BacnetDeviceModel = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if device is None:
            device = Device.create_device_model_obj(device_uuid, data)
            device.save_to_db()
        else:
            device.update(**data)
        return device

    @classmethod
    @marshal_with(device_all_fields)
    def patch(cls, device_uuid):
        data = Device.parser_patch.parse_args()
        device: BacnetDeviceModel = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if device is None:
            raise NotFoundException("Device not found")
        device.update(**data)
        return device

    @classmethod
    def delete(cls, device_uuid):
        device = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if device:
            device.delete_from_db()
        return '', 204

    @staticmethod
    def create_device_model_obj(device_uuid, data):
        return BacnetDeviceModel(device_uuid=device_uuid, **data)


class DeviceList(DeviceBase):
    @classmethod
    @marshal_with(device_all_fields, envelope="devices")
    def get(cls):
        return BacnetDeviceModel.find_all()

    @classmethod
    @marshal_with(device_all_fields)
    def post(cls):
        data = Device.post_parser.parse_args()
        device_uuid = data.pop('device_uuid')
        if BacnetDeviceModel.find_by_device_uuid(device_uuid):
            raise BadDataException(f"Device with device_uuid '{device_uuid}' already exists.")
        device = Device.create_device_model_obj(device_uuid, data)
        device.save_to_db()
        return device


class DeviceObjectList(RubixResource):
    @classmethod
    def get(cls, device_uuid):
        device = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        if not device:
            raise NotFoundException(f"No device with that ID is added {device_uuid}")
        res = {
            'network_uuid': device.network.network_uuid,
            'device_uuid': device.device_uuid,
            'device_name': device.device_name,
            'device_object_id': device.device_object_id,
            'device_mac': device.device_mac
        }
        try:
            points = DeviceService.get_instance().get_object_list(device)
            res = {**res, 'objects': points}
        except Exception as e:
            raise InternalServerErrorException(str(e))
        return res


class DiscoverPoints(RubixResource):
    @classmethod
    def get(cls, device_uuid, add_points):
        device = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        add_points = Functions.to_bool(add_points)
        if not device:
            raise NotFoundException(f"No device with that ID is added {device_uuid}")
        points = DeviceService.get_instance().read_point_list(device)
        if not points:
            raise NotFoundException(f"Can't read points {points}")
        points = {"points": points}
        if add_points:
            host = '0.0.0.0'
            port = '1718'
            url = f"http://{host}:{port}/api/bm/point"
            for point_group in points.get("points"):
                _point_group = points.get("points")
                _point_group = _point_group.get(point_group)
                if _point_group:
                    for point in _point_group:
                        device_uuid = device_uuid
                        point_object_type = ObjType.has_value_by_name(point_group)
                        point_name = point.get("point_name")
                        point_object_id = point.get("point_object_id")
                        body = {
                            "point_name": point_name,
                            "point_enable": True,
                            "point_object_id": point_object_id,
                            "point_object_type": point_object_type.name,
                            "device_uuid": device_uuid
                        }

                        requests.put(url,
                                     headers={'Content-Type': 'application/json'},
                                     json=body)

        return points


class GetAllPoints(RubixResource):
    @classmethod
    def get(cls, network_uuid, timeout):
        host = '0.0.0.0'
        port = '1718'
        url = f"http://{host}:{port}/api/bm/network/{network_uuid}"
        network = requests.get(url).json()
        data = DeviceService.get_instance().read_point_list_by_network(network, network_uuid, int(timeout))
        return data
