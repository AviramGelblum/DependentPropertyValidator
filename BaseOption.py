from Exceptions import DependencyInputError, ValidationError
import re



class BaseOption:
    """
    Abstract non-instantiatable base class for dependency options.
    Provides interface and dynamically constructs subclass instances.
    """
    def __new__(cls, *args, **kwargs):
        """
        Prevent instantiation of base class.
        """
        if cls is BaseOption:
            raise TypeError("BaseOption class may not be instantiated.")
        return object.__new__(cls)

    @staticmethod
    def construct(option: str, condition):
        """
        Match option string to specific concrete BaseOption subclass and return an instance.
        :param option: string specification of option
        :param condition: condition specification
        :return: option subclass instance
        """
        option_class = BaseOption.find_single_case_insensitive_submatch_in_list(
                          option, BaseOption.__subclasses__(), 'option name')  # match option string to subclass
        if option_class:
            return option_class(condition)  # construct and return if found match

    @classmethod
    def validate_condition(cls, input_condition):
        """
        Class method used to validate the input condition by comparing with the allowed conditions of the option
        subclass, using case-insensitive, start-of-string matching.
        :cls: the option subclass
        :param input_condition: a string describing the condition imposed on the type-pair.
        :return: condition in its standardized form, as found in the allowed conditions. For now only string.
        """
        if not hasattr(cls, 'allowed_conditions'):  # make sure the subclass has an 'allowed conditions' attribute
            raise NotImplementedError('allowed_conditions for selected option are not specified')
        return BaseOption.find_single_case_insensitive_submatch_in_list(
                          input_condition, cls.allowed_conditions, 'condition')
        # Return the condition string as found in allowed conditions, to be used when checking if the input arguments
        # satisfy the imposed condition.

    @staticmethod
    def find_single_case_insensitive_submatch_in_list(pattern, lst, error_string):
        """
        Find case-insensitive start-of-string matches to pattern in a list of strings or subclasses.
        :param pattern: string of pattern to match
        :param lst: list of strings/subclasses to find matches in.
        :param error_string: string input for error message.
        :return: matched string or subclass as found in the input list (lst).
        """
        # Find case-insensitive start-of-string matches using regular expressions
        if isinstance(lst[0], type):  # subclass list
            matches = [subclass for subclass in lst if re.search('^' + pattern, subclass.__name__, re.IGNORECASE)]
        else:  # string list
            matches = [string for string in lst if re.search('^' + pattern, string, re.IGNORECASE)]

        # Make sure only a single element was matched.
        if not matches:
            raise DependencyInputError('Invalid {0}.'.format(error_string))
        if len(matches) > 1:
            raise DependencyInputError('Ambiguous {0}.'.format(error_string))
        return matches[0]  # return matched subclass or full string

    def validate_input(self, dependent_property_validator):
        """
        Abstract method invoked when options/conditions are assessed for input arguments. Overriden by specific
        concrete option subclasses.
        :param dependent_property_validator: DependentPropertyValidator object containing the input
        arguments/properties.
        :return: boolean representing whether the input argument pair satisfies the condition (True) or not.
        """
        pass


class CompareSize(BaseOption):
    allowed_conditions = ['gt', 'lt', 'eq', 'ne', 'ge', 'le']

    def __init__(self, condition):
        """
        Match condition by comparing with the allowed conditions of CompareSize, using case-insensitive,
        start-of-string matching.
        :param condition: string condition to be matched with allowed_conditions
        """
        self.matched_condition = CompareSize.validate_condition(condition)

    def validate_input(self, dependent_property_validator):
        """
        Concrete method invoked when CompareSize option/condition is assessed for input arguments.
        :param dependent_property_validator: DependentPropertyValidator object containing the input
        arguments/properties.
        :return:  boolean representing whether the input argument pair satisfies the size comparison condition (True)
        or not.
        """
        # Input arguments must implement the __len__ method to compare sizes.
        if not callable(getattr(dependent_property_validator.first_input_property.input, '__len__', None)):
            raise ValidationError('Cannot compare input sizes. First input property has no __len__ '
                                  'method implementation.')
        if not callable(getattr(dependent_property_validator.second_input_property.input, '__len__', None)):
            raise ValidationError('Cannot compare input sizes. Second input property has no __len__ '
                                  'method implementation.')

        # Validate input by using a switch class which matches string condition to a function.
        condition_switch = CompareSize.ConditionSwitch(dependent_property_validator)
        return condition_switch.switch(self.matched_condition)

    class ConditionSwitch:
        """
        Switch class for CompareSize, implementing a comparison function for each allowed condition.
        """
        def __init__(self, dependent_property_validator):
            """
            :param dependent_property_validator: DependentPropertyValidator object containing the input
            arguments/properties.
            """
            self.first_input_property = dependent_property_validator.first_input_property.input
            self.second_input_property = dependent_property_validator.second_input_property.input

        def switch(self, condition):
            """
            A switch which matches a function to each possible input string condition (returning False if the condition
            is invalid), and evaluates it with the input arguments.
            :param condition: string condition
            :return: The output of the function matched with the condition, evaluated for the input arguments.
            """
            return getattr(self, condition, lambda: False)()

        # condition functions
        def gt(self): return len(self.first_input_property) > len(self.second_input_property)
        def ge(self): return len(self.first_input_property) >= len(self.second_input_property)
        def lt(self): return len(self.first_input_property) < len(self.second_input_property)
        def le(self): return len(self.first_input_property) <= len(self.second_input_property)
        def eq(self): return len(self.first_input_property) == len(self.second_input_property)
        def ne(self): return len(self.first_input_property) != len(self.second_input_property)


