try: import sql_init as sql
except: from . import sql_init as sql
from dataclasses import dataclass, is_dataclass, asdict
from functools import cache

# search parameter dataclasses so that each read_x isn't super long; also, more fun
# using the major tables---the stems---because they're the most useful ones
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
    # convert superclass to dict as to loop through for no if statements in main.py /api/post
    for class_item in vars(superclass).values():
        if is_dataclass(class_item):
            class_dict[class_item.__name__] = class_item
    return class_dict


def read_items(params: Search_Params):
    where_conditions, table = compile_where_conditions(params)
    with sql.Session(sql.engine) as session:
        # query the database for info, then return for display
        statement = sql.select(table).where(*where_conditions)
        results = session.execute(statement)
        requested_items = results.all()
        requested_items = [item._mapping for item in requested_items]
        return requested_items
    
def compile_where_conditions(params: Search_Params):
    # very long isolation of the table's name, but at least not hardcoded 
    table_name = str(params).split('.')[1].split('(')[0]
    table = getattr(sql, table_name) # to get Table object so that I don't have to make separate functions for each table

    # assemble conditions into a list to unpack into a command later
    param_dict = vars(params)
    where_conditions = []
    for k, v in param_dict.items():
        if v != None:
            where_conditions.append(getattr(table.c, k) == v)
    return where_conditions, table

