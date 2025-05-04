
import os
import requests
import sys
IG_API_KEY = os.getenv('IG_API_KEY')
IG_USERNAME = os.getenv('IG_USERNAME')
IG_PASSWORD = os.getenv('IG_PASSWORD')
IG_ACCOUNT_TYPE = os.getenv('IG_ACCOUNT_TYPE')
IG_BASE_URL = os.getenv('IG_BASE_URL')
_price_cache = {}
_epic_cache = {}

def get_ig_session():
    headers = {'X-IG-API-KEY': IG_API_KEY, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    payload = {'identifier': IG_USERNAME, 'password': IG_PASSWORD}
    resp = requests.post(f'{IG_BASE_URL}/session', headers=headers, json=payload)
    if (resp.status_code != 200):
        raise Exception('Failed to authenticate with IG')
    cst = resp.headers.get('CST')
    x_security_token = resp.headers.get('X-SECURITY-TOKEN')
    return (cst, x_security_token)

def get_epic_for_symbol(symbol: str, cst: str, xst: str) -> (str | None):
    if (symbol in _epic_cache):
        return _epic_cache[symbol]
    headers = {'X-IG-API-KEY': IG_API_KEY, 'CST': cst, 'X-SECURITY-TOKEN': xst, 'Accept': 'application/json'}
    resp = requests.get(f'{IG_BASE_URL}/markets?searchTerm={symbol}', headers=headers)
    if (resp.status_code != 200):
        return None
    results = resp.json().get('markets', [])
    if (not results):
        return None
    epic = results[0].get('epic')
    _epic_cache[symbol] = epic
    return epic

def fetch_ig_signals(symbol: str) -> dict:
    (cst, xst) = get_ig_session()
    epic = get_epic_for_symbol(symbol, cst, xst)
    if (not epic):
        return {'error': f"Could not find epic for symbol '{symbol}'"}
    headers = {'X-IG-API-KEY': IG_API_KEY, 'CST': cst, 'X-SECURITY-TOKEN': xst, 'Accept': 'application/json'}
    resp = requests.get(f'{IG_BASE_URL}/markets/{epic}', headers=headers)
    if (resp.status_code != 200):
        return {'error': 'Could not fetch market data'}
    data = resp.json().get('snapshot', {})
    return {'platform': 'IG', 'epic': epic, 'signal': ('BUY' if (data.get('bid') < data.get('offer')) else 'HOLD'), 'confidence': 0.85}

def get_ig_price(epic: str) -> float:
    if (epic in _price_cache):
        return _price_cache[epic]
    (cst, xst) = get_ig_session()
    headers = {'X-IG-API-KEY': IG_API_KEY, 'CST': cst, 'X-SECURITY-TOKEN': xst, 'Accept': 'application/json'}
    resp = requests.get(f'{IG_BASE_URL}/markets/{epic}', headers=headers)
    if (resp.status_code != 200):
        raise Exception(f"Failed to fetch IG market data for epic '{epic}' – {resp.status_code} {resp.text}")
    snapshot = resp.json().get('snapshot', {})
    bid = snapshot.get('bid')
    offer = snapshot.get('offer')
    if ((bid is not None) and (offer is not None)):
        price = ((bid + offer) / 2)
    elif (snapshot.get('lastPrice', {}).get('bid') is not None):
        price = snapshot['lastPrice']['bid']
    else:
        raise Exception(f"No valid price data returned for epic '{epic}'")
    _price_cache[epic] = price
    return price
if (__name__ == '__main__'):
    if (len(sys.argv) < 2):
        print('Usage: python ig_api.py <EPIC>')
        sys.exit(1)
    epic = sys.argv[1]
    try:
        price = get_ig_price(epic)
        print(f'Live price for {epic}: {price}')
    except Exception as e:
        print(f'Error: {e}')


import os
import requests
import pandas as pd
from datetime import datetime

def fetch_historical_data(epic, start_date, end_date, resolution='DAY'):
    IG_API_KEY = os.environ.get("IG_API_KEY")
    IG_USERNAME = os.environ.get("IG_USERNAME")
    IG_PASSWORD = os.environ.get("IG_PASSWORD")
    IG_ACCOUNT_ID = os.environ.get("IG_ACCOUNT_ID")
    IG_ENV = os.environ.get("IG_ENV", "DEMO").upper()

    BASE_URL = "https://demo-api.ig.com/gateway/deal" if IG_ENV == "DEMO" else "https://api.ig.com/gateway/deal"

    # Authenticate
    session = requests.Session()
    session.headers.update({
        'X-IG-API-KEY': IG_API_KEY,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8'
    })

    auth_response = session.post(
        f"{BASE_URL}/session",
        json={"identifier": IG_USERNAME, "password": IG_PASSWORD}
    )
    
    if auth_response.status_code != 200:
        print("IG login failed:", auth_response.text)
        return None

    cst = auth_response.headers.get("CST")
    x_sec_token = auth_response.headers.get("X-SECURITY-TOKEN")

    session.headers.update({
        "CST": cst,
        "X-SECURITY-TOKEN": x_sec_token
    })

    params = {
        "resolution": resolution,
        "from": start_date,
        "to": end_date,
        "pageSize": 1000
    }

    price_url = f"{BASE_URL}/prices/{epic}"
    response = session.get(price_url, params=params)

    if response.status_code != 200:
        print("Failed to fetch historical data:", response.text)
        return None

    prices = response.json().get("prices", [])
    records = []
    for p in prices:
        records.append({
            "timestamp": p["snapshotTime"],
            "open": p["openPrice"]["ask"],
            "high": p["highPrice"]["ask"],
            "low": p["lowPrice"]["ask"],
            "close": p["closePrice"]["ask"]
        })

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def place_ig_order(platform, signal):
    IG_API_KEY = os.environ.get("IG_API_KEY")
    IG_USERNAME = os.environ.get("IG_USERNAME")
    IG_PASSWORD = os.environ.get("IG_PASSWORD")
    IG_ACCOUNT_ID = os.environ.get("IG_ACCOUNT_ID")
    IG_ENV = os.environ.get("IG_ENV", "DEMO").upper()

    BASE_URL = "https://demo-api.ig.com/gateway/deal" if IG_ENV == "DEMO" else "https://api.ig.com/gateway/deal"

    session = requests.Session()
    session.headers.update({
        'X-IG-API-KEY': IG_API_KEY,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8'
    })

    auth_response = session.post(
        f"{BASE_URL}/session",
        json={"identifier": IG_USERNAME, "password": IG_PASSWORD}
    )

    if auth_response.status_code != 200:
        return {"error": "IG login failed", "details": auth_response.text}

    cst = auth_response.headers.get("CST")
    x_sec_token = auth_response.headers.get("X-SECURITY-TOKEN")

    session.headers.update({
        "CST": cst,
        "X-SECURITY-TOKEN": x_sec_token
    })

    # Prepare order
    order_data = {
        "epic": signal["epic"],
        "expiry": "DFB",
        "direction": "BUY",
        "size": signal.get("size", 1),
        "orderType": "MARKET",
        "currencyCode": platform.base_currency or "GBP",
        "forceOpen": True,
        "guaranteedStop": False,
        "stopLevel": signal.get("sl"),
        "limitLevel": signal.get("tp")
    }

    response = session.post(
        f"{BASE_URL}/positions/otc",
        json=order_data
    )

    if response.status_code != 200:
        return {"error": "Order placement failed", "details": response.text}

    return {"status": "order placed", "response": response.json()}
