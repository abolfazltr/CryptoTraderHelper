import pandas as pd
import numpy as np

def calculate_supertrend(df, period=10, multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    atr = (df['high'] - df['low']).rolling(window=period).mean()

    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    supertrend = [True]

    for i in range(1, len(df)):
        if df['close'][i] > upperband[i - 1]:
            supertrend.append(True)
        elif df['close'][i] < lowerband[i - 1]:
            supertrend.append(False)
        else:
            supertrend.append(supertrend[i - 1])
            if supertrend[i]:
                lowerband[i] = max(lowerband[i], lowerband[i - 1])
            else:
                upperband[i] = min(upperband[i], upperband[i - 1])

    df['supertrend'] = ['buy' if x else 'sell' for x in supertrend]
    return df

def calculate_ema_cross(df, short_period=9, long_period=21):
    df['ema_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long_period, adjust=False).mean()
    df['ema_cross'] = df['ema_short'] > df['ema_long']
    return df

def get_signal(df, return_debug=False):
    df = calculate_supertrend(df, period=10, multiplier=3)
    df = calculate_ema_cross(df)

    supertrend_signal = df['supertrend'].iloc[-1]
    ema_short = df['ema_short'].iloc[-1]
    ema_long = df['ema_long'].iloc[-1]
    ema_signal = df['ema_cross'].iloc[-1]

    signal = None
    if supertrend_signal == 'buy' and ema_signal:
        signal = 'buy'
    elif supertrend_signal == 'sell' and not ema_signal:
        signal = 'sell'

    if return_debug:
        return signal, supertrend_signal, ema_short, ema_long
    return signal