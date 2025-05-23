import pandas as pd

EMA_SHORT = 10
EMA_LONG = 21
SUPERTREND_PERIOD = 10
SUPERTREND_MULTIPLIER = 3

def calculate_ema(df):
    df["ema_short"] = df["close"].ewm(span=EMA_SHORT, adjust=False).mean()
    df["ema_long"] = df["close"].ewm(span=EMA_LONG, adjust=False).mean()
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

    if len(df) < 3:
        print("⚠️ تعداد کندل‌ها کافی نیست.")
        return "none"

    latest = df.iloc[-1]
    previous = df.iloc[-2]
    before = df.iloc[-3]

    # سیگنال لانگ
    if (
        float(before["ema_short"]) < float(before["ema_long"]) and
        float(previous["ema_short"]) < float(previous["ema_long"]) and
        float(latest["ema_short"]) > float(latest["ema_long"]) and
        bool(latest["supertrend"]) and
        float(latest["close"]) > float(latest["ema_long"])
    ):
        return "long"

    # سیگنال شورت
    elif (
        float(before["ema_short"]) > float(before["ema_long"]) and
        float(previous["ema_short"]) > float(previous["ema_long"]) and
        float(latest["ema_short"]) < float(latest["ema_long"]) and
        not bool(latest["supertrend"]) and
        float(latest["close"]) < float(latest["ema_long"])
    ):
        return "short"

    else:
        print("⛔ سیگنال رد شد به دلایل زیر:")
        if not (
            float(before["ema_short"]) < float(before["ema_long"]) and
            float(previous["ema_short"]) < float(previous["ema_long"]) and
            float(latest["ema_short"]) > float(latest["ema_long"])
        ) and (
            bool(latest["supertrend"]) and float(latest["close"]) > float(latest["ema_long"])
        ):
            print("❌ کراس EMA معتبر نیست (برای لانگ)")

        if not (
            float(before["ema_short"]) > float(before["ema_long"]) and
            float(previous["ema_short"]) > float(previous["ema_long"]) and
            float(latest["ema_short"]) < float(latest["ema_long"])
        ) and (
            not bool(latest["supertrend"]) and float(latest["close"]) < float(latest["ema_long"])
        ):
            print("❌ کراس EMA معتبر نیست (برای شورت)")

        if not bool(latest["supertrend"]):
            print("❌ Supertrend حالت صعودی نداره")

        if bool(latest["supertrend"]):
            print("❌ Supertrend حالت نزولی نداره")

        return "none"