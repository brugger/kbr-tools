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



def now() -> float:
    """ retuns current time as seconds inc microseconds """

    return time.time()

def to_string(ts):
    """ Convert a time to string, if an int will transform it to a timestamp before returning the string"""

    if isinstance(ts, str):
        return ts
    elif isinstance(ts, datetime.datetime):
        return str(ts.timestamp())
    else:
        return str(datetime.datetime.fromtimestamp( ts ))

    raise ValueError("Cannot convert {} to a string".format( ts))



def to_sec_since_epoch( ts ):

    if isinstance(ts, int) or isinstance(ts, float):
        return int(ts)
    elif isinstance( ts, datetime.datetime ):
        return  int( ts.timestamp() )
    elif isinstance( ts, str):
        return datetime.time.fromisoformat( ts )
    else:
        raise ValueError("Cannot convert {} to an int".format( ts))

def to_days_since_epoch(ts:int) -> int:
    timestamp = datetime.datetime.fromtimestamp(ts)
    stime = "{}-{}-{} 00:00:00".format( timestamp.year, timestamp.month, timestamp.day )

    return datetime.datetime.strptime(stime, "%Y-%m-%d %H:%M:%S").timestamp()

def to_months_since_epoch(ts:int) -> int:
    timestamp = datetime.datetime.fromtimestamp(ts)
    stime = "{}-{}-{} 00:00:00".format( timestamp.year, timestamp.month, timestamp.day )

    return datetime.datetime.strptime(stime, "%Y-%m-%d %H:%M:%S").timestamp()


def datestr_to_ts(datetime_str:str) -> any:

    for time_string in ["%Y-%m-%dT%H:%M:%S.%f%z",
                        "%Y-%m-%dT%H:%M:%S.%f",
                        "%Y-%m-%dT%H:%M:%S%z",
                        "%Y-%m-%dT%H:%M:%S",
                        "%Y-%m-%d %H:%M:%S.%f%z",
                        "%Y-%m-%d %H:%M:%S.%f",
                        "%Y-%m-%d %H:%M:%S%z",
                        "%Y-%m-%d %H:%M:%S"]:
        try:
            ts = datetime.datetime.strptime(datetime_str, time_string)
            return ts
        except:
            pass


    raise RuntimeError(f"cannot convert datetime string '{datetime}' to timestamp ")



def epoch_to_timestr(time:int):
    ts = datetime.datetime.fromtimestamp(time)
    return ts


def weekday(timestamp:str) -> []:

    try:
        ts = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f%z")
    except:
        try:
            ts = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S%z")
        except:
            print(f"Cannot convert timestamp {timestamp} to weekday")

    return ts.weekday(), ts.hour, ts.minute


#def time_delta(ts:int)
#    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)