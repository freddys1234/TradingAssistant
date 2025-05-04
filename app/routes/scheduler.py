from fastapi import APIRouter
from services.scheduler import run_daily_strategy_check

router = APIRouter()

@router.get("/run-daily")
def run_daily():
    try:
        run_daily_strategy_check()
        return {"status": "completed"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
