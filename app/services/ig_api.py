# app/services/ig_api.py

import os

import requests

IG_API_KEY = os.getenv("IG_API_KEY")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
IG_ACCOUNT_TYPE = os.getenv("IG_ACCOUNT_TYPE")  # or "LIVE"
IG_BASE_URL = os.getenv("IG_BASE_URL")

def get_ig_session():
    headers = {
        "X-IG-API-KEY": IG_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "identifier": IG_USERNAME,
        "password": IG_PASSWORD
    }

    resp = requests.post(
        f"{IG_BASE_URL}/session",
        headers=headers,
        json=payload
    )

    if resp.status_code != 200:
        raise Exception("Failed to authenticate with IG")

    data = resp.json()
    cst = resp.headers.get("CST")
    x_security_token = resp.headers.get("X-SECURITY-TOKEN")

    return cst, x_security_token

def fetch_ig_signals(symbol: str) -> dict:
    cst, xst = get_ig_session()

    epic = get_epic_for_symbol(symbol, cst, xst)
    if not epic:
        return {"error": f"Could not find epic for symbol '{symbol}'"}

    headers = {
        "X-IG-API-KEY": IG_API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": xst,
        "Accept": "application/json"
    }

    resp = requests.get(
        f"{IG_BASE_URL}/markets/{epic}",
        headers=headers
    )

    if resp.status_code != 200:
        return {"error": "Could not fetch market data"}

    data = resp.json().get("snapshot", {})
    return {
        "platform": "IG",
        "epic": epic,
        "signal": "BUY" if data.get("bid") < data.get("offer") else "HOLD",
        "confidence": 0.85
    }

_epic_cache = {}

def get_epic_for_symbol(symbol: str, cst: str, xst: str) -> str | None:
    if symbol in _epic_cache:
        return _epic_cache[symbol]

    headers = {
        "X-IG-API-KEY": IG_API_KEY,
        "CST": cst,
        "X-SECURITY-TOKEN": xst,
        "Accept": "application/json"
    }

    resp = requests.get(
        f"{IG_BASE_URL}/markets?searchTerm={symbol}",
        headers=headers
    )

    if resp.status_code != 200:
        return None

    results = resp.json().get("markets", [])
    if not results:
        return None

    epic = results[0].get("epic")
    _epic_cache[symbol] = epic
    return epic
