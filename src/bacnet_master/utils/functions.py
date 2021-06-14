from src.utils.functions import Functions


class BACnetFunctions:

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
        if isinstance(payload, (int, float)):
            return payload
        elif payload == "active":
            return 1
        elif payload == "inactive":
            return 0
        elif payload == True:
            return 1
        elif payload == False:
            return 0

    @staticmethod
    def common_whois(**kwargs):
        device_range_start = kwargs.get('range_start')
        device_range_end = kwargs.get('range_end')
        network_number = kwargs.get('network_number')
        if network_number != 0:
            return f'{network_number}:{device_range_start} {device_range_end}'
        else:
            return f'{device_range_start} {device_range_end}'

    @staticmethod
    def build_url(device=None, **kwargs):
        if isinstance(device, dict):
            ip = kwargs.get('device_ip') or device.get("device_ip")
            mask = kwargs.get('device_mask') or device.get("device_mask")
            port = kwargs.get('device_port') or device.get("device_port")
        else:
            ip = kwargs.get('device_ip') or device.device_ip
            mask = kwargs.get('device_mask') or device.device_mask
            port = kwargs.get('device_port') or device.device_port
        if mask is not None:
            if port is not None:
                return f"{ip}/{mask}:{port}"
            else:
                return f"{ip}/{mask}"
        else:
            return ip

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
        if len(_list) == 2:
            try:
                val = _list[0].split(':')
                if Functions.is_valid_ip(val[0]):
                    device_ip = val[0]
                else:
                    network_number = val[0]
                    device_mac = val[1]
                    if device_mac >= 1:
                        type_mstp = True
                device_object_id = _list[1]
                device_name = f"dev_{device_object_id}"
            except:
                pass
            return {
                "vendor_name": vendor_name,
                "device_name": device_name,
                "device_ip": device_ip,
                "network_number": network_number,
                "device_mac": device_mac,
                "device_object_id": device_object_id,
                "type_mstp": type_mstp,
                "supports_rpm": False,
                "supports_wpm": False
            }
        elif len(_list) == 4:
            try:
                val = _list[2].split(':')
                if Functions.is_valid_ip(val[0]):
                    device_ip = val[0]
                else:
                    network_number = val[0]
                    device_mac = val[1]
                    if device_mac >= 1:
                        type_mstp = True
                device_object_id = _list[3]
                device_name = _list[0]
            except:
                pass
            return {
                "vendor_name": vendor_name,
                "device_name": device_name,
                "device_ip": device_ip,
                "network_number": network_number,
                "device_mac": device_mac,
                "device_object_id": device_object_id,
                "type_mstp": type_mstp,
                "supports_rpm": False,
                "supports_wpm": False
            }
