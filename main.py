from data.fetch_data import fetch_stock_data, get_stock_list
from data.db import save_to_db
from data.loader import load_stock

from strategy.indicators.indicators import add_indicators
from strategy.signals.signals import generate_signals
from strategy.scoring.scoring import calculate_score

from backtesting.backtester import backtest
from execution.executor import execute_trade
from logs.logger import log_decision


def choose_stock():
    print("\nChoose stock category:")
    print("1. NIFTY 50")
    print("2. NSE stocks not in NIFTY 50")
    print("3. BSE stocks from CSV")

    category = input("\nEnter category number: ").strip()

    stock_list = get_stock_list(category)

    if not stock_list:
        print("No stocks found for this category.")
        return None

    print("\nAvailable stocks:")
    for i, symbol in enumerate(stock_list, start=1):
        print(f"{i}. {symbol}")

    choice = input("\nEnter stock number or exact symbol: ").strip().upper()

    if choice.isdigit():
        index = int(choice) - 1

        if index < 0 or index >= len(stock_list):
            print("Invalid stock number.")
            return None

        return stock_list[index]

    if category in ["1", "2"] and not choice.endswith(".NS"):
        choice += ".NS"

    if category == "3" and not choice.endswith(".BO"):
        choice += ".BO"

    return choice


def run_strategy(symbol):
    print(f"\nSelected stock: {symbol}")

    df = fetch_stock_data(symbol, period="2mo", interval="1d")

    if df is None:
        print("Cannot run strategy because data was not fetched.")
        return

    save_to_db(symbol, df)

    df = load_stock(symbol)

    if df.empty:
        print("No data found in MongoDB after saving.")
        return

    print("\nPast 2 months data:")
    print(df.tail(10))

    print("\nAdding indicators...")
    df = add_indicators(df)

    print("Generating signals...")
    df = generate_signals(df)

    print("Calculating score...")
    df = calculate_score(df)

    def decision(score):
        if score > 0.5:
            return "BUY"
        elif score < -0.5:
            return "SELL"
        else:
            return "HOLD"

    df["decision"] = df["score"].apply(decision)

    print("\nLatest Signals:")
    print(df[["Date", "Close", "score", "decision"]].tail())

    latest_row = df.iloc[-1]
    log_decision(latest_row)

    print("\nRunning Backtest...")
    final_capital, total_profit, trades = backtest(df)

    print("\nBacktest Results:")
    print("Final Capital:", final_capital)
    print("Total Profit:", total_profit)
    print("Number of Trades:", len(trades))

    print("\nExecuting latest trade...")
    execute_trade(symbol, latest_row["decision"], latest_row["Close"])


if __name__ == "__main__":
    selected_symbol = choose_stock()

    if selected_symbol:
        run_strategy(selected_symbol)1