
class DependentPropertyValidator:

    def __init__(self):
        self.property_dependencies = []

    # region Methods
    def add_property_dependency(self, dependency_list):
        dependency = PropertyDependency(dependency_list[0], dependency_list[1])
        self.property_dependencies.append(dependency)

    def validate(self, independent_property, dependent_property):
            placeholder = 1
    # endregion


class PropertyDependency:
    def __init__(self, independent_property_type, dependent_property_type):
        self.independent_property = PropertyType(independent_property_type)
        self.dependent_property = PropertyType(dependent_property_type)


class PropertyType:
    def __init__(self, property_type):
        self.type = property_type
        self.depth = len(property_type)

    def __len__(self):
        return self.depth


class InputProperty:
    def __init__(self, input_property):
        # self.input = input_property
        self.type = [type(input_property)]
        self.get_depth(input_property, 0)
        self.depth = len(self.type)

    def get_depth(self, property_segment, level):
        # Uses the first branch of the iterable. For now does not confirm all other
        # branches have identical data structure.

        if isinstance(property_segment, (list, tuple)):
            # check that all items are the same type
            assert InputProperty.check_same_type_list(property_segment),\
                "Elements of {0} property provided are not all of the same type.".format(self.type[
                    level].__name__)
            self.type.append(type(property_segment))
            self.get_depth(property_segment[0], level+1)
        elif isinstance(property_segment, dict):
            assert InputProperty.check_same_type_dict(property_segment), \
                "Elements of {0} property provided are not all of the same type.".format(self.type[
                    level].__name__)
            first_key = next(iter(property_segment))
            self.get_depth(property_segment[first_key], level + 1)

    @staticmethod
    def check_same_type_list(lst):
        return all(isinstance(x, type(lst[0])) for x in lst)

    @staticmethod
    def check_same_type_dict(dct):
        first_key = next(iter(dct))
        return all(isinstance(x[0],type(first_key)) and isinstance(x[1],type(dct[first_key])) for
                   x in dct.items())

    def __len__(self):
        return self.depth
