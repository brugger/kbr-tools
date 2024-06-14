import datetime
import pytest

import kbr.cron_utils as cron_utils


def test_to_range1():

    assert cron_utils.to_range("2") == [2]
    assert cron_utils.to_range("2-6") == [2, 3, 4, 5, 6]
    assert cron_utils.to_range("2-6", 2) == [2, 4, 6]
    assert cron_utils.to_range("6-2", 2) == []



def test_to_list1():
    assert cron_utils.to_list("mon-Sun", 0, 6) == [0, 1, 2, 3, 4, 5, 6]    
    assert cron_utils.to_list("Sun-Fri", 0, 6) == []
    assert cron_utils.to_list("2-6/2", 1, 12) == [2,4,6]
    assert cron_utils.to_list("*/2", 0, 23) == [0,2,4,6,8,10,12,14,16,18,20,22]
    assert cron_utils.to_list("*/3", 1, 12) == [1,4,7,10]
    assert cron_utils.to_list("1-4", 1, 12) == [1,2,3,4]
    assert cron_utils.to_list("1-2,4-6", 1, 12) == [1,2,4,5,6]
    assert cron_utils.to_list("Jan-mar", 0, 12) == [1,2,3]

def test_make_weekday():

    # A Friday at the end of feburary
    dt = datetime.datetime.strptime("2020-02-28", "%Y-%m-%d")
    print("DT", dt)
    assert cron_utils.make_weekdays(dt, 0) ==  [datetime.datetime(2020, 3, 2, 0, 0)]
    assert cron_utils.make_weekdays(dt, 3) ==  [datetime.datetime(2020, 3, 5, 0, 0)]
    assert cron_utils.make_weekdays(dt, 4) ==  [datetime.datetime(2020, 2, 28, 0, 0),datetime.datetime(2020, 3, 6, 0, 0)]
def test_next_time():

    dt = datetime.datetime.strptime("28/02/2020 16:31", "%d/%m/%Y %H:%M")

    assert cron_utils.next_time("*/2", dt=dt) ==  datetime.datetime(2020, 2, 28, 16, 32)
    assert cron_utils.next_time(minute="*/2", weekday="Mon", dt=dt) ==  datetime.datetime(2020, 3, 2, 0, 0)
    assert cron_utils.next_time(minute="*/2", hour="12", weekday="Fri", dt=dt) ==  datetime.datetime(2020, 3, 6, 12, 0)


