import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os


MODEL_PATH = "strategy/ml_model/model.pkl"


# -----------------------------
# FEATURES
# -----------------------------
def build_features(df):
    X = pd.DataFrame()
    X['rsi'] = df['rsi']
    X['macd'] = df['macd']
    X['macd_signal'] = df['macd_signal']
    X['macd_diff'] = df['macd'] - df['macd_signal']
    X['adx'] = df['adx']
    X['ema_ratio_9_21'] = df['ema_9'] / df['ema_21']
    X['ema_ratio_50_200'] = df['ema_50'] / df['ema_200']
    X['close_vs_ema200'] = df['Close'] / df['ema_200']
    return X


# -----------------------------
# LABELS
# -----------------------------
def build_labels(df, threshold=0.005):
    future_return = df['Close'].shift(-1) / df['Close'] - 1
    return (future_return > threshold).astype(int)


# -----------------------------
# TRAIN ON ALL MONGO STOCKS
# -----------------------------
def train_model(save_path=MODEL_PATH):
    from data.loader import load_stock
    from data.fetch_data import NIFTY_50, EXTRA_NSE
    from strategy.indicators.indicators import add_indicators
    from strategy.signals.signals import generate_signals

    all_symbols = NIFTY_50 + EXTRA_NSE
    all_X = []
    all_y = []

    for symbol in all_symbols:
        try:
            df = load_stock(symbol)
            if df.empty:
                print(f"Skipping {symbol} — no data in MongoDB")
                continue

            df = add_indicators(df)
            df = generate_signals(df)

            X = build_features(df)
            y = build_labels(df)

            X = X.iloc[:-1]
            y = y.iloc[:-1]

            mask = X.notna().all(axis=1) & y.notna()
            X, y = X[mask], y[mask]

            all_X.append(X)
            all_y.append(y)
            print(f"Loaded {symbol}: {len(X)} rows")

        except Exception as e:
            print(f"ERROR on {symbol}: {e}")

    if not all_X:
        print("No data loaded. Run fetch_data first.")
        return None

    X_all = pd.concat(all_X, ignore_index=True)
    y_all = pd.concat(all_y, ignore_index=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X_all, y_all, test_size=0.2, shuffle=False
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        eval_metric='logloss',
        random_state=42
    )

    model.fit(X_train, y_train)

    print("\nModel Evaluation:")
    print(classification_report(y_test, model.predict(X_test)))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model, save_path)
    print(f"Model saved to {save_path}")

    return model


# -----------------------------
# PREDICT
# -----------------------------
def predict_proba(df, model_path=MODEL_PATH):
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"No model at {model_path}. Run: python -m strategy.ml_model.model"
        )

    model = joblib.load(model_path)
    X = build_features(df).fillna(0)
    return model.predict_proba(X)[:, 1]


# -----------------------------
# MAIN — train mode
# -----------------------------
if __name__ == "__main__":
    train_model()