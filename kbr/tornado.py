import os
import json

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from tornado.web import RequestHandler

import pprint as pp




class BaseHandler( RequestHandler ):

    def prepare(self):
        ''' change the strings from bytestring to utf8 '''
        
        self.form_data = {
            key: [val.decode('utf8') for val in val_list]
            for key, val_list in self.request.arguments.items()
        }

    
    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    # Success
    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))
        raise gen.Return()

    # Created
    def send_response_201(self, data):
        return self.send_response( self, data, status=201)

    # Accecpted
    def send_response_202(self, data):
        return self.send_response( self, data, status=202)

    # No content
    def send_response_204(self, data):
        return self.send_response( self, data, status=204)

    # bad request
    def send_response_400(self, data):
        return self.send_response( self, data, status=400)

    # Unauthorized
    def send_response_401(self, data):
        return self.send_response( self, data, status=401)

    # Forbidden
    def send_response_403(self, data):
        return self.send_response( self, data, status=403)

    # Not fund
    def send_response_404(self, data):
        return self.send_response( self, data, status=404)

    # Internal Server Error
    def send_response_500(self, data):
        return self.send_response( self, data, status=500)

    # Not Implemented
    def send_response_501(self, data):
        return self.send_response( self, data, status=501)

    # Service Unavailable
    def send_response_503(self, data):
        return self.send_response( self, data, status=503)

        

def run_app(urls, port=8888, debug=False):

    app = Application(urls, debug=debug) 
    app.listen(port)
    IOLoop.current().start()
    
        
