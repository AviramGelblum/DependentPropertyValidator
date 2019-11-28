import pytest
from DependentPropertyValidator import DependentPropertyValidator, ValidationError

def single_dependent_validation(A, B, types_list):
        DPV = DependentPropertyValidator()
        DPV.add_property_dependency(types_list)
        try:
            DPV.validate(A, B)
            test = True
        except ValidationError:
            test = False
        except:
            raise
        return test

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
    test = single_dependent_validation('ff', 'dfd', [str, int])  # dependent
    assert test is False
    test = single_dependent_validation('ff', 'dfd', [int, str])  # independent
    assert test is False
    test = single_dependent_validation('ff', 'dfd', [int, dict])  # both
    assert test is False

def test_correct_ints():
    test = single_dependent_validation(3, 4, [int, int])
    assert test

def test_failed_ints():
    test = single_dependent_validation(3, 4, [list, int])  # independent
    assert test is False
    test = single_dependent_validation(3, 4, [int, str])  # dependent
    assert test is False
    test = single_dependent_validation(3, 4, [list, str])  # both
    assert test is False

def test_correct_lists():
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [list, list])
    assert test
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [list, list])  # diff content
    # type
    assert test
    test = single_dependent_validation([3, 4, 5], ['h', 'h'], [list, list])  # diff size
    assert test

def test_failed_lists():
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [list, int])  # dependent
    assert test is False
    test = single_dependent_validation(['h', 'h', 'h'], [6, 7, 8], [str, list])  # independent
    assert test is False
    test = single_dependent_validation([3, 4, 5], ['h', 'h'], [tuple, int])  # both
    assert test is False

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
                                       [dict, str])  # dependent
    assert test is False
    test = single_dependent_validation({'g': 4, 'fg': 5, 'f': 4}, {'m': 34, 'n': 43, 'k': 76},
                                       [int, dict])  # independent
    assert test is False
    test = single_dependent_validation({'g': 4, 'fg': 5, 'f': 4}, {'m': 34, 'n': 43, 'k': 76},
                                       [list, list])  # both
    assert test is False

def test_2d_correct_nested_lists():
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [[list, int], [list, int]])
    assert test
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [[list, int], list])  # 1d dependent
    # property type
    assert test
    test = single_dependent_validation([3, 4, 5], [6, 7, 8], [list, [list, int]])  # 1d
    # independent property type
    assert test


def test_2d_failed_nested_lists():
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, int], int])  #
    # dependent f1
    assert test is False
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, int], str])  #
    # dependent f1 t2
    assert test is False
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, int], [list, int]])  #
    # dependent t1 f2
    assert test is False

    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [str, [list, str]])  #
    # independent f1
    assert test is False
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [int, [list, str]])  #
    # independent f1 t2
    assert test is False
    test = single_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, str], [list, str]])  #
    # independent t1 f2
    assert test is False


def test_3d_correct_nested_lists():
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [[list, list, int], [list, list, str]])
    assert test
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [[list, list, int], list])  # 1d dependent property type
    assert test
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [list, [list, list, str]])  # 1d independent property type
    assert test
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [[list, list, int], [list, list]])  # 2d dependent property type
    assert test
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]], [['h', 'f'], ['h', 'g'],
                                                                     ['f','dfdf']],
                                [[list, list], [list, list, str]])  # 2d independent property type
    assert test

def test_3d_failed_nested_lists():
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], int])  # dependent f1
    assert test is False
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], str])  # dependent t3
    assert test is False
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], [list, list, int]])  # dependent t1-2 f3
    assert test is False
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], [list, tuple, int]])  # dependent t1 f2-3
    assert test is False
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, int], [list, tuple, str]])  # dependent t1 f2 t3
    assert test is False
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [str, [list, list, str]])  # independent f1
    assert test is False
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [int, [list, list, str]])  # independent t3
    assert test is False
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, list, str], [list, list, str]])  # independent t1-2 f3
    assert test is False
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, tuple, str], [list, list, str]])  # dependent t1 f2-3
    assert test is False
    test = single_dependent_validation([[3, 3], [4, 5], [5, 6, 7]],
                                [['h', 'f'], ['h', 'g'], ['f', 'dfdf']],
                                [[list, tuple, int], [list, list, str]])  # dependent t1 f2 t3
    assert test is False


def multiple_dependent_validation(A, B, types_list_list):
    DPV = DependentPropertyValidator()
    for type_list in types_list_list:
        DPV.add_property_dependency(type_list)
    try:
        DPV.validate(A, B)
        test = True
    except ValidationError:
        test = False
    except:
        raise
    return test

def test_multiple_with_correct_nested_lists():
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, list], [int, list]])
    assert test
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[[list, int], list],
                                                                      [[list, int], int]])
    assert test

def test_multiple_with_failed_nested_lists():
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[list, int], [int, list]])
    assert test is False
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[int, str], [int, list]])
    assert test is False
    test = multiple_dependent_validation([3, 4, 5], ['h', 'h', 'f'], [[[list, str], list],
                                                                      [[list, int], int]])
    assert test is False

