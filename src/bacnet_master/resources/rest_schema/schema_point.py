from flask_restful import fields
from collections import OrderedDict
from src.bacnet_master.resources.utils import map_rest_schema
priority_array_write_fields = OrderedDict({
    '_1': fields.Float,
    '_2': fields.Float,
    '_3': fields.Float,
    '_4': fields.Float,
    '_5': fields.Float,
    '_6': fields.Float,
    '_7': fields.Float,
    '_8': fields.Float,
    '_9': fields.Float,
    '_10': fields.Float,
    '_11': fields.Float,
    '_12': fields.Float,
    '_13': fields.Float,
    '_14': fields.Float,
    '_15': fields.Float,
    '_16': fields.Float,
})
point_all_attributes = {
    'point_name': {
        'type': str,
        'required': False,
        'help': 'point_name must be a string'
    },
    'point_enable': {
        'type': bool,
        'required': False,
        'help': 'enable/disable operation'
    },
    'point_object_id': {
        'type': int,
        'required': False,
        'help': 'point_object_id must be a int'
    },
    'point_object_type': {
        'type': str,
        'required': False,
        'nested': True,
        'dict': 'point_object_type.name',
        'help': 'point_object_type must be a string'
    },
    'device_uuid': {
        'type': str,
        'required': False,
        'help': 'point_name must be a string'
    },
    'get_priority': {
        'type': bool,
        'required': False,
        'help': 'point_name must be a string'
    },
    'timeout': {
        'type': int,
        'required': False,
        'help': 'point_name must be a string'
    },
    'feedback': {
        'type': bool,
        'required': False,
        'help': 'point_name must be a string'
    },
    'priority': {
        'type': int,
        'required': False,
        'help': 'point_name must be a string'
    },
    'point_value': {
        'type': float,
        'required': False,
        'help': 'point_name must be a string'
    },
    'priority_array': {
        'type':  fields.Nested(priority_array_write_fields),
        'required': False,
        'help': 'point_name must be a string'
    },
    'point_write_value': {
        'type': float,
        'required': False,
        'help': 'point_name must be a string'
    }
}

point_extra_attributes = {
    'point_uuid': {
        'type': str,
        'required': False,
        'help': 'point_uuid must be a string'
    },
}

point_all_fields = {}
map_rest_schema(point_extra_attributes, point_all_fields)
map_rest_schema(point_all_attributes, point_all_fields)
