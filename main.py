import yfinance as yf
import pandas as pd

from strategy.indicators.indicators import add_indicators
from strategy.signals.signals import generate_signals
from strategy.scoring.scoring import calculate_score

from backtesting.backtester import backtest
from execution.executor import execute_trade
from logs.logger import log_decision


def run(symbol="RELIANCE.NS"):
    print(f"Fetching data for {symbol}...")

    df = yf.download(symbol, period="6mo", interval="1d")

    # Fix multi-index issue
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if df.empty:
        print("No data fetched. Check symbol or internet.")
        return

    print("Adding indicators...")
    df = add_indicators(df)

    print("Generating signals...")
    df = generate_signals(df)

    print("Calculating score...")
    df = calculate_score(df)

    # --- DECISION FUNCTION ---
    def decision(score):
        if score > 0.5:
            return "BUY"
        elif score < -0.5:
            return "SELL"
        else:
            return "HOLD"

    df['decision'] = df['score'].apply(decision)

    print("\nLatest Signals:")
    print(df[['Close', 'score', 'decision']].tail())

    # =========================
    # 🔵 LOG LATEST DECISION
    # =========================
    latest_row = df.iloc[-1]
    log_decision(latest_row)

    # =========================
    # 🔵 BACKTEST
    # =========================
    print("\nRunning Backtest...")

    final_capital, total_profit, trades = backtest(df)

    print("\nBacktest Results:")
    print("Final Capital:", final_capital)
    print("Total Profit:", total_profit)
    print("Number of Trades:", len(trades))

    print("\nSample Trades:")
    for trade in trades[:5]:
        print(trade)

    # =========================
    # 🔵 EXECUTION (LIVE DECISION)
    # =========================
    print("\nExecuting latest trade...")

    decision_value = latest_row['decision']
    price = latest_row['Close']

    capital = 100000  # You can later make this dynamic
    quantity = capital // price

    execute_trade(symbol, decision_value, quantity, price)


if __name__ == "__main__":
    run()