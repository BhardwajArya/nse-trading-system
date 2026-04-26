from strategy.ml_model.model import predict_proba


def calculate_score(df):
    scores = []

    for i in range(len(df)):
        row = df.iloc[i]
        score = 0

        # 1. TREND
        if row['ema_50'] > row['ema_200']:
            score += 0.4
        else:
            score -= 0.4

        # 2. MACD with zero-line
        if row['macd'] > row['macd_signal'] and row['macd'] > 0:
            score += 0.25
        elif row['macd'] < row['macd_signal'] and row['macd'] < 0:
            score -= 0.25

        # 3. RSI tightened
        if 60 < row['rsi'] <= 70:
            score += 0.2
        elif 30 <= row['rsi'] < 40:
            score -= 0.2
        elif row['rsi'] > 70:
            score -= 0.05
        elif row['rsi'] < 30:
            score += 0.05

        # 4. SIGNAL BOOST
        score += 0.15 * row['signal']

        # 5. ADX confidence
        if row['adx'] > 25:
            score *= 1.2
        elif row['adx'] < 25:
            score *= 0.5

        scores.append(score)

    df['score'] = scores

    # 6. BLEND WITH ML (60% rule, 40% ML)
    try:
        ml_proba = predict_proba(df)          # 0→1 bullish probability
        ml_score = ml_proba * 2 - 1           # scale to -1→1
        df['score'] = 0.6 * df['score'] + 0.4 * ml_score
    except FileNotFoundError as e:
        print(f"[WARNING] ML model not found, using rule-based score only. {e}")

    return df