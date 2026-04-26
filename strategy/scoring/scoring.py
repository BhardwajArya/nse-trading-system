def calculate_score(df):
    scores = []

    for i in range(len(df)):
        row = df.iloc[i]
        score = 0

        # -----------------------------
        # 1. TREND (MOST IMPORTANT)
        # -----------------------------
        if row['ema_50'] > row['ema_200']:
            score += 0.4   # bullish structure
        else:
            score -= 0.4   # bearish structure

        # -----------------------------
        # 2. MOMENTUM (MACD)
        # -----------------------------
        if row['macd'] > row['macd_signal']:
            score += 0.25
        else:
            score -= 0.25

        # -----------------------------
        # 3. RSI STRENGTH
        # -----------------------------
        if row['rsi'] > 60:
            score += 0.2
        elif row['rsi'] < 40:
            score -= 0.2

        # -----------------------------
        # 4. SIGNAL BOOST (from signals.py)
        # -----------------------------
        score += 0.15 * row['signal']

        # -----------------------------
        # 5. ADX FILTER (trend strength)
        # -----------------------------
        if row['adx'] > 25:
            score *= 1.2   # strong trend → boost confidence
        elif row['adx'] < 20:
            score *= 0.5   # weak trend → reduce confidence

        scores.append(score)

    df['score'] = scores
    return df