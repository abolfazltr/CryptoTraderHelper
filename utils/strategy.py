import pandas as pd
import pandas_ta as ta
import numpy as np

def generate_signal(prices):
    try:
        df = pd.DataFrame(prices)
        df['EMA20'] = ta.ema(df['close'], length=20)
        df['EMA50'] = ta.ema(df['close'], length=50)
        df['RSI'] = ta.rsi(df['close'], length=14)

        df.dropna(inplace=True)  # خط خیلی مهم برای حذف NaNها

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