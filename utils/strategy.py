import os
import requests
import pandas as pd
from dotenv import load_dotenv

# بارگذاری API Key از .env
load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

EMA_SHORT = 10
EMA_LONG = 21
SUPERTREND_PERIOD = 10
SUPERTREND_MULTIPLIER = 3

def fetch_ohlc_data(symbol):
    symbol_map = {
        "eth": "X:ETHUSD",
        "link": "X:LINKUSD"
    }
    polygon_symbol = symbol_map.get(symbol.lower(), "")
    if not polygon_symbol:
        print(f"❌ نماد ناشناس برای {symbol}")
        return None

    try:
        url = f"https://api.polygon.io/v2/aggs/ticker/{polygon_symbol}/prev?adjusted=true&apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "results" not in data:
            print(f"❌ داده‌ای به نام 'results' برای {symbol.upper()} یافت نشد.")
            print("🔎 پاسخ کامل:", data)
            return None

        raw = data["results"]
        df = pd.DataFrame(raw if isinstance(raw, list) else [raw])
        df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
        df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close"}, inplace=True)
        df = df[["timestamp", "open", "high", "low", "close"]]
        return df

    except Exception as e:
        print(f"❌ خطا در دریافت داده برای {symbol.upper()}: {e}")
        return None

def calculate_supertrend(df, period=SUPERTREND_PERIOD, multiplier=SUPERTREND_MULTIPLIER):
    hl2 = (df["high"] + df["low"]) / 2

    tr = pd.concat([
        df["high"] - df["low"],
        abs(df["high"] - df["close"].shift()),
        abs(df["low"] - df["close"].shift())
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    supertrend = [True] * len(df)
    for i in range(1, len(df)):
        if df["close"].iloc[i] > upperband.iloc[i - 1]:
            supertrend[i] = True
        elif df["close"].iloc[i] < lowerband.iloc[i - 1]:
            supertrend[i] = False
        else:
            supertrend[i] = supertrend[i - 1]

    df["supertrend"] = supertrend
    return df

def analyze_token(token):
    print(f"\n🔍 تحلیل توکن: {token.upper()}")
    df = fetch_ohlc_data(token)
    if df is None or df.empty:
        print("❌ دریافت داده ناموفق بود.")
        return None

    df["ema_short"] = df["close"].ewm(span=EMA_SHORT).mean()
    df["ema_long"] = df["close"].ewm(span=EMA_LONG).mean()
    df = calculate_supertrend(df)

    current_close = df["close"].iloc[-1]
    ema_short = df["ema_short"].iloc[-1]
    ema_long = df["ema_long"].iloc[-1]
    st_trend = df["supertrend"].iloc[-1]

    print(f"📊 قیمت: {current_close:.2f} | EMA10: {ema_short:.2f} | EMA21: {ema_long:.2f}")
    print(f"📈 روند سوپرترند: {'صعودی' if st_trend else 'نزولی'}")

    if st_trend and current_close > ema_short and current_close > ema_long:
        print("✅ سیگنال قوی: LONG")
        return "long"
    elif not st_trend and current_close < ema_short and current_close < ema_long:
        print("✅ سیگنال قوی: SHORT")
        return "short"
    else:
        print("❌ هیچ سیگنال معتبری یافت نشد.")
        return None