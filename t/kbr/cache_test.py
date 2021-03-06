import unittest
import time


import kbr.cache_utils as cache

def test_set():
    cache.set('key-A', 1234)

def test_get():
    cache.set('key-A', 1234)
    value = cache.get('key-A')
    assert int(value) == 1234

def test_delete():
    cache.set('key-A', 1234)
    cache.delete('key-A')
    value = cache.get('key-A')
    assert value == None

def test_set_expire():
    cache.set('key-A', 1234, 2)
    time.sleep(2)
    value = cache.get('key-A')
    assert value == None

def test_set_expire_pre():
    cache.set('key-A', 1234, 20)
    time.sleep(1)
    value = cache.get('key-A')
    assert int(value) == 1234


def test_set_exists_true():
    cache.set('key-A', 1234, 2)
    assert cache.exists('key-A')

def test_set_exists_false():
    cache.set('key-A', 1234, 2)
    assert cache.exists('key-B') == False

def test_flush():
    cache.set('key-A', 1234, 2)
    cache.flush()
    assert cache.exists('key-A') == False
