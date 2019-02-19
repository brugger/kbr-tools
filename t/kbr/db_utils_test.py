import sys
import os
import pytest

import pprint as pp

from sqlalchemy.exc import * 


import kbr.db_utils as db_utils


sys.path.append(".")

def make_database():

    drop_database()
    
    q = "CREATE TABLE test ( id INTEGER PRIMARY KEY AUTOINCREMENT,   value      VARCHAR(200) );"

    db = db_utils.DB( 'sqlite:///testing')

    db.do(q)
    
    return db


def drop_database(db=None):
    if os.path.isfile( 'testing'):
        os.unlink( 'testing')
    


def test_makedb():

    db = make_database()
    drop_database( db )

    db.close()

def test_do():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b');")

def test_do_error():

    db = make_database()
    with pytest.raises( OperationalError ):
        db.do("insert into test (value) values (1) (2);")



def test_from_file():

    db = make_database()
    db.from_file( 't/data/test.sql')

def test_from_file_error():

    db = make_database()
    with pytest.raises( RuntimeError ):
        db.from_file( 't/data/testss.sql')



def test_table_names():
    db = make_database()
    assert db.table_names() == ['sqlite_sequence', 'test']

        
def test_get():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get( "select * From test")

    assert res == [{'id': 1, 'value': 'a'},
                   {'id': 2, 'value': 'b'},
                   {'id': 3, 'value': 'c'}]


def test_get_empty():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get( "select * From test where id == 7")

    assert res == []
    

def test_get_error():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    with pytest.raises( OperationalError ):
        db.get( "select * From tests")


def test_count():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.count( "select * From test;")

    assert res == 3


def test_count_empty():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.count( "select * From test where id = 5;")

    assert res == 0


def test_get_all():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get_all( 'test')
    assert res == [{'id': 1, 'value': 'a'},
                   {'id': 2, 'value': 'b'},
                   {'id': 3, 'value': 'c'}]


def test_get_all_order():

    db = make_database()
    db.do("insert into test (value) values ('c'), ('b'), ('a');")
    
    res = db.get_all( 'test', "value")
    assert res == [{'id': 3, 'value': 'a'},
                   {'id': 2, 'value': 'b'},
                   {'id': 1, 'value': 'c'}]
    
def test_get_all_empty():

    db = make_database()
    
    res = db.get_all( 'test')
    assert res == []
    


def test_get_by_value():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get_by_value( 'test', 'value', 'b')
    assert res == [{'id': 2, 'value': 'b'}]


    
def test_get_by_value_empty():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get_by_value( 'test', 'value', 'd')
    assert res == []
    
def test_get_by_value_order():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c'), ('c');")
    
    res = db.get_by_value( 'test', 'value', 'c', 'id desc')
    assert res == [{'id': 4, 'value': 'c'},
                   {'id': 3, 'value': 'c'}]



def test_get_by_values():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get_by_values( 'test', value='b')
    assert res == [{'id': 2, 'value': 'b'}]

def test_get_by_values():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get_by_values( 'test', value='b', id=3, order=' id desc', logic='or', )
    assert res == [{'id': 3, 'value': 'c'},
                   {'id': 2, 'value': 'b'}]

    
    
def test_get_by_id():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get_by_id( 'test', 2)
    assert res == [{'id': 2, 'value': 'b'}]

def test_get_by_id_empty():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get_by_id( 'test', 8)
    assert res == []
    


def  test_get_id():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get_id( 'test', 'value', 'b')
    assert res == 2
    
def test_get_id_empty():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    
    res = db.get_id( 'test', 'value', 'f')
    assert res == None



def test_add():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    res = db.add( 'test', {'value': 'f'})

    res = db.get_all('test')
    assert res == [{'id': 1, 'value': 'a'},
                   {'id': 2, 'value': 'b'},
                   {'id': 3, 'value': 'c'},
                   {'id': 4, 'value': 'f'}]

def test_add_error():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")
    with pytest.raises( OperationalError ):
        res = db.add( 'test', {'values': 'f'})

def test_add_empty():
    db = make_database()
    with pytest.raises( RuntimeError ):
        res = db.add( 'test', {})
        

def test_add_unique_empty():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")

    with pytest.raises( RuntimeError ):
        id = db.add_unique( 'test', {}, 'value')


def test_add_unique():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")

    id = db.add_unique( 'test', {'value':'b'}, 'value')

    assert id == 2
    


def test_add_unique_new():
    db = make_database()
    db.do("insert into test (value) values ('a'), ('b'), ('c');")

    id = db.add_unique( 'test', {'value':'f'}, 'value')

    assert id == 4

def test_add_bulk():
    db = make_database()
    res = db.add_bulk( 'test', [{'value': 'a'},
                                {'value': 'c'},
                                {'value': 'f'}])

    res = db.get_all('test')
    assert res == [{'id': 1, 'value': 'a'},
                   {'id': 2, 'value': 'c'},
                   {'id': 3, 'value': 'f'}]

def test_add_bulk_diff():
    db = make_database()
    with pytest.raises( RuntimeError ):
        res = db.add_bulk( 'test', [{'value': 'a'},
                                    {'value': 'c', 'state':'q'},
                                    {'value': 'f'}])

def test_add_bulk_empty():
    db = make_database()
    with pytest.raises( RuntimeError ):
        res = db.add_bulk( 'test', [])
    
    with pytest.raises( RuntimeError ):
        res = db.add_bulk( 'test', {})


        
def test_update():

    db = make_database()
    res = db.add_bulk( 'test', [{'value': 'a'},
                                {'value': 'c'},
                                {'value': 'f'}])

    entry = db.get_by_id( 'test',2)[0]
    assert entry == {'id': 2, 'value': 'c'}


    entry['value'] = 'c'
    db.update( 'test', entry, ['id'])


def test_update_no_values():

    db = make_database()
    res = db.add_bulk( 'test', [{'value': 'a'},
                                {'value': 'c'},
                                {'value': 'f'}])

    entry = db.get_by_id( 'test',2)[0]
    with pytest.raises( RuntimeError ):
        db.update( 'test', {}, ['id'])
    
def test_update_no_cond():

    db = make_database()
    res = db.add_bulk( 'test', [{'value': 'a'},
                                {'value': 'c'},
                                {'value': 'f'}])

    entry = db.get_by_id( 'test',2)[0]
    with pytest.raises( RuntimeError ):
        db.update( 'test', entry, [])
    
def test_update_wrong_cond():

    db = make_database()
    res = db.add_bulk( 'test', [{'value': 'a'},
                                {'value': 'c'},
                                {'value': 'f'}])

    entry = db.get_by_id( 'test',2)[0]
    with pytest.raises( RuntimeError ):
        db.update( 'test', entry, ['ids'])
