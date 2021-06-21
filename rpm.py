from typing import NamedTuple

import BAC0
from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.interfaces.object_property import ObjProperty
from BAC0.core.io.IOExceptions import (ReadPropertyException,
                                       NoResponseFromController,
                                       UnknownObjectError,
                                       UnknownPropertyError,
                                       ReadPropertyMultipleException)

from src.bacnet_master.utils.functions import serialize_priority_array

bacnet = BAC0.lite()


class BACnetObject:
    type: ObjType
    id: int
    name: str


def read_property_multiple(network, address, obj: BACnetObject,
                           properties: [ObjProperty]) -> dict:
    try:
        request = ' '.join([
            address,
            obj.type.name,
            str(obj.id),
            *[prop.name for prop in properties]
        ])
        response = network.readMultiple(request)
        # check values for None and empty strings
        values = 22
        # for i, value in enumerate(response):
        #     print(i, value)
            # print(i)
        # values = {properties[i]: value for i, value in response
        #
        #           }
        #
        # # if value is not None and str(value).strip()}

    except Exception as e:
        print((f'RPM Error: {e}'))
        raise ReadPropertyMultipleException(e)
    else:
        if values is not None:
            return values
        else:
            raise ReadPropertyMultipleException('Response is None')


def read_property(network, address, obj: BACnetObject, prop: ObjProperty):
    try:
        request = ' '.join([
            address,
            obj.type.name,
            str(obj.id),
            prop.name
        ])
        response = network.read(request)
    except Exception as e:
        print(e)
        raise e
        # return self.__get_fault_obj_properties(reliability='rp-error')
    else:
        if response is not None:
            if isinstance(response, str) and not response.strip():
                raise ReadPropertyException('Response is empty')
            return response
        raise ReadPropertyException('Response is None')


a = BACnetObject
a.name = "aa"
a.type = ObjType.device
a.id = 123
prop = ObjProperty.objectName
prop2 = ObjProperty.objectName
prop3 = ObjProperty.protocolServicesSupported
# aa = read_property(bacnet, "192.168.15.10", a, prop)
aaa = read_property_multiple(bacnet, "192.168.15.11", a, [prop, prop2, prop3])
print(aaa)
# print(aaa.get(('analogOutput', 1)))
a = [[('device', 123)], (10, 14, 58, 27), (121, 6, 10, 4), [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], 'operationalReadOnly', 'Nube iO Operations Pty Ltd', 1173, 'rubix-bac-stack-RC4', '3.9.5 (default, May 12 2021, 16:25:25) \n[GCC 8.3.0]', '20.11.21', 1, 0, [('device', 123)], 1024, 'segmentedBoth', 5000, 3000, 3, [], 16, ('device', 123), 'Nube-IO', 'http://christiantremblay.github.io/BAC0/', 'device', [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]]
