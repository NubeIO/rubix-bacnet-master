import logging
import BAC0
from BAC0.core.io.IOExceptions import UnknownObjectError, NoResponseFromController

from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.interfaces.device_supported_services import SupportedServices
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

    def _common_point(self, point, device, **kwargs):
        dev_url = kwargs.get('dev_url') or BACnetFunctions.build_url(device)
        network_number = kwargs.get('network_number') or device.network_number
        network_number = BACnetFunctions.network_number(network_number)
        object_instance = kwargs.get('object_instance') or point.point_object_id
        object_type = kwargs.get('object_type') or point.point_object_type.name
        prop = kwargs.get('prop') or ObjProperty.presentValue.name
        type_mstp = kwargs.get('type_mstp') or device.type_mstp
        device_mac = kwargs.get('device_mac') or device.device_mac
        logger.info(f"DO POINT READ dev_url:{dev_url}, type_mstp:{type_mstp}, "
                    f"device_mac:{device_mac}, object_instance:{object_instance},  "
                    f"object_type:{object_type},  prop:{prop}, "
                    f"network_number:{network_number}")
        if type_mstp:
            return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        if network_number != 0:
            return f'{network_number}:{dev_url} {object_type} {object_instance} {prop}'
        else:
            return f'{dev_url} {object_type} {object_instance} {prop}'

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
        if type_mstp:
            return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
        if network_number != 0:
            return f'{network_number}:{dev_url} {object_type} {object_instance} {prop}'
        else:
            return f'{dev_url} {object_type} {object_instance} {prop}'



    def _get_objects_unknown(self, device, **kwargs):
        """192.168.15.202/24:47808 device 202 objectList"""
        dev_url = BACnetFunctions.build_url(device)
        type_mstp = device.get("type_mstp", False)
        device_mac = device.get("device_mac", 0)
        object_instance = kwargs.get('object_instance') or device.get("device_object_id")
        network_number = device.get("network_number")
        network_number = BACnetFunctions.network_number(network_number)
        object_type = kwargs.get('object_type') or ObjType.device.name
        prop = kwargs.get('prop') or ObjProperty.objectList.name
        build_device_address = device.get("build_device_address")
        logger.info(f"GET DEVICE OBJECT LIST  dev_url:{dev_url}, type_mstp:{type_mstp}, "
                    f"device_mac:{device_mac}, device_object_id:{object_instance}, "
                    f"network_number:{network_number}")
        if not build_device_address:
            if type_mstp:
                logger.info(f"GET DEVICE OBJECT LIST - TYPE MSTP")
                return f'{network_number}:{device_mac} {object_type} {object_instance} {prop}'
            if network_number != 0:
                logger.info(f"GET DEVICE OBJECT LIST - TYPE IP with network number{network_number}")
                return f'{network_number}:{dev_url} {object_type} {object_instance} {prop}'
            else:
                logger.info(f"GET DEVICE OBJECT LIST - TYPE IP with NO network number{network_number}")
                return f'{dev_url} {object_type} {object_instance} {prop}'
        else:
            if type_mstp:
                logger.info(f"BUILD DEVICE ADDRESS - TYPE MSTP: {network_number}:{device_mac}")
                return f'{network_number}:{device_mac}'
            if network_number != 0:
                logger.info(f"BUILD DEVICE ADDRESS  - TYPE IP with network number:{network_number}:{dev_url}")
                return f'{network_number}:{dev_url}'
            else:
                logger.info(f"BUILD DEVICE ADDRESS  - TYPE IP with dev_url:{dev_url}")
                return f'{dev_url}'

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
            except NoResponseFromController as e:
                logger.error(
                    f"NoResponseFromController: {point.point_object_type.name}:{point.point_object_id}  priority:{priority} msg: {e}")
                return f"{point.point_object_type.name}:{point.point_object_id} priority:{priority} msg: {e}"
            except Exception as e:
                logger.error(f"{cmd} point write value error: {e}")
                return f"{point.point_object_type.name}:{point.point_object_id} priority:{priority} msg: {e}"

    # @staticmethod
    # def get_device_address(device_id, network):
    #     address, _device_id = next(
    #         (k for k in network.whois(str(device_id)).keys()
    #          if (isinstance(k, tuple)) and k[1] == device_id), (None, None)
    #     )
    #     if address is None:
    #         raise ValueError('No device found with device_id=%s on network: %s'
    #                          % (device_id, network,))
    #     return address

    def read_point_list_by_network(self, network, network_uuid, timeout):
        net = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not net:
            return {"net": "net is none"}
        network_instance = self._get_network_from_network(net)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        props = [ObjProperty.objectName.name, ObjProperty.presentValue.name]
        _list = {}
        build_points_list = {}
        for device in network.get("devices"):
            network_uuid = device["network_uuid"]
            device_name = device["device_name"]
            device_uuid = device["device_uuid"]
            device_object_id = device["device_object_id"]
            device_ip = device["device_ip"]
            network_number = device["network_number"]
            type_mstp = device["type_mstp"]
            supports_rpm = device["supports_rpm"]
            supports_wpm = device["supports_wpm"]
            address = self._get_objects_unknown(device,
                                                build_device_address=True
                                                )
            point_uuid_list = []
            point_name_list = []
            for point in device.get("points"):
                for items in point:
                    point_object_type = point.get("point_object_type")
                    point_object_type = ObjType.has_value_from_string(point_object_type).get("name")
                    point_uuid = point.get("point_uuid")
                    point_uuid_list.append(point_uuid)
                    point_uuid_list = list(dict.fromkeys(point_uuid_list))
                    point_name = point.get("point_name")
                    point_name_list.append(point_name)
                    point_name_list = list(dict.fromkeys(point_name_list))
                    point_object_id = point.get("point_object_id")
                    point_key = f"{point_object_type}:{point_object_id}"
                    _list.update({point_key: props})
            _rpm = {'address': address,
                    'objects': _list
                    }
            objects_dict = _rpm.get("objects")
            bacnet_return = ['']
            if objects_dict:
                bacnet_return = network_instance.readMultiple(device_ip, _rpm, timeout=timeout)
            if bacnet_return != ['']:
                count = 0
                for _point in list(bacnet_return):
                    device_points = bacnet_return.get(_point)
                    point_uuid = point_uuid_list[count]
                    new_point_uuid = ("uuid", point_uuid)
                    device_points.append(new_point_uuid)
                    point_name = None
                    # TODO remove this and fix it (made all point names unique )
                    try:
                        point_name = point_name_list[count]
                    except:
                        logger.info(f"ERROR on: read_point_list_by_network")
                    new_point_name = ("name", point_name)
                    device_points.append(new_point_name)
                    new_point_key = f"{_point[0]}_{_point[1]}"
                    bacnet_return[new_point_key] = bacnet_return.pop(_point)
                    count = count + 1
                    for _objects in list(device_points):
                        _device_points = device_points
                        for iii in list(_device_points):
                            try:
                                obj = f"{_objects[0]}"
                                value = f"{_objects[1]}"
                                value = BACnetFunctions.clean_active_inactive(value)
                                new_object = {obj: value}
                                _device_points.remove(_objects)
                                _device_points.append(new_object)
                            except:
                                logger.info(f"ERROR on: read_point_list_by_network")

                _dev = {
                    device_uuid: {"deviceUUID": device_uuid, "deviceName": device_name, "deviceId": device_object_id,
                                  "points": bacnet_return}}
                build_points_list.update(_dev)
                _list = {}
            else:
                build_points_list.update({device_uuid: "offline"})
                build_points_list[device_uuid] = {"deviceUUID": device_uuid, "deviceName": device_name,
                                                  "deviceId": device_object_id, "points": False}
        points_list = {network_uuid: build_points_list}
        return points_list

    def read_point_list(self, device):
        network_instance = self._get_network_from_device(device)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        analog_inputs = []
        analog_outputs = []
        analog_values = []
        binary_input = []
        binary_output = []
        binary_value = []
        multi_state_input = []
        multi_state_output = []
        multi_state_value = []
        object_list = network_instance.read(self._common_object(device))
        obj_name = ObjProperty.objectName.name
        obj_present_value = ObjProperty.presentValue.name
        point_types = ["analogInput", "analogOutput", "analogValue", "binaryInput", "binaryOutput",
                       "binaryValue", "multiStateInput", "multiStateOutput", "multiStateValue"]

        for obj in object_list:
            object_type = obj[0]
            object_instance = obj[1]
            if object_type in point_types:
                try:
                    point_name = network_instance.read(
                        self._common_object(device,
                                            object_type=object_type,
                                            object_instance=object_instance,
                                            prop=obj_name))
                    point_value = network_instance.read(
                        self._common_object(device,
                                            object_type=object_type,
                                            object_instance=object_instance,
                                            prop=obj_present_value))
                    point_object_id = obj[1]
                    point_value = BACnetFunctions.clean_point_value(point_value)
                    if object_type == "analogInput":
                        analog_inputs.append(
                            {"point_object_id": point_object_id, "point_name": point_name, "point_value": point_value})
                    elif object_type == "analogOutput":
                        analog_outputs.append(
                            {"point_object_id": point_object_id, "point_name": point_name, "point_value": point_value})
                    elif object_type == "analogValue":
                        analog_outputs.append(
                            {"point_object_id": point_object_id, "point_name": point_name, "point_value": point_value})
                    elif object_type == "binaryInput":
                        binary_input.append(
                            {"point_object_id": point_object_id, "point_name": point_name, "point_value": point_value})
                    elif object_type == "binaryOutput":
                        binary_output.append(
                            {"point_object_id": point_object_id, "point_name": point_name, "point_value": point_value})
                    elif object_type == "binaryValue":
                        binary_value.append(
                            {"point_object_id": point_object_id, "point_name": point_name, "point_value": point_value})
                    elif object_type == "multiStateInput":
                        multi_state_input.append(
                            {"point_object_id": point_object_id, "point_name": point_name, "point_value": point_value})
                    elif object_type == "multiStateOutput":
                        multi_state_output.append(
                            {"point_object_id": point_object_id, "point_name": point_name, "point_value": point_value})
                    elif object_type == "multiStateValue":
                        multi_state_value.append(
                            {"point_object_id": point_object_id, "point_name": point_name, "point_value": point_value})
                except BAC0.core.io.IOExceptions.UnknownPropertyError:
                    continue

        points_list = {
            "analog_inputs": analog_inputs,
            "analog_outputs": analog_outputs,
            "analog_values": analog_values,
            "binary_input": binary_input,
            "binary_output": binary_output,
            "binary_value": binary_value,
            "multi_state_input": multi_state_input,
            "multi_state_output": multi_state_output,
            "multi_state_value": multi_state_value,
        }
        return points_list

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
        if not net:
            return {"net": "net is none"}
        network_instance = self._get_network_from_network(net)
        if not network_instance:
            return {"network_instance": "network instance is none"}
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
                _whois_response = BACnetFunctions.whois_is_build(whois_response, network_instance, show_supported_services)
                return _whois_response

            else:
                if network_number == 0:
                    logger.info(f"WHOIS DISCOVER without network number:{who}")
                    network_instance.discover(limits=(range_start, range_end), global_broadcast=global_broadcast)
                    logger.info(f"WHOIS response:{network_instance.devices}")
                    _whois_response = BACnetFunctions.whois_is_build(network_instance.devices, network_instance, show_supported_services)
                    return _whois_response

                else:
                    logger.info(f"WHOIS DISCOVER with network number:{who}")
                    network_instance.discover(networks=[network_number], limits=(range_start, range_end),
                                              global_broadcast=global_broadcast)
                    logger.info(f"WHOIS response:{network_instance.devices}")
                    _whois_response = BACnetFunctions.whois_is_build(network_instance.devices, network_instance, show_supported_services)
                    return _whois_response

        except Exception as e:
            logger.error(f"WHO IS error: {e}")
            return {}

    def unknown_get_object_list(self, net_uuid, device):
        net = BacnetNetworkModel.find_by_network_uuid(net_uuid)
        if not net:
            return {"net": "net is none"}
        network_instance = self._get_network_from_network(net)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        read = self._get_objects_unknown(device)
        try:
            if network_instance:
                return network_instance.read(read)
        except:
            return {}

    def unknown_get_point_pv(self, net_uuid, device):
        net = BacnetNetworkModel.find_by_network_uuid(net_uuid)
        if not net:
            return {"net": "net is none"}
        network_instance = self._get_network_from_network(net)
        if not network_instance:
            return {"network_instance": "network instance is none"}
        object_type = device.get("point_object_type")  # analogOutput
        object_type = ObjType.has_value_from_string(object_type)
        if not object_type:
            return {"object_type": "invalid object type"}
        object_type = object_type.get("name")
        object_instance = device.get("point_object_id")  # 1
        prop = ObjProperty.presentValue.name
        read = self._get_objects_unknown(device, object_type=object_type, object_instance=object_instance, prop=prop)
        try:
            if network_instance:
                return network_instance.read(read)
        except:
            return {}
