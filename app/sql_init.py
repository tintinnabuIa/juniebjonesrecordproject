from typing import Annotated
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, MetaData, Table, inspect, Relationship, and_

# for grabbing data for DB
psql_conf = Path(__file__).parent.parent / "discogs-xml2db/postgresql" / "postgresql.conf"
with open(psql_conf, "rt", encoding="utf-8") as conf:
    user, password = "user", "password"
    for line in conf:
        index = line.find("user")
        if index != -1:
            user = line[len(user)+1:-1] # -1 to stop from grabbing \n
            pass

        index = line.find("password")
        if index != -1:
            password = line[len(password)+1:-1]
            pass

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:5432/discogs", echo=False)

# make schemas from the sql database tables
metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)
for table in metadata_obj.tables:
    # adding to globals so that they can be imported in other files
    globals()[table.title()] = metadata_obj.tables[table] 
