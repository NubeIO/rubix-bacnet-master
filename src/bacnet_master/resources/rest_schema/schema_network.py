from flask_restful import fields

from src.bacnet_master.resources.rest_schema.schema_device import device_all_fields
from src.bacnet_master.resources.utils import map_rest_schema

network_all_attributes = {
    'network_name': {
        'type': str,
        'required': False,
        'help': 'network_name must be a string'
    },
    'network_enable': {
        'type': bool,
        'required': False,
        'help': 'enable/disable operation'
    },
    'network_ip': {
        'type': str,
        'required': True,
        'help': 'network_ip must be a string'
    },
    'network_mask': {
        'type': int,
        'required': True,
        'help': 'network_mask must be an int length 2'
    },
    'network_port': {
        'type': int,
        'required': True,
        'help': 'network_port must must be an int length 4'
    },
    'network_device_object_id': {
        'type': int,
        'required': True,
        'help': 'network device object id is needed'
    },
    'network_device_name': {
        'type': str,
        'required': True,
        'help': 'network_device_name is needed'
    }
}

network_extra_attributes = {
    'network_uuid': {
        'type': str,
        'required': False,
        'help': 'network_uuid must be a string'
    },
}

network_all_fields = {}
map_rest_schema(network_extra_attributes, network_all_fields)
map_rest_schema(network_all_attributes, network_all_fields)
network_all_fields['devices'] = fields.List(fields.Nested(device_all_fields))
