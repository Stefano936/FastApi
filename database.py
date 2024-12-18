from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a connection to the database
#DATABASE_URL = "mysql+pymysql://root:rootpassword@host.docker.internal:3306/ObligatorioBases"
DATABASE_URL = "mysql+pymysql://root:rootpassword@localhost:3306/ObligatorioBases"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

