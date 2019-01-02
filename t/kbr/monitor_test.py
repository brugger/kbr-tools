import pytest

import kbr.db_utils as db_utils
import kbr.monitor as monitor

# I am running a docker postgresql for the testing

# How I starts the image: docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres
# Create a test database
# createdb -h localhost -U postgres --owner=postgres test
# Connect to the server with: psql -h localhost -U postgres (-d test )

test_db      = "test"
postgres_url = "postgresql://postgres:docker@localhost:5432/{}".format( test_db)


def create_db():

    db = db_utils.DB( postgres_url )

    drop_tables( db )

    db.from_file( 'sql/monitor.sql')

    return db

def drop_tables( db ):

    tables = db.table_names()

    for table in tables:
        db.do("DROP table IF EXISTS {} CASCADE".format( table ))
    

def test_create_db():
    db = create_db()

    m = monitor.connect( postgres_url )

    return m
    
def test_create_stat():

    test_create_db()
    monitor.add_stat( "nodes", "all", 10 )
    monitor.add_stat( "nodes", "all", 11 )
    monitor.add_stat( "nodes", "all", 12 )
    monitor.add_stat( "nodes", "all", 15 )
    

def test_create_event():

    test_create_db()
    monitor.add_event( "nodes", "all", "create_node 123423424")
