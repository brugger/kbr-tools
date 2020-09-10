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
    """ retuns current time as seconds inc microseconds """

    return time.time()
    
    return  datetime.datetime.now()

def to_string(ts):
    """ Convert a time to string, if an int will transform it to a timestamp before returning the string"""

    if isinstance(ts, str):
        return ts
    elif isinstance(ts, datetime.datetime):
        return str(ts.timestamp())
    else:
        return str(datetime.datetime.fromtimestamp( ts ))

    raise ValueError("Cannot convert {} to a string".format( ts))



def to_sec( ts ):

        
    if isinstance(ts, int) or isinstance(ts, float):
        return int(ts)
    elif isinstance( ts, datetime.datetime ):
        return  int( ts.timestamp() )
    elif isinstance( ts, str):
        return datetime.time.fromisoformat( ts )
#        return str(datetime.datetime.fromisoformat( ts ))
#        return int( ts )
    else:
        raise ValueError("Cannot convert {} to an int".format( ts))

