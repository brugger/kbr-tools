import os
import json

import tornado

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from tornado.web import RequestHandler, HTTPError

from uuid import UUID
import datetime



import pprint as pp
import requests


# bespoke decoder to handle UUID and timestamps
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)



class BaseHandler( RequestHandler ):

    def remote_ip(self):
        x_real_ip = self.request.headers.get("X-Real-IP")
        remote_ip = x_real_ip or self.request.remote_ip

        return remote_ip


    def acl_check(self, acls:[], url:str, access:str):

        pp.pprint( acls )

        for acl in acls:
            if acl['endpoint'] == url:
                if access in acl and acl[ access ]:
                    return True

        self.send_response_401( data="user not authorised to {} resource '{}'".format( access, url ) )


    
    def prepare(self):
        ''' change the strings from bytestring to utf8 '''
        
        self.form_data = {
            key: [val.decode('utf8') for val in val_list]
            for key, val_list in self.request.arguments.items()
        }


    def _arguments(self):

        values = {}
        for argument in self.request.arguments:
            values[ argument ] = self.get_argument( argument )

        return values
        

    def _check_arguments(self, values:dict, valid:list) -> bool:

        for key in values.keys():
            if key not in valid:
                return False

        return True

    def _valid_arguments(self, values:dict, valid:list) -> bool:

        valid_values = {}

        for key in values:
            if key in valid:
                valid_values[ key ] = values[ key ]

        return valid_values


    
    def access_token(self):
        token = None
        auth_header = self.request.headers.get('Authorization', None)
        print("Auth header: {}".format( auth_header ))
        if auth_header:
           token = auth_header[7:]

        if token is None:
            self.send_response_401( )

        return token

    
    def set_ACAO_header(self, sites="*"):
#        print( "setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", sites)
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


    def set_json_header(self):
         """Set the default response header to be JSON."""
         self.set_header("Content-Type", 'application/json; charset="utf-8"')

    # Success
    def send_response(self, data=None, status=200):
        """Construct and send a JSON response with appropriate status code."""

        self.set_status(status)
        # check if the data is already in valid json format, otherwise make it
        try:
            json_object = json.loads( data )
        except TypeError:
            data = json.dumps(data, cls=UUIDEncoder)

        self.finish( data  )


    def send_status_code(self, status:int):
        """Construct and send an empty response with appropriate status code."""

        self.set_status(status)
        return self.finish( )
    
    # Created
    def send_response_201(self):
        return self.send_response( data=None, status=201)

    # Accecpted
    def send_response_202(self, data):
        return self.send_status_code( status=202)

    # No content
    def send_response_204(self):
        return self.send_status_code( status=204)


    def raise_error(self, status:int, reason:any=None):
        if reason is not None:
            reason = json.dumps(reason)
            raise HTTPError( status, reason=reason)
        else:
            raise HTTPError( status )

    # bad request
    def send_response_400(self, data:any=None):
#        pp.pprint( data )
        self.raise_error(status=400, reason=data)

    # Unauthorized
    def send_response_401(self, data:any=None):
        self.raise_error(status=401, reason=data)

    # Forbidden
    def send_response_403(self, data:any=None):
        self.raise_error(status=403, reason=data)
#        return self.send_response( data=data, status=403)

    # Not fund
    def send_response_404(self):
        self.raise_error(status=404)
#        return self.send_response(status=404)

    # Internal Server Error
    def send_response_500(self, data:any=None):
        self.raise_error(status=500, reason=data)
#        return self.send_response( data=data, status=500)

    # Not Implemented
    def send_response_501(self, data:any=None):
        self.raise_error(status=501, reason=data)
#        return self.send_response( data=data, status=501)

    # Service Unavailable
    def send_response_503(self, data:any=None):
        self.raise_error(status=503, reason=data)
#        return self.send_response( data=data, status=503)

        

def json_decode(value):

    return tornado.escape.json_decode( value )

def url_unescape(uri:str) -> str:
    if uri is None:
        return uri
    
    return tornado.escape.url_unescape( uri )
    
def run_app(urls, port=8888, **kwargs):

    app = Application(urls, **kwargs)
    app.listen(port)
    IOLoop.current().start()
    
        
