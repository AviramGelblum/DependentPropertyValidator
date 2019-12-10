from Exceptions import ValidationError
from itertools import chain


class InputProperty:
    """
    Class for input arguments. Examines the input's multi-level structure: its depth and the type of each level.
    """
    def __init__(self, input_property):
        self.input = input_property
        self.type = [type(input_property)]
        self.__get_deep_types(input_property, 0)  # find multi-level object types
        self.depth = len(self.type)

    def __get_deep_types(self, separated, level: int):
        """
        Recursive private method for the extraction of the types of multi-level input.
        :param separated: input to be examined
        :param level: current data depth to be examined
        """
        if isinstance(separated, (list, tuple)):
            # check that all items are of the same type
            if not InputProperty.check_same_type_list(separated):
                raise ValidationError("Elements of {0} property provided are not all of the same type.".format(self.type[
                    level].__name__))
            self.type.append(type(separated[0]))  # add the type of the next level to the type list of the input.
            merged = InputProperty.merge_elements(separated, separated[0])  # Merge the next level to verify that all
            # items are of the same types in all levels.
            self.__get_deep_types(merged, level + 1)  # recur until current level type is not tuple/list/dict
        elif isinstance(separated, dict):
            # check that all items (keys and values) are of the same type
            if not InputProperty.check_same_type_dict(separated):
                raise ValidationError("Elements of {0} property provided are not all of the same type.".format(self.type[
                    level].__name__))

            first_key = next(iter(separated))
            self.type.append(type(separated[first_key]))  # add the type of the next level to the type list of the input.
            merged = InputProperty.merge_elements(separated.values(), separated[first_key])  # Merge the next level to
            # verify that all items are of the same types in all levels.
            self.__get_deep_types(merged, level + 1)  # recur until current level type is not tuple/list/dict

        # If the current level of data is not list/tuple/dict, then it is assumed to be the last level, and thus no
        # further actions are needed.


    # region Static helper methods

    @staticmethod
    def check_same_type_list(lst: list) -> bool:
        """
        Check that all items of a list share the same top-level type.
        :param lst: Input list to be checked
        """
        return all(isinstance(x, type(lst[0])) for x in lst)

    @staticmethod
    def check_same_type_dict(dct: dict) -> bool:
        """
        Check that all keys and values of a dictionary share the same top-level type (separately).
        :param dct: Input dictionary to be checked
        """
        first_key = next(iter(dct))
        return all(isinstance(x[0], type(first_key)) and isinstance(x[1], type(dct[first_key])) for
                   x in dct.items())

    @staticmethod
    def merge_dicts(dict1: dict, dict2: dict) -> dict:
        """
        Merge two dictionaries into a single dictionary. In case of duplicate keys, default to the value given in
        dict2.
        """
        return {**dict1, **dict2}

    @staticmethod
    def merge_elements(input_var, element):
        """
        Merge the input's elements into a single element, if they are of type list/tuple/dict.
        This allows verification of same-level type-sharing across the entirety of an argument.
        :param input_var: The input variable to be processed.
        :param element: A single element of the input variable.
        :return: A single merged-elements variable.
        """

        if isinstance(element, (list, tuple)):
            merged = list(chain.from_iterable(input_var))
        elif isinstance(element, dict):
            merged = dict()
            for dict_in_lst in input_var:
                merged = InputProperty.merge_dicts(merged, dict_in_lst)
        else:  # if not mergeable, simply take the element. This signifies the last recurrence of __get_deep_types.
            merged = element
        return merged

    # endregion


