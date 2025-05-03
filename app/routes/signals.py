# app/routes/signals.py

from fastapi import APIRouter, Query
from app.services.signal import fetch_signals

router = APIRouter()

@router.get("/")
def get_signal(platform: str = Query(...), identifier: str = Query(...)):
    return fetch_signals(platform, identifier)
