
import BAC0

bacnet = BAC0.lite()




# print(bacnet.readMultiple('192.168.15.202 device 202 all'))
# print(bacnet.readMultiple('192.168.15.202 binaryOutput 1 all'))
# print(bacnet.readMultiple('192.168.15.202 binaryOutput 1 85'))
aa = bacnet.read('192.168.15.202 analogOutput 1 87')


def serialize_priority_array(priority_array):
    priority_array_dict = {}
    for i in range(16):
        priority_array_dict[f'_{i + 1}'] = None if list(priority_array[i].keys())[0] == 'null' else \
            list(priority_array[i].values())[0]
    return priority_array_dict


r = bacnet.read('192.168.15.202 analogOutput 1 87')
r = serialize_priority_array(r.dict_contents())
print(r)
# # Write null @ 16
# address = '192.168.15.196'
# object_type = 'device'
# object_instance = "1234"
#
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
