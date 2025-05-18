import pandas as pd
import numpy as np
npNaN = np.nan
import pandas_ta as ta

def generate_signal():
    # فرض بر اینه که دیتای قیمت رو از جایی بگیری (مثلاً API)
    df = pd.DataFrame()  # اینجا باید دیتا پر بشه

    # اگر دیتا کافی نبود سیگنال نده
    if df.empty or len(df) < 100:
        return None

    # محاسبه EMA
    df["EMA20"] = ta.ema(df["close"], length=20)
    df["EMA50"] = ta.ema(df["close"], length=50)

    # سیگنال گرفتن از تقاطع EMA
    if df["EMA20"].iloc[-1] > df["EMA50"].iloc[-1] and df["EMA20"].iloc[-2] <= df["EMA50"].iloc[-2]:
        return "long"
    elif df["EMA20"].iloc[-1] < df["EMA50"].iloc[-1] and df["EMA20"].iloc[-2] >= df["EMA50"].iloc[-2]:
        return "short"
    else:
        return None