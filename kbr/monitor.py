""" 
 
 
 
 Kim Brugger (09 Nov 2018), contact: kim@brugger.dk
"""

import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
import time
import datetime


import kbr.db_utils as db_utils

db = None

def connect(url:str) -> None:
    """ connects to a database instance 

    Args:
      url: as specified by sqlalchemy ( {driver}://{user}:{password}@{host}:{port}/{dbase}

    Returns:
      none

    Raises:
      RuntimeError on failure.


    """
    global db
    db = db_utils.DB( url )
    

def disconnect():
    """ disconnect a db connection if is open """

    if db is not None:
        db.close()
    

    
def _get_or_add_id(table:str, key:str, value:str):
    """ adds a standard stat/event entry to a table function, that will be wrapped by simpler functions below


    Args:
      table: table to add to
      context: the context the entry relates to, eg create, total_nodes etc

    returns:
      None

    Raises:
      None
    """

    return db.add_unique(table, {key: value}, key )

    
def _add_entry(table:str, origin:str, source:int, context:int, log:str):
    """ adds a standard stat/event entry to a table function, that will be wrapped by simpler functions below


    Args:
      table: table to add to
      context: the context the entry relates to, eg create, total_nodes etc
      target: ip, name, region
      value: what happened, nr or something else

    returns:
      None

    Raises:
      None
    """

    origin_id  = _get_or_add_id( "{}_origin".format(table), 'origin', origin);
    source_id  = _get_or_add_id( "{}_source".format(table), 'source', source);
    context_id = _get_or_add_id( "{}_context".format(table), 'context', context);

    db.add(table, {'origin_id': origin_id, 'source_id': source_id, 'context_id': context_id, 'log': log})
    

    

    
    
def add_stat(origin:str, source:str, context:int, log:str):
    """ adds a standard stat/event entry to a table function, that will be wrapped by simpler functions below


    Args:
      origin: where the log originates from, eg hostname or IP
      source: the source of the log, eg program or user
      context: The keyword for the log, eg all_idle 
      log: what happened, nr or something else

    returns:
      None

    Raises:
      None
    """

    _add_entry( 'stat', origin,  source, context, log )


def add_event(origin:str, source:str, context:int, log:str):
    """ adds a standard stat/event entry to a table function, that will be wrapped by simpler functions below


    Args:
      origin: where the log originates from, eg hostname or IP
      source: the source of the log, eg program or user
      context: The keyword for the log, eg all_idle 
      log: what happened, nr or something else

    returns:
      None

    Raises:
      None
    """

    _add_entry( 'event', origin,  source, context, log )

    

def stat_origins():
    return db.get_all( "stat_origin")

def stat_sources():
    return db.get_all( "stat_source")

def stat_contexts():
    return db.get_all( "stat_context")


def event_origins():
    return db.get_all( "event_origin")

def event_sources():
    return db.get_all( "event_source")

def event_contexts():
    return db.get_all( "event_context")


def _get_entries(table, start=None, end=None, limit=None, offset=None, order='ts'):
    """ get data from the stats tables

    Args:
      start: start time to extract from
      end: end time to extract from
      limit: nr of items to return
      offset: offset into the list of items to return
      order: default is timestamp

    return
      list of dicts of entries

    Raises:
      None
    """

    q  = "SELECT t.id, t.ts, o.origin, s.source, c.context, t.log "
    q += "FROM {table} t, {table}_origin o, {table}_source s, {table}_context c ".format( table=table)
    q += "WHERE t.origin_id = o.id AND t.source_id = s.id AND t.context_id = c.id  "

    if start is not None:
        q += " AND ts >= '{}' ".format(start)

    if end is not None:
        q += " AND ts <= '{}' ".format(end)

    
    if order is not None:
        q += " ORDER BY {} ".format( order )

    if limit is not None:
        q += " LIMIT {} ".format( limit )

    if offset is not None:
        q += " OFFSET {}".format( offset )

    return db.get( q )

def get_stats( start=None, end=None, limit=None, offset=None, order='ts'):
    """ get data from the stats tables

    Args:
      limit: nr of items to return
      offset: offset into the list of items to return
      order: default is timestamp

    return
      list of dicts of entries

    Raises:
      None
    """
    return _get_entries('stat', start, end, limit, offset, order)


def get_events( start=None, end=None, limit=None, offset=None, order='ts'):
    """ get data from the stats tables

    Args:
      limit: nr of items to return
      offset: offset into the list of items to return
      order: default is timestamp

    return
      list of dicts of entries

    Raises:
      None
    """
    return _get_entries('event', start, end,limit, offset, order)




def _make_timeserie(start:str, end:str, res:int=60):
    """Extract a timeserie from the database. The values are filtered by
       keys if provided. The timerange is divided into bins of res
       size. If multiple values occur for a key the mean value is
       returned.

    Args:
    start: datatime format start time
    end: datatime format start time
    res: size of bins in seconds

    Returns
      list of times

    Raises:
      None

    """

    start = int(start.timestamp())
    end   = int(end.timestamp())

    bins = []
    for i in range(start, end+res, res):
        if i > end:
            break
        
        i = int( i/res)*res
        
        bins.append( datetime.datetime.fromtimestamp( i ))

    return bins



    
def _get_timeserie_range(table:str, start:str, end:str, keys:list=[], res:int=60, method:str='mean') -> {}:
    """Extract a timeserie from the database. The values are filtered by
       keys if provided. The timerange is divided into bins of res
       size. If multiple values occur for a key the mean value is
       returned.

    Args:
    start: datatime format start time
    end: datatime format start time
    keys: if provided keys to filter on
    method: how to handle multipl occurences in a bin. Possibilites are: mean, median, sum

    Returns
      dict of times and observations seen in each one

    Raises:
      None

    """


    Q =  "SELECT s.ts, st.value AS target, sc.value AS context, s.value AS count "
    Q += "FROM {table} s, {table}_context sc, {table}_target st WHERE s.context_id = sc.id AND s.target_id=st.id ".format(table=table)
    Q += " AND ts >= '{}' AND ts <= '{}' ORDER BY ts;"


    Q = Q.format( start, end )

    db_data =  db.get( Q )

    keys_in_dataset = [] + keys

    data = {}
    for entry in db_data:
        key = "{}-{}".format( entry['target'], entry['context'])
        if ( keys != [] and key not in keys):
            continue

        if ( key not in keys_in_dataset ):
            keys_in_dataset.append( key )
        
        ts   = entry[ 'ts' ].timestamp()
        ts = int( ts/res)*res

        ts = datetime.datetime.fromtimestamp( ts )

        if ( ts not in data ):
            data[ ts ] = {}
            
        if key not in data[ ts ]:
            data[ ts ][ key ] = []

        data[ ts ][ key ].append( int(entry['count']))

    left_padding = True
        
#    for timestamp in data:
    for timestamp in _make_timeserie(start, end, res):

        if timestamp not in data:
            data[ timestamp] = {}

        
        for key in keys_in_dataset:
            if left_padding and key not in data[ timestamp ]:
                data[ timestamp][ key ] = 0
            elif key in data[ timestamp ]:
                left_padding = False
                 
                if method == 'sum':
                    data[ timestamp][ key ] = sum(data[ timestamp][ key ])
                elif method == 'mean':
                    data[ timestamp][ key ] = sum(data[ timestamp][ key ])/len(data[ timestamp][ key ])
                elif method == 'median':
                    data[ timestamp][ key ] = sorted( data[ timestamp][ key ])
                    data[ timestamp][ key ] = data[ timestamp][ key ][ int(len ( data[ timestamp][ key ])/2)]
        
    return data


def transform_timeserie_to_dict( timeserie:dict):

    trans = {'x': []}

    for timestamp in sorted(timeserie):
        trans[ 'x' ].append( str( timestamp))
        
        for key in timeserie[ timestamp ]:
            if key not in trans:
                trans[ key ] = []
            trans[ key ].append( timeserie[ timestamp ][key] )

    

    return trans


def timeserie_max_value( timeserie:dict ):

    max_value = 12
    
    for timestamp in sorted(timeserie):
        for key in timeserie[ timestamp ]:
            if max_value < timeserie[ timestamp ][ key ]:
                max_value = timeserie[ timestamp ][ key ]

    return max_value


def _get_timeserie_offset(table:str, seconds:int, keys:list=[], method:str='mean'):


    now = time.time()

    now -= 3600
    
    start = datetime.datetime.fromtimestamp( now - seconds)
    end   = datetime.datetime.fromtimestamp( now )

    return _get_timeserie_range(table, start = start, end=end, keys=keys, method=method, res=30)


def timeserie_5min(table:str, keys:list=[], method:str='mean'):

    return _get_timeserie_offset(table, 5*60, keys=keys, method=method)

def timeserie_10min(table:str, keys:list=[], method:str='mean'):

    return _get_timeserie_offset(table, 10*60, keys=keys, method=method)

def timeserie_15min(table:str, keys:list=[], method:str='mean'):

    return _get_timeserie_offset(table, 15*60, keys=keys, method=method)

def timeserie_30min(table:str, keys:list=[], method:str='mean'):

    return _get_timeserie_offset(table, 30*60, keys=keys, method=method)

def timeserie_1hour(table:str, keys:list=[], method:str='mean'):

    return _get_timeserie_offset(table, 1*60*60, keys=keys, method=method)

def timeserie_2hour(table:str, keys:list=[], method:str='mean'):

    return _get_timeserie_offset(table, 2*60*60, keys=keys, method=method)

def timeserie_5hour(table:str, keys:list=[], method:str='mean'):

    return _get_timeserie_offset(table, 5*60*60, keys=keys, method=method)

def timeserie_10hour(table:str, keys:list=[], method:str='mean'):

    return _get_timeserie_offset(table, 10*60*60, keys=keys, method=method)

def timeserie_1day(table:str, keys:list=[], method:str='mean'):

    return _get_timeserie_offset(table, 1*24*60*60, keys=keys, method=method)
