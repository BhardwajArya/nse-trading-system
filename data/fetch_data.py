import yfinance as yf
import pandas as pd

NIFTY_50 = [
    "ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","ASIANPAINT.NS",
    "AXISBANK.NS","BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS",
    "BPCL.NS","BHARTIARTL.NS","BRITANNIA.NS","CIPLA.NS",
    "COALINDIA.NS","DIVISLAB.NS","DRREDDY.NS","EICHERMOT.NS",
    "GRASIM.NS","HCLTECH.NS","HDFCBANK.NS","HDFCLIFE.NS",
    "HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS","ICICIBANK.NS",
    "ITC.NS","INDUSINDBK.NS","INFY.NS","JSWSTEEL.NS",
    "KOTAKBANK.NS","LT.NS","M&M.NS","MARUTI.NS",
    "NTPC.NS","NESTLEIND.NS","ONGC.NS","POWERGRID.NS",
    "RELIANCE.NS","SBILIFE.NS","SBIN.NS","SUNPHARMA.NS",
    "TCS.NS","TATACONSUM.NS","TATAMOTORS.NS","TATASTEEL.NS",
    "TECHM.NS","TITAN.NS","ULTRACEMCO.NS","UPL.NS","WIPRO.NS"
]

EXTRA_NSE = [
    "DMART.NS","IRCTC.NS","ZOMATO.NS","PAYTM.NS","NYKAA.NS",
    "POLYCAB.NS","DIXON.NS","VOLTAS.NS","PIDILITIND.NS","BERGEPAINT.NS",
    "CDSL.NS","BSE.NS","HAL.NS","BEL.NS","MAZDOCK.NS",
    "COCHINSHIP.NS","TATAPOWER.NS","VEDL.NS","JUBLFOOD.NS","TRENT.NS"
]


def load_bse_from_csv():
    try:
        df = pd.read_csv("bse_companies.csv")
        return df["Symbol"].dropna().astype(str).tolist()
    except Exception as e:
        print(f"Could not load bse_companies.csv: {e}")
        return []


def fetch_stock_data(symbol, period="2mo", interval="1d"):
    try:
        print(f"\nFetching {symbol} past {period} data...")

        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            progress=False
        )

        if df.empty:
            print(f"No data found for {symbol}")
            return None

        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()
        df["Symbol"] = symbol

        print(f"Fetched {symbol}: {len(df)} rows")
        return df

    except Exception as e:
        print(f"ERROR fetching {symbol}: {e}")
        return None


def get_stock_list(category):
    bse_stocks = load_bse_from_csv()

    if category == "1":
        return NIFTY_50

    if category == "2":
        return EXTRA_NSE

    if category == "3":
        return bse_stocks

    return []
if __name__ == "__main__":
    from data.db import save_to_db

    all_symbols = NIFTY_50 + EXTRA_NSE

    for symbol in all_symbols:
        df = fetch_stock_data(symbol, period="2y", interval="1d")
        if df is not None:
            save_to_db(symbol, df)

    print("\nAll stocks fetched and saved to MongoDB.")