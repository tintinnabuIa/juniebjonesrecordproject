try: import sql_init as sql
except: from . import sql_init as sql
from dataclasses import dataclass, is_dataclass
from functools import cache

# search parameter dataclasses that use the major
# tables---the stems---because they're the most useful ones
@dataclass
class Search_Params:

    @dataclass
    class Artist:
        id: int = None
        name: str = None
        realname: str = None
        profile: str = None
        data_quality: str = None

    @dataclass
    class Label:
        id: int = None
        name: str = None
        contact_info: str = None
        profile: str = None
        parent_id: int = None
        parent_name: str = None
        data_quality: str = None

    @dataclass
    class Master:
        id: int = None
        title: str = None
        year: int = None
        main_release: int = None
        data_quality: str = None

    @dataclass 
    class Release:
        id: int = None
        title: str = None
        released: str = None
        country: str = None
        notes: str = None
        data_quality: str = None
        main: int = None
        master_id: int = None
        status: str = None

@cache
def construct_class_init_dict(superclass):
    class_dict = {}
    # convert superclass to dict as to loop through so that there
    # doesn't have to be a bunch of if statements in main.py /api/post
    for class_item in vars(superclass).values():
        if is_dataclass(class_item):
            class_dict[class_item.__name__] = class_item
    return class_dict

# Note: I'm using some strange combination of SQLModel, 
# where my database tables are reflected into SQLAlchemy tables, 
# but I'm using the SQLModel library, so statements that query 
# the database require SQLAlchemy formatting, like table.c.column_name and execute(). 
# I am a lazy bum who does not want to transfer the tables into SQLModel, 
# and I'd rather not switch to SQLAlchemy itself as to avoid 
# (1) rewriting more code and (2) get the autocompletes and such from my IDE.

def read_items(params: Search_Params):
    where_conditions, table = compile_where_conditions(params)
    with sql.Session(sql.engine) as session:
        # query the database for info, then return info
        statement = sql.select(table).where(*where_conditions)
        results = session.execute(statement)
        requested_items = results.all()
        # get the results of the execute() as a dictionary list
        requested_items = [item._mapping for item in requested_items]
        return requested_items
    
def compile_where_conditions(params: Search_Params):
    # very long isolation of the table's name
    table_name = str(params).split('.')[1].split('(')[0]
    table = getattr(sql, table_name) # to get Table object so that I don't have to make separate functions for each table

    # assemble conditions into a list to unpack into a command in read_items
    param_dict = vars(params)
    where_conditions = []
    for k, v in param_dict.items():
        # prevent searching for Nones
        if v != None:
            where_conditions.append(getattr(table.c, k) == v)
    return where_conditions, table

