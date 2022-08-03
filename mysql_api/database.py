from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = 'root'
PASSWORD = 'root'
DATABASE = 'gestor_asignaturas'

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{USER}:{PASSWORD}@localhost/{DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
