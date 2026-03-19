from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, MetaData, Table, inspect, Relationship, and_



engine = create_engine("postgresql+psycopg2://bells:bells@localhost:5432/juniebjonesrecordproject", echo=False)

# make schemas from the sql database tables
metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)
for table in metadata_obj.tables:
    # adding to globals so that they can be imported in other files
    globals()[table.title()] = metadata_obj.tables[table] 
