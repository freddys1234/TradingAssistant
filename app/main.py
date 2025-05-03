from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db import Base, engine, SessionLocal
from app.routes import signals
from app.models import User, Platform, Position

# --- App Initialization ---
app = FastAPI()  # 👈 MUST come before using `app`

# --- Register Routes ---
app.include_router(signals.router, prefix="/signals")  # 👈 Moved here


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Trading Assistant Backend is Live!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users/")
def create_user(email: str, name: str, db: Session = Depends(get_db)):
    db_user = User(email=email, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/platforms/{user_id}")
def create_platform(user_id: int, name: str, type: str, currency: str, fee: float, daily_budget: float = None, db: Session = Depends(get_db)):
    db_platform = Platform(user_id=user_id, name=name, type=type, currency=currency, fee=fee, daily_budget=daily_budget)
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    return db_platform

@app.post("/positions/{platform_id}")
def create_position(platform_id: int, symbol: str, quantity: float, entry_price: float, take_profit: float, stop_loss: float, reentry_strategy: str, db: Session = Depends(get_db)):
    db_position = Position(platform_id=platform_id, symbol=symbol, quantity=quantity, entry_price=entry_price, take_profit=take_profit, stop_loss=stop_loss, reentry_strategy=reentry_strategy)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

# --- Create DB Schema ---
Base.metadata.create_all(bind=engine)
