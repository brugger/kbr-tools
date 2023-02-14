import unittest
import time


import kbr.type_utils as type_utils


def test_is_string_001():
    assert type_utils.is_string('salty') == True

def test_is_string_002():
    assert type_utils.is_string({}) == False

def test_is_string_003():
    assert type_utils.is_string(32) == False


def test_is_int_000():
    assert type_utils.is_int(10000) == True

def test_is_int_001():
    assert type_utils.is_int('salty') == False

def test_is_int_002():
    class I( object ):
        def __int__():
            return 2

    assert type_utils.is_int(I()) == False

def test_is_int_003():
    assert type_utils.is_int(32.9) == False


def test_is_int_004():
    assert type_utils.is_int("32") == False


def test_is_float_001():
    assert type_utils.is_float('salty') == False

def test_is_float_002():
    class I( object ):
        def __float__():
            return 2.9

    assert type_utils.is_float(I()) == False

def test_is_float_003():
    assert type_utils.is_float(32.9) == True

def test_is_number_001():
    assert type_utils.is_number('salty') == False

def test_is_number_002():
    class I( object ):
        def __number__():
            return 2.9

    assert type_utils.is_number(I()) == False

def test_is_number_003():
    assert type_utils.is_number(32.9) == True

def test_is_number_004():
    assert type_utils.is_number(32) == True


def test_is_positive_number_001():
    assert type_utils.is_positive_number(1) == True

def test_is_positive_number_002():
    assert type_utils.is_positive_number(0) == False

def test_is_positive_number_003():
    assert type_utils.is_positive_number(-10) == False


def test_is_negative_number_001():
    assert type_utils.is_negative_number(1) == False

def test_is_negative_number_002():
    assert type_utils.is_negative_number(0) == False

def test_is_negative_number_003():
    assert type_utils.is_negative_number(-10) == True


def test_none_or_contains_value_001():
    assert type_utils.none_or_contains_value(None, None) == True

def test_none_or_contains_value_002():
    assert type_utils.none_or_contains_value(None, 10) == True

def test_none_or_contains_value_004():
    assert type_utils.none_or_contains_value([1,2,2,4,5], 4) == True

def test_none_or_contains_value_005():
    assert type_utils.none_or_contains_value([1,2,2,4,5], 30) == False


def test_none_or_contains_value_006():
    assert type_utils.none_or_contains_value([1,2,2,4,5], None) == False
