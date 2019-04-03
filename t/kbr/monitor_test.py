import pytest
from  random import randint
import  time

import pprint as pp
import json
import kbr.db_utils as db_utils
import kbr.monitor as monitor

# I am running a docker postgresql for the testing

# How I starts the image: docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres
# Create a test database
# createdb -h localhost -U postgres --owner=postgres test
# Connect to the server with: psql -h localhost -U postgres (-d test )

test_db      = "test"
postgres_url = "postgresql://postgres:docker@localhost:5432/{}".format( test_db)

def remove_ts( entries ):

    for entry in entries:
        entry[ 'ts' ] = 'T'

    return entries


def create_tables():

    # disconnect any hanging connections as this will deadlock the server
    monitor.disconnect()

    db = db_utils.DB( postgres_url )

    tables = db.table_names()

    for table in tables:
        db.do("DROP table IF EXISTS {} CASCADE".format( table ))

    db.from_file( 'sql/monitor.sql')

    db.close()

    m = monitor.connect( postgres_url )
    

def test_create_tables():
    create_tables()


def fill_tables():

    monitor.add_stat( "localhost1", "ehos3", "nodes_all4", 10, 'i')
    monitor.add_stat( "localhost2", "ehos4", "nodes_all5", 11, 'i')
    monitor.add_stat( "localhost3", "ehos5", "nodes_all6", 12, 'i')
    monitor.add_stat( "localhost4", "ehos3", "nodes_all7", 13, 'i')


    
    monitor.add_event( "localhost1", "ehos3", "start_all4", 9, 's' )  
    monitor.add_event( "localhost2", "ehos4", "start_all5", 11, 's')
    monitor.add_event( "localhost3", "ehos5", "start_all6", 12, 's')
    monitor.add_event( "localhost4", "ehos6", "start_all4", 13, 's')

    
def test_create_stat():

    test_create_tables()
    monitor.add_stat( "localhost", "ehos", "nodes_all", 10, 'i' )
    monitor.add_stat( "localhost", "ehos", "nodes_all", 11, 'i' )
    
    stats = monitor.get_stats()
    
    stats = remove_ts( stats) 

    pp.pprint( stats)
    
    assert stats == [{'context': 'nodes_all',
                       'id': 1,
                       'log': '10',
                       'origin': 'localhost',
                       'source': 'ehos',
                       'type': 'i',
                       'ts': 'T'},
                      {'context': 'nodes_all',
                       'id': 2,
                       'log': '11',
                       'origin': 'localhost',
                       'type': 'i',
                       'source': 'ehos',
                       'ts': 'T'}]
    


def test_create_event():

    test_create_tables()
    monitor.add_event( "localhost", "ehos", "create_node", json.dumps({'node_id': '423423424'}))
    monitor.add_event( "localhost", "ehos", "create_node", "create_nodes 123423424")

    events = monitor.get_events()
    events = remove_ts( events) 

    
    assert events == [{'context': 'create_node',
                       'id': 1,
                       'log': '{"node_id": "423423424"}',
                       'origin': 'localhost',
                       'type': 's',
                       'source': 'ehos',
                       'ts': 'T'},
                      {'context': 'create_node',
                       'id': 2,
                       'log': 'create_nodes 123423424',
                       'origin': 'localhost',
                       'source': 'ehos',
                       'type': 's',
                       'ts': 'T'}]
    

def test_get_order():

    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats(order ='ts desc')
    
    pp.pprint( stats )

    stats = remove_ts( stats) 

#    assert 1== 5
    
    assert stats == [{'context': 'nodes_all7',
                      'id': 4,
                      'log': '13',
                      'type': 'i',
                      'origin': 'localhost4',
                      'source': 'ehos3',
                      'ts': 'T'},
                     {'context': 'nodes_all6',
                      'id': 3,
                      'log': '12',
                      'type': 'i',
                      'origin': 'localhost3',
                      'source': 'ehos5',
                      'ts': 'T'},
                     {'context': 'nodes_all5',
                      'id': 2,
                      'log': '11',
                      'type': 'i',
                      'origin': 'localhost2',
                      'source': 'ehos4',
                      'ts': 'T'},
                     {'context': 'nodes_all4',
                      'id': 1,
                      'log': '10',
                      'type': 'i',
                      'origin': 'localhost1',
                      'source': 'ehos3',
                      'ts': 'T'}]

    

def test_get_start():

    test_create_tables()
    fill_tables()
    
    stats1 = monitor.get_stats()
    

    stats2 = monitor.get_stats( start = stats1[1]['ts'] )
    stats2 = remove_ts( stats2 ) 
    
    assert stats2 == [{'context': 'nodes_all5',
                      'id': 2,
                      'log': '11',
                      'origin': 'localhost2',
                      'type': 'i',
                      'source': 'ehos4',
                      'ts': 'T'},
                      {'context': 'nodes_all6',
                      'id': 3,
                      'type': 'i',
                      'log': '12',
                      'origin': 'localhost3',
                      'source': 'ehos5',
                      'ts': 'T'},
                      {'context': 'nodes_all7',
                      'id': 4,
                      'type': 'i',
                      'log': '13',
                      'origin': 'localhost4',
                      'source': 'ehos3',
                      'ts': 'T'},]


    


def test_get_end():

    test_create_tables()
    fill_tables()
    
    stats1 = monitor.get_stats()
    

    stats2 = monitor.get_stats( end = stats1[-2]['ts'])
    stats2 = remove_ts( stats2 ) 

    
    assert stats2 == [{'context': 'nodes_all4',
                      'id': 1,
                      'log': '10',
                      'type': 'i',
                      'origin': 'localhost1',
                      'source': 'ehos3',
                      'ts': 'T'},
                     {'context': 'nodes_all5',
                      'id': 2,
                      'type': 'i',
                      'log': '11',
                      'origin': 'localhost2',
                      'source': 'ehos4',
                      'ts': 'T'},
                     {'context': 'nodes_all6',
                      'id': 3,
                      'log': '12',
                      'type': 'i',
                      'origin': 'localhost3',
                      'source': 'ehos5',
                      'ts': 'T'}]


def test_get_range():

    test_create_tables()
    fill_tables()
    
    stats1 = monitor.get_stats()
    

    stats2 = monitor.get_stats( start = stats1[1]['ts'], end = stats1[-2]['ts'])
    stats2 = remove_ts( stats2 ) 
    
    assert stats2 == [{'context': 'nodes_all5',
                      'id': 2,
                      'log': '11',
                      'type': 'i',
                      'origin': 'localhost2',
                      'source': 'ehos4',
                      'ts': 'T'},
                     {'context': 'nodes_all6',
                      'id': 3,
                      'log': '12',
                      'type': 'i',
                      'origin': 'localhost3',
                      'source': 'ehos5',
                      'ts': 'T'}]


    
def test_get_limit():

    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats(limit=2, order ='ts desc')
    
    stats = remove_ts( stats) 
    
    assert stats == [{'context': 'nodes_all7',
                      'id': 4,
                      'log': '13',
                      'origin': 'localhost4',
                      'type': 'i',
                      'source': 'ehos3',
                      'ts': 'T'},
                     {'context': 'nodes_all6',
                      'id': 3,
                      'log': '12',
                      'origin': 'localhost3',
                      'type': 'i',
                      'source': 'ehos5',
                      'ts': 'T'}]
    
def test_get_offset():

    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats(limit=2, offset=1, order ='ts desc')
    
    stats = remove_ts( stats) 
    assert stats == [{'context': 'nodes_all6',
                      'id': 3,
                      'log': '12',
                      'origin': 'localhost3',
                      'type': 'i',
                      'source': 'ehos5',
                      'ts': 'T'},
                     {'context': 'nodes_all5',
                      'id': 2,
                      'log': '11',
                      'type': 'i',
                      'origin': 'localhost2',
                      'source': 'ehos4',
                      'ts': 'T'}]
    
    
def test_stat_origins():

    test_create_tables()
    fill_tables()
    

    origins = monitor.stat_origins()
    
    assert origins == [ {'id': 1,
                         'origin': 'localhost1'},
                        {'id': 2,
                         'origin': 'localhost2'},
                        {'id': 3,
                         'origin': 'localhost3'},
                        {'id': 4,
                         'origin': 'localhost4'}]
    
def test_stat_source():

    test_create_tables()
    fill_tables()
    

    sources = monitor.stat_sources()
    
    assert sources == [ {'id': 1,
                         'source': 'ehos3'},
                        {'id': 2,
                         'source': 'ehos4'},
                        {'id': 3,
                         'source': 'ehos5'}]


def test_stat_context():

    test_create_tables()
    fill_tables()
    
    
    contexts = monitor.stat_contexts()
    
    assert contexts == [ {'id': 1,
                         'context': 'nodes_all4'},
                        {'id': 2,
                         'context': 'nodes_all5'},
                        {'id': 3,
                         'context': 'nodes_all6'},
                        {'id': 4,
                         'context': 'nodes_all7'}]
    
    

    
def test_event_origins():

    test_create_tables()
    fill_tables()
    

    origins = monitor.event_origins()
    
    assert origins == [ {'id': 1,
                         'origin': 'localhost1'},
                        {'id': 2,
                         'origin': 'localhost2'},
                        {'id': 3,
                         'origin': 'localhost3'},
                        {'id': 4,
                         'origin': 'localhost4'}]


def test_event_source():

    test_create_tables()
    fill_tables()
    

    sources = monitor.event_sources()
    
    assert sources == [ {'id': 1,
                         'source': 'ehos3'},
                        {'id': 2,
                         'source': 'ehos4'},
                        {'id': 3,
                         'source': 'ehos5'},
                        {'id': 4,
                         'source': 'ehos6'}]


def test_event_context():

    test_create_tables()
    fill_tables()
    
    
    contexts = monitor.event_contexts()
    
    assert contexts == [ {'id': 1,
                         'context': 'start_all4'},
                        {'id': 2,
                         'context': 'start_all5'},
                        {'id': 3,
                         'context': 'start_all6'}]
    



def test_filters_illegal_logic():    
    with pytest.raises( RuntimeError ):
        monitor.filter( {}, logic='xor')


    
def test_filters_origins():    
    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats()

    

    assert remove_ts(monitor.filter( stats, origins='localhost1')) == [{'context': 'nodes_all4',
                                                            'id': 1,
                                                            'log': '10',
                                                            'origin': 'localhost1',
                                                            'source': 'ehos3',
                                                            'ts': 'T'}]




def test_filters_sources():    
    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats()

    
    assert remove_ts(monitor.filter( stats, sources='ehos3')) == [{'context': 'nodes_all4',
                                                                   'id': 1,
                                                                   'log': '10',
                                                                   'origin': 'localhost1',
                                                                   'source': 'ehos3',
                                                                   'ts': 'T'}]
def test_filters_contexts():    
    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats()


    assert remove_ts(monitor.filter( stats, contexts='nodes_all4')) == [{'context': 'nodes_all4',
                                                                    'id': 1,
                                                                    'log': '10',
                                                                    'type': 'i',
                                                                    'origin': 'localhost1',
                                                                    'source': 'ehos3',
                                                                    'ts': 'T'}]

    



def test_filters_origins():    
    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats()

    

    assert remove_ts(monitor.filter( stats, origins='localhost1')) == [{'context': 'nodes_all4',
                                                            'id': 1,
                                                            'log': '10',
                                                            'origin': 'localhost1',
                                                            'type': 'i',
                                                            'source': 'ehos3',
                                                            'ts': 'T'}]




def test_filters_sources():    
    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats()

    
    assert remove_ts(monitor.filter( stats, sources='ehos3')) == [{'context': 'nodes_all4',
                                                                   'id': 1,
                                                                   'log': '10',
                                                                   'origin': 'localhost1',
                                                                   'type': 'i',
                                                                   'source': 'ehos3',
                                                                   'ts': 'T'},
                                                                  {'context': 'nodes_all7',
                                                                   'id': 4,
                                                                   'log': '13',
                                                                   'type': 'i',
                                                                   'origin': 'localhost4',
                                                                   'source': 'ehos3',
                                                                   'ts': 'T'}]
def test_filters_and():    
    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats()


    assert remove_ts(monitor.filter( stats, origins=['localhost1'],
                                            sources='ehos3',
                                            contexts='nodes_all4')) == [{'context': 'nodes_all4',
                                                                    'id': 1,
                                                                    'log': '10',
                                                                    'origin': 'localhost1',
                                                                    'type': 'i',
                                                                    'source': 'ehos3',
                                                                    'ts': 'T'}]

    

def test_filters_or():    
    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats()


    assert remove_ts(monitor.filter( stats, origins=['localhost1'],
                                            sources='ehos4',
                                            contexts='nodes_all6',
                                            logic='or')) == [    {'context': 'nodes_all4',
                                                                  'id': 1,
                                                                  'log': '10',
                                                                  'type': 'i',
                                                                  'origin': 'localhost1',
                                                                  'source': 'ehos3',
                                                                  'ts': 'T'},
                                                                 
                                                                 {'context': 'nodes_all5',
                                                                  'id': 2,
                                                                  'log': '11',
                                                                  'origin': 'localhost2',
                                                                  'type': 'i',
                                                                  'source': 'ehos4',
                                                                  'ts': 'T'},
                                                                 
                                                                 {'context': 'nodes_all6',
                                                                  'id': 3,
                                                                  'log': '12',
                                                                  'type': 'i',
                                                                  'origin': 'localhost3',
                                                                  'source': 'ehos5',
                                                                  'ts': 'T'},
                                            ]
    
    
    
def test_make_bins():

    
    bins = monitor._make_bins( start = 10001, end= 10122)

    pp.pprint( bins )

    assert bins == [9960, 10020, 10080, 10140]
    

def test_aggregate_mean():

    d = []

    for i in range(0, 300):
        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 3,
                   'origin': 'localhost1',
                   'source': 'ehos3',
                   'ts': 1546527918  + i  } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 6 + i,
                   'origin': 'localhost1',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 7 + i*2,
                   'origin': 'localhost2',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )


#    pp.pprint( d )

    md = monitor.aggregate( d, size=10 )

    pp.pprint( md )
    assert md[ 1546527910] == {'localhost1.ehos3.nodes_all4': 3.0,
                               'localhost1.ehos4.nodes_all4': 6.5,
                               'localhost2.ehos4.nodes_all4': 8.0}


    assert md[ 1546528210 ] == {'localhost1.ehos3.nodes_all4': 3.0,
                                'localhost1.ehos4.nodes_all4': 301.5,
                                'localhost2.ehos4.nodes_all4': 598.0}
    


def test_aggregate_median():

    d = []

    for i in range(0, 300):
        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 3,
                   'origin': 'localhost1',
                   'source': 'ehos3',
                   'ts': 1546527918  + i  } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 6 + i,
                   'origin': 'localhost1',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 7 + i*2,
                   'origin': 'localhost2',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )


#    pp.pprint( d )

    md = monitor.aggregate( d, size=30, method='median' )

#    pp.pprint( md )
    assert md[ 1546527900] == {'localhost1.ehos3.nodes_all4': 3.0,
                               'localhost1.ehos4.nodes_all4': 12.0,
                               'localhost2.ehos4.nodes_all4': 19.0}

    assert md[ 1546528200 ] == {'localhost1.ehos3.nodes_all4': 3.0,
                                'localhost1.ehos4.nodes_all4': 297.0,
                                'localhost2.ehos4.nodes_all4': 589.0}

    

    
def test_aggregate_sum():

    d = []

    for i in range(0, 300):
        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 3,
                   'origin': 'localhost1',
                   'source': 'ehos3',
                   'ts': 1546527918  + i  } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 6 + i,
                   'origin': 'localhost1',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 7 + i*2,
                   'origin': 'localhost2',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )


#    pp.pprint( d )

    md = monitor.aggregate( d, size=30, method='sum' )

#    pp.pprint( md )
#    assert 1 == 3
    assert md[ 1546527900] == {'localhost1.ehos3.nodes_all4': 36.0,
                               'localhost1.ehos4.nodes_all4': 138.0,
                               'localhost2.ehos4.nodes_all4': 216.0}

    assert md[ 1546528200 ] == {'localhost1.ehos3.nodes_all4': 54.0,
                                'localhost1.ehos4.nodes_all4': 5337.0,
                                'localhost2.ehos4.nodes_all4': 10584.0}

    

def test_aggregate_illegal_method():

    d = []

    for i in range(0, 300):
        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 3,
                   'origin': 'localhost1',
                   'source': 'ehos3',
                   'ts': 1546527918  + i  } )


#    pp.pprint( d )

    with pytest.raises( RuntimeError ):
        md = monitor.aggregate( d, size=30, method='medians' )


def test_aggregate_illegal_value():

    d = []

    for i in range(0, 300):
        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': '3k',
                   'origin': 'localhost1',
                   'source': 'ehos3',
                   'ts': 1546527918  + i  } )


#    pp.pprint( d )

    with pytest.raises( RuntimeError ):
        md = monitor.aggregate( d, size=30, method='medians' )


        


def test_aggregate_left_padding():

    d = []

    for i in range(0, 300):
        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 3,
                   'origin': 'localhost1',
                   'source': 'ehos3',
                   'ts': 1546527918  + i  } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 6 + i,
                   'origin': 'localhost1',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 7 + i*2,
                   'origin': 'localhost2',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )

    
    for i in range(0, 300):
        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 3,
                   'origin': 'localhost1',
                   'source': 'ehos3',
                   'ts': 1546527918  + i  } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 6 + i,
                   'origin': 'localhost1',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 7 + i*2,
                   'origin': 'localhost2',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )


    md = monitor.aggregate( d, size=30, method='sum', start=1546527918-60, end=1546527918+350)

    assert md[ 1546527840 ] == {'localhost1.ehos3.nodes_all4': 0,
                               'localhost1.ehos4.nodes_all4': 0,
                               'localhost2.ehos4.nodes_all4': 0}


    assert md[ 1546528260 ] == {'localhost1.ehos3.nodes_all4': 0,
                               'localhost1.ehos4.nodes_all4': 0,
                               'localhost2.ehos4.nodes_all4': 0}
        

def test_transform_timeserie_to_dict():
    
    d = []

    for i in range(0, 40):
        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 3,
                   'origin': 'localhost1',
                   'source': 'ehos3',
                   'ts': 1546527918  + i  } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 6 + i,
                   'origin': 'localhost1',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 7 + i*2,
                   'origin': 'localhost2',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )


#    pp.pprint( d )

    md = monitor.aggregate( d, size=30, method='sum' )
    md = monitor.transform_timeserie_to_dict( md )


    assert md == {'localhost1.ehos3.nodes_all4': [36.0, 84.0, 0],
                  'localhost1.ehos4.nodes_all4': [138.0, 882.0, 0],
                  'localhost2.ehos4.nodes_all4': [216.0, 1624.0, 0],
                  'x': ['1546527900', '1546527930', '1546527960']}
    


def test_timeserie_max_value( ):

    d = []

    for i in range(0, 40):
        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 3,
                   'origin': 'localhost1',
                   'source': 'ehos3',
                   'ts': 1546527918  + i  } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 6 + i,
                   'origin': 'localhost1',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )

        d.append( {'context': 'nodes_all4',
                   'id': 1,
                   'log': 7 + i*2,
                   'origin': 'localhost2',
                   'source': 'ehos4',
                   'ts': 1546527918  + i } )


#    pp.pprint( d )

    md = monitor.aggregate( d, size=30, method='sum' )

    max_value = monitor.timeserie_max_value( md )
    
    assert max_value == 1624.0


def test_purge_origin_field():
    data =  [    {'context': 'nodes_all4',
                  'id': 1,
                  'log': '10',
                  'origin': 'localhost1',
                  'source': 'ehos3',
                  'ts': 'T'},
                 
                 {'context': 'nodes_all5',
                  'id': 2,
                  'log': '11',
                  'origin': 'localhost2',
                  'source': 'ehos4',
                  'ts': 'T'},
                 
                 {'context': 'nodes_all6',
                  'id': 3,
                  'log': '12',
                  'source': 'ehos5',
                  'ts': 'T'} ]


    data = monitor.purge_field( data, 'origin')


    assert data == [    {'context': 'nodes_all4',
                         'id': 1,
                         'log': '10',
                         'source': 'ehos3',
                         'ts': 'T'},
                        
                        {'context': 'nodes_all5',
                         'id': 2,
                         'log': '11',
                         'source': 'ehos4',
                         'ts': 'T'},
                        
                        {'context': 'nodes_all6',
                         'id': 3,
                         'log': '12',
                         'source': 'ehos5',
                         'ts': 'T'} ]
 

def test_time_range_from_now_seconds():

    
    start_time, end_time = monitor.time_range_from_now('500s', offset=3600)

    now = time.time() - 3600
    

    assert int(start_time) == int(now - 500)
    assert int(end_time) == int(now )


def test_time_range_from_now_mins():

    now = time.time()
    
    start_time, end_time = monitor.time_range_from_now('5m')

    assert int(start_time) == int(now - 5*60)
    assert int(end_time) == int(now )
    

def test_time_range_from_now_hours():

    now = time.time()
    
    start_time, end_time = monitor.time_range_from_now('5h')

    assert int(start_time) == int(now - 5*3600)
    assert int(end_time) == int(now )

    
def test_time_range_from_now_illegal():

    now = time.time()
    
    with pytest.raises( RuntimeError ):
        start_time, end_time = monitor.time_range_from_now('5ms')


    
    
def test_check_type():
    assert monitor._check_type('f')
    assert monitor._check_type('float')
    assert monitor._check_type('i')
    assert monitor._check_type('int')
    assert monitor._check_type('j')
    assert monitor._check_type('json')
    assert monitor._check_type('str')
    assert monitor._check_type('s')
    

def test_check_type_illegal():
    with pytest.raises( RuntimeError ):
        monitor._check_type('5ms')
    
