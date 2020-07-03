import pytest
import re
import tempfile
import os

import kbr.crypt_utils as utils


def test_init():

    utils.init('Secret_key')


def test_encrypt_str():
    utils.init('Secret_key')
    e = utils.encrypt_value('42')
    assert e == 'bc729496af0697be'


def test_encrypt_int():
    utils.init('Secret_key')
    e = utils.encrypt_value(42)
    assert e == 'bc729496af0697be'


def test_decrypt_str():
    utils.init('Secret_key')
    d = utils.decrypt_value('bc729496af0697be')
    assert d == '42'



