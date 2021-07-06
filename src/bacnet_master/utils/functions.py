import logging

import requests
from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.interfaces.device_supported_services import SupportedServices
from src.bacnet_master.interfaces.object_property import ObjProperty
from src.utils.functions import Functions

logger = logging.getLogger(__name__)


class BACnetFunctions:

    @staticmethod
    def validate_timeout(timeout: int) -> int:
        """
        validate timeout is an int and between 0 to 120 sec
        :param timeout:
        :return:
        """
        if not timeout:
            return 1
        timeout = Functions.to_int(timeout)
        _timeout = timeout in range(1, 120)
        if _timeout:
            return timeout
        else:
            return 1

    @staticmethod
    def bacnet_mac_address(mac_address: int) -> bool:
        """
        check if mac address is between 0 to 254
        :param mac_address:
        :return:
        """
        return mac_address in range(0, 255)

    @staticmethod
    def validate_network_number(network_number: int) -> bool:
        """
        check if network number is between 0 and 65534
        :param network_number:
        :return:
        """
        return network_number in range(0, 65534)

    @staticmethod
    def network_number(network_number: int) -> int:
        min_range = 0
        max_range = 65534
        if network_number == 0:
            return network_number
        elif network_number < min_range:
            return min_range
        elif network_number > max_range:
            return max_range
        else:
            return network_number

    @staticmethod
    def clean_point_value(payload):
        if payload == float("inf"):
            return -9999999999
        if payload == float("-inf"):
            return -9999999999
        if isinstance(payload, (int, float)):
            return payload
        elif payload == "active":
            return 1
        elif payload == "inactive":
            return 0
        elif payload:
            return 1
        elif not payload:
            return 0

    @staticmethod
    def clean_active_inactive(payload):
        if isinstance(payload, str):
            if payload == "active":
                return 1
            elif payload == "inactive":
                return 0
            else:
                return payload
        else:
            return payload

    @staticmethod
    def common_whois(**kwargs):
        device_range_start = kwargs.get('range_start')
        device_range_end = kwargs.get('range_end')
        network_number = kwargs.get('network_number')
        is_mstp = kwargs.get('is_mstp')
        if is_mstp:
            return f'{network_number}:*'
        if network_number != 0:
            return f'{network_number}:{device_range_start} {device_range_end}'
        else:
            return f'{device_range_start} {device_range_end}'

    @staticmethod
    def build_device_bac0_call(**kwargs):
        dev_url = kwargs.get("dev_url")
        network_number = kwargs.get("network_number")
        network_number = BACnetFunctions.network_number(network_number)
        device_mac = kwargs.get("device_mac")
        if device_mac >= 1:
            return f'{network_number}:{device_mac}'
        if network_number != 0:
            return f'{network_number}:{dev_url}'
        else:
            return f'{dev_url}'

    @staticmethod
    def build_url(device=None, **kwargs):
        if isinstance(device, dict):
            ip = kwargs.get('device_ip')
            mask = kwargs.get('device_mask')
            port = kwargs.get('device_port')

        elif device:
            ip = device.device_ip
            mask = device.device_mask
            port = device.device_port
        else:
            ip = kwargs.get('device_ip')
            mask = kwargs.get('device_mask')
            port = kwargs.get('device_port')

        if mask is not None:
            if port is not None:
                out = f"{ip}/{mask}:{port}"
                logger.info(f"FUNCTION BUILD URL ip/mask:port:{out}")
                return out
            else:
                out = f"{ip}/{mask}"
                logger.info(f"FUNCTION BUILD URL ip/mask:{out}")
                return out

        else:
            out = ip
            logger.info(f"FUNCTION BUILD URL ip:{out}")
            return out

    @staticmethod
    def check_priority(value) -> bool:
        """
        check if priority input is between 1 and 16
        :param value:
        :return:
        """
        return value in range(1, 17)

    @staticmethod
    def serialize_priority_array(priority_array) -> dict:
        """
        converts a bacpypes priority object to a dict
        :param priority_array:
        :return:
        """
        priority_array_dict = {}
        for i in range(16):
            priority_array_dict[f'_{i + 1}'] = None if list(priority_array[i].keys())[0] == 'null' else \
                list(priority_array[i].values())[0]
        return priority_array_dict

    @staticmethod
    def who_add_devices(devices, network_uuid):
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
            supports_rpm = _device.get("supports_rpm")
            supports_wpm = _device.get("supports_wpm")
            supported_services = _device.get("supported_services")
            ethernet_mac_address = _device.get("ethernet_mac_address")
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
                "supports_rpm": supports_rpm,
                "supports_wpm": supports_wpm,
                "network_uuid": network_uuid,
                "supported_services": supported_services,
                "ethernet_mac_address": ethernet_mac_address,
            }
            res = requests.put(url,
                               headers={'Content-Type': 'application/json'},
                               json=body)

            if res.status_code == 200:
                count = count + 1
                uuid = res.json().get("device_uuid")
                name = f"{device_name}_{uuid}"
                body.update({"device_uuid": uuid})
                dev = {name: body}

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

    @staticmethod
    def add_points(device_uuid, points, device_name):
        host = '0.0.0.0'
        port = '1718'
        url = f"http://{host}:{port}/api/bm/point"
        count = 0
        added_analog_inputs = []
        added_analog_outputs = []
        added_analog_values = []
        added_binary_input = []
        added_binary_output = []
        added_binary_value = []
        added_multi_state_input = []
        added_multi_state_output = []
        added_multi_state_value = []
        failed_analog_inputs = []
        failed_analog_outputs = []
        failed_analog_values = []
        failed_binary_input = []
        failed_binary_output = []
        failed_binary_value = []
        failed_multi_state_input = []
        failed_multi_state_output = []
        failed_multi_state_value = []
        points = points.get("discovered_points")
        points = points.get("points")
        for point_group in list(points):
            _point_group = points.get(point_group)
            if _point_group:
                for point in _point_group:
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
                    logger.info(
                        f"PASS -> ADD POINTS: HTTP BODY:{body}")
                    res = requests.put(url,
                                       headers={'Content-Type': 'application/json'},
                                       json=body)

                    count = count + 1
                    if res.status_code == 200:
                        logger.info(
                            f"PASS -> ADD POINTS: device_name:{device_name}: point_name{point_name}: status_code:{res.status_code}")
                    else:
                        logger.info(
                            f"ERROR > ADD POINTS: device_name:{device_name}: point_name{point_name}: status_code:{res.status_code}, text:{res.text}")
                    if point_object_type.name == ObjType.analogInput.name:
                        if res.status_code == 200:
                            added_analog_inputs.append(body)
                        else:
                            failed_analog_inputs.append(body)
                    elif point_object_type.name == ObjType.analogOutput.name:
                        if res.status_code == 200:
                            added_analog_outputs.append(body)
                        else:
                            failed_analog_outputs.append(body)
                    elif point_object_type.name == ObjType.analogValue.name:
                        if res.status_code == 200:
                            added_analog_values.append(body)
                        else:
                            failed_analog_values.append(body)
                    elif point_object_type.name == ObjType.binaryInput.name:
                        if res.status_code == 200:
                            added_binary_input.append(body)
                        else:
                            failed_binary_input.append(body)
                    elif point_object_type.name == ObjType.binaryOutput.name:
                        if res.status_code == 200:
                            added_binary_output.append(body)
                        else:
                            failed_binary_output.append(body)
                    elif point_object_type.name == ObjType.binaryValue.name:
                        if res.status_code == 200:
                            added_binary_value.append(body)
                        else:
                            failed_binary_value.append(body)
                    elif point_object_type.name == ObjType.multiStateInput.name:
                        if res.status_code == 200:
                            added_multi_state_input.append(body)
                        else:
                            failed_multi_state_input.append(body)
                    elif point_object_type.name == ObjType.multiStateOutput.name:
                        if res.status_code == 200:
                            added_multi_state_output.append(body)
                        else:
                            failed_multi_state_output.append(body)
                    elif point_object_type.name == ObjType.multiStateValue.name:
                        if res.status_code == 200:
                            added_multi_state_value.append(body)
                        else:
                            failed_multi_state_value.append(body)

        out_dict = {
            "discovered_points": points,
            "discovery_errors": points.get("discovery_errors"),
            "added_points_count": 0,
            "added_points": {
                "points": {
                    "analog_inputs": added_analog_inputs,
                    "analog_outputs": added_analog_outputs,
                    "analog_values": added_analog_values,
                    "binary_input": added_binary_input,
                    "binary_output": added_binary_output,
                    "binary_value": added_binary_value,
                    "multi_state_input": added_multi_state_input,
                    "multi_state_output": added_multi_state_output,
                    "multi_state_value": added_multi_state_value
                },
            },
            "existing_or_failed_points": {
                "points": {
                    "analog_inputs": failed_analog_inputs,
                    "analog_outputs": failed_analog_outputs,
                    "analog_values": failed_analog_values,
                    "binary_input": failed_binary_input,
                    "binary_output": failed_binary_output,
                    "binary_value": failed_binary_value,
                    "multi_state_input": failed_multi_state_input,
                    "multi_state_output": failed_multi_state_output,
                    "multi_state_value": failed_multi_state_value
                },
            },
        }
        return out_dict

    @staticmethod
    def common_object_no_device(**kwargs):
        """192.168.15.202/24:47808 device 202 objectList"""
        dev_url = kwargs.get('dev_url')
        type_mstp = kwargs.get('type_mstp')
        device_mac = kwargs.get('device_mac')
        device_object_id = kwargs.get('device_object_id')
        network_number = kwargs.get('network_number')
        network_number = BACnetFunctions.network_number(network_number)
        object_type = kwargs.get('object_type')
        prop = kwargs.get('prop')
        ethernet_mac_address = kwargs.get('ethernet_mac_address')
        if ethernet_mac_address:
            return f'{network_number}:{ethernet_mac_address} {object_type} {device_object_id} {prop}'
        if type_mstp:
            return f'{network_number}:{device_mac} {object_type} {device_object_id} {prop}'
        if network_number != 0:
            return f'{network_number}:{dev_url} {object_type} {device_object_id} {prop}'
        else:
            return f'{dev_url} {object_type} {device_object_id} {prop}'

    @staticmethod
    def whois_is_build(read, network_instance, show_supported_services) -> dict:
        logger.info(f"WHOIS response raw:{read}")
        _dict = {}
        count = 0
        for objects in read:
            count = count + 1
            each_device = BACnetFunctions.whois_split(objects)
            device_name = each_device.get('device_name')
            device_ip = each_device.get('device_ip')
            device_mac = each_device.get('device_mac')
            device_mask = each_device.get('device_mask')
            device_port = each_device.get('device_port')
            type_mstp = each_device.get('type_mstp')
            network_number = each_device.get('network_number')
            device_object_id = each_device.get('device_object_id')
            ethernet_mac_address = each_device.get('ethernet_mac_address')
            if ethernet_mac_address:
                device_name = f"{device_name}_{ethernet_mac_address}"
            logger.info(f"WHOIS device_name:{device_name} ethernet_mac_address{ethernet_mac_address}")
            dev_url = BACnetFunctions.build_url(device_ip=device_ip,
                                                device_mask=device_mask, device_port=device_port)
            if show_supported_services:
                get_ss = BACnetFunctions.common_object_no_device(
                    dev_url=dev_url,
                    device_mac=device_mac,
                    type_mstp=type_mstp,
                    network_number=network_number,
                    device_object_id=device_object_id,
                    object_type=ObjType.device.name,
                    prop=ObjProperty.protocolServicesSupported.name,
                    ethernet_mac_address=ethernet_mac_address
                )
                _get_ss = network_instance.read(get_ss)
                supported_services = SupportedServices.check_supported_services(_get_ss)
                logger.info(f"WHOIS protocolServicesSupported:{supported_services}")
                each_device["supports_rpm"] = supported_services.get("readPropertyMultiple")
                each_device["supports_wpm"] = supported_services.get("writePropertyMultiple")
                each_device.update({"supported_services": {}})
                each_device.update({"supported_services": supported_services})
                _dict.update({device_name: each_device})
            else:
                _dict.update({device_name: each_device})
        logger.info(f"WHOIS response  devices count found:{count}")
        logger.info(f"WHOIS response  devices found after clean:{_dict}")
        return _dict

    @staticmethod
    def whois_split(_list: list) -> dict:
        """
        converts a whois call into a dict and extracts the network_number and mac_address
        :param _list:
        :return:
        """
        device_ip = None
        network_number = 0
        device_mac = 0
        device_name = None
        vendor_name = None
        device_object_id = None
        type_mstp = False
        supports_rpm = False
        supports_wpm = False
        device_port = 47808
        device_mask = 24
        ethernet_mac_address = None  # example ('1:0x000000002939', 10553)
        manufacture = None
        # _list = ('1:0x000000002939', 10553)
        logger.error(f"FUNCTION whois_split _list: {_list}")
        if len(_list) == 2:
            try:
                val = _list[0].split(':')
                if Functions.is_valid_ip(val[0]):
                    device_ip = val[0]
                else:
                    network_number = val[0]
                    network_number = Functions.to_int(network_number)
                    device_ip = "0.0.0.0"
                    _mac = val[1]
                    if len(_mac) <= 4:
                        device_mac = Functions.to_int(_mac)
                        type_mstp = True
                    else:
                        ethernet_mac_address = _mac
                    device_port = 0
                    device_mask = 0
                device_object_id = _list[1]
                device_name = f"dev_{device_object_id}"
            except ValueError as e:
                logger.error(f"FUNCTION whois_split: {e}")
                pass
            logger.info(
                f"FUNCTION  whois_split:{device_name} device_ip{device_ip} device_port{device_port} "
                f"network_number{network_number} type_mstp{type_mstp} "
                f"device_mac:{device_mac} ethernet_mac_address{ethernet_mac_address}")
            return {
                "vendor_name": vendor_name,
                "device_name": device_name,
                "device_ip": device_ip,
                "network_number": network_number,
                "device_mac": device_mac,
                "device_object_id": device_object_id,
                "type_mstp": type_mstp,
                "supports_rpm": supports_rpm,
                "supports_wpm": supports_wpm,
                "device_port": device_port,
                "device_mask": device_mask,
                "ethernet_mac_address": ethernet_mac_address,
                "manufacture": manufacture
            }
        elif len(_list) == 4:
            try:
                val = _list[2].split(':')
                if Functions.is_valid_ip(val[0]):
                    device_ip = val[0]
                else:
                    network_number = val[0]
                    network_number = Functions.to_int(network_number)
                    device_ip = "0.0.0.0"
                    _mac = val[1]
                    if len(_mac) <= 4:
                        device_mac = Functions.to_int(_mac)
                        type_mstp = True
                    else:
                        ethernet_mac_address = _mac
                    device_port = 0
                    device_mask = 0
                device_object_id = _list[3]
                manufacture = _list[1]
                if _list[0] is not None:
                    device_name = f"dev_{device_object_id}_na_{Functions.make_uuid()[6:-6]}"
            except ValueError as e:
                logger.error(f"FUNCTION whois clean: {e}")
                pass
            logger.info(
                f"FUNCTION whois_split:{device_name} device_ip{device_ip} device_port{device_port} "
                f"network_number{network_number} type_mstp{type_mstp} device_mac:{device_mac} "
                f"ethernet_mac_address{ethernet_mac_address}")
            return {
                "vendor_name": vendor_name,
                "device_name": device_name,
                "device_ip": device_ip,
                "network_number": network_number,
                "device_mac": device_mac,
                "device_object_id": device_object_id,
                "type_mstp": type_mstp,
                "supports_rpm": supports_rpm,
                "supports_wpm": supports_wpm,
                "device_port": device_port,
                "device_mask": device_mask,
                "ethernet_mac_address": ethernet_mac_address,
                "manufacture": manufacture
            }
