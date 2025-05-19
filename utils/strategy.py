def generate_signal(df):
    if df is None or df.empty:
        print("No data received for signal generation.")
        return None

    df = supertrend(df, period=10, multiplier=3)

    if 'supertrend' not in df.columns or df['supertrend'].empty:
        print("Supertrend column missing or empty.")
        return None

    if df['supertrend'].iloc[-1] == 'LONG':
        return 'long'
    elif df['supertrend'].iloc[-1] == 'SHORT':
        return 'short'
    else:
        return None