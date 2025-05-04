# app/services/db_utils.py
from sqlalchemy.orm import Session
from app.models import Platform

def get_platform_by_id(db: Session, platform_id: int) -> Platform | None:
    return db.query(Platform).filter(Platform.id == platform_id).first()
