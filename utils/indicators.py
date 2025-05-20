import pandas as pd

def calculate_ema(prices, period):
    """
    محاسبه EMA واقعی با pandas
    """
    return pd.Series(prices).ewm(span=period, adjust=False).mean().tolist()

def calculate_supertrend(prices, period=10, multiplier=2):
    """
    محاسبه Supertrend ساده‌شده فقط بر اساس ترند قیمت بسته‌شده
    """
    df = pd.DataFrame({'close': prices})
    df['trend'] = 'down'
    for i in range(1, len(df)):
        if df['close'][i] > df['close'][i - 1]:
            df.at[i, 'trend'] = 'up'
        else:
            df.at[i, 'trend'] = 'down'
    return df['trend'].tolist()