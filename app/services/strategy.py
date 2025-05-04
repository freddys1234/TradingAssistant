# services/strategy.py

from app.db import get_user_platforms, get_platform_positions  # Adjust if needed
from app.models import Position  # Adjust import to match your structure

def evaluate_position_strategy(position: Position):
    """
    Evaluate strategy for a single position (TP, SL, re-entry).
    Returns one of: HOLD, BUY, SELL, ALERT
    """
    price = fetch_current_price(position.epic, position.platform_id)  # implement separately
    action = "HOLD"

    # Example strategy logic (replace with your own rules)
    if price >= position.take_profit:
        action = "SELL"
    elif price <= position.stop_loss:
        action = "SELL"
    elif price <= position.reentry_price:
        action = "BUY"

    return {
        "epic": position.epic,
        "current_price": price,
        "action": action,
        "tp": position.take_profit,
        "sl": position.stop_loss,
        "reentry": position.reentry_price,
    }

def run_strategy_for_user(user_id):
    """
    Runs strategy checks for all positions across all platforms for the given user.
    Returns a list of evaluated results.
    """
    platforms = get_user_platforms(user_id)
    all_results = []

    for platform in platforms:
        positions = get_platform_positions(platform.id)
        for pos in positions:
            result = evaluate_position_strategy(pos)
            all_results.append(result)

    return all_results

class StrategyEngine:
    def __init__(self, position, current_price, trading_fee):
        self.position = position
        self.current_price = current_price
        self.trading_fee = trading_fee

    def evaluate(self):
        pass  # Logic implemented here


def check_tp_sl(self):
    if self.current_price >= self.position.take_profit:
        return 'SELL', 'Take-Profit reached'
    elif self.current_price <= self.position.stop_loss:
        return 'SELL', 'Stop-Loss triggered'
    return 'HOLD', 'Within TP/SL range'

def check_reentry(self):
    if self.position.status == 'closed':
        if self.current_price <= self.position.reentry_price:
            return 'BUY', 'Re-entry price reached'
    return 'HOLD', 'Re-entry not triggered'

def calculate_pl(self):
    gross_pl = (self.current_price - self.position.entry_price) * self.position.quantity
    net_pl = gross_pl - (2 * self.trading_fee)  # entry and exit fees
    return net_pl

def evaluate(self):
    if self.position.status == 'open':
        signal, reason = self.check_tp_sl()
        pl = self.calculate_pl()
        return signal, reason, pl

    elif self.position.status == 'closed':
        signal, reason = self.check_reentry()
        return signal, reason, 0

    return 'HOLD', 'No action required', 0

