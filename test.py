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


from multiprocessing import SimpleQueue

from multiprocessing import SimpleQueue
from pathlib import Path
from threading import Thread
from time import sleep, time

from BAC0.core.io.IOExceptions import (ReadPropertyException,
                                       NoResponseFromController,
                                       UnknownObjectError,
                                       UnknownPropertyError,
                                       ReadPropertyMultipleException)


# from gateway.connectors import get_fault_obj_properties
# from gateway.connectors.bacnet import ObjProperty, ObjType, BACnetObject
# from gateway.logs import get_file_logger


class BACnetDevice(Thread):
    __slots__ = ('id', 'update_period', '__logger', '__connector', '__verifier_queue',
                 'address', 'network', 'support_rpm', 'not_support_rpm',
                 '__active', '__polling'
                 )

    def __init__(self,
                 verifier_queue: SimpleQueue,
                 connector,
                 address: str,
                 device_id: int,
                 network,
                 objects: BACnetObject,
                 update_period: int = 10):
        super().__init__()

        self.id = device_id
        self.update_period = update_period

        base_path = Path(__file__).resolve().parent.parent.parent
        # log_file_path = base_path / f'logs/{self.id}.log'
        #
        # self.__logger = get_file_logger(logger_name=f'{self}',
        #                                 size_bytes=50_000_000,
        #                                 file_path=log_file_path)

        self.setName(name=f'{self}-Thread')
        self.setDaemon(True)

        self.__connector = connector
        self.__verifier_queue = verifier_queue

        self.address = address
        self.network = network

        self.support_rpm: BACnetObject = objects
        self.not_support_rpm: BACnetObject = set()

        # self.__objects_per_rpm = 25
        # todo: Should we use one RPM for several objects?

        self.__active = True
        self.__polling = True

        self.__logger.info(f'{self} starting ...')
        self.start()

    def __repr__(self):
        return f'BACnetDevice [{self.id}]'

    def __len__(self):
        """ :return: the quantity of objects in the device received from the server
        """
        return len(self.support_rpm) + len(self.not_support_rpm)

    def run(self):
        while self.__polling:
            self.__logger.debug('Polling started')
            if self.__active:
                self.__logger.debug(f'{self} is active')
                try:
                    t0 = time()
                    self.poll()  # poll all objects
                    t1 = time()
                    time_delta = t1 - t0

                    self.__logger.info(
                        '\n==================================================\n'
                        f'{self} ip:{self.address} polled for: '
                        f'{round(time_delta, ndigits=2)} sec.\n'
                        f'Update period: {self.update_period} sec.\n'
                        f'Objects: {len(self)}\n'
                        f'Support RPM: {len(self.support_rpm)}\n'
                        f'Not support RPM: {len(self.not_support_rpm)}\n'
                        '==================================================')

                    self.__logger.info(
                        f'Timedelta = {time_delta}, upd_period = {self.update_period}')
                    if time_delta < self.update_period:
                        waiting_time = (self.update_period - time_delta) * 0.8
                        self.__logger.info(
                            f'{self} Sleeping {round(waiting_time, ndigits=2)} sec ...')
                        sleep(waiting_time)

                except Exception as e:
                    self.__logger.error(f'Polling error: {e}', exc_info=True)
            else:  # if device inactive
                self.__logger.debug(f'{self} is inactive')
                try:
                    device_obj = BACnetObject(type=ObjType.DEVICE,
                                              id=self.id,
                                              name='None')
                    device_id = self.read_property(obj=device_obj,
                                                   prop=ObjProperty.objectIdentifier)

                    self.__logger.info(f'PING: device_id: {device_id} <{type(device_id)}>')

                    if device_id:
                        self.__logger.debug(f'{self} setting to active ...')
                        self.__active = True
                        continue
                except Exception as e:
                    self.__logger.error(f"'Ping checking' error: {e}")
                    pass
                # delay
                # todo: move delay in config

                # todo: close Thread and push to bacnet-connector
                self.__logger.debug('Sleeping 60 sec ...')
                sleep(60)
        else:
            self.__logger.info(f'{self} stopped.')

    def start_polling(self) -> None:
        self.__polling = True
        self.__logger.info('Starting polling ...')
        self.start()

    def stop_polling(self) -> None:
        self.__polling = False
        # self.network.disconnect()
        self.__logger.info('Stopping polling ...')

    def set_inactive(self) -> None:
        self.__active = False
        self.__logger.warning(f'{self} switched to inactive.')

        # TODO put to bacnet connector for ping checking

    def poll(self) -> None:
        """ Poll all object from device.
            Send each object into verifier after answer.
            When all objects polled, send device_id into verifier as finish signal
        """
        for obj in self.support_rpm:
            assert isinstance(obj, BACnetObject)

            self.__logger.debug(f'Polling supporting PRM {obj} ...')
            try:
                values = self.rpm(obj=obj)
                self.__logger.debug(f'{obj} values: {values}')
            except ReadPropertyMultipleException as e:
                self.__logger.warning(f'{obj} rpm error: {e}\n'
                                      f'{obj} Marking as not supporting RPM ...')
                self.not_support_rpm.add(obj)
                # self.support_rpm.discard(obj)

            except Exception as e:
                self.__logger.error(f'{obj} polling error: {e}', exc_info=True)
            else:
                self.__logger.debug(f'From {obj} read: {values}. Sending to verifier ...')
                self.__put_data_into_verifier(properties=values)

        self.support_rpm.difference_update(self.not_support_rpm)

        for obj in self.not_support_rpm:
            assert isinstance(obj, BACnetObject)

            self.__logger.debug(f'Polling not supporting PRM {obj} ...')
            try:
                values = self.simulate_rpm(obj=obj)
            except UnknownObjectError as e:
                self.__logger.error(f'{obj} is unknown: {e}')
            except Exception as e:
                self.__logger.error(f'{obj} polling error: {e}', exc_info=True)
            else:
                self.__logger.debug(f'From {obj} read: {values}. Sending to verifier ...')
                self.__put_data_into_verifier(properties=values)

        # notify verifier, that device polled and should send collected objects via HTTP
        self.__logger.debug('All objects were polled. Send device_id to verifier')
        self.__put_device_end_to_verifier()

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
            self.__logger.error(f'RP Error: {e}')
            raise e
            # return self.__get_fault_obj_properties(reliability='rp-error')
        else:
            if response is not None:
                if isinstance(response, str) and not response.strip():
                    raise ReadPropertyException('Response is empty')
                return response
            raise ReadPropertyException('Response is None')

    def read_property_multiple(self, obj: BACnetObject,
                               properties: [ObjProperty]) -> dict:
        try:
            request = ' '.join([
                self.address,
                obj.type.name,
                str(obj.id),
                *[prop.name for prop in properties]
            ])
            response = self.network.readMultiple(request)

            # check values for None and empty strings
            values = {properties[i]: value for i, value in enumerate(response)
                      if value is not None and str(value).strip()}

        except Exception as e:
            self.__logger.warning(f'RPM Error: {e}')
            raise ReadPropertyMultipleException(e)
        else:
            if values is not None:
                return values
            else:
                raise ReadPropertyMultipleException('Response is None')

    def __simulate_rpm(self, obj: BACnetObject, properties: [ObjProperty]) -> dict:
        values = {}
        for prop in properties:
            try:
                response = self.read_property(obj=obj, prop=prop)

            except (UnknownObjectError, NoResponseFromController) as e:
                self.__logger.warning(f'sRPM Error: {e}')
                raise e

            except (UnknownPropertyError, ReadPropertyException) as e:
                if prop is ObjProperty.priorityArray:
                    continue
                self.__logger.warning(f'sRPM Error: {e}')
                raise e
            except TypeError as e:
                self.__logger.error(f'Type error: {e}')
                raise e
            except Exception as e:
                self.__logger.error(f'sRPM error: {e}', exc_info=True)

            else:
                values.update({prop: response})
                # self.not_support_rpm.update(obj)

        return values

    def rpm(self, obj: BACnetObject) -> dict:
        properties = {
            ObjProperty.deviceId: self.id,
            ObjProperty.objectName: obj.name,
            ObjProperty.objectType: obj.type,
            ObjProperty.objectIdentifier: obj.id,
        }
        try:
            values = self.read_property_multiple(obj=obj,
                                                 properties=obj.type.properties
                                                 )

        except ReadPropertyMultipleException as e:
            self.__logger.error(f'Read Error: {e}')
            raise e
        else:
            properties.update(values)
            return properties

    def simulate_rpm(self, obj: BACnetObject) -> dict:
        properties = {
            ObjProperty.deviceId: self.id,
            ObjProperty.objectName: obj.name,
            ObjProperty.objectType: obj.type,
            ObjProperty.objectIdentifier: obj.id,
        }

        try:
            values = self.__simulate_rpm(obj=obj,
                                         properties=obj.type.properties
                                         )

        except NoResponseFromController as e:
            self.__logger.error(f'No response error: {e}')
            values = get_fault_obj_properties(reliability='no-response')
        except UnknownPropertyError as e:
            self.__logger.error(f'Unknown property error: {e}')
            values = get_fault_obj_properties(reliability='unknown-property')
        except UnknownObjectError as e:
            self.__logger.error(f'Unknown object error: {e}')
            values = get_fault_obj_properties(reliability='unknown-object')
        except (ReadPropertyException, TypeError) as e:
            self.__logger.error(f'RP error: {e}')
            values = get_fault_obj_properties(reliability='rp-error')
        except Exception as e:
            self.__logger.error(f'Read Error: {e}', exc_info=True)
            values = get_fault_obj_properties(reliability='error')
        finally:
            properties.update(values)
            return properties

    def __put_device_end_to_verifier(self) -> None:
        """ device_id in queue means that device polled.
            Should send collected objects to HTTP
        """
        self.__verifier_queue.put(self.id)

    def __put_data_into_verifier(self, properties: dict) -> None:
        """ Send collected data about obj into BACnetVerifier
        """
        self.__verifier_queue.put(properties)


def __start_device(self, device_id: int, objects: BACnetObject,
                   update_interval: int) -> None:
    """ Start BACnet device thread """

    # _log.debug(f'Starting Device [{device_id}] ...')
    try:
        self.__polling_devices[device_id] = BACnetDevice(
            verifier_queue=self.__verifier_queue,
            connector=self,
            address=self.address_cache[device_id],
            device_id=device_id,
            network=self.__network,
            objects=objects,
            update_period=update_interval
        )

    except Exception as e:
        print(22)
        # _log.error(f'Device [{device_id}] '
        #            f'starting error: {e}', exc_info=True)
    else:
        print(22)
        # _log.info(f'Device [{device_id}] started')
