# import os
# os.chdir('/home/aidan/code/bacnet-stack-bacnet-stack-1.0.0/bin')
# cmd = './bacwi'
# os.system(cmd)  # returns the exit status


import socket, struct


# Convert a hex to IP
def hex2ip(hex_ip):
    addr_long = int(hex_ip, 16)
    hex(addr_long)
    hex_ip = socket.inet_ntoa(struct.pack(">L", addr_long))
    return hex_ip


# Convert IP to bin
def ip2bin(ip):
    ip1 = '.'.join([bin(int(x) + 256)[3:] for x in ip.split('.')])
    return ip1


# Convert IP to hex
def ip2hex(ip):
    ip1 = ''.join([hex(int(x) + 256)[3:] for x in ip.split('.')])
    return ip1


print(hex2ip("C0A80F65"))
print(ip2bin("192.168.15.202"))
print(ip2hex("192.168.15.202"))


aa = {'discovered_points': {'points': {'analog_inputs': [{'point_object_id': 1, 'point_name': 'AI 1 222222', 'point_value': 100.0}, {'point_object_id': 2, 'point_name': 'AI 2', 'point_value': 100.0}, {'point_object_id': 3, 'point_name': 'AI 3', 'point_value': 100.0}, {'point_object_id': 4, 'point_name': 'AI 4', 'point_value': 100.0}, {'point_object_id': 5, 'point_name': 'AI 5', 'point_value': 100.0}, {'point_object_id': 6, 'point_name': 'AI 6', 'point_value': 100.0}, {'point_object_id': 7, 'point_name': 'AI 7', 'point_value': 100.0}, {'point_object_id': 8, 'point_name': 'AI 8', 'point_value': 100.0}], 'analog_outputs': [{'point_object_id': 1, 'point_name': 'CHV_1', 'point_value': 123.0}, {'point_object_id': 2, 'point_name': 'AO 2', 'point_value': 11.0}, {'point_object_id': 3, 'point_name': 'AO 3', 'point_value': 77777.0}, {'point_object_id': 4, 'point_name': 'AO 4', 'point_value': 1.0}], 'analog_values': [], 'binary_input': [{'point_object_id': 1, 'point_name': 'DI 1 10101', 'point_value': 1}, {'point_object_id': 2, 'point_name': 'DI 2', 'point_value': 1}, {'point_object_id': 3, 'point_name': 'DI 3', 'point_value': 1}, {'point_object_id': 4, 'point_name': 'DI 4', 'point_value': 1}, {'point_object_id': 5, 'point_name': 'DI 5', 'point_value': 1}, {'point_object_id': 6, 'point_name': 'DI 6', 'point_value': 1}, {'point_object_id': 7, 'point_name': 'DI 7', 'point_value': 1}, {'point_object_id': 8, 'point_name': 'DI 8 22', 'point_value': 1}, {'point_object_id': 9, 'point_name': 'DI 9', 'point_value': 1}, {'point_object_id': 10, 'point_name': 'DI 10', 'point_value': 1}, {'point_object_id': 11, 'point_name': 'DI 11', 'point_value': 1}, {'point_object_id': 12, 'point_name': 'DI 12', 'point_value': 1}, {'point_object_id': 13, 'point_name': 'DI 13', 'point_value': 1}, {'point_object_id': 14, 'point_name': 'DI 14', 'point_value': 1}, {'point_object_id': 15, 'point_name': 'DI 15', 'point_value': 1}, {'point_object_id': 16, 'point_name': 'DI 16', 'point_value': 1}], 'binary_output': [{'point_object_id': 1, 'point_name': 'DO 1', 'point_value': 0}, {'point_object_id': 2, 'point_name': 'DO 2', 'point_value': 0}, {'point_object_id': 3, 'point_name': 'DO 3', 'point_value': 0}, {'point_object_id': 4, 'point_name': 'DO 4', 'point_value': 0}, {'point_object_id': 5, 'point_name': 'DO 5', 'point_value': 0}, {'point_object_id': 6, 'point_name': 'DO 6', 'point_value': 0}, {'point_object_id': 7, 'point_name': 'DO 7', 'point_value': 0}, {'point_object_id': 8, 'point_name': 'DO 8', 'point_value': 0}], 'binary_value': [], 'multi_state_input': [], 'multi_state_output': [], 'multi_state_value': []}}, 'discovery_errors': 'discovery_errors', 'added_points_count': 0, 'added_points': {}, 'existing_or_failed_points': {}}
aa = aa.get("discovered_points")
aa = aa.get("points")
for i in aa:
    print(i)

# for key, value in enumerate(aa):
#     _rpm = {'address': '1001:1',
#             "objects": value
#             }
#
#     print(_rpm)

