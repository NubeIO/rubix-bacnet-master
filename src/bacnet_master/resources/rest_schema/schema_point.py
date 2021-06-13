from src.bacnet_master.resources.utils import map_rest_schema

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
    'point_value': {
        'type': int,
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
