import time

# import BAC0
#
# bacnet = BAC0.lite('192.168.15.102/24:47808')

# points = device.points
# print(points)
#
import BAC0

bacnet = BAC0.lite()

rpm = {'address': '1001:1',
       'objects': {'analogInput:1': ['objectName', 'presentValue'], 'analogInput:2': ['objectName', 'presentValue'],
                   'analogInput:3': ['objectName', 'presentValue'], 'analogInput:4': ['objectName', 'presentValue'],
                   'analogInput:5': ['objectName', 'presentValue'], 'analogInput:6': ['objectName', 'presentValue'],
                   'analogInput:7': ['objectName', 'presentValue'], 'analogInput:8': ['objectName', 'presentValue'],
                   'analogOutput:1': ['objectName', 'presentValue'], 'analogOutput:2': ['objectName', 'presentValue'],
                   'analogOutput:3': ['objectName', 'presentValue'], 'analogOutput:4': ['objectName', 'presentValue'],
                   'binaryInput:1': ['objectName', 'presentValue'], 'binaryInput:2': ['objectName', 'presentValue'],
                   'binaryInput:3': ['objectName', 'presentValue'], 'binaryInput:4': ['objectName', 'presentValue'],
                   'binaryInput:5': ['objectName', 'presentValue'], 'binaryInput:6': ['objectName', 'presentValue'],
                   'binaryInput:7': ['objectName', 'presentValue'], 'binaryInput:8': ['objectName', 'presentValue'],
                   'binaryInput:9': ['objectName', 'presentValue'], 'binaryInput:10': ['objectName', 'presentValue'],
                   'binaryInput:11': ['objectName', 'presentValue'], 'binaryInput:12': ['objectName', 'presentValue'],
                   'binaryInput:13': ['objectName', 'presentValue'], 'binaryInput:14': ['objectName', 'presentValue'],
                   'binaryInput:15': ['objectName', 'presentValue'], 'binaryInput:16': ['objectName', 'presentValue'],
                   'binaryOutput:1': ['objectName', 'presentValue'], 'binaryOutput:2': ['objectName', 'presentValue'],
                   'binaryOutput:3': ['objectName', 'presentValue'], 'binaryOutput:4': ['objectName', 'presentValue'],
                   'binaryOutput:5': ['objectName', 'presentValue'], 'binaryOutput:6': ['objectName', 'presentValue'],
                   'binaryOutput:7': ['objectName', 'presentValue'], 'binaryOutput:8': ['objectName', 'presentValue']}}
_rpm = {'address': '1001:1',
        'objects': {
            'analogOutput:1': ['objectName', 'presentValue'],
            'analogOutput:2': ['objectName', 'presentValue']
        }
        }

# print(bacnet.read('192.168.15.202 device 202 objectList'))
# network_instance.readMultiple(device_ip, _rpm, timeout=timeout)
# print(bacnet.read('1001:1 analogOutput 1 presentValue'))
print(bacnet.readMultiple('1001:1', request_dict=_rpm))

# so my issue is this
# this is what the func can take     def readMultiple(self, args, vendor_id=0, timeout=10, prop_id_required=False):
# but this is an older version of bac0
# when i look here it is here
# def readMultiple(
#         self, args, request_dict=None, vendor_id=0, timeout=10, prop_id_required=False
# ):
# so now pls have a look
# is my issue this?

# lst = [("analogOutput", 1), ("analogOutput", 2)]
# for each in lst:
#     # print(bacnet.read("1001:1 {} {} presentValue").format(each[0], each[1]))
#     # print(bacnet.read("192.168.15.202 {} {} presentValue".format(each[0], each[1])))
#     print(each)
#     # print(bacnet.readMultiple("192.168.15.202 {} {} presentValue units".format(each[0], each[1])))
# or
#  print(bacnet.readMultiple("2:5 {} {} presentValue units.format(each[0],each[1]))
# bacnet.disconnect()
