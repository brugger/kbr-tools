import unittest
import time


import kbr.cache_utils as cache

instance = 'localhost'
port     = 11211
namespace = ''

def _connect():
    cache.disconnect()
    cache.connect( instance, port, namespace=namespace )


def test_connect():
    _connect()
    cache.disconnect()

def test_set():
    _connect()
    cache.set('key-A', 1234)

def test_get():
    _connect()
    cache.set('key-A', 1234)
    value = cache.get('key-A')
    assert int(value) == 1234

def test_delete():
    _connect()
    cache.set('key-A', 1234)
    cache.delete('key-A')
    value = cache.get('key-A')
    assert value == None

def test_set_expire():
    _connect()
    cache.set('key-A', 1234, 2)
    time.sleep(2)
    value = cache.get('key-A')
    assert value == None

def test_set_expire_pre():
    _connect()
    cache.set('key-A', 1234, 20)
    time.sleep(1)
    value = cache.get('key-A')
    assert int(value) == 1234


def test_set_exists_true():
    _connect()
    cache.set('key-A', 1234, 2)
    assert cache.exists('key-A')

def test_set_exists_false():
    _connect()
    cache.set('key-A', 1234, 2)
    assert cache.exists('key-B') == False

def test_flush():
    _connect()
    cache.set('key-A', 1234, 2)
    cache.flush()
    assert cache.exists('key-A') == False
