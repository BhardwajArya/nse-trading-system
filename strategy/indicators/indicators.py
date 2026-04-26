import pandas as pd
import numpy as np


# -----------------------------
# EMA
# -----------------------------
def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()


# -----------------------------
# RSI
# -----------------------------
def compute_rsi(df, period=14):
    delta = df['Close'].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


# -----------------------------
# MACD
# -----------------------------
def compute_macd(df):
    ema12 = ema(df['Close'], 12)
    ema26 = ema(df['Close'], 26)

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    return macd, signal


# -----------------------------
# ADX (FIXED VERSION)
# -----------------------------
def compute_adx(df, period=14):
    high = df['High']
    low = df['Low']
    close = df['Close']

    plus_dm = high.diff()
    minus_dm = -low.diff()

    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
    minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()

    plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(period).mean()

    if isinstance(adx, pd.DataFrame):
        adx = adx.iloc[:, 0]

    return adx

# -----------------------------
# MASTER FUNCTION
# -----------------------------
def add_indicators(df):
    df = df.copy()

    df['ema_9'] = ema(df['Close'], 9)
    df['ema_21'] = ema(df['Close'], 21)
    df['ema_50'] = ema(df['Close'], 50)
    df['ema_200'] = ema(df['Close'], 200)

    df['rsi'] = compute_rsi(df)

    macd, signal = compute_macd(df)
    df['macd'] = macd
    df['macd_signal'] = signal

    df['adx'] = compute_adx(df)   # only once

    return df