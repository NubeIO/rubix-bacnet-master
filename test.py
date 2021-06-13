# from src.bacnet_master.interfaces.device import ObjType
import ipaddress

dis = [
    [
        "Nube-IO",
        "Nube iO Operations Pty Ltd",
        "192.168.15.101",
        123
    ]
]

dis_is_network = [
    [
        "Nube-IO",
        "Nube iO Operations Pty Ltd",
        "1000:1",
        123
    ]
]

who_is = [
    [
        "192.168.15.101",
        123
    ]
]

who_is_network = [
    [
        "1000:1",  # network:mac
        123  # device id
    ]
]



# def split_device_address(_list: list) -> dict:
#     device_ip = None
#     network_number = 0
#     device_mac = 0
#     device_name = None
#     vendor_name = None
#     device_object_id = None
#     if len(_list) == 2:
#         try:
#             val = _list[0].split(':')
#             if is_valid_ip(val[0]):
#                 device_ip = val[0]
#             else:
#                 network_number = val[0]
#                 device_mac = val[1]
#             device_object_id = _list[1]
#             device_name = f"dev_{device_object_id}"
#         except:
#             pass
#         return {
#             "vendor_name": vendor_name,
#             "device_name": device_name,
#             "device_ip": device_ip,
#             "network_number": network_number,
#             "device_mac": device_mac,
#             "device_object_id": device_object_id
#         }
#     elif len(_list) == 4:
#         try:
#             val = _list[2].split(':')
#             if is_valid_ip(val[0]):
#                 device_ip = val[0]
#             else:
#                 network_number = val[0]
#                 device_mac = val[1]
#             device_object_id = _list[3]
#             device_name = _list[0]
#         except:
#             pass
#         return {
#             "vendor_name": vendor_name,
#             "device_name": device_name,
#             "device_ip": device_ip,
#             "network_number": network_number,
#             "device_mac": device_mac,
#             "device_object_id": device_object_id
#         }




for objects in dis:
    print(split_device_address(objects))

for objects in who_is_network:
    print(split_device_address(objects))

for objects in who_is:
    print(split_device_address(objects))