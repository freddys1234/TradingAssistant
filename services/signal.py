# services/signal.py

from .ig_api import fetch_ig_signals
from .ibkr_api import fetch_ibkr_signals

def fetch_signals(platform: str, identifier: str) -> dict:
    """
    Routes the request to the appropriate platform fetcher.

    Args:
        platform (str): Platform name, e.g., "IG" or "IBKR"
        identifier (str): Epic (for IG) or Ticker (for IBKR)

    Returns:
        dict: Signal response from the platform
    """
    platform = platform.upper()
    
    if platform == "IG":
        return fetch_ig_signals(identifier)
    elif platform == "IBKR":
        return fetch_ibkr_signals(identifier)
    else:
        return {
            "error": f"Unsupported platform '{platform}'"
        }
