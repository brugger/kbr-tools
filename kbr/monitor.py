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
    

def _get_or_add_id(table:str, value:str):
    """ adds a standard stat/event entry to a table function, that will be wrapped by simpler functions below


    Args:
      table: table to add to
      context: the context the entry relates to, eg create, total_nodes etc

    returns:
      None

    Raises:
      None
    """

    return db.add_unique(table, {'value': value}, 'value' )

    
def _add_entry(table:str, context:int, target:int, value:str):
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

    context_id = _get_or_add_id( "{}_context".format(table), context);
    target_id  = _get_or_add_id( "{}_target".format(table), target);

    db.add(table, {'context_id': context_id, 'target_id': target_id, 'value': value})
    

    

    
    
def add_stat(context:int, target:int, value:str):
    """ adds a standard stat/event entry to a table function, that will be wrapped by simpler functions below


    Args:
      table: table to add to
      context:  
      target:
      value: what happened, nr or something else

    returns:
      None

    Raises:
      None
    """

    _add_entry( 'stat', context, target, value )


def add_event(context:int, target:int, value:str):
    """ adds a standard stat/event entry to a table function, that will be wrapped by simpler functions below


    Args:
      table: table to add to
      context_id:  
      target_id:
      value: what happened, nr or something else

    returns:
      None

    Raises:
      None
    """

    _add_entry( 'event', context, target, value )



    

    

    
    

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

    
    
    
def _get_timeserie_range(start:str, end:str, keys:list=[], res:int=60, method:str='mean') -> {}:
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


    Q =  "select s.ts, st.value as target, sc.value as context, s.value as count "
    Q += "from stat s, stat_context sc, stat_target st where s.context_id = sc.id and s.target_id=st.id "
    Q += " and ts >= '{}' and ts <= '{}' order by ts;"


    Q = Q.format( start, end )

    db_data =  db.query( Q ).as_dict()

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


def _get_timeserie_offset(seconds:int, keys:list=[], method:str='mean'):


    now = time.time()
    
    start = datetime.datetime.fromtimestamp( now - seconds)
    end   = datetime.datetime.fromtimestamp( now )

    return _get_timeserie_range(start = start, end=end, keys=keys, method=method, res=30)


def timeserie_5min(keys:list=[], method:str='mean'):

    return _get_timeserie_offset(5*60, keys=keys, method=method)

def timeserie_10min(keys:list=[], method:str='mean'):

    return _get_timeserie_offset(10*60, keys=keys, method=method)

def timeserie_15min(keys:list=[], method:str='mean'):

    return _get_timeserie_offset(15*60, keys=keys, method=method)

def timeserie_30min(keys:list=[], method:str='mean'):

    return _get_timeserie_offset(30*60, keys=keys, method=method)

def timeserie_1hour(keys:list=[], method:str='mean'):

    return _get_timeserie_offset(1*60*60, keys=keys, method=method)

def timeserie_2hour(keys:list=[], method:str='mean'):

    return _get_timeserie_offset(2*60*60, keys=keys, method=method)

def timeserie_5hour(keys:list=[], method:str='mean'):

    return _get_timeserie_offset(5*60*60, keys=keys, method=method)

def timeserie_10hour(keys:list=[], method:str='mean'):

    return _get_timeserie_offset(10*60*60, keys=keys, method=method)

def timeserie_1day(keys:list=[], method:str='mean'):

    return _get_timeserie_offset(1*24*60*60, keys=keys, method=method)
