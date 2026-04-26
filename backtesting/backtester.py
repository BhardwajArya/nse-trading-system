import pandas as pd
from risk.stop_loss import calculate_stop_loss
from risk.position_size import calculate_position_size


def backtest(data, initial_capital=100000):
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

        if pd.isna(row['Close']) or pd.isna(row['decision']):
            continue

        decision = row['decision']
        price = row['Close']

        if decision == "BUY" and position == 0:
            stop_loss_price = calculate_stop_loss(price, "BUY", 0.02)
            quantity = calculate_position_size(capital, 0.02, price, stop_loss_price)

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

        if position > 0:
            stop_loss = calculate_stop_loss(buy_price, "BUY", 0.02)
            target = buy_price * 1.05

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

    total_profit = capital - initial_capital

    return capital, total_profit, trades