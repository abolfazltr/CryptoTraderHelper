import pandas as pd
import requests

EMA_SHORT = 10
EMA_LONG = 21
SUPERTREND_PERIOD = 10
SUPERTREND_MULTIPLIER = 3

def fetch_ohlc_data(symbol):
    print(f"⚙️ تلاش برای دریافت کندل برای {symbol.upper()} از CoinGecko...")
    df = fetch_ohlc_coingecko(symbol)
    if df is not None and not df.empty:
        print("✅ دریافت موفق از CoinGecko")
        return df
    else:
        print(f"🌀 CoinGecko شکست خورد. تلاش با Bitget برای {symbol.upper()}...")

        try:
            url = f"https://api.bitget.com/api/mix/v1/market/candles?symbol={symbol.upper()}USDT_UMCBL&granularity=300"
            response = requests.get(url)
            data = response.json()
            raw = data["data"]

            df = pd.DataFrame(raw, columns=[
                "timestamp", "open", "high", "low", "close", "volume", "xx", "yy"
            ])

            df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
            df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)

            print("✅ دریافت موفق از Bitget")
            return df
        except Exception as e:
            print(f"❌ شکست در دریافت کندل از Bitget برای {symbol.upper()}: {e}")
            return None

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
        print(f"❌ استثنا در اتصال به CoinGecko برای {symbol.upper()}: {e}")
        return None

def ema_signal(df):
    df["ema_short"] = df["close"].ewm(span=EMA_SHORT).mean()
    df["ema_long"] = df["close"].ewm(span=EMA_LONG).mean()

    last_ema_short = df["ema_short"].iloc[-2]
    last_ema_long = df["ema_long"].iloc[-2]
    prev_ema_short = df["ema_short"].iloc[-3]
    prev_ema_long = df["ema_long"].iloc[-3]

    if prev_ema_short < prev_ema_long and last_ema_short > last_ema_long:
        return "long"
    elif prev_ema_short > prev_ema_long and last_ema_short < last_ema_long:
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
    print(f"\n🔍 دریافت و تحلیل برای: {token.upper()}")
    df = fetch_ohlc_data(token)
    if df is None or df.empty:
        print("❌ دریافت کندل ناموفق بود.")
        return None

    df = calculate_supertrend(df)
    st_signal = "long" if df["supertrend"].iloc[-2] else "short"

    ema_sig = ema_signal(df)

    print(f"📉 EMA short: {df['ema_short'].iloc[-2]:.2f}")
    print(f"📈 EMA long: {df['ema_long'].iloc[-2]:.2f}")
    print(f"🟢 وضعیت Supertrend: {st_signal.upper()}")
    print(f"🔎 EMA signal: {ema_sig}")

    if ema_sig == st_signal:
        print(f"✅ سیگنال معتبر: {ema_sig.upper()}")
        return ema_sig
    else:
        print("❌ هیچ سیگنال معتبری صادر نشد.")
        return None