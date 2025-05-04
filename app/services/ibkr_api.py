

def fetch_ibkr_signals(ticker: str) -> dict:
    return {'platform': 'IBKR', 'ticker': ticker, 'signal': 'HOLD', 'confidence': None}

def get_ibkr_price(epic: str) -> float:
    print(f'[IBKR API] Fetching price for {epic}')
    return 200.0


from ib_insync import IB, MarketOrder, Stock
import os

def place_ib_order(platform, signal):
    try:
        ib = IB()
        ib_host = os.environ.get("IB_HOST", "127.0.0.1")
        ib_port = int(os.environ.get("IB_PORT", 7497))
        ib_client_id = int(os.environ.get("IB_CLIENT_ID", 1))

        ib.connect(ib_host, ib_port, clientId=ib_client_id)

        symbol = signal["epic"]
        currency = platform.base_currency or "USD"
        exchange = "SMART"

        contract = Stock(symbol, exchange, currency)
        order = MarketOrder("BUY", signal.get("quantity", 1))
        trade = ib.placeOrder(contract, order)

        ib.sleep(1)
        response = {
            "orderId": trade.order.orderId,
            "status": trade.orderStatus.status,
            "filled": trade.orderStatus.filled
        }

        ib.disconnect()
        return {"status": "order placed", "details": response}

    except Exception as e:
        return {"error": "IBKR order failed", "details": str(e)}
