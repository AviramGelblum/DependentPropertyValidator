from BaseOption import BaseOption
from Exceptions import DependencyInputError

# region Property Dependency Class


class PropertyDependency:
    """
    Class for type-pair dependency specifications. Contains type-pairs as well as accompanying options/conditions.
    """
    def __init__(self, input_dependency: list, options_dict: dict):
        """
        :param input_dependency: type-pair list, see DependentPropertyValidator.add_property_dependency
        :param options_dict: keyword arguments specifying the options selected for the type-pair dependency.
        """
        self.first_property = PropertyDependencyType(input_dependency[0])
        self.second_property = PropertyDependencyType(input_dependency[1])
        self.options = []  # initialization of the dependency option list
        self.construct_options(options_dict)  # construct option instances

    def construct_options(self, options_dict: dict):
        """
        Construct option instances according to the appropriate BaseOption subclass.
        :param options_dict: dictionary specifying the options/conditions list for the dependency
        """
        for key, value in options_dict.items():
            specified_option = BaseOption.construct(key, value)  # construct option instance
            self.options.append(specified_option)

# endregion

# region Property Dependency Type Class


class PropertyDependencyType:
    """
    Class for input property dependency type. Restructures the input dependency type if needed, and validates it.
    """
    def __init__(self, property_type):
        # property_type can be a single type, implying a single-level type, or a list, implying multi-level type.
        if isinstance(property_type, list):
            self.type = property_type
            self.depth = len(property_type)
        else:
            self.type = [property_type]
            self.depth = 1
        self.validate_type()

    def validate_type(self):
        """
        Validate input property dependency type, to be either type, or a lists of types. Raise error if needed.
        """
        if self.depth == 1:
            if isinstance(self.type[0], type):
                return
        elif self.depth > 1:
            if all(isinstance(x, type) for x in self.type):
                return
        raise DependencyInputError('Property dependency type not formatted correctly.')

# endregion