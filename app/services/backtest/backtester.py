
import datetime
import numpy as np
import pandas as pd
from app.services.strategy import evaluate_signal

class Backtester:
    def __init__(self, initial_capital, fetch_data_func, strategy_func, trade_sizing_func):
        self.initial_capital = initial_capital
        self.fetch_data = fetch_data_func
        self.strategy_func = strategy_func
        self.trade_sizing = trade_sizing_func
        self.results = []

    def run(self, epic, start_date, end_date):
        df = self.fetch_data(epic, start_date, end_date)
        if df is None or df.empty:
            print("No historical data fetched.")
            return None

        capital = self.initial_capital
        open_position = None
        history = []

        for index, row in df.iterrows():
            decision = self.strategy_func(row, open_position)
            price = row['close']
            time = row['timestamp']

            if decision == "BUY" and not open_position:
                size = self.trade_sizing(capital, price)
                open_position = {'entry_price': price, 'size': size, 'timestamp': time}

            elif decision == "SELL" and open_position:
                profit = (price - open_position['entry_price']) * open_position['size']
                capital += profit
                history.append({
                    'entry_time': open_position['timestamp'],
                    'exit_time': time,
                    'entry_price': open_position['entry_price'],
                    'exit_price': price,
                    'profit': profit
                })
                open_position = None

        self.results = pd.DataFrame(history)
        self.capital = capital
        return self.results

    def summary(self):
        if self.results.empty:
            return "No trades executed."

        total_return = self.capital - self.initial_capital
        win_rate = (self.results['profit'] > 0).mean()
        max_drawdown = self._calculate_max_drawdown()
        sharpe = self._calculate_sharpe()

        return {
            'final_capital': self.capital,
            'total_return': total_return,
            'win_rate': round(win_rate * 100, 2),
            'max_drawdown': round(max_drawdown, 2),
            'sharpe_ratio': round(sharpe, 2)
        }

    def _calculate_max_drawdown(self):
        equity = self.initial_capital + self.results['profit'].cumsum()
        peak = equity.cummax()
        drawdown = (peak - equity).max()
        return drawdown

    def _calculate_sharpe(self, risk_free_rate=0.01):
        daily_returns = self.results['profit']
        if len(daily_returns) < 2:
            return 0.0
        excess_returns = daily_returns - risk_free_rate / 252
        return excess_returns.mean() / (excess_returns.std() + 1e-8)


# Integration block
from app.services.ig_api import fetch_historical_data
from app.services.strategy import evaluate_signal

def spread_bet_sizing(capital, price, risk_per_trade=0.02):
    # Risk per trade as % of capital
    risk_amount = capital * risk_per_trade
    # Assume 100 point SL for sizing; this should match strategy logic
    stop_distance_points = 100
    stake_per_point = risk_amount / stop_distance_points
    return round(stake_per_point, 2)

def strategy_wrapper(row, open_position):
    # Convert row to dict input for evaluate_signal
    signal = {
        "price": row["close"],
        "high": row["high"],
        "low": row["low"],
        "timestamp": row["timestamp"]
    }
    result = evaluate_signal(signal, open_position)
    return result
