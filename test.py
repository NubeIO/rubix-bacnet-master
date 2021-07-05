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


# print(hex2ip("C0A80F65"))
# print(ip2bin("192.168.15.202"))
# print(ip2hex("10.4.8.131"))
print(hex2ip("0A0408A7"))
