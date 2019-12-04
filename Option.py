from Exceptions import DependencyInputError
import re


class Option:

    def __new__(cls, *args, **kwargs):
        if cls is Option:
            raise TypeError("Base Option class may not be instantiated.")
        return object.__new__(cls)


    @staticmethod
    def construct_option_instance(option, condition):
        option_class = Option.__validate_option(option, condition)
        if option_class:
            return option_class(condition)

    @staticmethod
    def __validate_option(option_name, condition):
        valid_gen = (option_class for option_class in Option.__subclasses__() if option_name is
                     option_class.__name__)
        try:
            return next(valid_gen)
        except StopIteration:
            raise DependencyInputError('Invalid option name.')

    @classmethod
    def __validate_and_standardize_condition(cls, input_condition):
        if not hasattr(cls, 'allowed_conditions'):
            raise NotImplementedError('allowed_conditions for selected option are not specified')

        matches = [re.search(input_condition, allowed_condition, re.IGNORECASE) for
                   allowed_condition in cls.allowed_conditions]
        match_indices = [match[0] for match in enumerate(matches) if match is not None]
        if not len(match_indices) == 1:
            if not match_indices:
                raise DependencyInputError('Invalid condition.')
            if len(match_indices) > 1:
                raise DependencyInputError('Ambiguous condition.')

        return cls.allowed_conditions[match_indices[0]]

    def validate_input(self, independent_input_property, dependent_input_property):
        pass


class CompareSize(Option):
    allowed_conditions = ['>', '<', '=', 'Equal', 'Greater', 'Smaller']

    def __init__(self, condition):
        self.standardized_condition = CompareSize.__validate_and_standardize_condition(condition)

    def __validate_and_standardize_condition(self, input_condition):
        pass


    def validate_input(self, independent_input_property, dependent_input_property):
        pass



