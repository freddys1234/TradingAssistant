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

