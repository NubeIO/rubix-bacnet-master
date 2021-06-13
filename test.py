# from src.bacnet_master.interfaces.device import ObjType
import ipaddress

devices = {
    'dev_123': {'vendor_name': None, 'device_name': 'dev_123', 'device_ip': '192.168.15.101', 'network_number': 0,
                'device_mac': 0, 'device_object_id': 123},
    'dev_260001': {'vendor_name': None, 'device_name': 'dev_260001', 'device_ip': '192.168.15.12', 'network_number': 0,
                   'device_mac': 0, 'device_object_id': 260001}}

for idx, device in enumerate(devices):
    _device = devices.get(device)
    device_name = _device.get("device_name")
    device_ip = _device.get("device_ip")
    device_mask = _device.get("device_mask")
    device_port = _device.get("device_port")
    device_mac = _device.get("device_mac")
    device_object_id = _device.get("device_object_id")
    network_number = _device.get("network_number")
    type_mstp = _device.get("type_mstp")
    network_uuid = "network_uuid"
    body = {
        "device_name": device_name,
        "device_ip": device_ip,
        "device_mask": device_mask,
        "device_port": device_port,
        "device_mac": device_mac,
        "device_object_id": device_object_id,
        "network_number": network_number,
        "type_mstp": type_mstp,
        "network_uuid": network_uuid
    }
    print(body)
