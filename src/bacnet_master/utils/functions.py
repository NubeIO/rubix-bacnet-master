def to_bool(value):
    if value == True:
        return True
    elif not value:
        return False
    else:
        return {"True": True, "true": True}.get(value, False)


def serialize_priority_array(priority_array):
    priority_array_dict = {}
    for i in range(16):
        priority_array_dict[f'_{i + 1}'] = None if list(priority_array[i].keys())[0] == 'null' else \
            list(priority_array[i].values())[0]
    return priority_array_dict
