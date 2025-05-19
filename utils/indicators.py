import pandas as pd

def ema(series, period=14):
    return series.ewm(span=period, adjust=False).mean()

def supertrend(df, period=10, multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    atr = df['high'].rolling(window=period).max() - df['low'].rolling(window=period).min()
    atr = atr.rolling(window=period).mean()

    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)
    supertrend = [True] * len(df)

    for i in range(1, len(df)):
        if df['close'][i] > upperband[i - 1]:
            supertrend[i] = True
        elif df['close'][i] < lowerband[i - 1]:
            supertrend[i] = False
        else:
            supertrend[i] = supertrend[i - 1]
            if supertrend[i] and lowerband[i] < lowerband[i - 1]:
                lowerband[i] = lowerband[i - 1]
            if not supertrend[i] and upperband[i] > upperband[i - 1]:
                upperband[i] = upperband[i - 1]

    trend = ['LONG' if st else 'SHORT' for st in supertrend]
    df['supertrend'] = trend
    return df