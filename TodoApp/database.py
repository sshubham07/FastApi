from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Rahul123@localhost/TodoApplicationDatabase'
# FOR SQLITE :-
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})
# For Postgres :-
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

