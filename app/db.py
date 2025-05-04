# app/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.models import Platform  # You can safely import this here

# --- Database URL ---
DATABASE_URL = os.getenv("DATABASE_URL")

# --- Engine and Session ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Declarative Base ---
Base = declarative_base()

# --- Dependency Injection for FastAPI ---
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Utility Function ---
def get_platform_by_id(platform_id: int) -> Platform | None:
    db: Session = SessionLocal()
    return db.query(Platform).filter(Platform.id == platform_id).first()
