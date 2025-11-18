# holds all connection strings to be able to be connected to mysql
# creates the engine, creates a session factory, holds my base class

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://blog_user:password@localhost:3306/simple_blog_platform'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()