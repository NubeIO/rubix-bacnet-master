import BAC0

bacnet = BAC0.lite('10.17.71.15/22:47808')
print(bacnet.read('2314:1762314 device 1762314 objectList'))

_rpm = {'address': '2314:0x0000001ae40a',
        'objects': {
            'analogValue:11': ['objectName', 'presentValue', 'statusFlags', 'units','description'],
            'analogValue:13': ['objectName', 'presentValue', 'statusFlags', 'units', 'description']
            }
        }

a = bacnet.readMultiple('2314:0x0000001ae40a', request_dict=_rpm)
print(a)
