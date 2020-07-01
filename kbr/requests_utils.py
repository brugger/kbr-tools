from requests import Request, Session

import json

token = None

def set_token(new_token:str):
    global token
    token = new_token

def request_call(url:str, as_json:bool=True):

    s = Session()
    req = Request('GET',  url, )

    prepped = s.prepare_request(req)

    global token

    if token is not None:
        prepped.headers['Authorization'] = f"bearer {token}"

    r = s.send(prepped)
    r.raise_for_status()

    token = None

    if as_json:
        if 'Authorization' in r.headers:
            token = r.headers['Authorization'][7:]

        return json.loads( r.text ), token
    else:
        return r.text, token


def get_info(instance:str) -> {}:
    return request_call(f"{instance}/info")
