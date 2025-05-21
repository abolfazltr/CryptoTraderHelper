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
        print("❌ توکن پشتیبانی نمی‌شود:", symbol)
        return None

    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/ohlc?vs_currency=usd&days=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ خطا در دریافت کندل {symbol.upper()}: Status {response.status_code} | {response.text}")
            return None
        raw = response.json()
        df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close"])
        return df
    except Exception as e:
        print(f"❌ استثنا در اتصال CoinGecko برای {symbol.upper()}: {e}")
        return None

def ema_signal(df):
    df["ema_short"] = df["close"].ewm(span=EMA_SHORT).mean()
    df["ema_long"] = df["close"].ewm(span=EMA_LONG).mean()

    if df["ema_short"].iloc[-3] < df["ema_long"].iloc[-3] and df["ema_short"].iloc[-2] > df["ema_long"].iloc[-2]:
        return "long"
    elif df["ema_short"].iloc[-3] > df["ema_long"].iloc[-3] and df["ema_short"].iloc[-2] < df["ema_long"].iloc[-2]:
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
    print("🔍 در حال دریافت کندل‌های CoinGecko...")
    df = fetch_ohlc_coingecko(token)
    if df is None or df.empty:
        print("❌ دریافت کندل ناموفق بود.")
        return None

    df = calculate_supertrend(df)
    st_signal = "long" if df["supertrend"].iloc[-2] else "short"  # تغییر مهم
    ema_sig = ema_signal(df)

    print(f"📈 EMA short: {df['ema_short'].iloc[-2]:.2f}")
    print(f"📉 EMA long: {df['ema_long'].iloc[-2]:.2f}")
    print(f"🟢 Supertrend وضعیت: {st_signal.upper()}")
    print(f"🔍 EMA signal: {ema_sig}")

    if ema_sig == st_signal:
        print(f"✅ سیگنال معتبر: {ema_sig.upper()}")
        return ema_sig
    else:
        print("❌ هیچ سیگنال معتبری صادر نشد.")
        return None