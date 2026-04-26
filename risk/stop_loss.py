def calculate_stop_loss(entry_price, direction="BUY", percent=0.02):
    """
    entry_price: trade entry price
    direction: BUY or SELL
    percent: stop loss percentage, 0.02 = 2%
    """

    if direction == "BUY":
        return entry_price * (1 - percent)

    if direction == "SELL":
        return entry_price * (1 + percent)

    return entry_price