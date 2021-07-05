import logging
from BAC0.core.io.IOExceptions import UnknownObjectError, NoResponseFromController, UnknownPropertyError

from src.bacnet_master.bacnet_exceptions import BACnetNetworkInstanceError
from src.bacnet_master.interfaces.device import ObjType, PointObjType
from src.bacnet_master.interfaces.object_property import ObjProperty
from src.bacnet_master.models.device import BacnetDeviceModel
from src.bacnet_master.models.network import BacnetNetworkModel

from src.bacnet_master.services.network import Network
from src.bacnet_master.utils.functions import BACnetFunctions

logger = logging.getLogger(__name__)


class Device:
    __instance = None

    @staticmethod
    def get_instance():
        if Device.__instance is None:
            Device()
        return Device.__instance

    def __init__(self):
        if Device.__instance is not None:
            print("Device class is a singleton! @ Binod to check")
            # raise Exception("Device class is a singleton!")
        else:
            Device.__instance = self

    def get_dev_url(self, device):
        return f"{device.device_ip}:{device.device_port}"

    # @staticmethod
    # def test(uuid):
    #     from src.bacnet_master.resources.point import AddPoint
    #     return AddPoint.add_point(uuid)

    def _common_point(self, point, device, **kwargs):
        dev_url = kwargs.get('dev_url') or BACnetFunctions.build_url(device)
        network_number = kwargs.get('network_number') or device.network_number
        network_number = BACnetFunctions.network_number(network_number)
        object_instance = kwargs.get('object_instance') or point.point_object_id
        object_type = kwargs.get('object_type') or point.point_object_type.name
        prop = kwargs.get('prop') or ObjProperty.presentValue.name
        type_mstp = kwargs.get('type_mstp') or device.type_mstp
        device_mac = kwargs.get('device_mac') or device.device_mac
        ethernet_mac_address = kwargs.get("ethernet_mac_address") or device.ethernet_mac_address
        logger.info(f"DO POINT READ dev_url:{dev_url}, type_mstp:{type_mstp}, "
                    f"device_mac:{device_mac}, object_instance:{object_instance},  "
                    f"object_type:{object_type},  prop:{prop}, "
                    f"network_number:{network_number}")
        if ethernet_mac_address:
            return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        if type_mstp:
            return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        if network_number != 0:
            return f'{network_number}:{dev_url} {object_type} {object_instance} {prop}'
        else:
            return f'{dev_url} {object_type} {object_instance} {prop}'

    def build_device_address(self, device):
        dev_url = BACnetFunctions.build_url(device)
        device_mac = device.device_mac
        network_number = device.network_number
        network_number = BACnetFunctions.network_number(network_number)
        if device_mac >= 1:
            return f'{network_number}:{device_mac}'
        if network_number != 0:
            return f'{network_number}:{dev_url}'
        else:
            return f'{dev_url}'

    def _common_object(self, device=None, **kwargs):
        """192.168.15.202/24:47808 device 202 objectList"""
        dev_url = kwargs.get('dev_url') or BACnetFunctions.build_url(device)
        type_mstp = kwargs.get('type_mstp') or device.type_mstp or False
        device_mac = kwargs.get('device_mac') or device.device_mac
        object_instance = kwargs.get('object_instance') or device.device_object_id
        network_number = kwargs.get('network_number')
        if network_number != 0:
            network_number = device.network_number
        network_number = BACnetFunctions.network_number(network_number)
        object_type = kwargs.get('object_type') or ObjType.device.name
        prop = kwargs.get('prop') or ObjProperty.objectList.name
        ethernet_mac_address = kwargs.get("ethernet_mac_address") or device.ethernet_mac_address
        if ethernet_mac_address:
            return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        if type_mstp:
            return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        if network_number != 0:
            return f'{network_number}:{dev_url} {object_type} {object_instance} {prop}'
        else:
            return f'{dev_url} {object_type} {object_instance} {prop}'

    def _get_network_from_device(self, device):
        return Network.get_instance().get_network(device.network)

    def _get_network_from_network(self, network):
        return Network.get_instance().get_network(network)

    def get_point_pv(self, point):
        device = BacnetDeviceModel.find_by_device_uuid(point.device_uuid)
        if not device:
            return {"device": "device is none"}
        network_instance = self._get_network_from_device(device)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        read = self._common_point(point, device)
        if network_instance:
            try:
                value = network_instance.read(read)
                value = BACnetFunctions.clean_point_value(value)
                logger.info(f"DO POINT READ: {read}: return value:{value}")
                return value
            except UnknownObjectError as e:
                logger.error(f"{point.point_object_type.name}:{point.point_object_id} is unknown: {e}")
                return f"{point.point_object_type.name}:{point.point_object_id} is unknown"
            except Exception as e:
                logger.error(f"{read} read present value error: {e}")
                return f"{point.point_object_type.name}:{point.point_object_id} is unknown: {e}"

    def get_point_priority_errors(self, point):
        device = BacnetDeviceModel.find_by_device_uuid(point.device_uuid)
        if not device:
            return {"device": "device is none"}
        network_instance = self._get_network_from_device(device)
        object_type = point.point_object_type.name
        object_instance = point.point_object_id
        prop = ObjProperty.priorityArray.value
        if not network_instance:
            return {"network_instance": "network instance is none"}
        read = self._common_object(device, object_type=object_type,
                                   object_instance=object_instance,
                                   prop=prop)
        if network_instance:
            try:
                value = network_instance.read(read)
                value = BACnetFunctions.serialize_priority_array(value.dict_contents())
                return {
                    "value": value,
                    "error": None
                }
            except UnknownPropertyError as e:
                logger.error(f"{point.point_object_type.name}:{point.point_object_id} is unknown: {e}")
                return {
                    "value": None,
                    "error": f"UnknownPropertyError: {e}"
                }
            except UnknownObjectError as e:
                logger.error(f"{point.point_object_type.name}:{point.point_object_id} is unknown: {e}")
                return {
                    "value": None,
                    "error": f"UnknownObjectError: {e}"
                }
            except Exception as e:
                logger.error(f"{read} read priority value error: {e}")
                return {
                    "value": None,
                    "error": f"UnknownObjectError: {e}"
                }

    def get_point_priority(self, point):
        device = BacnetDeviceModel.find_by_device_uuid(point.device_uuid)
        if not device:
            return {"device": "device is none"}
        network_instance = self._get_network_from_device(device)
        object_type = point.point_object_type.name
        object_instance = point.point_object_id
        prop = ObjProperty.priorityArray.value
        if not network_instance:
            return {"network_instance": "network instance is none"}
        read = self._common_object(device, object_type=object_type,
                                   object_instance=object_instance,
                                   prop=prop)
        if network_instance:
            try:
                value = network_instance.read(read)
                value = BACnetFunctions.serialize_priority_array(value.dict_contents())
                return value
            except UnknownObjectError as e:
                logger.error(f"{point.point_object_type.name}:{point.point_object_id} is unknown: {e}")
                return {f"{point.point_object_type.name}:{point.point_object_id} is unknown"}
            except Exception as e:
                logger.error(f"{read} read priority value error: {e}")
                return {f"{point.point_object_type.name}:{point.point_object_id} is unknown"}

    def write_point_pv(self, point, value, priority):
        device = BacnetDeviceModel.find_by_device_uuid(point.device_uuid)
        if not device:
            return {"device": "device is none"}
        network_instance = self._get_network_from_device(device)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        point_object = point.point_object_type
        if value != 'null':
            value = float(value)
            if point_object == ObjType.binaryOutput or point_object == ObjType.binaryValue:
                if value >= 1:
                    value = "active"
                elif value < 1:
                    value = "inactive"
        cmd = self._common_point(point, device)
        write = f"{cmd} {value} - {priority}"
        if network_instance:
            try:
                value = network_instance.write(write)

                return value
            except UnknownObjectError as e:
                logger.error(
                    f"UnknownObjectError: {point.point_object_type.name}:{point.point_object_id}  priority:{priority} msg: {e}")
                return f"{point.point_object_type.name}:{point.point_object_id} priority:{priority} msg: {e}"
            except UnknownPropertyError as e:
                logger.error(
                    f"UnknownPropertyError: {point.point_object_type.name}:{point.point_object_id}  priority:{priority} msg: {e}")
                return f"{point.point_object_type.name}:{point.point_object_id} priority:{priority} msg: {e}"
            except NoResponseFromController as e:
                logger.error(
                    f"NoResponseFromController: {point.point_object_type.name}:{point.point_object_id}  priority:{priority} msg: {e}")
                return f"{point.point_object_type.name}:{point.point_object_id} priority:{priority} msg: {e}"
            except Exception as e:
                logger.error(f"{cmd} point write value error: {e}")
                return f"{point.point_object_type.name}:{point.point_object_id} priority:{priority} msg: {e}"

    def read_point_object(self, device, network_instance, **kwargs) -> dict:
        object_instance = kwargs.get('object_instance')
        object_type = kwargs.get('object_type')
        prop = kwargs.get('prop')
        timeout = BACnetFunctions.validate_timeout(kwargs.get('timeout'))
        try:
            value = network_instance.read(
                self._common_object(device,
                                    object_type=object_type,
                                    object_instance=object_instance,
                                    prop=prop), timeout=timeout)
            return {
                "value": value,
                "error": None

            }
        except UnknownObjectError as e:
            logger.error(
                f"UnknownObjectError: {e}")
            return {
                "value": None,
                "error": e
            }

    def get_point_pv_dict(self, point, **kwargs):
        device = BacnetDeviceModel.find_by_device_uuid(point.device_uuid)
        if not device:
            return {"device": "device is none"}
        network_instance = self._get_network_from_device(device)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        read = self._common_point(point, device)
        timeout = kwargs.get('timeout')
        if network_instance:
            try:
                value = network_instance.read(read, timeout=timeout)
                value = BACnetFunctions.clean_point_value(value)
                return {
                    "value": value,
                    "error": None

                }
            except UnknownObjectError as e:
                logger.error(
                    f"UnknownObjectError: {e}")
                return {
                    "value": None,
                    "error": e
                }

            except Exception as e:
                logger.error(
                    f"Exception: {e}")
                return {
                    "value": None,
                    "error": e
                }

    def read_point_object_rpm(self, device, network_instance, **kwargs) -> dict:
        object_instance = kwargs.get('object_instance')
        object_type = kwargs.get('object_type')
        prop = kwargs.get('prop')
        timeout = BACnetFunctions.validate_timeout(kwargs.get('timeout'))
        try:
            value = network_instance.readMultiple(
                self._common_object(device,
                                    object_type=object_type,
                                    object_instance=object_instance,
                                    prop=prop), timeout=timeout)
            return {
                "value": value,
                "error": None

            }
        except UnknownObjectError as e:
            logger.error(
                f"UnknownObjectError: {e}")
            return {
                "value": None,
                "error": e
            }

    def poll_points_list(self, device, **kwargs):
        network_instance = self._get_network_from_device(device)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        object_list = kwargs.get('object_list')
        timeout = kwargs.get('timeout')
        points = device.points
        points_list = {}
        points_list_name = {}
        analog_input = []
        analog_output = []
        analog_value = []
        binary_input = []
        binary_output = []
        binary_value = []
        multi_state_input = []
        multi_state_output = []
        multi_state_value = []
        address = self.build_device_address(device)
        device_name = device.device_name
        type_mstp = device.type_mstp
        if object_list:
            for obj in object_list:
                object_type = obj[0]
                if PointObjType.check_is_point_type(object_type):
                    # if object_type == ObjType.analogInput.name or object_type == ObjType.analogInput.name:
                    point_object_id = obj[1]
                    key = f"{object_type}:{point_object_id}"
                    points_list[key] = ['objectName', 'presentValue']
        else:
            for point in points:
                object_type = point.point_object_type
                point_object_id = point.point_object_id
                point_name = point.point_name
                key = f"{object_type.name}:{point_object_id}"
                points_list[key] = ['objectName', 'presentValue']
                points_list_name[key] = point_name

        def chunk_dict(d, chunk_size):
            r = {}
            for k, v in d.items():
                if len(r) == chunk_size:
                    yield r
                    r = {}
                r[k] = v
            if r:
                yield r

        if type_mstp:
            _points_list = list(chunk_dict(points_list, 2))
        else:
            _points_list = list(chunk_dict(points_list, 5))

        def payload(_list):
            return {"point_object_id": _list[0], "point_name": _list[1], "point_value": _list[2]}

        for key, value in enumerate(_points_list):
            _rpm = {'address': address,
                    "objects": value
                    }
            r = network_instance.readMultiple(address, request_dict=_rpm, timeout=timeout)
            if isinstance(r, str):
                logger.error(f"POLL-POINTS readMultiple: was empty address:{address} device_name:{device_name}")
            if isinstance(r, dict):
                logger.info(f"POLL-POINTS readMultiple: address:{address} device_name:{device_name}")
                for _key, rpm_points in enumerate(r):
                    _pnt = r[rpm_points]
                    object_type = rpm_points[0]
                    point_object_id = rpm_points[1]
                    key = f"{object_type}:{point_object_id}"
                    if object_list:
                        object_name = _pnt[0][1]
                    else:
                        object_name = points_list_name.get(key)
                    present_value = BACnetFunctions.clean_point_value(_pnt[1][1])
                    if object_type == ObjType.analogInput.name:  # AI
                        analog_input.append(payload([point_object_id, object_name, present_value]))
                    elif object_type == ObjType.analogOutput.name:  # AO
                        analog_output.append(payload([point_object_id, object_name, present_value]))
                    elif object_type == ObjType.analogValue.name:  # AV
                        analog_value.append(payload([point_object_id, object_name, present_value]))
                    elif object_type == ObjType.binaryInput.name:  # BI
                        binary_input.append(payload([point_object_id, object_name, present_value]))
                    elif object_type == ObjType.binaryOutput.name:  # BO
                        binary_output.append(payload([point_object_id, object_name, present_value]))
                    elif object_type == ObjType.binaryValue.name:  # BV
                        binary_value.append(payload([point_object_id, object_name, present_value]))
                    elif object_type == ObjType.multiStateInput.name:  # MI
                        multi_state_input.append(payload([point_object_id, object_name, present_value]))
                    elif object_type == ObjType.multiStateOutput.name:  # MO
                        multi_state_output.append(payload([point_object_id, object_name, present_value]))
                    elif object_type == ObjType.multiStateValue.name:  # MV
                        multi_state_value.append(payload([point_object_id, object_name, present_value]))
        return {
            "discovered_points": {
                "points": {
                    "analog_input": analog_input,
                    "analog_output": analog_output,
                    "analog_value": analog_value,
                    "binary_input": binary_input,
                    "binary_output": binary_output,
                    "binary_value": binary_value,
                    "multi_state_input": multi_state_input,
                    "multi_state_output": multi_state_output,
                    "multi_state_value": multi_state_value,
                }
            },
            "discovery_errors": {},
            "added_points_count": 0,

            "added_points": {},
            "existing_or_failed_points": {}
        }

    def build_point_list_new(self, device, **kwargs):
        network_instance = self._get_network_from_device(device)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        get_point_priority = kwargs.get('object_type')
        timeout = 1
        logger.info(f"POLL-POINTS discovery/read object list")
        try:
            object_list = network_instance.read(self._common_object(device), timeout=timeout)
            return object_list
        except Exception as e:
            logger.error(
                f"Exception: on build points list cant see device {device.device_name}  msg: {e} ")
            return f"Exception: on build points list cant see device {device.device_name}  msg: {e} "

    def get_object_list(self, device):
        network_instance = self._get_network_from_device(device)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        read = self._common_object(device)
        try:
            if network_instance:
                return network_instance.read(read)
        except:
            return {}

    def whois(self, network_uuid, **kwargs):
        net = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        network_instance = self._get_network_from_network(net)
        if not network_instance:
            raise BACnetNetworkInstanceError("BACnet network instance is error: check IP network settings")
        min_range = 0
        max_range = 4194302
        full_range = kwargs.get('full_range', False)
        is_mstp = kwargs.get('is_mstp')
        show_supported_services = kwargs.get('show_supported_services')
        if full_range:
            range_start = min_range
            range_end = max_range
        else:
            range_start = kwargs.get('range_start', min_range)
            if range_start < min_range:
                range_start = min_range
            range_end = kwargs.get('range_end', max_range)
            if range_end > max_range:
                range_end = max_range
        network_number = kwargs.get('network_number', 0)
        network_number = BACnetFunctions.network_number(network_number)
        whois = kwargs.get('whois', True)
        global_broadcast = kwargs.get('global_broadcast', False)
        who = BACnetFunctions.common_whois(range_start=range_start,
                                           range_end=range_end,
                                           network_number=network_number,
                                           is_mstp=is_mstp)
        try:
            if whois:
                logger.info(f"WHOIS:{who}")
                whois_response = network_instance.whois(who, global_broadcast)
                logger.info(f"WHOIS response:{whois_response}")
                _whois_response = BACnetFunctions.whois_is_build(whois_response, network_instance,
                                                                 show_supported_services)
                return _whois_response

            else:
                if network_number == 0:
                    logger.info(f"WHOIS DISCOVER without network number:{who}")
                    network_instance.discover(limits=(range_start, range_end), global_broadcast=global_broadcast)
                    logger.info(f"WHOIS response:{network_instance.devices}")
                    _whois_response = BACnetFunctions.whois_is_build(network_instance.devices, network_instance,
                                                                     show_supported_services)
                    return _whois_response

                else:
                    logger.info(f"WHOIS DISCOVER with network number:{who}")
                    network_instance.discover(networks=[network_number], limits=(range_start, range_end),
                                              global_broadcast=global_broadcast)
                    logger.info(f"WHOIS response:{network_instance.devices}")
                    _whois_response = BACnetFunctions.whois_is_build(network_instance.devices, network_instance,
                                                                     show_supported_services)
                    return _whois_response

        except Exception as e:
            logger.error(f"WHO IS error: {e}")
            return {}
