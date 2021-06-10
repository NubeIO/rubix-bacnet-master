from typing import NamedTuple

from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.interfaces.object_property import ObjProperty
from BAC0.core.io.IOExceptions import (ReadPropertyException,
                                       NoResponseFromController,
                                       UnknownObjectError,
                                       UnknownPropertyError,
                                       ReadPropertyMultipleException)


class BACnetObject(NamedTuple):
    type: ObjType
    id: int
    name: str


def get_fault_obj_properties(reliability: int or str,
                             pv='null',
                             sf: list = None) -> dict:
    """ Returns properties for unknown objects
    """
    if sf is None:
        sf = [0, 1, 0, 0]
    return {
        ObjProperty.presentValue: pv,
        ObjProperty.statusFlags: sf,
        ObjProperty.reliability: reliability
        #  todo: make reliability class as Enum
    }


def read_property(self, obj: BACnetObject, prop: ObjProperty):
    try:
        request = ' '.join([
            self.address,
            obj.type.name,
            str(obj.id),
            prop.name
        ])
        response = self.network.read(request)
    # except UnknownPropertyError:
    #     return self.__get_fault_obj_properties(reliability='unknown-property')
    # except UnknownObjectError:
    #     return self.__get_fault_obj_properties(reliability='unknown-object')
    # except NoResponseFromController:
    #     return self.__get_fault_obj_properties(reliability='no-response')
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


def __simulate_rpm(obj: BACnetObject, properties: [ObjProperty]) -> dict:
    values = {}
    for prop in properties:
        try:
            response = read_property(obj=obj, prop=prop)

        except (UnknownObjectError, NoResponseFromController) as e:

            raise e

        except (UnknownPropertyError, ReadPropertyException) as e:
            if prop is ObjProperty.priorityArray:
                continue

            raise e
        except TypeError as e:

            raise e
        except Exception as e:
            print(e)


        else:
            values.update({prop: response})
            # self.not_support_rpm.update(obj)

    return values


def simulate_rpm(obj: BACnetObject, deviceId) -> dict:
    properties = {
        ObjProperty.deviceId: deviceId,
        ObjProperty.objectName: obj.name,
        ObjProperty.objectType: obj.type,
        ObjProperty.objectIdentifier: obj.id,
    }

    try:
        values = __simulate_rpm(obj=obj,
                                properties=obj.type.properties
                                )

    except NoResponseFromController as e:
        print(e)

        values = get_fault_obj_properties(reliability='no-response')
    except UnknownPropertyError as e:
        print(e)
        values = get_fault_obj_properties(reliability='unknown-property')
    except UnknownObjectError as e:
        print(e)
        values = get_fault_obj_properties(reliability='unknown-object')
    except (ReadPropertyException, TypeError) as e:
        print(e)
        values = get_fault_obj_properties(reliability='rp-error')
    except Exception as e:
        print(e)
        values = get_fault_obj_properties(reliability='error')
    finally:
        properties.update(values)
        return properties




values = get_fault_obj_properties(reliability='unknown-property')
print(values)
