from Option import Option
from Exceptions import DependencyInputError

# region Property Dependency Class
class PropertyDependency:
    # allowed_options = [option.__name__ for option in Option.__subclasses__()]

    def __init__(self, input_dependency, options_dict):
        self.independent_property = PropertyType(input_dependency[0])
        self.dependent_property = PropertyType(input_dependency[1])
        self.options = []
        self.construct_options(options_dict)

    def construct_options(self, options_dict):
        for key, value in options_dict.items():
            specified_option = Option.construct_option_instance(key, value)
            self.options.append(specified_option)

# endregion

# region Property Type Class
class PropertyType:
    def __init__(self, property_type):
        if isinstance(property_type, list):
            self.type = property_type
            self.depth = len(property_type)
        else:
            self.type = [property_type]
            self.depth = 1
        self.validate_type()

    def __len__(self):
        return self.depth

    def validate_type(self):
        if self.depth == 1:
            if isinstance(self.type[0],type):
                return
        elif self.depth > 1:
            if all(isinstance(x, type) for x in self.type):
                return
        raise DependencyInputError('Property dependency type not formatted correctly.')

# endregion