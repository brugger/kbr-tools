import unittest


import kbr.requests_utils as requests

instance = 'http://localhost:8088/'
token    = 'my_secret'

def test_set_token():
    requests.set_token( token )


def test_request_get():

    requests.set_token( token )
    response, return_token = requests.get(instance)

    assert return_token == token

def test_request_post():

    requests.set_token( token )
    response, return_token = requests.post(instance, {'user': 'me'})

    assert return_token == token

def test_request_patch():

    requests.set_token( token )
    response, return_token = requests.patch(instance, {'user': 'me'})

    assert return_token == token

def test_request_delete():

    requests.set_token( token )
    response, return_token = requests.delete(instance, {'user': 'me'})

    assert return_token == token
