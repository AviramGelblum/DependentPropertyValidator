from PropertyDependency import PropertyDependency
from InputProperty import InputProperty
from Exceptions import ValidationError

class DependentPropertyValidator:

    def __init__(self):
        self.property_dependencies = []

    # region Instance Methods
    def add_property_dependency(self, input_dependency, **options_dict):
        dependency = PropertyDependency(input_dependency, options_dict)
        self.property_dependencies.append(dependency)

    def validate(self, independent_property, dependent_property):
        independent_input_property = InputProperty(independent_property)
        dependent_input_property = InputProperty(dependent_property)

        relevant_options = self.validate_types(independent_input_property, dependent_input_property)
        if relevant_options:
            self.validate_conditions(independent_input_property, dependent_input_property,
                                     relevant_options)

    def validate_types(self, independent_input_property, dependent_input_property):
        matching_dependencies = (dependency for dependency in self.property_dependencies
                                 if DependentPropertyValidator.check_partial_property_type(
                                 independent_input_property.type, dependency.independent_property.type))
        relevant_options = []
        error_string = 'Independent'
        for matching_dependency in matching_dependencies:
            error_string = 'Dependent'
            allowed_dependent_type = matching_dependency.dependent_property.type
            if DependentPropertyValidator.check_partial_property_type(
               dependent_input_property.type, allowed_dependent_type):  # match
                if matching_dependency.options:
                    relevant_options.append(matching_dependency.options)
                return relevant_options

        raise ValidationError('{} property type does not match allowed types.'.format(error_string))
    # endregion

    # region Static Methods

    @staticmethod
    def validate_conditions(independent_input_property, dependent_input_property,
                            relevant_options):
        for option in relevant_options:
            option.validate_input(independent_input_property, dependent_input_property)

    @staticmethod
    def check_partial_property_type(submitted_type, allowed_type):
        string_allowed_input_property = ', '.join(map(str, allowed_type))
        string_submitted_input_property = ', '.join(map(str, submitted_type))

        string_length_allowed_input_property = len(string_allowed_input_property)
        return string_allowed_input_property == string_submitted_input_property[
                                            0:string_length_allowed_input_property]

    # endregion


