from requests import Request, Session

import json

token = None
verify = True

def set_token(new_token:str):
    global token
    token = new_token

def set_verify(new_verify:any):
    global verify
    verify = new_verify


def get(url:str, as_json:bool=True):
    return generic_request(url, as_json, call='GET')

def post(url:str, data:{}):
    return generic_request(url, call='POST', data=data)

def patch(url:str, data:{}):
    return generic_request(url, call='PATCH', data=data)

def delete(url:str, data:{}):
    return generic_request(url, call='DELETE', data=data)



def generic_request(url:str, as_json:bool=True, call='GET', data:{}=None):

    global token, verify

    s = Session()
    s.verify = verify

    if as_json and data is not None:
        req = Request(call,  url, json=data)
    else:
        req = Request(call,  url, data=data)

    prepped = s.prepare_request(req)


    if token is not None:
        prepped.headers['Authorization'] = f"bearer {token}"

    r = s.send(prepped)
    r.raise_for_status()


    if as_json and r.text:
        return json.loads( r.text ), token
    else:
        return r.text, token
