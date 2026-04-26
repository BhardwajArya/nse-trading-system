import os
import pandas as pd
import datetime

LOG_DIR = "logs"


def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def log_trade(trade):
    ensure_log_dir()

    file_path = os.path.join(LOG_DIR, "trades.csv")

    trade["LoggedAt"] = datetime.datetime.now()

    df = pd.DataFrame([trade])

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode="a", header=False, index=False)

    print("[LOG] Trade saved")


def log_decision(row):
    ensure_log_dir()

    file_path = os.path.join(LOG_DIR, "decisions.csv")

    decision_data = {
        "LoggedAt": datetime.datetime.now(),
        "Date": row.get("Date", row.name),
        "Symbol": row.get("Symbol", None),
        "Close": row.get("Close", None),
        "Decision": row.get("decision", None),
        "Score": row.get("score", None)
    }

    df = pd.DataFrame([decision_data])

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode="a", header=False, index=False)

    print("[LOG] Decision saved")