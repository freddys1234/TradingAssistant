from fastapi import APIRouter
from app.services.ig_api import get_ig_price  # ✅ absolute import

router = APIRouter()

@router.get("/test-ig-price/{epic}")
def test_ig_price(epic: str):
    try:
        price = get_ig_price(epic)
        return {"epic": epic, "price": price}
    except Exception as e:
        return {"error": str(e)}
