import BAC0

bacnet = BAC0.lite('10.17.71.15/22:47808')

print(bacnet.read('2304:0x0000001ae400 analogValue 1012 presentValue'))

print(bacnet.read('2304:1762304 analogValue 1012 presentValue'))

print(bacnet.whois('2304:*'))

print(bacnet.read('2304:0x0000001ae400 device 1762304 objectList'))
print(22)
print(bacnet.read('2304:1762304 device 1762304 objectList'))
print(22)

_rpm = {'address': '2304:0x0000001ae400',
        'objects': {
            'analogValue:11': ['objectName', 'presentValue', 'statusFlags', 'units', 'description'],
            'analogValue:13': ['objectName', 'presentValue', 'statusFlags', 'units', 'description']
        }
        }

a = bacnet.readMultiple('2304:0x0000001ae400', request_dict=_rpm)
print(a)
