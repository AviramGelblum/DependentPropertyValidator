from PropertyDependency import PropertyDependency
from InputProperty import InputProperty
from Exceptions import ValidationError


class DependentPropertyValidator:
    """
    Multiple-level type validation for two given arguments (often properties of a class), in a dependent manner, given
    possible type-pairs. The class can check for other optional dependencies between the input  arguments, such as array
    size.
    """

    def __init__(self, first_property, second_property):
        """
        Input arguments/properties to perform validation on.
        """
        self.first_input_property = InputProperty(first_property)
        self.second_input_property = InputProperty(second_property)
        self.property_dependencies = []  # initialization of the type-pair/option dependency list

    # region Instance Methods
    def add_property_dependency(self, input_dependency: list, **options_dict):
        """
        Method allowing the user to specify an allowed type-pair, along with its associated options.
        :param input_dependency: list containing two elements, corresponding to the two input arguments in order.
        Each of which can either be a type or a list of types. These specify the allowed type at each level of the
        input arguments. For example: [[list, str],int] specifies that the first argument is expected to be a list of
        strings, and the second an integer. [list, list] specifies that both arguments are expected to be lists (of any type).
        :param options_dict: keyword arguments specifying the options selected for the type-pair dependency.
        """
        dependency = PropertyDependency(input_dependency, options_dict)
        self.property_dependencies.append(dependency)

    def validate(self):
        """
        Method allowing the user to validate the input arguments according to the type-pair/options dependencies
        that were added to the DependentPropertyValidator object.
        """
        if not self.property_dependencies:
            raise ValidationError('No property dependency provided.')

        relevant_options = self.__validate_types()  # validate the types of the input arguments
        if relevant_options:
            self.__validate_conditions(relevant_options)  # validate the conditions imposed by the options for the
            # relevant type-pair dependencies

    def __validate_types(self):
        """
        Validation of the input arguments' types according to the type-pair dependencies added to the
        DependentPropertyValidator object.
        """
        # find all dependencies which match the type of the first input argument
        matching_dependencies = (dependency for dependency in self.property_dependencies
                                 if DependentPropertyValidator.check_partial_property_type(
                                 self.first_input_property.type, dependency.first_property.type))
        relevant_option_lists_list = []
        error_string = 'First'
        for matching_dependency in matching_dependencies:
            # out of all the matching dependencies, find those that also match the second input argument
            error_string = 'Second'
            allowed_second_type = matching_dependency.second_property.type
            if DependentPropertyValidator.check_partial_property_type(
               self.second_input_property.type, allowed_second_type):
                # if both arguments match, add options to a list to be validated in __validate_conditions subsequently
                if matching_dependency.options:
                    relevant_option_lists_list.append(matching_dependency.options)
                return relevant_option_lists_list

        raise ValidationError('{} property type does not match allowed types.'.format(error_string))

    def __validate_conditions(self, relevant_option_lists_list: list):
        """
        Validation of the conditions imposed on the input arguments by to the options specified in the
        matching type-pair dependencies added to the DependentPropertyValidator object.
        :param relevant_option_lists_list: list of lists of options of type-pair dependencies matching the types of
        the input arguments.
        """
        # Logical "or" validation: if multiple type-pair dependencies match the input arguments' types, only a single
        # dependency option list must be fulfilled for the input argument pair to be valid.

        # Loop over type-matching dependencies, getting each dependency's options/conditions list
        for relevant_option_list in relevant_option_lists_list:
            validate_input_gen = (option.validate_input(self) for option in relevant_option_list)
            validated = True
            while validated:  # go over all conditions in current option list
                try:
                    # If condition is met, continue to next condition in list. If not, break while loop to check the
                    # next option list.
                    validated = next(validate_input_gen)
                except StopIteration:
                    # If no more conditions in the list need to be verified, all conditions are satisfied and the
                    # method returns without raising error (i.e. the input conditions are validated).
                    return

        # Raise error if no conditions list was fully satisfied.
        raise ValidationError('Input does not meet any option condition.')

    # endregion

    # region Static Methods

    @staticmethod
    def check_partial_property_type(submitted_type: list, allowed_type: list) -> bool:
        """
        Method used to check if a list is partially contained in another list, starting at the first element, using
        string comparison.
        In the context of DependentPropertyValidator, this method is used to compare (possibly partial) type list
        specified in dependency with the full multi-level type of the input.
        :param submitted_type: The full list (The multi-level full list of types of an input argument)
        :param allowed_type: The contained list (The list of types allowed in the dependency, can be partial)
        """
        # transform lists to strings
        string_allowed_input_property = ', '.join(map(str, allowed_type))
        string_submitted_input_property = ', '.join(map(str, submitted_type))

        # Check if the first N characters of the full list constitute the partial list, where N is the length of the
        # partial list.
        string_length_allowed_input_property = len(string_allowed_input_property)
        return string_allowed_input_property == string_submitted_input_property[
                                            0:string_length_allowed_input_property]

    # endregion