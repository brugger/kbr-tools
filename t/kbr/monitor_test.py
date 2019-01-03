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
    monitor.add_stat( "localhost1", "ehos3", "nodes_all4", 10 )
    monitor.add_stat( "localhost2", "ehos4", "nodes_all5", 11 )
    monitor.add_stat( "localhost3", "ehos5", "nodes_all6", 12 )
    monitor.add_stat( "localhost4", "ehos6", "nodes_all7", 13 )


    
    monitor.add_event( "localhost1", "ehos3", "start_all4", 9  )
    monitor.add_event( "localhost2", "ehos4", "start_all5", 11 )
    monitor.add_event( "localhost3", "ehos5", "start_all6", 12 )
    monitor.add_event( "localhost4", "ehos6", "start_all4", 13 )
    
def test_create_stat():

    test_create_tables()
    monitor.add_stat( "localhost", "ehos", "nodes_all", 10 )
    monitor.add_stat( "localhost", "ehos", "nodes_all", 11 )
    
    stats = monitor.get_stats()
    
    stats = remove_ts( stats) 
    
    assert stats == [{'context': 'nodes_all',
                       'id': 1,
                       'log': '10',
                       'origin': 'localhost',
                       'source': 'ehos',
                       'ts': 'T'},
                      {'context': 'nodes_all',
                       'id': 2,
                       'log': '11',
                       'origin': 'localhost',
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
                       'source': 'ehos',
                       'ts': 'T'},
                      {'context': 'create_node',
                       'id': 2,
                       'log': 'create_nodes 123423424',
                       'origin': 'localhost',
                       'source': 'ehos',
                       'ts': 'T'}]
    

def test_get_order():

    test_create_tables()
    fill_tables()
    
    stats = monitor.get_stats(order ='ts desc')
    
    stats = remove_ts( stats) 

    assert stats == [{'context': 'nodes_all7',
                      'id': 4,
                      'log': '13',
                      'origin': 'localhost4',
                      'source': 'ehos6',
                      'ts': 'T'},
                     {'context': 'nodes_all6',
                      'id': 3,
                      'log': '12',
                      'origin': 'localhost3',
                      'source': 'ehos5',
                      'ts': 'T'},
                     {'context': 'nodes_all5',
                      'id': 2,
                      'log': '11',
                      'origin': 'localhost2',
                      'source': 'ehos4',
                      'ts': 'T'},
                     {'context': 'nodes_all4',
                      'id': 1,
                      'log': '10',
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
                      'source': 'ehos4',
                      'ts': 'T'},
                      {'context': 'nodes_all6',
                      'id': 3,
                      'log': '12',
                      'origin': 'localhost3',
                      'source': 'ehos5',
                      'ts': 'T'},
                      {'context': 'nodes_all7',
                      'id': 4,
                      'log': '13',
                      'origin': 'localhost4',
                      'source': 'ehos6',
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
                      'origin': 'localhost2',
                      'source': 'ehos4',
                      'ts': 'T'},
                     {'context': 'nodes_all6',
                      'id': 3,
                      'log': '12',
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
                      'source': 'ehos6',
                      'ts': 'T'},
                     {'context': 'nodes_all6',
                      'id': 3,
                      'log': '12',
                      'origin': 'localhost3',
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
                      'source': 'ehos5',
                      'ts': 'T'},
                     {'context': 'nodes_all5',
                      'id': 2,
                      'log': '11',
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
                         'source': 'ehos5'},
                        {'id': 4,
                         'source': 'ehos6'}]


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
    

    
def _timeseries_bulk_stat():

    print( "This one will take some time... ")
    
    test_create_tables()
    for i in range(0, 5000):
        v = randint(300,500)
        time.sleep( randint( 30,40)/1000000.0)
        monitor.add_stat( "localhost", "nodes", "idle", v )
    

def _timeserie_extract():

    m = monitor.connect( postgres_url )

    pp.pprint( monitor.timeserie_30min('stat'))

    assert 1==4, 'm'
