from sqlalchemy import DateTime, Float, create_engine, ForeignKey, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database
from local_settings import postgresql as settings

Base=declarative_base()

#adder methods need some work

def get_engine(user,passwd,host,port,db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
         create_database(url)
    engine=create_engine(url, pool_size=50, echo=False)
    return engine

def get_engine_from_settings():
    keys=['pguser','pgpasswd', 'pghost','pgport', 'pgdb']
    if not all(key in keys for key in settings.keys()):
        raise Exception('Bad Config File')
    return get_engine(settings['pguser'], settings['pgpasswd'], settings['pghost'], settings['pgport'], settings['pgdb'])

def get_session():
    engine=get_engine_from_settings()
    session=sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    return session

session=get_session()
