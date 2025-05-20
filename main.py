import time
from utils.price import get_price_data
from utils.gmx_v2 import open_position
from utils.strategy import generate_signal

symbols = ["ETHUSDT", "LINKUSDT"]

while True:
    for symbol in symbols:
        print(f"\nبررسی {symbol} ...")

        try:
            df = get_price_data(symbol)
            if df is None or df.empty:
                print(f"⛔ داده‌ای برای {symbol} دریافت نشد.")
                continue

            signal = generate_signal(symbol, df)

            if signal == "buy" or signal == "sell":
                print(f"✅ سیگنال معتبر برای {symbol}: {signal.upper()}")
                open_position(symbol, signal)
            else:
                print(f"❌ هیچ سیگنالی برای {symbol} نیست. (No Signal)")

        except Exception as e:
            print(f"⚠️ خطا در بررسی {symbol}: {str(e)}")

    print("\n⏳ منتظر ۵ دقیقه بعدی ...")
    time.sleep(300)