from itertools import chain


def merge_dicts(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def unpack_types(input_var, first_element):
    if isinstance(first_element, (list, tuple)):
        unpacked = list(chain.from_iterable(input_var))
    elif isinstance(first_element, dict):
        unpacked = dict()
        for dict_in_lst in input_var:
            unpacked = merge_dicts(unpacked, dict_in_lst)
    else:
        unpacked = first_element
    return unpacked
