import pandas as pd
from utils.indicators import supertrend, ema

def generate_signal(df):
    if df is None or df.empty:
        print("No data received for signal generation.")
        return None

    # محاسبه اندیکاتورها
    df['ema_short'] = ema(df['close'], period=9)
    df['ema_long'] = ema(df['close'], period=21)
    df = supertrend(df, period=10, multiplier=3)

    # چک کردن اینکه همه ستون‌ها وجود دارند
    if 'supertrend' not in df.columns or df['supertrend'].empty:
        print("Supertrend column missing or empty.")
        return None

    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # شرایط پوزیشن لانگ:
    if (
        last_row['supertrend'] == 'LONG' and
        last_row['ema_short'] > last_row['ema_long'] and
        prev_row['ema_short'] <= prev_row['ema_long']
    ):
        return 'buy'

    # شرایط پوزیشن شورت:
    elif (
        last_row['supertrend'] == 'SHORT' and
        last_row['ema_short'] < last_row['ema_long'] and
        prev_row['ema_short'] >= prev_row['ema_long']
    ):
        return 'sell'

    else:
        return None