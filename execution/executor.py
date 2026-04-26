from logs.logger import log_trade
import datetime


def execute_trade(symbol, decision, quantity, price):
    """
    Execute trade (simulation + logging)
    """

    # --- SAFETY CHECKS ---
    if decision not in ["BUY", "SELL", "HOLD"]:
        print("[ERROR] Invalid decision")
        return

    if quantity <= 0:
        print("[ERROR] Quantity must be > 0")
        return

    # --- HOLD CASE ---
    if decision == "HOLD":
        print("[EXECUTION] HOLD - No trade")
        return

    # --- EXECUTION ---
    print(f"[EXECUTION] {decision} {quantity} of {symbol} at {price}")

    # --- CREATE TRADE OBJECT ---
    trade = {
        "Time": datetime.datetime.now(),
        "Symbol": symbol,
        "Type": decision,
        "Price": price,
        "Quantity": quantity
    }

    # --- LOG TRADE ---
    log_trade(trade)