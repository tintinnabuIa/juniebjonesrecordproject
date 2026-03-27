from typing import Annotated
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, MetaData, Table, inspect, Relationship, and_

psql_conf = Path(__file__).parent.parent / "discogs-xml2db/postgresql" / "postgresql.conf"
with open(psql_conf, "rt", encoding="utf-8") as conf:
    name, user, password = "name", "user", "password"
    for line in conf:
        index = line.find("name")
        if index != -1:
            name = line[len(name)+1:]
            pass

        index = line.find("user")
        if index != -1:
            user = line[len(user)+1:]
            pass

        index = line.find("password")
        if index != -1:
            password = line[len(password)+1:]

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:5432/{name}", echo=False)

# make schemas from the sql database tables
metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)
for table in metadata_obj.tables:
    # adding to globals so that they can be imported in other files
    globals()[table.title()] = metadata_obj.tables[table] 
