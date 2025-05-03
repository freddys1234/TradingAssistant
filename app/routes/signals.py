from fastapi import APIRouter, Query
from app.services.signal import fetch_signals_by_platform_id

router = APIRouter()

@router.get("/")
def get_signal(platform_id: int = Query(...), symbol: str = Query(...)):
    return fetch_signals_by_platform_id(platform_id, symbol)
