import os
import pandas as pd


LOG_DIR = "logs"


def ensure_log_dir():
    """
    Create logs directory if it doesn't exist
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def log_trade(trade):
    """
    Save trade to trades.csv
    """

    ensure_log_dir()

    file_path = os.path.join(LOG_DIR, "trades.csv")

    df = pd.DataFrame([trade])

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)


def log_decision(row):
    """
    Save decision to decisions.csv
    """

    ensure_log_dir()

    file_path = os.path.join(LOG_DIR, "decisions.csv")

    df = pd.DataFrame([{
        "Date": row.name,
        "Close": row['Close'],
        "Decision": row['decision'],
        "Score": row.get('score', None)
    }])

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False) 