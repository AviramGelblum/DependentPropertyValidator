from PropertyDependency import PropertyDependency
from InputProperty import InputProperty
from Exceptions import ValidationError


class DependentPropertyValidator:
    def __init__(self, independent_property, dependent_property):
        self.independent_input_property = InputProperty(independent_property)
        self.dependent_input_property = InputProperty(dependent_property)
        self.property_dependencies = []

    # region Instance Methods
    def add_property_dependency(self, input_dependency, **options_dict):
        dependency = PropertyDependency(input_dependency, options_dict)
        self.property_dependencies.append(dependency)

    def validate(self):
        if not self.property_dependencies:
            raise ValidationError('No property dependency provided.')

        relevant_options = self.validate_types()
        if relevant_options:
            self.validate_conditions(relevant_options)

    def validate_types(self):
        matching_dependencies = (dependency for dependency in self.property_dependencies
                                 if DependentPropertyValidator.check_partial_property_type(
                                 self.independent_input_property.type,dependency.independent_property.type))
        relevant_option_lists_list = []
        error_string = 'Independent'
        for matching_dependency in matching_dependencies:
            error_string = 'Dependent'
            allowed_dependent_type = matching_dependency.dependent_property.type
            if DependentPropertyValidator.check_partial_property_type(
               self.dependent_input_property.type, allowed_dependent_type):  # match
                if matching_dependency.options:
                    relevant_option_lists_list.append(matching_dependency.options)
                return relevant_option_lists_list

        raise ValidationError('{} property type does not match allowed types.'.format(error_string))
    # endregion

    # region Static Methods

    def validate_conditions(self, relevant_option_lists_list):
        for relevant_option_list in relevant_option_lists_list:
            validate_input_gen = (option.validate_input(self) for option in relevant_option_list)
            validated = True
            while validated:
                try:
                    validated = next(validate_input_gen)
                except StopIteration:
                    return
        raise ValidationError('Input does not meet any option condition.')

    @staticmethod
    def check_partial_property_type(submitted_type, allowed_type):
        string_allowed_input_property = ', '.join(map(str, allowed_type))
        string_submitted_input_property = ', '.join(map(str, submitted_type))

        string_length_allowed_input_property = len(string_allowed_input_property)
        return string_allowed_input_property == string_submitted_input_property[
                                            0:string_length_allowed_input_property]

    # endregion


