import pandas as pd


def backtest(data, initial_capital=100000):
    """
    Robust backtesting engine using decision column
    """

    # --- SAFETY CHECKS ---
    required_cols = ['Close', 'decision']
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    capital = initial_capital
    position = 0
    buy_price = 0

    trades = []

    for i in range(1, len(data)):

        row = data.iloc[i]

        # --- SKIP INVALID DATA ---
        if pd.isna(row['Close']) or pd.isna(row['decision']):
            continue

        decision = row['decision']
        price = row['Close']

        # =========================
        # 🔵 BUY LOGIC
        # =========================
        if decision == "BUY" and position == 0:

            quantity = capital // price

            if quantity > 0:
                buy_price = price
                position = quantity
                capital -= quantity * price

                trades.append({
                    "Type": "BUY",
                    "Price": price,
                    "Quantity": quantity,
                    "Capital": capital,
                    "Index": i
                })

        # =========================
        # 🔵 MANAGE POSITION
        # =========================
        if position > 0:

            stop_loss = buy_price * 0.97   # 3% SL
            target = buy_price * 1.05      # 5% target

            # --- STOP LOSS ---
            if price < stop_loss:
                capital += position * price

                trades.append({
                    "Type": "STOP LOSS",
                    "Price": price,
                    "Quantity": position,
                    "Capital": capital,
                    "Index": i
                })

                position = 0
                continue

            # --- TARGET ---
            if price > target:
                capital += position * price

                trades.append({
                    "Type": "TARGET",
                    "Price": price,
                    "Quantity": position,
                    "Capital": capital,
                    "Index": i
                })

                position = 0
                continue

        # =========================
        # 🔵 SELL LOGIC
        # =========================
        if decision == "SELL" and position > 0:

            profit = (price - buy_price) * position
            capital += position * price

            trades.append({
                "Type": "SELL",
                "Price": price,
                "Quantity": position,
                "Profit": profit,
                "Capital": capital,
                "Index": i
            })

            position = 0

    # =========================
    # 🔵 FINAL RESULTS
    # =========================
    total_profit = capital - initial_capital

    return capital, total_profit, trades