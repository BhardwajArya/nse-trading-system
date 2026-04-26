from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "nse_trading_system"


def get_collection_name(symbol):
    return symbol.replace(".", "_").replace("-", "_").replace("&", "AND")


def save_to_db(symbol, df):
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]

    collection_name = get_collection_name(symbol)

    records = df.to_dict("records")

    db[collection_name].delete_many({})
    db[collection_name].insert_many(records)

    client.close()

    print(f"Saved {symbol} to MongoDB collection: {collection_name}")