import pandas as pd
import requests

EMA_SHORT = 10
EMA_LONG = 21
SUPERTREND_PERIOD = 10
SUPERTREND_MULTIPLIER = 3

def fetch_ohlc_kucoin(symbol="eth", interval="5min"):
    pair_map = {
        "eth": "ETH-USDT",
        "link": "LINK-USDT"
    }

    pair = pair_map.get(symbol.lower())
    if not pair:
        return None

    url = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={pair}"
    res = requests.get(url)
    if res.status_code != 200:
        return None

    raw = res.json()["data"]
    df = pd.DataFrame(raw)[[0,1,2,3,4,5]]
    df.columns = ["timestamp", "open", "close", "high", "low", "volume"]
    df = df[::-1]
    df[["open", "close", "high", "low"]] = df[["open", "close", "high", "low"]].astype(float)
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
    df = fetch_ohlc_kucoin(token)
    if df is None or df.empty:
        print("❌ کندل‌داده‌ها برای تحلیل دریافت نشد.")
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