from flask_restful import fields

from src.bacnet_master.resources.rest_schema.schema_point import point_all_fields
from src.bacnet_master.resources.utils import map_rest_schema

device_all_attributes = {
    'device_name': {
        'type': str,
        'required': False,
        'help': 'device_name must be a string'
    },
    'device_enable': {
        'type': bool,
        'required': False,
        'help': 'enable/disable operation'
    },
    'device_mac': {
        'type': int,
        'required': False,
        'help': 'BACnet mstp device device_mac address'
    },
    'device_id': {
        'type': int,
        'required': True,
        'help': 'Every device needs a bacnet device_id'
    },
    'device_ip': {
        'type': str,
        'required': False,
        'help': 'Every device needs a network device_ip'
    },
    'device_mask': {
        'type': int,
        'required': False,
        'help': 'Every device needs a network device_mask'
    },
    'device_port': {
        'type': int,
        'required': False,
        'help': 'Every device needs a network device_port'
    },
    'network_uuid': {
        'type': str,
        'required': True,
        'help': 'Every device needs a network_uuid'
    },
    'type_mstp': {
        'type': bool,
        'required': False,
        'help': 'True if device is type MSTP'
    },
    'supports_rpm': {
        'type': bool,
        'required': False,
        'help': 'True if device support read property multiple'
    },
    'supports_wpm': {
        'type': bool,
        'required': False,
        'help': 'True if device support write property multiple'
    },
    'network_number': {
        'type': int,
        'required': False,
        'help': 'Used for discovering networking (set to 0 to disable)'
    }
}
device_extra_attributes = {
    'device_uuid': {
        'type': str,
        'required': True,
        'help': 'device_uuid must be a string'
    },
}

device_all_fields = {}
map_rest_schema(device_extra_attributes, device_all_fields)
map_rest_schema(device_all_attributes, device_all_fields)
device_all_fields['points'] = fields.List(fields.Nested(point_all_fields))