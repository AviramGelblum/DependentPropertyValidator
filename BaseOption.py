from Exceptions import DependencyInputError, ValidationError
import re


class BaseOption:

    def __new__(cls, *args, **kwargs):
        if cls is BaseOption:
            raise TypeError("BaseOption class may not be instantiated.")
        return object.__new__(cls)

    @staticmethod
    def construct(option, condition):
        option_class = BaseOption.__validate_option(option)
        if option_class:
            return option_class(condition)

    @staticmethod
    def __validate_option(option_name):
        return BaseOption.find_single_case_insensitive_submatch_in_list(
                          option_name, BaseOption.__subclasses__(), 'option name')

    @classmethod
    def validate_condition(cls, input_condition):
        if not hasattr(cls, 'allowed_conditions'):
            raise NotImplementedError('allowed_conditions for selected option are not specified')
        return BaseOption.find_single_case_insensitive_submatch_in_list(
                          input_condition, cls.allowed_conditions, 'condition')

    @staticmethod
    def find_single_case_insensitive_submatch_in_list(pattern, lst, error_string):
        if isinstance(lst[0], type):
            matches = [subclass for subclass in lst if re.search(pattern, subclass.__name__, re.IGNORECASE)]
        else:
            matches = [string for string in lst if re.search(pattern, string, re.IGNORECASE)]

        if not matches:
            raise DependencyInputError('Invalid {0}.'.format(error_string))
        if len(matches) > 1:
            raise DependencyInputError('Ambiguous {0}.'.format(error_string))
        return matches[0]

    def validate_input(self, dependent_property):
        pass


class CompareSize(BaseOption):
    allowed_conditions = ['gt', 'lt', 'eq', 'ne', 'ge', 'le']

    def __init__(self, condition):
        self.standardized_condition = CompareSize.validate_condition(condition)

    def validate_input(self, dependent_property_validator):
        if not callable(getattr(dependent_property_validator.independent_input_property.input, '__len__', None)):
            raise ValidationError('Cannot compare input sizes. Independent input property has no __len__ '
                                  'method implementation.')
        if not callable(getattr(dependent_property_validator.dependent_input_property.input, '__len__', None)):
            raise ValidationError('Cannot compare input sizes. Dependent input property has no __len__ '
                                  'method implementation.')

        condition_switch = CompareSize.ConditionSwitch(dependent_property_validator)
        return condition_switch.switch(self.standardized_condition)

    class ConditionSwitch:
        def __init__(self, dependent_property):
            self.independent_input_property = dependent_property.independent_input_property.input
            self.dependent_input_property = dependent_property.dependent_input_property.input

        def switch(self, condition):
            return getattr(self, condition, lambda: False)()

        def gt(self): return len(self.independent_input_property) > len(self.dependent_input_property)
        def ge(self): return len(self.independent_input_property) >= len(self.dependent_input_property)
        def lt(self): return len(self.independent_input_property) < len(self.dependent_input_property)
        def le(self): return len(self.independent_input_property) <= len(self.dependent_input_property)
        def eq(self): return len(self.independent_input_property) == len(self.dependent_input_property)
        def ne(self): return len(self.independent_input_property) != len(self.dependent_input_property)


