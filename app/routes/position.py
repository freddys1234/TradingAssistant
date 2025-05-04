
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Position, Platform
from app.services.strategy import StrategyEngine
from app.services.signal import get_current_price
router = APIRouter()

@router.get('/positions/{position_id}/evaluate')
def evaluate_position(position_id: int, db: Session=Depends(get_db)):
    position = db.query(Position).filter((Position.id == position_id)).first()
    if (not position):
        raise HTTPException(status_code=404, detail='Position not found')
    platform = db.query(Platform).filter((Platform.id == position.platform_id)).first()
    if (not platform):
        raise HTTPException(status_code=404, detail='Platform not found')
    current_price = get_current_price(platform.epic)
    strategy = StrategyEngine(position, current_price, platform.trading_fee)
    (signal, reason, pl) = strategy.evaluate()
    return {'signal': signal, 'reason': reason, 'profit_loss': pl}
