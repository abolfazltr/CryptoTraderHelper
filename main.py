import time
from utils.price import get_ohlcv
from utils.strategy import generate_signal
from utils.gmx import open_position

print("ربات تریدر با موفقیت اجرا شد...")

while True:
    try:
        # گرفتن کندل‌های ۵ دقیقه‌ای اتریوم از Binance
        df = get_ohlcv(symbol="ETHUSDT", interval="5m")

        # بررسی سیگنال با استراتژی SuperTrend
        signal = generate_signal(df)

        # اگر سیگنال داشت، پوزیشن باز کن
        if signal:
            print(f"سیگنال دریافت شد: {signal}")
            open_position(signal)
        else:
            print("فعلاً سیگنالی نیست.")

    except Exception as e:
        print("خطا در اجرای ربات:", e)

    # صبر ۵ دقیقه‌ای بین بررسی‌ها
    time.sleep(300)