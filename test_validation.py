import pytest
from DependentPropertyValidator import DependentPropertyValidator
from Exceptions import ValidationError, DependencyInputError

#region Wrappers
def single_dependent_validation(A, B, types_list, **options_dict):
    DPV = DependentPropertyValidator(A, B)
    DPV.add_property_dependency(types_list, **options_dict)
    try:
        DPV.validate()
        return True
    except (ValidationError, DependencyInputError) as err:
        return err.args[0]

def multiple_dependent_validation(A, B, types_list_list, **options_dict):
    DPV = DependentPropertyValidator(A, B)
    for type_list in types_list_list:
        DPV.add_property_dependency(type_list, **options_dict)
    try:
        DPV.validate()
        return True
    except (ValidationError, DependencyInputError) as err:
        return err.args[0]

#endregion

# region Type Dependency Integration Validation Tests



def test_correct_strings():
    test = single_dependent_validation('ff', 'dfd', [str, str])  # only single quotes
    assert test
    test = single_dependent_validation('f', 'dfd', [str, str])  # one char string
    assert test
    test = single_dependent_validation("ffg", 'dfd', [str, str])  # double and single quotes
    assert test
    test = single_dependent_validation("ffg", "dfd", [str, str])  # only double quotes
    assert test

def test_failed_strings():
    test = single_dependent_validation('ff', 'dfd', [str, int])  # second
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation('ff', 'dfd', [int, str])  # first
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation('ff', 'dfd', [int, dict])  # both
    assert test == 'First property type does not match allowed types.'

def test_correct_ints():
    test = single_dependent_validation(3, 4, [int, int])
    assert test

def test_failed_ints():
    test = single_dependent_validation(3, 4, [list, int])  # first
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation(3, 4, [int, str])  # second
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation(3, 4, [list, str])  # both
    assert test == 'First property type does not match allowed types.'

def test_correct_lists():
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [list, list])
    assert test
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [list, list])  # diff content
    # type
    assert test
    test = single_dependent_validation([3, 4, 5], ['h', 'h'], [list, list])  # diff size
    assert test

def test_failed_lists():
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [list, int])  # second
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation(['h', 'h', 'h'], [6, 7, 8], [str, list])  # first
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation([3, 4, 5], ['h', 'h'], [tuple, int])  # both
    assert test == 'First property type does not match allowed types.'

def test_correct_dicts():
    test = single_dependent_validation({'g': 4, 'fg': 5, 'f': 4}, {'g': 'gfg', 'fg': 'g',
                                                                   'f': 'gf'},[dict, dict])  # diff value type
    assert test
    test = single_dependent_validation({'g': 4, 'fg': 5, 'f': 4}, {'m': 34, 'n': 43, 'k': 76},
                                [dict, dict])  # diff key
    assert test
    test = single_dependent_validation({'g': 4, 'fg': 5, 'f': 4}, {'m': 34}, [dict, dict])  # diff size
    assert test


def test_failed_dicts():
    test = single_dependent_validation({'g': 4, 'fg': 5, 'f': 4}, {'m': 34, 'n': 43, 'k': 76},
                                       [dict, str])  # second
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation({'g': 4, 'fg': 5, 'f': 4}, {'m': 34, 'n': 43, 'k': 76},
                                       [int, dict])  # first
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation({'g': 4, 'fg': 5, 'f': 4}, {'m': 34, 'n': 43, 'k': 76},
                                       [list, list])  # both
    assert test == 'First property type does not match allowed types.'

def test_2d_correct_nested_lists():
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [[list, int], [list, int]])
    assert test
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [[list, int], list])  # 1d second
    # property type
    assert test
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [list, [list, int]])  # 1d
    # first property type
    assert test


def test_2d_failed_nested_lists():
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, int], int])  #
    # second f1
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, int], str])  #
    # second f1 t2
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, int], [list, int]])  #
    # second t1 f2
    assert test == 'Second property type does not match allowed types.'

    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [str, [list, str]])  #
    # first f1
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [int, [list, str]])  #
    # first f1 t2
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, str], [list, str]])  #
    # first t1 f2
    assert test == 'First property type does not match allowed types.'


def test_3d_correct_nested_lists():
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [[list, list, int], [list, list, str]])
    assert test
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [[list, list, int], list])  # 1d second property type
    assert test
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [list, [list, list, str]])  # 1d first property type
    assert test
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [[list, list, int], [list, list]])  # 2d second property type
    assert test
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [[list, list], [list, list, str]])  # 2d first property type
    assert test

def test_3d_failed_nested_lists():
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], int])  # second f1
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], str])  # second t3
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], [list, list, int]])  # second t1-2 f3
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], [list, tuple, int]])  # second t1 f2-3
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], [list, tuple, str]])  # second t1 f2 t3
    assert test == 'Second property type does not match allowed types.'
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [str, [list, list, str]])  # first f1
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [int, [list, list, str]])  # first t3
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, str], [list, list, str]])  # first t1-2 f3
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, tuple, str], [list, list, str]])  # first t1 f2-3
    assert test == 'First property type does not match allowed types.'
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, tuple, int], [list, list, str]])  # first t1 f2 t3
    assert test == 'First property type does not match allowed types.'




def test_multiple_with_correct_nested_lists():
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, list], [int, list]])
    assert test
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[[list, int], list],
                                                                      [[list, int], int]])
    assert test

def test_multiple_with_failed_nested_lists():
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, int], [int, list]])
    assert test == 'Second property type does not match allowed types.'
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[int, str], [int, list]])
    assert test == 'First property type does not match allowed types.'
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[[list, str], list],
                                                                      [[list, int], int]])
    assert test == 'Second property type does not match allowed types.'

# endregion

# region Option Integration Validation Tests
def test_compare_size():
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [list, list], CompareSize='ge')
    assert test
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [list, list], compare='ge')
    assert test
    test = single_dependent_validation([3, 4, 5, 6], [6, 7, 8], [list, list], compare='ge')
    assert test
    test = single_dependent_validation([3, 4], [6, 7, 8], [list, list], compare='ge')
    assert test == 'Input does not meet any option condition.'


    test = multiple_dependent_validation([3, 4, 5], [6, 7, 8],[[[list, int], list],[int, str]], compare='ge')
    assert test

#endregion

#region Unit Tests
def test_DependentPropertyValidator_validate():
    DPV = DependentPropertyValidator([4,5,6],[7,8,9])

    # no dependencies error:
    try:
        DPV.validate()
        assert False
    except ValidationError as err:
        assert err.args[0] == 'No property dependency provided.'


