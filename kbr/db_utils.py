"""

Generica low level function for interacting with a database through the records package


"""


import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
import time
import datetime

import records




class DB( object ):

    def __init__( self, url:str) -> bool:
        """ connects to a database instance 

        Args:
        url: as specified by sqlalchemy ( {driver}://{user}:{password}@{host}:{port}/{dbase}
        
        Returns:
        none
        
        Raises:
        RuntimeError on failure.


        """
    
        self._db = records.Database( url )
        


    def execute_file(self, filename:str):
        """ readin a sql file and execute the content 

        Args:
          filename: file to read from

        Returns:
          None

        Raises:
          error on file not exist or sql errors
        """
        
        file_handle = open(file_path, 'r')
        content = file_handle.read()
        file_handle.close()

        for command in content(sql_file).replace("\n", " ").split(';'):
            if command.strip() == "":
                continue
        self.do(command)

    def do(self, sql:str) -> None:
        """ execute a query 

        Args:
          sql: query to execute

        returns
          the result of the query

        raises:
          None
        """
        return self._db.query( sql )

    def get(self, sql:str) -> {}:
        """ executes a query and returns the data as a dict

        Args:
          sql query to execute
        
        Returns:
          result as a dict, or dict list

        Raises:
          None
        """

        return self.do( sql ).as_dict()
        
    def count(self, sql:str) -> int:
        """ executes a query and returns the number of rows generated 
        
        Args:
          sql query to execute

        Returns:
          nr of rows, 0 if none found

        Raises:
          None

        """

        res = self.do( sql ).all()
        return len( res )

        

    def get_all( self, table:str, order:str=None):
        q = "SELECT * FROM {table}".format( table=table )

        if order is not None:
            q += " order by {order}".format( order )

        return self.get( q )
            


    def get_by_value(self, table, key:str, value:str, order:str=None ) -> {}:
        q = "SELECT * from {table} where {key} = '{value}'"
        q = q.format( table=table, key=key, value=value )

        if order is not None:
            q += " order by {order}".format( order )

        return self.get( q )

    
    def get_by_id(self, table, value ) -> {}:
        return self.get_by_value( table, 'id', value)


    def get_id(self, table, key, value ) -> id:
        q = "SELECT id from {table} where {key} = '{value}'"
        q = q.format( table=table, key=key, value=value )
        res = self.get( q )
        if 'id' in res[0]:
            return res[0][ 'id' ]
        else:
            return None
    
    def add( self, table:str, entry:{}):

        keys = list( entry.keys())
        values = []


        for key, value in entry:

            keys.append( key )
            values.append( value )

        q = "INSERT INTO {table} ({keys}) VALUES ({values})".format( table = table,
                                                                     keys=",".join(keys),
                                                                     values=",".join(values))
        self.do( q )


    def add_bulk( self, table:str, entries:[] ):

        all_values = []
        keys = list(entries[ 0 ].keys())


        for key in keys:
            if key not in column_name:
                raise RuntimeError("column {key} is not present in table {table}",format(key=key, table=table))

        
        for entry in entries:

            if  keys  != list(entry.keys()):
                raise RuntimeError( 'Not the same number of values in all entries!')
            values = []
            for key, value in entry:
                values.append
                
            all_values.append( "( {values}) )".format( ",".join( self.escape_str(values))))

        q = "INSERT INTO {table} ({keys}) VALUES ({values})".format( table = table,
                                                                     keys=",".join(keys),
                                                                     values=",".join(all_values))
        self.do( q )

                            
                
    def update(self, table:str, values:[], conditions):
        
        keys = list( entry.keys())
        values = []


        updates = []
        for key, value in entry:

            updates.append( "{key} = '{value}'".format( key=key, value=value))

        cond_values = []
        cond_keys = list( conditions.keys())
        self.check_column_names( table, cond_keys)
        conds = []
        for key, value in condition:
            conds.append( "{key} = '{value}'".format( key=key, value=value))


            
        
        q = "UPDATE {table} set {updates} WHERE {conds}".format( table = table,
                                                                 updates=" and ".join(updates),
                                                                 conds=" and ".join(conds))
        self.do( q )




