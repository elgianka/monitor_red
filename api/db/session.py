from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

Base = declarative_base()

# Construct the absolute path to the database file
# Assumes the project root is one level up from the 'api' directory
# and 'api' is one level up from 'db'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATABASE_URL = f"sqlite:///{os.path.join(PROJECT_ROOT, "api", "monitor_ping.db")}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
