def generate_signals(df):
    assert df.columns.is_unique, f"Duplicate columns found: {df.columns[df.columns.duplicated()].tolist()}"

    signals = []

    for i in range(len(df)):
        row = df.iloc[i]
        signal = 0

        # Trend filter
        if row['Close'] > row['ema_200']:
            trend = 1
        else:
            trend = -1

        # RSI
        if row['rsi'] < 30:
            signal += 1
        elif row['rsi'] > 70:
            signal -= 1

        # EMA crossover
        if row['ema_9'] > row['ema_21']:
            signal += 1
        else:
            signal -= 1

        # MACD
        if row['macd'] > row['macd_signal']:
            signal += 1
        else:
            signal -= 1

        signal = signal * trend

        # ADX filter
        if row['adx'] < 20:
            signal = 0

        signals.append(signal)

    df['signal'] = signals
    return df