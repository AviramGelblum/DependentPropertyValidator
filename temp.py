# from DependentPropertyValidator import DependentPropertyValidator
# DPV = DependentPropertyValidator()
# DPV.add_property_dependency([str, str])
# test = DPV.validate('ff', 'dfd')

from Exceptions import DependencyInputError
class A:

    def __new__(cls, *args, **kwargs):
        if cls is A:
            raise TypeError("base class may not be instantiated")
        return object.__new__(cls)


    @staticmethod
    def construct_option_instance(option, condition):
        option_class = A.__validate_option(option, condition)
        if option_class:
            return option_class(condition)


    @staticmethod
    def __validate_option(option_name, condition):
        valid_gen = (option_class for option_class in A.__subclasses__() if option_name is
                      option_class.__name__)
        try:
            return next(valid_gen)
        except StopIteration:
            raise DependencyInputError



    def validate_condition(self):
        pass

    def validate_input(self):
        pass


class CompareSize(A):

    def __init__(self, condition):
        print('well done')

j = A.construct_option_instance('CompareSize',[])
k = A()
b = 1
