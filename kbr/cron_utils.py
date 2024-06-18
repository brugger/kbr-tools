#! env python 
import sys
import datetime
import re


import pprint as pp

from datetime import timedelta

from dateutil.relativedelta import relativedelta

# Uses the cron time format, but with fields sep. with :
# sec:min:hour:day_of_month:month:weekday
# minute: 0-59
# hour:	0-23
# day of month:1-31
# month: 1-12, where 1 is January, 2 is February, and so on.
# Uppercase, lowercase and mixed-case three character strings, based on the English name of the month. For example: jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, or dec.
# day of week: 0-7, where 0 is Monday, 1 is Tuesday, and so on.
# Uppercase, and lowercase or mixed-case three character strings, based on the English name of the day: mon, tue, wed, thu, fri, sat, or sun.
# https://www.ibm.com/docs/en/db2oc?topic=task-unix-cron-format

def to_range(value:str, step:int=1):
    if "-" in value:
        st, nd = map(int, value.split("-"))
        return list(range(st, nd+1, step))

    try:
#        print( " ---->", int(value))
        return [int(value)]
    except:
        print('value in wrong format, see documentation')
        sys.exit(1)


#print(to_range("2"))
#print(to_range("2-6"))
#print(to_range("2-6", 2))
#print(to_range("2nd"))

def to_list(value, min:int, max:int):
    if value == "*":
        return []
    
    if isinstance(value, int):
        return [value]
    
#    print("Value:", value)

    value = value.lower()
    value = re.sub(r'mon', r'0', value)
    value = re.sub(r'tue', r'1', value)
    value = re.sub(r'wed', r'2', value)
    value = re.sub(r'thu', r'3', value)
    value = re.sub(r'fri', r'4', value)
    value = re.sub(r'sat', r'5', value)
    value = re.sub(r'sun', r'6', value)

    value = re.sub(r'jan', r'1',  value)
    value = re.sub(r'feb', r'2',  value)
    value = re.sub(r'mar', r'3',  value)
    value = re.sub(r'apr', r'4',  value)
    value = re.sub(r'may', r'5',  value)
    value = re.sub(r'jun', r'6',  value)
    value = re.sub(r'jul', r'7',  value)
    value = re.sub(r'aug', r'8',  value)
    value = re.sub(r'sep', r'9',  value)
    value = re.sub(r'oct', r'10', value)
    value = re.sub(r'nov', r'11', value)
    value = re.sub(r'dec', r'12', value)


 #   print("VALUE:", value)

    if m:=re.match(r'(\d+-\d+)/(\d+)', value):
        return to_range(m.group(1), int(m.group(2)))

    elif m:=re.match(r'\*/(\d+)', value):
        return list(range(min, max+1, int(m.group(1))))

    res = []
    for v in value.split(","):
        res += to_range(v)

    return res



def make_weekdays_old(dt, weekday):
    """
    Generate a list of 5 dates starting from the given date that fall on the specified weekday.

    Parameters:
        dt (datetime.datetime): The starting date.
        weekday (int): The weekday to search for. 0 represents Monday, 1 represents Tuesday, and so on.

    Returns:
        list: A list of datetime objects representing the dates that fall on the specified weekday.
    """
    tmp_dts = []
    dt  = dt.replace(day=1)
    days_added = 0
    while True:
        days_ahead = weekday - dt.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        tmp_dts.append( dt + datetime.timedelta(days=days_ahead) )
        dt = tmp_dts[-1]

        if len(tmp_dts) > 5:
            break
            
    return tmp_dts



def make_weekdays(dt, weekday):
    """
    Generate a list of dates starting from the given date that fall on the specified weekday.

    Parameters:
        dt (datetime.datetime): The starting date.
        weekday (int): The weekday to search for. 0 represents Monday, 1 represents Tuesday, and so on.

    Returns:
        list: A list of datetime objects representing the dates that fall on the specified weekday.
    """
    tmp_dts = []
    days_ahead = weekday - dt.weekday()
    if days_ahead < 0: # Target day already happened this week, skip it
        pass

    elif days_ahead == 0: # Target day is the dt, add it!
        tmp_dts.append( dt )
    days_ahead += 7

    tmp_dts.append( dt + datetime.timedelta(days=days_ahead))

    return tmp_dts



def make_dts(dts, offsets, dt_type):
    now = datetime.datetime.now()

    tmp_dts = []
    for dt in dts:
        for offset in offsets :
            #print("O", dt_type, offset, offsets, type(offsets))
            if dt_type == 'minute':
                tmp_dts.append(dt.replace(minute=offset))
            elif dt_type == 'hour':
                tmp_dts.append(dt.replace(hour=offset))
            elif dt_type == 'day':
                try:
                    tmp_dts.append(dt.replace(day=offset))
                except:
                    pass
            elif dt_type == 'month':
                tmp_dts.append(dt.replace(month=offset))
            elif dt_type == 'weekday':
#                tmp_dt = dt.replace(day=1)
#                days_ahead = offset - now.weekday()
#                if days_ahead <= 0: # Target day already happened this week
#                    days_ahead += 7
#                tmp_dts.append(dt+ datetime.timedelta(days=days_ahead))
                tmp_dts += make_weekdays( dt, offset)
            elif dt_type == 'year':
                tmp_dts.append(dt.replace(year=offset))

    dts = tmp_dts.copy()

    for dt in sorted(set(dts)):
        if dt > now:
            tmp_dts.append(dt)


    return tmp_dts



def next_time(minute:str="*", hour:str="*", day:str="*", month:str="*", weekday:str="*", dt:datetime.datetime=None) -> datetime.datetime:

    now = datetime.datetime.now()
    now = now.replace(microsecond = 0, second = 0)

    # mainly for testing
    if dt is not None:
        now = dt

    mins     = to_list(minute,  0, 59)
    hours    = to_list(hour,    0, 23)
    days     = to_list(day,     1, 31)
    months   = to_list(month,   1, 12)
    weekdays = to_list(weekday, 0, 6)


    dts = [now]

    if not mins:
        mins.append( 0 )
        mins.append( (now + timedelta(seconds=60)).minute)

    if not hours:
        hours.append( 0 )
        hours.append( now.hour)
        hours.append( now.hour)
        hours.append( (now + timedelta(hours=1)).hour)

    if not days and not weekdays:
        days.append( now.day)
        days.append( (now + timedelta(days=1)).day)

    if not months:
        months.append( now.month)
        months.append( (now + relativedelta(months=1)).month)

    years = [now.year, now.year+1]


#    print( f"m: {mins} h: {hours}, d: {days}, m: {months}, w: {weekdays}, y: {years}")

    dts = make_dts(dts, mins,   "minute")
    dts = make_dts(dts, hours,  "hour")
    dts = make_dts(dts, months, "month")

    dts_days = make_dts(dts, days,   "day")# + 
    dts_weekdays = make_dts(dts, weekdays,   "weekday")

    if len(dts) == 1:
        dts = make_dts(dts, years,  "year")


    dts = dts_days + dts_weekdays

#    dts = make_dts(dts, weekdays, "weekday")

    tmp_dts = []

    for dt in sorted(set(dts)):
        if dt > now:
            tmp_dts.append(dt)

    dts = tmp_dts
#    print( now )
#    pp.pprint( dts )
#    print( min( dts ))


    return min( dts ) #next_time


def next_cron(cron:str):
    return next_time(*cron.split(":"))


#next_pull = next_time(minute='5', hour='*', day='15-19/2', month=11,weekday='mon,fri')
#next_pull = next_time(minute='0,15,30,45', hour='*',  weekday='mon,wed,fri')
#print( "NextPull at:", next_pull)



