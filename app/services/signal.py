# app/services/signal.py

from app.services.ig_api import fetch_ig_signals
from app.services.ibkr_api import fetch_ibkr_signals
from app.db import SessionLocal
from app.models import Platform

def fetch_signals_by_platform_id(platform_id: int, symbol: str) -> dict:
    db = SessionLocal()
    try:
        platform = db.query(Platform).filter(Platform.id == platform_id).first()
        if not platform:
            return {"error": f"Platform ID {platform_id} not found"}

        platform_type = platform.type.upper()

        if platform_type == "IG":
            return fetch_ig_signals(symbol)
        elif platform_type == "IBKR":
            return fetch_ibkr_signals(symbol)
        else:
            return {"error": f"Unsupported platform type: {platform_type}"}
    finally:
        db.close()
