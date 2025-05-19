from utils.indicators import supertrend

def generate_signal(df):
    """
    بر اساس SuperTrend بررسی می‌کنه که سیگنال خرید یا فروش هست یا نه.
    """
    df = supertrend(df, period=10, multiplier=3)

    # بررسی آخرین مقدار ستون supertrend
    if df['supertrend'].iloc[-1] == 'LONG':
        return 'long'
    elif df['supertrend'].iloc[-1] == 'SHORT':
        return 'short'
    else:
        return None