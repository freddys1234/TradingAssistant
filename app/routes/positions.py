
from fastapi import APIRouter, HTTPException
from app.db import SessionLocal
from app.models import Position, Platform
from app.services.signal import evaluate_ig_spread_position
from app.services.ig_api import get_ig_price
router = APIRouter()

@router.get('/positions/{position_id}/evaluate')
def evaluate_position(position_id: int):
    db = SessionLocal()
    try:
        position = db.query(Position).filter((Position.id == position_id)).first()
        if (not position):
            raise HTTPException(status_code=404, detail='Position not found')
        platform = db.query(Platform).filter((Platform.id == position.platform_id)).first()
        if (not platform):
            raise HTTPException(status_code=404, detail='Platform not found')
        if (platform.type.upper() != 'IG'):
            raise HTTPException(status_code=400, detail='Only IG spread betting supported in this test route')
        price = get_ig_price(position.symbol)
        fee = (platform.fee or 0.0)
        result = evaluate_ig_spread_position(position, price, fee)
        return result
    finally:
        db.close()
