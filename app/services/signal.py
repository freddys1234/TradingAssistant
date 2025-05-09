
from app.services.ig_api import fetch_ig_signals
from app.services.ibkr_api import fetch_ibkr_signals
from app.db import SessionLocal
from app.models import Platform
from app.services.db_utils import get_platform_by_id
from app.services.ig_api import get_ig_price
from app.services.ibkr_api import get_ibkr_price

def fetch_signals_by_platform_id(platform_id: int, symbol: str) -> dict:
    db = SessionLocal()
    try:
        platform = db.query(Platform).filter((Platform.id == platform_id)).first()
        if (not platform):
            return {'error': f'Platform ID {platform_id} not found'}
        platform_type = platform.type.upper()
        if (platform_type == 'IG'):
            return fetch_ig_signals(symbol)
        elif (platform_type == 'IBKR'):
            return fetch_ibkr_signals(symbol)
        else:
            return {'error': f'Unsupported platform type: {platform_type}'}
    finally:
        db.close()
_price_cache = {}

def fetch_current_price(epic: str, platform_id: int) -> float:
    cache_key = f'{epic}_{platform_id}'
    if (cache_key in _price_cache):
        return _price_cache[cache_key]
    platform = get_platform_by_id(platform_id)
    if (not platform):
        raise ValueError(f'Platform with ID {platform_id} not found.')
    platform_type = platform.name.lower()
    if ('ig' in platform_type):
        price = get_ig_price(epic)
    elif ('ibkr' in platform_type):
        price = get_ibkr_price(epic)
    else:
        raise ValueError(f'Unsupported platform: {platform.name}')
    _price_cache[cache_key] = price
    return price
