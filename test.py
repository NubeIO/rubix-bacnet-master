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


aa = {'analog_inputs': [], 'analog_outputs': [], 'analog_values': [], 'binary_input': [], 'binary_output': [], 'binary_value': [], 'multi_state_input': [], 'multi_state_output': [], 'multi_state_value': [{'point_object_id': 0, 'point_name': None, 'point_value': None}, {'point_object_id': 1, 'point_name': '0:capture command', 'point_value': 1}, {'point_object_id': 2, 'point_name': '1:capture buf_size', 'point_value': 1}, {'point_object_id': 3, 'point_name': '1:capture command', 'point_value': 1}]}

print(aa.get('multi_state_value'))
