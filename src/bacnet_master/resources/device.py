import logging
import requests
from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import NotFoundException, BadDataException, InternalServerErrorException
from rubix_http.resource import RubixResource

from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.models.device import BacnetDeviceModel
from src.bacnet_master.models.network import BacnetNetworkModel
from src.bacnet_master.resources.rest_schema.schema_device import device_all_attributes, device_all_fields, \
    device_extra_attributes
from src.bacnet_master.services.device import Device as DeviceService
from src.bacnet_master.utils.functions import BACnetFunctions
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
        network_uuid = data.get("network_uuid")
        device_mac = data.get("device_mac")
        type_mstp = data.get("type_mstp")
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        network_number = data.get("network_number")
        device_object_id = data.get("device_object_id")
        check_object_id: BacnetDeviceModel = BacnetDeviceModel.existing_device_id_to_net(network_number,
                                                                                         device_object_id)
        if check_object_id:
            raise NotFoundException(
                f"Device same Object ID:{device_object_id} and Network Number:{network_number} already exists")
        check_mac_address: BacnetDeviceModel = BacnetDeviceModel.existing_net_to_mac(network_number, device_mac)
        if type_mstp:
            if check_mac_address:
                raise NotFoundException(
                    f"Device same mac address:{device_mac} and Network Number:{network_number} already exists")
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
        if device is None:
            raise NotFoundException("Device not found")
        if device:
            device.delete_from_db()
            return {"message": f"pass"}, 204
        else:
            return {"message": "failed to delete"}, 404

    @staticmethod
    def create_device_model_obj(device_uuid, data):
        return BacnetDeviceModel(device_uuid=device_uuid, **data)


class DeleteDevices(DeviceBase):
    @classmethod
    def delete(cls, network_uuid):
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        device = BacnetDeviceModel.delete_all_device_by_network(network_uuid)
        if device:
            return 'pass', 204
        else:
            return 'fail', 404


class DeviceList(DeviceBase):
    @classmethod
    @marshal_with(device_all_fields, envelope="devices")
    def get(cls, with_children):
        with_children = Functions.to_bool(with_children)
        if not with_children:
            devices = BacnetDeviceModel.find_all()
            for device in devices:
                device.points = []
            return devices
        else:
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
    def post(cls, device_uuid, add_points, get_pv):
        # data = Device.post_parser.parse_args()
        get_pv = Functions.to_bool(get_pv)
        device = BacnetDeviceModel.find_by_device_uuid(device_uuid)
        add_points = Functions.to_bool(add_points)
        if not device:
            raise NotFoundException(f"No device with that ID is added {device_uuid}")
        if add_points:
            return BACnetFunctions.add_points(device_uuid, get_pv, add_points)
        else:
            points = DeviceService.get_instance().read_point_list(device, get_pv)
            print(points.get("discovery_errors"))
            # points = {"points": points}

            if not points:
                raise NotFoundException(f"Can't read points {points}")
            return {
                "discovered_points": {"points": points.get("points")},
                "discovery_errors": points.get("discovery_errors"),
                "added_points_count": 0,
                "added_points": {
                    "points": {
                        "analog_inputs": [],
                        "analog_outputs": [],
                        "analog_values": [],
                        "binary_input": [],
                        "binary_output": [],
                        "binary_value": [],
                        "multi_state_input": [],
                        "multi_state_output": [],
                        "multi_state_value": []
                    }
                },
                "existing_or_failed_points": {
                    "points": {
                        "analog_inputs": [],
                        "analog_outputs": [],
                        "analog_values": [],
                        "binary_input": [],
                        "binary_output": [],
                        "binary_value": [],
                        "multi_state_input": [],
                        "multi_state_output": [],
                        "multi_state_value": []
                    }
                }
            }




class AddAllPoints(RubixResource):
    @classmethod
    def post(cls, network_uuid, add_points):
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        host = '0.0.0.0'
        port = '1718'
        url = f"http://{host}:{port}/api/bm/network/{network_uuid}"
        network = requests.get(url).json()
        get_pv = False
        add_points = Functions.to_bool(add_points)
        if not network:
            raise NotFoundException("Network not found")
        count = 0
        devices = {}
        for device in network.get("devices"):
            device_uuid = device["device_uuid"]
            device_name = device["device_name"]
            res = BACnetFunctions.add_points(device_uuid, get_pv, add_points)
            count = count + 1
            devices.update({"devices_found": count})
            name = f"{device_name}_{device_uuid}"
            devices.update({name: res})
        return devices


class GetAllPoints(RubixResource):
    @classmethod
    def post(cls, network_uuid, timeout):
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        host = '0.0.0.0'
        port = '1718'
        url = f"http://{host}:{port}/api/bm/network/{network_uuid}"
        get_network = requests.get(url).json()
        data = DeviceService.get_instance().read_point_list_by_network(get_network, network_uuid, int(timeout))
        return data
