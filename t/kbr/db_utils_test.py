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
    

def test_do():

    db = make_database()
    db.do("insert into test (value) values ('a'), ('b');")

def test_do_error():

    db = make_database()
    with pytest.raises( OperationalError ):
        db.do("insert into test (value) values (1) (2);")


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
