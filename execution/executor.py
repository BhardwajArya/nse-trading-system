from logs.logger import log_trade
from risk.stop_loss import calculate_stop_loss
from risk.position_size import calculate_position_size
import datetime


def execute_trade(symbol, decision, price, capital=100000, risk_percent=0.02):
    if decision not in ["BUY", "SELL", "HOLD"]:
        print("[ERROR] Invalid decision")
        return

    if decision == "HOLD":
        print(f"[EXECUTION] HOLD {symbol} - No trade")
        return

    stop_loss = calculate_stop_loss(price, decision, 0.02)

    quantity = calculate_position_size(
        capital=capital,
        risk_percent=risk_percent,
        entry_price=price,
        stop_loss=stop_loss
    )

    if quantity <= 0:
        print("[ERROR] Quantity must be > 0")
        return

    print(f"[EXECUTION] {decision} {quantity} of {symbol} at {price}")
    print(f"[RISK] Stop Loss: {stop_loss}")

    trade = {
        "Time": datetime.datetime.now(),
        "Symbol": symbol,
        "Type": decision,
        "Price": price,
        "Quantity": quantity,
        "StopLoss": stop_loss,
        "Capital": capital,
        "RiskPercent": risk_percent
    }

    log_trade(trade)