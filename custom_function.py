import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv
load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("host", "")
port = os.getenv("port", 5432)
database_name = os.getenv("database_name")

engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database_name}")

Base = declarative_base()

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
