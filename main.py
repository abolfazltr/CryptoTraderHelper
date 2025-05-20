import time
from utils.price import get_price_data
from utils.strategy import get_signal
from utils.gmx_v2 import open_position

symbols = ["ETHUSD", "LINKUSDT"]

while True:
    for symbol in symbols:
        print(f"\n⏳ بررسی {symbol}...", flush=True)
        price, df = get_price_data(symbol)

        if not price or df is None or df.empty:
            print(f"⚠️ قیمت برای {symbol} دریافت نشد.", flush=True)
            continue

        print(f"✅ {symbol} از GMX: {price}", flush=True)
        print(f"✅ {symbol} از CoinGecko: {round(df['close'].iloc[-1], 2)}", flush=True)
        print(f"✅ قیمت نهایی {symbol}: {price}", flush=True)

        signal = get_signal(df)

        if signal:
            print(f"📢 سیگنال {symbol}: {signal}", flush=True)
            open_position(symbol, signal)
        else:
            print(f"⛔ هیچ سیگنالی برای {symbol} نیست. (No Signal)", flush=True)

    time.sleep(300)