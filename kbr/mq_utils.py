#!/usr/bin/env python3
""" 
 
 Kim Brugger (03 Apr 2019), contact: kim@brugger.dk
"""

import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

import pika


class Mq(object):


    def __init__(self):
        self.connection = None
        self.channel    = None
        self.exchange   = None
        self.channels   = []

    def connect(self,  uri:str, exchange:str='default', exchange_type:str='direct'):
        self.connection = pika.BlockingConnection( pika.connection.URLParameters(uri) )
        self.channel    = self.connection.channel()
        self.exchange   = exchange
    
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=exchange_type, durable=True)


    def disconnect(self):
        self.close()


    def _check_channel(self, name:str):
        if name not in self.channels:
            
            result = self.channel.queue_declare(queue=name, durable=True)
            
            self.channel.queue_bind(exchange=self.exchange,
                                    queue=name,
                                    routing_key=name)
        
            self.channels.append( name )
            
    def publish(self, body:str, route:str='default'):

        self._check_channel( route)
        self.channel.basic_publish( exchange=self.exchange, routing_key=route, body=body, properties=pika.BasicProperties( delivery_mode=2))
        
    def consume(self, route:str, callback):
        try:
            self._check_channel( route)
            self.channel.basic_consume(queue=route, on_message_callback=callback)
            self.channel.start_consuming()
        except Exception as e:
            print( e )


    def queue_length(self, queue:str=None):
        result = self.channel.queue_declare(queue=queue, durable=True, passive=True)
        return result.method.message_count
    
