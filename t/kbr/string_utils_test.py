import pytest

import kbr.string_utils as string_utils


def test_comma_sep_001():
    assert string_utils.comma_sep([]) == ""

def test_comma_sep_002():
    with pytest.raises(TypeError):
        string_utils.comma_sep()

def test_comma_sep_003():
    assert string_utils.comma_sep([1, "2", "test"]) == "1, 2, test"
