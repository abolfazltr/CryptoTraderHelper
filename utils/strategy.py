import pandas as pd
from utils.indicators import supertrend, ema

def supertrend_signal(df, period=10, multiplier=2):
    df = supertrend(df, period=period, multiplier=multiplier)
    if df is not None and not df.empty:
        return df['supertrend_direction'].iloc[-1]
    return None

def ema_cross_signal(df, short_window=9, long_window=21):
    df['ema_short'] = ema(df, short_window)
    df['ema_long'] = ema(df, long_window)

    if df['ema_short'].iloc[-2] < df['ema_long'].iloc[-2] and df['ema_short'].iloc[-1] > df['ema_long'].iloc[-1]:
        return "buy"
    elif df['ema_short'].iloc[-2] > df['ema_long'].iloc[-2] and df['ema_short'].iloc[-1] < df['ema_long'].iloc[-1]:
        return "sell"
    else:
        return "none"

def generate_signal(symbol, df):
    print(f"\nآخرین وضعیت برای {symbol}:")

    supertrend_result = supertrend_signal(df)
    print(f"supertrend: {supertrend_result}")

    df['ema_short'] = ema(df, 9)
    df['ema_long'] = ema(df, 21)

    ema_short = df['ema_short'].iloc[-1]
    ema_long = df['ema_long'].iloc[-1]

    print(f"EMA short: {round(ema_short, 2)} | EMA long: {round(ema_long, 2)}")

    if df['ema_short'].iloc[-2] < df['ema_long'].iloc[-2] and ema_short > ema_long:
        print(f"EMA cross condition: {round(df['ema_short'].iloc[-2],2)} → {round(ema_short,2)}")
        ema_result = "buy"
    elif df['ema_short'].iloc[-2] > df['ema_long'].iloc[-2] and ema_short < ema_long:
        print(f"EMA cross condition: {round(df['ema_short'].iloc[-2],2)} → {round(ema_short,2)}")
        ema_result = "sell"
    else:
        print("❌ هیچ شرایط سیگنال EMA برقرار نیست.")
        ema_result = "none"

    if supertrend_result == "buy" and ema_result == "buy":
        print("✅ سیگنال تولید شد: ورود لانگ.")
        return "buy"
    elif supertrend_result == "sell" and ema_result == "sell":
        print("✅ سیگنال تولید شد: ورود شورت.")
        return "sell"
    else:
        print("⛔ هیچ سیگنالی برای ورود وجود ندارد.")
        return None