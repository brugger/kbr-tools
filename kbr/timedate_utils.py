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
import re


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
        return str(datetime.datetime.fromtimestamp(ts))

    raise ValueError("Cannot convert {} to a string".format(ts))


def to_sec_since_epoch(ts):
    if isinstance(ts, int) or isinstance(ts, float):
        return int(ts)
    elif isinstance(ts, datetime.datetime):
        return int(ts.timestamp())
    elif isinstance(ts, str):
        return datetime.time.fromisoformat(ts)
    else:
        raise ValueError("Cannot convert {} to an int".format(ts))


def to_days_since_epoch(ts: int) -> int:
    timestamp = datetime.datetime.fromtimestamp(ts)
    stime = "{}-{}-{} 00:00:00".format(timestamp.year, timestamp.month, timestamp.day)

    return datetime.datetime.strptime(stime, "%Y-%m-%d %H:%M:%S").timestamp()


def to_months_since_epoch(ts: int) -> int:
    timestamp = datetime.datetime.fromtimestamp(ts)
    stime = "{}-{}-{} 00:00:00".format(timestamp.year, timestamp.month, timestamp.day)

    return datetime.datetime.strptime(stime, "%Y-%m-%d %H:%M:%S").timestamp()


def datestr_to_ts(datetime_str: str) -> any:
    for time_string in ["%Y-%m-%dT%H:%M:%S.%f%z",
                        "%Y-%m-%dT%H:%M:%S.%f",
                        "%Y-%m-%dT%H:%M:%S%z",
                        "%Y-%m-%dT%H:%M:%S",
                        "%Y-%m-%d %H:%M:%S.%f%z",
                        "%Y-%m-%d %H:%M:%S.%f",
                        "%Y-%m-%d %H:%M:%S%z",
                        "%Y-%m-%d %H:%M:%S",
                        "%a %Y-%m-%d%d %H:%M:%S %Z",
                        "%a %Y-%m-%d%d %H:%M:%S"]:
        try:
            ts = datetime.datetime.strptime(datetime_str, time_string)
            return ts
        except:
            pass

    raise RuntimeError(f"cannot convert datetime string '{datetime}' to timestamp ")


def epoch_to_timestr(time: int):
    ts = datetime.datetime.fromtimestamp(time)
    return ts


def weekday(timestamp: str) -> []:
    try:
        ts = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f%z")
    except:
        try:
            ts = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S%z")
        except:
            print(f"Cannot convert timestamp {timestamp} to weekday")

    return ts.weekday(), ts.hour, ts.minute


def timedelta_to_epoc(timerange) -> int:
    ''' 3h, 2d, 1w --> now - delta as epoc secs '''

    if timerange == '' or timerange is None:
        return 0

    time_delta = 0
    try:
        g = re.match(r'(\d+)([hdw])', timerange)
        num, range = g.groups(0)
        ts = time.time()
        if range == 'h':
            time_delta = ts - 3600 * int(num)
        elif range == 'd':
            time_delta = ts - 24 * 3600 * int(num)
        elif range == 'w':
            time_delta = ts - 24 * 3600 * 7 * int(num)
    except Exception as e:
        print(f"timerange {timerange} is invalid valid examples: 1d 2h 1w ")
        sys.exit(1)

    return time_delta


# def time_delta(ts:int)
#    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)


def timedelta_to_sec(timerange) -> int:
    ''' 1m, 3h, 2d, 1w --> now - delta as epoc secs '''

    if timerange == '' or timerange is None:
        return 0

    time_delta = 0
    try:
        g = re.match(r'(\d+)([mhdwM])', timerange)
        num, range = g.groups(0)
        if range == 'm':
            time_delta = 60 * int(num)
        if range == 'h':
            time_delta = 3600 * int(num)
        elif range == 'd':
            time_delta = 24 * 3600 * int(num)
        elif range == 'w':
            time_delta = 24 * 3600 * 7 * int(num)
        elif range == 'M':
            time_delta = 30 * 24 * 3600 * 7 * int(num)
    except Exception as e:
        print(f"timerange {timerange} is invalid valid examples: 1d 2h 1w 1M")
        sys.exit(1)

    return time_delta


def date_range(start: str, end: str, timeframe: str) -> []:
    start = datestr_to_ts(start)
    end = datestr_to_ts(end)
    timeframe = timedelta_to_sec(timeframe)

    res = [start]
    while True:
        start = start + datetime.timedelta(seconds=timeframe)
        print(start)
        if start >= end:
            break
        res.append(start)

    return res
