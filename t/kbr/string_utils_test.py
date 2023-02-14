import pytest

import kbr.string_utils as string_utils


def test_comma_sep_001():
    assert string_utils.comma_sep([]) == ""

def test_comma_sep_002():
    with pytest.raises(TypeError):
        string_utils.comma_sep()

def test_comma_sep_003():
    assert string_utils.comma_sep([1, "2", "test"]) == "1, 2, test"



def test_readable_bytes_001():
    assert string_utils.readable_bytes(1023) == "1023B"

def test_readable_bytes_002():
    assert string_utils.readable_bytes(1025) == "1.00 KB"


def test_readable_bytes_003():
    assert string_utils.readable_bytes(2048) == "2.00 KB"

def test_readable_bytes_004():
    assert string_utils.readable_bytes(3*pow(1024, 2)-10*1024) == "2.99 MB"

def test_readable_bytes_005():
    assert string_utils.readable_bytes(3*pow(1024, 2)) == "3.00 MB"

def test_readable_bytes_006():
    assert string_utils.readable_bytes(4*pow(1024, 3)) == "4.00 GB"

def test_readable_bytes_007():
    assert string_utils.readable_bytes(3*pow(1024, 4)-1) == "3.00 TB"


def test_snake2CamelCase_001():
    assert string_utils.snake2CamelCase("Any_b_a_C") == "AnyBAC"

def test_snake2CamelCase_002():
    assert string_utils.snake2CamelCase("any_b_a_c") == "AnyBAC"

def test_snake2CamelCase_003():
    assert string_utils.snake2CamelCase("any__b_a_c") == "AnyBAC"

def test_snake2camelBack_001():
    assert string_utils.snake2camelBack("Any_b_a_C") == "anyBAC"

def test_snake2camelBack_002():
    assert string_utils.snake2camelBack("Any_b_a__C") == "anyBAC"

def test_snake2camelBack_003():
    assert string_utils.snake2camelBack("Any_b_A_C") == "anyBAC"

def test_CamelCase2snake_003():
    assert string_utils.CamelCase2snake("AnyBadAnts") == "any_bad_ants"

def test_CamelCase2snake_003():
    assert string_utils.CamelCase2snake("AnyBadDAnts") == "any_bad_d_ants"

def test_CamelCase2snake_003():
    assert string_utils.CamelCase2snake("anyBadDAnts") == "any_bad_d_ants"

def test_camelBack2snake_001():
    assert string_utils.camelBack2snake("anyBadDAnts") == "any_bad_d_ants"

def test_camelBack2snake_002():
    assert string_utils.camelBack2snake("AnyBadDAnts") == "any_bad_d_ants"

def test_minus2CamelCase_001():
    assert string_utils.minus2CamelCase("Any-Bad-D-Ants") == "AnyBadDAnts"

def test_minus2CamelCase_002():
    assert string_utils.minus2CamelCase("Any--Bad-D-Ants") == "AnyBadDAnts"


def test_minus2camelBack_001():
    assert string_utils.minus2camelBack("Any--Bad-D-Ants") == "anyBadDAnts"


def test_to_CamelCase_001():
    assert string_utils.to_CamelCase("Any--Bad-D-Ants") == "AnyBadDAnts"

def test_to_CamelCase_002():
    assert string_utils.to_CamelCase("anyBadDAnts") == "AnyBadDAnts"

def test_to_CamelCase_003():
    assert string_utils.to_CamelCase("Any--Bad_D_Ants") == "AnyBadDAnts"

def test_to_CamelCase_004():
    assert string_utils.to_CamelCase("AnyBadDAnts") == "AnyBadDAnts"


def test_to_camelBack_001():
    assert string_utils.to_camelBack("Any--Bad-D-Ants") == "anyBadDAnts"

def test_to_camelBack_002():
    assert string_utils.to_camelBack("anyBadDAnts") == "anyBadDAnts"

def test_to_camelBack_003():
    assert string_utils.to_camelBack("Any--Bad_D_Ants") == "anyBadDAnts"

def test_to_camelBack_004():
    assert string_utils.to_camelBack("AnyBadDAnts") == "anyBadDAnts"


def test_to_snake_001():
    assert string_utils.to_snake("Any--Bad-D-Ants") == "any_bad_d_ants"

def test_to_snake_002():
    assert string_utils.to_snake("anyBadDAnts") == "any_bad_d_ants"

def test_to_snake_003():
    assert string_utils.to_snake("Any__Bad_D-Ants") == "any_bad_d_ants"

def test_to_snake_003():
    assert string_utils.to_snake("Any--Bad-D-Ants") == "any_bad_d_ants"



def test_to_minus_001():
    assert string_utils.to_minus("Any--Bad-D-Ants") == "any-bad-d-ants"

def test_to_minus_002():
    assert string_utils.to_minus("anyBadDAnts") == "any-bad-d-ants"

def test_to_minus_003():
    assert string_utils.to_minus("Any__Bad_D-Ants") == "any-bad-d-ants"

def test_to_minus_003():
    assert string_utils.to_minus("Any--Bad-D-Ants") == "any-bad-d-ants"


def test_to_minus_004():
    assert string_utils.to_minus("AnyBadDAnts") == "any-bad-d-ants"


