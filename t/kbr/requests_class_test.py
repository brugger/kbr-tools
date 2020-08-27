import unittest


import kbr.requests_class as requests_class

instance = 'http://localhost:8088/'
token    = 'my_secret'

def test_set_token():
    r = requests_class.KBRRequests(base_url=instance)
    r.set_token( token )


def test_request_get():

    r = requests_class.KBRRequests(base_url=instance)
    r.set_token( token )
    response, return_token = r._get()

    assert return_token == token

def test_request_post():

    r = requests_class.KBRRequests(base_url=instance)
    r.set_token( token )
    response, return_token = r._post()

    assert return_token == token

def test_request_patch():

    r = requests_class.KBRRequests(base_url=instance)
    r.set_token( token )
    response, return_token = r._patch()

    assert return_token == token

def test_request_delete():

    r = requests_class.KBRRequests(base_url=instance)
    r.set_token( token )
    response, return_token = r._delete()

    assert return_token == token
