import pytest
import shutil

import kbr.version_utils as version_utils


def create_temporary_copy(filename):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'temp_file_name')
    shutil.copy2(path, temp_path)
    return temp_path



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


#def test_version_bump_version_001():


def test_info_001(capsys):
    version_utils.ANGULAR_SETUP = 'not_found'
    version_utils.VERSION_FILE = 'test_version.json'
    version_utils.info()
    captured = capsys.readouterr()
    assert captured.out == "Version: 1.2.3\n"

def test_info_002(capsys):
    version_utils.ANGULAR_SETUP = 'not_found'
    version_utils.VERSION_FILE = 'test_version.json'
    version_utils.info("v: ")
    captured = capsys.readouterr()
    assert captured.out == "v: 1.2.3\n"


def test_info_003(capsys):
    version_utils.VERSION_FILE = 'not_found'
    version_utils.ANGULAR_SETUP = 'test_setup.ts'
    version_utils.info()
    captured = capsys.readouterr()
    assert captured.out == "Version: 2.3.4\n"

def test_info_004(capsys):
    version_utils.VERSION_FILE = 'not_found'
    version_utils.ANGULAR_SETUP = 'test_setup.ts'
    version_utils.info("v: ")
    captured = capsys.readouterr()
    assert captured.out == "v: 2.3.4\n"

def test_info_005(capsys):
    version_utils.VERSION_FILE = 'not_found'
    version_utils.ANGULAR_SETUP = 'not_found'
    with pytest.raises( FileNotFoundError):
        version_utils.info("v: ")



def test_as_string_001():
    version_utils.ANGULAR_SETUP = 'not_found'
    version_utils.VERSION_FILE = 'test_version.json'
    assert version_utils.as_string() == "1.2.3"

def test_as_string_002():
    version_utils.VERSION_FILE = 'not_found'
    version_utils.ANGULAR_SETUP = 'test_setup.ts'
    assert version_utils.as_string() == "2.3.4"

def test_as_string_003():
    version_utils.VERSION_FILE = 'not_found'
    version_utils.ANGULAR_SETUP = 'not_found'
    with pytest.raises( FileNotFoundError):
        version_utils.as_string()
