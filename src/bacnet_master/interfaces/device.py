from enum import Enum


class ObjType(Enum):
    analogInput = "analog_input", 0, 'analogInput'
    analogOutput = "analog_output", 1, 'analogOutput'
    analogValue = "analog_value", 2, 'analogValue'
    binaryInput = "binary_input", 3, 'binaryInput'
    binaryOutput = "binary_output", 4, 'binaryOutput'
    binaryValue = "binary_value", 5, 'binaryValue'
    calendar = "calendar", 6, 'calendar'
    command = "command", 7, 'command'
    device = "device", 8, 'device'
    eventEnrollment = "event_enrollment", 9, 'eventEnrollment'
    file = "file", 10, 'file'
    group = "group", 11, 'group'
    loop = "loop", 12, 'loop'
    multiStateInput = "multi_state_input", 13, 'multiStateInput'
    multiStateOutput = "multi_state_output", 14, 'multiStateOutput'
    notificationClass = "notification_class", 15, 'notificationClass'
    program = "program", 16, 'program'
    schedule = "schedule", 17, 'schedule'
    averaging = "averaging", 18, 'averaging'
    multiStateValue = "multi_state_value", 19, 'multiStateValue'
    trendLog = "trend_log", 20, 'trendLog'
    lifeSafetyPoint = "life_safety_point", 21, 'lifeSafetyPoint'
    lifeSafetyZone = "life_safety_zone", 22, 'lifeSafetyZone'
    accumulator = "accumulator", 23, 'accumulator'
    pulseConverter = "pulse_converter", 24, 'pulseConverter'
    accessPoint = "access_point", 33, 'accessPoint'

    @classmethod
    def has_value(cls, value):
        print(cls.__members__)
        if value in cls.__members__:
            return value

    @classmethod
    def has_value_by_name(cls, val):
        for i in ObjType:
            name_underscore = i.value[0]
            if name_underscore in val:
                return i

    @classmethod
    def has_value_from_string(cls, value) -> dict:
        if value in cls.__members__:
            return {
                "value": ObjType[value],
                "name": ObjType[value].get_name,
                "id": ObjType[value].id
            }

    @property
    def id(self) -> int:
        return self.value[1]

    @property
    def get_name(self) -> str:
        return self.value[2]

    @property
    def name_underscore(self) -> str:
        return self.value[0]

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def all_obj(cls) -> dict:
        d = {}
        for i in ObjType:
            d[i.value[2]] = i.value[0]
        return d

    @classmethod
    def obj_as_false(cls) -> dict:
        d = {}
        for i in ObjType:
            d[i.value[2]] = False
        return d

    @classmethod
    def from_underscore(cls, lookup: str) -> str:
        """
        :param lookup:  binary_input
        :return: binaryInput
        """
        for key, value in cls.all_obj().items():
            for v in value:
                if lookup in value:
                    return key



