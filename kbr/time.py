#!/usr/bin/python3
""" 
 
Various functions related to date, time,  and timestamps 
 
 Kim Brugger (07 Jan 2019), contact: kim@brugger.dk
"""

import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

import time
import datetime



def now():
    """ retuns current time w/ microseconds """

    return  datetime.now()

def to_string(ts):
    """ Convert a time to string, if an int will transform it to a timestamp before returning the string"""

    if isinstance(ts, int):
        return ts
    elif isinstance(ts, datetime.datetime):
        return str(ts.timestamp())
    else:
        return str(datetime.datetime.fromtimestamp( ts ))

    raise ValueError("Cannot convert {} to a string".format( ts))



def to_int( ts ):

        
    if isinstance(ts, int):
        return ts
    elif isinstance( ts, datetime.datetime ):
        return  int( ts.timestamp() )
    elif isinstance( ts, str):
        return int( entry[ 'ts' ] )
    else:
        raise ValueError("Cannot convert {} to an int".format( ts))

