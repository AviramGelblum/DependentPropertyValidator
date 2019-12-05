from Exceptions import ValidationError
from helpers import unpack_types

class InputProperty:
    def __init__(self, input_property):
        self.input = input_property
        self.type = [type(input_property)]
        self.__get_deep_types(input_property, 0)
        self.depth = len(self.type)

    def __get_deep_types(self, property_segment, level):
        # todo: add support for custom iterables? probably not needed, right?

        if isinstance(property_segment, (list, tuple)):
            # check that all items are of the same type
            if not InputProperty.check_same_type_list(property_segment):
                raise ValidationError("Elements of {0} property provided are not all of the same type.".format(self.type[
                    level].__name__))
            self.type.append(type(property_segment[0]))
            unpacked = unpack_types(property_segment, property_segment[0])
            self.__get_deep_types(unpacked, level + 1)
        elif isinstance(property_segment, dict):
            if not InputProperty.check_same_type_dict(property_segment):
                raise ValidationError("Elements of {0} property provided are not all of the same type.".format(self.type[
                    level].__name__))

            first_key = next(iter(property_segment))
            self.type.append(type(property_segment[first_key]))
            unpacked = unpack_types(property_segment.values(), property_segment[first_key])
            self.__get_deep_types(property_segment[first_key], level + 1)


    # region Static Methods

    @staticmethod
    def check_same_type_list(lst):
        return all(isinstance(x, type(lst[0])) for x in lst)

    @staticmethod
    def check_same_type_dict(dct):
        first_key = next(iter(dct))
        return all(isinstance(x[0], type(first_key)) and isinstance(x[1], type(dct[first_key])) for
                   x in dct.items())

    # endregion


