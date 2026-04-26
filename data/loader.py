from pymongo import MongoClient
import pandas as pd

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "nse_trading_system"


def get_collection_name(symbol):
    return symbol.replace(".", "_").replace("-", "_").replace("&", "AND")


def load_stock(symbol):
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]

    collection_name = get_collection_name(symbol)
    data = list(db[collection_name].find({}, {"_id": 0}))

    client.close()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)