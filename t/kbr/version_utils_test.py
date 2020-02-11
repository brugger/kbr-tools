import pytest

import kbr.version_utils as version_utils


def test_bump_major_001():
    assert version_utils._bump_major(1,0,0) == [2,0,0]

def test_bump_major_002():
    assert version_utils._bump_major(1,1,0) == [2,0,0]

def test_bump_major_003():
    assert version_utils._bump_major(1,0,1) == [2,0,0]


def test_bump_minor_001():
    assert version_utils._bump_minor(1,0,0) == [1,1,0]


def test_bump_minor_002():
    assert version_utils._bump_minor(1,0,1) == [1,1,0]


def test_bump_patch_001():
    assert version_utils._bump_patch(1,2,3) == [1,2,4]



def test_bumping_001():
    assert version_utils.bumping('major',1,2,3) == [2,0,0]

def test_bumping_002():
    assert version_utils.bumping('minor',1,2,3) == [1,3,0]

def test_bumping_003():
    assert version_utils.bumping('patch',1,2,3) == [1,2,4]

def test_bumping_004():
    with pytest.raises(RuntimeError):
        version_utils.bumping('majors',1,2,3)
