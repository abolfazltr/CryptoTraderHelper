import pandas as pd

EMA_SHORT = 10
EMA_LONG = 21
SUPERTREND_PERIOD = 10
SUPERTREND_MULTIPLIER = 3

def calculate_ema(df):
    df["ema_short"] = df["close"].ewm(span=EMA_SHORT, adjust=False).mean()
    df["ema_long"] = df["close"].ewm(span=EMA_LONG, adjust=False).mean()
    return df

def calculate_rsi(df, period=14):
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))
    return df

def calculate_supertrend(df, period=SUPERTREND_PERIOD, multiplier=SUPERTREND_MULTIPLIER):
    hl2 = (df["high"] + df["low"]) / 2
    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - df["close"].shift()).abs()
    tr3 = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()

    upperband = hl2 + multiplier * atr
    lowerband = hl2 - multiplier * atr

    supertrend = [True] * len(df)
    for i in range(1, len(df)):
        if df["close"].iloc[i] > upperband.iloc[i - 1]:
            supertrend[i] = True
        elif df["close"].iloc[i] < lowerband.iloc[i - 1]:
            supertrend[i] = False
        else:
            supertrend[i] = supertrend[i - 1]

    df["supertrend"] = supertrend
    df["upperband"] = upperband
    df["lowerband"] = lowerband
    return df

def analyze_token(df):
    df = calculate_ema(df)
    df = calculate_supertrend(df)
    df = calculate_rsi(df)

    if len(df) < 20:
        print("⚠️ تعداد کندل‌ها کافی نیست.")
        return "none"

    latest = df.iloc[-1]

    # ورود به پوزیشن لانگ
    if (
        latest["supertrend"] == True and
        latest["ema_short"] > latest["ema_long"] and
        latest["close"] > latest["ema_long"] and
        40 <= latest["rsi"] <= 65
    ):
        return "long"

    # ورود به پوزیشن شورت
    elif (
        latest["supertrend"] == False and
        latest["ema_short"] < latest["ema_long"] and
        latest["close"] < latest["ema_long"] and
        35 <= latest["rsi"] <= 60
    ):
        return "short"

    else:
        print("⛔ سیگنال رد شد به دلایل زیر:")
        if not latest["supertrend"]:
            print("❌ Supertrend صعودی نیست")
        if not (latest["ema_short"] > latest["ema_long"]):
            print("❌ EMA کراس صعودی نیست")
        if not (latest["close"] > latest["ema_long"]):
            print("❌ قیمت بالای EMA_LONG نیست")
        if not (40 <= latest["rsi"] <= 65):
            print(f"❌ RSI مناسب نیست: {latest['rsi']:.2f}")
        return "none"