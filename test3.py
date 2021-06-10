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

_rpm = {'address': '192.168.15.11',
        'objects': {
            'analogOutput:1': ['objectName', 'presentValue', 'statusFlags', 'units', 'description'],
            'analogOutput:2': ['objectName', 'presentValue', 'statusFlags', 'units', 'description'],
        }
        }

a = bacnet.readMultiple('192.168.15.10', _rpm)


print(a.get(('analogOutput', 1)))
