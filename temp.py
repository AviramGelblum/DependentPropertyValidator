# from DependentPropertyValidator import DependentPropertyValidator
# DPV = DependentPropertyValidator()
# DPV.add_property_dependency([str, str])
# test = DPV.validate('ff', 'dfd')

# from Exceptions import DependencyInputError
# class A:
#
#     def __new__(cls, *args, **kwargs):
#         if cls is A:
#             raise TypeError("base class may not be instantiated")
#         return object.__new__(cls)
#
#
#     @staticmethod
#     def construct_option_instance(option, condition):
#         option_class = A.__validate_option(option, condition)
#         if option_class:
#             return option_class(condition)
#
#
#     @staticmethod
#     def __validate_option(option_name, condition):
#         valid_gen = (option_class for option_class in A.__subclasses__() if option_name is
#                       option_class.__name__)
#         try:
#             return next(valid_gen)
#         except StopIteration:
#             raise DependencyInputError
#
#
#
#     def validate_condition(self):
#         pass
#
#     def validate_input(self):
#         pass
#
#
# class CompareSize(A):
#
#     def __init__(self, condition):
#         print('well done')
#
# j = A.construct_option_instance('CompareSize',[])
# k = A()
# b = 1

from itertools import chain


def merge_dicts(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def check_same_type_list(lst):
    return all(isinstance(x, type(lst[0])) for x in lst)


def check_same_type_dict(dct):
    first_key = next(iter(dct))
    return all(isinstance(x[0], type(first_key)) and isinstance(x[1], type(dct[first_key])) for
               x in dct.items())


def get_deep_types(p, level, type_list=None):
    if type_list is None:
        type_list = []
    if isinstance(p, (list, tuple)):
        if not check_same_type_list(p):
            raise Exception("1")
        type_list.append(type(p[0]))
        unpacked = unpack(p, p[0])
        return get_deep_types(unpacked, level + 1, type_list)
    elif isinstance(p, dict):
        if not check_same_type_dict(p):
            raise Exception("2")
        first_key = next(iter(p))
        type_list.append(type(p[first_key]))
        unpacked = unpack(p.values(), p[first_key])
        return get_deep_types(unpacked, level + 1, type_list)
    else:
        return type_list





# a = [[1, 5], [2, 3]]
# b = [1, 2, 3]
# k = [{'h': 3}, {'b': 5}, {'c': 6, 'b': 7}]
# jj = [{'h': [3,4,5]}, {'b': [5,6,7]}, {'c': [6,6,8], 'b': [7]}]
jj2 = [{'h': {'b':[7],'f':[8,9,10]}}, {'b': {'m':['j'],'b':[5]}},
      {'c': {'nn':[30,6,4,5],'jj':[5]}, 'b':  {'n':[5],'jj':[7]}}]

# print(list(chain(a)))
# print(list(chain(b)))
#
# type_list = get_deep_types(a, 0)
# print('type_list a ={0}'.format(type_list))
#
# type_list = get_deep_types(b, 0)
# print('type_list b ={0}'.format(type_list))
#
# type_list = get_deep_types(k, 0)
# print('type_list k ={0}'.format(type_list))
#
# type_list = get_deep_types(jj, 0)
# print('type_list jj ={0}'.format(type_list))

type_list = get_deep_types(jj2, 0)
print('type_list jj2 ={0}'.format(type_list))