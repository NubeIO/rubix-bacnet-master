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


aa = {
    "points_IO-30S-BM_ec799194f1df9502": {
        "discovered_points": {
            "analog_inputs": [
                {
                    "point_object_id": 1,
                    "point_name": "AI 1 222222",
                    "point_value": "null"
                }
                ]
        }
    }
}

a = {}
for key, value in aa.items():
    a.update(value)
print(a)
