class DependentPropertyValidator:

    def __init__(self):
        self.property_dependencies = []

    # region Instance Methods
    def add_property_dependency(self, dependency_list):
        dependency = PropertyDependency(dependency_list[0], dependency_list[1])
        self.property_dependencies.append(dependency)

    def validate(self, independent_property, dependent_property):
        independent_input_property = InputProperty(independent_property)
        dependent_input_property = InputProperty(dependent_property)

        relevant_dependencies = self.validate_types(independent_input_property, dependent_input_property)
        foobar = self.validate_conditions(independent_input_property,dependent_input_property, relevant_dependencies)

    def validate_types(self, independent_input_property, dependent_input_property):
        matching_independent_type_dependencies = (dependency for dependency in self.property_dependencies
                                                    if DependentPropertyValidator.check_partial_property_type(
                                                    independent_input_property.type, dependency.independent_property.type))
        relevant_dependencies = []
        error_string = 'Independent'
        for matching_independent_type_dependency in matching_independent_type_dependencies:
            error_string = 'Dependent'
            allowed_dependent_type = matching_independent_type_dependency.dependent_property.type
            #todo: change to options instead of the whole dependency.
            if DependentPropertyValidator.check_partial_property_type(
               dependent_input_property.type, allowed_dependent_type):  # match
                relevant_dependencies.append(matching_independent_type_dependency)

        if relevant_dependencies:
            return relevant_dependencies

        raise ValidationError('{} property type does not match allowed types.'.format(error_string))

    def validate_conditions(self, independent_input_property, dependent_input_property, relevant_dependencies):
        #todo: implement
        return
    # endregion

    # region Static Methods
    @staticmethod
    def check_partial_property_type(submitted_type, allowed_type):
        string_allowed_input_property = ', '.join(map(str, allowed_type))
        string_submitted_input_property = ', '.join(map(str, submitted_type))

        string_length_allowed_input_property = len(string_allowed_input_property)
        return string_allowed_input_property == string_submitted_input_property[
                                            0:string_length_allowed_input_property]

    # endregion


class PropertyDependency:
    def __init__(self, independent_property_type, dependent_property_type):
        self.independent_property = PropertyType(independent_property_type)
        self.dependent_property = PropertyType(dependent_property_type)


class PropertyType:
    def __init__(self, property_type):
        if isinstance(property_type, list):
            self.type = property_type
            self.depth = len(property_type)
        else:
            self.type = [property_type]
            self.depth = 1

    def __len__(self):
        return self.depth


class InputProperty:
    def __init__(self, input_property):
        # self.input = input_property
        self.type = [type(input_property)]
        self.__get_deep_types(input_property, 0)
        self.depth = len(self.type)

    def __get_deep_types(self, property_segment, level):
        # todo: add support for custom iterables? probably not needed, right?
        # todo: add support for whole structure same data type checking

        if isinstance(property_segment, (list, tuple)):
            # check that all items are of the same type
            assert InputProperty.check_same_type_list(property_segment),\
                "Elements of {0} property provided are not all of the same type.".format(self.type[
                    level].__name__)
            self.type.append(type(property_segment[0]))
            self.__get_deep_types(property_segment[0], level + 1)
        elif isinstance(property_segment, dict):
            assert InputProperty.check_same_type_dict(property_segment), \
                "Elements of {0} property provided are not all of the same type.".format(self.type[
                    level].__name__)
            first_key = next(iter(property_segment))
            self.type.append(type(property_segment[first_key]))
            self.__get_deep_types(property_segment[first_key], level + 1)

    @staticmethod
    def check_same_type_list(lst):
        return all(isinstance(x, type(lst[0])) for x in lst)

    @staticmethod
    def check_same_type_dict(dct):
        first_key = next(iter(dct))
        return all(isinstance(x[0], type(first_key)) and isinstance(x[1], type(dct[first_key])) for
                   x in dct.items())

    def __len__(self):
        return self.depth


class ValidationError(Exception):
    pass
