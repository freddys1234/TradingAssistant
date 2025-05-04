
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import Base, engine, SessionLocal
from app.routes import signals, platforms
from app.models import User, Platform, Position
from app.db import get_db
from app.routes import ig_test
from app.routes import positions
app = FastAPI()
app.include_router(ig_test.router)
app.include_router(positions.router, prefix='/positions')
app.include_router(signals.router, prefix='/signals')
app.include_router(platforms.router)

@app.get('/platforms/')
def list_platforms(db: Session=Depends(get_db)):
    return db.query(Platform).all()

@app.get('/users/')
def list_users(db: Session=Depends(get_db)):
    return db.query(User).all()

@app.get('/')
def root():
    return {'message': 'Trading Assistant Backend is Live!'}

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/run-daily')
def run_daily():
    scheduler.run_daily_strategy_check()
    return {'status': 'done'}

@app.post('/users/')
def create_user(email: str, name: str, db: Session=Depends(get_db)):
    db_user = User(email=email, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get('/positions/')
def list_positions(db: Session=Depends(get_db)):
    return db.query(Position).all()
from pydantic import BaseModel

class PlatformCreate(BaseModel):
    name: str
    type: str
    currency: str
    fee: float
    daily_budget: (float | None) = None

@app.post('/platforms/{user_id}')
def create_platform(user_id: int, platform: PlatformCreate, db: Session=Depends(get_db)):
    db_platform = Platform(user_id=user_id, name=platform.name, type=platform.type, currency=platform.currency, fee=platform.fee, daily_budget=platform.daily_budget)
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    return db_platform

class PositionCreate(BaseModel):
    symbol: str
    quantity: float
    entry_price: float
    take_profit: float
    stop_loss: float
    reentry_strategy: str

@app.post('/positions/{platform_id}')
def create_position(platform_id: int, position: PositionCreate, db: Session=Depends(get_db)):
    db_position = Position(platform_id=platform_id, symbol=position.symbol, quantity=position.quantity, entry_price=position.entry_price, take_profit=position.take_profit, stop_loss=position.stop_loss, reentry_strategy=position.reentry_strategy)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

@app.get('/positions/{position_id}/evaluate')
def evaluate_position(position_id: int, db: Session=Depends(get_db)):
    position = db.query(Position).filter((Position.id == position_id)).first()
    if (not position):
        raise HTTPException(status_code=404, detail='Position not found')
    platform = db.query(Platform).filter((Platform.id == position.platform_id)).first()
    if (not platform):
        raise HTTPException(status_code=404, detail='Platform not found')
    current_price = (position.entry_price + 2.0)
    from app.services.strategy import StrategyEngine
    strategy = StrategyEngine(position, current_price, platform.fee)
    (signal, reason, pl) = strategy.evaluate()
    return {'signal': signal, 'reason': reason, 'profit_loss': pl}
Base.metadata.create_all(bind=engine)
