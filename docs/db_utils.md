# db_utils

# examples 

###db = db.DB( url )
    url format: postgresql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DB-NAME>


###db.get(table, logic:str='AND', order:str=None, limit:int=None, offset:int=None, **values ) -> {}
    type_samples = self._db.get('sample_type', type_id=1, name='sample_name1')


###db.add( table:str, entry:{}):
        db.add_unique('type', {'name': name, 'reference':'ref2'})
        
###db.add_unique('node_state', {'name':node_state}, key='name')
        db.add_unique('type', {'name': name, 'reference':'ref2'}, 'name')

###db.get_as_dict(query)
    db.get_as_dict("SELECT * FROM node WHERE uuid = '12';")

###db.get_id(table, **values)
    db.get_id('center', name=center_name)

###update(self, table:str, entry:{}, conditions:{}):
    db.update_node('table1', {'name': 'new_name'}, {'id': 1})

    
###db.do(query)

    db.do("select * from sample;")


