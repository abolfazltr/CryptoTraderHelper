import pandas as pd
import requests

EMA_SHORT = 10
EMA_LONG = 21
SUPERTREND_PERIOD = 10
SUPERTREND_MULTIPLIER = 3

def fetch_ohlc_coingecko(symbol):
    coingecko_ids = {
        "eth": "ethereum",
        "link": "chainlink"
    }

    token_id = coingecko_ids.get(symbol.lower())
    if not token_id:
        print("❌ توکن پشتیبانی نمی‌شود.")
        return None

    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/ohlc?vs_currency=usd&days=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print(f"❌ خطا در دریافت کندل {symbol.upper()}: {response.text}")
        return None

    raw = response.json()
    df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close"])
    return df

def ema_signal(df):
    df["ema_short"] = df["close"].ewm(span=EMA_SHORT).mean()
    df["ema_long"] = df["close"].ewm(span=EMA_LONG).mean()

    if df["ema_short"].iloc[-2] < df["ema_long"].iloc[-2] and df["ema_short"].iloc[-1] > df["ema_long"].iloc[-1]:
        return "long"
    elif df["ema_short"].iloc[-2] > df["ema_long"].iloc[-2] and df["ema_short"].iloc[-1] < df["ema_long"].iloc[-1]:
        return "short"
    return None

def calculate_supertrend(df, period=SUPERTREND_PERIOD, multiplier=SUPERTREND_MULTIPLIER):
    hl2 = (df["high"] + df["low"]) / 2
    atr = df["high"].rolling(period).max() - df["low"].rolling(period).min()
    atr = atr.ewm(span=period, adjust=False).mean()

    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    supertrend = [True] * len(df)
    for i in range(1, len(df)):
        prev_close = df["close"].iloc[i - 1]
        if prev_close <= upperband.iloc[i - 1]:
            supertrend[i] = True
        else:
            supertrend[i] = False

    df["supertrend"] = supertrend
    return df

def analyze_token(token):
    df = fetch_ohlc_coingecko(token)
    if df is None or df.empty:
        print("❌ کندل‌داده‌ها دریافت نشد.")
        return None

    df = calculate_supertrend(df)
    st_signal = "long" if df["supertrend"].iloc[-1] else "short"
    ema_sig = ema_signal(df)

    # چاپ وضعیت دقیق
    print(f"📈 EMA short: {df['ema_short'].iloc[-1]:.2f}")
    print(f"📉 EMA long: {df['ema_long'].iloc[-1]:.2f}")
    print(f"🟢 Supertrend وضعیت: {'LONG' if st_signal == 'long' else 'SHORT'}")
    print(f"🔍 EMA signal: {ema_sig}")

    if ema_sig == st_signal:
        print(f"✅ تحلیل نهایی: ورود به پوزیشن {ema_sig.upper()}")
        return ema_sig
    else:
        print("❌ هیچ سیگنال معتبری صادر نشده.")
        return None