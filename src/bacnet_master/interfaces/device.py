from enum import Enum


class ObjType(Enum):
    ANALOG_INPUT = "analog_input", 0, 'analogInput'
    ANALOG_OUTPUT = "analog_output", 1, 'analogOutput'
    ANALOG_VALUE = "analog_value", 2, 'analogValue'
    BINARY_INPUT = "binary_input", 3, 'binaryInput'
    BINARY_OUTPUT = "binary_output", 4, 'binaryOutput'
    BINARY_VALUE = "binary_value", 5, 'binaryValue'
    CALENDAR = "calendar", 6, 'calendar'
    COMMAND = "command", 7, 'command'
    DEVICE = "device", 8, 'device'
    EVENT_ENROLLMENT = "event_enrollment", 9, 'eventEnrollment'
    FILE = "file", 10, 'file'
    GROUP = "group", 11, 'group'
    LOOP = "loop", 12, 'loop'
    MULTI_STATE_INPUT = "multi_state_input", 13, 'multiStateInput'
    MULTI_STATE_OUTPUT = "multi_state_output", 14, 'multiStateOutput'
    NOTIFICATION_CLASS = "notification_class", 15, 'notificationClass'
    PROGRAM = "program", 16, 'program'
    SCHEDULE = "schedule", 17, 'schedule'
    AVERAGING = "averaging", 18, 'averaging'
    MULTI_STATE_VALUE = "multi_state_value", 19, 'multiStateValue'
    TREND_LOG = "trend_log", 20, 'trendLog'
    LIFE_SAFETY_POINT = "life_safety_point", 21, 'lifeSafetyPoint'
    LIFE_SAFETY_ZONE = "life_safety_zone", 22, 'lifeSafetyZone'
    ACCUMULATOR = "accumulator", 23, 'accumulator'
    PULSE_CONVERTER = "pulse_converter", 24, 'pulseConverter'
    ACCESS_POINT = "access_point", 33, 'accessPoint'

    @classmethod
    def has_value(cls, value):
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
                "name": ObjType[value]._name,
                "id": ObjType[value].id
            }

    @property
    def id(self) -> int:
        return self.value[1]

    @property
    def _name(self) -> str:
        return self.value[2]

    @property
    def _name_underscore(self) -> str:
        return self.value[0]

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def all_obj(cls) -> dict:
        d = {}
        for i in ObjType:
            d[i.value[2]] = i.value[1]
        return d

    @classmethod
    def obj_as_false(cls) -> dict:
        d = {}
        for i in ObjType:
            d[i.value[2]] = False
        return d

print(ObjType.has_value_from_string("ANALOG_OUTPUT").get("name"))