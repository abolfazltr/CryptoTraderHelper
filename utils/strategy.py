import pandas as pd
import pandas_ta as ta
import numpy as np
from numpy import nan as NaN  # رفع خطای NaN

def generate_signal(prices):
    try:
        df = pd.DataFrame(prices)  # باید شامل لیستی از کندل‌ها باشه

        df['EMA20'] = ta.ema(df['close'], length=20)
        df['EMA50'] = ta.ema(df['close'], length=50)
        df['RSI'] = ta.rsi(df['close'], length=14)

        latest = df.iloc[-1]

        if latest['EMA20'] > latest['EMA50'] and latest['RSI'] < 70:
            return "long"
        elif latest['EMA20'] < latest['EMA50'] and latest['RSI'] > 30:
            return "short"
        else:
            return None

    except Exception as e:
        print("خطا در تحلیل استراتژی:", str(e))
        return None