def generate_signals(df):
    assert df.columns.is_unique, f"Duplicate columns: {df.columns[df.columns.duplicated()].tolist()}"

    signals = []

    for i in range(len(df)):
        row = df.iloc[i]
        signal = 0

        trend = 1 if row['Close'] > row['ema_200'] else -1

        if row['rsi'] < 30:
            signal += 1
        elif row['rsi'] > 70:
            signal -= 1

        if row['ema_9'] > row['ema_21']:
            signal += 1
        else:
            signal -= 1

        # MACD with zero-line confirmation
        if row['macd'] > row['macd_signal'] and row['macd'] > 0:
            signal += 1
        elif row['macd'] < row['macd_signal'] and row['macd'] < 0:
            signal -= 1

        signal = signal * trend

        # ADX filter raised to 25
        if row['adx'] < 25:
            signal = 0

        signals.append(signal)

    df['signal'] = signals
    return df