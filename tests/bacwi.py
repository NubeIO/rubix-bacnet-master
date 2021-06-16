import BAC0

bacnet = BAC0.lite()

# print(bacnet.discover(networks=[1001]))
# print(bacnet.discover(networks='known'))
# print(bacnet.discover())
# print(bacnet.discover(networks='known', limits=(0,4194303), global_broadcast=False))
# print(bacnet.discover())
# print(bacnet.devices)
# print(bacnet.whois("255.255.255.255/24"))
# print(bacnet.whois("0.0.0.0/24"))
# print(bacnet.whois("255.255.255.0/24"))
# print(bacnet.whois("192.168.15.255/24"))
# print(bacnet.whois("192.168.15.255"))
# print(bacnet.whois("1001:*"))
# print(bacnet.whois("255.255.255.0/24"))
# print(bacnet.whois("255.255.255.0/24"))
# print(bacnet.whois('1001:*'))
# print(bacnet.whois(global_broadcast=False))  # WhoIs broadcast globally.  Every device will respond with an IAm
# print(bacnet.whois('1001:31'))  # WhoIs looking for the device at (Network 1001, Address 31)
# print(bacnet.whois('1001:10 1000'))  # WhoIs looking for the device at (Network 1001, Devices in the ID range (10 - 1000))
# print(bacnet.whois('10 1000'))  # WhoIs looking for devices in the ID range (10 - 1000)
print(bacnet.whois("1001:*"))  # all devices on network 1001
# print(bacnet.devices)

# read_vals = f' 192.168.15.202 device 202 objectList'
# #
# points = bacnet.read(read_vals)
# print(points)

