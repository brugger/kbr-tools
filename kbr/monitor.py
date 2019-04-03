""" 
 
 
 
 Kim Brugger (09 Nov 2018), contact: kim@brugger.dk
"""

import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
import time
import datetime
import re

import kbr.db_utils as db_utils
import kbr.misc as misc
import kbr.time

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
    

    
def _check_type( entry_type:str ) -> bool:
    """ check if a type is in the allowed types of either: ['float', 'int', 'json', 'str']

    the user can submit shorted ( first letter ) version of these types

    Args:
      entry_type, name to check
    
    Returns:
      bool

    Raises:
      RuntimeError on illegal value
    """
    
    allowed_types = ['float', 'int', 'json', 'str']

    
    if entry_type == 'f':
        entry_type = 'float'
    elif entry_type == 'i':
        entry_type = 'int'
    elif entry_type == 'j':
        entry_type = 'json'
    elif entry_type == 's':
        entry_type = 'str'


    if  entry_type in allowed_types:
        return True
        
    raise RuntimeError("Illegal type '{}' submitted, allowed types are: {}".format( entry_type, allowed_types ))
    

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

    
def _add_entry(table:str, origin:str, source:int, context:int, log:str, entry_type:str):
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
    type_id    = _get_or_add_id( "types", 'type', entry_type)

    
#    db.add(table, {'origin_id': origin_id, 'source_id': source_id, 'context_id': context_id, 'log': log})
    db.add(table, {'origin_id': origin_id, 'source_id': source_id, 'context_id': context_id, 'log': log, 'type_id': type_id})
    

    

    
    
def add_stat(origin:str, source:str, context:int, value, entry_type:str='i'):
    """ adds a standard stat/event entry to a table function, that will be wrapped by simpler functions below


    Args:
      origin: where the log originates from, eg hostname or IP
      source: the source of the log, eg program or user
      context: The keyword for the log, eg all_idle 
      value: value to store, ideally an int or float
      entry_type: the type of data, default i[integer]

    returns:
      None

    Raises:
      None
    """

    _add_entry( 'stat', origin,  source, context, value, entry_type )


def add_event(origin:str, source:str, context:int, log:str, entry_type:str='s'):
    """ adds a standard stat/event entry to a table function, that will be wrapped by simpler functions below


    Args:
      origin: where the log originates from, eg hostname or IP
      source: the source of the log, eg program or user
      context: The keyword for the log, eg all_idle 
      log: what happened, nr or something else
      entry_type: the type of data, default s[tring]

    returns:
      None

    Raises:
      None
    """

    _add_entry( 'event', origin,  source, context, log, entry_type )

    

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


def values_only(entries):

    res = []
    
    for entry in entries:
        for key in entry:
            if key != 'id':
                res.append( entry[ key ])

    return res
                        

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

#    q  = "SELECT t.id, extract(epoch from t.ts) as ts, o.origin, s.source, c.context, t.log, ty.type "
    q  = "SELECT t.id, t.ts, o.origin, s.source, c.context, t.log, ty.type "
    q += "FROM {table} t, {table}_origin o, {table}_source s, {table}_context c, types ty ".format( table=table)
    q += "WHERE t.origin_id = o.id AND t.source_id = s.id AND t.context_id = c.id AND t.type_id=ty.id "

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
      order: default is timestamp, newest first

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
      order: default is timestamp, newest first

    return
      list of dicts of entries

    Raises:
      None
    """
    return _get_entries('event', start, end,limit, offset, order)





def filter(entries, origins=None, sources=None, contexts=None, logic='AND'):

    logic = logic.upper()
    if logic != 'AND' and logic !='OR':
        raise RuntimeError( "logic operators for filtering have to be either 'AND' or 'OR'")

    filtered = []
    for entry in entries:
        if ( logic == 'AND' and
             misc.none_or_contains_value(origins, entry['origin']) and
             misc.none_or_contains_value(sources, entry['source']) and
             misc.none_or_contains_value(contexts, entry['context'])):
            filtered.append( entry )

        elif ( logic == 'OR' and
             (misc.none_or_contains_value(origins, entry['origin']) or
              misc.none_or_contains_value(sources, entry['source']) or
              misc.none_or_contains_value(contexts, entry['context']))):
            filtered.append( entry )
                  
    return filtered




def _make_bins(start:int, end:int, size:int=60):
    """Makes bins for binning of data. The first bin will contain start, and the last one the end.

    Args:
      start: datatime format start time
      end: datatime format start time
      size: size of bins in seconds

    Returns
      list of times

    Raises:
      None

    """


    bins = []
    for i in range(start, end+size, size):
        i = int( i/size)*size
        
        bins.append( i )

        if i > end:
            break
        

    return bins

def aggregate( entries, size=60, method='mean',  start=None, end=None):
    """ aggregates numerical entries into bins and using means by default

    Args:
    entries: data to aggregate
    size: of bins
    method: Possibilites are: mean, median, sum

    Returns
      list of dict of aggregated observations

    Raises:
      None

    """

    if entries == [] or entries is None:
        return entries

    print("=======================================")
    print( start, end )
    
    entries = convert_ts_to_sec( entries )

    
    aggregate = {}

#    print( start, end )
    if start is None:
        start = entries[0]['ts']
        
    if end is None:
        end = entries[-1]['ts']


#    print( start, end )
        
    bins = _make_bins( start, end, size)
    for ts in bins:
        aggregate[ ts ] = {}

    # collect and sum the data
    keys = {}
    for entry in entries:
        ts   = entry[ 'ts' ]
        ts = int( ts/size)*size

        key_fields = []
        if 'origin' in entry:
             key_fields.append( entry['origin'] )

        if 'source' in entry:
             key_fields.append( entry['source'] )

        if 'context' in entry:
             key_fields.append( entry['context'] )

        key = ".".join( key_fields )
             
#        key = "{}.{}.{}".format( entry['origin'], entry['source'], entry['context'])

        if (ts not in aggregate ):
            aggregate[ ts ] = {}
        
        if key not in aggregate[ ts ]:
            aggregate[ ts ][ key ] = []

        keys[ key ] = 1
        

        if not misc.isnumber( entry['log']):
            raise RuntimeError( "Can only aggregate on numbers, '{}' (type: {}) is not a valid number".format( entry['log'] , type(entry['log'] )))

        aggregate[ ts ][ key ].append( float(entry['log']) )
        

    left_padding = True

    agg_list = []

#    pp.pprint( aggregate )
    
    # apply the wanted statistical method to the accumulated data.
    for ts in sorted( aggregate.keys() ):

        for key in keys:

            if key not in aggregate[ ts ]:
                aggregate[ ts ][ key ] = [0]

            
                 
            if method == 'sum':
                aggregate[ ts][ key ] = sum(aggregate[ ts ][ key ])
            elif method == 'mean':
                aggregate[ ts ][ key ] = sum(aggregate[ ts ][ key ])/len(aggregate[ ts ][ key ])
            elif method == 'median':
                aggregate[ ts ][ key ] = sorted( aggregate[ ts ][ key ])
                aggregate[ ts ][ key ] = aggregate[ ts ][ key ][ int(len ( aggregate[ ts ][ key ])/2)]
            else:
                raise RuntimeError("Illegal aggregate method '{}', use either mean, median or sum".format( method )) 

                
            entry = {'ts' : ts,
                     'method': method,
                      key:  aggregate[ ts ][ key ] }

            agg_list.append(entry)


#    return aggregate
    return agg_list


def transform_timeserie_to_dict( timeserie:dict):

    trans = {'x': []}

    for timestamp in sorted(timeserie):
        trans[ 'x' ].append( str( timestamp))
        
        for key in timeserie[ timestamp ]:
            if key not in trans:
                trans[ key ] = []
            trans[ key ].append( timeserie[ timestamp ][key] )

    return trans


def transform_aggregate_to_dict( aggregate:list):

    trans = {'x': []}

    for entry in aggregate:
        for key in entry:
            if ( key == 'ts'):
                entry['ts'] = kbr.time.to_string(entry['ts'])
                if entry['ts'] not in trans['x']:
                    trans['x'].append(entry['ts'] )
                    
            elif( key == 'method'):
                trans['method'] = entry[ 'method' ]
            
            else:
                if key not in trans:
                    trans[ key ] = []
                trans[ key ].append( entry[key] )

    return trans



def timeserie_max_value( timeserie:dict ):

    max_value = 12
    
    for timestamp in sorted(timeserie):
        for key in timeserie[ timestamp ]:
            if max_value < timeserie[ timestamp ][ key ]:
                max_value = timeserie[ timestamp ][ key ]

    return max_value



def purge_field( entries, field ):
    for entry in entries:
        if field in entry:
            del entry[ field ]
    
    return entries


def time_range_from_now( window, offset=0  ):

    now = time.time() - offset
#    now = kbr.time.now() - offset

    start = None
    end   = None
    
    if re.match( r'^(\d+)s$', window):

        match = re.match( r'^(\d+)s$', window)
        start, end = now - int(match.group( 1 )), now

    elif re.match( r'^(\d+)m$', window):

        match = re.match( r'^(\d+)m$', window)
        start, end = now - 60*int(match.group( 1 )), now

    elif re.match( r'^(\d+)h$', window):

        match = re.match( r'^(\d+)h$', window)
        start, end =  now - 3600*int(match.group( 1 )), now

    else:
        raise RuntimeError("Illegal timeformat {}, it has to be a integer followed by either s, m or h. Eg: 31m for 31 minuttes".format( window ))


    return start,  end

def convert_ts_to_sec( entries ):
    
    for entry in entries:
        if 'ts' in entry:
            if isinstance(entry[ 'ts' ], int):
                pass
            elif isinstance(entry[ 'ts' ], datetime.datetime):
                entry[ 'ts' ] =  int(entry[ 'ts' ].timestamp())
            else:
                entry[ 'ts' ] = int( entry[ 'ts' ] )

    return entries


def convert_ts_to_str( entries ):

    for entry in entries:
        if 'ts' in entry:
            if isinstance(entry[ 'ts' ], str):
                pass
            elif isinstance(entry[ 'ts' ], int):
                entry[ 'ts' ] =  str(datetime.datetime.fromtimestamp( entry[ 'ts' ]))
                
            elif isinstance(entry[ 'ts' ], datetime.datetime):
                entry[ 'ts' ] =  str(entry[ 'ts' ])

    return entries
