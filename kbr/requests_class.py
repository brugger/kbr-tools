import json 
from urllib.parse import urljoin


from requests import Request, Session


class KBRRequests( object ):
    def __init__(self, base_url:str, token:str=None, verify:any=True):
        self._token = token
        self._base_url = base_url
        self._verify = verify

    def _generic_request(self, url:str, as_json:bool=True, call='GET', data:{}=None, send_as_json:bool=True):

#        print(":::: URL ::::: " , url, flush=True)

        s = Session()
        s.verify = self._verify
        if send_as_json:
            req = Request(call,  url, json=data)
        else:
            req = Request(call,  url, data=data)

        prepped = s.prepare_request(req)


        if self._token is not None:
            prepped.headers['Authorization'] = f"bearer {self._token}"

        r = s.send(prepped)
        r.raise_for_status()

        if as_json and r.text:
            return json.loads( r.text )
        elif r.text:
            return None


    def _get(self, url:str, as_json:bool=True, data:{}=None):
        return self._generic_request(urljoin(self._base_url, url), as_json, call='GET', data=data, send_as_json=False)

    def _post(self, url:str, data:{}):
        return self._generic_request(urljoin(self._base_url, url), call='POST', data=data)

    def _patch(self, url:str, data:{}):
        return self._generic_request(urljoin(self._base_url, url), call='PATCH', data=data)

    def _delete(self, url:str, data:{}):
        return self._generic_request(urljoin(self._base_url, url), call='DELETE', data=data)

    def set_token(self, new_token:str):
        self._token = new_token


    def get_example_function(self) -> {}:
        return self._get(f"{self._base_url}/info/")


