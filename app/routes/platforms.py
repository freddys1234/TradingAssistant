
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Platform
router = APIRouter()

class PlatformCreate(BaseModel):
    name: str
    type: str
    currency: str
    fee: float

@router.post('/platforms/{user_id}')
def create_platform(user_id: int, platform: PlatformCreate, db: Session=Depends(get_db)):
    new_platform = Platform(user_id=user_id, name=platform.name, platform_type=platform.type, base_currency=platform.currency, trading_fee=platform.fee)
    db.add(new_platform)
    db.commit()
    db.refresh(new_platform)
    return new_platform
