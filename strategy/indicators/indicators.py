import pandas as pd
import numpy as np


def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()


def compute_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def compute_macd(df):
    ema12 = ema(df['Close'], 12)
    ema26 = ema(df['Close'], 26)
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal


def compute_adx(df, period=14):
    high = df['High']
    low = df['Low']
    close = df['Close']

    plus_dm = high.diff()
    minus_dm = -low.diff()

    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
    minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()
    plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(period).mean()

    if isinstance(adx, pd.DataFrame):
        adx = adx.iloc[:, 0]

    return adx


def add_indicators(df):
    df = df.copy()

    # Ensure Date is a column not index
    if 'Date' not in df.columns:
        df = df.reset_index()

    # Ensure Close is a flat Series
    if isinstance(df['Close'], pd.DataFrame):
        df['Close'] = df['Close'].iloc[:, 0]

    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')

    df['ema_9'] = ema(df['Close'], 9)
    df['ema_21'] = ema(df['Close'], 21)
    df['ema_50'] = ema(df['Close'], 50)
    df['ema_200'] = ema(df['Close'], 200)

    df['rsi'] = compute_rsi(df)

    macd, signal = compute_macd(df)
    df['macd'] = macd
    df['macd_signal'] = signal

    df['adx'] = compute_adx(df)

    return df