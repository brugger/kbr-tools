#!/usr/bin/python3
""" 
 
Various functions related to date, time,  and timestamps 
 
 Kim Brugger (07 Jan 2019), contact: kim@brugger.dk
"""

import time
import datetime
import re
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)


time_strings = ["%Y-%m-%dT%H:%M:%S.%f%z",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S.%fZ" # cromwell
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f%z",
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%d %H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S",
                "%a %Y-%m-%d %H:%M:%S %Z",
                "%a %Y-%m-%d %H:%M:%S",
                
                "%Y-%m-%d %Z",
                "%Y-%m-%d",
                ]


def now(tz: str = None) -> datetime.datetime:
    """ retuns current time as seconds inc microseconds """

    return datetime.datetime.now(tz)


def now_ts() -> float:
    return time.time()


def string_to_datetime(datetime_str: str) -> datetime:
    for time_string in time_strings:
        try:
            dt = datetime.datetime.strptime(datetime_str, time_string)
            return dt
        except Exception as e:
            #  print(e)
            pass

    raise RuntimeError(f"cannot convert datetime string '{datetime_str}' to timestamp ")


def epoch_to_datetime(timestamp: any) -> datetime:
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt


def to_datetime(value: any) -> datetime:
    if isinstance(value, datetime.datetime):
        return value
    elif isinstance(value, str):
        return string_to_datetime(value)
    elif isinstance(value, int) or isinstance(value, float):
        return epoch_to_datetime(value)
    else:
        raise RuntimeError("Cannot convert type {} to datetime".format(type(value)))


def to_string(value, format: str = None) -> str:
    """ Convert a time to string, if an int will transform it to a timestamp before returning the string"""

    dt = to_datetime(value)
    if format is None:
        return dt.isoformat()

    return dt.strftime(format)


def to_epoch(value, milli: bool = False, nano: bool = False) -> float:
    dt = to_datetime(value)
    ts = float(dt.timestamp())
    if milli:
        ts *= 1000000
    elif nano:
        ts *= 1000000000

    return ts


def to_epoch_milli(dt):
    return to_epoch(dt, milli=True)


def to_epoch_nano(dt, nano=True):
    return to_epoch(dt, nano=True)




def weekday(value: any, zero_indexed:bool=False) -> str:
    dt = to_datetime(value)
    if zero_indexed:
        return dt.weekday()

    return dt.isoweekday()


def week(value: any) -> str:
    dt = to_datetime(value)
    _, week, _ = dt.isocalendar()
    return week

def timedelta_to_secs(timerange:str) -> int:
    ''' 1m, 3h, 2d, 1w -->  secs '''

    if timerange == '' or timerange is None:
        return 0

    timerange = timerange.replace(" ", "")

    time_delta = 0
    try:
        g = re.match(r'^(\d+)([smhdwM])\Z', timerange)
        num, range = g.groups(0)
        num = int(num)

        if num <= 0:
            raise RuntimeError("delta < 1 does not make sense!")

        if range == 's':
            time_delta = num
        elif range == 'm':
            time_delta = 60 * num
        elif range == 'h':
            time_delta = 3600 * num
        elif range == 'd':
            time_delta = 24 * 3600 * num
        elif range == 'w':
            time_delta = 24 * 3600 * 7 * num
        elif range == 'M':
            time_delta = 30 * 24 * 3600 * num
    except Exception as e:
        raise RuntimeError(f"timerange '{timerange}' is invalid valid examples: 1d 2h 1w 1M")

    return time_delta

def timedeltas_to_secs(values:any) -> int:
    if isinstance(values, str):
        values = values.split(" ")
    total_secs = 0
    for value in values:
        total_secs += timedelta_to_secs(value)

    return  total_secs

def to_timedelta(timerange:str) -> datetime.timedelta:

    return datetime.timedelta(seconds=timedelta_to_secs(timerange))


def begin_of_day(value: any) -> datetime.datetime:
    dt = to_datetime(value)
    return dt.replace(hour=0, minute=0, second=0)


def begin_of_month(value: any) -> datetime.datetime:
    dt = to_datetime(value)
    return dt.replace(day=1, hour=0, minute=0, second=0)




class Timerange:

    """Iterator that increments in intervals between start and end"""

    def __init__(self, start:str, end:str, interval:str):
        self._start     = to_datetime(start)
        self._end       = to_datetime(end)
        self._timeframe = timedelta_to_secs( interval )

    def __iter__(self):
        return self

    def __next__(self) -> datetime.datetime:
        ts = self._start
        self._start = self._start + datetime.timedelta(seconds = self._timeframe)
        if ts > self._end:
            raise StopIteration  # signals "the end"
        return ts



