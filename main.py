import time
from utils.price import get_price_data
from utils.strategy import get_signal
from utils.gmx_v2 import open_position

symbols = ["ETHUSD", "LINKUSDT"]

while True:
    for symbol in symbols:
        print(f"\n⏳ بررسی {symbol}...")
        result = get_price_data(symbol)

        if not result:
            print(f"⚠️ قیمت برای {symbol} دریافت نشد.")
            continue

        price, df = result
        print(f"✅ قیمت نهایی {symbol}: {price}")

        signal = get_signal(df)

        if signal:
            print(f"📢 سیگنال {symbol}: {signal}")
            open_position(symbol, signal)
        else:
            print(f"⛔ هیچ سیگنالی برای {symbol} یافت نشد. (No Signal)")

    time.sleep(300)