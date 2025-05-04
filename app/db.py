import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")  # Use env var instead of hardcoding

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db.py

from app.models import Platform
from sqlalchemy.orm import Session
from app.db import SessionLocal  # adjust for your setup

def get_platform_by_id(platform_id: int) -> Platform:
    db: Session = SessionLocal()
    return db.query(Platform).filter(Platform.id == platform_id).first()
