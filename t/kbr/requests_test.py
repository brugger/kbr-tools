import unittest

import responses

import nels_galaxy_api.api_requests as requests

instance = 'http://localhost:8088/'
token    = 'my_secret'

def test_set_token():
    requests.set_token( token )


def test_request_get():

    requests.set_token( token )
    response, return_token = requests.request_get(instance)

    assert return_token == token

def test_request_post():

    requests.set_token( token )
    response, return_token = requests.request_post(instance, {'user': 'me'})

    assert return_token == token

def test_request_patch():

    requests.set_token( token )
    response, return_token = requests.request_patch(instance, {'user': 'me'})

    assert return_token == token

def test_request_delete():

    requests.set_token( token )
    response, return_token = requests.request_delete(instance, {'user': 'me'})

    assert return_token == token
