from src.bacnet_master.resources.utils import map_rest_schema

network_whois_all_attributes = {
    'network_number': {
        'type': int,
        'required': False,
        'help': 'network number'
    },
    'whois': {
        'type': bool,
        'required': False,
        'help': 'f true do a whois, if false do a network discover'
    },
    'global_broadcast': {
        'type': bool,
        'required': False,
        'help': 'global broadcast'
    },
    'full_range': {
        'type': bool,
        'required': False,
        'help': 'WhoIs full range'
    },
    'range_start': {
        'type': int,
        'required': False,
        'help': 'WhoIs looking for devices in the ID range EXAMPLE: START 10 (10 - 1000)'
    },
    'range_end': {
        'type': int,
        'required': False,
        'help': 'WhoIs looking for devices in the ID range (10 - 1000) EXAMPLE: END 1000'
    },
    'add_devices': {
        'type': bool,
        'required': False,
        'help': 'Set to true if you wanna add all discovered devices'
    },
    'is_mstp': {
        'type': bool,
        'required': False,
        'help': 'Set the network type is mstp'
    },
    'show_supported_services': {
        'type': bool,
        'required': False,
        'help': 'Set the network type is mstp'
    },
    'add_points': {
        'type': bool,
        'required': False,
        'help': 'Set the network type is mstp'
    },
    'fast_poll': {
        'type': bool,
        'required': False,
        'help': 'Set the network type is mstp'
    },
    'timeout': {
        'type': int,
        'required': False,
        'help': 'Set the network type is mstp'
    }
}

network_unknown_device_objects_attributes = {
    'device_name': {
        'type': str,
        'required': False,
        'help': 'BACnet mstp device device_mac address'
    }, 'device_mac': {
        'type': int,
        'required': False,
        'help': 'BACnet mstp device device_mac address'
    }, 'device_object_id': {
        'type': int,
        'required': True,
        'help': 'Every device needs a bacnet device id'
    }, 'device_ip': {
        'type': str,
        'required': False,
        'help': 'Every device needs a network device_ip.'
    }, 'device_mask': {
        'type': int,
        'required': False,
        'help': 'Every device needs a network device_mask'
    }, 'device_port': {
        'type': int,
        'required': False,
        'help': 'Every device needs a network device_port'
    }, 'type_mstp': {
        'type': bool,
        'required': False,
        'help': 'True if device is type MSTP'
    }, 'network_number': {
        'type': int,
        'required': False,
        'help': 'Used for discovering networking (set to 0 to disable)'
    },
}

point_unknown_read_point_pv_attributes = {
    'device_name': {
        'type': str,
        'required': False,
        'help': 'BACnet mstp device device_mac address'
    },
    'device_mac': {
        'type': int,
        'required': False,
        'help': 'BACnet mstp device device_mac address'
    }, 'device_object_id': {
        'type': int,
        'required': True,
        'help': 'Every device needs a bacnet device id'
    }, 'device_ip': {
        'type': str,
        'required': False,
        'help': 'Every device needs a network device_ip.'
    }, 'device_mask': {
        'type': int,
        'required': False,
        'help': 'Every device needs a network device_mask'
    }, 'device_port': {
        'type': int,
        'required': False,
        'help': 'Every device needs a network device_port'
    }, 'type_mstp': {
        'type': bool,
        'required': False,
        'help': 'True if device is type MSTP'
    }, 'network_number': {
        'type': int,
        'required': False,
        'help': 'Used for discovering networking (set to 0 to disable)'
    }, 'point_object_id': {
        'type': int,
        'required': True,
        'help': 'Every device needs a network device_uuid'
    }, 'point_object_type': {
        'type': str,
        'required': False,
        'help': 'True if device is type MSTP'
    }
}
