def calculate_position_size(capital, risk_percent, entry_price, stop_loss):
    """
    capital: total capital (e.g. 100000)
    risk_percent: risk per trade (e.g. 0.02 for 2%)
    entry_price: price you enter trade
    stop_loss: stop loss price

    returns: number of shares to buy
    """

    # total money you're willing to lose
    risk_amount = capital * risk_percent

    # risk per share
    risk_per_share = abs(entry_price - stop_loss)

    if risk_per_share == 0:
        return 0

    quantity = risk_amount / risk_per_share

    return max(0, int(quantity))