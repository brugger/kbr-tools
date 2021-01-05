import pytest

import kbr.datetime_utils as datetime_utils
import time
import datetime


def test_now_001():
    dt = datetime_utils.now()
    assert isinstance(dt, datetime.datetime)


def test_now_ts_001():
    dt = datetime_utils.now_ts()
    print(f"{dt} -- {type(dt)}")
    now = time.time()
    assert isinstance(dt, float) and now > dt


def test_string_to_datetime_001():
    now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)
    print("Now: ", now)
    # not optimal, but works for this
    valid = [now]
    valid.append(now.replace(tzinfo=None))
    valid.append(now.replace(hour=0, minute=0, second=0))
    valid.append(now.replace(hour=0, minute=0, second=0, tzinfo=None))
    for time_string in datetime_utils.time_strings:
        date = now.strftime(time_string)
        rev_date = datetime_utils.string_to_datetime(date)
        assert rev_date in valid


def test_string_to_datetime_002():
    with pytest.raises(RuntimeError):
        datetime_utils.string_to_datetime("Now a valid date string!")


def test_epoc_to_datetime_001():
    now = time.time()
    dt = datetime_utils.epoch_to_datetime(now)
    assert isinstance(dt, datetime.datetime)


def test_epoc_to_datetime_002():
    with pytest.raises(TypeError):
        datetime_utils.epoch_to_datetime("should fail")


def test_to_date_001():
    dt = datetime_utils.to_datetime(time.time())
    assert isinstance(dt, datetime.datetime)


def test_to_date_002():
    dt = datetime_utils.to_datetime(int(time.time()))
    assert isinstance(dt, datetime.datetime)


def test_to_date_003():
    dt = datetime_utils.to_datetime("2021-01-05T07:49:16")
    assert isinstance(dt, datetime.datetime)


def test_to_date_004():
    dt = datetime_utils.to_datetime(datetime.datetime.now())
    assert isinstance(dt, datetime.datetime)


def test_to_date_005():
    with pytest.raises(RuntimeError):
        datetime_utils.to_datetime(["Not valid"])


def test_to_string_001():
    date = datetime_utils.to_string(time.time())
    assert isinstance(date, str)


def test_to_string_002():
    date = datetime_utils.to_string(datetime.datetime.now())
    assert isinstance(date, str)


def test_to_string_003():
    date = datetime_utils.to_string(time.time(), "%Y-%m-%dT%H:%M:%S.%f")
    assert isinstance(date, str)


def test_to_string_004():
    date = datetime_utils.to_string(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%f")
    assert isinstance(date, str)


def test_to_epoc_001():
    date = datetime_utils.to_epoch(datetime.datetime.now())
    assert isinstance(date, float)


def test_to_epoc_002():
    date = datetime_utils.to_epoch("2021-01-05T07:49:16")
    assert isinstance(date, float)


def test_to_epoc_milli_001():
    ts = 1000000 * time.time()
    date = datetime_utils.to_epoch_milli(datetime.datetime.now())
    assert isinstance(date, float) and date >= ts


def test_to_epoc_nano_001():
    ts = 1000000000 * time.time()
    date = datetime_utils.to_epoch_nano(datetime.datetime.now())
    assert isinstance(date, float) and date >= ts


def test_weekday_001():
    day = datetime_utils.weekday("2021-01-06T07:49:16")
    assert day == 3


def test_weekday_002():
    day = datetime_utils.weekday("2021-01-06T07:49:16", zero_indexed=True)
    assert day == 2

def test_week_001():
    week = datetime_utils.week("2021-01-06T07:49:16")
    assert week == 1


def test_begin_of_day_001():
    dt = datetime_utils.begin_of_day("2021-01-06T07:49:16")
    dt_day = datetime_utils.to_datetime("2021-01-06T00:00:00")
    assert dt == dt_day

def test_begin_of_month_001():
    dt = datetime_utils.begin_of_month("2021-01-06T07:49:16")
    dt_month = datetime_utils.to_datetime("2021-01-01T00:00:00")
    assert dt == dt_month

def test_timedelta_001():
    dt = datetime_utils.to_timedelta( "1m")
    dt_check = datetime.timedelta(seconds=60)
    assert dt == dt_check

def test_timedelta_002():
    dt = datetime_utils.to_timedelta( "1d")
    dt_check = datetime.timedelta(seconds=60*60*24)
    assert dt == dt_check

def test_timedelta_002():
    td = datetime_utils.to_timedelta( "1d")
    dt = datetime_utils.to_datetime("2021-01-06T07:49:16") - td
    dt_check = datetime_utils.to_datetime("2021-01-05T07:49:16")
    assert dt   == dt_check

def test_timedelta_003():
    td = datetime_utils.to_timedelta( "1d")
    dt = datetime_utils.to_datetime("2021-01-06T07:49:16") + td
    dt_check = datetime_utils.to_datetime("2021-01-07T07:49:16")
    assert dt   == dt_check


########################################################

def test_timedelta_to_secs_000():
    unit = 1
    td = datetime_utils.timedelta_to_secs(None)
    assert td == 0
    td = datetime_utils.timedelta_to_secs("")
    assert td == 0


def test_timedelta_to_secs_001():
    unit = 1
    td = datetime_utils.timedelta_to_secs("1s")
    assert td == 1 * unit
    td = datetime_utils.timedelta_to_secs("100s")
    assert td == 100 * unit


def test_timedelta_to_secs_002():
    unit = 60
    td = datetime_utils.timedelta_to_secs("1m")
    assert td == 1 * unit
    td = datetime_utils.timedelta_to_secs("100m")
    assert td == 100 * unit


def test_timedelta_to_secs_003():
    unit = 60 * 60
    td = datetime_utils.timedelta_to_secs("1h")
    assert td == 1 * unit
    td = datetime_utils.timedelta_to_secs("100h")
    assert td == 100 * unit


def test_timedelta_to_secs_004():
    unit = 60 * 60 * 24
    td = datetime_utils.timedelta_to_secs("1d")
    assert td == 1 * unit
    td = datetime_utils.timedelta_to_secs("100d")
    assert td == 100 * unit


def test_timedelta_to_secs_005():
    unit = 60 * 60 * 24 * 7
    td = datetime_utils.timedelta_to_secs("1w")
    assert td == 1 * unit
    td = datetime_utils.timedelta_to_secs("100w")
    assert td == 100 * unit


def test_timedelta_to_secs_006():
    unit = 60 * 60 * 24 * 30
    td = datetime_utils.timedelta_to_secs("1M")
    assert td == 1 * unit
    td = datetime_utils.timedelta_to_secs("100M")
    assert td == 100 * unit


def test_timedelta_to_secs_007():
    unit = 60 * 60 * 24 * 30
    td = datetime_utils.timedelta_to_secs(" 1M")
    assert td == 1 * unit
    td = datetime_utils.timedelta_to_secs("100M  ")
    assert td == 100 * unit


def test_timedelta_to_secs_008():
    with pytest.raises(RuntimeError):
        td = datetime_utils.timedelta_to_secs("M")


def test_timedelta_to_secs_009():
    with pytest.raises(RuntimeError):
        td = datetime_utils.timedelta_to_secs("0s")


def test_timedelta_to_secs_010():
    with pytest.raises(RuntimeError):
        td = datetime_utils.timedelta_to_secs("1Y")


def test_timedelta_to_secs_011():
    with pytest.raises(RuntimeError):
        td = datetime_utils.timedelta_to_secs("-10m")

def test_timedeltas_to_secs_001():
    td = datetime_utils.timedeltas_to_secs("1s")
    assert td == 1

def test_timedeltas_to_secs_002():
    td = datetime_utils.timedeltas_to_secs("1s 1m")
    assert td == 61

def test_timedeltas_to_secs_003():
    td = datetime_utils.timedeltas_to_secs("1s  1m  ")
    assert td == 61

def test_timedeltas_to_secs_004():
    td = datetime_utils.timedeltas_to_secs(["1s"])
    assert td == 1

def test_timedeltas_to_secs_005():
    td = datetime_utils.timedeltas_to_secs(["1s", "2m"])
    assert td == 121

def test_Timerange_001():

    st = datetime_utils.to_datetime("2021-01-01T00:00:00")
    nd = datetime_utils.to_datetime("2021-01-10T00:00:00")

    intervals = list(datetime_utils.Timerange(st, nd, "1d"))
    assert len(intervals) == 10 and intervals[0] == st and intervals[-1] == nd


