
from app.services.ig_api import place_ig_order
from app.services.ibkr_api import place_ib_order
from app.db import SessionLocal
from app.models import Platform, Position
import os

MAX_TRADE_AMOUNT = float(os.environ.get("MAX_TRADE_AMOUNT", 1000))
DAILY_BUDGET = float(os.environ.get("DAILY_BUDGET", 3000))

def route_order(platform_id, signal):
    db = SessionLocal()
    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if not platform:
        return {"error": "Platform not found"}

    platform_type = platform.name.lower()
    price = signal.get("price")
    quantity = signal.get("quantity", 1)

    if (price * quantity) > MAX_TRADE_AMOUNT:
        return {"error": "Trade exceeds max per-trade limit"}

    # TODO: Add daily budget tracking
    result = None
    if "spread" in platform_type:
        result = place_ig_order(platform, signal)
    elif "isa" in platform_type or "cfd" in platform_type:
        result = place_ib_order(platform, signal)
    else:
        return {"error": "Unknown platform type"}

    # Save the executed position
    pos = Position(
        platform_id=platform.id,
        epic=signal.get("epic"),
        entry_price=price,
        quantity=quantity,
        tp_level=signal.get("tp"),
        sl_level=signal.get("sl")
    )
    db.add(pos)
    db.commit()
    return {"status": "order routed", "details": result}
