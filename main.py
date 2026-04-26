import yfinance as yf
import pandas as pd
from strategy.indicators.indicators import add_indicators
from strategy.signals.signals import generate_signals
from strategy.scoring.scoring import calculate_score


def run(symbol="RELIANCE.NS"):
    print(f" Fetching data for {symbol}...")

    df = yf.download(symbol, period="6mo", interval="1d")

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

    def decision(score):
        if score > 0.5:
            return "BUY"
        elif score < -0.5:
            return "SELL"
        else:
            return "HOLD"

    df['decision'] = df['score'].apply(decision)

    print("\n Final Output:")
    print(df[['Close', 'rsi', 'signal', 'score', 'decision']].tail())


if __name__ == "__main__":
    run()