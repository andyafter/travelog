""" db stuff """

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import closing
import sqlite3
from travelog import config

Base = declarative_base()
engine = create_engine(config.DATABASEURI)
metadata = MetaData(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

class Photo(Base):
    __table__ = Table('photos', metadata, autoload=True)

class Tag(Base):
    __table__ = Table('tags', metadata, autoload=True)
    
class PhotoTag(Base):
    __table__ = Table('phototag', metadata, autoload=True)
    
def connect_db():
    db = sqlite3.connect(config.DATABASE)
    db.cursor().executescript("PRAGMA foreign_keys = ON;") # should implement delete-cascade but doesn't
    return db
    
def init_db(schema_file='./schema.sql'):
    with closing(connect_db()) as db:
        with open(schema_file, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
def init_test_db():
    init_db('./test_schema.sql')
