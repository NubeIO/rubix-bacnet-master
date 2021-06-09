
import BAC0

from src.bacnet_master.utils.functions import serialize_priority_array

bacnet = BAC0.lite()




# print(bacnet.readMultiple('192.168.15.202 device 202 all'))
# print(bacnet.readMultiple('192.168.15.202 binaryOutput 1 all'))
# print(bacnet.readMultiple('192.168.15.202 binaryOutput 1 85'))
aa = bacnet.read('192.168.15.202 analogOutput 1 87')




r = bacnet.read('192.168.15.202 analogOutput 1 87')
r = serialize_priority_array(r.dict_contents())
print(r)
# # Write null @ 16
# address = '192.168.15.196'
# object_type = 'device'
# object_instance = "1234"
#
# read_vals = bacnet.read('192.168.15.202 analogOutput 1 87')
# read_vals = f'{address} {object_type} {object_instance} 97'

# aaa = SupportedServices.get(address, object_type, object_instance)
# print(aaa)
# #
# ss = bacnet.read(read_vals)
# print(ss)
# print(SupportedServices.check(ss))
# # print(aaaa)

# <addr> <type> <inst> <prop>
# print(bacnet.read('192.168.15.202/24:47808 analogOutput 1 presentValue'))  # or 85
# print(bacnet.read('192.168.15.202/24:47808 analogOutput 1 85'))
# # print(bacnet.read('202 analogOutput 1 85'))
# print(bacnet.read('192.168.15.202/24:47808 device 202 objectList'))  # or 76
# print(bacnet.read('192.168.15.202/24:47808 device 202 76'))
# for x in range(len(ss)):
#     print(22222)
#     print(x)
# # def get_key(val):
#     for key, value in types.items():
#         if val == value:
#             return key
#
#     return "key doesn't exist"
#
#
# readProperty = get_key(14)
# print(aa)
